#!/usr/bin/env bash
# Quick Start Script for Healthcare System Frontend
# Run this script to set up the frontend quickly

echo "╔═══════════════════════════════════════════════════════════════════════════════╗"
echo "║          Healthcare System - Modern Frontend - Quick Start                    ║"
echo "╚═══════════════════════════════════════════════════════════════════════════════╝"
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if in healthcare directory
if [ ! -f "manage.py" ]; then
    echo -e "${YELLOW}⚠️  Not in healthcare directory!${NC}"
    echo "Please navigate to the healthcare folder and run this script again."
    exit 1
fi

echo -e "${BLUE}Step 1: Running Django Migrations${NC}"
python manage.py migrate
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}⚠️  Migrations failed!${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Migrations complete${NC}"
echo ""

echo -e "${BLUE}Step 2: Collecting Static Files${NC}"
python manage.py collectstatic --noinput
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}⚠️  Static collection failed!${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Static files collected${NC}"
echo ""

echo -e "${BLUE}Step 3: Checking Django Setup${NC}"
python manage.py check
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}⚠️  Django check failed!${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Django check passed${NC}"
echo ""

echo -e "${GREEN}═══════════════════════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✓ Setup Complete!${NC}"
echo ""
echo -e "${BLUE}Next Steps:${NC}"
echo "1. Create a superuser (if not already created):"
echo "   python manage.py createsuperuser"
echo ""
echo "2. Start the development server:"
echo "   python manage.py runserver"
echo ""
echo "3. Open your browser and visit:"
echo "   http://127.0.0.1:8000/"
echo ""
echo -e "${YELLOW}Documentation Files:${NC}"
echo "  • FRONTEND_README.md - Complete feature documentation"
echo "  • FRONTEND_SETUP.md - Detailed setup instructions"
echo "  • FRONTEND_VERIFICATION.md - Testing checklist"
echo "  • IMPLEMENTATION_SUMMARY.md - Implementation overview"
echo ""
echo -e "${GREEN}═══════════════════════════════════════════════════════════════════════════════${NC}"
