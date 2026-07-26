# ByGone Spoofer

<div align="center">

Hardware identifier spoofing tool for Windows — built **specifically for Roblox**.

[![Stars](https://img.shields.io/github/stars/nitaybl/ByGoneSpoofer?style=for-the-badge&logo=github&color=00b4d8)](https://github.com/nitaybl/ByGoneSpoofer/stargazers)
[![Downloads](https://img.shields.io/github/downloads/nitaybl/ByGoneSpoofer/total?style=for-the-badge&logo=github&color=52b788)](https://github.com/nitaybl/ByGoneSpoofer/releases)
[![Release](https://img.shields.io/github/v/release/nitaybl/ByGoneSpoofer?style=for-the-badge&color=9d4edd)](https://github.com/nitaybl/ByGoneSpoofer/releases/latest)
[![License](https://img.shields.io/badge/License-MIT-f77f00?style=for-the-badge)](LICENSE)
[![Discord](https://img.shields.io/badge/Discord-Join%20Us-5865F2?style=for-the-badge&logo=discord&logoColor=white)](https://discord.gg/3aZX4TukBC)

<br>

[![Read the Docs](https://img.shields.io/badge/📖_Read_the_Full_Docs-GitBook-3884FF?style=for-the-badge&logo=gitbook&logoColor=white)](https://bygonespoofer.gitbook.io/bygonespoofer-docs)

</div>

> 🎯 **This tool is made SPECIFICALLY for Roblox** — not Fortnite, not Valorant, not any
> other game. If it happens to work elsewhere, that's a coincidence; it was never made
> for that, and non-Roblox use isn't supported.

## 📚 Documentation

**All guides live in the GitBook docs** — installation, a full spoof walkthrough,
spoofing modes, VPN setup, Windows activation, troubleshooting, and warnings:

### 👉 [Read the documentation on GitBook](https://bygonespoofer.gitbook.io/bygonespoofer-docs)

## 👀 What it looks like

```text
 ╭──────────────────────────────────────────────────────────────────────╮
 │            Nitaybl's ByGone Spoofer (join discord.gg/3aZX4TukBC)       │
 │              Version: v4.7 (HWID Fixes + Roblox Path Detection)        │
 ╰──────────────────────────────────────────────────────────────────────╯

    ─────────────────────────────  Main Menu  ─────────────────────────────

        1. Spoofing
        2. Fixer
        3. Utilities
        0. Exit

    [?] Select an option:
```

## ⚠️ Disclaimer

**For educational and research purposes only.** Use at your own risk.

## Features

- **HWID Spoofing** - Modify system UUID, motherboard serial
- **MAC Address Spoofing** - Change network adapter identifiers, with a post-spoof
  connectivity check (pings google.com and offers to restore your MAC if you go offline)
- **Wider Adapter Support** - Detects adapters via WMIC, PowerShell, or the registry
- **EDID Spoofing** - Modify monitor serials
- **Trace Removal** - Clean registry, event logs, temp files
- **Backup & Restore** - Save and restore original hardware IDs
- **FishStrap / BloxStrap Support** - Choose your preferred Roblox bootstrapper on reinstall

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
scripts\compile_bygone_spoofer.bat
```

The EXE will be in the `dist/` folder.

## Spoofing Modes

| Mode | Use Case | Changes |
|------|----------|---------|
| **Full Spoof** | Hard HWID ban | HWID + MAC + EDID + Traces |
| **Light Spoof** | Soft ban | MAC + EDID + Traces |
| **Recommended** | Continue cheating | Traces + MAC (no HWID) |
| **Reverse** | Undo changes | Restore from backup |

## Roblox Install Options

When reinstalling Roblox, you can choose:
- **Standard Roblox** — Official installer from roblox.com
- **FishStrap** — Custom bootstrapper with extra features (via fishstrap.app)
- **BloxStrap** — Custom bootstrapper auto-downloaded from GitHub

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
├── ico.ico                   # Application icon
└── scripts/                  # Compilation scripts
    ├── compile_bygone_spoofer.bat
    └── ByGoneSpoofer.spec
```

## Contributors

| Contributor | Contributions |
|-------------|---------------|
| [@nitaybl](https://github.com/nitaybl) | Creator & maintainer |
| [@echohumm](https://github.com/echohumm) | Compilation script bug reports & fixes (line endings, path resolution, PyInstaller PATH, echo escaping) |

## Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT License - see [LICENSE](LICENSE) file for details. Usage terms and disclaimer:
see [DISCLAIMER.md](DISCLAIMER.md).

## Support

- **Discord:** [discord.gg/3aZX4TukBC](https://discord.gg/3aZX4TukBC)
- **Issues:** Open an issue in this repository
- **Documentation:** [bygonespoofer.gitbook.io](https://bygonespoofer.gitbook.io/bygonespoofer-docs)

---

**Use responsibly and legally.**
