# ByGone Spoofer

Hardware identifier spoofing tool for Windows.

## ⚠️ Disclaimer

**For educational and research purposes only.** Use at your own risk.

## Features

- **HWID Spoofing** - Modify system UUID, motherboard serial
- **MAC Address Spoofing** - Change network adapter identifiers
- **EDID Spoofing** - Modify monitor serials
- **Trace Removal** - Clean registry, event logs, temp files
- **Backup & Restore** - Save and restore original hardware IDs

## Quick Start

### Installation

```bash
pip install -r requirements.txt
```

### Usage

Run as administrator:

```bash
python ByGoneSpoofer.py
```

### Compilation

To create a standalone executable:

```bash
cd scripts
compile_bygone_spoofer.bat
```

The EXE will be in the `dist/` folder.

## Spoofing Modes

| Mode | Use Case | Changes |
|------|----------|---------|
| **Full Spoof** | Hard HWID ban | HWID + MAC + EDID + Traces |
| **Light Spoof** | Soft ban | MAC + EDID + Traces |
| **Recommended** | Continue cheating | Traces + MAC (no HWID) |
| **Reverse** | Undo changes | Restore from backup |

## Safety

The tool includes:
- System restore point creation before changes
- Hardware ID backup to JSON file
- HWID and EDID registry backup for reversal
- Preflight system checks

**Important:**
- HWID/EDID can be restored from backup (not just restore point)
- MAC addresses always reversible
- Create backup before first use

## Known Limitations

- **ASUS motherboards** may block HWID changes
- **WiFi adapters** often don't support MAC spoofing
- **Administrator rights** required for all operations
- **System reboot** needed after EDID changes

## Requirements

- Windows 10/11 (64-bit)
- Python 3.8+
- Administrator privileges

## Project Structure

```
ByGoneSpoofer/
├── ByGoneSpoofer.py          # Main application
├── requirements.txt           # Dependencies
├── README.md                 # This file
├── LICENSE                   # MIT License
├── CHANGELOG.md             # Version history
└── scripts/                  # Compilation scripts
    ├── compile_bygone_spoofer.bat
    ├── ByGoneSpoofer.spec
    └── bygone_webview2_fixer.py
```

## Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Support

- **Issues:** Open an issue in this repository
- **Documentation:** See code comments in `ByGoneSpoofer.py`

---

**Use responsibly and legally.**
