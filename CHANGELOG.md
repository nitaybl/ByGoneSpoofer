# Changelog

All notable changes to ByGone Spoofer will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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

