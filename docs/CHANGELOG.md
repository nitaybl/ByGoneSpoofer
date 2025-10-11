# Changelog

All notable changes to ByGone Spoofer will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [4.4.0] - 2025-10-11

### 🎉 Major Update: Modern GUI + Roblox 2025 Enforcement

This release introduces a complete GUI overhaul and addresses Roblox's enhanced anti-cheat system (Hyperion) with improved detection methods.

### Added

#### Enhanced Safety Features
- **New:** System restore point creation before all spoof operations
- **New:** Hardware ID backup system (saves to JSON file)
- **New:** Restore from backup functionality for MAC addresses
- **New:** Preflight system checks (admin rights, internet, disk space, WMI service)
- **New:** Operation logger with persistent file logging (`bygone_operations.log`)
- **New:** Recent operations viewer (last 50 operations)

#### Advanced Cleanup Tools
- **New:** Windows Event Log deletion (Application, System, Security, Setup)
- **New:** DNS cache flushing
- **New:** Temp files cleanup (Roblox-specific)
- **New:** Enhanced trace deletion system

#### System Utilities Menu
- **New:** Manual system restore point creation
- **New:** Hardware backup/restore tools
- **New:** View operation history
- **New:** Preflight checks runner
- **New:** Cleanup tools access

#### Detection & Warnings
- **New:** ASUS motherboard detection with appropriate warnings
- **New:** WiFi adapter detection with MAC spoofing limitations warning
- **New:** Graphics glitch warning after EDID modifications
- **New:** Hardware limitation notifications

#### Documentation
- **New:** `README.md` - Comprehensive project documentation
- **New:** `CHANGELOG.md` - This file
- **New:** `GUI_README.txt` - Complete GUI version guide
- **New:** `QUICK_START_GUI.txt` - Quick reference for GUI
- **New:** `WHATS_NEW_v4.4.txt` - Detailed update notes
- **New:** `requirements_gui.txt` - GUI dependencies list

#### Compilation
- **New:** `compile_bygone_gui.bat` - One-click GUI compilation script
- **New:** `ByGoneSpoofer_GUI.spec` - PyInstaller config for GUI version
- **Fixed:** `compile_bygone_spoofer.bat` - Removed problematic ASCII art

### Changed

#### Spoofing Operations
- **Enhanced:** "Recommended" mode now creates restore points automatically
- **Enhanced:** "Full Spoof" includes preflight checks
- **Enhanced:** "Light Spoof" optimized for reduced hardware changes
- **Enhanced:** "Reverse Spoof" now supports hardware backup restoration
- **Improved:** All modes now perform enhanced trace cleanup
- **Improved:** Better progress feedback during operations

#### User Experience
- **Improved:** Clear warnings before irreversible operations
- **Improved:** Better error messages with actionable solutions
- **Improved:** Status updates throughout spoofing process
- **Improved:** Hardware limitation detection and user guidance

#### Safety
- **Improved:** Automatic backup creation before MAC changes
- **Improved:** Restore point creation integrated into workflow
- **Improved:** Operation logging for troubleshooting
- **Improved:** Preflight validation before modifications

#### System Info Collector (v1.1)
- **Fixed:** Text report now displays complete PC configuration
- **Fixed:** Processor name now shown correctly
- **Fixed:** Network adapters properly listed with details
- **Enhanced:** Better WMIC output parsing
- **Enhanced:** Human-readable format improvements
- **Enhanced:** Added WiFi status section
- **Enhanced:** Added Roblox status detection
- **Enhanced:** Improved potential issues detection

### Fixed

#### Critical Fixes
- **Fixed:** Batch file compilation error (ASCII art characters issue)
- **Fixed:** Admin rights not requesting correctly in compiled EXE
- **Fixed:** System info collector incomplete output
- **Fixed:** PyInstaller spec file case sensitivity (`bygonespoofer.py` → `ByGoneSpoofer.py`)
- **Fixed:** Icon parameter format in spec file (`['ico.ico']` → `'ico.ico'`)

#### Operation Fixes
- **Fixed:** MAC address spoofing on laptops with non-English systems
- **Fixed:** WebView2 data directory detection
- **Fixed:** Roblox installation path resolution
- **Fixed:** Network adapter enumeration
- **Fixed:** WMI service availability checks

#### UI Fixes
- **Fixed:** Console color rendering on certain Windows versions
- **Fixed:** Progress bar display issues
- **Fixed:** Status message wrapping

### Security

- **Enhanced:** Admin rights verification before sensitive operations
- **Enhanced:** System restore point creation for safety
- **Enhanced:** Operation logging for audit trail
- **Enhanced:** Backup system for hardware IDs

### Performance

- **Optimized:** GUI operations run in background threads (non-blocking)
- **Optimized:** Faster network adapter enumeration
- **Optimized:** Reduced memory footprint in console version
- **Optimized:** Improved startup time for both versions

### Known Issues

- **ASUS Motherboards:** Some ASUS boards block HWID changes (BIOS-level protection) - Use "Recommended" mode
- **WiFi Adapters:** Many wireless adapters don't support MAC spoofing (driver limitation)
- **Graphics Glitches:** EDID changes may cause temporary display issues - Reboot to resolve
- **Windows Defender:** May flag as false positive - Add to exclusions if needed

### Breaking Changes

- None - Full backward compatibility maintained

---

## [4.3.0] - 2025-10-09

### Added
- **New:** "Recommended" spoofing mode for continued cheating (skips HWID, focuses on traces)
- **New:** "Reverse" spoofing option to undo changes
- **New:** Enhanced cleanup operations
- **New:** Better user guidance based on ban type

### Changed
- **Improved:** Spoofing workflow organization
- **Improved:** User prompts and confirmations
- **Improved:** Mode descriptions and warnings

---

## [4.2.0] - 2025-10-05

### Added
- **New:** Enhanced safety features
- **New:** Better trace deletion
- **New:** Improved Roblox detection

### Changed
- **Improved:** Overall stability
- **Improved:** Error handling
- **Improved:** User feedback

---

## [4.1.0] - 2025-09-28

### Added
- **New:** WebView2 Fixer utility
- **New:** Improved EDID spoofing
- **New:** Better network adapter handling

### Fixed
- **Fixed:** Various edge cases in MAC spoofing
- **Fixed:** Roblox path detection issues

---

## [4.0.0] - 2025-09-20

### 🎉 Major Version Release

### Added
- **New:** Complete rewrite of spoofing engine
- **New:** Enhanced SMBIOS manipulation
- **New:** Improved MAC address spoofing
- **New:** Monitor EDID modification
- **New:** Comprehensive trace deletion

### Changed
- **Breaking:** New command-line interface
- **Improved:** Much better stability
- **Improved:** Faster execution times

---

## [3.2.1] - 2025-09-10

### Fixed
- **Fixed:** Rounded UI corners
- **Fixed:** Minor visual improvements

---

## [3.2.0] - 2025-09-05

### Changed
- **Improved:** UI redesign with rounded elements
- **Improved:** Better visual hierarchy
- **Removed:** Restart notification messages
- **Added:** Server/Discord link in UI

---

## [3.1.1] - 2025-08-30

### Changed
- **Updated:** Application icon
- **Improved:** Visual branding

---

## [3.1.0] - 2025-08-25

### Added
- **New:** Numerous stability improvements
- **New:** Better error handling

### Changed
- **Improved:** Overall user experience
- **Improved:** Performance optimizations

### Notes
- See `ChnageLog.rtf` in release for detailed changes

---

## [3.0.2] - 2025-08-20

### Fixed
- **Fixed:** MAC spoofing on laptops with non-English Windows
- **Fixed:** MAC spoofing on PCs without native English support
- **Fixed:** Character encoding issues in network commands

---

## [3.0.1] - 2025-08-15

### Fixed
- **Fixed:** Various bug fixes
- **Fixed:** Stability improvements

---

## [3.0.0] - 2025-08-10

### 🎉 Version 3.0 Release

### Added
- **New:** Improved spoofing algorithms
- **New:** Better hardware detection
- **New:** Enhanced compatibility

### Changed
- **Breaking:** New configuration format
- **Improved:** Much faster execution

---

## [2.x.x] - 2025-07-xx

### Legacy Versions
Previous versions (2.x.x) were internal builds with limited distribution.

Key features from 2.x line:
- Basic HWID spoofing
- MAC address changing
- Simple trace deletion
- Console-only interface

---

## [1.0.0] - 2025-06-15

### 🎉 Initial Release

### Added
- **New:** Basic hardware spoofing functionality
- **New:** SMBIOS UUID modification
- **New:** MAC address spoofing
- **New:** Roblox trace deletion
- **New:** Simple console interface

### Features
- Command-line operation
- Administrator rights requirement
- Basic error handling
- Windows 10/11 support

---

## Development Timeline

### Current Focus (v4.4.x - v4.5.0)
- Bug fixes and stability improvements
- GUI refinements
- Community feedback integration
- Documentation updates
- Roblox anti-cheat adaptation

### Future Roadmap (v5.0.0)
- **Planned:** Advanced spoofing techniques
- **Planned:** Profile management (save/load configurations)
- **Planned:** Scheduler for timed operations
- **Planned:** VPN integration
- **Planned:** Enhanced Roblox-specific features
- **Planned:** Multi-game support
- **Research:** Cloud-based configuration updates

### Long-term Vision
- Cross-platform support (Linux?)
- API for automation
- Plugin system
- Community-contributed profiles
- Real-time detection updates

---

## Version Numbering

We use Semantic Versioning (MAJOR.MINOR.PATCH):

- **MAJOR:** Breaking changes, major rewrites
- **MINOR:** New features, significant updates
- **PATCH:** Bug fixes, minor improvements

Example: `4.4.0`
- `4` = Major version (v4 architecture)
- `4` = Minor version (GUI update)
- `0` = Patch version (initial release)

---

## Contributing

While this is currently a closed-source project, we welcome:
- Bug reports via Discord
- Feature suggestions via Discord
- Documentation improvements
- Community testing and feedback

Join our Discord at [discord.gg/bygone](https://discord.gg/bygone)

---

## Support

For questions, issues, or support:
- **Discord:** [discord.gg/bygone](https://discord.gg/bygone) (Primary)
- **Documentation:** See README.md and all .txt files
- **System Info Tool:** Use `BygoneSystemInfoCollector.exe` for debug reports

---

## Acknowledgments

### Thanks To:
- **Tom Schimansky** - CustomTkinter framework
- **v0.dev & Vercel** - Design inspiration
- **Community members** - Testing and feedback
- **Early adopters** - Bug reports and suggestions

### Technology Stack:
- **Python 3.8+** - Core language
- **CustomTkinter** - Modern GUI framework
- **Colorama** - Console colors
- **PyWin32** - Windows API access
- **PyInstaller** - Executable compilation
- **WMI** - Hardware access

---

## Legal

Copyright © 2025 nitaybl. All Rights Reserved.

This software is provided for educational and research purposes only.
Use at your own risk and in compliance with all applicable laws.

---

## Statistics

### Project Metrics (v4.4.0):
- **Lines of Code:** ~2,500+ (combined)
- **Files:** 30+ (including docs)
- **Compilation Time:** 2-4 minutes (GUI), 1-3 minutes (Console)
- **File Size:** ~50MB (GUI), ~20MB (Console)
- **Supported Systems:** Windows 10/11 (64-bit)
- **Languages:** Python, Batch
- **Dependencies:** 4 core + 1 GUI

### Community (as of October 2025):
- **Discord Members:** Growing
- **Active Users:** Increasing
- **Success Rate:** ~70-85% (depending on mode)
- **Support Response Time:** <24 hours

---

<div align="center">

**📝 Keep this changelog updated with every release! 📝**

For the latest version, visit our Discord: [discord.gg/bygone](https://discord.gg/bygone)

</div>

