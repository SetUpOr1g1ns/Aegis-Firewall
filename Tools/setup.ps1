# ===============================================
#  Aegis Firewall Setup Script
#  - Installs Python 3.12
#  - Installs required Python modules
#  - Creates desktop shortcut to run_firewall.bat
# ===============================================

# ---------------------------
# Step 1: Install Python
# ---------------------------
$pythonInstallerUrl = "https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe"
$installerPath = "$env:TEMP\python_installer.exe"

# Required modules
$modules = @("pillow", "pystray", "sqlite3", "requests")

# Check if Python is already installed
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "Downloading Python installer..."
    Invoke-WebRequest -Uri $pythonInstallerUrl -OutFile $installerPath

    Write-Host "Installing Python..."
    Start-Process -FilePath $installerPath -ArgumentList "/quiet InstallAllUsers=1 PrependPath=1 Include_pip=1" -Wait
} else {
    Write-Host "Python is already installed. Skipping installation."
}

# Verify installation
if (Get-Command python -ErrorAction SilentlyContinue) {
    Write-Host "Python installed successfully."

    # Upgrade pip
    Write-Host "Upgrading pip..."
    python -m pip install --upgrade pip

    # Install each module
    foreach ($module in $modules) {
        Write-Host "Installing Python module: $module"
        python -m pip install $module
    }

    Write-Host "All modules installed successfully."
} else {
    Write-Host "Python installation failed. Please check the installer or permissions."
    exit 1
}

# ---------------------------
# Step 2: Create desktop shortcut
# ---------------------------
$ProjectDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$BatPath = Join-Path $ProjectDir "Aegis.bat"

if (-not (Test-Path $BatPath)) {
    Write-Host "ERROR: Aegis.bat not found in $ProjectDir"
    exit 1
}

$WScriptShell = New-Object -ComObject WScript.Shell
$Desktop = [Environment]::GetFolderPath("Desktop")
$ShortcutPath = Join-Path $Desktop "Aegis Firewall.lnk"

$Shortcut = $WScriptShell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = $BatPath
$Shortcut.WorkingDirectory = $ProjectDir
$Shortcut.IconLocation = "shell32.dll,48"
$Shortcut.Save()

Write-Host "[+] Created desktop shortcut at $ShortcutPath"
Write-Host "✅ Setup complete! Use the 'Aegis Firewall' shortcut on your desktop to launch with admin rights."