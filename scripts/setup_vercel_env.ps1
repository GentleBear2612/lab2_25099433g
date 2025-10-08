# PowerShell script to help set up Vercel environment variables
# Usage: .\scripts\setup_vercel_env.ps1

Write-Host "=" -NoNewline; Write-Host ("=" * 59)
Write-Host "Vercel Environment Variables Setup Helper"
Write-Host "=" -NoNewline; Write-Host ("=" * 59)
Write-Host ""

# Check if vercel CLI is installed
Write-Host "Checking for Vercel CLI..." -ForegroundColor Yellow
$vercelInstalled = Get-Command vercel -ErrorAction SilentlyContinue

if (-not $vercelInstalled) {
    Write-Host "❌ Vercel CLI is not installed." -ForegroundColor Red
    Write-Host ""
    Write-Host "To install Vercel CLI, run:" -ForegroundColor Cyan
    Write-Host "  npm install -g vercel" -ForegroundColor White
    Write-Host ""
    Write-Host "Or set environment variables manually in the Vercel Dashboard:" -ForegroundColor Cyan
    Write-Host "  1. Visit https://vercel.com/dashboard" -ForegroundColor White
    Write-Host "  2. Select your project" -ForegroundColor White
    Write-Host "  3. Go to Settings > Environment Variables" -ForegroundColor White
    Write-Host ""
    exit 1
}

Write-Host "✅ Vercel CLI is installed" -ForegroundColor Green
Write-Host ""

# Check if user is logged in
Write-Host "Checking Vercel login status..." -ForegroundColor Yellow
$whoami = vercel whoami 2>&1

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Not logged in to Vercel." -ForegroundColor Red
    Write-Host ""
    Write-Host "Please log in first:" -ForegroundColor Cyan
    Write-Host "  vercel login" -ForegroundColor White
    Write-Host ""
    exit 1
}

Write-Host "✅ Logged in as: $whoami" -ForegroundColor Green
Write-Host ""

# Prompt for MongoDB URI
Write-Host "=" -NoNewline; Write-Host ("=" * 59)
Write-Host "MongoDB Configuration"
Write-Host "=" -NoNewline; Write-Host ("=" * 59)
Write-Host ""

Write-Host "⚠️  IMPORTANT: Your MongoDB URI should look like:" -ForegroundColor Yellow
Write-Host "   mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority" -ForegroundColor Gray
Write-Host ""

$mongoUri = Read-Host "Enter your MongoDB URI (or press Enter to skip)"

if ([string]::IsNullOrWhiteSpace($mongoUri)) {
    Write-Host "⚠️  Skipping MONGO_URI. Your app will use in-memory storage." -ForegroundColor Yellow
    Write-Host "   Data will NOT be persisted!" -ForegroundColor Yellow
    Write-Host ""
} else {
    # Validate URI format
    if ($mongoUri -match "^mongodb(\+srv)?://") {
        Write-Host "✅ URI format looks valid" -ForegroundColor Green
        
        # Add to Vercel
        Write-Host ""
        Write-Host "Adding MONGO_URI to Vercel..." -ForegroundColor Yellow
        
        # For security, don't echo the full URI
        $cmd = "vercel env add MONGO_URI production"
        Write-Host "Running: $cmd" -ForegroundColor Gray
        
        # Create a temporary file with the URI
        $tempFile = [System.IO.Path]::GetTempFileName()
        $mongoUri | Out-File -FilePath $tempFile -Encoding utf8 -NoNewline
        
        # Use the temp file as input
        Get-Content $tempFile | vercel env add MONGO_URI production
        
        # Clean up
        Remove-Item $tempFile -Force
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ MONGO_URI added successfully" -ForegroundColor Green
        } else {
            Write-Host "❌ Failed to add MONGO_URI" -ForegroundColor Red
        }
    } else {
        Write-Host "❌ Invalid URI format. Expected to start with 'mongodb://' or 'mongodb+srv://'" -ForegroundColor Red
        Write-Host "   Please add it manually in the Vercel Dashboard." -ForegroundColor Yellow
    }
}

Write-Host ""

# Prompt for database name
$dbName = Read-Host "Enter database name (default: notetaker_db, press Enter to use default)"

if ([string]::IsNullOrWhiteSpace($dbName)) {
    $dbName = "notetaker_db"
    Write-Host "✅ Using default database name: $dbName" -ForegroundColor Green
}

Write-Host ""
Write-Host "Adding MONGO_DB_NAME to Vercel..." -ForegroundColor Yellow
echo $dbName | vercel env add MONGO_DB_NAME production

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ MONGO_DB_NAME added successfully" -ForegroundColor Green
} else {
    Write-Host "❌ Failed to add MONGO_DB_NAME" -ForegroundColor Red
}

Write-Host ""
Write-Host "=" -NoNewline; Write-Host ("=" * 59)
Write-Host "Setup Complete!"
Write-Host "=" -NoNewline; Write-Host ("=" * 59)
Write-Host ""

Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. Verify environment variables in Vercel Dashboard" -ForegroundColor White
Write-Host "  2. Deploy your application:" -ForegroundColor White
Write-Host "       vercel --prod" -ForegroundColor Gray
Write-Host "  3. Test your deployment:" -ForegroundColor White
Write-Host "       Visit https://your-app.vercel.app/api/notes" -ForegroundColor Gray
Write-Host ""

Write-Host "For more help, see:" -ForegroundColor Cyan
Write-Host "  - DEPLOY_VERCEL.md" -ForegroundColor White
Write-Host "  - VERCEL_SETUP.md" -ForegroundColor White
Write-Host ""
