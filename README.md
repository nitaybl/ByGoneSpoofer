# ByGone Spoofer

<div align="center">

**Hardware Identifier Spoofing Tool for Windows**

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows%2010%2F11-lightgrey.svg)](https://www.microsoft.com/windows)

*Open-source tool for modifying hardware identifiers and removing system traces*

</div>

---

## ⚠️ Disclaimer

**This software is provided for educational and research purposes only.** Using this tool may violate terms of service agreements. Use at your own risk and responsibility. The developers are not liable for any misuse or damages.

---

## 📋 Overview

ByGone Spoofer is a Windows application designed to modify hardware identifiers (HWID) and remove system traces. It's particularly useful for understanding hardware fingerprinting and bypassing hardware-based restrictions.

### Key Features

- 🔧 **Hardware Spoofing** - Modify SMBIOS, MAC addresses, EDID
- 🧹 **Trace Removal** - Clean registry, event logs, temp files
- 💾 **Safety Features** - System restore points, hardware backups
- 🔍 **Preflight Checks** - System validation before changes
- 📋 **Operation Logging** - Complete audit trail

---

## 🚀 Quick Start

### Prerequisites

- Windows 10/11 (64-bit)
- Python 3.8 or higher
- Administrator privileges

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/bygone-spoofer.git
cd bygone-spoofer
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run as administrator:
```bash
python ByGoneSpoofer.py
```

---

## 📖 Usage

### Basic Usage

Run the script with administrator privileges:

```bash
python ByGoneSpoofer.py
```

### Spoofing Options

1. **Full Spoof** - Complete HWID, EDID, and MAC spoofing
2. **Light Spoof** - EDID and MAC only (no HWID changes)
3. **Recommended** - Trace removal focused (safest option)
4. **Reverse** - Undo MAC address changes

### Safety Features

The tool includes built-in safety mechanisms:

- **System Restore Points** - Automatic backup before changes
- **Hardware ID Backup** - Save original values to JSON
- **Preflight Checks** - Validates system before modifications
- **Operation Logging** - Complete audit trail

---

## 🔧 What Gets Modified

### Hardware Identifiers

| Component | Modified | Reversible |
|-----------|----------|------------|
| SMBIOS UUID | ✓ | Via restore point |
| MAC Address | ✓ | Yes (via backup) |
| Monitor EDID | ✓ | Via restore point |
| Motherboard Serial | ✓ | Via restore point |

### System Cleanup

- Registry traces (Roblox-specific)
- Windows Event Logs
- Temporary files
- DNS cache
- Application data

---

## ⚙️ Configuration

### Requirements File

```txt
colorama>=0.4.6
requests>=2.31.0
pywin32>=306
```

### System Requirements

- **OS:** Windows 10/11 (64-bit)
- **RAM:** 4 GB minimum
- **Storage:** 500 MB free space
- **Privileges:** Administrator rights required

---

## 🛡️ Safety & Reversal

### Before Spoofing

Always:
1. Create a system restore point
2. Backup your hardware IDs
3. Run preflight checks
4. Understand what will be changed

### Reversing Changes

- **MAC Addresses:** Use "Reverse Spoofing" option
- **HWID/EDID:** Use Windows System Restore
- **Traces:** Cannot be recovered (permanent)

---

## ⚠️ Known Limitations

### Hardware Restrictions

- **ASUS Motherboards:** May block HWID changes due to BIOS protection
- **WiFi Adapters:** Many don't support MAC address spoofing
- **Laptop BIOSes:** Some have locked configurations

### Operation Limitations

- HWID/EDID changes require system reboot
- Some changes are irreversible without restore point
- Requires administrator privileges for all operations

---

## 🔧 Compilation

To compile into a standalone executable:

```bash
pip install pyinstaller
pyinstaller ByGoneSpoofer.spec
```

The executable will be created in the `dist/` folder.

---

## 📚 Documentation

Complete documentation is available in the `/docs/` folder:

- **README.md** - This file
- **CHANGELOG.md** - Version history
- **COMPILATION_README.txt** - Detailed compilation guide
- **START_HERE.txt** - Quick start guide

---

## 🐛 Troubleshooting

### Common Issues

**"No Admin Rights" Error**
- Solution: Right-click and "Run as administrator"

**HWID Spoofing Fails**
- Check if you have an ASUS motherboard
- Use "Recommended" mode instead

**MAC Spoofing Doesn't Work**
- Likely a WiFi adapter limitation
- Try with Ethernet adapter

**Graphics Glitches**
- Normal after EDID changes
- Reboot system to resolve

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

### How to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🔒 Security & Ethics

### Intended Use

This tool is designed for:
- Educational purposes
- Security research
- Understanding hardware fingerprinting
- Legitimate privacy concerns

### Not Intended For

- Bypassing legitimate security measures
- Violating terms of service
- Malicious activities
- Identity theft

**Use responsibly and legally.**

---

## 📞 Support

- **Issues:** Open an issue in this repository
- **Documentation:** See `/docs/` folder
- **System Info Tool:** Use `bygone_system_info_collector.py` for debug reports

---

## 🎓 Technical Details

### Architecture

```
ByGoneSpoofer.py (Main Application)
├── Spoofing Engine
│   ├── SMBIOS manipulation
│   ├── MAC address spoofing
│   ├── EDID modification
│   └── Trace deletion
├── Safety Layer
│   ├── System restore points
│   ├── Hardware ID backup
│   ├── Preflight checks
│   └── Operation logging
└── Utilities
    ├── Event log deletion
    ├── DNS flush
    ├── Temp cleanup
    └── Roblox reinstall
```

### Dependencies

- **Python 3.8+** - Core language
- **Colorama** - Console colors
- **PyWin32** - Windows API access
- **Requests** - HTTP requests

---

## 📊 Project Status

- **Version:** 4.4
- **Status:** Active Development
- **Platform:** Windows 10/11
- **Language:** Python

---

## ⭐ Acknowledgments

- Windows API documentation
- Python community
- Security research community
- All contributors

---

## 📜 Version History

See [CHANGELOG.md](docs/CHANGELOG.md) for detailed version history.

**Current Version: 4.4**
- Enhanced safety features
- System restore point integration
- Improved trace deletion
- Hardware backup system
- Preflight validation

---

<div align="center">

**Made for educational and research purposes**

**Use responsibly • Follow applicable laws • Respect terms of service**

[Report Bug](../../issues) • [Request Feature](../../issues) • [View Documentation](docs/)

</div>

