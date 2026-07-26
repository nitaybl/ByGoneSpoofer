# Spoofing Modes

Under **1. Spoofing** you'll find four modes. Pick based on the kind of ban you're
dealing with.

```text
    ─────────────────────────────  Spoofing  ──────────────────────────────

        1. Recommended   (traces + MAC, no HWID)   <-- start here
        2. Full Spoof    (HWID + MAC + EDID + traces)
        3. Light Spoof   (MAC + EDID + traces)
        4. Reverse       (undo changes / restore backup)
        0. Back

    [?] Select an option:
```

## 🟢 1. Recommended — *start here*

**Changes:** Trace cleanup + MAC address. **No HWID/SMBIOS changes.**

The safest option and the one you should try **first**. It clears local traces and
randomizes your MAC without touching low-level hardware identifiers, so there's no risk
of destabilizing your PC and no HWID reset needed for your executor.

> Use when: you got soft-banned or just want a clean slate to continue playing.

## 🔴 2. Full Spoof — *hard ban only*

**Changes:** HWID (SMBIOS UUID + serials) + MAC + EDID + traces.

The "hard spoof". This rewrites deep hardware identifiers via AMIDEWIN. Use it **only**
if a Recommended spoof didn't lift a genuine hardware ban.

{% hint style="warning" %}
⚠️ A Full/hard spoof can destabilize some systems and **will throw off any script or
executor that uses HWID to detect multiple devices** — you'll need to do an **HWID reset
in that executor after every hard spoof**. Read the full
[Hard Spoof Warning](../warnings/hard-spoof.md) before using this.
{% endhint %}

## 🟡 3. Light Spoof — *soft ban*

**Changes:** MAC + EDID + traces. Skips the SMBIOS/HWID rewrite.

A middle ground: more than Recommended, but without the risky HWID changes.

## ♻️ 4. Reverse — *undo*

Restores your MAC to default and, if you made one, restores your hardware IDs from the
backup file. Use this to roll back any changes.

## 📊 Quick comparison

| Mode | Traces | MAC | EDID | HWID/SMBIOS | Risk | Try when |
| --- | :---: | :---: | :---: | :---: | --- | --- |
| **Recommended** | ✅ | ✅ | ❌ | ❌ | 🟢 Low | First, always |
| **Light** | ✅ | ✅ | ✅ | ❌ | 🟡 Medium | Soft ban persists |
| **Full** | ✅ | ✅ | ✅ | ✅ | 🔴 High | Confirmed hard ban |
| **Reverse** | — | ↩️ | ↩️ | ↩️ | 🟢 Low | Undo everything |

## ➡️ Next

See a mode in action → [Full Walkthrough](../usage/walkthrough.md).
