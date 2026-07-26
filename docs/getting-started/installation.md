# Installation

This page gets ByGone Spoofer onto your machine. There are two ways to run it: the
**pre-built EXE** (easiest) or **from Python source** (for developers).

{% hint style="danger" %}
🎯 Reminder: this tool is for **Roblox only**. It is not built or supported for any
other game.
{% endhint %}

## ✅ Requirements

| Requirement | Details |
| --- | --- |
| **OS** | Windows 10 or Windows 11 (64-bit) |
| **Privileges** | **Administrator** — required for every operation |
| **Python** (source only) | Python 3.8 or newer |
| **Internet** | Needed to download tools and reinstall Roblox |
| **VPN** | Strongly recommended — see [Use a VPN](../guides/vpn.md) |

## 🅰️ Option A — Pre-built EXE (recommended for most users)

1. Go to the [Releases page](https://github.com/nitaybl/ByGoneSpoofer/releases/latest).
2. Download the latest `ByGoneSpoofer.exe`.
3. **Right-click → Run as administrator.**

That's it — skip to [First Run](first-run.md).

{% hint style="warning" %}
⚠️ Windows SmartScreen or your antivirus may flag the EXE. This is common for HWID
tools because of the low-level registry and driver operations they perform. Only
download from the official [GitHub Releases](https://github.com/nitaybl/ByGoneSpoofer/releases)
page, and add an exclusion if you trust the source.
{% endhint %}

## 🅱️ Option B — Run from Python source

1. **Install Python 3.8+** from [python.org](https://www.python.org/downloads/) and tick
   *"Add Python to PATH"* during setup.
2. **Download the source** — clone or download the repo:

   ```bash
   git clone https://github.com/nitaybl/ByGoneSpoofer.git
   cd ByGoneSpoofer
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

   This installs `colorama`, `requests`, and `pywin32`.

4. **Run as administrator.** Open an **elevated** terminal (right-click Command Prompt →
   *Run as administrator*), then:

   ```bash
   python ByGoneSpoofer.py
   ```

{% hint style="info" %}
If you launch it without admin rights, the tool automatically tries to relaunch itself
through a UAC prompt. Click **Yes** when Windows asks.
{% endhint %}

## 🛠️ Option C — Build your own EXE

If you want to compile the source into a standalone EXE:

```bash
scripts\compile_bygone_spoofer.bat
```

The finished executable lands in the `dist/` folder.

## ➡️ Next

Head to [First Run](first-run.md) to see what happens the first time you launch it.
