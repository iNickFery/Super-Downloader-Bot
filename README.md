# 🎬 Super Video Downloader Bot

<div align="center">

![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.9+-green.svg)
![License](https://img.shields.io/badge/license-MIT-yellow.svg)
![Telegram](https://img.shields.io/badge/Telegram-Bot-blue.svg)

**The most powerful video downloader bot on Telegram**

[English](#english) | [فارسی](https://github.com/iNickFery/Super-Downloader-Bot/blob/main/README_fa.md)

</div>

## English

### 📖 About

This is a professional Telegram bot for downloading videos from **1000+ websites**. Download videos in qualities up to **4K Ultra HD**.

### ✨ Features

- 🌐 Support for **1000+ platforms** (YouTube, Instagram, Twitter, TikTok, etc.)
- 📊 Quality selection from **240p to 4K**
- 🎵 **Audio-only** extraction in high quality
- 🍪 **Cookie support** for private content
- 🌍 **Multi-language** (Persian & English)
- ⚡ High download speed
- 📈 Real-time progress tracking
- 🔒 Encrypted cookie storage
- 👑 VIP system with higher limits
- 🛠 Admin panel for management

### 🚀 Quick Start

#### Prerequisites

- Python 3.9+
- FFmpeg (optional, for merging video/audio)

#### Installation

```bash
# Clone the repository
git clone https://github.com//iNickFery/Super-Downloader-Bot.git
cd Super-Downloader-Bot

# Run installation script
chmod +x install.sh
./install.sh
```

Or manual installation:

```bash
# Create virtual environment
sudo apt install python3.12-venv
python3 -m venv venv
source venv/bin/activate
sudo apt install build-essential python3-dev -y

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
nano .env  # Edit settings

# Run the bot
python bot.py
```

### ⚙️ Configuration

Edit `.env` file:

```env
# Required
API_ID=your_api_id
API_HASH=your_api_hash
BOT_TOKEN=your_bot_token
OWNER_ID=your_user_id

# Optional
DEFAULT_LANGUAGE=en
DEFAULT_QUALITY=1080
```

### 📱 Commands

| Command | Description |
|---------|-------------|
| `/start` | Start the bot |
| `/help` | Show help |
| `/language` | Change language |
| `/cookie` | Upload cookie |
| `/quality` | Set default quality |
| `/stats` | Your statistics |
| `/history` | Download history |
| `/cancel` | Cancel download |

### 🐳 Docker

```bash
# Build image
docker build -t video-downloader-bot .

# Run
docker run -d --name vdbot --env-file .env video-downloader-bot

# Or with docker-compose
docker-compose up -d
```

### 🌐 Adding New Languages

See [LANGUAGE_GUIDE.md](LANGUAGE_GUIDE.md) for instructions on adding new languages.

1. Copy `languages/lang_template.py` to `languages/lang_XX.py`
2. Update the `_meta` section
3. Translate all strings
4. Save - the bot will auto-detect it!

### 📊 Supported Platforms

<details>
<summary>Click to expand full list</summary>

- **Video Platforms:** YouTube, Vimeo, Dailymotion, Twitch
- **Social Media:** Instagram, Twitter/X, Facebook, TikTok, Reddit
- **Regional:** Aparat (Iran), Namasha, VK (Russia), Bilibili (China)
- **Educational:** Coursera, Udemy, Khan Academy
- **And 1000+ more...**

</details>

### 🔧 Admin Commands

| Command | Description |
|---------|-------------|
| `/adminpanel` | Admin dashboard |
| `/broadcast` | Send message to all users |
| `/ban` | Ban a user |
| `/unban` | Unban a user |
| `/setvip` | Grant VIP status |
| `/cleanup` | Clean temp files |

### 📝 License

This project is licensed under the MIT License.

### 🤝 Contributing

Contributions are welcome! Please read the contributing guidelines first.

### 📞 Support

For support, open an issue on GitHub.

---

<div align="center">

**Made with ❤️ for the [NickFery](https://github.com/iNickFery)**

</div>
