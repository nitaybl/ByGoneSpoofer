# Troubleshooting

Common problems and how to fix them. If your issue isn't here, join the
[Discord](https://discord.gg/3aZX4TukBC) or open a
[GitHub issue](https://github.com/nitaybl/ByGoneSpoofer/issues).

## Adapter not detected

**Symptom:** *"No suitable network adapters found"* or your adapter isn't listed.

**Fix:** As of **v4.6**, adapter detection tries three methods automatically:

1. `wmic` (Windows 10 / older builds)
2. **PowerShell CIM** — for modern Windows 11 builds where `wmic` was removed
3. **Direct registry walk** — a fully offline last resort

So most "adapter not found on this PC" cases are now handled out of the box. If it still
happens:

* Make sure you're running **as administrator**.
* Confirm the adapter is **enabled** in *Control Panel → Network Connections*.
* If you disabled PowerShell or WMI, re-enable at least one of them.

## No internet after spoofing (connectivity check timed out)

**Symptom:** after the MAC spoof you see *"Connectivity check TIMED OUT... google.com is
unreachable."*

**Fix:** The tool detects this for you and asks:

```text
    [?] Restore original MAC address(es) for the spoofed adapter(s)? (y/n):
```

* Press **`y`** to restore your original MAC and get back online.
* If you already pressed `n`, run **Spoofing → Reverse** to restore the MAC, or simply
  **reboot** — the adapter usually renegotiates.
* Some **Wi-Fi adapters** reject spoofed MACs entirely (see below) — use Ethernet or
  restore.

## Wi-Fi adapter won't change its MAC

**Symptom:** *"Failed to set MAC address"* on a wireless adapter.

**Why:** Many Wi-Fi/wireless chipsets and drivers simply **don't support** MAC address
overrides. This is a hardware/driver limitation, **not a bug** in the tool.

**Fix:** Spoof a wired **Ethernet** adapter instead, or accept that this particular
adapter can't be changed.

## HWID change blocked (ASUS and some OEM boards)

**Symptom:** SMBIOS/HWID spoof appears to run but values don't change.

**Why:** Some motherboards — **ASUS** in particular — lock SMBIOS writes at the firmware
level.

**Fix:** There's no software workaround for a firmware lock. Rely on the **Recommended**
mode (traces + MAC) on these boards.

## Executor says "HWID mismatch" / asks for a reset

**Symptom:** After a **Full/hard spoof**, your script executor thinks you're on a new/
extra device.

**Why:** This is expected. A hard spoof changes the HWID the executor keys on. See the
[Hard Spoof Warning](warnings/hard-spoof.md).

**Fix:** Do an **HWID reset** in that executor. You'll need to repeat this **after every
hard spoof** — which is why we recommend the [Recommended](usage/spoofing-modes.md) mode
first.

## Windows shows "Not activated" after a Full spoof

**Fix:** Usually automatic if your license is linked to a Microsoft account. Full steps:
[Activating Windows](guides/windows-activation.md).

## SmartScreen / antivirus flags the EXE

**Why:** HWID tools trip heuristic detection because of their low-level registry and
driver operations.

**Fix:** Only download from the official
[Releases page](https://github.com/nitaybl/ByGoneSpoofer/releases), and add an exclusion
if you trust it. Prefer running from **Python source** if you'd rather not use the EXE.

## "Administrator privileges required"

**Fix:** Close the tool and relaunch **as administrator** (right-click → *Run as
administrator*). Every spoof operation needs elevation.

## Where are the logs?

Operation logs are written to `%TEMP%\bygone_operations.log`. View recent entries via
**Utilities → View Operation Logs**. Include them when asking for help.
