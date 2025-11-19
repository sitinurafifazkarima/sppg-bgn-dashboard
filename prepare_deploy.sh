#!/bin/bash

# Script untuk initialize Git dan prepare untuk deployment
# Jalankan script ini sebelum deploy ke Streamlit Cloud

echo "🚀 Preparing Dashboard SPPG BGN for Deployment..."
echo ""

# Check if git is installed
if ! command -v git &> /dev/null
then
    echo "❌ Git tidak terinstall!"
    echo "Download dari: https://git-scm.com/downloads"
    exit 1
fi

echo "✅ Git version: $(git --version)"
echo ""

# Initialize git if not already
if [ ! -d .git ]; then
    echo "📦 Initializing Git repository..."
    git init
    echo "✅ Git initialized"
else
    echo "✅ Git repository already exists"
fi

# Check if files exist
echo ""
echo "📝 Checking required files..."

required_files=(
    "dashboard_sppg.py"
    "requirements.txt"
    "sppg_data_complete_with_coordinates.csv"
    "README.md"
)

all_files_exist=true
for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✅ $file"
    else
        echo "  ❌ $file (MISSING!)"
        all_files_exist=false
    fi
done

if [ "$all_files_exist" = false ]; then
    echo ""
    echo "❌ Beberapa file penting tidak ditemukan!"
    exit 1
fi

# Add files to git
echo ""
echo "📤 Adding files to git..."
git add .

# Show status
echo ""
echo "📊 Git status:"
git status --short

echo ""
echo "✅ Repository ready for deployment!"
echo ""
echo "📋 Next steps:"
echo ""
echo "1. Commit changes:"
echo "   git commit -m \"Initial commit: SPPG BGN Dashboard\""
echo ""
echo "2. Create GitHub repository:"
echo "   https://github.com/new"
echo ""
echo "3. Add remote and push:"
echo "   git remote add origin https://github.com/YOUR_USERNAME/sppg-bgn-dashboard.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "4. Deploy to Streamlit Cloud:"
echo "   https://share.streamlit.io"
echo ""
echo "🎉 Happy deploying!"
