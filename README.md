# ByGone Spoofer - Now Updated! (v1.1.1) Enhanced HWID Spoofing & More!

> **Why Did You Create this?:** i was bored and wanted to fool around with gemini and reliaised that changing your mac and resintalling roblox prob isnt enough

> **Is It free?:** YES

> **Is it true that you hate your life?:** Yes.

> **Do You Provide Support:** We Do Provide support in our discord server at https://discord.gg/ysYGTJuKqv
---

# ByGone Spoofer by @nitaybl 🛡️

**ByGone Spoofer** is a spoofer i created to circuvment roblox bans which are handeled by hyperion?, THIS TOOL DOES NOT REMOVE YOUR ACCOUNT BAN AND IM NOT RESPONSIBLE FOR ANYTHING YOU DO WITH IT this is for educational purposes ONLY
This tool is designed for users who understand the implications of modifying system identifiers and are looking for an automated way to manage potential hardware or account flags. **It is licensed strictly for personal, non-commercial, and educational use (see `LICENSE.md` for full terms).**

*Disclaimer: This tool is provided **strictly for personal, non-commercial, and educational purposes only.** Users are solely responsible for their actions. Modifying system identifiers and attempting to circumvent bans may violate Roblox's Terms of Service. Please use this tool responsibly and at your own risk. Refer to the [LICENSE.md](https://github.com/nitayb1/ByGoneSpoofer/blob/main/README.md) file for full terms of use.*

---

## What does it do?

It Does all of the following order to circuvment your ban
1.  Reqests admin privilegies so it can do all of the circumventing for you
2.  Checks if you have an internet connection
3.  Kills roblox so you can actually delete it
4.  Uninstalls roblox for you with automatic installer, does have a fall back to delete manually
5.  Deletes cookies traces and related roblox registry keys (not hyperion)
6.  Spoofs your mac for your ethernet/wifi/vpn adapters.
7.  Spoofs and changes your monitor edid
8.  Removes hyperion identifying registry value from registry
9.  Spoofs your smbios using Amidewin (Only For Supported Motherboards)
10.  Restarts Wmi Service To Make Sure Hwid Changes Propagate
11.  Grabs roblox installer exe and attempts to install it for you (just means it runs automaticlly the installer)
12.  Verifies it installed And Cleans Up the installer exe
---

## 🚀 How to Use (Using the `.exe`)

If you lazy and just want the exe:

1.  **Download:** Go to releases and download the latest exe
2.  **Run the EXE:** Just double-click `ByGoneSpoofer.exe` to run it.
3.  **Administrator Prompt:** The application requires administrator privileges. If you are not already running it as an administrator, a UAC (User Account Control) prompt should appear. Please click "Yes" to grant these permissions.
4.  **Automated Process:** The exe will go through the steps explained above
5.  **Encountering Problems?** If you face any issues or errors, please **open an issue ticket** on this GitHub repository.
6.  **Completion:** Once finished, it will display an "All operations completed!" message. A system restart might be beneficial for all changes to fully propagate.

**General Requirements (for `.exe` users):**
* **Operating System:** Windows 10 (Should Work On 11,8,7).
* **Permissions:** Administrator privileges are mandatory.
* **Internet Connection:** Required for downloading the Roblox installer.

---
ill let gemini explain this section:
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
```

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

📧 **`dmca@bygonsp.xyz`**

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
* **DMCA/Legal:** For DMCA or other legal inquiries, please use `dmca@bygonsp.xyz` as noted above.

**Developed by nitaybl.**
Copyright (c) 2025 nitaybl. All Rights Reserved.
