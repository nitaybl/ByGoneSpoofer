# Copyright (c) 2025 nitaybl. All Rights Reserved.


import os
import sys
import subprocess
import time
import random
import ctypes
import shutil
import winreg
import requests
import re  # Added for parsing WMIC output
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# ASCII Art
BANNER = r"""


 /$$$$$$$             /$$$$$$                                      /$$$$$$$  /$$$$$$$         /$$$$$$                                 /$$$$$$                   
| $$__  $$           /$$__  $$                                    | $$__  $$| $$__  $$       /$$__  $$                               /$$__  $$                  
| $$  \ $$ /$$   /$$| $$  \__/  /$$$$$$  /$$$$$$$   /$$$$$$       | $$  \ $$| $$  \ $$      | $$  \__/  /$$$$$$   /$$$$$$   /$$$$$$ | $$  \__//$$$$$$   /$$$$$$ 
| $$$$$$$ | $$  | $$| $$ /$$$$ /$$__  $$| $$__  $$ /$$__  $$      | $$$$$$$/| $$$$$$$       |  $$$$$$  /$$__  $$ /$$__  $$ /$$__  $$| $$$$   /$$__  $$ /$$__  $$
| $$__  $$| $$  | $$| $$|_  $$| $$  \ $$| $$  \ $$| $$$$$$$$      | $$__  $$| $$__  $$       \____  $$| $$  \ $$| $$  \ $$| $$  \ $$| $$_/  | $$$$$$$$| $$  \__/
| $$  \ $$| $$  | $$| $$  \ $$| $$  | $$| $$  | $$| $$_____/      | $$  \ $$| $$  \ $$       /$$  \ $$| $$  | $$| $$  | $$| $$  | $$| $$    | $$_____/| $$      
| $$$$$$$/|  $$$$$$$|  $$$$$$/|  $$$$$$/| $$  | $$|  $$$$$$$      | $$  | $$| $$$$$$$/      |  $$$$$$/| $$$$$$$/|  $$$$$$/|  $$$$$$/| $$    |  $$$$$$$| $$      
|_______/  \____  $$ \______/  \______/ |__/  |__/ \_______/      |__/  |__/|_______/        \______/ | $$____/  \______/  \______/ |__/     \_______/|__/      
           /$$  | $$                                                                                  | $$                                                      
          |  $$$$$$/                                                                                  | $$                                                      
           \______/                                                                                   |__/                                                      



"""

# --- MAC Spoofing Constants (from the other script) ---
REG_KEY_BASE = r"SYSTEM\CurrentControlSet\Control\Class\{4d36e972-e325-11ce-bfc1-08002be10318}"
HEX_CHARS = "0123456789ABCDEF"
SECOND_CHAR_OPTIONS = "AE26"  # Ensures second char of first octet is one of these for some NICs


def is_admin():
    """Check if the script is running with admin privileges"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def restart_with_admin():
    """Restart the script with admin privileges"""
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    sys.exit(0)


def print_progress_bar(iteration, total, prefix='', suffix='', length=50, fill='=', color=Fore.WHITE):
    """Print a progress bar with the specified color"""
    percent = f"{100 * (iteration / float(total)):.1f}"
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + ' ' * (length - filled_length)
    print(f'\r{prefix} [{color}{bar}{Style.RESET_ALL}] {percent}% {suffix}', end='', flush=True)
    if iteration == total:
        print()


def kill_roblox_processes():
    """Force-close any running Roblox processes"""
    print(f"{Fore.RED}[+] Checking for running Roblox processes...{Style.RESET_ALL}")
    targets = [
        'RobloxPlayerBeta.exe',
        'RobloxPlayerLauncher.exe',
        'RobloxPlayer.exe',
        'RobloxStudio.exe'
    ]
    for proc_name in targets:
        try:
            subprocess.run(
                ['taskkill', '/F', '/IM', proc_name],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, check=False
            )
        except Exception:
            pass
    print(f"{Fore.GREEN}[✓] All Roblox processes terminated (if any were running).{Style.RESET_ALL}")


def delete_roblox_cookies():
    """Delete Roblox cookies folder and show progress"""
    kill_roblox_processes()
    print(f"{Fore.RED}[+] Deleting Roblox cookies...{Style.RESET_ALL}")
    cookie_paths = [
        os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Roblox', 'browsercookie'),
        os.path.join(os.environ.get('APPDATA', ''), 'Roblox', 'cookies'),
        os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Packages', 'ROBLOXCORPORATION.ROBLOX_55nm5eh3cm0pr', 'AC',
                     'Cookies')
    ]
    deleted_count = 0
    for path in cookie_paths:
        if os.path.exists(path):
            try:
                if os.path.isdir(path):
                    shutil.rmtree(path)
                else:
                    os.remove(path)
                deleted_count += 1
            except Exception as e:
                print(f"{Fore.YELLOW}    Warning: Could not delete {path}: {e}{Style.RESET_ALL}")
    total_steps = max(1, len(cookie_paths))  # Avoid division by zero if no paths
    for i in range(total_steps + 1):
        print_progress_bar(i, total_steps, prefix='    Progress:', suffix='Complete', length=30, color=Fore.RED)
        time.sleep(0.1)  # Reduced sleep time
    if deleted_count > 0 or not any(os.path.exists(p) for p in cookie_paths):
        print(f"{Fore.GREEN}[✓] Roblox cookies deleted successfully!{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}[!] No Roblox cookies found or failed to delete.{Style.RESET_ALL}")
    return True


def uninstall_roblox():
    """Uninstall Roblox from the system"""
    print(f"\n{Fore.RED}[+] Uninstalling Roblox...{Style.RESET_ALL}")
    roblox_paths = [
        os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Roblox'),
        os.path.join(os.environ.get('PROGRAMFILES', ''), 'Roblox'),
        os.path.join(os.environ.get('PROGRAMFILES(X86)', ''), 'Roblox')
    ]
    uninstaller_path = None
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall') as key:
            i = 0
            while True:
                try:
                    sub = winreg.EnumKey(key, i)
                    with winreg.OpenKey(key, sub) as sk:
                        name = winreg.QueryValueEx(sk, 'DisplayName')[0]
                        if 'roblox' in name.lower():
                            uninstaller_path = winreg.QueryValueEx(sk, 'UninstallString')[0]
                            break
                except WindowsError:  # Catches when EnumKey goes out of bounds
                    break
                except Exception:  # Other potential errors reading registry
                    pass  # Continue to next subkey
                finally:
                    i += 1
    except Exception:
        pass

    success = False
    if uninstaller_path:
        try:
            # Ensure quotes around path if it contains spaces, /S for silent
            cmd = f'"{uninstaller_path}" /S' if " " in uninstaller_path else f'{uninstaller_path} /S'
            p = subprocess.Popen(cmd, shell=True)
            p.wait(timeout=60)  # Wait for uninstaller with a timeout
            success = True
        except subprocess.TimeoutExpired:
            print(
                f"{Fore.YELLOW}    Roblox uninstaller timed out. May still be running in background.{Style.RESET_ALL}")
            # We can assume it might have worked or try manual deletion
        except Exception as e:
            print(
                f"{Fore.YELLOW}    Error running Roblox uninstaller: {e}. Attempting manual deletion.{Style.RESET_ALL}")

    # Fallback or additional step: manual deletion
    manual_deletion_attempted = False
    for path in roblox_paths:
        if os.path.exists(path):
            manual_deletion_attempted = True
            try:
                shutil.rmtree(path)
                success = True  # Mark success if at least one path is removed
            except Exception as e:
                print(f"{Fore.YELLOW}    Warning: Could not delete {path}: {e}{Style.RESET_ALL}")

    for i in range(11):
        print_progress_bar(i, 10, prefix='    Progress:', suffix='Complete', length=30, color=Fore.RED)
        time.sleep(0.3)  # Reduced sleep time

    if success:
        print(f"{Fore.GREEN}[✓] Roblox uninstalled (or removal attempted).{Style.RESET_ALL}")
    elif manual_deletion_attempted:
        print(
            f"{Fore.YELLOW}[!] Roblox uninstallation faced issues but manual deletion was attempted.{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}[!] Roblox may not have been fully uninstalled or was not found.{Style.RESET_ALL}")
    return True


# --- New MAC Spoofing Functions ---
def _run_shell_command(command, capture_output=True, text=True, check=False, shell=True):
    """Helper to run shell commands, simplified."""
    try:
        return subprocess.run(command, capture_output=capture_output, text=text, check=check, shell=shell,
                              errors='ignore')
    except Exception as e:
        print(f"{Fore.RED}    Shell command error: {e}{Style.RESET_ALL}")
        return None


def get_nic_index_from_name(network_adapter_name):
    """Retrieves the device index (registry folder name) for a given NIC's NetConnectionID."""
    try:
        # Using "NetConnectionID" as it's usually what 'netsh interface show interface' provides as name.
        # WMIC Index is typically the numeric folder name like 0001, 0007.
        command = f'wmic nic where "NetConnectionID=\'{network_adapter_name}\'" get Index /format:value'
        process = _run_shell_command(command)
        if process and process.stdout:
            match = re.search(r"Index=(\d+)", process.stdout)
            if match:
                return match.group(1)  # This is the string like "1", "7", "12"
    except Exception as e:
        print(f"{Fore.RED}    Error getting NIC index for '{network_adapter_name}': {e}{Style.RESET_ALL}")
    return None


def generate_random_mac_value():
    """Generates a random MAC address value (12 hex chars, no colons)."""
    mac_parts = [
        random.choice(HEX_CHARS) + random.choice(SECOND_CHAR_OPTIONS)
    ]
    for _ in range(5):  # Remaining 5 octets
        mac_parts.append(random.choice(HEX_CHARS) + random.choice(HEX_CHARS))
    return "".join(mac_parts)


def format_mac_for_display(mac_value_no_colons):
    """Formats a 12-char MAC string with colons for display."""
    return ":".join(mac_value_no_colons[i:i + 2] for i in range(0, 12, 2))


def change_mac_address():
    """Randomize and apply MAC addresses on all enabled, physical adapters."""
    print(f"\n{Fore.BLUE}[+] Changing MAC addresses for enabled adapters...{Style.RESET_ALL}")
    changed_count = 0
    adapter_names_to_change = []

    try:
        # Get NetConnectionID for enabled adapters (usually physical, non-virtual)
        # `netsh interface show interface` lists interfaces.
        # We are interested in 'Enabled' and 'Connected' or 'Disconnected' (means it's a configurable NIC)
        # and typically want to avoid purely virtual adapters if possible, though this is harder to filter robustly.
        # For now, we take all 'Enabled' ones.
        res = _run_shell_command(['netsh', 'interface', 'show', 'interface'])
        if not (res and res.stdout):
            print(f"{Fore.RED}    Could not list network interfaces via netsh.{Style.RESET_ALL}")
            return False

        lines = res.stdout.splitlines()
        # Skip header lines, look for lines with "Enabled"
        # Example line: "Enabled  Connected   Dedicated  Ethernet" (name is "Ethernet")
        # Or:         "Enabled  Disconnected  Dedicated  Wi-Fi"    (name is "Wi-Fi")
        for line in lines:
            line_stripped = line.strip()
            if line_stripped.lower().startswith("enabled"):
                parts = line_stripped.split()
                if len(parts) >= 4:  # "Enabled", "State", "Type", "Interface Name" (can be multi-word)
                    adapter_name = " ".join(parts[3:])
                    if adapter_name:  # Ensure name is not empty
                        adapter_names_to_change.append(adapter_name)

        if not adapter_names_to_change:
            print(f"{Fore.YELLOW}    No suitable enabled interfaces found to change MAC address.{Style.RESET_ALL}")
            return False

    except Exception as e:
        print(f"{Fore.RED}    Error listing network interfaces: {e}{Style.RESET_ALL}")
        return False

    total_adapters_to_process = len(adapter_names_to_change)
    for idx, nic_name in enumerate(adapter_names_to_change):
        print_progress_bar(idx + 1, total_adapters_to_process, prefix=f'    Processing {nic_name[:20]:<20}:',
                           suffix='Working', length=30, color=Fore.BLUE)
        time.sleep(0.1)  # Small delay for visual feedback

        nic_reg_index_str = get_nic_index_from_name(nic_name)  # Gets string like "1", "7"

        if nic_reg_index_str:
            # The registry key is often zero-padded to 4 digits (e.g., 0001, 0007, 0011)
            full_registry_path = rf"{REG_KEY_BASE}\{nic_reg_index_str.zfill(4)}"
            new_mac_value = generate_random_mac_value()
            new_mac_display = format_mac_for_display(new_mac_value)

            try:
                # 1. Disable adapter
                _run_shell_command(f'netsh interface set interface name="{nic_name}" admin=disable',
                                   capture_output=False)
                time.sleep(1)  # Give time for the adapter to disable

                # 2. Set MAC in registry
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, full_registry_path, 0, winreg.KEY_SET_VALUE)
                winreg.SetValueEx(key, "NetworkAddress", 0, winreg.REG_SZ, new_mac_value)
                winreg.CloseKey(key)
                time.sleep(0.5)

                # 3. Enable adapter
                _run_shell_command(f'netsh interface set interface name="{nic_name}" admin=enable',
                                   capture_output=False)
                time.sleep(2)  # Give time for adapter to enable and MAC to apply

                print(
                    f"\r    {Fore.CYAN}{nic_name:<30}{Style.RESET_ALL} → {Fore.GREEN}{new_mac_display}{Style.RESET_ALL}  (Index: {nic_reg_index_str.zfill(4)})")
                changed_count += 1
            except FileNotFoundError:  # Specific to winreg.OpenKey if path is wrong
                print(
                    f"\r    {Fore.YELLOW}Registry key not found for {nic_name} (Index: {nic_reg_index_str.zfill(4)}). Path: {full_registry_path}. Skipping.{Style.RESET_ALL}")
            except Exception as e:
                print(f"\r    {Fore.RED}Error changing MAC for {nic_name}: {e}{Style.RESET_ALL}")
                # Attempt to re-enable adapter if an error occurred after disabling
                _run_shell_command(f'netsh interface set interface name="{nic_name}" admin=enable',
                                   capture_output=False)
        else:
            print(
                f"\r    {Fore.YELLOW}Could not find registry index for adapter: {nic_name}. Skipping MAC change.{Style.RESET_ALL}")
        # Clear the progress bar line before printing the next adapter's status or finishing
        print(' ' * 80, end='\r')

    if changed_count > 0:
        print(f"{Fore.GREEN}[✓] {changed_count} MAC address(es) randomized successfully!{Style.RESET_ALL}")
    elif not adapter_names_to_change:  # This case handled earlier, but for safety
        pass
    else:
        print(f"{Fore.YELLOW}[!] No MAC addresses were changed. Check logs above for details.{Style.RESET_ALL}")
    return changed_count > 0


# --- End of New MAC Spoofing Functions ---


def install_roblox():
    """Download and silently install Roblox"""
    print(f"\n{Fore.GREEN}[+] Installing Roblox...{Style.RESET_ALL}")
    roblox_urls = [
        "https://www.roblox.com/download/client",
        "https://www.roblox.com/download/client",
        "https://www.roblox.com/download/client"
    ]
    installer_path = os.path.join(os.environ.get('TEMP', ''), 'RobloxInstaller.exe')

    # Attempt to delete old installer if it exists
    if os.path.exists(installer_path):
        try:
            os.remove(installer_path)
        except Exception:
            pass  # Ignore if deletion fails

    curl_ok = _run_shell_command(['where', 'curl'], shell=True).returncode == 0 if _run_shell_command(['where', 'curl'],
                                                                                                      shell=True) else False
    downloaded = False

    if curl_ok:
        print("    Attempting download with cURL...")
        for url in roblox_urls:
            try:
                # Using -L for redirects, -o for output, --silent for less verbose, --retry for robustness
                _run_shell_command(['curl', '-L', url, '-o', installer_path, '--silent', '--retry', '3'], shell=False,
                                   check=True)
                if os.path.exists(installer_path) and os.path.getsize(
                        installer_path) > 1000000:  # Basic check for valid exe
                    downloaded = True
                    print(f"    Downloaded successfully from: {url}")
                    break
            except subprocess.CalledProcessError:
                print(f"    cURL failed for: {url}")
                continue
            except Exception:  # Catch other potential errors like os.path.getsize if file not found
                continue
    else:
        print("    cURL not found. Trying with requests library...")

    if not downloaded:  # Fallback to requests if cURL failed or not available
        print("    Attempting download with Python requests...")
        for url in roblox_urls:
            try:
                r = requests.get(url, stream=True, timeout=20,
                                 headers={'User-Agent': 'Mozilla/5.0'})  # Added User-Agent
                r.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
                with open(installer_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
                if os.path.exists(installer_path) and os.path.getsize(installer_path) > 1000000:
                    downloaded = True
                    print(f"    Downloaded successfully from: {url}")
                    break
            except requests.exceptions.RequestException as e:
                print(f"    Request failed for {url}: {e}")
                continue
            except Exception as e:  # Other errors
                print(f"    An error occurred downloading from {url}: {e}")
                continue

    if not downloaded:
        print(
            f"{Fore.RED}[!] Could not download Roblox installer after trying multiple sources. Skipping installation.{Style.RESET_ALL}")
        return False

    print(f"    Starting Roblox installation (silent)... Path: {installer_path}")
    try:
        # Use start /B to run installer in background without new window, and allow script to continue
        # Using Popen to not wait for it here, but this means the progress bar is less accurate for install completion.
        # For a true silent install that this script waits for, /S might not be enough,
        # Roblox installer behavior can vary.
        subprocess.Popen([installer_path, '/S'], shell=False)  # shell=False as it's a direct exe path
    except Exception as e:
        print(f"{Fore.RED}    Failed to start Roblox installer: {e}{Style.RESET_ALL}")
        return False

    for i in range(11):  # This progress bar now represents "time allowed for install to run"
        print_progress_bar(i, 10, prefix='    Installing:', suffix='Please wait...', length=30, color=Fore.GREEN)
        time.sleep(2.73)  # Increased time per step

    # Due to background install, we can't be certain it's finished here.
    # We can check for Roblox executable as a basic verification.
    roblox_exe_path = os.path.join(os.environ.get('LOCALAPPDATA', ''), "Roblox", "Versions")
    installed_version_path = ""
    if os.path.exists(roblox_exe_path):
        versions = [d for d in os.listdir(roblox_exe_path) if os.path.isdir(os.path.join(roblox_exe_path, d))]
        if versions:
            # Typically the latest version folder contains RobloxPlayerBeta.exe
            # Find a folder that contains RobloxPlayerBeta.exe
            for version_folder in sorted(versions, reverse=True):  # Check newest first
                if os.path.exists(os.path.join(roblox_exe_path, version_folder, "RobloxPlayerBeta.exe")):
                    installed_version_path = os.path.join(roblox_exe_path, version_folder)
                    break
    if installed_version_path:
        print(
            f"\n{Fore.GREEN}[✓] Roblox installation process initiated. Found version at: {installed_version_path}{Style.RESET_ALL}")
    else:
        print(
            f"\n{Fore.YELLOW}[!] Roblox installation process initiated, but could not verify installation directory immediately. It might still be installing.{Style.RESET_ALL}")
    return True


def main():
    os.system('cls')
    print(f"{Fore.CYAN}{BANNER}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{'=' * 80}{Style.RESET_ALL}")
    print(f"{Fore.WHITE}Nitaybl's ByGone Spoofer{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{'=' * 80}{Style.RESET_ALL}\n")

    if not is_admin():
        print(f"{Fore.RED}[!] Admin privileges required. Attempting to restart as admin...{Style.RESET_ALL}")
        time.sleep(1)
        restart_with_admin()  # Exits after this if it tries to restart
        # If restart_with_admin fails or UAC is denied, script might continue here if not exited.
        # Add a check again or rely on sys.exit(0) in restart_with_admin.
        # For safety, explicitly exit if still not admin after trying to restart.
        if not is_admin():
            print(f"{Fore.RED}[!] Failed to acquire admin privileges. Exiting.{Style.RESET_ALL}")
            input("\nPress Enter to exit...")
            sys.exit(1)

    print(f"{Fore.GREEN}[✓] Running as administrator{Style.RESET_ALL}")
    time.sleep(1)

    try:
        print(f"{Fore.BLUE}[+] Checking internet connection...{Style.RESET_ALL}")
        try:
            requests.get("https://www.google.com", timeout=5)
            print(f"{Fore.GREEN}[✓] Internet connection detected.{Style.RESET_ALL}")
        except requests.exceptions.RequestException:
            print(f"{Fore.RED}[!] No internet connection detected.{Style.RESET_ALL}")
            if input("    Continue anyway? (y/n): ").lower() != 'y':
                sys.exit(0)

        delete_roblox_cookies()
        uninstall_roblox()
        change_mac_address()  # This is the new function
        install_roblox()

        print(f"\n{Fore.GREEN}{'=' * 80}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[✓] All operations completed!{Style.RESET_ALL}")
        print(f"{Fore.GREEN}{'=' * 80}{Style.RESET_ALL}")

    except SystemExit:  # To allow exiting from internet check
        print(f"{Fore.YELLOW}Exiting script as requested.{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}\nAn unexpected error occurred in main execution: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()  # Prints full traceback for debugging

    input("\nPress Enter to exit...")


if __name__ == "__main__":
    main()
# Copyright (c) 2025 nitaybl. All Rights Reserved.