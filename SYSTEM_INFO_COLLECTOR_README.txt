================================================================================
ByGone System Info Collector - README
================================================================================

PURPOSE:
This tool helps you debug user issues by collecting comprehensive system
information. When a user reports a problem (slow WiFi, spoofing failures, etc.),
have them run this tool and send you the generated files.

================================================================================
WHAT IT COLLECTS:
================================================================================

✓ Basic System Info
  - OS version, architecture, computer name
  - Python version, admin status

✓ CPU Information
  - Processor name, cores, threads, CPU ID

✓ Motherboard Information (CRITICAL for HWID issues)
  - Manufacturer (detects ASUS boards)
  - Model number
  - BIOS version
  - Serial numbers

✓ GPU Information (for graphics glitch issues)
  - Graphics card name
  - Driver version
  - VRAM
  - Status

✓ Memory Information
  - Total RAM
  - Memory module details

✓ Disk Information
  - Physical drives
  - Logical drives
  - Free space (detects low disk space)

✓ Network Adapters (CRITICAL for MAC spoofing issues)
  - All network adapters
  - Current MAC addresses
  - WiFi adapter detection (flags WiFi limitations)
  - Adapter manufacturers
  - IP configurations

✓ System UUID
  - Computer UUID
  - System model

✓ Installed Software
  - Roblox installation status
  - Antivirus software
  - Windows Defender status

✓ Running Processes
  - Checks for running Roblox processes
  - Full process list

✓ System Issues Detection
  - WMI service status
  - Low disk space warnings
  - Admin privilege check

================================================================================
HOW TO COMPILE TO EXE:
================================================================================

1. Install PyInstaller (if not already installed):
   pip install pyinstaller

2. Make sure colorama is installed:
   pip install colorama

3. Compile using the spec file:
   pyinstaller bygone_system_info_collector.spec

4. The EXE will be in the 'dist' folder:
   dist\BygoneSystemInfoCollector.exe

5. Distribute this EXE to users who need help!

================================================================================
HOW USERS RUN IT:
================================================================================

1. Download BygoneSystemInfoCollector.exe
2. Right-click → Run as Administrator (for complete info)
3. Press Enter to start collection
4. Wait for collection to complete (~10-30 seconds)
5. Find the generated files:
   - bygone_system_info_YYYYMMDD_HHMMSS.json (complete data)
   - bygone_system_info_YYYYMMDD_HHMMSS.txt (human-readable)
6. Send both files to you for debugging

================================================================================
OUTPUT FILES:
================================================================================

JSON File:
- Complete system information in machine-readable format
- Contains all raw data from WMIC commands
- Best for automated analysis

TXT File:
- Human-readable summary
- Shows key information at a glance
- Lists any detected issues

================================================================================
COMMON ISSUES DETECTED:
================================================================================

⚠️  ASUS Motherboard Detected
    → User may not be able to change HWID (hardware limitation)

⚠️  Wireless Adapter Detected
    → User may not be able to change MAC on WiFi (driver limitation)

⚠️  WMI Service Not Running
    → Spoofing will fail completely (needs to start service)

⚠️  Low Disk Space
    → May cause Roblox install failures

⚠️  Not Running as Administrator
    → All spoofing operations will fail

⚠️  Roblox Process Running
    → User needs to close Roblox before spoofing

================================================================================
DEBUGGING WORKFLOW:
================================================================================

1. User reports issue on Discord
2. Send them BygoneSystemInfoCollector.exe
3. User runs it and sends you the files
4. Open the TXT file first for quick overview
5. Check "POTENTIAL ISSUES DETECTED" section
6. If needed, open JSON for detailed info
7. Cross-reference with their reported issue
8. Provide targeted solution

Examples:

Issue: "MAC spoofing doesn't work"
→ Check network_info → Look for WiFi adapters
→ Solution: Explain it's a driver limitation on wireless

Issue: "HWID spoofing failed"
→ Check motherboard_info → is_asus: true
→ Solution: Explain ASUS motherboard limitation

Issue: "Spoofer crashes immediately"
→ Check system_issues → WMI not running
→ Solution: Start WMI service: net start winmgmt

Issue: "Graphics look weird after spoofing"
→ Check gpu_info → driver version, GPU model
→ Solution: Reboot or update GPU drivers

================================================================================
PRIVACY NOTE:
================================================================================

This tool collects hardware information only. It does NOT collect:
- Personal files
- Passwords
- Browser history
- User data

However, it does collect:
- Serial numbers
- MAC addresses
- Computer name
- Installed software list

Make sure users are comfortable sharing this info before requesting it.

================================================================================
SUPPORT:
================================================================================

For issues with the System Info Collector itself:
- Join discord.gg/bygone
- Report in the support channel

================================================================================
VERSION: 1.0
CREATED: 2025
AUTHOR: nitaybl
================================================================================

