#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    Professional Video Downloader Bot                         ║
║                                                                              ║
║  A high-performance, production-grade Telegram bot for downloading           ║
║  videos from 1000+ platforms with enterprise-level features.                 ║
║                                                                              ║
║  Author: Professional Developer                                              ║
║  Version: 2.0.0                                                              ║
║  License: MIT                                                                ║
║  Default Language: Persian (Farsi)                                           ║
║                                                                              ║
║  Features:                                                                   ║
║  • Support for 1000+ video platforms                                         ║
║  • Quality selection up to 4K                                                ║
║  • Cookie-based authentication for private content                           ║
║  • Multi-language support (Persian/English)                                  ║
║  • Real-time progress tracking                                               ║
║  • Admin panel with statistics                                               ║
║  • Rate limiting and VIP system                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

from __future__ import annotations

# ═══════════════════════════════════════════════════════════════════════════════
# STANDARD LIBRARY IMPORTS
# ═══════════════════════════════════════════════════════════════════════════════

import os
import sys
import re
import json
import html
import time
import shutil
import asyncio
import hashlib
import logging
import secrets
import sqlite3
import tempfile
import traceback
from pathlib import Path
from datetime import datetime, timedelta
from typing import (
    Dict, List, Any, Optional, Union, Tuple, 
    Callable, TypeVar, Set, AsyncGenerator
)
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import defaultdict
from contextlib import asynccontextmanager
from concurrent.futures import ThreadPoolExecutor
import base64
import uuid

# ═══════════════════════════════════════════════════════════════════════════════
# THIRD-PARTY IMPORTS
# ═══════════════════════════════════════════════════════════════════════════════

try:
    from pyrogram import Client, filters, enums
    from pyrogram.types import (
        Message, CallbackQuery, InlineKeyboardMarkup, 
        InlineKeyboardButton, InputMediaVideo, InputMediaAudio
    )
    from pyrogram.errors import (
        FloodWait, MessageNotModified, MessageIdInvalid,
        UserIsBlocked, InputUserDeactivated, PeerIdInvalid,
        ChatWriteForbidden, BadRequest
    )
except ImportError:
    print("❌ Pyrogram is not installed. Run: pip install pyrogram tgcrypto")
    sys.exit(1)

try:
    import yt_dlp
except ImportError:
    print("❌ yt-dlp is not installed. Run: pip install yt-dlp")
    sys.exit(1)

try:
    import aiohttp
    import aiofiles
except ImportError:
    print("❌ aiohttp/aiofiles not installed. Run: pip install aiohttp aiofiles")
    sys.exit(1)

try:
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
except ImportError:
    print("❌ cryptography not installed. Run: pip install cryptography")
    sys.exit(1)

try:
    import aiosqlite
except ImportError:
    print("❌ aiosqlite not installed. Run: pip install aiosqlite")
    sys.exit(1)

# ═══════════════════════════════════════════════════════════════════════════════
# LOCAL IMPORTS
# ═══════════════════════════════════════════════════════════════════════════════

from config import (
    load_config, get_config, BotConfig,
    VERSION, CODENAME, BUILD_DATE,
    TEMP_DIR, DOWNLOADS_DIR, COOKIES_DIR, LOGS_DIR, DATABASE_DIR,
    TELEGRAM_FILE_LIMIT, PROGRESS_UPDATE_INTERVAL,
    QUALITY_PRESETS, SUPPORTED_LANGUAGES, DEFAULT_LANGUAGE,
    detect_platform, is_valid_url, format_file_size, format_duration,
    is_admin, is_owner, get_ytdlp_options, get_info_extract_options,
    Platform, DownloadStatus, VideoQuality
)

from languages import (
    get_text, t, get_user_language, set_user_language,
    get_available_languages, is_rtl, load_all_languages
)

from languages.utils import (
    to_persian_digits, format_file_size as format_size_localized,
    format_duration_text, format_speed, escape_html,
    generate_progress_bar, clean_filename, truncate_text
)


# ═══════════════════════════════════════════════════════════════════════════════
# LOGGING SETUP
# ═══════════════════════════════════════════════════════════════════════════════

def setup_logging(config: BotConfig) -> logging.Logger:
    """
    Configure and return the main logger with file and console handlers.
    
    Args:
        config: Bot configuration object
        
    Returns:
        Configured logger instance
    """
    # Create logs directory if not exists
    log_dir = Path(config.logging.log_dir)
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Create logger
    logger = logging.getLogger("VideoDownloaderBot")
    logger.setLevel(getattr(logging, config.logging.level.upper(), logging.INFO))
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # Create formatter
    formatter = logging.Formatter(
        fmt=config.logging.format_string,
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    # Console handler
    if config.logging.log_to_console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        console_handler.setLevel(logging.DEBUG)
        logger.addHandler(console_handler)
    
    # File handler with rotation
    if config.logging.log_to_file:
        from logging.handlers import RotatingFileHandler
        
        file_handler = RotatingFileHandler(
            filename=log_dir / "bot.log",
            maxBytes=config.logging.max_bytes,
            backupCount=config.logging.backup_count,
            encoding="utf-8"
        )
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.DEBUG)
        logger.addHandler(file_handler)
        
        # Error file handler
        error_handler = RotatingFileHandler(
            filename=log_dir / "error.log",
            maxBytes=config.logging.max_bytes,
            backupCount=config.logging.backup_count,
            encoding="utf-8"
        )
        error_handler.setFormatter(formatter)
        error_handler.setLevel(logging.ERROR)
        logger.addHandler(error_handler)
    
    return logger


# Initialize configuration and logger
config = get_config()
logger = setup_logging(config)

# Log startup info
logger.info("=" * 60)
logger.info(f"🎬 Video Downloader Bot v{VERSION} ({CODENAME})")
logger.info(f"📅 Build Date: {BUILD_DATE}")
logger.info(f"🌐 Default Language: {DEFAULT_LANGUAGE}")
logger.info("=" * 60)


# ═══════════════════════════════════════════════════════════════════════════════
# TYPE DEFINITIONS
# ═══════════════════════════════════════════════════════════════════════════════

T = TypeVar('T')
MessageHandler = Callable[[Client, Message], Any]
CallbackHandler = Callable[[Client, CallbackQuery], Any]


# ═══════════════════════════════════════════════════════════════════════════════
# DATA CLASSES
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class VideoInfo:
    """Represents extracted video information."""
    url: str
    title: str
    duration: int = 0
    uploader: str = ""
    view_count: int = 0
    like_count: int = 0
    description: str = ""
    thumbnail: str = ""
    upload_date: str = ""
    platform: Platform = Platform.UNKNOWN
    formats: List[Dict[str, Any]] = field(default_factory=list)
    is_live: bool = False
    is_private: bool = False
    age_restricted: bool = False
    extractor: str = ""
    webpage_url: str = ""
    
    @property
    def duration_formatted(self) -> str:
        """Get formatted duration string."""
        return format_duration(self.duration) if self.duration else "N/A"
    
    @property
    def views_formatted(self) -> str:
        """Get formatted view count."""
        if self.view_count:
            if self.view_count >= 1_000_000:
                return f"{self.view_count / 1_000_000:.1f}M"
            elif self.view_count >= 1_000:
                return f"{self.view_count / 1_000:.1f}K"
            return str(self.view_count)
        return "N/A"


@dataclass
class FormatInfo:
    """Represents a video/audio format option."""
    format_id: str
    ext: str
    quality: str
    height: int = 0
    width: int = 0
    fps: int = 0
    filesize: int = 0
    vcodec: str = ""
    acodec: str = ""
    abr: int = 0
    vbr: int = 0
    is_audio_only: bool = False
    format_note: str = ""
    
    @property
    def resolution(self) -> str:
        """Get resolution string."""
        if self.height and self.width:
            return f"{self.width}x{self.height}"
        elif self.height:
            return f"{self.height}p"
        return self.quality
    
    @property
    def size_formatted(self) -> str:
        """Get formatted file size."""
        return format_file_size(self.filesize) if self.filesize else "Unknown"


@dataclass
class DownloadTask:
    """Represents an active download task."""
    task_id: str
    user_id: int
    chat_id: int
    message_id: int
    url: str
    video_info: Optional[VideoInfo] = None
    selected_format: Optional[FormatInfo] = None
    status: DownloadStatus = DownloadStatus.PENDING
    progress: float = 0.0
    downloaded_bytes: int = 0
    total_bytes: int = 0
    speed: float = 0.0
    eta: int = 0
    file_path: Optional[Path] = None
    error_message: str = ""
    started_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    cancelled: bool = False
    
    @property
    def elapsed_time(self) -> float:
        """Get elapsed time in seconds."""
        end_time = self.completed_at or datetime.now()
        return (end_time - self.started_at).total_seconds()


@dataclass
class UserData:
    """Represents user data and preferences."""
    user_id: int
    username: str = ""
    first_name: str = ""
    last_name: str = ""
    language: str = DEFAULT_LANGUAGE
    default_quality: str = "1080"
    is_vip: bool = False
    vip_expiry: Optional[datetime] = None
    is_banned: bool = False
    ban_reason: str = ""
    total_downloads: int = 0
    successful_downloads: int = 0
    failed_downloads: int = 0
    total_size: int = 0
    created_at: datetime = field(default_factory=datetime.now)
    last_active: datetime = field(default_factory=datetime.now)
    daily_downloads: int = 0
    daily_reset: datetime = field(default_factory=datetime.now)
    
    @property
    def full_name(self) -> str:
        """Get user's full name."""
        if self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.first_name or self.username or str(self.user_id)
    
    @property
    def success_rate(self) -> float:
        """Get download success rate percentage."""
        if self.total_downloads == 0:
            return 0.0
        return (self.successful_downloads / self.total_downloads) * 100


# ═══════════════════════════════════════════════════════════════════════════════
# GLOBAL STATE MANAGEMENT
# ═══════════════════════════════════════════════════════════════════════════════

class BotState:
    """
    Manages global bot state including active downloads, user data, and caches.
    Thread-safe implementation with proper locking.
    """
    
    def __init__(self):
        self._lock = asyncio.Lock()
        self._downloads: Dict[str, DownloadTask] = {}
        self._user_downloads: Dict[int, Set[str]] = defaultdict(set)
        self._user_data: Dict[int, UserData] = {}
        self._cache: Dict[str, Tuple[Any, float]] = {}
        self._rate_limits: Dict[int, List[float]] = defaultdict(list)
        self._start_time = datetime.now()
        self._total_downloads = 0
        self._successful_downloads = 0
        self._failed_downloads = 0
    
    @property
    def uptime(self) -> timedelta:
        """Get bot uptime."""
        return datetime.now() - self._start_time
    
    @property
    def uptime_formatted(self) -> str:
        """Get formatted uptime string."""
        uptime = self.uptime
        days = uptime.days
        hours, remainder = divmod(uptime.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        parts = []
        if days:
            parts.append(f"{days}d")
        if hours:
            parts.append(f"{hours}h")
        if minutes:
            parts.append(f"{minutes}m")
        if seconds or not parts:
            parts.append(f"{seconds}s")
        
        return " ".join(parts)
    
    async def add_download(self, task: DownloadTask) -> None:
        """Add a new download task."""
        async with self._lock:
            self._downloads[task.task_id] = task
            self._user_downloads[task.user_id].add(task.task_id)
    
    async def get_download(self, task_id: str) -> Optional[DownloadTask]:
        """Get a download task by ID."""
        return self._downloads.get(task_id)
    
    async def remove_download(self, task_id: str) -> None:
        """Remove a download task."""
        async with self._lock:
            if task_id in self._downloads:
                task = self._downloads[task_id]
                self._user_downloads[task.user_id].discard(task_id)
                del self._downloads[task_id]
    
    async def get_user_download_count(self, user_id: int) -> int:
        """Get number of active downloads for a user."""
        return len(self._user_downloads.get(user_id, set()))
    
    async def get_user_downloads(self, user_id: int) -> List[DownloadTask]:
        """Get all active downloads for a user."""
        task_ids = self._user_downloads.get(user_id, set())
        return [self._downloads[tid] for tid in task_ids if tid in self._downloads]
    
    async def cancel_user_downloads(self, user_id: int) -> int:
        """Cancel all downloads for a user. Returns count of cancelled."""
        async with self._lock:
            task_ids = list(self._user_downloads.get(user_id, set()))
            cancelled = 0
            for task_id in task_ids:
                if task_id in self._downloads:
                    self._downloads[task_id].cancelled = True
                    cancelled += 1
            return cancelled
    
    def get_global_download_count(self) -> int:
        """Get total number of active downloads."""
        return len(self._downloads)
    
    async def get_cached(self, key: str, ttl: int = 300) -> Optional[Any]:
        """Get cached value if not expired."""
        if key in self._cache:
            value, timestamp = self._cache[key]
            if time.time() - timestamp < ttl:
                return value
            del self._cache[key]
        return None
    
    async def set_cached(self, key: str, value: Any) -> None:
        """Set cached value with current timestamp."""
        async with self._lock:
            self._cache[key] = (value, time.time())
    
    async def check_rate_limit(self, user_id: int, limit: int, window: int = 86400) -> Tuple[bool, int]:
        """
        Check if user has exceeded rate limit.
        
        Returns:
            Tuple of (is_allowed, remaining_count)
        """
        current_time = time.time()
        cutoff_time = current_time - window
        
        async with self._lock:
            # Clean old entries
            self._rate_limits[user_id] = [
                ts for ts in self._rate_limits[user_id] 
                if ts > cutoff_time
            ]
            
            current_count = len(self._rate_limits[user_id])
            remaining = limit - current_count
            
            if current_count < limit:
                self._rate_limits[user_id].append(current_time)
                return True, remaining - 1
            
            return False, 0
    
    async def increment_stats(self, success: bool = True) -> None:
        """Increment download statistics."""
        async with self._lock:
            self._total_downloads += 1
            if success:
                self._successful_downloads += 1
            else:
                self._failed_downloads += 1
    
    def get_stats(self) -> Dict[str, Any]:
        """Get bot statistics."""
        return {
            "uptime": self.uptime_formatted,
            "total_downloads": self._total_downloads,
            "successful_downloads": self._successful_downloads,
            "failed_downloads": self._failed_downloads,
            "active_downloads": len(self._downloads),
            "cached_items": len(self._cache),
            "success_rate": (
                f"{(self._successful_downloads / self._total_downloads * 100):.1f}%"
                if self._total_downloads > 0 else "N/A"
            )
        }


# Initialize global state
bot_state = BotState()


# ═══════════════════════════════════════════════════════════════════════════════
# DATABASE MANAGER
# ═══════════════════════════════════════════════════════════════════════════════

class DatabaseManager:
    """
    Async database manager for SQLite with connection pooling.
    Handles user data, download history, and statistics.
    """
    
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self._pool: List[aiosqlite.Connection] = []
        self._pool_size = 5
        self._lock = asyncio.Lock()
        self._initialized = False
    
    async def initialize(self) -> None:
        """Initialize database and create tables."""
        if self._initialized:
            return
        
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        async with aiosqlite.connect(self.db_path) as db:
            await db.executescript("""
                -- Users table
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    first_name TEXT,
                    last_name TEXT,
                    language TEXT DEFAULT 'fa',
                    default_quality TEXT DEFAULT '1080',
                    is_vip INTEGER DEFAULT 0,
                    vip_expiry TEXT,
                    is_banned INTEGER DEFAULT 0,
                    ban_reason TEXT,
                    total_downloads INTEGER DEFAULT 0,
                    successful_downloads INTEGER DEFAULT 0,
                    failed_downloads INTEGER DEFAULT 0,
                    total_size INTEGER DEFAULT 0,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    last_active TEXT DEFAULT CURRENT_TIMESTAMP,
                    daily_downloads INTEGER DEFAULT 0,
                    daily_reset TEXT DEFAULT CURRENT_TIMESTAMP
                );
                
                -- Download history table
                CREATE TABLE IF NOT EXISTS downloads (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    url TEXT,
                    title TEXT,
                    platform TEXT,
                    quality TEXT,
                    file_size INTEGER,
                    duration INTEGER,
                    status TEXT,
                    error_message TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    completed_at TEXT,
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                );
                
                -- Cookies table
                CREATE TABLE IF NOT EXISTS cookies (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    platform TEXT,
                    cookie_data TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    expires_at TEXT,
                    is_valid INTEGER DEFAULT 1,
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                );
                
                -- Statistics table
                CREATE TABLE IF NOT EXISTS statistics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT UNIQUE,
                    total_downloads INTEGER DEFAULT 0,
                    successful_downloads INTEGER DEFAULT 0,
                    failed_downloads INTEGER DEFAULT 0,
                    unique_users INTEGER DEFAULT 0,
                    total_size INTEGER DEFAULT 0,
                    top_platform TEXT
                );
                
                -- Create indexes
                CREATE INDEX IF NOT EXISTS idx_downloads_user ON downloads(user_id);
                CREATE INDEX IF NOT EXISTS idx_downloads_date ON downloads(created_at);
                CREATE INDEX IF NOT EXISTS idx_cookies_user ON cookies(user_id);
                CREATE INDEX IF NOT EXISTS idx_cookies_platform ON cookies(platform);
            """)
            await db.commit()
        
        self._initialized = True
        logger.info("✅ Database initialized successfully")
    
    @asynccontextmanager
    async def get_connection(self) -> AsyncGenerator[aiosqlite.Connection, None]:
        """Get a database connection from pool."""
        async with self._lock:
            if self._pool:
                conn = self._pool.pop()
            else:
                conn = await aiosqlite.connect(self.db_path)
                conn.row_factory = aiosqlite.Row
        
        try:
            yield conn
        finally:
            async with self._lock:
                if len(self._pool) < self._pool_size:
                    self._pool.append(conn)
                else:
                    await conn.close()
    
    async def get_user(self, user_id: int) -> Optional[UserData]:
        """Get user data by ID."""
        async with self.get_connection() as db:
            async with db.execute(
                "SELECT * FROM users WHERE user_id = ?", (user_id,)
            ) as cursor:
                row = await cursor.fetchone()
                if row:
                    return UserData(
                        user_id=row["user_id"],
                        username=row["username"] or "",
                        first_name=row["first_name"] or "",
                        last_name=row["last_name"] or "",
                        language=row["language"],
                        default_quality=row["default_quality"],
                        is_vip=bool(row["is_vip"]),
                        vip_expiry=datetime.fromisoformat(row["vip_expiry"]) if row["vip_expiry"] else None,
                        is_banned=bool(row["is_banned"]),
                        ban_reason=row["ban_reason"] or "",
                        total_downloads=row["total_downloads"],
                        successful_downloads=row["successful_downloads"],
                        failed_downloads=row["failed_downloads"],
                        total_size=row["total_size"],
                        created_at=datetime.fromisoformat(row["created_at"]),
                        last_active=datetime.fromisoformat(row["last_active"]),
                        daily_downloads=row["daily_downloads"],
                        daily_reset=datetime.fromisoformat(row["daily_reset"])
                    )
        return None
    
    async def create_or_update_user(self, user_id: int, **kwargs) -> UserData:
        """Create or update user data."""
        existing = await self.get_user(user_id)
        
        async with self.get_connection() as db:
            if existing:
                # Update existing user
                set_clauses = []
                values = []
                for key, value in kwargs.items():
                    set_clauses.append(f"{key} = ?")
                    if isinstance(value, datetime):
                        values.append(value.isoformat())
                    else:
                        values.append(value)
                
                set_clauses.append("last_active = ?")
                values.append(datetime.now().isoformat())
                values.append(user_id)
                
                await db.execute(
                    f"UPDATE users SET {', '.join(set_clauses)} WHERE user_id = ?",
                    values
                )
            else:
                # Create new user
                columns = ["user_id"] + list(kwargs.keys())
                placeholders = ["?"] * len(columns)
                values = [user_id]
                for value in kwargs.values():
                    if isinstance(value, datetime):
                        values.append(value.isoformat())
                    else:
                        values.append(value)
                
                await db.execute(
                    f"INSERT INTO users ({', '.join(columns)}) VALUES ({', '.join(placeholders)})",
                    values
                )
            
            await db.commit()
        
        return await self.get_user(user_id)
    
    async def increment_download_count(
        self, 
        user_id: int, 
        success: bool = True, 
        size: int = 0
    ) -> None:
        """Increment user's download count."""
        async with self.get_connection() as db:
            if success:
                await db.execute("""
                    UPDATE users SET 
                        total_downloads = total_downloads + 1,
                        successful_downloads = successful_downloads + 1,
                        total_size = total_size + ?,
                        daily_downloads = daily_downloads + 1,
                        last_active = ?
                    WHERE user_id = ?
                """, (size, datetime.now().isoformat(), user_id))
            else:
                await db.execute("""
                    UPDATE users SET 
                        total_downloads = total_downloads + 1,
                        failed_downloads = failed_downloads + 1,
                        daily_downloads = daily_downloads + 1,
                        last_active = ?
                    WHERE user_id = ?
                """, (datetime.now().isoformat(), user_id))
            
            await db.commit()
    
    async def add_download_history(
        self,
        user_id: int,
        url: str,
        title: str,
        platform: str,
        quality: str,
        file_size: int,
        duration: int,
        status: str,
        error_message: str = ""
    ) -> None:
        """Add download to history."""
        async with self.get_connection() as db:
            await db.execute("""
                INSERT INTO downloads 
                (user_id, url, title, platform, quality, file_size, duration, status, error_message, completed_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                user_id, url, title, platform, quality, file_size, 
                duration, status, error_message, datetime.now().isoformat()
            ))
            await db.commit()
    
    async def get_download_history(
        self, 
        user_id: int, 
        limit: int = 50, 
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """Get user's download history."""
        async with self.get_connection() as db:
            async with db.execute("""
                SELECT * FROM downloads 
                WHERE user_id = ? 
                ORDER BY created_at DESC 
                LIMIT ? OFFSET ?
            """, (user_id, limit, offset)) as cursor:
                rows = await cursor.fetchall()
                return [dict(row) for row in rows]
    
    async def save_cookie(
        self, 
        user_id: int, 
        platform: str, 
        cookie_data: str,
        expires_at: Optional[datetime] = None
    ) -> None:
        """Save encrypted cookie for user."""
        async with self.get_connection() as db:
            # Remove existing cookie for this platform
            await db.execute(
                "DELETE FROM cookies WHERE user_id = ? AND platform = ?",
                (user_id, platform)
            )
            
            # Insert new cookie
            await db.execute("""
                INSERT INTO cookies (user_id, platform, cookie_data, expires_at)
                VALUES (?, ?, ?, ?)
            """, (
                user_id, platform, cookie_data,
                expires_at.isoformat() if expires_at else None
            ))
            await db.commit()
    
    async def get_cookie(self, user_id: int, platform: str) -> Optional[str]:
        """Get cookie for user and platform."""
        async with self.get_connection() as db:
            async with db.execute("""
                SELECT cookie_data FROM cookies 
                WHERE user_id = ? AND platform = ? AND is_valid = 1
            """, (user_id, platform)) as cursor:
                row = await cursor.fetchone()
                return row["cookie_data"] if row else None
    
    async def get_all_cookies(self, user_id: int) -> List[Dict[str, Any]]:
        """Get all cookies for user."""
        async with self.get_connection() as db:
            async with db.execute("""
                SELECT platform, created_at, expires_at, is_valid 
                FROM cookies WHERE user_id = ?
            """, (user_id,)) as cursor:
                rows = await cursor.fetchall()
                return [dict(row) for row in rows]
    
    async def delete_cookie(self, user_id: int, platform: str) -> bool:
        """Delete cookie for user and platform."""
        async with self.get_connection() as db:
            cursor = await db.execute(
                "DELETE FROM cookies WHERE user_id = ? AND platform = ?",
                (user_id, platform)
            )
            await db.commit()
            return cursor.rowcount > 0
    
    async def get_total_users(self) -> int:
        """Get total number of users."""
        async with self.get_connection() as db:
            async with db.execute("SELECT COUNT(*) FROM users") as cursor:
                row = await cursor.fetchone()
                return row[0] if row else 0
    
    async def get_active_users(self, hours: int = 24) -> int:
        """Get number of active users in last N hours."""
        cutoff = (datetime.now() - timedelta(hours=hours)).isoformat()
        async with self.get_connection() as db:
            async with db.execute(
                "SELECT COUNT(*) FROM users WHERE last_active > ?", (cutoff,)
            ) as cursor:
                row = await cursor.fetchone()
                return row[0] if row else 0
    
    async def get_vip_users(self) -> int:
        """Get number of VIP users."""
        async with self.get_connection() as db:
            async with db.execute(
                "SELECT COUNT(*) FROM users WHERE is_vip = 1"
            ) as cursor:
                row = await cursor.fetchone()
                return row[0] if row else 0
    
    async def get_banned_users(self) -> int:
        """Get number of banned users."""
        async with self.get_connection() as db:
            async with db.execute(
                "SELECT COUNT(*) FROM users WHERE is_banned = 1"
            ) as cursor:
                row = await cursor.fetchone()
                return row[0] if row else 0
    
    async def get_all_user_ids(self) -> List[int]:
        """Get all user IDs for broadcasting."""
        async with self.get_connection() as db:
            async with db.execute(
                "SELECT user_id FROM users WHERE is_banned = 0"
            ) as cursor:
                rows = await cursor.fetchall()
                return [row[0] for row in rows]
    
    async def close(self) -> None:
        """Close all connections in pool."""
        async with self._lock:
            for conn in self._pool:
                await conn.close()
            self._pool.clear()


# Initialize database
db = DatabaseManager(DATABASE_DIR / "bot.db")


# ═══════════════════════════════════════════════════════════════════════════════
# ENCRYPTION HELPERS
# ═══════════════════════════════════════════════════════════════════════════════

class CookieEncryption:
    """
    Handles secure encryption/decryption of cookies using Fernet (AES-128).
    """
    
    def __init__(self, encryption_key: Optional[str] = None):
        """
        Initialize encryption with a key.
        
        Args:
            encryption_key: Base64-encoded 32-byte key or None to generate
        """
        if encryption_key:
            # Use provided key
            key_bytes = base64.urlsafe_b64decode(encryption_key)
        else:
            # Generate a key from a password
            password = secrets.token_bytes(32)
            salt = secrets.token_bytes(16)
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
            )
            key_bytes = kdf.derive(password)
        
        self._fernet = Fernet(base64.urlsafe_b64encode(key_bytes[:32]))
    
    def encrypt(self, data: str) -> str:
        """
        Encrypt a string.
        
        Args:
            data: Plain text to encrypt
            
        Returns:
            Base64-encoded encrypted string
        """
        encrypted = self._fernet.encrypt(data.encode('utf-8'))
        return base64.urlsafe_b64encode(encrypted).decode('utf-8')
    
    def decrypt(self, encrypted_data: str) -> str:
        """
        Decrypt an encrypted string.
        
        Args:
            encrypted_data: Base64-encoded encrypted string
            
        Returns:
            Decrypted plain text
        """
        encrypted_bytes = base64.urlsafe_b64decode(encrypted_data)
        decrypted = self._fernet.decrypt(encrypted_bytes)
        return decrypted.decode('utf-8')


# Initialize encryption
cookie_encryption = CookieEncryption(config.security.encryption_key)


# ═══════════════════════════════════════════════════════════════════════════════
# PROGRESS TRACKER
# ═══════════════════════════════════════════════════════════════════════════════

class ProgressTracker:
    """
    Tracks download progress and handles Telegram message updates.
    Implements debouncing to avoid flood wait errors.
    """
    
    def __init__(
        self,
        client: Client,
        chat_id: int,
        message_id: int,
        user_id: int,
        task_id: str,
        lang_code: str = DEFAULT_LANGUAGE
    ):
        self.client = client
        self.chat_id = chat_id
        self.message_id = message_id
        self.user_id = user_id
        self.task_id = task_id
        self.lang_code = lang_code
        
        self._last_update = 0.0
        self._update_interval = PROGRESS_UPDATE_INTERVAL
        self._last_text = ""
        self._lock = asyncio.Lock()
        
        # Progress data
        self.status = DownloadStatus.PENDING
        self.progress = 0.0
        self.downloaded_bytes = 0
        self.total_bytes = 0
        self.speed = 0.0
        self.eta = 0
        self.quality = ""
        self.filename = ""
    
    def _format_progress_message(self) -> str:
        """Generate formatted progress message."""
        # Progress bar
        progress_bar = generate_progress_bar(
            self.progress / 100 if self.progress <= 100 else 1.0,
            length=20,
            lang_code=self.lang_code
        )
        
        # Format values based on language
        if self.lang_code == "fa":
            percentage = to_persian_digits(f"{self.progress:.1f}%")
            downloaded = format_size_localized(self.downloaded_bytes, "fa")
            total = format_size_localized(self.total_bytes, "fa") if self.total_bytes else "نامشخص"
            speed = format_speed(self.speed, "fa")
            eta_text = format_duration_text(self.eta, "fa", short=True) if self.eta else "نامشخص"
        else:
            percentage = f"{self.progress:.1f}%"
            downloaded = format_file_size(self.downloaded_bytes)
            total = format_file_size(self.total_bytes) if self.total_bytes else "Unknown"
            speed = format_speed(self.speed, "en")
            eta_text = format_duration_text(self.eta, "en", short=True) if self.eta else "Unknown"
        
        # Get status-specific message
        if self.status == DownloadStatus.DOWNLOADING:
            status_key = "download.progress"
        elif self.status == DownloadStatus.MERGING:
            return get_text("download.merging", lang_code=self.lang_code)
        elif self.status == DownloadStatus.UPLOADING:
            status_key = "download.uploading"
        else:
            return get_text("common.processing", lang_code=self.lang_code)
        
        return get_text(
            status_key,
            lang_code=self.lang_code,
            progress_bar=progress_bar,
            percentage=percentage,
            downloaded=downloaded,
            uploaded=downloaded,  # For upload progress
            total=total,
            speed=speed,
            eta=eta_text,
            quality=self.quality or "N/A"
        )
    
    async def update(
        self,
        status: Optional[DownloadStatus] = None,
        progress: Optional[float] = None,
        downloaded_bytes: Optional[int] = None,
        total_bytes: Optional[int] = None,
        speed: Optional[float] = None,
        eta: Optional[int] = None,
        force: bool = False
    ) -> None:
        """
        Update progress and optionally update Telegram message.
        
        Args:
            status: Current download status
            progress: Progress percentage (0-100)
            downloaded_bytes: Bytes downloaded so far
            total_bytes: Total bytes to download
            speed: Download speed in bytes/second
            eta: Estimated time remaining in seconds
            force: Force update even if within debounce interval
        """
        async with self._lock:
            # Update values if provided
            if status is not None:
                self.status = status
            if progress is not None:
                self.progress = progress
            if downloaded_bytes is not None:
                self.downloaded_bytes = downloaded_bytes
            if total_bytes is not None:
                self.total_bytes = total_bytes
            if speed is not None:
                self.speed = speed
            if eta is not None:
                self.eta = eta
            
            # Check if we should update the message
            current_time = time.time()
            if not force and current_time - self._last_update < self._update_interval:
                return
            
            # Generate new message text
            new_text = self._format_progress_message()
            
            # Skip if message hasn't changed
            if new_text == self._last_text:
                return
            
            # Update the message
            try:
                await self.client.edit_message_text(
                    chat_id=self.chat_id,
                    message_id=self.message_id,
                    text=new_text,
                    parse_mode=enums.ParseMode.HTML
                )
                self._last_text = new_text
                self._last_update = current_time
                
            except MessageNotModified:
                pass
            except FloodWait as e:
                logger.warning(f"FloodWait: sleeping for {e.value} seconds")
                await asyncio.sleep(e.value)
            except Exception as e:
                logger.error(f"Error updating progress message: {e}")
    
    async def set_status(self, status: DownloadStatus, force: bool = True) -> None:
        """Update status and force message update."""
        await self.update(status=status, force=force)
    
    async def complete(self, text: str) -> None:
        """Set completion message."""
        try:
            await self.client.edit_message_text(
                chat_id=self.chat_id,
                message_id=self.message_id,
                text=text,
                parse_mode=enums.ParseMode.HTML
            )
        except Exception as e:
            logger.error(f"Error setting completion message: {e}")


class YTDLPProgressHook:
    """
    Progress hook for yt-dlp that updates ProgressTracker.
    """
    
    def __init__(self, tracker: ProgressTracker, loop: asyncio.AbstractEventLoop):
        self.tracker = tracker
        self.loop = loop
        self._last_status = None
    
    def __call__(self, d: Dict[str, Any]) -> None:
        """Handle progress callback from yt-dlp."""
        status = d.get('status')
        
        if status == 'downloading':
            # Extract progress data
            downloaded = d.get('downloaded_bytes', 0)
            total = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
            speed = d.get('speed', 0) or 0
            eta = d.get('eta', 0) or 0
            
            # Calculate progress percentage
            if total > 0:
                progress = (downloaded / total) * 100
            else:
                progress = 0
            
            # Schedule async update
            asyncio.run_coroutine_threadsafe(
                self.tracker.update(
                    status=DownloadStatus.DOWNLOADING,
                    progress=progress,
                    downloaded_bytes=downloaded,
                    total_bytes=total,
                    speed=speed,
                    eta=eta
                ),
                self.loop
            )
        
        elif status == 'finished':
            # Download finished, might need to merge
            asyncio.run_coroutine_threadsafe(
                self.tracker.update(
                    status=DownloadStatus.MERGING,
                    progress=100,
                    force=True
                ),
                self.loop
            )
        
        elif status == 'error':
            logger.error(f"yt-dlp error: {d.get('error', 'Unknown error')}")


# ═══════════════════════════════════════════════════════════════════════════════
# VIDEO INFO EXTRACTION
# ═══════════════════════════════════════════════════════════════════════════════

async def extract_video_info(
    url: str,
    user_id: Optional[int] = None,
    use_cookies: bool = True
) -> Optional[VideoInfo]:
    """
    Extract video information using yt-dlp.
    
    Args:
        url: Video URL
        user_id: User ID for cookie lookup
        use_cookies: Whether to use saved cookies
        
    Returns:
        VideoInfo object or None if extraction failed
    """
    # Check cache first
    cache_key = f"video_info:{hashlib.md5(url.encode()).hexdigest()}"
    cached = await bot_state.get_cached(cache_key, ttl=300)
    if cached:
        logger.debug(f"Using cached video info for {url}")
        return cached
    
    # Prepare cookie file if available
    cookie_file = None
    if use_cookies and user_id:
        platform = detect_platform(url)
        if platform != Platform.UNKNOWN:
            cookie_data = await db.get_cookie(user_id, platform.value)
            if cookie_data:
                try:
                    decrypted = cookie_encryption.decrypt(cookie_data)
                    cookie_file = COOKIES_DIR / f"temp_{user_id}_{platform.value}.txt"
                    async with aiofiles.open(cookie_file, 'w') as f:
                        await f.write(decrypted)
                except Exception as e:
                    logger.error(f"Error decrypting cookie: {e}")
    
    # Get yt-dlp options
    ydl_opts = get_info_extract_options(config, cookie_file)
    
    try:
        # Run extraction in thread pool
        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor() as executor:
            info = await loop.run_in_executor(
                executor,
                lambda: _extract_info_sync(url, ydl_opts)
            )
        
        if not info:
            return None
        
        # Parse formats
        formats = []
        for fmt in info.get('formats', []):
            if fmt.get('format_id'):
                format_info = FormatInfo(
                    format_id=fmt.get('format_id', ''),
                    ext=fmt.get('ext', 'mp4'),
                    quality=fmt.get('format_note', '') or fmt.get('quality', ''),
                    height=fmt.get('height', 0) or 0,
                    width=fmt.get('width', 0) or 0,
                    fps=fmt.get('fps', 0) or 0,
                    filesize=fmt.get('filesize', 0) or fmt.get('filesize_approx', 0) or 0,
                    vcodec=fmt.get('vcodec', ''),
                    acodec=fmt.get('acodec', ''),
                    abr=fmt.get('abr', 0) or 0,
                    vbr=fmt.get('vbr', 0) or 0,
                    is_audio_only=fmt.get('vcodec') == 'none',
                    format_note=fmt.get('format_note', '')
                )
                formats.append(format_info.__dict__)
        
        # Detect platform
        platform = detect_platform(url)
        
        # Create VideoInfo object
        video_info = VideoInfo(
            url=url,
            title=info.get('title', 'Unknown'),
            duration=info.get('duration', 0) or 0,
            uploader=info.get('uploader', '') or info.get('channel', '') or '',
            view_count=info.get('view_count', 0) or 0,
            like_count=info.get('like_count', 0) or 0,
            description=info.get('description', '') or '',
            thumbnail=info.get('thumbnail', '') or '',
            upload_date=info.get('upload_date', '') or '',
            platform=platform,
            formats=formats,
            is_live=info.get('is_live', False),
            is_private=info.get('is_private', False),
            age_restricted=info.get('age_limit', 0) > 0,
            extractor=info.get('extractor', ''),
            webpage_url=info.get('webpage_url', url)
        )
        
        # Cache the result
        await bot_state.set_cached(cache_key, video_info)
        
        return video_info
        
    except Exception as e:
        logger.error(f"Error extracting video info: {e}")
        return None
    
    finally:
        # Clean up temp cookie file
        if cookie_file and cookie_file.exists():
            try:
                cookie_file.unlink()
            except:
                pass


def _extract_info_sync(url: str, ydl_opts: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Synchronous wrapper for yt-dlp extraction."""
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            return ydl.extract_info(url, download=False)
    except yt_dlp.utils.DownloadError as e:
        logger.error(f"yt-dlp download error: {e}")
        return None
    except Exception as e:
        logger.error(f"yt-dlp error: {e}")
        return None


# ═══════════════════════════════════════════════════════════════════════════════
# VIDEO DOWNLOAD FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

async def download_video(
    url: str,
    output_path: Path,
    quality: str = "1080",
    user_id: Optional[int] = None,
    progress_tracker: Optional[ProgressTracker] = None,
    audio_only: bool = False
) -> Tuple[bool, Optional[Path], str]:
    """
    Download video using yt-dlp.
    
    Args:
        url: Video URL
        output_path: Path to save the video
        quality: Quality setting
        user_id: User ID for cookies
        progress_tracker: Progress tracking object
        audio_only: Download audio only
        
    Returns:
        Tuple of (success, file_path, error_message)
    """
    # Prepare cookie file
    cookie_file = None
    if user_id:
        platform = detect_platform(url)
        if platform != Platform.UNKNOWN:
            cookie_data = await db.get_cookie(user_id, platform.value)
            if cookie_data:
                try:
                    decrypted = cookie_encryption.decrypt(cookie_data)
                    cookie_file = COOKIES_DIR / f"temp_{user_id}_{platform.value}.txt"
                    async with aiofiles.open(cookie_file, 'w') as f:
                        await f.write(decrypted)
                except Exception as e:
                    logger.error(f"Error decrypting cookie: {e}")
    
    # Set up progress hook
    loop = asyncio.get_event_loop()
    progress_hook = None
    if progress_tracker:
        progress_hook = YTDLPProgressHook(progress_tracker, loop)
    
    # Get yt-dlp options
    ydl_opts = get_ytdlp_options(
        config,
        quality=quality,
        audio_only=audio_only,
        output_path=output_path,
        cookie_file=cookie_file,
        progress_hook=progress_hook
    )
    
    try:
        # Run download in thread pool
        with ThreadPoolExecutor() as executor:
            result = await loop.run_in_executor(
                executor,
                lambda: _download_sync(url, ydl_opts)
            )
        
        if result['success']:
            # Find the downloaded file
            downloaded_file = result.get('filename')
            if downloaded_file and Path(downloaded_file).exists():
                return True, Path(downloaded_file), ""
            
            # Try to find the file by pattern
            for ext in ['mp4', 'mkv', 'webm', 'mp3', 'm4a']:
                pattern = output_path.parent / f"*{output_path.stem}*.{ext}"
                files = list(output_path.parent.glob(f"*{output_path.stem}*.{ext}"))
                if files:
                    return True, files[0], ""
            
            return False, None, "Downloaded file not found"
        else:
            return False, None, result.get('error', 'Download failed')
            
    except Exception as e:
        logger.error(f"Download error: {e}")
        return False, None, str(e)
    
    finally:
        # Clean up temp cookie file
        if cookie_file and cookie_file.exists():
            try:
                cookie_file.unlink()
            except:
                pass


def _download_sync(url: str, ydl_opts: Dict[str, Any]) -> Dict[str, Any]:
    """Synchronous wrapper for yt-dlp download."""
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            if info:
                filename = ydl.prepare_filename(info)
                # Handle merged output
                if ydl_opts.get('merge_output_format'):
                    base, _ = os.path.splitext(filename)
                    filename = f"{base}.{ydl_opts['merge_output_format']}"
                return {'success': True, 'filename': filename, 'info': info}
            return {'success': False, 'error': 'No info returned'}
    except yt_dlp.utils.DownloadError as e:
        error_msg = str(e)
        if 'Private video' in error_msg:
            return {'success': False, 'error': 'private_video'}
        elif 'Sign in' in error_msg:
            return {'success': False, 'error': 'login_required'}
        elif 'age' in error_msg.lower():
            return {'success': False, 'error': 'age_restricted'}
        elif 'geo' in error_msg.lower() or 'country' in error_msg.lower():
            return {'success': False, 'error': 'geo_restricted'}
        return {'success': False, 'error': error_msg}
    except Exception as e:
        return {'success': False, 'error': str(e)}


async def download_direct_link(
    url: str,
    output_path: Path,
    progress_tracker: Optional[ProgressTracker] = None
) -> Tuple[bool, Optional[Path], str]:
    """
    Download file from direct URL using aiohttp.
    
    Args:
        url: Direct file URL
        output_path: Path to save the file
        progress_tracker: Progress tracking object
        
    Returns:
        Tuple of (success, file_path, error_message)
    """
    try:
        timeout = aiohttp.ClientTimeout(total=config.download.timeout)
        
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(url) as response:
                if response.status != 200:
                    return False, None, f"HTTP {response.status}"
                
                # Get total size
                total_size = int(response.headers.get('content-length', 0))
                
                # Check file size limit
                if total_size > TELEGRAM_FILE_LIMIT:
                    return False, None, "file_too_large"
                
                # Create output directory
                output_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Download with progress
                downloaded = 0
                start_time = time.time()
                
                async with aiofiles.open(output_path, 'wb') as f:
                    async for chunk in response.content.iter_chunked(config.download.chunk_size):
                        await f.write(chunk)
                        downloaded += len(chunk)
                        
                        if progress_tracker:
                            elapsed = time.time() - start_time
                            speed = downloaded / elapsed if elapsed > 0 else 0
                            eta = int((total_size - downloaded) / speed) if speed > 0 else 0
                            progress = (downloaded / total_size * 100) if total_size else 0
                            
                            await progress_tracker.update(
                                status=DownloadStatus.DOWNLOADING,
                                progress=progress,
                                downloaded_bytes=downloaded,
                                total_bytes=total_size,
                                speed=speed,
                                eta=eta
                            )
                
                return True, output_path, ""
                
    except asyncio.TimeoutError:
        return False, None, "timeout"
    except aiohttp.ClientError as e:
        return False, None, f"Network error: {e}"
    except Exception as e:
        logger.error(f"Direct download error: {e}")
        return False, None, str(e)


# ═══════════════════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def generate_task_id() -> str:
    """Generate unique task ID."""
    return str(uuid.uuid4())[:8]


async def get_or_create_user(message: Message) -> UserData:
    """Get or create user data from message."""
    user = message.from_user
    user_data = await db.get_user(user.id)
    
    if not user_data:
        user_data = await db.create_or_update_user(
            user_id=user.id,
            username=user.username or "",
            first_name=user.first_name or "",
            last_name=user.last_name or "",
            language=DEFAULT_LANGUAGE
        )
    else:
        # Update last active
        await db.create_or_update_user(
            user_id=user.id,
            username=user.username or "",
            first_name=user.first_name or "",
            last_name=user.last_name or "",
            last_active=datetime.now()
        )
    
    # Sync language preference
    set_user_language(user.id, user_data.language)
    
    return user_data


def create_quality_keyboard(
    formats: List[Dict[str, Any]],
    task_id: str,
    lang_code: str = DEFAULT_LANGUAGE
) -> InlineKeyboardMarkup:
    """
    Create inline keyboard with quality options.
    
    Args:
        formats: List of available formats
        task_id: Task ID for callback data
        lang_code: Language code for labels
        
    Returns:
        InlineKeyboardMarkup with quality buttons
    """
    buttons = []
    
    # Get unique heights and sort
    heights = set()
    audio_available = False
    
    for fmt in formats:
        height = fmt.get('height', 0)
        if height and height > 0:
            heights.add(height)
        if fmt.get('is_audio_only'):
            audio_available = True
    
    heights = sorted(heights, reverse=True)
    
    # Quality buttons
    quality_map = {
        2160: ("4k", "🔵"),
        1440: ("2k", "🟣"),
        1080: ("1080p", "🟢"),
        720: ("720p", "🟡"),
        480: ("480p", "🟠"),
        360: ("360p", "🔴"),
        240: ("240p", "⚫️"),
    }
    
    row = []
    for height in heights[:6]:  # Limit to 6 options
        label_key, emoji = quality_map.get(height, (f"{height}p", "⚪️"))
        label = f"{emoji} {height}p"
        callback_data = f"dl:{task_id}:{height}"
        row.append(InlineKeyboardButton(label, callback_data=callback_data))
        
        if len(row) == 3:
            buttons.append(row)
            row = []
    
    if row:
        buttons.append(row)
    
    # Best quality button
    buttons.append([
        InlineKeyboardButton(
            get_text("buttons.quality_best", lang_code=lang_code),
            callback_data=f"dl:{task_id}:best"
        )
    ])
    
    # Audio only button
    if audio_available or formats:
        buttons.append([
            InlineKeyboardButton(
                get_text("buttons.quality_audio", lang_code=lang_code),
                callback_data=f"dl:{task_id}:audio"
            )
        ])
    
    # Cancel button
    buttons.append([
        InlineKeyboardButton(
            get_text("buttons.cancel", lang_code=lang_code),
            callback_data=f"cancel:{task_id}"
        )
    ])
    
    return InlineKeyboardMarkup(buttons)


def create_language_keyboard() -> InlineKeyboardMarkup:
    """Create language selection keyboard."""
    buttons = []
    
    for lang_code, lang_info in SUPPORTED_LANGUAGES.items():
        flag = lang_info.get('flag', '🌐')
        name = lang_info.get('name', lang_code)
        buttons.append([
            InlineKeyboardButton(
                f"{flag} {name}",
                callback_data=f"lang:{lang_code}"
            )
        ])
    
    return InlineKeyboardMarkup(buttons)


async def cleanup_temp_files(max_age_hours: int = 24) -> Tuple[int, int]:
    """
    Clean up old temporary files.
    
    Args:
        max_age_hours: Maximum age of files in hours
        
    Returns:
        Tuple of (files_deleted, bytes_freed)
    """
    files_deleted = 0
    bytes_freed = 0
    cutoff = datetime.now() - timedelta(hours=max_age_hours)
    
    for directory in [TEMP_DIR, DOWNLOADS_DIR]:
        if not directory.exists():
            continue
            
        for file_path in directory.rglob('*'):
            if file_path.is_file():
                try:
                    mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
                    if mtime < cutoff:
                        size = file_path.stat().st_size
                        file_path.unlink()
                        files_deleted += 1
                        bytes_freed += size
                except Exception as e:
                    logger.error(f"Error cleaning up {file_path}: {e}")
    
    logger.info(f"Cleanup: deleted {files_deleted} files, freed {format_file_size(bytes_freed)}")
    return files_deleted, bytes_freed


async def send_video_to_user(
    client: Client,
    chat_id: int,
    file_path: Path,
    video_info: VideoInfo,
    progress_tracker: Optional[ProgressTracker] = None
) -> bool:
    """
    Send downloaded video to user via Telegram.
    
    Args:
        client: Pyrogram client
        chat_id: Chat ID to send to
        file_path: Path to video file
        video_info: Video information
        progress_tracker: Progress tracker for upload
        
    Returns:
        True if successful, False otherwise
    """
    try:
        file_size = file_path.stat().st_size
        
        # Check file size
        if file_size > TELEGRAM_FILE_LIMIT:
            logger.error(f"File too large: {format_file_size(file_size)}")
            return False
        
        # Update status to uploading
        if progress_tracker:
            await progress_tracker.set_status(DownloadStatus.UPLOADING)
        
        # Upload progress callback
        async def upload_progress(current: int, total: int):
            if progress_tracker:
                await progress_tracker.update(
                    status=DownloadStatus.UPLOADING,
                    progress=(current / total) * 100,
                    downloaded_bytes=current,
                    total_bytes=total
                )
        
        # Determine if audio or video
        ext = file_path.suffix.lower()
        is_audio = ext in ['.mp3', '.m4a', '.aac', '.ogg', '.opus', '.wav', '.flac']
        
        # Prepare caption
        lang_code = get_user_language(chat_id)
        caption = get_text(
            "download.completed",
            lang_code=lang_code,
            title=escape_html(truncate_text(video_info.title, 100)),
            quality=video_info.formats[0].get('quality', 'N/A') if video_info.formats else 'N/A',
            size=format_size_localized(file_size, lang_code),
            duration=format_duration_text(video_info.duration, lang_code, short=True)
        )
        
        if is_audio:
            await client.send_audio(
                chat_id=chat_id,
                audio=str(file_path),
                caption=caption,
                parse_mode=enums.ParseMode.HTML,
                duration=video_info.duration,
                title=video_info.title,
                performer=video_info.uploader,
                progress=upload_progress
            )
        else:
            # Try to get thumbnail
            thumb = None
            if video_info.thumbnail:
                try:
                    thumb_path = TEMP_DIR / f"thumb_{generate_task_id()}.jpg"
                    async with aiohttp.ClientSession() as session:
                        async with session.get(video_info.thumbnail) as resp:
                            if resp.status == 200:
                                async with aiofiles.open(thumb_path, 'wb') as f:
                                    await f.write(await resp.read())
                                thumb = str(thumb_path)
                except:
                    pass
            
            await client.send_video(
                chat_id=chat_id,
                video=str(file_path),
                caption=caption,
                parse_mode=enums.ParseMode.HTML,
                duration=video_info.duration,
                thumb=thumb,
                supports_streaming=True,
                progress=upload_progress
            )
            
            # Clean up thumbnail
            if thumb:
                try:
                    Path(thumb).unlink()
                except:
                    pass
        
        return True
        
    except Exception as e:
        logger.error(f"Error sending video: {e}")
        return False


# ═══════════════════════════════════════════════════════════════════════════════
# DECORATORS
# ═══════════════════════════════════════════════════════════════════════════════

def rate_limit_check(func: MessageHandler) -> MessageHandler:
    """Decorator to check rate limits before handling message."""
    @wraps(func)
    async def wrapper(client: Client, message: Message):
        user_id = message.from_user.id
        user_data = await db.get_user(user_id)
        
        # Get limits based on VIP status
        if user_data and user_data.is_vip:
            daily_limit = config.rate_limit.vip_daily_limit
            concurrent_limit = config.rate_limit.vip_concurrent_limit
        else:
            daily_limit = config.rate_limit.daily_limit
            concurrent_limit = config.rate_limit.concurrent_limit
        
        # Check daily limit
        allowed, remaining = await bot_state.check_rate_limit(user_id, daily_limit)
        if not allowed:
            lang_code = get_user_language(user_id)
            await message.reply_text(
                get_text(
                    "errors.rate_limit",
                    lang_code=lang_code,
                    limit=daily_limit,
                    reset_time="24h"
                ),
                parse_mode=enums.ParseMode.HTML
            )
            return
        
        # Check concurrent limit
        active_downloads = await bot_state.get_user_download_count(user_id)
        if active_downloads >= concurrent_limit:
            lang_code = get_user_language(user_id)
            await message.reply_text(
                get_text(
                    "errors.concurrent_limit",
                    lang_code=lang_code,
                    current=active_downloads,
                    max=concurrent_limit
                ),
                parse_mode=enums.ParseMode.HTML
            )
            return
        
        return await func(client, message)
    
    return wrapper


def admin_only(func: MessageHandler) -> MessageHandler:
    """Decorator to restrict command to admins only."""
    @wraps(func)
    async def wrapper(client: Client, message: Message):
        user_id = message.from_user.id
        if not is_admin(user_id, config):
            lang_code = get_user_language(user_id)
            await message.reply_text(
                get_text("errors.not_admin", lang_code=lang_code),
                parse_mode=enums.ParseMode.HTML
            )
            return
        return await func(client, message)
    
    return wrapper


def owner_only(func: MessageHandler) -> MessageHandler:
    """Decorator to restrict command to owner only."""
    @wraps(func)
    async def wrapper(client: Client, message: Message):
        user_id = message.from_user.id
        if not is_owner(user_id, config):
            lang_code = get_user_language(user_id)
            await message.reply_text(
                get_text("errors.not_owner", lang_code=lang_code),
                parse_mode=enums.ParseMode.HTML
            )
            return
        return await func(client, message)
    
    return wrapper


def check_banned(func: MessageHandler) -> MessageHandler:
    """Decorator to check if user is banned."""
    @wraps(func)
    async def wrapper(client: Client, message: Message):
        user_id = message.from_user.id
        user_data = await db.get_user(user_id)
        
        if user_data and user_data.is_banned:
            lang_code = get_user_language(user_id)
            await message.reply_text(
                get_text(
                    "errors.banned",
                    lang_code=lang_code,
                    reason=user_data.ban_reason or "No reason provided"
                ),
                parse_mode=enums.ParseMode.HTML
            )
            return
        
        return await func(client, message)
    
    return wrapper


def maintenance_check(func: MessageHandler) -> MessageHandler:
    """Decorator to check if bot is in maintenance mode."""
    @wraps(func)
    async def wrapper(client: Client, message: Message):
        if config.maintenance_mode:
            # Allow owner during maintenance
            if is_owner(message.from_user.id, config):
                return await func(client, message)
            
            lang_code = get_user_language(message.from_user.id)
            await message.reply_text(
                get_text(
                    "errors.maintenance",
                    lang_code=lang_code,
                    message=config.maintenance_message or ""
                ),
                parse_mode=enums.ParseMode.HTML
            )
            return
        
        return await func(client, message)
    
    return wrapper


# ═══════════════════════════════════════════════════════════════════════════════
# PYROGRAM CLIENT INITIALIZATION
# ═══════════════════════════════════════════════════════════════════════════════

# Create Pyrogram client
app = Client(
    name=config.telegram.session_name,
    api_id=config.telegram.api_id,
    api_hash=config.telegram.api_hash,
    bot_token=config.telegram.bot_token,
    workers=config.telegram.workers,
    parse_mode=enums.ParseMode.HTML
)

# ═══════════════════════════════════════════════════════════════════════════════
# COMMAND HANDLERS
# ═══════════════════════════════════════════════════════════════════════════════

@app.on_message(filters.command("start") & filters.private)
@maintenance_check
@check_banned
async def start_command(client: Client, message: Message):
    """Handle /start command."""
    user = message.from_user
    user_data = await get_or_create_user(message)
    lang_code = user_data.language
    
    # Check if first time user
    is_new = user_data.total_downloads == 0
    
    if is_new:
        text = get_text(
            "start.first_time_user",
            lang_code=lang_code,
            name=escape_html(user_data.full_name)
        )
    else:
        text = get_text(
            "start.welcome_back",
            lang_code=lang_code,
            name=escape_html(user_data.full_name)
        )
    
    # Create main menu keyboard
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                get_text("buttons.help", lang_code=lang_code),
                callback_data="menu:help"
            ),
            InlineKeyboardButton(
                get_text("buttons.language", lang_code=lang_code),
                callback_data="menu:language"
            )
        ],
        [
            InlineKeyboardButton(
                get_text("buttons.stats", lang_code=lang_code),
                callback_data="menu:stats"
            ),
            InlineKeyboardButton(
                get_text("buttons.history", lang_code=lang_code),
                callback_data="menu:history"
            )
        ],
        [
            InlineKeyboardButton(
                get_text("buttons.cookie", lang_code=lang_code),
                callback_data="menu:cookie"
            ),
            InlineKeyboardButton(
                get_text("buttons.quality", lang_code=lang_code),
                callback_data="menu:quality"
            )
        ]
    ])
    
    # Add admin button for admins
    if is_admin(user.id, config):
        keyboard.inline_keyboard.append([
            InlineKeyboardButton(
                get_text("buttons.admin", lang_code=lang_code),
                callback_data="menu:admin"
            )
        ])
    
    await message.reply_text(
        get_text("start.welcome", lang_code=lang_code),
        reply_markup=keyboard,
        parse_mode=enums.ParseMode.HTML
    )
    
    logger.info(f"User {user.id} ({user.username}) started the bot")


@app.on_message(filters.command("help") & filters.private)
@maintenance_check
@check_banned
async def help_command(client: Client, message: Message):
    """Handle /help command."""
    user_data = await get_or_create_user(message)
    lang_code = user_data.language
    
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "🍪 " + get_text("buttons.cookie", lang_code=lang_code),
                callback_data="help:cookie"
            ),
            InlineKeyboardButton(
                "📊 " + get_text("buttons.quality", lang_code=lang_code),
                callback_data="help:quality"
            )
        ],
        [
            InlineKeyboardButton(
                "🌐 " + get_text("video_info.platform", lang_code=lang_code),
                callback_data="help:platforms"
            )
        ],
        [
            InlineKeyboardButton(
                get_text("buttons.back", lang_code=lang_code),
                callback_data="menu:main"
            )
        ]
    ])
    
    await message.reply_text(
        get_text("help.main", lang_code=lang_code),
        reply_markup=keyboard,
        parse_mode=enums.ParseMode.HTML
    )


@app.on_message(filters.command("language") & filters.private)
@maintenance_check
@check_banned
async def language_command(client: Client, message: Message):
    """Handle /language command."""
    user_data = await get_or_create_user(message)
    lang_code = user_data.language
    
    await message.reply_text(
        get_text("language.select", lang_code=lang_code),
        reply_markup=create_language_keyboard(),
        parse_mode=enums.ParseMode.HTML
    )


@app.on_message(filters.command("cookie") & filters.private)
@maintenance_check
@check_banned
async def cookie_command(client: Client, message: Message):
    """Handle /cookie command."""
    user_data = await get_or_create_user(message)
    lang_code = user_data.language
    
    await message.reply_text(
        get_text("help.cookie_guide", lang_code=lang_code),
        parse_mode=enums.ParseMode.HTML
    )


@app.on_message(filters.command("listcookies") & filters.private)
@maintenance_check
@check_banned
async def list_cookies_command(client: Client, message: Message):
    """Handle /listcookies command."""
    user_data = await get_or_create_user(message)
    lang_code = user_data.language
    user_id = message.from_user.id
    
    cookies = await db.get_all_cookies(user_id)
    
    if not cookies:
        await message.reply_text(
            get_text("cookie.list_empty", lang_code=lang_code),
            parse_mode=enums.ParseMode.HTML
        )
        return
    
    # Format cookies list
    cookies_list = []
    for i, cookie in enumerate(cookies, 1):
        platform = cookie['platform']
        created = cookie['created_at'][:10] if cookie['created_at'] else "N/A"
        
        if cookie['is_valid']:
            status = get_text("cookie.status_valid", lang_code=lang_code)
        else:
            status = get_text("cookie.status_expired", lang_code=lang_code)
        
        cookies_list.append(
            get_text(
                "cookie.list_item",
                lang_code=lang_code,
                number=i,
                platform=platform,
                date=created,
                status=status
            )
        )
    
    await message.reply_text(
        get_text(
            "cookie.list_title",
            lang_code=lang_code,
            cookies_list="\n".join(cookies_list)
        ),
        parse_mode=enums.ParseMode.HTML
    )


@app.on_message(filters.command("deletecookie") & filters.private)
@maintenance_check
@check_banned
async def delete_cookie_command(client: Client, message: Message):
    """Handle /deletecookie command."""
    user_data = await get_or_create_user(message)
    lang_code = user_data.language
    user_id = message.from_user.id
    
    # Check for platform argument
    args = message.text.split()[1:] if len(message.text.split()) > 1 else []
    
    if args:
        platform = args[0].lower()
        success = await db.delete_cookie(user_id, platform)
        
        if success:
            await message.reply_text(
                get_text("cookie.delete_success", lang_code=lang_code, platform=platform),
                parse_mode=enums.ParseMode.HTML
            )
        else:
            await message.reply_text(
                get_text("cookie.delete_not_found", lang_code=lang_code),
                parse_mode=enums.ParseMode.HTML
            )
    else:
        # Show list of cookies to delete
        cookies = await db.get_all_cookies(user_id)
        
        if not cookies:
            await message.reply_text(
                get_text("cookie.list_empty", lang_code=lang_code),
                parse_mode=enums.ParseMode.HTML
            )
            return
        
        buttons = []
        for cookie in cookies:
            platform = cookie['platform']
            buttons.append([
                InlineKeyboardButton(
                    f"🗑 {platform}",
                    callback_data=f"delcookie:{platform}"
                )
            ])
        
        buttons.append([
            InlineKeyboardButton(
                get_text("buttons.cancel", lang_code=lang_code),
                callback_data="menu:main"
            )
        ])
        
        await message.reply_text(
            get_text("cookie.delete_prompt", lang_code=lang_code, cookies_list=""),
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode=enums.ParseMode.HTML
        )


@app.on_message(filters.command("quality") & filters.private)
@maintenance_check
@check_banned
async def quality_command(client: Client, message: Message):
    """Handle /quality command."""
    user_data = await get_or_create_user(message)
    lang_code = user_data.language
    
    # Quality options
    qualities = [
        ("2160", "🔵 4K"),
        ("1440", "🟣 2K"),
        ("1080", "🟢 1080p"),
        ("720", "🟡 720p"),
        ("480", "🟠 480p"),
        ("360", "🔴 360p"),
    ]
    
    buttons = []
    row = []
    for quality, label in qualities:
        # Mark current default
        if quality == user_data.default_quality:
            label = f"✓ {label}"
        row.append(InlineKeyboardButton(label, callback_data=f"setquality:{quality}"))
        if len(row) == 3:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    
    buttons.append([
        InlineKeyboardButton(
            get_text("buttons.back", lang_code=lang_code),
            callback_data="menu:main"
        )
    ])
    
    await message.reply_text(
        get_text(
            "quality.set_default",
            lang_code=lang_code,
            quality=user_data.default_quality
        ),
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode=enums.ParseMode.HTML
    )


@app.on_message(filters.command("stats") & filters.private)
@maintenance_check
@check_banned
async def stats_command(client: Client, message: Message):
    """Handle /stats command."""
    user_data = await get_or_create_user(message)
    lang_code = user_data.language
    
    # Determine status
    if user_data.is_vip:
        status = get_text("stats.status_vip", lang_code=lang_code)
    elif user_data.is_banned:
        status = get_text("stats.status_banned", lang_code=lang_code)
    else:
        status = get_text("stats.status_normal", lang_code=lang_code)
    
    # Get limits
    if user_data.is_vip:
        daily_limit = config.rate_limit.vip_daily_limit
        concurrent_limit = config.rate_limit.vip_concurrent_limit
    else:
        daily_limit = config.rate_limit.daily_limit
        concurrent_limit = config.rate_limit.concurrent_limit
    
    active_downloads = await bot_state.get_user_download_count(user_data.user_id)
    
    # Format stats
    if lang_code == "fa":
        join_date = to_persian_digits(user_data.created_at.strftime("%Y/%m/%d"))
        total_downloads = to_persian_digits(str(user_data.total_downloads))
        successful = to_persian_digits(str(user_data.successful_downloads))
        failed = to_persian_digits(str(user_data.failed_downloads))
        success_rate = to_persian_digits(f"{user_data.success_rate:.1f}%")
        today_size = format_size_localized(0, "fa")  # TODO: Calculate
        month_size = format_size_localized(0, "fa")
        total_size = format_size_localized(user_data.total_size, "fa")
        daily_used = to_persian_digits(str(user_data.daily_downloads))
        daily_limit_str = to_persian_digits(str(daily_limit))
        concurrent_used = to_persian_digits(str(active_downloads))
        concurrent_limit_str = to_persian_digits(str(concurrent_limit))
    else:
        join_date = user_data.created_at.strftime("%Y/%m/%d")
        total_downloads = str(user_data.total_downloads)
        successful = str(user_data.successful_downloads)
        failed = str(user_data.failed_downloads)
        success_rate = f"{user_data.success_rate:.1f}%"
        today_size = format_file_size(0)
        month_size = format_file_size(0)
        total_size = format_file_size(user_data.total_size)
        daily_used = str(user_data.daily_downloads)
        daily_limit_str = str(daily_limit)
        concurrent_used = str(active_downloads)
        concurrent_limit_str = str(concurrent_limit)
    
    await message.reply_text(
        get_text(
            "stats.title",
            lang_code=lang_code,
            user_id=user_data.user_id,
            name=escape_html(user_data.full_name),
            join_date=join_date,
            status=status,
            total_downloads=total_downloads,
            successful=successful,
            failed=failed,
            success_rate=success_rate,
            today_size=today_size,
            month_size=month_size,
            total_size=total_size,
            daily_used=daily_used,
            daily_limit=daily_limit_str,
            concurrent_used=concurrent_used,
            concurrent_limit=concurrent_limit_str
        ),
        parse_mode=enums.ParseMode.HTML
    )


@app.on_message(filters.command("history") & filters.private)
@maintenance_check
@check_banned
async def history_command(client: Client, message: Message):
    """Handle /history command."""
    user_data = await get_or_create_user(message)
    lang_code = user_data.language
    user_id = message.from_user.id
    
    history = await db.get_download_history(user_id, limit=10)
    
    if not history:
        await message.reply_text(
            get_text("history.empty", lang_code=lang_code),
            parse_mode=enums.ParseMode.HTML
        )
        return
    
    # Format history list
    history_items = []
    for item in history:
        title = truncate_text(item['title'] or "Unknown", 30)
        date = item['created_at'][:10] if item['created_at'] else "N/A"
        size = format_size_localized(item['file_size'] or 0, lang_code)
        
        if item['status'] == 'completed':
            status = get_text("history.status_completed", lang_code=lang_code)
        else:
            status = get_text("history.status_failed", lang_code=lang_code)
        
        history_items.append(
            get_text(
                "history.item",
                lang_code=lang_code,
                title=escape_html(title),
                date=date,
                size=size,
                status=status
            )
        )
    
    await message.reply_text(
        get_text(
            "history.title",
            lang_code=lang_code,
            history_list="\n\n".join(history_items),
            showing=len(history),
            total=user_data.total_downloads,
            pagination=""
        ),
        parse_mode=enums.ParseMode.HTML
    )


@app.on_message(filters.command("cancel") & filters.private)
@maintenance_check
async def cancel_command(client: Client, message: Message):
    """Handle /cancel command."""
    user_id = message.from_user.id
    lang_code = get_user_language(user_id)
    
    cancelled = await bot_state.cancel_user_downloads(user_id)
    
    if cancelled > 0:
        await message.reply_text(
            get_text("download.cancelled", lang_code=lang_code),
            parse_mode=enums.ParseMode.HTML
        )
    else:
        await message.reply_text(
            get_text("common.none", lang_code=lang_code),
            parse_mode=enums.ParseMode.HTML
        )


# ═══════════════════════════════════════════════════════════════════════════════
# ADMIN COMMANDS
# ═══════════════════════════════════════════════════════════════════════════════

@app.on_message(filters.command("adminpanel") & filters.private)
@admin_only
async def admin_panel_command(client: Client, message: Message):
    """Handle /adminpanel command."""
    lang_code = get_user_language(message.from_user.id)
    
    # Gather statistics
    total_users = await db.get_total_users()
    active_users = await db.get_active_users(24)
    vip_users = await db.get_vip_users()
    banned_users = await db.get_banned_users()
    
    bot_stats = bot_state.get_stats()
    
    # System stats
    try:
        import psutil
        cpu_usage = f"{psutil.cpu_percent()}%"
        ram = psutil.virtual_memory()
        ram_usage = f"{ram.percent}%"
        disk = psutil.disk_usage('/')
        disk_usage = f"{disk.percent}%"
    except ImportError:
        cpu_usage = "N/A"
        ram_usage = "N/A"
        disk_usage = "N/A"
    
    # Top platforms (placeholder)
    top_platforms = "• YouTube\n• Instagram\n• TikTok"
    
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                get_text("buttons.broadcast", lang_code=lang_code),
                callback_data="admin:broadcast"
            ),
            InlineKeyboardButton(
                get_text("buttons.users", lang_code=lang_code),
                callback_data="admin:users"
            )
        ],
        [
            InlineKeyboardButton(
                get_text("buttons.cleanup", lang_code=lang_code),
                callback_data="admin:cleanup"
            ),
            InlineKeyboardButton(
                get_text("buttons.refresh", lang_code=lang_code),
                callback_data="admin:refresh"
            )
        ],
        [
            InlineKeyboardButton(
                get_text("buttons.back", lang_code=lang_code),
                callback_data="menu:main"
            )
        ]
    ])
    
    await message.reply_text(
        get_text(
            "admin.panel_title",
            lang_code=lang_code,
            total_users=total_users,
            active_users=active_users,
            vip_users=vip_users,
            banned_users=banned_users,
            today_downloads=bot_stats['total_downloads'],
            week_downloads=bot_stats['total_downloads'],
            total_downloads=bot_stats['total_downloads'],
            success_rate=bot_stats['success_rate'],
            uptime=bot_stats['uptime'],
            cpu_usage=cpu_usage,
            ram_usage=ram_usage,
            disk_usage=disk_usage,
            top_platforms=top_platforms
        ),
        reply_markup=keyboard,
        parse_mode=enums.ParseMode.HTML
    )


@app.on_message(filters.command("broadcast") & filters.private)
@owner_only
async def broadcast_command(client: Client, message: Message):
    """Handle /broadcast command."""
    lang_code = get_user_language(message.from_user.id)
    
    # Check if message has text after command
    if len(message.text.split(None, 1)) < 2:
        user_count = await db.get_total_users()
        await message.reply_text(
            get_text(
                "admin.broadcast_prompt",
                lang_code=lang_code,
                count=user_count
            ),
            parse_mode=enums.ParseMode.HTML
        )
        return
    
    broadcast_text = message.text.split(None, 1)[1]
    user_ids = await db.get_all_user_ids()
    
    # Confirm broadcast
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                get_text("buttons.confirm", lang_code=lang_code),
                callback_data=f"broadcast:confirm"
            ),
            InlineKeyboardButton(
                get_text("buttons.cancel", lang_code=lang_code),
                callback_data="menu:admin"
            )
        ]
    ])
    
    # Store broadcast text temporarily
    await bot_state.set_cached(f"broadcast:{message.from_user.id}", broadcast_text)
    
    await message.reply_text(
        get_text(
            "admin.broadcast_confirm",
            lang_code=lang_code,
            count=len(user_ids),
            message=escape_html(truncate_text(broadcast_text, 200))
        ),
        reply_markup=keyboard,
        parse_mode=enums.ParseMode.HTML
    )


@app.on_message(filters.command("ban") & filters.private)
@admin_only
async def ban_command(client: Client, message: Message):
    """Handle /ban command."""
    lang_code = get_user_language(message.from_user.id)
    
    args = message.text.split()[1:]
    if not args:
        await message.reply_text(
            "Usage: /ban <user_id> [reason]",
            parse_mode=enums.ParseMode.HTML
        )
        return
    
    try:
        target_id = int(args[0])
        reason = " ".join(args[1:]) if len(args) > 1 else "No reason provided"
        
        await db.create_or_update_user(
            user_id=target_id,
            is_banned=True,
            ban_reason=reason
        )
        
        await message.reply_text(
            get_text(
                "admin.ban_success",
                lang_code=lang_code,
                user_id=target_id,
                reason=reason
            ),
            parse_mode=enums.ParseMode.HTML
        )
    except ValueError:
        await message.reply_text(
            get_text("admin.user_not_found", lang_code=lang_code),
            parse_mode=enums.ParseMode.HTML
        )


@app.on_message(filters.command("unban") & filters.private)
@admin_only
async def unban_command(client: Client, message: Message):
    """Handle /unban command."""
    lang_code = get_user_language(message.from_user.id)
    
    args = message.text.split()[1:]
    if not args:
        await message.reply_text(
            "Usage: /unban <user_id>",
            parse_mode=enums.ParseMode.HTML
        )
        return
    
    try:
        target_id = int(args[0])
        
        await db.create_or_update_user(
            user_id=target_id,
            is_banned=False,
            ban_reason=""
        )
        
        await message.reply_text(
            get_text(
                "admin.unban_success",
                lang_code=lang_code,
                user_id=target_id
            ),
            parse_mode=enums.ParseMode.HTML
        )
    except ValueError:
        await message.reply_text(
            get_text("admin.user_not_found", lang_code=lang_code),
            parse_mode=enums.ParseMode.HTML
        )


@app.on_message(filters.command("setvip") & filters.private)
@owner_only
async def set_vip_command(client: Client, message: Message):
    """Handle /setvip command."""
    lang_code = get_user_language(message.from_user.id)
    
    args = message.text.split()[1:]
    if not args:
        await message.reply_text(
            "Usage: /setvip <user_id> [days=30]",
            parse_mode=enums.ParseMode.HTML
        )
        return
    
    try:
        target_id = int(args[0])
        days = int(args[1]) if len(args) > 1 else 30
        expiry = datetime.now() + timedelta(days=days)
        
        await db.create_or_update_user(
            user_id=target_id,
            is_vip=True,
            vip_expiry=expiry
        )
        
        await message.reply_text(
            get_text(
                "admin.vip_granted",
                lang_code=lang_code,
                user_id=target_id,
                expiry=expiry.strftime("%Y-%m-%d")
            ),
            parse_mode=enums.ParseMode.HTML
        )
    except ValueError:
        await message.reply_text(
            get_text("admin.user_not_found", lang_code=lang_code),
            parse_mode=enums.ParseMode.HTML
        )


@app.on_message(filters.command("cleanup") & filters.private)
@admin_only
async def cleanup_command(client: Client, message: Message):
    """Handle /cleanup command."""
    lang_code = get_user_language(message.from_user.id)
    
    await message.reply_text(
        get_text("admin.cleanup_started", lang_code=lang_code),
        parse_mode=enums.ParseMode.HTML
    )
    
    files_deleted, bytes_freed = await cleanup_temp_files(max_age_hours=1)
    
    await message.reply_text(
        get_text(
            "admin.cleanup_completed",
            lang_code=lang_code,
            files=files_deleted,
            size=format_size_localized(bytes_freed, lang_code)
        ),
        parse_mode=enums.ParseMode.HTML
    )


# ═══════════════════════════════════════════════════════════════════════════════
# DOCUMENT HANDLER (Cookie Upload)
# ═══════════════════════════════════════════════════════════════════════════════

@app.on_message(filters.document & filters.private)
@maintenance_check
@check_banned
async def document_handler(client: Client, message: Message):
    """Handle document uploads (cookies)."""
    user_data = await get_or_create_user(message)
    lang_code = user_data.language
    user_id = message.from_user.id
    
    document = message.document
    
    # Check if it's a cookie file
    if not document.file_name.endswith(('.txt', '.json')):
        return
    
    # Check file size
    if document.file_size > config.security.max_cookie_size:
        await message.reply_text(
            get_text("errors.file_too_large", lang_code=lang_code, size="1 MB"),
            parse_mode=enums.ParseMode.HTML
        )
        return
    
    # Download the file
    status_msg = await message.reply_text(
        get_text("cookie.uploading", lang_code=lang_code),
        parse_mode=enums.ParseMode.HTML
    )
    
    try:
        # Download to temp location
        file_path = await message.download(file_name=TEMP_DIR / f"cookie_{user_id}.txt")
        
        # Read and validate cookie content
        async with aiofiles.open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            cookie_content = await f.read()
        
        # Basic validation - check for Netscape format
        if '# Netscape HTTP Cookie File' not in cookie_content and not cookie_content.strip().startswith('{'):
            await status_msg.edit_text(
                get_text("cookie.invalid_format", lang_code=lang_code),
                parse_mode=enums.ParseMode.HTML
            )
            Path(file_path).unlink(missing_ok=True)
            return
        
        # Detect platform from cookie content
        platform = "generic"
        platform_patterns = {
            "youtube": ["youtube.com", "google.com"],
            "instagram": ["instagram.com"],
            "twitter": ["twitter.com", "x.com"],
            "facebook": ["facebook.com"],
            "tiktok": ["tiktok.com"],
        }
        
        for plat, patterns in platform_patterns.items():
            if any(p in cookie_content.lower() for p in patterns):
                platform = plat
                break
        
        # Encrypt and save
        encrypted = cookie_encryption.encrypt(cookie_content)
        await db.save_cookie(user_id, platform, encrypted)
        
        # Clean up temp file
        Path(file_path).unlink(missing_ok=True)
        
        await status_msg.edit_text(
            get_text(
                "cookie.upload_success",
                lang_code=lang_code,
                platform=platform,
                date=datetime.now().strftime("%Y-%m-%d")
            ),
            parse_mode=enums.ParseMode.HTML
        )
        
        logger.info(f"User {user_id} uploaded cookie for {platform}")
        
    except Exception as e:
        logger.error(f"Error processing cookie upload: {e}")
        await status_msg.edit_text(
            get_text(
                "cookie.upload_failed",
                lang_code=lang_code,
                reason=str(e)
            ),
            parse_mode=enums.ParseMode.HTML
        )


# ═══════════════════════════════════════════════════════════════════════════════
# URL HANDLER (Main Download Logic)
# ═══════════════════════════════════════════════════════════════════════════════

@app.on_message(filters.text & filters.private & ~filters.command(["start", "help", "language", "cookie", "listcookies", "deletecookie", "quality", "stats", "history", "cancel", "adminpanel", "broadcast", "ban", "unban", "setvip", "cleanup"]))
@maintenance_check
@check_banned
@rate_limit_check
async def url_handler(client: Client, message: Message):
    """Handle URL messages for downloading."""
    user_data = await get_or_create_user(message)
    lang_code = user_data.language
    user_id = message.from_user.id
    
    text = message.text.strip()
    
    # Extract URL from text
    url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
    urls = re.findall(url_pattern, text)
    
    if not urls:
        return  # Not a URL, ignore
    
    url = urls[0]
    
    # Validate URL
    if not is_valid_url(url):
        await message.reply_text(
            get_text("errors.invalid_url", lang_code=lang_code),
            parse_mode=enums.ParseMode.HTML
        )
        return
    
    # Detect platform
    platform = detect_platform(url)
    platform_name = get_text(f"platforms.{platform.value}", lang_code=lang_code)
    
    # Send processing message
    status_msg = await message.reply_text(
        get_text(
            "download.extracting_with_platform",
            lang_code=lang_code,
            platform=platform_name
        ),
        parse_mode=enums.ParseMode.HTML
    )
    
    # Generate task ID
    task_id = generate_task_id()
    
    try:
        # Extract video info
        video_info = await extract_video_info(url, user_id=user_id)
        
        if not video_info:
            await status_msg.edit_text(
                get_text("errors.extraction_failed", lang_code=lang_code),
                parse_mode=enums.ParseMode.HTML
            )
            return
        
        # Check for private/age-restricted content
        if video_info.is_private:
            await status_msg.edit_text(
                get_text("errors.private_video", lang_code=lang_code),
                parse_mode=enums.ParseMode.HTML
            )
            return
        
        if video_info.age_restricted:
            # Check if user has cookies
            cookie = await db.get_cookie(user_id, platform.value)
            if not cookie:
                await status_msg.edit_text(
                    get_text("errors.age_restricted", lang_code=lang_code),
                    parse_mode=enums.ParseMode.HTML
                )
                return
        
        # Create download task
        task = DownloadTask(
            task_id=task_id,
            user_id=user_id,
            chat_id=message.chat.id,
            message_id=status_msg.id,
            url=url,
            video_info=video_info,
            status=DownloadStatus.PENDING
        )
        await bot_state.add_download(task)
        
        # Format video info for display
        if lang_code == "fa":
            duration = format_duration_text(video_info.duration, "fa", short=True)
            views = to_persian_digits(video_info.views_formatted)
        else:
            duration = video_info.duration_formatted
            views = video_info.views_formatted
        
        # Create quality selection keyboard
        keyboard = create_quality_keyboard(video_info.formats, task_id, lang_code)
        
        await status_msg.edit_text(
            get_text(
                "download.select_quality",
                lang_code=lang_code,
                title=escape_html(truncate_text(video_info.title, 100)),
                uploader=escape_html(video_info.uploader or "N/A"),
                duration=duration,
                views=views
            ),
            reply_markup=keyboard,
            parse_mode=enums.ParseMode.HTML
        )
        
    except Exception as e:
        logger.error(f"Error processing URL {url}: {e}")
        logger.error(traceback.format_exc())
        
        await status_msg.edit_text(
            get_text(
                "errors.generic",
                lang_code=lang_code,
                message=str(e)[:100]
            ),
            parse_mode=enums.ParseMode.HTML
        )


# ═══════════════════════════════════════════════════════════════════════════════
# CALLBACK QUERY HANDLERS
# ═══════════════════════════════════════════════════════════════════════════════

@app.on_callback_query()
async def callback_handler(client: Client, callback: CallbackQuery):
    """Handle all callback queries."""
    user_id = callback.from_user.id
    lang_code = get_user_language(user_id)
    data = callback.data
    
    try:
        # Menu callbacks
        if data.startswith("menu:"):
            await handle_menu_callback(client, callback, data, lang_code)
        
        # Language callbacks
        elif data.startswith("lang:"):
            await handle_language_callback(client, callback, data, lang_code)
        
        # Help callbacks
        elif data.startswith("help:"):
            await handle_help_callback(client, callback, data, lang_code)
        
        # Download callbacks
        elif data.startswith("dl:"):
            await handle_download_callback(client, callback, data, lang_code)
        
        # Cancel callbacks
        elif data.startswith("cancel:"):
            await handle_cancel_callback(client, callback, data, lang_code)
        
        # Quality setting callbacks
        elif data.startswith("setquality:"):
            await handle_quality_callback(client, callback, data, lang_code)
        
        # Cookie delete callbacks
        elif data.startswith("delcookie:"):
            await handle_cookie_delete_callback(client, callback, data, lang_code)
        
        # Admin callbacks
        elif data.startswith("admin:"):
            await handle_admin_callback(client, callback, data, lang_code)
        
        # Broadcast callbacks
        elif data.startswith("broadcast:"):
            await handle_broadcast_callback(client, callback, data, lang_code)
        
        else:
            await callback.answer("Unknown action", show_alert=True)
            
    except Exception as e:
        logger.error(f"Callback error: {e}")
        logger.error(traceback.format_exc())
        await callback.answer(
            get_text("common.error", lang_code=lang_code),
            show_alert=True
        )


async def handle_menu_callback(client: Client, callback: CallbackQuery, data: str, lang_code: str):
    """Handle menu navigation callbacks."""
    action = data.split(":")[1]
    
    if action == "main":
        # Back to main menu
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    get_text("buttons.help", lang_code=lang_code),
                    callback_data="menu:help"
                ),
                InlineKeyboardButton(
                    get_text("buttons.language", lang_code=lang_code),
                    callback_data="menu:language"
                )
            ],
            [
                InlineKeyboardButton(
                    get_text("buttons.stats", lang_code=lang_code),
                    callback_data="menu:stats"
                ),
                InlineKeyboardButton(
                    get_text("buttons.history", lang_code=lang_code),
                    callback_data="menu:history"
                )
            ]
        ])
        
        await callback.message.edit_text(
            get_text("start.welcome", lang_code=lang_code),
            reply_markup=keyboard,
            parse_mode=enums.ParseMode.HTML
        )
    
    elif action == "help":
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🍪 Cookie", callback_data="help:cookie"),
                InlineKeyboardButton("📊 Quality", callback_data="help:quality")
            ],
            [
                InlineKeyboardButton("🌐 Platforms", callback_data="help:platforms")
            ],
            [
                InlineKeyboardButton(
                    get_text("buttons.back", lang_code=lang_code),
                    callback_data="menu:main"
                )
            ]
        ])
        
        await callback.message.edit_text(
            get_text("help.main", lang_code=lang_code),
            reply_markup=keyboard,
            parse_mode=enums.ParseMode.HTML
        )
    
    elif action == "language":
        await callback.message.edit_text(
            get_text("language.select", lang_code=lang_code),
            reply_markup=create_language_keyboard(),
            parse_mode=enums.ParseMode.HTML
        )
    
    elif action == "stats":
        await callback.answer()
        # Trigger stats command logic
        user_data = await db.get_user(callback.from_user.id)
        if user_data:
            # Similar to stats_command
            await callback.answer(get_text("common.loading", lang_code=lang_code))
    
    elif action == "history":
        await callback.answer()
        # Trigger history command logic
    
    elif action == "cookie":
        await callback.message.edit_text(
            get_text("help.cookie_guide", lang_code=lang_code),
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton(
                    get_text("buttons.back", lang_code=lang_code),
                    callback_data="menu:main"
                )
            ]]),
            parse_mode=enums.ParseMode.HTML
        )
    
    elif action == "quality":
        user_data = await db.get_user(callback.from_user.id)
        current_quality = user_data.default_quality if user_data else "1080"
        
        qualities = [
            ("2160", "🔵 4K"),
            ("1440", "🟣 2K"),
            ("1080", "🟢 1080p"),
            ("720", "🟡 720p"),
            ("480", "🟠 480p"),
        ]
        
        buttons = []
        row = []
        for quality, label in qualities:
            if quality == current_quality:
                label = f"✓ {label}"
            row.append(InlineKeyboardButton(label, callback_data=f"setquality:{quality}"))
            if len(row) == 3:
                buttons.append(row)
                row = []
        if row:
            buttons.append(row)
        
        buttons.append([
            InlineKeyboardButton(
                get_text("buttons.back", lang_code=lang_code),
                callback_data="menu:main"
            )
        ])
        
        await callback.message.edit_text(
            get_text("quality.set_default", lang_code=lang_code, quality=current_quality),
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode=enums.ParseMode.HTML
        )
    
    elif action == "admin":
        if not is_admin(callback.from_user.id, config):
            await callback.answer(get_text("errors.not_admin", lang_code=lang_code), show_alert=True)
            return
        
        # Show admin panel
        await callback.answer()
    
    await callback.answer()


async def handle_language_callback(client: Client, callback: CallbackQuery, data: str, lang_code: str):
    """Handle language selection callbacks."""
    new_lang = data.split(":")[1]
    user_id = callback.from_user.id
    
    if new_lang in SUPPORTED_LANGUAGES:
        # Update user language
        await db.create_or_update_user(user_id=user_id, language=new_lang)
        set_user_language(user_id, new_lang)
        
        await callback.message.edit_text(
            get_text("language.changed", lang_code=new_lang),
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton(
                    get_text("buttons.back", lang_code=new_lang),
                    callback_data="menu:main"
                )
            ]]),
            parse_mode=enums.ParseMode.HTML
        )
        
        await callback.answer(get_text("common.success", lang_code=new_lang))
    else:
        await callback.answer(
            get_text("language.not_available", lang_code=lang_code),
            show_alert=True
        )


async def handle_help_callback(client: Client, callback: CallbackQuery, data: str, lang_code: str):
    """Handle help section callbacks."""
    section = data.split(":")[1]
    
    back_button = InlineKeyboardMarkup([[
        InlineKeyboardButton(
            get_text("buttons.back", lang_code=lang_code),
            callback_data="menu:help"
        )
    ]])
    
    if section == "cookie":
        await callback.message.edit_text(
            get_text("help.cookie_guide", lang_code=lang_code),
            reply_markup=back_button,
            parse_mode=enums.ParseMode.HTML
        )
    
    elif section == "quality":
        await callback.message.edit_text(
            get_text("help.quality_guide", lang_code=lang_code),
            reply_markup=back_button,
            parse_mode=enums.ParseMode.HTML
        )
    
    elif section == "platforms":
        await callback.message.edit_text(
            get_text("help.platforms", lang_code=lang_code),
            reply_markup=back_button,
            parse_mode=enums.ParseMode.HTML
        )
    
    await callback.answer()


async def handle_download_callback(client: Client, callback: CallbackQuery, data: str, lang_code: str):
    """Handle download quality selection callbacks."""
    parts = data.split(":")
    task_id = parts[1]
    quality = parts[2]
    
    user_id = callback.from_user.id
    
    # Get download task
    task = await bot_state.get_download(task_id)
    
    if not task:
        await callback.answer(
            get_text("common.error", lang_code=lang_code),
            show_alert=True
        )
        return
    
    if task.user_id != user_id:
        await callback.answer("Not your download!", show_alert=True)
        return
    
    # Update task status
    task.status = DownloadStatus.DOWNLOADING
    
    # Acknowledge callback
    await callback.answer(get_text("download.starting", lang_code=lang_code))
    
    # Create progress tracker
    progress_tracker = ProgressTracker(
        client=client,
        chat_id=task.chat_id,
        message_id=task.message_id,
        user_id=user_id,
        task_id=task_id,
        lang_code=lang_code
    )
    progress_tracker.quality = quality
    
    # Update message to show starting
    await callback.message.edit_text(
        get_text("download.starting", lang_code=lang_code),
        parse_mode=enums.ParseMode.HTML
    )
    
    try:
        # Prepare output path
        safe_title = clean_filename(task.video_info.title)
        output_path = TEMP_DIR / f"{safe_title}_{task_id}"
        
        # Determine if audio only
        audio_only = quality == "audio"
        
        # Start download
        success, file_path, error = await download_video(
            url=task.url,
            output_path=output_path,
            quality=quality if not audio_only else "best",
            user_id=user_id,
            progress_tracker=progress_tracker,
            audio_only=audio_only
        )
        
        if task.cancelled:
            await progress_tracker.complete(
                get_text("download.cancelled", lang_code=lang_code)
            )
            await bot_state.remove_download(task_id)
            return
        
        if not success:
            # Handle specific errors
            error_key = "errors.download_failed"
            if error == "private_video":
                error_key = "errors.private_video"
            elif error == "age_restricted":
                error_key = "errors.age_restricted"
            elif error == "geo_restricted":
                error_key = "errors.geo_restricted"
            elif error == "file_too_large":
                error_key = "errors.file_too_large"
            
            await progress_tracker.complete(
                get_text(error_key, lang_code=lang_code, reason=error, size="2 GB")
            )
            
            # Update stats
            await db.increment_download_count(user_id, success=False)
            await bot_state.increment_stats(success=False)
            
            # Add to history
            await db.add_download_history(
                user_id=user_id,
                url=task.url,
                title=task.video_info.title,
                platform=task.video_info.platform.value,
                quality=quality,
                file_size=0,
                duration=task.video_info.duration,
                status="failed",
                error_message=error
            )
            
            await bot_state.remove_download(task_id)
            return
        
        # Upload to Telegram
        await progress_tracker.set_status(DownloadStatus.UPLOADING)
        
        upload_success = await send_video_to_user(
            client=client,
            chat_id=task.chat_id,
            file_path=file_path,
            video_info=task.video_info,
            progress_tracker=progress_tracker
        )
        
        if upload_success:
            # Delete progress message
            try:
                await callback.message.delete()
            except:
                pass
            
            # Update stats
            file_size = file_path.stat().st_size
            await db.increment_download_count(user_id, success=True, size=file_size)
            await bot_state.increment_stats(success=True)
            
            # Add to history
            await db.add_download_history(
                user_id=user_id,
                url=task.url,
                title=task.video_info.title,
                platform=task.video_info.platform.value,
                quality=quality,
                file_size=file_size,
                duration=task.video_info.duration,
                status="completed"
            )
            
            logger.info(f"Download completed for user {user_id}: {task.video_info.title}")
        else:
            await progress_tracker.complete(
                get_text("errors.upload_failed", lang_code=lang_code)
            )
            await db.increment_download_count(user_id, success=False)
            await bot_state.increment_stats(success=False)
        
        # Cleanup
        if file_path and file_path.exists():
            try:
                file_path.unlink()
            except:
                pass
        
        await bot_state.remove_download(task_id)
        
    except asyncio.CancelledError:
        await progress_tracker.complete(
            get_text("download.cancelled", lang_code=lang_code)
        )
        await bot_state.remove_download(task_id)
        
    except Exception as e:
        logger.error(f"Download error: {e}")
        logger.error(traceback.format_exc())
        
        await progress_tracker.complete(
            get_text("errors.generic", lang_code=lang_code, message=str(e)[:100])
        )
        
        await db.increment_download_count(user_id, success=False)
        await bot_state.increment_stats(success=False)
        await bot_state.remove_download(task_id)


async def handle_cancel_callback(client: Client, callback: CallbackQuery, data: str, lang_code: str):
    """Handle download cancellation callbacks."""
    task_id = data.split(":")[1]
    user_id = callback.from_user.id
    
    task = await bot_state.get_download(task_id)
    
    if task and task.user_id == user_id:
        task.cancelled = True
        await bot_state.remove_download(task_id)
        
        await callback.message.edit_text(
            get_text("download.cancelled", lang_code=lang_code),
            parse_mode=enums.ParseMode.HTML
        )
        
        await callback.answer(get_text("common.cancelled", lang_code=lang_code))
    else:
        await callback.answer(get_text("common.error", lang_code=lang_code), show_alert=True)


async def handle_quality_callback(client: Client, callback: CallbackQuery, data: str, lang_code: str):
    """Handle default quality setting callbacks."""
    quality = data.split(":")[1]
    user_id = callback.from_user.id
    
    await db.create_or_update_user(user_id=user_id, default_quality=quality)
    
    await callback.answer(
        get_text("quality.default_changed", lang_code=lang_code, quality=quality)
    )
    
    # Refresh the keyboard
    await callback.message.edit_text(
        get_text("quality.set_default", lang_code=lang_code, quality=quality),
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton(
                get_text("buttons.back", lang_code=lang_code),
                callback_data="menu:main"
            )
        ]]),
        parse_mode=enums.ParseMode.HTML
    )


async def handle_cookie_delete_callback(client: Client, callback: CallbackQuery, data: str, lang_code: str):
    """Handle cookie deletion callbacks."""
    platform = data.split(":")[1]
    user_id = callback.from_user.id
    
    success = await db.delete_cookie(user_id, platform)
    
    if success:
        await callback.answer(
            get_text("cookie.delete_success", lang_code=lang_code, platform=platform)
        )
        await callback.message.edit_text(
            get_text("cookie.delete_success", lang_code=lang_code, platform=platform),
            parse_mode=enums.ParseMode.HTML
        )
    else:
        await callback.answer(
            get_text("cookie.delete_failed", lang_code=lang_code),
            show_alert=True
        )


async def handle_admin_callback(client: Client, callback: CallbackQuery, data: str, lang_code: str):
    """Handle admin panel callbacks."""
    if not is_admin(callback.from_user.id, config):
        await callback.answer(get_text("errors.not_admin", lang_code=lang_code), show_alert=True)
        return
    
    action = data.split(":")[1]
    
    if action == "cleanup":
        await callback.answer(get_text("admin.cleanup_started", lang_code=lang_code))
        files, size = await cleanup_temp_files(max_age_hours=1)
        await callback.message.edit_text(
            get_text(
                "admin.cleanup_completed",
                lang_code=lang_code,
                files=files,
                size=format_size_localized(size, lang_code)
            ),
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton(
                    get_text("buttons.back", lang_code=lang_code),
                    callback_data="menu:admin"
                )
            ]]),
            parse_mode=enums.ParseMode.HTML
        )
    
    elif action == "refresh":
        await callback.answer(get_text("common.loading", lang_code=lang_code))
        # Refresh admin panel
    
    elif action == "broadcast":
        user_count = await db.get_total_users()
        await callback.message.edit_text(
            get_text("admin.broadcast_prompt", lang_code=lang_code, count=user_count),
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton(
                    get_text("buttons.cancel", lang_code=lang_code),
                    callback_data="menu:admin"
                )
            ]]),
            parse_mode=enums.ParseMode.HTML
        )


async def handle_broadcast_callback(client: Client, callback: CallbackQuery, data: str, lang_code: str):
    """Handle broadcast confirmation callbacks."""
    if not is_owner(callback.from_user.id, config):
        await callback.answer(get_text("errors.not_owner", lang_code=lang_code), show_alert=True)
        return
    
    action = data.split(":")[1]
    
    if action == "confirm":
        # Get cached broadcast message
        broadcast_text = await bot_state.get_cached(f"broadcast:{callback.from_user.id}")
        
        if not broadcast_text:
            await callback.answer("Broadcast expired", show_alert=True)
            return
        
        await callback.answer(get_text("admin.broadcast_started", lang_code=lang_code))
        
        user_ids = await db.get_all_user_ids()
        success_count = 0
        fail_count = 0
        
        status_msg = await callback.message.edit_text(
            get_text("admin.broadcast_progress", lang_code=lang_code, sent=0, total=len(user_ids)),
            parse_mode=enums.ParseMode.HTML
        )
        
        for i, uid in enumerate(user_ids):
            try:
                await client.send_message(uid, broadcast_text, parse_mode=enums.ParseMode.HTML)
                success_count += 1
            except (UserIsBlocked, InputUserDeactivated, PeerIdInvalid):
                fail_count += 1
            except FloodWait as e:
                await asyncio.sleep(e.value)
                try:
                    await client.send_message(uid, broadcast_text, parse_mode=enums.ParseMode.HTML)
                    success_count += 1
                except:
                    fail_count += 1
            except Exception:
                fail_count += 1
            
            # Update progress every 50 users
            if (i + 1) % 50 == 0:
                try:
                    await status_msg.edit_text(
                        get_text(
                            "admin.broadcast_progress",
                            lang_code=lang_code,
                            sent=i + 1,
                            total=len(user_ids)
                        ),
                        parse_mode=enums.ParseMode.HTML
                    )
                except:
                    pass
        
        await status_msg.edit_text(
            get_text(
                "admin.broadcast_completed",
                lang_code=lang_code,
                success=success_count,
                failed=fail_count,
                total=len(user_ids)
            ),
            parse_mode=enums.ParseMode.HTML
        )


# ═══════════════════════════════════════════════════════════════════════════════
# BACKGROUND TASKS
# ═══════════════════════════════════════════════════════════════════════════════

async def cleanup_task():
    """Background task to clean up temporary files periodically."""
    while True:
        try:
            await asyncio.sleep(3600)  # Every hour
            await cleanup_temp_files(max_age_hours=24)
        except asyncio.CancelledError:
            break
        except Exception as e:
            logger.error(f"Cleanup task error: {e}")


async def daily_reset_task():
    """Background task to reset daily limits at midnight."""
    while True:
        try:
            # Calculate time until midnight
            now = datetime.now()
            midnight = now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
            seconds_until_midnight = (midnight - now).total_seconds()
            
            await asyncio.sleep(seconds_until_midnight)
            
            # Reset daily downloads for all users
            async with db.get_connection() as conn:
                await conn.execute("UPDATE users SET daily_downloads = 0, daily_reset = ?", 
                                 (datetime.now().isoformat(),))
                await conn.commit()
            
            logger.info("Daily limits reset completed")
            
        except asyncio.CancelledError:
            break
        except Exception as e:
            logger.error(f"Daily reset task error: {e}")


# ═══════════════════════════════════════════════════════════════════════════════
# ERROR HANDLERS
# ═══════════════════════════════════════════════════════════════════════════════

@app.on_error()
async def error_handler(client: Client, error: Exception):
    """Global error handler."""
    logger.error(f"Unhandled error: {error}")
    logger.error(traceback.format_exc())


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN EXECUTION
# ═══════════════════════════════════════════════════════════════════════════════

async def main():
    """Main entry point."""
    logger.info("🚀 Starting Video Downloader Bot...")
    
    # Initialize database
    await db.initialize()
    
    # Load languages
    load_all_languages()
    
    # Ensure directories exist
    for directory in [TEMP_DIR, DOWNLOADS_DIR, COOKIES_DIR, LOGS_DIR]:
        directory.mkdir(parents=True, exist_ok=True)
    
    # Start background tasks
    cleanup_task_handle = asyncio.create_task(cleanup_task())
    daily_reset_handle = asyncio.create_task(daily_reset_task())
    
    try:
        # Start the bot
        await app.start()
        logger.info("✅ Bot started successfully!")
        logger.info(f"👤 Bot username: @{(await app.get_me()).username}")
        
        # Keep the bot running
        await asyncio.Event().wait()
        
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        logger.error(traceback.format_exc())
        
    finally:
        # Cleanup
        cleanup_task_handle.cancel()
        daily_reset_handle.cancel()
        
        await db.close()
        await app.stop()
        
        logger.info("👋 Bot stopped")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.critical(f"Fatal error: {e}")
        logger.critical(traceback.format_exc())
        sys.exit(1)