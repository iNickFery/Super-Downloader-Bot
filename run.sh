#!/bin/bash

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║                    Professional Video Downloader Bot                         ║
# ║                         Run Script                                           ║
# ║                                                                              ║
# ║  Usage: chmod +x run.sh && ./run.sh                                          ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║          🎬 Video Downloader Bot - Starting...               ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Virtual environment not found. Running install.sh...${NC}"
    chmod +x install.sh
    ./install.sh
fi

# Activate virtual environment
echo -e "${GREEN}Activating virtual environment...${NC}"
source venv/bin/activate

# Check if .env exists
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}Warning: .env file not found!${NC}"
    echo "Please copy .env.example to .env and configure it."
    exit 1
fi

# Create required directories
mkdir -p temp downloads cookies logs cache database

# Run the bot
echo -e "${GREEN}Starting bot...${NC}"
echo ""
python -u bot.py