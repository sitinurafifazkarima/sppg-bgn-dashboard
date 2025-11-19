# Script untuk initialize Git dan prepare untuk deployment
# Jalankan: .\prepare_deploy.ps1

Write-Host "Preparing Dashboard SPPG BGN for Deployment..." -ForegroundColor Cyan
Write-Host ""

# Check if git is installed
try {
    $gitVersion = git --version
    Write-Host "[OK] $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Git tidak terinstall!" -ForegroundColor Red
    Write-Host "Download dari: https://git-scm.com/downloads"
    exit 1
}

Write-Host ""

# Initialize git if not already
if (!(Test-Path .git)) {
    Write-Host "Initializing Git repository..." -ForegroundColor Yellow
    git init
    Write-Host "[OK] Git initialized" -ForegroundColor Green
} else {
    Write-Host "[OK] Git repository already exists" -ForegroundColor Green
}

# Check if files exist
Write-Host ""
Write-Host "Checking required files..." -ForegroundColor Cyan

$requiredFiles = @(
    "dashboard_sppg.py",
    "requirements.txt",
    "sppg_data_complete_with_coordinates.csv",
    "README.md"
)

$allFilesExist = $true
foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Write-Host "  [OK] $file" -ForegroundColor Green
    } else {
        Write-Host "  [MISSING] $file" -ForegroundColor Red
        $allFilesExist = $false
    }
}

if (!$allFilesExist) {
    Write-Host ""
    Write-Host "[ERROR] Beberapa file penting tidak ditemukan!" -ForegroundColor Red
    exit 1
}

# Add files to git
Write-Host ""
Write-Host "Adding files to git..." -ForegroundColor Yellow
git add .

# Show status
Write-Host ""
Write-Host "Git status:" -ForegroundColor Cyan
git status --short

Write-Host ""
Write-Host "[SUCCESS] Repository ready for deployment!" -ForegroundColor Green
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "NEXT STEPS:" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Commit changes:" -ForegroundColor Yellow
Write-Host '   git commit -m "Initial commit: SPPG BGN Dashboard"' -ForegroundColor White
Write-Host ""
Write-Host "2. Create GitHub repository:" -ForegroundColor Yellow
Write-Host "   https://github.com/new" -ForegroundColor White
Write-Host ""
Write-Host "3. Add remote and push (ganti YOUR_USERNAME):" -ForegroundColor Yellow
Write-Host "   git remote add origin https://github.com/YOUR_USERNAME/sppg-bgn-dashboard.git" -ForegroundColor White
Write-Host "   git branch -M main" -ForegroundColor White
Write-Host "   git push -u origin main" -ForegroundColor White
Write-Host ""
Write-Host "4. Deploy to Streamlit Cloud:" -ForegroundColor Yellow
Write-Host "   https://share.streamlit.io" -ForegroundColor White
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Happy deploying!" -ForegroundColor Magenta
