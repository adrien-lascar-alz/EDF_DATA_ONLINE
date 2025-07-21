#!/bin/bash

# 🚀 GitHub Deployment Setup Script
# This script helps you set up your repository for deployment

echo "🔧 Setting up GitHub repository for deployment..."
echo "================================================="

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "❌ Not a git repository. Initializing..."
    git init
    git branch -M main
fi

# Add all files
echo "📁 Adding files to git..."
git add .

# Check if there are changes to commit
if git diff --cached --quiet; then
    echo "✅ No changes to commit"
else
    echo "💾 Committing changes..."
    git commit -m "🚀 Add GitHub Actions deployment workflows

- Add Streamlit Cloud deployment workflow
- Add Docker deployment workflow  
- Add comprehensive deployment guide
- Update README with deployment options"
fi

# Check if remote exists
if git remote get-url origin >/dev/null 2>&1; then
    echo "🌐 Remote repository found"
    echo "📤 Pushing to GitHub..."
    git push -u origin main
else
    echo "⚠️  No remote repository found."
    echo "To complete setup:"
    echo "1. Create a new repository on GitHub"
    echo "2. Add it as remote: git remote add origin https://github.com/USERNAME/REPO.git"
    echo "3. Push: git push -u origin main"
fi

echo ""
echo "✅ Setup complete! Next steps:"
echo ""
echo "🎯 For Streamlit Cloud deployment:"
echo "   1. Visit https://share.streamlit.io"
echo "   2. Connect your GitHub repository"
echo "   3. Deploy beacon_analyzer_app.py"
echo ""
echo "🐳 For Docker deployment:"
echo "   1. GitHub Actions will automatically build images"
echo "   2. Check the Actions tab in your GitHub repository"
echo ""
echo "📚 For detailed instructions, see DEPLOYMENT.md"
