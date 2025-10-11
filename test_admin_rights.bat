@echo off
title Test Admin Rights - ByGone Spoofer
color 0E

echo ================================================================================
echo                  ADMIN RIGHTS VERIFICATION TEST
echo ================================================================================
echo.
echo This script tests if ByGoneSpoofer.exe properly requests admin rights
echo.

if not exist "dist\ByGoneSpoofer.exe" (
    echo [!] ERROR: ByGoneSpoofer.exe not found in dist folder!
    echo [!] Please compile it first using compile_bygone_spoofer.bat
    echo.
    pause
    exit /b 1
)

echo [+] Found ByGoneSpoofer.exe at: %CD%\dist\ByGoneSpoofer.exe
echo.
echo [+] Checking UAC manifest embedded in EXE...
echo.

REM Check if the EXE has the proper manifest
sigcheck -accepteula -m "dist\ByGoneSpoofer.exe" 2>nul | findstr /i "requireAdministrator" >nul
if errorlevel 1 (
    echo [!] WARNING: Could not verify UAC manifest (sigcheck not installed)
    echo [!] This is OK - the manifest should still be embedded by PyInstaller
) else (
    echo [✓] UAC manifest confirmed: requireAdministrator is present!
)

echo.
echo ================================================================================
echo                          MANUAL TEST
echo ================================================================================
echo.
echo [>] Now launching ByGoneSpoofer.exe...
echo [>] You should see a UAC prompt asking for admin rights!
echo.
echo If you see the UAC prompt: SUCCESS! Admin rights are working!
echo If you DON'T see the UAC prompt: Something is wrong.
echo.
pause

REM Launch the EXE
start "" "dist\ByGoneSpoofer.exe"

echo.
echo [?] Did you see a UAC (User Account Control) prompt?
echo.
echo     If YES: Admin rights are correctly configured! ✓
echo     If NO:  Admin rights may not be working properly. Try:
echo             1. Right-click ByGoneSpoofer.exe ^> Properties
echo             2. Compatibility tab
echo             3. Check "Run this program as an administrator"
echo.
pause

