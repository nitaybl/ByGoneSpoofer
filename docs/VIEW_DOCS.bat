@echo off
title ByGone Spoofer - Documentation Viewer
color 0B

echo.
echo ================================================================================
echo                  ByGone Spoofer v4.4 - Documentation
echo ================================================================================
echo.
echo Choose a document to view:
echo.
echo  [1] README.md (Main Documentation) ⭐
echo  [2] ROBLOX_2025_GUIDE.md (Anti-Cheat Guide) ⭐
echo  [3] INDEX.md (Documentation Index)
echo  [4] CHANGELOG.md (Version History)
echo  [5] QUICK_START_GUI.txt (GUI Quick Start)
echo  [6] START_HERE.txt (Console Quick Start)
echo  [7] GUI_README.txt (GUI Complete Guide)
echo  [8] COMPILATION_README.txt (Compilation Guide)
echo  [9] WHATS_NEW_v4.4.txt (Latest Updates)
echo  [A] Open Project Folder
echo  [0] Exit
echo.
echo ================================================================================
echo.

set /p choice="Enter your choice: "

if "%choice%"=="1" start README.md
if "%choice%"=="2" start ROBLOX_2025_GUIDE.md
if "%choice%"=="3" start INDEX.md
if "%choice%"=="4" start CHANGELOG.md
if "%choice%"=="5" start ..\QUICK_START_GUI.txt
if "%choice%"=="6" start ..\START_HERE.txt
if "%choice%"=="7" start ..\GUI_README.txt
if "%choice%"=="8" start ..\COMPILATION_README.txt
if "%choice%"=="9" start ..\WHATS_NEW_v4.4.txt
if /i "%choice%"=="A" start ..
if "%choice%"=="0" exit

echo.
echo Opening document...
timeout /t 2 >nul

cls
goto :eof

