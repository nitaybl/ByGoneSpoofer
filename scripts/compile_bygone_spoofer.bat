@echo off
title ByGone Spoofer - Compilation Script
color 0B

echo ================================================================================
echo.
echo        ByGone Spoofer - Compilation Script
echo        Compiling with Admin Rights Enabled
echo.
echo ================================================================================
echo.

echo [+] Starting ByGone Spoofer compilation process...
echo.

REM Check if Python is installed
echo [+] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo [!] ERROR: Python is not installed or not in PATH!
    echo [!] Please install Python from https://www.python.org/
    pause
    exit /b 1
)
echo [✓] Python is installed
echo.

REM Check if ByGoneSpoofer.py exists
echo [+] Checking if ByGoneSpoofer.py exists...
if not exist "ByGoneSpoofer.py" (
    echo [!] ERROR: ByGoneSpoofer.py not found in current directory!
    echo [!] Current directory: %CD%
    pause
    exit /b 1
)
echo [✓] ByGoneSpoofer.py found
echo.

REM Check if spec file exists
echo [+] Checking if ByGoneSpoofer.spec exists...
if not exist "ByGoneSpoofer.spec" (
    echo [!] ERROR: ByGoneSpoofer.spec not found!
    pause
    exit /b 1
)
echo [✓] ByGoneSpoofer.spec found
echo.

REM Check if icon exists
echo [+] Checking if icon file exists...
if not exist "ico.ico" (
    echo [!] WARNING: ico.ico not found. EXE will have default icon.
    echo.
) else (
    echo [✓] ico.ico found
    echo.
)

REM Install/Check PyInstaller
echo [+] Checking PyInstaller installation...
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo [!] PyInstaller not found. Installing...
    pip install pyinstaller
    if errorlevel 1 (
        echo [!] ERROR: Failed to install PyInstaller!
        pause
        exit /b 1
    )
    echo [✓] PyInstaller installed successfully
) else (
    echo [✓] PyInstaller is already installed
)
echo.

REM Install/Check required dependencies
echo [+] Checking required dependencies...
echo [+] Installing/verifying colorama...
pip install colorama --quiet
echo [+] Installing/verifying requests...
pip install requests --quiet
echo [+] Installing/verifying pywin32...
pip install pywin32 --quiet
echo [✓] All dependencies verified
echo.

REM Clean previous builds
echo [+] Cleaning previous build files...
if exist "build" (
    echo [>] Removing old build directory...
    rmdir /s /q build 2>nul
)
if exist "dist\ByGoneSpoofer.exe" (
    echo [>] Removing old ByGoneSpoofer.exe...
    del /f /q dist\ByGoneSpoofer.exe 2>nul
)
echo [✓] Cleanup complete
echo.

echo ================================================================================
echo                          STARTING COMPILATION
echo ================================================================================
echo.
echo [>] Compiling ByGoneSpoofer.py with ADMIN RIGHTS enabled...
echo [>] This may take 1-3 minutes. Please wait...
echo.

REM Run PyInstaller with the spec file
pyinstaller --clean --noconfirm ByGoneSpoofer.spec

REM Check if compilation was successful
if errorlevel 1 (
    echo.
    echo ================================================================================
    echo                          COMPILATION FAILED!
    echo ================================================================================
    echo [!] PyInstaller encountered errors during compilation.
    echo [!] Check the output above for error messages.
    echo.
    pause
    exit /b 1
)

REM Verify the EXE was created
if not exist "dist\ByGoneSpoofer.exe" (
    echo.
    echo ================================================================================
    echo                          COMPILATION FAILED!
    echo ================================================================================
    echo [!] ByGoneSpoofer.exe was not created in the dist folder.
    echo [!] Check for errors in the compilation process above.
    echo.
    pause
    exit /b 1
)

REM Success!
echo.
echo ================================================================================
echo                      COMPILATION SUCCESSFUL!
echo ================================================================================
echo.
echo [✓] ByGoneSpoofer.exe has been created successfully!
echo [✓] Location: %CD%\dist\ByGoneSpoofer.exe
echo.
echo [INFO] The EXE is configured with the following settings:
echo        - UAC Admin Rights: ENABLED (will request elevation on run)
echo        - Icon: %CD%\ico.ico
echo        - Console Mode: Enabled
echo        - Single File: Yes
echo.

REM Get file size
for %%A in (dist\ByGoneSpoofer.exe) do (
    set size=%%~zA
    set /a sizeMB=%%~zA/1024/1024
)
echo [INFO] File size: %sizeMB% MB
echo.

echo ================================================================================
echo                          NEXT STEPS
echo ================================================================================
echo.
echo 1. Navigate to: dist\ByGoneSpoofer.exe
echo 2. Run the EXE - it will automatically request admin rights (UAC prompt)
echo 3. The spoofer should work correctly with full admin privileges
echo.
echo [TIP] If UAC prompt doesn't appear, try:
echo       - Right-click the EXE ^> Properties ^> Compatibility
echo       - Check "Run this program as an administrator"
echo.
echo ================================================================================
echo                    Join discord.gg/bygone for support!
echo ================================================================================
echo.

pause

