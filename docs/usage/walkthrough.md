# Full Walkthrough

This is a start-to-finish walk through a spoof, including the **new connectivity check**
that runs after your MAC is changed.

{% hint style="info" %}
This walkthrough uses the **Recommended** mode as the example because it's the one you
should run first. The Full and Light flows follow the same shape.
{% endhint %}

## Step 0 — Prep

1. Turn your **VPN on** (Warp by Cloudflare — [why?](../guides/vpn.md)).
2. Launch **as administrator**.
3. Utilities → **Backup Hardware IDs** (first time only).

## Step 1 — Pick the mode

`Main Menu → 1. Spoofing → 1. Recommended`

The tool runs **preflight checks** (admin rights, internet, disk space, WMI service) and
asks you to confirm:

```text
    [+] Preflight checks passed.
    [?] Do you understand and wish to proceed? (y/n): y
```

## Step 2 — Safety backups

It creates a **system restore point** and backs up your hardware IDs automatically.

```text
    [!] Creating safety backups before making changes...
    [+] System restore point created.
    [+] Hardware IDs backed up.
```

## Step 3 — Trace cleanup + Roblox reset

Event logs, temp files, and the DNS cache are cleared, then Roblox is uninstalled and
its cookies/registry keys removed.

## Step 4 — MAC spoof + connectivity check ⭐ *new in v4.6*

The tool lists your network adapters (detected across a
[wider range of methods](../troubleshooting.md#adapter-not-detected) now) and spoofs the
one you choose:

```text
    ───────────────────────────  MAC Address Spoofer  ──────────────────────

    [+] Available Network Adapters:
            1. Ethernet
            2. Wi-Fi

    [?] Select adapter to spoof (e.g., 1, or type 'all', 'skip'): 1
    [>] Spoofing Ethernet with MAC: 02:1A:3B:4C:5D:6E
    [+] Disabling network adapter: Ethernet...
    [>] Setting MAC 021A3B4C5D6E for Ethernet...
    [+] Enabling network adapter: Ethernet...
    [+] MAC address successfully set for Ethernet.
    [✓] 1 MAC address(es) spoofed.
```

Then the **connectivity check** runs automatically:

```text
    ─────────────────────────────  Connectivity Check  ─────────────────────

    [+] Waiting 10s for network adapters to stabilize before pinging google.com...
    [✓] Connectivity confirmed (google.com reachable).
```

### If the internet doesn't come back

If `google.com` doesn't respond, it **rechecks every 10 seconds for up to 40 seconds**
before timing out:

```text
    [!] No response from google.com. Retrying every 10s for up to 40s...
        [+] Rechecking connectivity... (10s / 40s)
        [+] Rechecking connectivity... (20s / 40s)
        [+] Rechecking connectivity... (30s / 40s)
        [+] Rechecking connectivity... (40s / 40s)
    [!] Connectivity check TIMED OUT after 40s. google.com is unreachable.
        [!] The new MAC address may be blocking your internet connection.
    [?] Restore original MAC address(es) for the spoofed adapter(s)? (y/n):
```

* Type **`y`** → the tool restores your original MAC and rechecks connectivity.
* Type **`n`** → the spoofed MAC stays; your internet may remain down until you revert
  (via **Reverse Spoof**) or reboot.

{% hint style="success" %}
✅ This safety net means a bad MAC can no longer silently leave you offline — you'll
always be told, and offered a one-key rollback.
{% endhint %}

## Step 5 — Finish

Remaining steps run (EDID/HWID depending on mode), then Roblox is reinstalled — you can
choose **Standard Roblox**, **FishStrap**, or **BloxStrap**.

```text
    ─────────────────────────  All Operations Completed  ───────────────────
    [✓] Done. Reboot if you changed EDID/HWID.
```

## ➡️ Next

* Something went wrong? → [Troubleshooting](../troubleshooting.md)
* Read the risks of Full mode → [Hard Spoof Warning](../warnings/hard-spoof.md)
