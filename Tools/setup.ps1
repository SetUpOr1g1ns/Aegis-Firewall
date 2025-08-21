# Define Python installer URL and local path
$pythonInstallerUrl = "https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe"
$installerPath = "$env:TEMP\python_installer.exe"

# Define Python modules to install
$modules = @("tkinter", "PIL", "pystray", "threading", "sqlite3", "subprocess", "ipaddress", "datetime", "csv", "request")

# Download Python installer
Write-Host "Downloading Python installer..."
Invoke-WebRequest -Uri $pythonInstallerUrl -OutFile $installerPath

# Install Python silently with pip and add to PATH
Write-Host "Installing Python..."
Start-Process -FilePath $installerPath -ArgumentList "/quiet InstallAllUsers=1 PrependPath=1 Include_pip=1" -Wait

# Confirm Python installation
if (Get-Command python -ErrorAction SilentlyContinue) {
    Write-Host "Python installed successfully."

    # Upgrade pip (optional but recommended)
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
}
