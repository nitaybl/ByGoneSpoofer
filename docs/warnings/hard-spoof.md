# Hard Spoof Warning

{% hint style="warning" %}
⚠️ **READ THIS BEFORE USING FULL / HARD SPOOF.**

A **hard spoof** (the **Full Spoof** mode) rewrites deep, low-level hardware identifiers
(SMBIOS UUID, motherboard/hardware serials). This is powerful, but it comes with real
risks:

* 🧨 **It can mess up your PC.** Deep SMBIOS changes can cause instability, driver
  weirdness, boot quirks, or Windows activation loss on some systems. Not every machine
  reacts the same way.
* 🎮 **It can throw off scripts and executors.** Any script or executor that relies on
  **HWID** to check that you're **not using multiple devices** can get confused by a
  hard spoof. After each hard spoof it will look like a brand-new machine — so you'll
  need to perform an **HWID reset in that executor after every hard spoof**.
* 🔁 **Every hard spoof = another HWID reset.** This isn't a one-time thing. Each time
  you run a Full Spoof, expect to redo the executor's HWID reset.
* 🪪 **Windows may need reactivating** — usually automatic if your license is linked to a
  Microsoft account. See [Activating Windows](../guides/windows-activation.md).

**This is exactly why we recommend running the regular
[Recommended](../usage/spoofing-modes.md) spoof first.** Only escalate to a hard/Full
spoof if the Recommended spoof did not lift your ban.
{% endhint %}

## Do this instead (the safe order)

1. **Recommended spoof first.** Traces + MAC, no HWID. Low risk, no executor HWID reset
   needed. → [Spoofing Modes](../usage/spoofing-modes.md)
2. If that doesn't work, try **Light**.
3. **Only then**, if you're sure it's a genuine hardware ban, use **Full (hard)** — and
   be ready to HWID-reset your executor and re-check Windows activation.

## Before any hard spoof — checklist

* [ ] I tried the **Recommended** spoof first
* [ ] I created a **backup** (Utilities → Backup Hardware IDs)
* [ ] I created a **system restore point**
* [ ] My **VPN is on** ([why?](../guides/vpn.md))
* [ ] I know I'll need to **HWID-reset my executor** afterward
* [ ] I know Windows may need [reactivating](../guides/windows-activation.md)

## If something breaks

Use **Reverse Spoof** to restore from your backup, or roll back with the system restore
point you created. See [Troubleshooting](../troubleshooting.md) for specific fixes.
