# Activating Windows

A **Full (hard) spoof** rewrites low-level hardware identifiers (SMBIOS UUID, serials).
Because Windows ties its **digital license** to your hardware, a hard spoof can
occasionally make Windows report itself as **not activated** afterwards.

{% hint style="info" %}
ℹ️ This mostly affects the **Full Spoof**. The **Recommended** and **Light** modes don't
touch SMBIOS/HWID, so they very rarely affect activation.
{% endhint %}

## 🔑 The easy fix: link a Microsoft account

If your Windows digital license is **linked to a Microsoft account**, Windows will
usually **reactivate itself automatically** after a spoof — the license is tied to your
account, so it reassociates with the "new" hardware on its own.

> ✅ **This means that with a Microsoft account, you generally do NOT need to manually
> reactivate Windows after every full spoof.** It just handles it.

### How to link your account (do this once, before spoofing)

1. Open **Settings → Accounts → Your info**.
2. If it says *"Sign in with a Microsoft account instead"*, click it and sign in.
3. Open **Settings → System → Activation** and confirm it shows
   *"Windows is activated with a digital license linked to your Microsoft account."*

Once you see that message, you're set — future spoofs should reactivate automatically.

## 🛠️ If Windows still shows "Not activated"

If activation doesn't come back on its own:

1. **Reboot** — activation often refreshes after a restart.
2. Go to **Settings → System → Activation → Troubleshoot** and run the
   **Activation troubleshooter**. If your license is linked to your Microsoft account,
   choose *"I changed hardware on this device recently"* and reactivate.
3. As a last resort, from an **elevated** command prompt:

   ```bat
   slmgr /ato
   ```

   This forces an online activation attempt against your existing license.

{% hint style="warning" %}
⚠️ Only reactivate a license you legitimately own. This guide is about restoring your
**own** existing Windows activation after a hardware spoof — not about bypassing
licensing.
{% endhint %}

## ➡️ Next

* [Hard Spoof Warning](../warnings/hard-spoof.md)
* [Troubleshooting](../troubleshooting.md)
