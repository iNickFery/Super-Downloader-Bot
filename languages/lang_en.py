#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    Professional Video Downloader Bot                         ║
║                         English Language                                     ║
║                                                                              ║
║  Complete English translations for the Video Downloader Bot.                 ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

STRINGS = {
    # ═══════════════════════════════════════════════════════════════════════════
    # META INFORMATION
    # ═══════════════════════════════════════════════════════════════════════════
    "_meta": {
        "code": "en",
        "name": "English",
        "native_name": "English",
        "flag": "🇬🇧",
        "rtl": False,
        "version": "2.0.0",
        "author": "Video Downloader Team",
    },
    
    # ═══════════════════════════════════════════════════════════════════════════
    # WELCOME & START MESSAGES
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
  Size: ~2-8 GB/hour

• 🟣 <b>2K (1440p)</b> - Excellent quality
  Size: ~1-4 GB/hour

• 🟢 <b>1080p Full HD</b> - Recommended
  Size: ~0.5-2 GB/hour

• 🟡 <b>720p HD</b> - Quality/size balance
  Size: ~0.3-1 GB/hour

• 🟠 <b>480p SD</b> - Low size
  Size: ~0.2-0.5 GB/hour

• 🎵 <b>Audio Only</b> - MP3
  Size: ~50-100 MB/hour

━━━━━━━━━━━━━━━━━━━━
💡 Default quality: 1080p""",

        "platforms": """🌐 <b>Supported Platforms</b>

━━━━━━━━━━━━━━━━━━━━
📹 <b>Video:</b>
• YouTube (+ Shorts, Live, Playlist)
• Vimeo
• Dailymotion
• Twitch (+ Clips)

📱 <b>Social Networks:</b>
• Instagram (Post, Reel, Story)
• Twitter/X
• Facebook
• TikTok
• Reddit
• LinkedIn

🎓 <b>Educational:</b>
• Coursera
• Udemy
• Khan Academy

🇮🇷 <b>Iranian:</b>
• Aparat
• Namasha

🌏 <b>International:</b>
• VK (Russia)
• Bilibili (China)

📎 <b>Direct Links:</b>
• MP4, MKV, WebM, AVI, MOV

<i>And over 1000+ other sites...</i>""",
    },
    
    # ═══════════════════════════════════════════════════════════════════════════
    # LANGUAGE SELECTION
    # ═══════════════════════════════════════════════════════════════════════════
    "language": {
        "select": "🌐 <b>Select your language:</b>",
        "changed": "✅ Language changed to <b>English</b>.",
        "current": "🌐 Current language: <b>English</b> 🇬🇧",
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

        "unsupported_platform": """❌ <b>This platform is not supported!</b>

🌐 Detected platform: {platform}

💡 List of supported platforms: /help""",

        "video_not_found": """❌ <b>Video not found!</b>

Possible reasons:
• Video has been deleted
• Video is private
• Invalid link

💡 For private content use /cookie""",

        "private_video": """🔒 <b>This video is private!</b>

To download private content:
1. Upload cookies via /cookie
2. Send the link again

📚 Guide: /cookie""",

        "age_restricted": """🔞 <b>This video is age-restricted!</b>

To download:
1. Upload cookies via /cookie
2. Send the link again""",

        "geo_restricted": """🌍 <b>This video is geo-restricted!</b>

Unfortunately, this video is not available for download in your region.

💡 Using a VPN is recommended.""",

        "file_too_large": """📦 <b>File size exceeds the limit!</b>

• File size: {size}
• Maximum allowed: 2 GB

💡 Select a lower quality.""",

        "download_failed": """❌ <b>Download failed!</b>

{reason}

🔄 Please try again.
If the problem persists, contact support.""",

        "timeout": """⏱ <b>Operation timed out!</b>

Server is not responding. Please:
• Wait a few minutes
• Try again""",

        "network_error": """🌐 <b>Network error!</b>

Problem connecting to server.
Please try again.""",

        "rate_limit": """⏳ <b>Rate limit exceeded!</b>

You have reached your daily download limit.

• Limit: {limit} downloads per day
• Reset time: {reset_time}

💎 Upgrade to VIP for higher limits!""",

        "concurrent_limit": """⚠️ <b>Concurrent download limit!</b>

You currently have {current} active downloads.
Maximum allowed: {max}

Please wait for the previous download to complete.""",

        "ffmpeg_not_found": """⚠️ <b>FFmpeg not found!</b>

Some qualities require FFmpeg.
Video will be downloaded in available quality.""",

        "cookie_expired": """🍪 <b>Cookie has expired!</b>

Please upload a new cookie.
Guide: /cookie""",

        "cookie_invalid": """❌ <b>Invalid cookie!</b>

Cookie file format is incorrect.
Guide: /cookie""",

        "maintenance": """🔧 <b>Bot is under maintenance!</b>

{message}

⏳ Please check back later.""",

        "banned": """🚫 <b>Your access has been blocked!</b>

Reason: {reason}

Contact admin to appeal.""",

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
        "upload_prompt": """🍪 <b>Upload Cookie</b>

Send your cookie file.

📁 Accepted formats:
• cookies.txt (Netscape format)
• cookies.json

📚 Cookie extraction guide: /help

⚠️ <b>Note:</b> Cookies are stored encrypted.""",

        "upload_for_platform": """🍪 <b>Upload {platform} Cookie</b>

Send your {platform} cookie file.

This cookie will be used for:
• Private videos
• Age-restricted content
• Exclusive posts""",

        "uploading": "📤 Uploading and verifying cookie...",
        
        "upload_success": """✅ <b>Cookie saved successfully!</b>

🏷 Platform: {platform}
📅 Date: {date}
🔒 Encryption: Enabled

You can now download private content.""",

        "upload_failed": """❌ <b>Cookie save failed!</b>

{reason}

Please try again.""",

        "invalid_format": """❌ <b>Invalid cookie format!</b>

Please send the file in correct format:
• Netscape cookies.txt
• JSON format

Guide: /cookie""",

        "list_title": """📋 <b>Saved Cookies:</b>

{cookies_list}

━━━━━━━━━━━━━━━━━━━━
💡 To delete: /deletecookie [number]""",

        "list_item": "• {number}. {platform} - {date} {status}",
        "list_empty": "📭 No cookies saved.",
        
        "status_valid": "✅",
        "status_expired": "⚠️ Expired",
        "status_unknown": "❓",
        
        "delete_prompt": """🗑 <b>Delete Cookie</b>

Which cookie should be deleted?

{cookies_list}""",

        "delete_success": "✅ Cookie for {platform} deleted successfully.",
        "delete_failed": "❌ Failed to delete cookie.",
        "delete_not_found": "❌ Cookie not found.",
        "delete_all_success": "✅ All cookies deleted.",
        
        "expiry_warning": """⚠️ <b>Cookie Expiry Warning!</b>

Your {platform} cookie will expire in {days} days.

Please upload a new cookie.""",
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

        "item": """• <b>{title}</b>
  📅 {date} | 📦 {size} | {status}""",

        "empty": """📭 <b>History is empty!</b>

You haven't downloaded any videos yet.

📎 To start, send a link.""",

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
• Disk space: {disk_usage}

━━━━━━━━━━━━━━━━━━━━
🌐 <b>Top Platforms:</b>
{top_platforms}""",

        "broadcast_prompt": """📢 <b>Broadcast Message</b>

Send your message.
This message will be sent to all {count} users.

❌ To cancel: /cancel""",

        "broadcast_confirm": """⚠️ <b>Confirm Broadcast</b>

The following message will be sent to <b>{count}</b> users:

━━━━━━━━━━━━━━━━━━━━
{message}
━━━━━━━━━━━━━━━━━━━━

Do you confirm?""",

        "broadcast_started": "📤 Starting broadcast...",
        "broadcast_progress": "📤 Sending: {sent}/{total}",
        "broadcast_completed": """✅ <b>Broadcast completed!</b>

• Successful: {success}
• Failed: {failed}
• Total: {total}""",

        "ban_success": "✅ User {user_id} has been banned.\nReason: {reason}",
        "ban_failed": "❌ Failed to ban user.",
        "unban_success": "✅ User {user_id} has been unbanned.",
        "unban_failed": "❌ Failed to unban user.",
        "user_not_found": "❌ User not found.",
        
        "vip_granted": "✅ User {user_id} is now VIP until {expiry}.",
        "vip_revoked": "✅ VIP status revoked for user {user_id}.",
        
        "cleanup_started": "🧹 Starting temp file cleanup...",
        "cleanup_completed": """✅ <b>Cleanup completed!</b>

• Files deleted: {files}
• Space freed: {size}""",

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
        
        # Quality buttons
        "quality_4k": "🔵 4K",
        "quality_2k": "🟣 2K",
        "quality_1080p": "🟢 1080p",
        "quality_720p": "🟡 720p",
        "quality_480p": "🟠 480p",
        "quality_360p": "🔴 360p",
        "quality_audio": "🎵 Audio",
        "quality_best": "⭐️ Best",
        
        # Admin buttons
        "broadcast": "📢 Broadcast",
        "users": "👥 Users",
        "statistics": "📊 Statistics",
        "cleanup": "🧹 Cleanup",
        "logs": "📋 Logs",
        
        # Cookie buttons
        "upload_cookie": "📤 Upload Cookie",
        "delete_cookie": "🗑 Delete Cookie",
        "list_cookies": "📋 List Cookies",
        
        # Language buttons
        "lang_fa": "🇮🇷 فارسی",
        "lang_en": "🇬🇧 English",
        
        # Yes/No
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


# Export the strings
__all__ = ["STRINGS"]