#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    Professional Video Downloader Bot                         ║
║                         Language System - Main Handler                       ║
║                                                                              ║
║  This module provides:                                                       ║
║  - Automatic language file loading                                           ║
║  - Language switching functionality                                          ║
║  - RTL/LTR text direction handling                                           ║
║  - Fallback mechanism for missing translations                               ║
║  - Thread-safe language operations                                           ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

from __future__ import annotations

import os
import importlib
import logging
from pathlib import Path
from typing import Dict, Any, Optional, List, Set, Callable
from functools import lru_cache
from threading import Lock
import re

# Logger setup
logger = logging.getLogger(__name__)

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 1: Constants and Configuration
# ═══════════════════════════════════════════════════════════════════════════════

# Default and fallback languages
DEFAULT_LANGUAGE: str = "fa"
FALLBACK_LANGUAGE: str = "en"

# Language directory
LANGUAGES_DIR: Path = Path(__file__).parent

# RTL languages list
RTL_LANGUAGES: Set[str] = {"fa", "ar", "he", "ur", "ps", "ku"}

# Thread lock for safe operations
_language_lock = Lock()

# Loaded languages cache
_loaded_languages: Dict[str, Dict[str, Any]] = {}

# User language preferences (user_id -> language_code)
_user_languages: Dict[int, str] = {}


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 2: Language Loading System
# ═══════════════════════════════════════════════════════════════════════════════

def _discover_language_files() -> List[str]:
    """
    Discover all available language files in the languages directory.
    
    Returns:
        List of language codes (e.g., ['fa', 'en'])
    """
    language_codes = []
    
    for file in LANGUAGES_DIR.glob("lang_*.py"):
        # Extract language code from filename (lang_fa.py -> fa)
        match = re.match(r"lang_([a-z]{2})\.py$", file.name)
        if match:
            language_codes.append(match.group(1))
    
    return sorted(language_codes)


def _load_language_module(lang_code: str) -> Optional[Dict[str, Any]]:
    """
    Load a language module by its code.
    
    Args:
        lang_code: Two-letter language code (e.g., 'fa', 'en')
        
    Returns:
        Language dictionary or None if not found
    """
    try:
        module_name = f"languages.lang_{lang_code}"
        module = importlib.import_module(module_name)
        
        # Get the STRINGS dictionary from the module
        if hasattr(module, "STRINGS"):
            logger.info(f"✅ Loaded language: {lang_code}")
            return module.STRINGS
        else:
            logger.warning(f"⚠️ Language module {lang_code} has no STRINGS dictionary")
            return None
            
    except ImportError as e:
        logger.warning(f"⚠️ Could not load language '{lang_code}': {e}")
        return None
    except Exception as e:
        logger.error(f"❌ Error loading language '{lang_code}': {e}")
        return None


def load_all_languages() -> Dict[str, Dict[str, Any]]:
    """
    Load all available language files.
    
    Returns:
        Dictionary of all loaded languages
    """
    global _loaded_languages
    
    with _language_lock:
        if _loaded_languages:
            return _loaded_languages
        
        language_codes = _discover_language_files()
        
        for code in language_codes:
            lang_data = _load_language_module(code)
            if lang_data:
                _loaded_languages[code] = lang_data
        
        # Ensure default and fallback languages are loaded
        if DEFAULT_LANGUAGE not in _loaded_languages:
            logger.error(f"❌ Default language '{DEFAULT_LANGUAGE}' not found!")
        
        if FALLBACK_LANGUAGE not in _loaded_languages:
            logger.error(f"❌ Fallback language '{FALLBACK_LANGUAGE}' not found!")
        
        logger.info(f"📚 Loaded {len(_loaded_languages)} languages: {list(_loaded_languages.keys())}")
        
        return _loaded_languages


def reload_language(lang_code: str) -> bool:
    """
    Reload a specific language file (useful for hot-reloading).
    
    Args:
        lang_code: Language code to reload
        
    Returns:
        True if successful, False otherwise
    """
    global _loaded_languages
    
    with _language_lock:
        try:
            module_name = f"languages.lang_{lang_code}"
            
            # Remove from cache if exists
            if module_name in importlib.sys.modules:
                del importlib.sys.modules[module_name]
            
            # Reload
            lang_data = _load_language_module(lang_code)
            if lang_data:
                _loaded_languages[lang_code] = lang_data
                return True
            return False
            
        except Exception as e:
            logger.error(f"❌ Error reloading language '{lang_code}': {e}")
            return False


def reload_all_languages() -> int:
    """
    Reload all language files.
    
    Returns:
        Number of successfully reloaded languages
    """
    global _loaded_languages
    
    with _language_lock:
        _loaded_languages.clear()
        
    return len(load_all_languages())


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 3: Language Access Functions
# ═══════════════════════════════════════════════════════════════════════════════

def get_available_languages() -> List[Dict[str, Any]]:
    """
    Get list of all available languages with their metadata.
    
    Returns:
        List of language info dictionaries
    """
    if not _loaded_languages:
        load_all_languages()
    
    languages = []
    for code, data in _loaded_languages.items():
        languages.append({
            "code": code,
            "name": data.get("_meta", {}).get("name", code),
            "native_name": data.get("_meta", {}).get("native_name", code),
            "flag": data.get("_meta", {}).get("flag", "🌐"),
            "rtl": code in RTL_LANGUAGES,
        })
    
    return languages


def get_language(lang_code: str) -> Dict[str, Any]:
    """
    Get a complete language dictionary.
    
    Args:
        lang_code: Language code
        
    Returns:
        Language dictionary (falls back to default if not found)
    """
    if not _loaded_languages:
        load_all_languages()
    
    if lang_code in _loaded_languages:
        return _loaded_languages[lang_code]
    
    if FALLBACK_LANGUAGE in _loaded_languages:
        return _loaded_languages[FALLBACK_LANGUAGE]
    
    return _loaded_languages.get(DEFAULT_LANGUAGE, {})


def is_language_available(lang_code: str) -> bool:
    """
    Check if a language is available.
    
    Args:
        lang_code: Language code to check
        
    Returns:
        True if available, False otherwise
    """
    if not _loaded_languages:
        load_all_languages()
    
    return lang_code in _loaded_languages


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 4: User Language Management
# ═══════════════════════════════════════════════════════════════════════════════

def set_user_language(user_id: int, lang_code: str) -> bool:
    """
    Set a user's preferred language.
    
    Args:
        user_id: Telegram user ID
        lang_code: Language code
        
    Returns:
        True if set successfully, False if language not available
    """
    if not is_language_available(lang_code):
        return False
    
    with _language_lock:
        _user_languages[user_id] = lang_code
    
    return True


def get_user_language(user_id: int) -> str:
    """
    Get a user's preferred language.
    
    Args:
        user_id: Telegram user ID
        
    Returns:
        Language code (default if not set)
    """
    return _user_languages.get(user_id, DEFAULT_LANGUAGE)


def remove_user_language(user_id: int) -> None:
    """
    Remove a user's language preference (reset to default).
    
    Args:
        user_id: Telegram user ID
    """
    with _language_lock:
        _user_languages.pop(user_id, None)


def get_all_user_languages() -> Dict[int, str]:
    """
    Get all user language preferences.
    
    Returns:
        Dictionary of user_id -> language_code
    """
    return _user_languages.copy()


def load_user_languages(data: Dict[int, str]) -> None:
    """
    Load user language preferences from external source (e.g., database).
    
    Args:
        data: Dictionary of user_id -> language_code
    """
    global _user_languages
    
    with _language_lock:
        _user_languages.update(data)


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 5: Text Retrieval Functions
# ═══════════════════════════════════════════════════════════════════════════════

def get_text(
    key: str,
    lang_code: Optional[str] = None,
    user_id: Optional[int] = None,
    **kwargs
) -> str:
    """
    Get a translated text string with optional formatting.
    
    Args:
        key: Translation key (can be nested with dots, e.g., "errors.not_found")
        lang_code: Language code (optional, uses user's preference if user_id provided)
        user_id: User ID to get their preferred language
        **kwargs: Format arguments for the string
        
    Returns:
        Translated and formatted string
    """
    # Determine language
    if lang_code is None:
        if user_id is not None:
            lang_code = get_user_language(user_id)
        else:
            lang_code = DEFAULT_LANGUAGE
    
    # Get language dictionary
    lang_dict = get_language(lang_code)
    fallback_dict = get_language(FALLBACK_LANGUAGE) if lang_code != FALLBACK_LANGUAGE else None
    
    # Navigate to the key
    text = _get_nested_value(lang_dict, key)
    
    # Fallback to English if not found
    if text is None and fallback_dict:
        text = _get_nested_value(fallback_dict, key)
    
    # Return key if still not found
    if text is None:
        logger.warning(f"⚠️ Missing translation: '{key}' for language '{lang_code}'")
        return f"[{key}]"
    
    # Format the string if kwargs provided
    if kwargs:
        try:
            text = text.format(**kwargs)
        except KeyError as e:
            logger.warning(f"⚠️ Missing format key {e} for '{key}'")
        except Exception as e:
            logger.warning(f"⚠️ Format error for '{key}': {e}")
    
    return text


def _get_nested_value(dictionary: Dict[str, Any], key: str) -> Optional[str]:
    """
    Get a value from a nested dictionary using dot notation.
    
    Args:
        dictionary: The dictionary to search
        key: Dot-separated key (e.g., "errors.not_found")
        
    Returns:
        Value if found, None otherwise
    """
    keys = key.split(".")
    value = dictionary
    
    for k in keys:
        if isinstance(value, dict) and k in value:
            value = value[k]
        else:
            return None
    
    return value if isinstance(value, str) else None


def t(key: str, user_id: Optional[int] = None, **kwargs) -> str:
    """
    Shorthand for get_text().
    
    Args:
        key: Translation key
        user_id: User ID for language preference
        **kwargs: Format arguments
        
    Returns:
        Translated string
    """
    return get_text(key, user_id=user_id, **kwargs)


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 6: Text Direction and RTL Support
# ═══════════════════════════════════════════════════════════════════════════════

def is_rtl(lang_code: str) -> bool:
    """
    Check if a language is Right-to-Left.
    
    Args:
        lang_code: Language code
        
    Returns:
        True if RTL, False otherwise
    """
    return lang_code in RTL_LANGUAGES


def get_text_direction(lang_code: str) -> str:
    """
    Get text direction for a language.
    
    Args:
        lang_code: Language code
        
    Returns:
        'rtl' or 'ltr'
    """
    return "rtl" if is_rtl(lang_code) else "ltr"


def add_rtl_mark(text: str, lang_code: str) -> str:
    """
    Add RTL mark to text if language is RTL.
    
    Args:
        text: Text to process
        lang_code: Language code
        
    Returns:
        Text with RTL mark if needed
    """
    if is_rtl(lang_code):
        # Add Right-to-Left Mark (U+200F) at the beginning
        return "\u200F" + text
    return text


def format_rtl_text(text: str, lang_code: str) -> str:
    """
    Format text for proper RTL display in Telegram.
    
    Args:
        text: Text to format
        lang_code: Language code
        
    Returns:
        Properly formatted text
    """
    if not is_rtl(lang_code):
        return text
    
    # Add RTL embedding characters
    # RLE (Right-to-Left Embedding): U+202B
    # PDF (Pop Directional Formatting): U+202C
    return f"\u202B{text}\u202C"


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 7: Initialization
# ═══════════════════════════════════════════════════════════════════════════════

# Auto-load languages on module import
load_all_languages()


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 8: Exports
# ═══════════════════════════════════════════════════════════════════════════════

__all__ = [
    # Constants
    "DEFAULT_LANGUAGE",
    "FALLBACK_LANGUAGE",
    "RTL_LANGUAGES",
    "LANGUAGES_DIR",
    
    # Loading functions
    "load_all_languages",
    "reload_language",
    "reload_all_languages",
    
    # Language access
    "get_available_languages",
    "get_language",
    "is_language_available",
    
    # User language management
    "set_user_language",
    "get_user_language",
    "remove_user_language",
    "get_all_user_languages",
    "load_user_languages",
    
    # Text retrieval
    "get_text",
    "t",
    
    # RTL support
    "is_rtl",
    "get_text_direction",
    "add_rtl_mark",
    "format_rtl_text",
]