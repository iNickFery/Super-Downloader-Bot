#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    Professional Video Downloader Bot                         ║
║                         Language Utilities                                   ║
║                                                                              ║
║  Helper functions for language handling, formatting, and validation.         ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

from __future__ import annotations

import re
import html
from typing import Dict, Any, Optional, List, Union
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 1: Number Formatting
# ═══════════════════════════════════════════════════════════════════════════════

# Persian/Arabic digits mapping
PERSIAN_DIGITS = "۰۱۲۳۴۵۶۷۸۹"
ARABIC_DIGITS = "٠١٢٣٤٥٦٧٨٩"
ENGLISH_DIGITS = "0123456789"


def to_persian_digits(text: str) -> str:
    """
    Convert English/Arabic digits to Persian digits.
    
    Args:
        text: Text containing digits
        
    Returns:
        Text with Persian digits
    """
    result = str(text)
    for i, digit in enumerate(ENGLISH_DIGITS):
        result = result.replace(digit, PERSIAN_DIGITS[i])
    for i, digit in enumerate(ARABIC_DIGITS):
        result = result.replace(digit, PERSIAN_DIGITS[i])
    return result


def to_english_digits(text: str) -> str:
    """
    Convert Persian/Arabic digits to English digits.
    
    Args:
        text: Text containing digits
        
    Returns:
        Text with English digits
    """
    result = str(text)
    for i, digit in enumerate(PERSIAN_DIGITS):
        result = result.replace(digit, ENGLISH_DIGITS[i])
    for i, digit in enumerate(ARABIC_DIGITS):
        result = result.replace(digit, ENGLISH_DIGITS[i])
    return result


def format_number(
    number: Union[int, float],
    lang_code: str = "fa",
    decimal_places: int = 2,
    use_grouping: bool = True
) -> str:
    """
    Format a number according to language conventions.
    
    Args:
        number: Number to format
        lang_code: Language code
        decimal_places: Number of decimal places for floats
        use_grouping: Whether to use thousand separators
        
    Returns:
        Formatted number string
    """
    if isinstance(number, float):
        formatted = f"{number:,.{decimal_places}f}" if use_grouping else f"{number:.{decimal_places}f}"
    else:
        formatted = f"{number:,}" if use_grouping else str(number)
    
    # For Persian, convert digits and swap separators
    if lang_code == "fa":
        # Persian uses different decimal separator
        formatted = formatted.replace(",", "٬")  # Arabic thousands separator
        formatted = to_persian_digits(formatted)
    
    return formatted


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 2: Date and Time Formatting
# ═══════════════════════════════════════════════════════════════════════════════

PERSIAN_MONTHS = [
    "فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور",
    "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"
]

PERSIAN_WEEKDAYS = [
    "شنبه", "یکشنبه", "دوشنبه", "سه‌شنبه", "چهارشنبه", "پنجشنبه", "جمعه"
]

ENGLISH_MONTHS = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

ENGLISH_WEEKDAYS = [
    "Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"
]


def format_duration_text(
    seconds: int,
    lang_code: str = "fa",
    short: bool = False
) -> str:
    """
    Format duration in human-readable text.
    
    Args:
        seconds: Duration in seconds
        lang_code: Language code
        short: Use short format
        
    Returns:
        Formatted duration string
    """
    if seconds < 0:
        return "نامشخص" if lang_code == "fa" else "Unknown"
    
    hours, remainder = divmod(int(seconds), 3600)
    minutes, secs = divmod(remainder, 60)
    
    if lang_code == "fa":
        if short:
            if hours > 0:
                return to_persian_digits(f"{hours}:{minutes:02d}:{secs:02d}")
            return to_persian_digits(f"{minutes}:{secs:02d}")
        else:
            parts = []
            if hours > 0:
                parts.append(f"{to_persian_digits(str(hours))} ساعت")
            if minutes > 0:
                parts.append(f"{to_persian_digits(str(minutes))} دقیقه")
            if secs > 0 or not parts:
                parts.append(f"{to_persian_digits(str(secs))} ثانیه")
            return " و ".join(parts)
    else:
        if short:
            if hours > 0:
                return f"{hours}:{minutes:02d}:{secs:02d}"
            return f"{minutes}:{secs:02d}"
        else:
            parts = []
            if hours > 0:
                parts.append(f"{hours} hour{'s' if hours > 1 else ''}")
            if minutes > 0:
                parts.append(f"{minutes} minute{'s' if minutes > 1 else ''}")
            if secs > 0 or not parts:
                parts.append(f"{secs} second{'s' if secs > 1 else ''}")
            return " and ".join(parts)


def format_time_ago(
    timestamp: datetime,
    lang_code: str = "fa"
) -> str:
    """
    Format a timestamp as 'time ago' text.
    
    Args:
        timestamp: Datetime object
        lang_code: Language code
        
    Returns:
        Formatted 'time ago' string
    """
    now = datetime.now()
    diff = now - timestamp
    
    seconds = int(diff.total_seconds())
    
    if seconds < 0:
        return "در آینده" if lang_code == "fa" else "in the future"
    
    intervals = [
        (31536000, ("سال", "year")),
        (2592000, ("ماه", "month")),
        (604800, ("هفته", "week")),
        (86400, ("روز", "day")),
        (3600, ("ساعت", "hour")),
        (60, ("دقیقه", "minute")),
        (1, ("ثانیه", "second")),
    ]
    
    for interval_seconds, (fa_unit, en_unit) in intervals:
        count = seconds // interval_seconds
        if count >= 1:
            if lang_code == "fa":
                return f"{to_persian_digits(str(count))} {fa_unit} پیش"
            else:
                plural = "s" if count > 1 else ""
                return f"{count} {en_unit}{plural} ago"
    
    return "همین الان" if lang_code == "fa" else "just now"


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 3: File Size Formatting
# ═══════════════════════════════════════════════════════════════════════════════

def format_file_size(
    size_bytes: int,
    lang_code: str = "fa",
    decimal_places: int = 1
) -> str:
    """
    Format file size in human-readable format.
    
    Args:
        size_bytes: Size in bytes
        lang_code: Language code
        decimal_places: Number of decimal places
        
    Returns:
        Formatted size string
    """
    if size_bytes < 0:
        return "نامشخص" if lang_code == "fa" else "Unknown"
    
    units_fa = ["بایت", "کیلوبایت", "مگابایت", "گیگابایت", "ترابایت"]
    units_en = ["B", "KB", "MB", "GB", "TB"]
    
    units = units_fa if lang_code == "fa" else units_en
    
    size = float(size_bytes)
    unit_index = 0
    
    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024
        unit_index += 1
    
    formatted_size = f"{size:.{decimal_places}f}"
    
    if lang_code == "fa":
        formatted_size = to_persian_digits(formatted_size)
    
    return f"{formatted_size} {units[unit_index]}"


def format_speed(
    bytes_per_second: float,
    lang_code: str = "fa"
) -> str:
    """
    Format download/upload speed.
    
    Args:
        bytes_per_second: Speed in bytes per second
        lang_code: Language code
        
    Returns:
        Formatted speed string
    """
    size = format_file_size(int(bytes_per_second), lang_code, 1)
    suffix = "/ث" if lang_code == "fa" else "/s"
    return f"{size}{suffix}"


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 4: Text Formatting and Sanitization
# ═══════════════════════════════════════════════════════════════════════════════

def escape_html(text: str) -> str:
    """
    Escape HTML special characters for safe display in Telegram.
    
    Args:
        text: Text to escape
        
    Returns:
        Escaped text
    """
    return html.escape(str(text))


def escape_markdown(text: str) -> str:
    """
    Escape Markdown special characters.
    
    Args:
        text: Text to escape
        
    Returns:
        Escaped text
    """
    special_chars = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    result = str(text)
    for char in special_chars:
        result = result.replace(char, f"\\{char}")
    return result


def truncate_text(
    text: str,
    max_length: int = 100,
    suffix: str = "..."
) -> str:
    """
    Truncate text to a maximum length.
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add when truncated
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def clean_filename(filename: str) -> str:
    """
    Clean a filename by removing/replacing invalid characters.
    
    Args:
        filename: Original filename
        
    Returns:
        Cleaned filename
    """
    # Remove invalid characters
    cleaned = re.sub(r'[<>:"/\\|?*]', '', filename)
    # Replace multiple spaces/underscores with single ones
    cleaned = re.sub(r'[\s_]+', '_', cleaned)
    # Remove leading/trailing spaces and dots
    cleaned = cleaned.strip('. ')
    # Limit length
    if len(cleaned) > 200:
        cleaned = cleaned[:200]
    return cleaned or "video"


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 5: Progress Bar Generation
# ═══════════════════════════════════════════════════════════════════════════════

def generate_progress_bar(
    progress: float,
    length: int = 20,
    filled_char: str = "█",
    empty_char: str = "░",
    show_percentage: bool = True,
    lang_code: str = "fa"
) -> str:
    """
    Generate a text-based progress bar.
    
    Args:
        progress: Progress value (0.0 to 1.0)
        length: Length of the progress bar
        filled_char: Character for filled portion
        empty_char: Character for empty portion
        show_percentage: Whether to show percentage
        lang_code: Language code for number formatting
        
    Returns:
        Progress bar string
    """
    progress = max(0.0, min(1.0, progress))
    filled_length = int(length * progress)
    bar = filled_char * filled_length + empty_char * (length - filled_length)
    
    if show_percentage:
        percentage = f"{progress * 100:.1f}%"
        if lang_code == "fa":
            percentage = to_persian_digits(percentage)
        return f"{bar} {percentage}"
    
    return bar


def generate_animated_progress(
    progress: float,
    frame: int = 0
) -> str:
    """
    Generate an animated progress indicator.
    
    Args:
        progress: Progress value (0.0 to 1.0)
        frame: Animation frame number
        
    Returns:
        Animated progress string
    """
    # Different animation styles
    animations = [
        ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"],
        ["🕐", "🕑", "🕒", "🕓", "🕔", "🕕", "🕖", "🕗", "🕘", "🕙", "🕚", "🕛"],
        ["◐", "◓", "◑", "◒"],
        ["▁", "▂", "▃", "▄", "▅", "▆", "▇", "█"],
    ]
    
    spinner = animations[0]
    current_frame = spinner[frame % len(spinner)]
    
    return f"{current_frame} {generate_progress_bar(progress)}"


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 6: Quality Labels
# ═══════════════════════════════════════════════════════════════════════════════

def get_quality_label(
    height: int,
    fps: Optional[int] = None,
    lang_code: str = "fa"
) -> str:
    """
    Get a human-readable quality label.
    
    Args:
        height: Video height in pixels
        fps: Frames per second (optional)
        lang_code: Language code
        
    Returns:
        Quality label string
    """
    # Determine quality tier
    if height >= 2160:
        label = "4K Ultra HD" if lang_code == "en" else "۴K فوق‌العاده"
    elif height >= 1440:
        label = "2K QHD" if lang_code == "en" else "۲K کیفیت بالا"
    elif height >= 1080:
        label = "Full HD" if lang_code == "en" else "فول اچ‌دی"
    elif height >= 720:
        label = "HD" if lang_code == "en" else "اچ‌دی"
    elif height >= 480:
        label = "SD" if lang_code == "en" else "کیفیت متوسط"
    elif height >= 360:
        label = "Low" if lang_code == "en" else "کیفیت پایین"
    else:
        label = "Very Low" if lang_code == "en" else "کیفیت خیلی پایین"
    
    # Add resolution
    resolution = f"{height}p"
    if lang_code == "fa":
        resolution = to_persian_digits(resolution)
    
    # Add FPS if high frame rate
    if fps and fps > 30:
        fps_text = str(fps) if lang_code == "en" else to_persian_digits(str(fps))
        return f"{label} ({resolution}{fps_text})"
    
    return f"{label} ({resolution})"


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 7: Exports
# ═══════════════════════════════════════════════════════════════════════════════

__all__ = [
    # Number formatting
    "to_persian_digits",
    "to_english_digits",
    "format_number",
    
    # Time formatting
    "format_duration_text",
    "format_time_ago",
    
    # Size formatting
    "format_file_size",
    "format_speed",
    
    # Text formatting
    "escape_html",
    "escape_markdown",
    "truncate_text",
    "clean_filename",
    
    # Progress bar
    "generate_progress_bar",
    "generate_animated_progress",
    
    # Quality
    "get_quality_label",
]