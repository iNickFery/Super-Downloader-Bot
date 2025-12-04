#!/bin/bash

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║                    Professional Video Downloader Bot                         ║
# ║                         Installation Script                                  ║
# ║                                                                              ║
# ║  Usage: chmod +x install.sh && ./install.sh                                  ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# ═══════════════════════════════════════════════════════════════════════════════
# FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

print_banner() {
    echo -e "${CYAN}"
    echo "╔══════════════════════════════════════════════════════════════════════╗"
    echo "║           🎬 Video Downloader Bot - Installation Script              ║"
    echo "║                         Version 2.0.0                                 ║"
    echo "╚══════════════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

print_step() {
    echo -e "\n${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${PURPLE}📦 $1${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${CYAN}ℹ️  $1${NC}"
}

check_command() {
    if command -v $1 &> /dev/null; then
        print_success "$1 is installed"
        return 0
    else
        print_warning "$1 is not installed"
        return 1
    fi
}

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN INSTALLATION
# ═══════════════════════════════════════════════════════════════════════════════

print_banner

# Check OS
print_step "Checking Operating System"
OS="$(uname -s)"
case "${OS}" in
    Linux*)     MACHINE=Linux;;
    Darwin*)    MACHINE=Mac;;
    CYGWIN*)    MACHINE=Cygwin;;
    MINGW*)     MACHINE=MinGw;;
    *)          MACHINE="UNKNOWN:${OS}"
esac
print_info "Operating System: ${MACHINE}"

# Check Python
print_step "Checking Python Installation"
if check_command python3; then
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    print_info "Python version: ${PYTHON_VERSION}"
    
    # Check if version is 3.9+
    PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
    PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)
    
    if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 9 ]); then
        print_error "Python 3.9 or higher is required!"
        exit 1
    fi
else
    print_error "Python 3 is not installed!"
    print_info "Please install Python 3.9 or higher and try again."
    exit 1
fi

# Check pip
print_step "Checking pip Installation"
if check_command pip3; then
    PIP_VERSION=$(pip3 --version 2>&1 | awk '{print $2}')
    print_info "pip version: ${PIP_VERSION}"
else
    print_warning "pip3 not found, trying pip..."
    if check_command pip; then
        print_info "Using pip instead of pip3"
    else
        print_error "pip is not installed!"
        exit 1
    fi
fi

# Check FFmpeg
print_step "Checking FFmpeg Installation"
if check_command ffmpeg; then
    FFMPEG_VERSION=$(ffmpeg -version 2>&1 | head -n1 | awk '{print $3}')
    print_info "FFmpeg version: ${FFMPEG_VERSION}"
else
    print_warning "FFmpeg is not installed!"
    print_info "Some features may not work without FFmpeg."
    
    if [ "$MACHINE" = "Linux" ]; then
        print_info "Install with: sudo apt install ffmpeg"
    elif [ "$MACHINE" = "Mac" ]; then
        print_info "Install with: brew install ffmpeg"
    fi
    
    read -p "Continue without FFmpeg? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Create virtual environment
print_step "Creating Virtual Environment"
if [ -d "venv" ]; then
    print_warning "Virtual environment already exists"
    read -p "Recreate virtual environment? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf venv
        python3 -m venv venv
        print_success "Virtual environment recreated"
    fi
else
    python3 -m venv venv
    print_success "Virtual environment created"
fi

# Activate virtual environment
print_step "Activating Virtual Environment"
source venv/bin/activate
print_success "Virtual environment activated"

# Upgrade pip
print_step "Upgrading pip"
pip install --upgrade pip setuptools wheel
print_success "pip upgraded"

# Install dependencies
print_step "Installing Python Dependencies"
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    print_success "Dependencies installed"
else
    print_error "requirements.txt not found!"
    exit 1
fi

# Create directories
print_step "Creating Required Directories"
directories=("temp" "downloads" "cookies" "logs" "cache" "database" "languages")
for dir in "${directories[@]}"; do
    if [ ! -d "$dir" ]; then
        mkdir -p "$dir"
        print_success "Created: $dir/"
    else
        print_info "Exists: $dir/"
    fi
done

# Setup .env file
print_step "Setting Up Environment Configuration"
if [ -f ".env" ]; then
    print_warning ".env file already exists"
    read -p "Overwrite .env file? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_info "Keeping existing .env file"
    else
        cp .env.example .env
        print_success ".env file created from template"
    fi
else
    if [ -f ".env.example" ]; then
        cp .env.example .env
        print_success ".env file created from template"
    else
        print_error ".env.example not found!"
        exit 1
    fi
fi

# Interactive configuration
print_step "Bot Configuration"
echo -e "${YELLOW}"
echo "Please configure your bot settings."
echo "You can edit .env file later for more options."
echo -e "${NC}"

# Get API credentials
read -p "Enter your Telegram API_ID: " API_ID
read -p "Enter your Telegram API_HASH: " API_HASH
read -p "Enter your Bot Token: " BOT_TOKEN
read -p "Enter your Telegram User ID (Owner): " OWNER_ID

# Update .env file
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    sed -i '' "s/API_ID=.*/API_ID=${API_ID}/" .env
    sed -i '' "s/API_HASH=.*/API_HASH=${API_HASH}/" .env
    sed -i '' "s/BOT_TOKEN=.*/BOT_TOKEN=${BOT_TOKEN}/" .env
    sed -i '' "s/OWNER_ID=.*/OWNER_ID=${OWNER_ID}/" .env
else
    # Linux
    sed -i "s/API_ID=.*/API_ID=${API_ID}/" .env
    sed -i "s/API_HASH=.*/API_HASH=${API_HASH}/" .env
    sed -i "s/BOT_TOKEN=.*/BOT_TOKEN=${BOT_TOKEN}/" .env
    sed -i "s/OWNER_ID=.*/OWNER_ID=${OWNER_ID}/" .env
fi

print_success "Configuration updated"

# Generate encryption key
print_step "Generating Encryption Key"
ENCRYPTION_KEY=$(python3 -c "import secrets; import base64; print(base64.b64encode(secrets.token_bytes(32)).decode())")

if [[ "$OSTYPE" == "darwin"* ]]; then
    sed -i '' "s/ENCRYPTION_KEY=.*/ENCRYPTION_KEY=${ENCRYPTION_KEY}/" .env
else
    sed -i "s/ENCRYPTION_KEY=.*/ENCRYPTION_KEY=${ENCRYPTION_KEY}/" .env
fi

print_success "Encryption key generated"

# Create systemd service (Linux only)
if [ "$MACHINE" = "Linux" ]; then
    print_step "Creating Systemd Service (Optional)"
    read -p "Create systemd service for auto-start? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        CURRENT_DIR=$(pwd)
        SERVICE_FILE="video-downloader-bot.service"
        
        cat > $SERVICE_FILE << EOF
[Unit]
Description=Video Downloader Telegram Bot
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$CURRENT_DIR
ExecStart=$CURRENT_DIR/venv/bin/python $CURRENT_DIR/bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF
        
        print_success "Service file created: $SERVICE_FILE"
        print_info "To install the service:"
        echo "  sudo cp $SERVICE_FILE /etc/systemd/system/"
        echo "  sudo systemctl daemon-reload"
        echo "  sudo systemctl enable video-downloader-bot"
        echo "  sudo systemctl start video-downloader-bot"
    fi
fi

# Final summary
print_step "Installation Complete!"
echo ""
echo -e "${GREEN}╔══════════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║                    ✅ Installation Successful!                        ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${CYAN}📋 Next Steps:${NC}"
echo ""
echo -e "  1. ${YELLOW}Review your configuration:${NC}"
echo -e "     nano .env"
echo ""
echo -e "  2. ${YELLOW}Activate virtual environment:${NC}"
echo -e "     source venv/bin/activate"
echo ""
echo -e "  3. ${YELLOW}Start the bot:${NC}"
echo -e "     python bot.py"
echo ""
echo -e "  4. ${YELLOW}Or use Docker:${NC}"
echo -e "     docker-compose up -d"
echo ""
echo -e "${CYAN}📚 Documentation:${NC}"
echo -e "  • README.md - General documentation"
echo -e "  • LANGUAGE_GUIDE.md - Adding new languages"
echo ""
echo -e "${PURPLE}🎬 Happy downloading!${NC}"
echo ""