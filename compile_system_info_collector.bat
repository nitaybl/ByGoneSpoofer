@echo off
echo ================================================================================
echo ByGone System Info Collector - Compilation Script
echo ================================================================================
echo.

echo Checking if PyInstaller is installed...
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo PyInstaller not found. Installing...
    pip install pyinstaller
) else (
    echo PyInstaller is already installed.
)

echo.
echo Checking if colorama is installed...
pip show colorama >nul 2>&1
if errorlevel 1 (
    echo Colorama not found. Installing...
    pip install colorama
) else (
    echo Colorama is already installed.
)

echo.
echo ================================================================================
echo Starting compilation...
echo ================================================================================
echo.

pyinstaller bygone_system_info_collector.spec

echo.
echo ================================================================================
echo Compilation complete!
echo ================================================================================
echo.
echo Your EXE is located at: dist\BygoneSystemInfoCollector.exe
echo.
echo [INFO] The EXE is configured with:
echo        - UAC Admin Rights: ENABLED (will request elevation on run)
echo        - This ensures complete system information collection
echo.
echo You can now distribute this EXE to users for debugging!
echo.
pause

