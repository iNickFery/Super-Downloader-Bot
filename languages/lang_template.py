#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    Professional Video Downloader Bot                         ║
║                         Language Template                                    ║
║                                                                              ║
║  ╔═══════════════════════════════════════════════════════════════════════╗   ║
║  ║                    HOW TO ADD A NEW LANGUAGE                          ║   ║
║  ╠═══════════════════════════════════════════════════════════════════════╣   ║
║  ║  1. Copy this file to 'lang_XX.py' where XX is language code          ║   ║
║  ║     Example: lang_de.py for German, lang_es.py for Spanish            ║   ║
║  ║                                                                       ║   ║
║  ║  2. Update the "_meta" section with your language info                ║   ║
║  ║                                                                       ║   ║
║  ║  3. Translate ALL strings (keep the keys, change the values)          ║   ║
║  ║                                                                       ║   ║
║  ║  4. Save the file - the bot will auto-detect it!                      ║   ║
║  ║                                                                       ║   ║
║  ║  That's it! No other code changes needed!                             ║   ║
║  ╚═══════════════════════════════════════════════════════════════════════╝   ║
║                                                                              ║
║  NOTES:                                                                      ║
║  • Keep all {variable} placeholders intact                                   ║
║  • Keep HTML tags (<b>, </b>, etc.) intact                                   ║
║  • For RTL languages (Arabic, Hebrew, etc.), set "rtl": True in _meta        ║
║  • Test your translations by changing language in the bot                    ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

LANGUAGE CODES REFERENCE:
-------------------------
ar = Arabic (العربية)          - RTL
de = German (Deutsch)
es = Spanish (Español)
fr = French (Français)
hi = Hindi (हिन्दी)
id = Indonesian (Bahasa Indonesia)
it = Italian (Italiano)
ja = Japanese (日本語)
ko = Korean (한국어)
nl = Dutch (Nederlands)
pl = Polish (Polski)
pt = Portuguese (Português)
ru = Russian (Русский)
tr = Turkish (Türkçe)
uk = Ukrainian (Українська)
ur = Urdu (اردو)              - RTL
zh = Chinese (中文)
"""

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORTANT: This is a TEMPLATE file.
# Copy this file and rename it to lang_XX.py (where XX is your language code)
# Then translate all the strings below.
# ═══════════════════════════════════════════════════════════════════════════════

STRINGS = {
    # ═══════════════════════════════════════════════════════════════════════════
    # META INFORMATION - UPDATE THIS SECTION FIRST!
    # ═══════════════════════════════════════════════════════════════════════════
    "_meta": {
        "code": "xx",                    # ← Change to your language code (e.g., "de", "es")
        "name": "Language Name",         # ← English name of the language
        "native_name": "Native Name",    # ← Name in the language itself
        "flag": "🏳️",                    # ← Flag emoji for the language
        "rtl": False,                    # ← Set True for Right-to-Left languages
        "version": "2.0.0",
        "author": "Your Name",           # ← Your name/username (optional)
    },
    
    # ═══════════════════════════════════════════════════════════════════════════
    # WELCOME & START MESSAGES
    # Translate the text but keep {name} and other {variables} as they are
    # ═══════════════════════════════════════════════════════════════════════════
    "start": {
        "welcome": """🎬 <b>Welcome to Video Downloader Bot!</b>

🌟 <b>The Most Powerful Video Downloader on Telegram</b>

I can download videos from <b>over 1000+ websites</b> for you!

━━━━━━━━━━━━━━━━━━━━
🔹 <b>Popular Platforms:</b>
• YouTube, Instagram, Twitter
• TikTok, Facebook, Twitch
• Aparat, Namasha, and more...

🔹 <b>Special Features:</b>
• Quality up to 4K Ultra HD
• High-quality audio extraction
• Private content support
• Super fast download speed
━━━━━━━━━━━━━━━━━━━━

📎 <b>To start, just send a video link!</b>""",

        "welcome_back": """👋 <b>Welcome back, {name}!</b>

🎬 Ready to download videos.

📎 Send the video link you want to download.""",

        "first_time_user": """🎉 <b>Welcome, {name}!</b>

This is your first time using the bot.

💡 <b>Quick Guide:</b>
1. Copy the video link
2. Send the link here
3. Select your preferred quality
4. Wait for the download!

For complete guide use /help""",
    },
    
    # ═══════════════════════════════════════════════════════════════════════════
    # HELP MESSAGES
    # ═══════════════════════════════════════════════════════════════════════════
    "help": {
        "main": """📚 <b>Video Downloader Bot Guide</b>

━━━━━━━━━━━━━━━━━━━━
🎬 <b>How to use:</b>
Just send the video link!

━━━━━━━━━━━━━━━━━━━━
📋 <b>Commands:</b>

🔹 <b>Main Commands:</b>
• /start - Start the bot
• /help - Show this guide
• /language - Change language

🔹 <b>Cookie Management:</b>
• /cookie - Upload cookie
• /listcookies - List cookies
• /deletecookie - Delete cookie

🔹 <b>Settings:</b>
• /quality - Default quality
• /history - Download history
• /stats - Your statistics

🔹 <b>General:</b>
• /cancel - Cancel current operation

━━━━━━━━━━━━━━━━━━━━
💡 <b>Tips:</b>
• Maximum file size: 2 GB
• Direct link support
• Auto-conversion to MP4""",

        "cookie_guide": """🍪 <b>Cookie Upload Guide</b>

Cookies are required to download private content.

━━━━━━━━━━━━━━━━━━━━
📝 <b>Steps to get cookies:</b>

<b>1. Install Extension:</b>
• Chrome/Edge: "Get cookies.txt LOCALLY"
• Firefox: "cookies.txt"

<b>2. Login to Account:</b>
• Go to the target website
• Login to your account

<b>3. Export Cookies:</b>
• Click on the extension icon
• Click "Export"
• Save the file

<b>4. Send to Bot:</b>
• Send the cookies.txt file here

━━━━━━━━━━━━━━━━━━━━
⚠️ <b>Security Notes:</b>
• Cookies are encrypted
• Only you have access to them
• Renew after expiration""",

        "quality_guide": """📊 <b>Quality Selection Guide</b>

━━━━━━━━━━━━━━━━━━━━
🎥 <b>Available Qualities:</b>

• 🔵 <b>4K (2160p)</b> - Highest quality
• 🟣 <b>2K (1440p)</b> - Excellent quality
• 🟢 <b>1080p Full HD</b> - Recommended
• 🟡 <b>720p HD</b> - Quality/size balance
• 🟠 <b>480p SD</b> - Low size
• 🎵 <b>Audio Only</b> - MP3

━━━━━━━━━━━━━━━━━━━━
💡 Default quality: 1080p""",

        "platforms": """🌐 <b>Supported Platforms</b>

━━━━━━━━━━━━━━━━━━━━
📹 <b>Video:</b>
• YouTube, Vimeo, Dailymotion, Twitch

📱 <b>Social Networks:</b>
• Instagram, Twitter/X, Facebook, TikTok, Reddit

🎓 <b>Educational:</b>
• Coursera, Udemy, Khan Academy

📎 <b>Direct Links:</b>
• MP4, MKV, WebM, AVI, MOV

<i>And over 1000+ other sites...</i>""",
    },
    
    # ═══════════════════════════════════════════════════════════════════════════
    # LANGUAGE SELECTION
    # ═══════════════════════════════════════════════════════════════════════════
    "language": {
        "select": "🌐 <b>Select your language:</b>",
        "changed": "✅ Language changed to <b>LANGUAGE_NAME</b>.",  # ← Put your language name
        "current": "🌐 Current language: <b>LANGUAGE_NAME</b> FLAG",  # ← Put your language name and flag
        "not_available": "❌ This language is not available.",
    },
    
    # ═══════════════════════════════════════════════════════════════════════════
    # DOWNLOAD PROCESS
    # ═══════════════════════════════════════════════════════════════════════════
    "download": {
        "extracting": "🔍 <b>Extracting video information...</b>\n\n⏳ Please wait...",
        "extracting_with_platform": "🔍 <b>Extracting information from {platform}...</b>\n\n⏳ Please wait...",
        
        "select_quality": """📊 <b>Select download quality:</b>

🎬 <b>{title}</b>

👤 Uploader: {uploader}
⏱ Duration: {duration}
👁 Views: {views}

━━━━━━━━━━━━━━━━━━━━
<i>Select your preferred quality:</i>""",

        "starting": "🚀 <b>Starting download...</b>\n\n📥 Preparing...",
        
        "progress": """🔥 <b>Downloading...</b>

{progress_bar}

📊 Progress: <b>{percentage}</b>
📦 Size: <b>{downloaded}</b> / <b>{total}</b>
⚡️ Speed: <b>{speed}</b>
⏱ ETA: <b>{eta}</b>
🎬 Quality: <b>{quality}</b>""",

        "merging": "🔄 <b>Merging video and audio...</b>\n\n⏳ This may take a moment...",
        
        "uploading": """📤 <b>Uploading to Telegram...</b>

{progress_bar}

📊 Progress: <b>{percentage}</b>
📦 Uploaded: <b>{uploaded}</b> / <b>{total}</b>""",

        "completed": """✅ <b>Download completed successfully!</b>

🎬 <b>{title}</b>

━━━━━━━━━━━━━━━━━━━━
📊 Quality: {quality}
📦 Size: {size}
⏱ Duration: {duration}
━━━━━━━━━━━━━━━━━━━━

🙏 Thank you for using our bot!""",

        "cancelled": "❌ Download cancelled.",
        "audio_only": "🎵 <b>Audio Only</b>",
        "best_quality": "⭐️ Best Quality",
        "auto_quality": "🔄 Auto Select",
    },
    
    # ═══════════════════════════════════════════════════════════════════════════
    # VIDEO INFO
    # ═══════════════════════════════════════════════════════════════════════════
    "video_info": {
        "title": "🎬 Title",
        "uploader": "👤 Uploader",
        "duration": "⏱ Duration",
        "views": "👁 Views",
        "likes": "❤️ Likes",
        "upload_date": "📅 Upload Date",
        "description": "📝 Description",
        "platform": "🌐 Platform",
        "quality": "📊 Quality",
        "size": "📦 Size",
        "format": "🎞 Format",
        "fps": "🎯 FPS",
        "resolution": "📐 Resolution",
        "codec": "🔧 Codec",
        "unknown": "Unknown",
        "private": "🔒 Private",
        "live": "🔴 Live",
    },
    
    # ═══════════════════════════════════════════════════════════════════════════
    # QUALITY OPTIONS
    # ═══════════════════════════════════════════════════════════════════════════
    "quality": {
        "4k": "🔵 4K Ultra HD (2160p)",
        "2k": "🟣 2K QHD (1440p)",
        "1080p": "🟢 Full HD (1080p)",
        "1080p60": "🟢 Full HD 60fps (1080p60)",
        "720p": "🟡 HD (720p)",
        "720p60": "🟡 HD 60fps (720p60)",
        "480p": "🟠 SD (480p)",
        "360p": "🔴 Low (360p)",
        "240p": "⚫️ Very Low (240p)",
        "audio": "🎵 Audio Only (MP3)",
        "best": "⭐️ Best Available Quality",
        "auto": "🔄 Auto Select",
        "with_size": "{quality} • {size}",
        "unavailable": "❌ {quality} (Unavailable)",
        "set_default": "📊 Current default quality: <b>{quality}</b>\n\nSelect new quality:",
        "default_changed": "✅ Default quality changed to <b>{quality}</b>.",
    },
    
    # ═══════════════════════════════════════════════════════════════════════════
    # ERROR MESSAGES
    # ═══════════════════════════════════════════════════════════════════════════
    "errors": {
        "generic": "❌ <b>An error occurred!</b>\n\n{message}\n\n🔄 Please try again.",
        "invalid_url": """❌ <b>Invalid URL!</b>

Please send a valid video link.

💡 <b>Examples:</b>
• https://youtube.com/watch?v=...
• https://instagram.com/p/...
• https://twitter.com/.../status/...""",
        "unsupported_platform": "❌ <b>This platform is not supported!</b>\n\n🌐 Detected platform: {platform}",
        "video_not_found": "❌ <b>Video not found!</b>\n\nThe video may have been deleted or is private.",
        "private_video": "🔒 <b>This video is private!</b>\n\nTo download private content, upload cookies via /cookie",
        "age_restricted": "🔞 <b>This video is age-restricted!</b>\n\nUpload cookies via /cookie to download.",
        "geo_restricted": "🌍 <b>This video is geo-restricted!</b>\n\nNot available in your region.",
        "file_too_large": "📦 <b>File size exceeds the limit!</b>\n\n• File size: {size}\n• Maximum allowed: 2 GB\n\n💡 Select a lower quality.",
        "download_failed": "❌ <b>Download failed!</b>\n\n{reason}\n\n🔄 Please try again.",
        "timeout": "⏱ <b>Operation timed out!</b>\n\nPlease try again.",
        "network_error": "🌐 <b>Network error!</b>\n\nPlease try again.",
        "rate_limit": "⏳ <b>Rate limit exceeded!</b>\n\n• Limit: {limit} downloads per day\n• Reset time: {reset_time}",
        "concurrent_limit": "⚠️ <b>Concurrent download limit!</b>\n\nYou have {current} active downloads. Maximum: {max}",
        "ffmpeg_not_found": "⚠️ <b>FFmpeg not found!</b>\n\nSome qualities may not be available.",
        "cookie_expired": "🍪 <b>Cookie has expired!</b>\n\nPlease upload a new cookie.",
        "cookie_invalid": "❌ <b>Invalid cookie!</b>\n\nPlease check the cookie format.",
        "maintenance": "🔧 <b>Bot is under maintenance!</b>\n\n{message}",
        "banned": "🚫 <b>Your access has been blocked!</b>\n\nReason: {reason}",
        "not_admin": "⛔️ This command is for admins only!",
        "not_owner": "⛔️ This command is for the bot owner only!",
        "extraction_failed": "❌ Error extracting video info. Please try again.",
        "no_formats": "❌ No downloadable formats found.",
        "upload_failed": "❌ Error uploading to Telegram. Please try again.",
    },
    
    # ═══════════════════════════════════════════════════════════════════════════
    # COOKIE MANAGEMENT
    # ═══════════════════════════════════════════════════════════════════════════
    "cookie": {
        "upload_prompt": "🍪 <b>Upload Cookie</b>\n\nSend your cookie file.\n\n📁 Accepted formats:\n• cookies.txt\n• cookies.json",
        "upload_for_platform": "🍪 <b>Upload {platform} Cookie</b>\n\nSend your {platform} cookie file.",
        "uploading": "📤 Uploading and verifying cookie...",
        "upload_success": "✅ <b>Cookie saved successfully!</b>\n\n🏷 Platform: {platform}\n📅 Date: {date}\n🔒 Encryption: Enabled",
        "upload_failed": "❌ <b>Cookie save failed!</b>\n\n{reason}",
        "invalid_format": "❌ <b>Invalid cookie format!</b>\n\nPlease send in correct format.",
        "list_title": "📋 <b>Saved Cookies:</b>\n\n{cookies_list}",
        "list_item": "• {number}. {platform} - {date} {status}",
        "list_empty": "📭 No cookies saved.",
        "status_valid": "✅",
        "status_expired": "⚠️ Expired",
        "status_unknown": "❓",
        "delete_prompt": "🗑 <b>Delete Cookie</b>\n\nWhich cookie should be deleted?\n\n{cookies_list}",
        "delete_success": "✅ Cookie for {platform} deleted successfully.",
        "delete_failed": "❌ Failed to delete cookie.",
        "delete_not_found": "❌ Cookie not found.",
        "delete_all_success": "✅ All cookies deleted.",
        "expiry_warning": "⚠️ <b>Cookie Expiry Warning!</b>\n\nYour {platform} cookie will expire in {days} days.",
    },
    
    # ═══════════════════════════════════════════════════════════════════════════
    # USER STATISTICS
    # ═══════════════════════════════════════════════════════════════════════════
    "stats": {
        "title": """📊 <b>Your Statistics</b>

━━━━━━━━━━━━━━━━━━━━
👤 <b>User Info:</b>
• ID: {user_id}
• Name: {name}
• Joined: {join_date}
• Status: {status}

━━━━━━━━━━━━━━━━━━━━
📥 <b>Download Stats:</b>
• Total downloads: {total_downloads}
• Successful: {successful} ✅
• Failed: {failed} ❌
• Success rate: {success_rate}

━━━━━━━━━━━━━━━━━━━━
📦 <b>Download Size:</b>
• Today: {today_size}
• This month: {month_size}
• Total: {total_size}

━━━━━━━━━━━━━━━━━━━━
⚡️ <b>Limits:</b>
• Daily: {daily_used}/{daily_limit}
• Concurrent: {concurrent_used}/{concurrent_limit}""",
        "status_normal": "Normal",
        "status_vip": "💎 VIP",
        "status_banned": "🚫 Banned",
    },
    
    # ═══════════════════════════════════════════════════════════════════════════
    # DOWNLOAD HISTORY
    # ═══════════════════════════════════════════════════════════════════════════
    "history": {
        "title": """📜 <b>Download History</b>

{history_list}

━━━━━━━━━━━━━━━━━━━━
📊 Showing {showing} of {total}

{pagination}""",
        "item": "• <b>{title}</b>\n  📅 {date} | 📦 {size} | {status}",
        "empty": "📭 <b>History is empty!</b>\n\nYou haven't downloaded any videos yet.",
        "status_completed": "✅",
        "status_failed": "❌",
        "clear_confirm": "⚠️ Are you sure you want to clear history?",
        "clear_success": "✅ Download history cleared.",
    },
    
    # ═══════════════════════════════════════════════════════════════════════════
    # ADMIN PANEL
    # ═══════════════════════════════════════════════════════════════════════════
    "admin": {
        "panel_title": """🛠 <b>Admin Panel</b>

━━━━━━━━━━━━━━━━━━━━
📊 <b>General Stats:</b>
• Total users: {total_users}
• Active users (24h): {active_users}
• VIP users: {vip_users}
• Banned users: {banned_users}

━━━━━━━━━━━━━━━━━━━━
📥 <b>Download Stats:</b>
• Today's downloads: {today_downloads}
• This week's downloads: {week_downloads}
• Total downloads: {total_downloads}
• Success rate: {success_rate}

━━━━━━━━━━━━━━━━━━━━
💾 <b>Server:</b>
• Uptime: {uptime}
• CPU usage: {cpu_usage}
• RAM usage: {ram_usage}
• Disk space: {disk_usage}""",
        "broadcast_prompt": "📢 <b>Broadcast Message</b>\n\nSend your message.\nThis will be sent to all {count} users.\n\n❌ To cancel: /cancel",
        "broadcast_confirm": "⚠️ <b>Confirm Broadcast</b>\n\nSend to <b>{count}</b> users?\n\n━━━━━━━━━━━━━━━━━━━━\n{message}\n━━━━━━━━━━━━━━━━━━━━",
        "broadcast_started": "📤 Starting broadcast...",
        "broadcast_progress": "📤 Sending: {sent}/{total}",
        "broadcast_completed": "✅ <b>Broadcast completed!</b>\n\n• Successful: {success}\n• Failed: {failed}\n• Total: {total}",
        "ban_success": "✅ User {user_id} has been banned.\nReason: {reason}",
        "ban_failed": "❌ Failed to ban user.",
        "unban_success": "✅ User {user_id} has been unbanned.",
        "unban_failed": "❌ Failed to unban user.",
        "user_not_found": "❌ User not found.",
        "vip_granted": "✅ User {user_id} is now VIP until {expiry}.",
        "vip_revoked": "✅ VIP status revoked for user {user_id}.",
        "cleanup_started": "🧹 Starting temp file cleanup...",
        "cleanup_completed": "✅ <b>Cleanup completed!</b>\n\n• Files deleted: {files}\n• Space freed: {size}",
        "restart_warning": "⚠️ Bot is restarting...",
        "restart_completed": "✅ Bot restarted successfully.",
    },
    
    # ═══════════════════════════════════════════════════════════════════════════
    # BUTTONS
    # ═══════════════════════════════════════════════════════════════════════════
    "buttons": {
        "download": "📥 Download",
        "download_audio": "🎵 Download Audio",
        "cancel": "❌ Cancel",
        "back": "🔙 Back",
        "close": "✖️ Close",
        "confirm": "✅ Confirm",
        "retry": "🔄 Retry",
        "next": "Next ➡️",
        "previous": "⬅️ Previous",
        "refresh": "🔄 Refresh",
        "settings": "⚙️ Settings",
        "help": "❓ Help",
        "language": "🌐 Language",
        "stats": "📊 Stats",
        "history": "📜 History",
        "cookie": "🍪 Cookie",
        "quality": "📊 Quality",
        "admin": "🛠 Admin",
        "quality_4k": "🔵 4K",
        "quality_2k": "🟣 2K",
        "quality_1080p": "🟢 1080p",
        "quality_720p": "🟡 720p",
        "quality_480p": "🟠 480p",
        "quality_360p": "🔴 360p",
        "quality_audio": "🎵 Audio",
        "quality_best": "⭐️ Best",
        "broadcast": "📢 Broadcast",
        "users": "👥 Users",
        "statistics": "📊 Statistics",
        "cleanup": "🧹 Cleanup",
        "logs": "📋 Logs",
        "upload_cookie": "📤 Upload Cookie",
        "delete_cookie": "🗑 Delete Cookie",
        "list_cookies": "📋 List Cookies",
        "lang_fa": "🇮🇷 فارسی",
        "lang_en": "🇬🇧 English",
        "yes": "✅ Yes",
        "no": "❌ No",
    },
    
    # ═══════════════════════════════════════════════════════════════════════════
    # COMMON MESSAGES
    # ═══════════════════════════════════════════════════════════════════════════
    "common": {
        "please_wait": "⏳ Please wait...",
        "processing": "🔄 Processing...",
        "loading": "⌛️ Loading...",
        "success": "✅ Operation successful!",
        "failed": "❌ Operation failed!",
        "cancelled": "❌ Cancelled.",
        "done": "✅ Done!",
        "error": "❌ Error!",
        "warning": "⚠️ Warning!",
        "info": "ℹ️ Information:",
        "tip": "💡 Tip:",
        "note": "📝 Note:",
        "unknown": "Unknown",
        "none": "None",
        "yes": "Yes",
        "no": "No",
        "or": "or",
        "and": "and",
        "from": "from",
        "to": "to",
        "page": "Page {current} of {total}",
    },
    
    # ═══════════════════════════════════════════════════════════════════════════
    # PLATFORM NAMES
    # ═══════════════════════════════════════════════════════════════════════════
    "platforms": {
        "youtube": "YouTube",
        "instagram": "Instagram",
        "twitter": "Twitter/X",
        "tiktok": "TikTok",
        "facebook": "Facebook",
        "vimeo": "Vimeo",
        "dailymotion": "Dailymotion",
        "twitch": "Twitch",
        "reddit": "Reddit",
        "aparat": "Aparat",
        "namasha": "Namasha",
        "vk": "VK",
        "bilibili": "Bilibili",
        "direct": "Direct Link",
        "unknown": "Unknown",
    },
    
    # ═══════════════════════════════════════════════════════════════════════════
    # TIME UNITS
    # ═══════════════════════════════════════════════════════════════════════════
    "time": {
        "second": "second",
        "seconds": "seconds",
        "minute": "minute",
        "minutes": "minutes",
        "hour": "hour",
        "hours": "hours",
        "day": "day",
        "days": "days",
        "week": "week",
        "weeks": "weeks",
        "month": "month",
        "months": "months",
        "year": "year",
        "years": "years",
        "ago": "ago",
        "remaining": "remaining",
        "now": "now",
        "today": "today",
        "yesterday": "yesterday",
        "tomorrow": "tomorrow",
    },
    
    # ═══════════════════════════════════════════════════════════════════════════
    # NOTIFICATIONS
    # ═══════════════════════════════════════════════════════════════════════════
    "notifications": {
        "download_complete": "✅ Download of '{title}' completed!",
        "download_failed": "❌ Download of '{title}' failed.",
        "cookie_expiring": "⚠️ Your {platform} cookie is expiring!",
        "vip_expiring": "⚠️ Your VIP subscription expires in {days} days.",
        "new_feature": "🎉 New feature: {feature}",
        "maintenance_scheduled": "🔧 Scheduled maintenance: {time}",
    },
}

# ═══════════════════════════════════════════════════════════════════════════════
# DO NOT MODIFY BELOW THIS LINE
# ═══════════════════════════════════════════════════════════════════════════════

# Export the strings
__all__ = ["STRINGS"]

# ═══════════════════════════════════════════════════════════════════════════════
# VALIDATION (Optional - helps catch missing translations)
# ═══════════════════════════════════════════════════════════════════════════════

def validate_translations():
    """
    Validate that all required keys are present.
    Run this function to check for missing translations.
    """
    required_sections = [
        "_meta", "start", "help", "language", "download", "video_info",
        "quality", "errors", "cookie", "stats", "history", "admin",
        "buttons", "common", "platforms", "time", "notifications"
    ]
    
    missing = []
    for section in required_sections:
        if section not in STRINGS:
            missing.append(section)
    
    if missing:
        print(f"⚠️ Missing sections: {', '.join(missing)}")
        return False
    
    print("✅ All required sections are present!")
    return True


if __name__ == "__main__":
    # Run validation when file is executed directly
    validate_translations()
    print(f"\n📝 Language: {STRINGS['_meta']['native_name']} ({STRINGS['_meta']['code']})")
    print(f"🏳️ Flag: {STRINGS['_meta']['flag']}")
    print(f"📖 RTL: {STRINGS['_meta']['rtl']}")