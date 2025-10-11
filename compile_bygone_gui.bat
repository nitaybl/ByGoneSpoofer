@echo off
title ByGone Spoofer GUI - Compilation Script
color 0B

echo ================================================================================
echo.
echo        ByGone Spoofer GUI - Modern UI Compilation
echo        Compiling with Admin Rights Enabled
echo.
echo ================================================================================
echo.

echo [+] Starting ByGone Spoofer GUI compilation process...
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

REM Check if files exist
echo [+] Checking if ByGoneSpoofer_GUI.py exists...
if not exist "ByGoneSpoofer_GUI.py" (
    echo [!] ERROR: ByGoneSpoofer_GUI.py not found!
    pause
    exit /b 1
)
echo [✓] ByGoneSpoofer_GUI.py found
echo.

echo [+] Checking if ByGoneSpoofer.py exists (backend required)...
if not exist "ByGoneSpoofer.py" (
    echo [!] ERROR: ByGoneSpoofer.py not found! Backend required!
    pause
    exit /b 1
)
echo [✓] ByGoneSpoofer.py found
echo.

echo [+] Checking if ByGoneSpoofer_GUI.spec exists...
if not exist "ByGoneSpoofer_GUI.spec" (
    echo [!] ERROR: ByGoneSpoofer_GUI.spec not found!
    pause
    exit /b 1
)
echo [✓] ByGoneSpoofer_GUI.spec found
echo.

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
echo [+] Installing/verifying required dependencies...
echo [+] Installing colorama...
pip install colorama --quiet
echo [+] Installing requests...
pip install requests --quiet
echo [+] Installing pywin32...
pip install pywin32 --quiet
echo [+] Installing customtkinter...
pip install customtkinter --quiet
echo [✓] All dependencies verified
echo.

REM Clean previous builds
echo [+] Cleaning previous build files...
if exist "build" (
    echo [>] Removing old build directory...
    rmdir /s /q build 2>nul
)
if exist "dist\ByGoneSpoofer_GUI.exe" (
    echo [>] Removing old ByGoneSpoofer_GUI.exe...
    del /f /q dist\ByGoneSpoofer_GUI.exe 2>nul
)
echo [✓] Cleanup complete
echo.

echo ================================================================================
echo                          STARTING COMPILATION
echo ================================================================================
echo.
echo [>] Compiling ByGoneSpoofer_GUI.py with ADMIN RIGHTS enabled...
echo [>] This may take 2-4 minutes. Please wait...
echo.

REM Run PyInstaller with the spec file
pyinstaller --clean --noconfirm ByGoneSpoofer_GUI.spec

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
if not exist "dist\ByGoneSpoofer_GUI.exe" (
    echo.
    echo ================================================================================
    echo                          COMPILATION FAILED!
    echo ================================================================================
    echo [!] ByGoneSpoofer_GUI.exe was not created in the dist folder.
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
echo [✓] ByGoneSpoofer_GUI.exe has been created successfully!
echo [✓] Location: %CD%\dist\ByGoneSpoofer_GUI.exe
echo.
echo [INFO] The EXE is configured with the following settings:
echo        - Modern GUI: CustomTkinter-based sleek interface
echo        - UAC Admin Rights: ENABLED (will request elevation on run)
echo        - Icon: %CD%\ico.ico
echo        - Console Mode: Disabled (GUI only)
echo        - Single File: Yes
echo.

REM Get file size
for %%A in (dist\ByGoneSpoofer_GUI.exe) do (
    set size=%%~zA
    set /a sizeMB=%%~zA/1024/1024
)
echo [INFO] File size: %sizeMB% MB
echo.

echo ================================================================================
echo                          NEXT STEPS
echo ================================================================================
echo.
echo 1. Navigate to: dist\ByGoneSpoofer_GUI.exe
echo 2. Run the EXE - it will automatically request admin rights (UAC prompt)
echo 3. Enjoy the modern, sleek UI!
echo.
echo [TIP] The GUI version has all features of the console version
echo       but with a beautiful modern interface.
echo.
echo ================================================================================
echo                    Join discord.gg/bygone for support!
echo ================================================================================
echo.

pause

