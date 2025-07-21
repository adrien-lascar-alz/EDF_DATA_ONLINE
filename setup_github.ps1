# 🚀 GitHub Deployment Setup Script (PowerShell)
# This script helps you set up your repository for deployment

Write-Host "🔧 Setting up GitHub repository for deployment..." -ForegroundColor Green
Write-Host "=================================================" -ForegroundColor Green

# Check if we're in a git repository
if (!(Test-Path ".git")) {
    Write-Host "❌ Not a git repository. Initializing..." -ForegroundColor Yellow
    git init
    git branch -M main
}

# Add all files
Write-Host "📁 Adding files to git..." -ForegroundColor Cyan
git add .

# Check if there are changes to commit
$changes = git diff --cached --quiet
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ No changes to commit" -ForegroundColor Green
} else {
    Write-Host "💾 Committing changes..." -ForegroundColor Cyan
    git commit -m "🚀 Add GitHub Actions deployment workflows

- Add Streamlit Cloud deployment workflow
- Add Docker deployment workflow  
- Add comprehensive deployment guide
- Update README with deployment options"
}

# Check if remote exists
$remote = git remote get-url origin 2>$null
if ($remote) {
    Write-Host "🌐 Remote repository found" -ForegroundColor Green
    Write-Host "📤 Pushing to GitHub..." -ForegroundColor Cyan
    git push -u origin main
} else {
    Write-Host "⚠️  No remote repository found." -ForegroundColor Yellow
    Write-Host "To complete setup:" -ForegroundColor White
    Write-Host "1. Create a new repository on GitHub" -ForegroundColor White
    Write-Host "2. Add it as remote: git remote add origin https://github.com/USERNAME/REPO.git" -ForegroundColor White
    Write-Host "3. Push: git push -u origin main" -ForegroundColor White
}

Write-Host ""
Write-Host "✅ Setup complete! Next steps:" -ForegroundColor Green
Write-Host ""
Write-Host "🎯 For Streamlit Cloud deployment:" -ForegroundColor Magenta
Write-Host "   1. Visit https://share.streamlit.io" -ForegroundColor White
Write-Host "   2. Connect your GitHub repository" -ForegroundColor White
Write-Host "   3. Deploy beacon_analyzer_app.py" -ForegroundColor White
Write-Host ""
Write-Host "🐳 For Docker deployment:" -ForegroundColor Blue
Write-Host "   1. GitHub Actions will automatically build images" -ForegroundColor White
Write-Host "   2. Check the Actions tab in your GitHub repository" -ForegroundColor White
Write-Host ""
Write-Host "📚 For detailed instructions, see DEPLOYMENT.md" -ForegroundColor Cyan
