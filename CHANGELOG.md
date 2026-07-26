# Changelog

All notable changes to ByGone Spoofer will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [4.8.0] - 2026-07-26

### Added

- **Built-in auto-updater.** On launch, ByGone Spoofer checks GitHub for a newer
  release. If one is found it shows the new version's changelog and lets you choose to:
  - **Install now** — downloads the new EXE and relaunches into it automatically
    (a small batch script swaps the executable once the old one exits),
  - **Remind me later** — you'll be asked again next launch, or
  - **Skip this version** — you won't be prompted about that version again.
  Running from source shows the release link instead of self-replacing. A failed or
  offline check is silent and never blocks startup.

### Changed

- Centralized the version in a single `APP_VERSION` constant (used by the banner and
  the updater) and bumped it to v4.8.0.

---

## [4.7.0] - 2026-07-26

### Fixed

- **HWID spoof now actually changes the System UUID.** The SMBIOS spoof previously
  passed the invalid argument `/SU Auto` to AMIDEWIN, so the UUID never changed. It now
  generates a real random UUID and also randomizes the system and baseboard serials
  (`/SU`, `/SS`, `/BS`), and surfaces AMIDEWIN's output when a write is blocked.
- **HWID restore-from-backup now works.** `restore_hwid_from_backup()` called an
  undefined `get_bundled_amidewin()` and always failed. Added `get_amidewin_exe()`
  (downloads AMIDEWIN if needed), corrected the swapped `/SS` (system serial) and `/BS`
  (baseboard serial) parameters, and hardened the WMIC CSV parsing.
- **Roblox detection checks all install locations.** The WebView2 fixer only looked in
  `C:\Program Files (x86)\Roblox\Versions`. It now searches `C:\Program Files`,
  `C:\Program Files (x86)`, and `%LOCALAPPDATA%\Roblox\Versions`, picking the newest
  version folder across all of them.
- **LICENSE now detected by GitHub.** Moved the usage disclaimer into `DISCLAIMER.md`
  so the `LICENSE` file is clean MIT text and GitHub's license detection recognizes it.

### Added

- **Automated Windows build & release** via GitHub Actions
  (`.github/workflows/build-release.yml`): pushes to `main` and PRs build the EXE for
  validation, and pushing a `v*` tag builds the EXE on a Windows runner and attaches it
  to the GitHub Release automatically.

### Changed

- Updated banner version string to v4.7.
- README: added a quick-links guide row at the top and a documentation index; docs
  landing page no longer shows the screenshot-placeholder note.

---

## [4.6.0] - 2026-07-26

### Added

- **Post-spoof connectivity check** — After a MAC address is spoofed, the tool now
  waits 10 seconds and pings `google.com`. If there is no response, it rechecks every
  10 seconds for up to 40 seconds before timing out. On timeout the user is warned and
  offered the choice to restore the original MAC address(es) or keep the spoofed ones.
- **Wider network adapter detection** — Adapter enumeration now falls back through
  multiple sources so adapters are found on a much wider range of machines:
  1. `wmic` (Windows 10 / older builds)
  2. PowerShell CIM (`Get-CimInstance Win32_NetworkAdapter`) for modern Windows 11
     builds where `wmic` has been removed
  3. Direct registry walk of the network class key (fully offline last resort)
- **GitBook documentation site** — A complete `docs/` tree (getting started, usage
  walkthrough, spoofing modes, VPN guidance, Windows activation, troubleshooting, and a
  hard-spoof warning) plus a GitBook setup guide.

### Changed

- Extracted a shared `restore_mac_for_adapter()` helper used by both the Reverse Spoof
  option and the new connectivity restore-offer.
- Removed the redundant blind 10-second "stabilize" pauses in the Full / Light /
  Recommended flows — the active connectivity check now handles adapter stabilization.
- Refreshed `README.md`: Roblox-only banner, status badges, ASCII loader preview, and a
  link to the GitBook docs.
- Updated banner version string to v4.6.

---

## [4.5.0] - 2026-07-12

### Added

- **FishStrap / BloxStrap installer support** — When reinstalling Roblox, users can now choose between:
  - Standard Roblox (official installer)
  - FishStrap (custom bootstrapper via fishstrap.app)
  - BloxStrap (custom bootstrapper auto-downloaded from GitHub)
- **Download progress bar** for Roblox/BloxStrap installer downloads
- **Skip installation option** — Users can now choose to skip the Roblox reinstall step

### Fixed

- **Compilation script fixes** (reported by [@echohumm](https://github.com/echohumm)):
  - Fixed LF line endings → CRLF for Windows compatibility
  - Fixed path assumptions — script now navigates to project root from `scripts/` directory
  - Fixed `pyinstaller` not on PATH — now uses `python -m PyInstaller`
  - Fixed `echo [>]` creating a stray `]` file — now properly escaped with `[^>]`
  - Fixed `pip` commands → `python -m pip` for reliability
- **Updated Discord link** to new server: discord.gg/3aZX4TukBC

### Changed

- Refactored `install_roblox()` into modular functions (`_install_standard_roblox()`, `_install_via_fishstrap()`, `_install_via_bloxstrap()`, `_wait_for_roblox_install()`)
- Added shared `_download_file_with_progress()` helper with progress bar support
- Updated version string to v4.5

### Contributors

- [@echohumm](https://github.com/echohumm) — Identified and documented all 4 compilation script issues

---

## [4.4.0] - 2025-10-11

### Added

- **System restore point creation** before spoofing operations
- **Hardware ID backup system** (saves to JSON file)
- **Restore from backup** functionality for MAC addresses
- **Preflight system checks** (admin rights, internet, disk space, WMI service)
- **Operation logger** with persistent file logging
- **Windows Event Log deletion** (Application, System, Security, Setup)
- **DNS cache flushing**
- **Temp files cleanup** (application-specific)
- **Enhanced trace deletion system**
- **ASUS motherboard detection** with appropriate warnings
- **WiFi adapter detection** with MAC spoofing limitations warning
- Hardware limitation notifications

### Changed

- **Enhanced "Recommended" mode** - Now creates restore points automatically
- **Improved "Full Spoof"** - Includes preflight checks
- **Optimized "Light Spoof"** - Reduced hardware changes
- **Better "Reverse Spoof"** - Supports hardware backup restoration
- **Improved trace cleanup** - More thorough removal
- **Better progress feedback** - Real-time status updates
- **Enhanced error messages** - More actionable solutions

### Fixed

- Admin rights verification issues
- MAC address spoofing on non-English systems
- Network adapter enumeration
- WMI service availability checks
- Roblox installation path resolution

### Security

- Enhanced admin rights verification
- System restore point creation for safety
- Operation logging for audit trail
- Backup system for hardware IDs

---

## [4.3.0] - 2025-10-09

### Added

- "Recommended" spoofing mode (skips HWID, focuses on traces)
- "Reverse" spoofing option to undo changes
- Enhanced cleanup operations
- Better user guidance based on use case

### Changed

- Improved spoofing workflow organization
- Better user prompts and confirmations
- Enhanced mode descriptions and warnings

---

## [4.2.0] - 2025-10-05

### Added

- Enhanced safety features
- Better trace deletion
- Improved system detection

### Changed

- Overall stability improvements
- Better error handling
- Enhanced user feedback

---

## [4.0.0] - 2025-09-20

### Added

- Complete rewrite of spoofing engine
- Enhanced SMBIOS manipulation
- Improved MAC address spoofing
- Monitor EDID modification
- Comprehensive trace deletion

### Changed

- **Breaking:** New command-line interface
- Much better stability
- Faster execution times

---

## [3.0.0] - 2025-08-10

### Added

- Improved spoofing algorithms
- Better hardware detection
- Enhanced compatibility

### Changed

- **Breaking:** New configuration format
- Faster execution

---

## [1.0.0] - 2025-06-15

### Added

- Initial release
- Basic hardware spoofing functionality
- SMBIOS UUID modification
- MAC address spoofing
- Trace deletion
- Console interface
- Administrator rights requirement
- Basic error handling
- Windows 10/11 support

---

## Roadmap

### Planned for v5.0.0

- Advanced spoofing techniques
- Profile management (save/load configurations)
- Scheduler for timed operations
- Enhanced trace detection
- Multi-platform support research
- Improved hardware compatibility

### Long-term Vision

- Cross-platform support
- API for automation
- Plugin system
- Community-contributed profiles
- Real-time detection updates

---

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
