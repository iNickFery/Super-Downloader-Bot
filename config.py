#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    Professional Video Downloader Bot                         ║
║                         Configuration System                                 ║
║                                                                              ║
║  Author: Professional Developer                                              ║
║  Version: 2.0.0                                                              ║
║  License: MIT                                                                ║
║  Default Language: Persian (Farsi)                                           ║
╚══════════════════════════════════════════════════════════════════════════════╝

This module handles all configuration settings with:
- Environment variable loading with validation
- Type-safe configuration classes
- Default values with override capability
- Runtime validation and error handling
- Constants and enums for type safety
"""

from __future__ import annotations

import os
import sys
import logging
from pathlib import Path
from typing import Optional, List, Dict, Any, Set, FrozenSet
from dataclasses import dataclass, field
from enum import Enum, auto
from functools import lru_cache
import re

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv(override=True)
except ImportError:
    pass  # dotenv is optional in production


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 1: Enums and Constants
# ═══════════════════════════════════════════════════════════════════════════════

class LogLevel(Enum):
    """Supported log levels."""
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL


class VideoQuality(Enum):
    """Supported video quality options."""
    QUALITY_4K = "2160"
    QUALITY_2K = "1440"
    QUALITY_1080P = "1080"
    QUALITY_720P = "720"
    QUALITY_480P = "480"
    QUALITY_360P = "360"
    QUALITY_240P = "240"
    QUALITY_AUDIO = "audio"
    QUALITY_BEST = "best"
    QUALITY_AUTO = "auto"


class DownloadStatus(Enum):
    """Download status indicators."""
    PENDING = auto()
    EXTRACTING = auto()
    DOWNLOADING = auto()
    MERGING = auto()
    UPLOADING = auto()
    COMPLETED = auto()
    FAILED = auto()
    CANCELLED = auto()


class Platform(Enum):
    """Supported platform identifiers."""
    YOUTUBE = "youtube"
    INSTAGRAM = "instagram"
    TWITTER = "twitter"
    TIKTOK = "tiktok"
    FACEBOOK = "facebook"
    VIMEO = "vimeo"
    DAILYMOTION = "dailymotion"
    TWITCH = "twitch"
    REDDIT = "reddit"
    APARAT = "aparat"
    NAMASHA = "namasha"
    VK = "vk"
    BILIBILI = "bilibili"
    DIRECT = "direct"
    UNKNOWN = "unknown"


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 2: Configuration Constants
# ═══════════════════════════════════════════════════════════════════════════════

# Version information
VERSION: str = "2.0.0"
BUILD_DATE: str = "2025-01-01"
CODENAME: str = "Phoenix"

# Directory paths
BASE_DIR: Path = Path(__file__).parent.absolute()
TEMP_DIR: Path = BASE_DIR / "temp"
DOWNLOADS_DIR: Path = BASE_DIR / "downloads"
COOKIES_DIR: Path = BASE_DIR / "cookies"
LOGS_DIR: Path = BASE_DIR / "logs"
CACHE_DIR: Path = BASE_DIR / "cache"
DATABASE_DIR: Path = BASE_DIR / "database"
LANGUAGES_DIR: Path = BASE_DIR / "languages"

# File size limits (in bytes)
TELEGRAM_FILE_LIMIT: int = 2 * 1024 * 1024 * 1024  # 2 GB (Telegram Premium limit)
TELEGRAM_STANDARD_LIMIT: int = 50 * 1024 * 1024  # 50 MB (Standard limit)
MAX_THUMBNAIL_SIZE: int = 200 * 1024  # 200 KB
MAX_COOKIE_FILE_SIZE: int = 1 * 1024 * 1024  # 1 MB

# Time constants (in seconds)
PROGRESS_UPDATE_INTERVAL: float = 2.0  # Update progress every 2 seconds
VIDEO_INFO_TIMEOUT: int = 30
DOWNLOAD_TIMEOUT: int = 3600  # 1 hour
UPLOAD_TIMEOUT: int = 1800  # 30 minutes
CACHE_TTL: int = 300  # 5 minutes
COOKIE_EXPIRY_WARNING_DAYS: int = 7

# Network settings
CHUNK_SIZE: int = 1024 * 1024  # 1 MB chunks
MAX_RETRIES: int = 3
RETRY_DELAY: float = 1.0
CONNECTION_TIMEOUT: int = 30
READ_TIMEOUT: int = 60

# Rate limiting
DEFAULT_DAILY_LIMIT: int = 50
DEFAULT_CONCURRENT_LIMIT: int = 5
VIP_DAILY_LIMIT: int = 200
VIP_CONCURRENT_LIMIT: int = 10
GLOBAL_CONCURRENT_LIMIT: int = 50
COOLDOWN_PERIOD: int = 60  # seconds

# Supported languages (code -> name mapping)
SUPPORTED_LANGUAGES: Dict[str, Dict[str, str]] = {
    "fa": {"name": "فارسی", "flag": "🇮🇷", "rtl": True, "native_name": "Persian"},
    "en": {"name": "English", "flag": "🇬🇧", "rtl": False, "native_name": "English"},
}

# Default language
DEFAULT_LANGUAGE: str = "fa"
FALLBACK_LANGUAGE: str = "en"

# Supported video formats
SUPPORTED_VIDEO_FORMATS: FrozenSet[str] = frozenset({
    "mp4", "mkv", "webm", "avi", "mov", "flv", "wmv", "m4v", "3gp"
})

SUPPORTED_AUDIO_FORMATS: FrozenSet[str] = frozenset({
    "mp3", "m4a", "aac", "ogg", "opus", "wav", "flac"
})

# Output format (always MP4 for compatibility)
OUTPUT_VIDEO_FORMAT: str = "mp4"
OUTPUT_AUDIO_FORMAT: str = "mp3"

# Quality presets with format strings
QUALITY_PRESETS: Dict[str, str] = {
    "2160": "bestvideo[height<=2160][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<=2160]+bestaudio/best[height<=2160]",
    "1440": "bestvideo[height<=1440][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<=1440]+bestaudio/best[height<=1440]",
    "1080": "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<=1080]+bestaudio/best[height<=1080]",
    "720": "bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<=720]+bestaudio/best[height<=720]",
    "480": "bestvideo[height<=480][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<=480]+bestaudio/best[height<=480]",
    "360": "bestvideo[height<=360][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<=360]+bestaudio/best[height<=360]",
    "240": "bestvideo[height<=240][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<=240]+bestaudio/best[height<=240]",
    "audio": "bestaudio[ext=m4a]/bestaudio/best",
    "best": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best",
    "auto": "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<=1080]+bestaudio/best[height<=1080]",
}

# Platform detection patterns
PLATFORM_PATTERNS: Dict[str, List[str]] = {
    "youtube": [
        r"(?:https?://)?(?:www\.)?youtube\.com/watch\?v=[\w-]+",
        r"(?:https?://)?(?:www\.)?youtu\.be/[\w-]+",
        r"(?:https?://)?(?:www\.)?youtube\.com/shorts/[\w-]+",
        r"(?:https?://)?(?:www\.)?youtube\.com/live/[\w-]+",
        r"(?:https?://)?(?:www\.)?youtube\.com/playlist\?list=[\w-]+",
    ],
    "instagram": [
        r"(?:https?://)?(?:www\.)?instagram\.com/(?:p|reel|tv)/[\w-]+",
        r"(?:https?://)?(?:www\.)?instagram\.com/stories/[\w.]+/\d+",
    ],
    "twitter": [
        r"(?:https?://)?(?:www\.)?(?:twitter|x)\.com/\w+/status/\d+",
        r"(?:https?://)?(?:www\.)?(?:twitter|x)\.com/i/status/\d+",
    ],
    "tiktok": [
        r"(?:https?://)?(?:www\.)?tiktok\.com/@[\w.]+/video/\d+",
        r"(?:https?://)?(?:vm|vt)\.tiktok\.com/[\w]+",
        r"(?:https?://)?(?:www\.)?tiktok\.com/t/[\w]+",
    ],
    "facebook": [
        r"(?:https?://)?(?:www\.)?facebook\.com/.+/videos/\d+",
        r"(?:https?://)?(?:www\.)?fb\.watch/[\w]+",
        r"(?:https?://)?(?:www\.)?facebook\.com/watch/?\?v=\d+",
    ],
    "vimeo": [
        r"(?:https?://)?(?:www\.)?vimeo\.com/\d+",
        r"(?:https?://)?player\.vimeo\.com/video/\d+",
    ],
    "dailymotion": [
        r"(?:https?://)?(?:www\.)?dailymotion\.com/video/[\w]+",
        r"(?:https?://)?dai\.ly/[\w]+",
    ],
    "twitch": [
        r"(?:https?://)?(?:www\.)?twitch\.tv/videos/\d+",
        r"(?:https?://)?(?:www\.)?twitch\.tv/\w+/clip/[\w-]+",
        r"(?:https?://)?clips\.twitch\.tv/[\w-]+",
    ],
    "reddit": [
        r"(?:https?://)?(?:www\.)?reddit\.com/r/\w+/comments/[\w]+",
        r"(?:https?://)?(?:www\.)?redd\.it/[\w]+",
        r"(?:https?://)?v\.redd\.it/[\w]+",
    ],
    "aparat": [
        r"(?:https?://)?(?:www\.)?aparat\.com/v/[\w]+",
    ],
    "namasha": [
        r"(?:https?://)?(?:www\.)?namasha\.com/v/[\w]+",
    ],
    "vk": [
        r"(?:https?://)?(?:www\.)?vk\.com/video-?\d+_\d+",
        r"(?:https?://)?(?:www\.)?vk\.com/clip-?\d+_\d+",
    ],
    "bilibili": [
        r"(?:https?://)?(?:www\.)?bilibili\.com/video/[\w]+",
        r"(?:https?://)?b23\.tv/[\w]+",
    ],
}

# Direct link patterns
DIRECT_LINK_PATTERNS: List[str] = [
    r"(?:https?://)[^\s]+\.(?:mp4|mkv|webm|avi|mov|flv|wmv|m4v|3gp)(?:\?[^\s]*)?$",
]

# URL validation pattern
URL_PATTERN: re.Pattern = re.compile(
    r'^https?://'
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'
    r'localhost|'
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
    r'(?::\d+)?'
    r'(?:/?|[/?]\S+)$',
    re.IGNORECASE
)

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 3: Configuration Data Classes
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass(frozen=True)
class TelegramConfig:
    """Telegram API configuration."""
    api_id: int
    api_hash: str
    bot_token: str
    owner_id: int
    admin_ids: FrozenSet[int] = frozenset()
    session_name: str = "video_downloader_bot"
    workers: int = 8
    max_concurrent_transmissions: int = 4
    
    def __post_init__(self) -> None:
        """Validate Telegram configuration."""
        if not self.api_id or self.api_id <= 0:
            raise ValueError("Invalid API_ID")
        if not self.api_hash or len(self.api_hash) != 32:
            raise ValueError("Invalid API_HASH (must be 32 characters)")
        if not self.bot_token or ":" not in self.bot_token:
            raise ValueError("Invalid BOT_TOKEN format")


@dataclass(frozen=True)
class DownloadConfig:
    """Download settings configuration."""
    temp_dir: Path = TEMP_DIR
    downloads_dir: Path = DOWNLOADS_DIR
    default_quality: str = "1080"
    max_file_size: int = TELEGRAM_FILE_LIMIT
    chunk_size: int = CHUNK_SIZE
    max_retries: int = MAX_RETRIES
    timeout: int = DOWNLOAD_TIMEOUT
    concurrent_fragments: int = 4
    ffmpeg_location: Optional[str] = None
    prefer_ffmpeg: bool = True
    merge_output_format: str = OUTPUT_VIDEO_FORMAT
    
    def __post_init__(self) -> None:
        """Validate and create directories."""
        object.__setattr__(self, 'temp_dir', Path(self.temp_dir))
        object.__setattr__(self, 'downloads_dir', Path(self.downloads_dir))


@dataclass(frozen=True)
class RateLimitConfig:
    """Rate limiting configuration."""
    daily_limit: int = DEFAULT_DAILY_LIMIT
    concurrent_limit: int = DEFAULT_CONCURRENT_LIMIT
    vip_daily_limit: int = VIP_DAILY_LIMIT
    vip_concurrent_limit: int = VIP_CONCURRENT_LIMIT
    global_concurrent_limit: int = GLOBAL_CONCURRENT_LIMIT
    cooldown_period: int = COOLDOWN_PERIOD
    enable_rate_limit: bool = True


@dataclass(frozen=True)
class CacheConfig:
    """Caching configuration."""
    enabled: bool = True
    ttl: int = CACHE_TTL
    max_size: int = 1000
    cache_dir: Path = CACHE_DIR
    cache_thumbnails: bool = True
    cache_metadata: bool = True


@dataclass(frozen=True)
class LoggingConfig:
    """Logging configuration."""
    level: str = "INFO"
    log_dir: Path = LOGS_DIR
    max_bytes: int = 10 * 1024 * 1024  # 10 MB
    backup_count: int = 30
    format_string: str = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
    json_format: bool = False
    log_to_file: bool = True
    log_to_console: bool = True


@dataclass(frozen=True)
class SecurityConfig:
    """Security configuration."""
    encryption_key: Optional[str] = None
    cookie_encryption: bool = True
    secure_delete: bool = True
    input_sanitization: bool = True
    max_cookie_size: int = MAX_COOKIE_FILE_SIZE
    allowed_cookie_formats: FrozenSet[str] = frozenset({"txt", "json"})


@dataclass(frozen=True)
class DatabaseConfig:
    """Database configuration."""
    enabled: bool = True
    path: Path = DATABASE_DIR / "bot.db"
    connection_pool_size: int = 5
    timeout: int = 30
    backup_enabled: bool = True
    backup_interval: int = 86400  # 24 hours


@dataclass
class BotConfig:
    """Main bot configuration - aggregates all config sections."""
    telegram: TelegramConfig
    download: DownloadConfig = field(default_factory=DownloadConfig)
    rate_limit: RateLimitConfig = field(default_factory=RateLimitConfig)
    cache: CacheConfig = field(default_factory=CacheConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    security: SecurityConfig = field(default_factory=SecurityConfig)
    database: DatabaseConfig = field(default_factory=DatabaseConfig)
    
    # Language settings
    default_language: str = DEFAULT_LANGUAGE
    fallback_language: str = FALLBACK_LANGUAGE
    
    # Feature flags
    enable_cookies: bool = True
    enable_history: bool = True
    enable_stats: bool = True
    enable_admin_panel: bool = True
    enable_broadcast: bool = True
    enable_vip_system: bool = True
    
    # Maintenance mode
    maintenance_mode: bool = False
    maintenance_message: str = ""


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 4: Configuration Loading and Validation
# ═══════════════════════════════════════════════════════════════════════════════

def get_env(key: str, default: Any = None, required: bool = False, 
            cast: type = str) -> Any:
    """
    Get environment variable with type casting and validation.
    
    Args:
        key: Environment variable name
        default: Default value if not found
        required: Raise error if required and not found
        cast: Type to cast the value to
        
    Returns:
        Casted environment variable value
        
    Raises:
        ValueError: If required variable is missing or cast fails
    """
    value = os.getenv(key)
    
    if value is None:
        if required:
            raise ValueError(f"Required environment variable '{key}' is not set")
        return default
    
    try:
        if cast == bool:
            return value.lower() in ("true", "1", "yes", "on")
        elif cast == list:
            return [item.strip() for item in value.split(",") if item.strip()]
        elif cast == frozenset:
            items = [int(item.strip()) for item in value.split(",") if item.strip()]
            return frozenset(items)
        return cast(value)
    except (ValueError, TypeError) as e:
        raise ValueError(f"Failed to cast '{key}' to {cast.__name__}: {e}")


def ensure_directories() -> None:
    """Create all required directories if they don't exist."""
    directories = [
        TEMP_DIR,
        DOWNLOADS_DIR,
        COOKIES_DIR,
        LOGS_DIR,
        CACHE_DIR,
        DATABASE_DIR,
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)


def validate_ffmpeg() -> Optional[str]:
    """
    Check if FFmpeg is available and return its path.
    
    Returns:
        Path to FFmpeg if found, None otherwise
    """
    import shutil
    
    # Check environment variable first
    ffmpeg_path = os.getenv("FFMPEG_PATH")
    if ffmpeg_path and Path(ffmpeg_path).exists():
        return ffmpeg_path
    
    # Check system PATH
    ffmpeg = shutil.which("ffmpeg")
    if ffmpeg:
        return ffmpeg
    
    # Common installation paths
    common_paths = [
        "/usr/bin/ffmpeg",
        "/usr/local/bin/ffmpeg",
        "/opt/homebrew/bin/ffmpeg",  # macOS Homebrew
        r"C:\ffmpeg\bin\ffmpeg.exe",  # Windows
    ]
    
    for path in common_paths:
        if Path(path).exists():
            return path
    
    return None


@lru_cache(maxsize=1)
def load_config() -> BotConfig:
    """
    Load and validate all configuration from environment variables.
    
    Returns:
        Complete BotConfig instance
        
    Raises:
        ValueError: If required configuration is missing or invalid
    """
    # Ensure directories exist
    ensure_directories()
    
    # Load Telegram configuration (required)
    telegram_config = TelegramConfig(
        api_id=get_env("API_ID", required=True, cast=int),
        api_hash=get_env("API_HASH", required=True),
        bot_token=get_env("BOT_TOKEN", required=True),
        owner_id=get_env("OWNER_ID", required=True, cast=int),
        admin_ids=get_env("ADMIN_IDS", default=frozenset(), cast=frozenset),
        session_name=get_env("SESSION_NAME", default="video_downloader_bot"),
        workers=get_env("WORKERS", default=8, cast=int),
        max_concurrent_transmissions=get_env("MAX_CONCURRENT_TRANSMISSIONS", default=4, cast=int),
    )
    
    # Load download configuration
    download_config = DownloadConfig(
        temp_dir=Path(get_env("TEMP_DIR", default=str(TEMP_DIR))),
        downloads_dir=Path(get_env("DOWNLOADS_DIR", default=str(DOWNLOADS_DIR))),
        default_quality=get_env("DEFAULT_QUALITY", default="1080"),
        max_file_size=get_env("MAX_FILE_SIZE", default=TELEGRAM_FILE_LIMIT, cast=int),
        chunk_size=get_env("CHUNK_SIZE", default=CHUNK_SIZE, cast=int),
        max_retries=get_env("MAX_RETRIES", default=MAX_RETRIES, cast=int),
        timeout=get_env("DOWNLOAD_TIMEOUT", default=DOWNLOAD_TIMEOUT, cast=int),
        concurrent_fragments=get_env("CONCURRENT_FRAGMENTS", default=4, cast=int),
        ffmpeg_location=validate_ffmpeg(),
        prefer_ffmpeg=get_env("PREFER_FFMPEG", default=True, cast=bool),
        merge_output_format=get_env("MERGE_OUTPUT_FORMAT", default=OUTPUT_VIDEO_FORMAT),
    )
    
    # Load rate limit configuration
    rate_limit_config = RateLimitConfig(
        daily_limit=get_env("DAILY_LIMIT", default=DEFAULT_DAILY_LIMIT, cast=int),
        concurrent_limit=get_env("CONCURRENT_LIMIT", default=DEFAULT_CONCURRENT_LIMIT, cast=int),
        vip_daily_limit=get_env("VIP_DAILY_LIMIT", default=VIP_DAILY_LIMIT, cast=int),
        vip_concurrent_limit=get_env("VIP_CONCURRENT_LIMIT", default=VIP_CONCURRENT_LIMIT, cast=int),
        global_concurrent_limit=get_env("GLOBAL_CONCURRENT_LIMIT", default=GLOBAL_CONCURRENT_LIMIT, cast=int),
        cooldown_period=get_env("COOLDOWN_PERIOD", default=COOLDOWN_PERIOD, cast=int),
        enable_rate_limit=get_env("ENABLE_RATE_LIMIT", default=True, cast=bool),
    )
    
    # Load cache configuration
    cache_config = CacheConfig(
        enabled=get_env("CACHE_ENABLED", default=True, cast=bool),
        ttl=get_env("CACHE_TTL", default=CACHE_TTL, cast=int),
        max_size=get_env("CACHE_MAX_SIZE", default=1000, cast=int),
        cache_dir=Path(get_env("CACHE_DIR", default=str(CACHE_DIR))),
        cache_thumbnails=get_env("CACHE_THUMBNAILS", default=True, cast=bool),
        cache_metadata=get_env("CACHE_METADATA", default=True, cast=bool),
    )
    
    # Load logging configuration
    logging_config = LoggingConfig(
        level=get_env("LOG_LEVEL", default="INFO"),
        log_dir=Path(get_env("LOG_DIR", default=str(LOGS_DIR))),
        max_bytes=get_env("LOG_MAX_BYTES", default=10 * 1024 * 1024, cast=int),
        backup_count=get_env("LOG_BACKUP_COUNT", default=30, cast=int),
        json_format=get_env("LOG_JSON_FORMAT", default=False, cast=bool),
        log_to_file=get_env("LOG_TO_FILE", default=True, cast=bool),
        log_to_console=get_env("LOG_TO_CONSOLE", default=True, cast=bool),
    )
    
    # Load security configuration
    security_config = SecurityConfig(
        encryption_key=get_env("ENCRYPTION_KEY"),
        cookie_encryption=get_env("COOKIE_ENCRYPTION", default=True, cast=bool),
        secure_delete=get_env("SECURE_DELETE", default=True, cast=bool),
        input_sanitization=get_env("INPUT_SANITIZATION", default=True, cast=bool),
        max_cookie_size=get_env("MAX_COOKIE_SIZE", default=MAX_COOKIE_FILE_SIZE, cast=int),
    )
    
    # Load database configuration
    database_config = DatabaseConfig(
        enabled=get_env("DATABASE_ENABLED", default=True, cast=bool),
        path=Path(get_env("DATABASE_PATH", default=str(DATABASE_DIR / "bot.db"))),
        connection_pool_size=get_env("DB_POOL_SIZE", default=5, cast=int),
        timeout=get_env("DB_TIMEOUT", default=30, cast=int),
        backup_enabled=get_env("DB_BACKUP_ENABLED", default=True, cast=bool),
        backup_interval=get_env("DB_BACKUP_INTERVAL", default=86400, cast=int),
    )
    
    # Create main configuration
    config = BotConfig(
        telegram=telegram_config,
        download=download_config,
        rate_limit=rate_limit_config,
        cache=cache_config,
        logging=logging_config,
        security=security_config,
        database=database_config,
        default_language=get_env("DEFAULT_LANGUAGE", default=DEFAULT_LANGUAGE),
        fallback_language=get_env("FALLBACK_LANGUAGE", default=FALLBACK_LANGUAGE),
        enable_cookies=get_env("ENABLE_COOKIES", default=True, cast=bool),
        enable_history=get_env("ENABLE_HISTORY", default=True, cast=bool),
        enable_stats=get_env("ENABLE_STATS", default=True, cast=bool),
        enable_admin_panel=get_env("ENABLE_ADMIN_PANEL", default=True, cast=bool),
        enable_broadcast=get_env("ENABLE_BROADCAST", default=True, cast=bool),
        enable_vip_system=get_env("ENABLE_VIP_SYSTEM", default=True, cast=bool),
        maintenance_mode=get_env("MAINTENANCE_MODE", default=False, cast=bool),
        maintenance_message=get_env("MAINTENANCE_MESSAGE", default=""),
    )
    
    return config


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 5: Helper Functions
# ═══════════════════════════════════════════════════════════════════════════════

def detect_platform(url: str) -> Platform:
    """
    Detect the platform from a given URL.
    
    Args:
        url: The video URL to check
        
    Returns:
        Platform enum value
    """
    url = url.lower().strip()
    
    for platform, patterns in PLATFORM_PATTERNS.items():
        for pattern in patterns:
            if re.match(pattern, url, re.IGNORECASE):
                return Platform(platform)
    
    # Check for direct links
    for pattern in DIRECT_LINK_PATTERNS:
        if re.match(pattern, url, re.IGNORECASE):
            return Platform.DIRECT
    
    return Platform.UNKNOWN


def is_valid_url(url: str) -> bool:
    """
    Validate if a string is a valid URL.
    
    Args:
        url: String to validate
        
    Returns:
        True if valid URL, False otherwise
    """
    return bool(URL_PATTERN.match(url))


def get_quality_format(quality: str) -> str:
    """
    Get the yt-dlp format string for a given quality.
    
    Args:
        quality: Quality string (e.g., "1080", "720", "audio")
        
    Returns:
        yt-dlp format string
    """
    return QUALITY_PRESETS.get(quality, QUALITY_PRESETS["auto"])


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human-readable format.
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Formatted string (e.g., "1.5 GB")
    """
    if size_bytes < 0:
        return "Unknown"
    
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if abs(size_bytes) < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    
    return f"{size_bytes:.1f} PB"


def format_duration(seconds: int) -> str:
    """
    Format duration in human-readable format.
    
    Args:
        seconds: Duration in seconds
        
    Returns:
        Formatted string (e.g., "1:23:45")
    """
    if seconds < 0:
        return "Unknown"
    
    hours, remainder = divmod(int(seconds), 3600)
    minutes, secs = divmod(remainder, 60)
    
    if hours > 0:
        return f"{hours}:{minutes:02d}:{secs:02d}"
    return f"{minutes}:{secs:02d}"


def get_language_info(code: str) -> Dict[str, Any]:
    """
    Get language information by code.
    
    Args:
        code: Language code (e.g., "fa", "en")
        
    Returns:
        Dictionary with language info
    """
    return SUPPORTED_LANGUAGES.get(code, SUPPORTED_LANGUAGES[DEFAULT_LANGUAGE])


def is_rtl_language(code: str) -> bool:
    """
    Check if a language is Right-to-Left.
    
    Args:
        code: Language code
        
    Returns:
        True if RTL, False otherwise
    """
    return SUPPORTED_LANGUAGES.get(code, {}).get("rtl", False)


def is_admin(user_id: int, config: BotConfig) -> bool:
    """
    Check if a user is an admin.
    
    Args:
        user_id: Telegram user ID
        config: Bot configuration
        
    Returns:
        True if admin, False otherwise
    """
    return user_id == config.telegram.owner_id or user_id in config.telegram.admin_ids


def is_owner(user_id: int, config: BotConfig) -> bool:
    """
    Check if a user is the owner.
    
    Args:
        user_id: Telegram user ID
        config: Bot configuration
        
    Returns:
        True if owner, False otherwise
    """
    return user_id == config.telegram.owner_id


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 6: YT-DLP Options Generator
# ═══════════════════════════════════════════════════════════════════════════════

def get_ytdlp_options(
    config: BotConfig,
    quality: str = "auto",
    audio_only: bool = False,
    output_path: Optional[Path] = None,
    cookie_file: Optional[Path] = None,
    progress_hook: Optional[callable] = None,
) -> Dict[str, Any]:
    """
    Generate yt-dlp options dictionary.
    
    Args:
        config: Bot configuration
        quality: Desired quality
        audio_only: Extract audio only
        output_path: Output file path
        cookie_file: Path to cookies file
        progress_hook: Progress callback function
        
    Returns:
        Dictionary of yt-dlp options
    """
    options: Dict[str, Any] = {
        # Format selection
        "format": "bestaudio/best" if audio_only else get_quality_format(quality),
        
        # Output settings
        "outtmpl": str(output_path) if output_path else "%(title)s.%(ext)s",
        "merge_output_format": None if audio_only else config.download.merge_output_format,
        
        # Network settings
        "socket_timeout": config.download.timeout,
        "retries": config.download.max_retries,
        "fragment_retries": config.download.max_retries,
        "concurrent_fragment_downloads": config.download.concurrent_fragments,
        
        # Behavior settings
        "quiet": True,
        "no_warnings": True,
        "ignoreerrors": False,
        "noplaylist": True,
        "extract_flat": False,
        "geo_bypass": True,
        "nocheckcertificate": True,
        
        # Metadata
        "writeinfojson": False,
        "writethumbnail": False,
        "writesubtitles": False,
        
        # FFmpeg settings
        "prefer_ffmpeg": config.download.prefer_ffmpeg,
        "postprocessor_args": ["-hide_banner", "-loglevel", "error"],
    }
    
    # Add FFmpeg location if available
    if config.download.ffmpeg_location:
        options["ffmpeg_location"] = config.download.ffmpeg_location
    
    # Add cookie file if provided
    if cookie_file and cookie_file.exists():
        options["cookiefile"] = str(cookie_file)
    
    # Add progress hook if provided
    if progress_hook:
        options["progress_hooks"] = [progress_hook]
    
    # Audio-only post-processing
    if audio_only:
        options["postprocessors"] = [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "320",
        }]
    
    return options


def get_info_extract_options(
    config: BotConfig,
    cookie_file: Optional[Path] = None,
) -> Dict[str, Any]:
    """
    Generate yt-dlp options for info extraction only.
    
    Args:
        config: Bot configuration
        cookie_file: Path to cookies file
        
    Returns:
        Dictionary of yt-dlp options for extraction
    """
    options: Dict[str, Any] = {
        "quiet": True,
        "no_warnings": True,
        "ignoreerrors": False,
        "noplaylist": True,
        "extract_flat": False,
        "geo_bypass": True,
        "nocheckcertificate": True,
        "socket_timeout": VIDEO_INFO_TIMEOUT,
        "skip_download": True,
        "writeinfojson": False,
        "writethumbnail": False,
        "format": "bestvideo+bestaudio/best",
    }
    
    if cookie_file and cookie_file.exists():
        options["cookiefile"] = str(cookie_file)
    
    if config.download.ffmpeg_location:
        options["ffmpeg_location"] = config.download.ffmpeg_location
    
    return options


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 7: Module Initialization
# ═══════════════════════════════════════════════════════════════════════════════

# Pre-load configuration on module import for validation
try:
    _config = load_config()
except ValueError as e:
    print(f"❌ Configuration Error: {e}")
    print("Please check your .env file and ensure all required variables are set.")
    sys.exit(1)


def get_config() -> BotConfig:
    """
    Get the loaded configuration instance.
    
    Returns:
        BotConfig instance
    """
    return _config


# Export commonly used items
__all__ = [
    # Version info
    "VERSION",
    "BUILD_DATE",
    "CODENAME",
    
    # Enums
    "LogLevel",
    "VideoQuality",
    "DownloadStatus",
    "Platform",
    
    # Constants
    "SUPPORTED_LANGUAGES",
    "DEFAULT_LANGUAGE",
    "FALLBACK_LANGUAGE",
    "QUALITY_PRESETS",
    "TELEGRAM_FILE_LIMIT",
    "PROGRESS_UPDATE_INTERVAL",
    
    # Paths
    "BASE_DIR",
    "TEMP_DIR",
    "DOWNLOADS_DIR",
    "COOKIES_DIR",
    "LOGS_DIR",
    "CACHE_DIR",
    "DATABASE_DIR",
    "LANGUAGES_DIR",
    
    # Config classes
    "TelegramConfig",
    "DownloadConfig",
    "RateLimitConfig",
    "CacheConfig",
    "LoggingConfig",
    "SecurityConfig",
    "DatabaseConfig",
    "BotConfig",
    
    # Functions
    "load_config",
    "get_config",
    "get_env",
    "ensure_directories",
    "validate_ffmpeg",
    "detect_platform",
    "is_valid_url",
    "get_quality_format",
    "format_file_size",
    "format_duration",
    "get_language_info",
    "is_rtl_language",
    "is_admin",
    "is_owner",
    "get_ytdlp_options",
    "get_info_extract_options",
]


if __name__ == "__main__":
    # Test configuration loading
    print(f"✅ Video Downloader Bot Configuration v{VERSION}")
    print(f"📁 Base Directory: {BASE_DIR}")
    print(f"🔧 FFmpeg: {validate_ffmpeg() or 'Not Found'}")
    print(f"🌐 Default Language: {DEFAULT_LANGUAGE}")
    print(f"📊 Supported Languages: {', '.join(SUPPORTED_LANGUAGES.keys())}")
    print(f"✅ Configuration loaded successfully!")