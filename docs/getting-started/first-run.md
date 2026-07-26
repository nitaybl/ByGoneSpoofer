# First Run

Here's exactly what to expect the first time you launch ByGone Spoofer.

## 1. Elevation (UAC prompt)

Every operation needs administrator rights. If you didn't start it elevated, the tool
relaunches itself and Windows shows a **User Account Control** prompt. Click **Yes**.

## 2. The banner + main menu

Once elevated, you'll see the banner and the main menu:

```text
 ╭──────────────────────────────────────────────────────────────────────╮
 │            Nitaybl's ByGone Spoofer (join discord.gg/3aZX4TukBC)       │
 │              Version: v4.6 (Connectivity Check + Wider Adapters)       │
 ╰──────────────────────────────────────────────────────────────────────╯

    ─────────────────────────────  Main Menu  ─────────────────────────────

        1. Spoofing
        2. Fixer
        3. Utilities
        0. Exit

    [?] Select an option:
```

| Option | What's inside |
| --- | --- |
| **1. Spoofing** | The four spoof modes (Recommended / Full / Light / Reverse) |
| **2. Fixer** | Repair tools (e.g. nuke WebView2) |
| **3. Utilities** | Restore point, backups, logs, preflight checks, temp/DNS cleanup |
| **0. Exit** | Close the tool |

## 3. Make a backup FIRST (highly recommended)

Before your very first spoof, open **3. Utilities → Backup Hardware IDs**. This writes
your original hardware identifiers to a JSON file so you can always roll back.

```text
    ─────────────────────────────  Utilities  ─────────────────────────────

        1. Create System Restore Point
        2. Backup Hardware IDs        <-- do this first
        3. Restore From Backup
        4. View Operation Logs
        5. Run Preflight Checks
        6. Clear Temp Files
        7. Flush DNS Cache
        0. Back

    [?] Select an option: 2
```

{% hint style="success" %}
✅ A backup + a system restore point means almost any change the tool makes is
reversible. Two minutes now saves a lot of stress later.
{% endhint %}

## 4. Before you spoof — the checklist

* [ ] Running **as administrator**
* [ ] **VPN is ON** (Warp by Cloudflare recommended) — [why?](../guides/vpn.md)
* [ ] **Backup created** (Utilities → Backup Hardware IDs)
* [ ] You've read the [Hard Spoof Warning](../warnings/hard-spoof.md)
* [ ] You know [which mode to pick](../usage/spoofing-modes.md)

## ➡️ Next

Pick your mode → [Spoofing Modes](../usage/spoofing-modes.md), or follow the
[Full Walkthrough](../usage/walkthrough.md).
