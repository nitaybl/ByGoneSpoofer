> **Note:** The detailed information in this README, while accurate to the script's functionality, was largely structured and written with the assistance of Google's Gemini, as the primary developer (@nitaybl) focused on coding.

---

# ByGone Spoofer by @nitaybl 🛡️

**ByGone Spoofer** is an automated Python utility crafted to assist users in addressing Roblox ban-related issues, particularly those associated with the Byfron anti-cheat system. It aims to provide a comprehensive solution by performing a thorough system cleanup, modifying key system identifiers, and reinstalling a fresh version of Roblox.

This tool is designed for users who understand the implications of modifying system identifiers and are looking for an automated way to manage potential hardware or account flags. **It is licensed strictly for personal, non-commercial, and educational use (see `LICENSE.md` for full terms).**

*Disclaimer: This tool is provided **strictly for personal, non-commercial, and educational purposes only.** Users are solely responsible for their actions. Modifying system identifiers and attempting to circumvent bans may violate Roblox's Terms of Service. Please use this tool responsibly and at your own risk. Refer to the `LICENSE.md` file for full terms of use.*

---

## 🌟 Key Features & Functionality

ByGone Spoofer automates a sequence of operations to refresh your Roblox environment:

1.  **Administrator Privileges:**
    * Automatically checks if the script is running with administrator privileges.
    * If not, it attempts to re-launch itself with elevated rights, as these are necessary for most of its core functions.

2.  **Roblox Process Termination:**
    * Ensures a clean slate by force-closing all known running Roblox processes (e.g., `RobloxPlayerBeta.exe`, `RobloxPlayerLauncher.exe`, `RobloxStudio.exe`) before any cleaning or modification tasks begin.

3.  **Comprehensive Roblox Data Cleansing:**
    * **Cookie Deletion:** Targets and removes Roblox cookies and related browser data from common storage locations within `LOCALAPPDATA` and `APPDATA`, including specific Roblox package paths, to clear session and tracking information.
    * **Trace File Removal (Implied):** While not explicitly listing every file, the uninstallation and cookie deletion aim to remove common trace files left by the client.

4.  **Thorough Roblox Uninstallation:**
    * **Official Uninstaller:** Attempts to silently execute the official Roblox uninstaller found in the system registry.
    * **Manual File Removal:** As a fallback or supplementary step, it performs a manual deletion of common Roblox installation directories (`%LOCALAPPDATA%\Roblox`, Program Files paths) to ensure a more complete removal.

5.  **Automated MAC Address Spoofing:**
    * **Adapter Detection:** Identifies all enabled network interface controllers (NICs) on your system using `netsh` and `wmic`.
    * **Random MAC Generation:** For each detected adapter, it generates a new, valid, and randomized MAC address. The generation logic ensures the second character of the first octet is one of `A`, `E`, `2`, or `6` for better compatibility, especially with wireless adapters.
    * **Registry Modification:** Applies the new MAC address by modifying the `NetworkAddress` value in the Windows Registry for the specific adapter (`HKLM\SYSTEM\CurrentControlSet\Control\Class\{4d36e972-e325-11ce-bfc1-08002be10318}\XXXX`).
    * **Adapter Reset:** Disables and then re-enables each modified network adapter via `netsh` commands to ensure the new MAC address takes effect.

6.  **Roblox Client Reinstallation:**
    * **Secure Download:** Downloads the latest Roblox client installer from official Roblox URLs. It first attempts to use `curl` (if available) and falls back to Python's `requests` library for robustness.
    * **Silent Installation:** Executes the downloaded installer with silent flags (`/S`) for an automated, non-interactive setup of a fresh Roblox client.

7.  **User-Friendly Console Interface:**
    * **Clear Visuals:** Displays a distinctive ASCII art banner upon launch.
    * **Status Updates:** Provides real-time, color-coded (via Colorama) status messages for each major operation.
    * **Progress Indicators:** Shows progress bars for time-consuming tasks like file deletion and installation waits, enhancing user experience.
    * **Internet Check:** Verifies internet connectivity before attempting to download the Roblox installer.

---

## ⚙️ How It Works (Operational Flow)

ByGone Spoofer follows a systematic process:

1.  **Initialization:** Checks for admin rights and internet connectivity.
2.  **Cleanup Phase 1:** Kills active Roblox processes.
3.  **Cleanup Phase 2:** Deletes Roblox cookies and associated local data.
4.  **Uninstallation:** Removes the existing Roblox client.
5.  **Spoofing Phase:** Changes the MAC addresses of all enabled network adapters.
6.  **Reinstallation:** Downloads and installs a fresh Roblox client.
7.  **Completion:** Reports that all operations are completed.

---

## 🚀 How to Use (Using the `.exe` Executable)

If you have downloaded the pre-compiled `ByGoneSpoofer.exe`:

1.  **Download:** Obtain the `ByGoneSpoofer.exe` file.
2.  **Run the Executable:** Simply double-click `ByGoneSpoofer.exe` to run it.
3.  **Administrator Prompt:** The application requires administrator privileges. If you are not already running it as an administrator, a UAC (User Account Control) prompt should appear. Please click "Yes" to grant these permissions.
4.  **Automated Process:** The script will then proceed through all the steps automatically. Monitor the console output for progress.
5.  **Encountering Problems?** If you face any issues or errors, please **open an issue ticket** on this GitHub repository.
6.  **Completion:** Once finished, it will display an "All operations completed!" message. A system restart might be beneficial for all changes to fully propagate.

**General Requirements (for `.exe` users):**
* **Operating System:** Windows.
* **Permissions:** Administrator privileges are mandatory.
* **Internet Connection:** Required for downloading the Roblox installer.

---

## 🐍 Using the Python Source Code (Advanced Users)

If you prefer to run the script directly from its Python source code (`.py` file):

### Requirements for Python Source:
* **Python:** Python 3.x (Python 3.7+ recommended).
* **pip:** Python package installer (usually comes with Python).
* **Python Modules:**
    * `requests`
    * `colorama`
* **Operating System:** Windows (due to reliance on `wmic`, `netsh`, `reg`, and Windows-specific paths/APIs).
* **Permissions:** Administrator privileges are mandatory.
* **Internet Connection:** Required for downloading the Roblox installer.

### Installation of Dependencies:
Open your command prompt or PowerShell and install the required Python modules:
```bash
pip install requests colorama
````

### How to Run the `.py` Script:

1.  **Download:** Obtain the `ByGoneSpoofer.py` script.
2.  **Open Terminal:** Navigate to the directory where you saved the script using Command Prompt or PowerShell.
3.  **Run as Administrator:** You **must** run the script from a terminal that has administrator privileges.
      * Right-click on Command Prompt/PowerShell and select "Run as administrator". Then navigate to the script directory.
4.  **Execute the Script:**
    ```bash
    python ByGoneSpoofer.py
    ```
5.  **Automated Process:** The script will then proceed through all the steps. Monitor the console output.
6.  **Encountering Problems?** If you face any issues or errors, please **open an issue ticket** on this GitHub repository.
7.  **Completion:** Once finished, it will display an "All operations completed\!" message.

-----

## ⚖️ DMCA & Takedown Notices (Roblox Corporation)

ByGone Spoofer is an independently developed tool. It operates on user's local machines to modify system identifiers and manage software installations, primarily for personal, non-commercial, and educational exploration.

If Roblox Corporation or its designated legal representatives believe that this tool, or any part of its code or functionality, directly infringes upon Roblox's copyrighted materials or intellectual property in a manner that warrants a DMCA takedown notice, please direct all such formal communications to:

📧 **`dmca@nitaybl.xyz`**

We are committed to addressing legitimate concerns promptly and professionally. Please ensure your notice substantially complies with the requirements of the Digital Millennium Copyright Act.

-----

## ⚠️ Important Considerations

  * **Educational & Personal Use Only:** This software is licensed strictly for personal, non-commercial, and educational purposes. Please refer to `LICENSE.md` for detailed terms.
  * **Effectiveness Not Guaranteed:** While this tool automates common steps believed to help with ban evasion, its success can vary greatly depending on Roblox's detection methods and individual circumstances.
  * **Roblox Terms of Service:** Using tools to circumvent bans or manipulate game software typically violates Roblox's Terms of Service and can lead to further account actions.
  * **System Changes:** This script makes changes to your system's network configuration (MAC addresses) and software installations. Understand these changes before running the script.
  * **Network Interruption:** MAC address changes require temporarily disabling and re-enabling network adapters, which will briefly disconnect your internet.
  * **Consider Using a VPN (Optional but Recommended):** After running ByGone Spoofer, for an additional layer of privacy and to change your IP address (another potential tracking point), consider using a reputable VPN service. Services like Cloudflare WARP can be an option.

-----

## 📞 Contact, Feedback & Issue Reporting

  * **For Bugs & Technical Problems:** If you encounter any issues, errors, or bugs while using ByGone Spoofer, please **create a new issue ticket on this GitHub repository.** This is the preferred method for tracking and resolving problems. *Individual support for troubleshooting via direct messages (e.g., Discord) is not provided for technical issues.*
  * **General Feedback & Questions:** For general feedback, suggestions, or non-critical questions, you can find **nitaybl** on Discord: `nitaybl`
  * **DMCA/Legal:** For DMCA or other legal inquiries, please use `dmca@nitaybl.xyz` as noted above.

**Developed by nitaybl.**
