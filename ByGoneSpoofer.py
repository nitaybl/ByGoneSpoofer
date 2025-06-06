# Copyright (c) 2025 nitaybl. All Rights Reserved.
# i hate my life 😁

import os
import sys
import subprocess
import time
import random
import ctypes
import shutil
import winreg
import requests
import re
from colorama import init, Fore, Style  # Assuming colorama is still desired
import uuid
import string

# Initialize colorama
init(autoreset=True)


# --- ANSI Color Codes (for new MAC spoofer part) ---
class AnsiColor:  # Renamed to avoid conflict if 'Color' is used elsewhere
    YELLOW = '\033[93m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    END = '\033[0m'


# --- Windows API Constants for Transparency ---
GWL_EXSTYLE = -20
WS_EX_LAYERED = 0x00080000
LWA_ALPHA = 0x00000002

# ASCII Art
BANNER = r"""
 /$$$$$$$             /$$$$$$                                      /$$$$$$$  /$$$$$$$         /$$$$$$                                 /$$$$$$
| $$__  $$           /$$__  $$                                    | $$__  $$| $$__  $$       /$$__  $$                               /$$__  $$
| $$  \ $$ /$$   /$$| $$  \__/  /$$$$$$  /$$$$$$$   /$$$$$$       | $$  \ $$| $$  \ $$      | $$  \__/  /$$$$$$   /$$$$$$   /$$$$$$ | $$  \__//$$$$$$   /$$$$$$
| $$$$$$$ | $$  | $$| $$ /$$$$ /$$__  $$| $$__  $$ /$$__  $$      | $$$$$$$/| $$$$$$$       |  $$$$$$  /$$__  $$ /$$__  $$ /$$__  $$| $$$$   /$$__  $$ /$$__  $$
| $$__  $$| $$  | $$| $$|_  $$| $$  \ $$| $$  \ $$| $$$$$$$$      | $$__  $$| $$__  $$       \____  $$| $$  \ $$| $$  \ $$| $$  \ $$| $$_/  | $$$$$$$$| $$  \__/
| $$  \ $$| $$  | $$| $$  \ $$| $$  | $$| $$  | $$| $$_____/      | $$  \ $$| $$  \ $$       /$$  \ $$| $$  | $$| $$  \ $$| $$  \ $$| $$    | $$_____/| $$
| $$$$$$$/|  $$$$$$$|  $$$$$$/|  $$$$$$/| $$  | $$|  $$$$$$$      | $$  | $$| $$$$$$$/      |  $$$$$$/| $$$$$$$/|  $$$$$$/|  $$$$$$/| $$    |  $$$$$$$| $$
|_______/  \____  $$ \______/  \______/ |__/  |__/ \_______/      |__/  |__/|_______/        \______/ | $$____/  \______/  \______/ |__/     \_______/|__/
           /$$  | $$                                                                                  | $$
          |  $$$$$$/                                                                                  | $$
           \______/                                                                                   |__/
"""

# --- pywin32 availability check ---
try:
    import win32security
    import win32api

    PYWIN32_AVAILABLE = True
except ImportError:
    PYWIN32_AVAILABLE = False

# --- Constants for FOCUSED SMBIOS spoofing (AMIDEWIN) ---
AMIDEWIN_DIR_HWID = r"C:\Windows\Fonts"  # Consider a less sensitive directory like %TEMP%\AmideWinTools
AMIDEWIN_TOOLS_MAP = {
    os.path.join(AMIDEWIN_DIR_HWID,
                 "AMIDEWINx64.EXE"): "https://github.com/xxdotdos/amidewinpast/raw/main/AMIDEWINx64.EXE",
    os.path.join(AMIDEWIN_DIR_HWID,
                 "amigendrv64.sys"): "https://github.com/xxdotdos/amidewinpast/raw/main/amigendrv64.sys",
    os.path.join(AMIDEWIN_DIR_HWID,
                 "amifldrv64.sys"): "https://github.com/xxdotdos/amidewinpast/raw/main/amifldrv64.sys",
}
AMIDEWIN_FILES_TO_DELETE = [
    os.path.join(AMIDEWIN_DIR_HWID, "AMIDEWINx64.EXE"),
    os.path.join(AMIDEWIN_DIR_HWID, "amifldrv64.sys"),
    os.path.join(AMIDEWIN_DIR_HWID, "amigendrv64.sys"),
]

# --- MAC Spoofing Constants (from new MAC spoofer) ---
REG_PATH_MAC_SPOOFER = r"HKLM\SYSTEM\CurrentControlSet\Control\Class\{4d36e972-e325-11ce-bfc1-08002be10318}"
HEX_CHARS_MAC_SPOOFER = "0123456789ABCDEF"


# --- Utility Functions ---
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def restart_with_admin():
    try:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    except Exception as e:
        print(f"{Fore.RED}Failed to elevate privileges: {e}{Style.RESET_ALL}")
    sys.exit(0)  # Exit after attempting elevation


def print_progress_bar(iteration, total, prefix='', suffix='', length=50, fill='=', color=Fore.WHITE):
    if total <= 0:
        percent_str = "N/A"
        bar_fill = ' ' * length
    else:
        percent = 100 * (iteration / float(total))
        percent_str = f"{percent:.1f}"
        filled_length = int(length * iteration // total)
        bar_fill = fill * filled_length + ' ' * (length - filled_length)
    print(f'\r{prefix} [{color}{bar_fill}{Style.RESET_ALL}] {percent_str}% {suffix}', end='', flush=True)
    if iteration >= total: print()


def _run_shell_command_simple(command, capture_output_if_no_pipes=True, text=True, check=False, shell=True, stdout=None,
                              stderr=None, timeout=None, cwd=None):  # Added cwd parameter
    actual_command_for_run = command
    display_command_str = ""

    if isinstance(command, list):
        display_command_str = ' '.join(command)
        if shell:
            actual_command_for_run = subprocess.list2cmdline(command)
    elif isinstance(command, str):
        display_command_str = command
    else:
        print(f"{Fore.RED}    Invalid command type: {type(command)}{Style.RESET_ALL}")
        return None

    try:
        if stdout is not None or stderr is not None:
            return subprocess.run(actual_command_for_run, text=text, check=check,
                                  shell=shell, errors='ignore', stdout=stdout, stderr=stderr,
                                  timeout=timeout, cwd=cwd)  # Pass cwd
        elif capture_output_if_no_pipes:
            return subprocess.run(actual_command_for_run, capture_output=True, text=text, check=check,
                                  shell=shell, errors='ignore', timeout=timeout, cwd=cwd)  # Pass cwd
        else:
            return subprocess.run(actual_command_for_run, text=text, check=check,
                                  shell=shell, errors='ignore', stdout=None, stderr=None,
                                  timeout=timeout, cwd=cwd)  # Pass cwd
    except FileNotFoundError:
        print(f"{Fore.RED}    Command not found: {display_command_str}{Style.RESET_ALL}")
        return None
    except subprocess.TimeoutExpired:
        print(f"{Fore.YELLOW}    Command timed out: {display_command_str}{Style.RESET_ALL}")
        return None
    except Exception as e:
        print(f"{Fore.RED}    Shell command error for '{display_command_str}': {e}{Style.RESET_ALL}")
        return None


def _run_shell_command_wrapper(command_list, capture_output=False, text=True, check=False, shell=False, cwd=None,
                               timeout=None, hide_window=False):
    command_str = ' '.join(command_list) if isinstance(command_list, list) else command_list
    startupinfo, creationflags = None, 0
    if hide_window:
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE
        creationflags = subprocess.CREATE_NO_WINDOW
    try:
        console_encoding = sys.stdout.encoding if sys.stdout.encoding else 'utf-8'
        if capture_output:
            return subprocess.run(command_list, capture_output=True, text=text, check=check, shell=shell,
                                  encoding=console_encoding, errors='replace', cwd=cwd, timeout=timeout,
                                  startupinfo=startupinfo, creationflags=creationflags)
        else:
            return subprocess.run(command_list, text=text, check=check, shell=shell,
                                  encoding=console_encoding, errors='replace', cwd=cwd, timeout=timeout,
                                  startupinfo=startupinfo, creationflags=creationflags,
                                  stdout=None, stderr=None)
    except subprocess.TimeoutExpired:
        print(f"{Fore.YELLOW}    Command timed out (wrapper): {command_str}{Style.RESET_ALL}")
        return None
    except Exception as e:
        print(f"{Fore.RED}    Shell command error (wrapper) for '{command_str}': {e}{Style.RESET_ALL}")
        return None


def set_terminal_transparency(alpha_percentage=75):
    if os.name != 'nt': return
    if not (0 <= alpha_percentage <= 100):
        print(f"{Fore.YELLOW}Transparency % must be 0-100.{Style.RESET_ALL}")
        return
    alpha_value = int((alpha_percentage / 100.0) * 255)
    try:
        hwnd = ctypes.windll.kernel32.GetConsoleWindow()
        if not hwnd: return
        current_style = ctypes.windll.user32.GetWindowLongA(hwnd, GWL_EXSTYLE)
        if not (current_style & WS_EX_LAYERED):
            ctypes.windll.user32.SetWindowLongA(hwnd, GWL_EXSTYLE, current_style | WS_EX_LAYERED)
        ctypes.windll.user32.SetLayeredWindowAttributes(hwnd, 0, alpha_value, LWA_ALPHA)
    except Exception:
        pass  # Silently fail if transparency cannot be set


# --- Roblox related functions ---
def kill_roblox_processes():
    print(f"{Fore.RED}[+] Checking for running Roblox processes...{Style.RESET_ALL}")
    targets = ['RobloxPlayerBeta.exe', 'RobloxPlayerLauncher.exe', 'Roblox.exe', 'RobloxStudio.exe',
               'RobloxCrashHandler.exe']
    killed_any = False
    for proc_name in targets:
        result = _run_shell_command_simple(['taskkill', '/F', '/IM', proc_name],
                                           stdout=subprocess.DEVNULL,
                                           stderr=subprocess.DEVNULL,
                                           shell=False, check=False,
                                           capture_output_if_no_pipes=False)
        if result and result.returncode == 0:
            killed_any = True
    if killed_any:
        print(f"{Fore.GREEN}[✓] Roblox processes terminated (if any were running).{Style.RESET_ALL}")
    else:
        print(f"{Fore.GREEN}[✓] No critical Roblox processes found running or terminated.{Style.RESET_ALL}")


def delete_roblox_registry_keys():
    print(f"\n{Fore.RED}[+] Deleting specific Roblox registry keys...{Style.RESET_ALL}")
    keys_to_delete = [
        (winreg.HKEY_CURRENT_USER, r"Software\ROBLOX Corporation"),
    ]
    deleted_count = 0
    for hkey_root, key_path in keys_to_delete:
        hive_name = 'HKCU' if hkey_root == winreg.HKEY_CURRENT_USER else 'HKLM'
        full_key_path_for_cmd = f"{hive_name}\\{key_path}"
        print(f"    Attempting to delete: {full_key_path_for_cmd}")

        cmd = ['reg', 'delete', full_key_path_for_cmd, '/f']
        result = _run_shell_command_simple(cmd, shell=False, capture_output_if_no_pipes=True, text=True)

        key_confirmed_deleted = False
        try:
            key_handle = winreg.OpenKey(hkey_root, key_path)
            winreg.CloseKey(key_handle)
            print(
                f"    {Fore.RED}[!] Failed to delete registry key via 'reg delete': {full_key_path_for_cmd} (still exists).{Style.RESET_ALL}")
            if result and result.stdout and result.stdout.strip(): print(f"        REG STDOUT: {result.stdout.strip()}")
            if result and result.stderr and result.stderr.strip(): print(f"        REG STDERR: {result.stderr.strip()}")
        except FileNotFoundError:
            print(
                f"    {Fore.GREEN}[✓] Registry key {full_key_path_for_cmd} confirmed deleted or was not found.{Style.RESET_ALL}")
            deleted_count += 1
            key_confirmed_deleted = True
        except Exception as e_check:
            print(
                f"    {Fore.YELLOW}[!] Error checking deletion status for {full_key_path_for_cmd}: {e_check}{Style.RESET_ALL}")

        if not key_confirmed_deleted and result:
            if result.returncode != 0:
                print(
                    f"    {Fore.YELLOW}[!] 'reg delete' command failed for {full_key_path_for_cmd}. RC: {result.returncode}{Style.RESET_ALL}")
                if result.stdout and result.stdout.strip(): print(f"        REG STDOUT: {result.stdout.strip()}")
                if result.stderr and result.stderr.strip(): print(f"        REG STDERR: {result.stderr.strip()}")

    if deleted_count == len(keys_to_delete):
        print(
            f"{Fore.GREEN}[✓] Finished attempting to delete {deleted_count} specified Roblox registry key(s).{Style.RESET_ALL}")
    elif deleted_count > 0:
        print(
            f"{Fore.YELLOW}[!] Processed {len(keys_to_delete)} keys, {deleted_count} confirmed deleted.{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}[!] No specified Roblox registry keys were confirmed deleted.{Style.RESET_ALL}")


def delete_roblox_cookies():
    print(f"{Fore.RED}[+] Deleting Roblox cookies & related data...{Style.RESET_ALL}")
    app_data_local = os.environ.get('LOCALAPPDATA', '')
    app_data_roaming = os.environ.get('APPDATA', '')  # For Roaming AppData
    cookie_paths = [
        os.path.join(app_data_local, 'Roblox', 'browsercookie'),
        os.path.join(app_data_roaming, 'Roblox', 'cookies'),  # Roaming path
        os.path.join(app_data_local, 'Packages', 'ROBLOXCORPORATION.ROBLOX_55nm5eh3cm0pr', 'AC', 'Cookies'),  # UWP
        os.path.join(app_data_local, 'Roblox', 'RobloxCookies.dat'),
        os.path.join(app_data_local, 'Roblox', 'RobloxBrowserCache'),
        os.path.join(app_data_local, 'Roblox', 'http'),
        os.path.join(app_data_local, 'Roblox', 'logs'),  # Logs folder
        os.path.join(app_data_local, 'Roblox', 'LocalStorage'),
    ]
    deleted_items_count = 0
    total_steps = len(cookie_paths) if cookie_paths else 1
    for i, path in enumerate(cookie_paths):
        print_progress_bar(i, total_steps, prefix='    Cookie/Data Deletion:',
                           suffix=f'{os.path.basename(path)[:15]:<15}', length=30, color=Fore.RED)
        time.sleep(0.02)
        if os.path.exists(path):
            try:
                if os.path.isdir(path):
                    shutil.rmtree(path, ignore_errors=True)  # ignore_errors will suppress most issues
                else:
                    os.remove(path)

                # Verify deletion
                if not os.path.exists(path):
                    deleted_items_count += 1
            except Exception as e_del_cookie:
                print(f"\n    {Fore.YELLOW}Could not delete {path}: {e_del_cookie}{Style.RESET_ALL}")
                pass
    print_progress_bar(total_steps, total_steps, prefix='    Cookie/Data Deletion:', suffix='Done             ',
                       length=30, color=Fore.RED)
    if deleted_items_count > 0:
        print(
            f"{Fore.GREEN}[✓] Roblox cookie/cache items processed ({deleted_items_count} items/groups confirmed deleted).{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}[!] No specific Roblox cookie/cache items found/deleted.{Style.RESET_ALL}")


def uninstall_roblox():
    print(f"\n{Fore.RED}[+] Uninstalling Roblox...{Style.RESET_ALL}")

    kill_roblox_processes()
    time.sleep(1)

    roblox_local_appdata_path = os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Roblox')
    roblox_program_files_x86_path = os.path.join(os.environ.get('PROGRAMFILES(X86)', ''), 'Roblox')
    roblox_paths_to_delete_manually = [roblox_local_appdata_path, roblox_program_files_x86_path]
    user_program_files = os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Programs', 'Roblox')
    if os.path.exists(user_program_files):
        roblox_paths_to_delete_manually.append(user_program_files)

    uninstaller_path_cmd, uninstaller_exe = None, None
    uninstall_reg_keys = [
        (winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall', winreg.KEY_WOW64_64KEY),
        (winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall', 0),
        (winreg.HKEY_CURRENT_USER, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall', 0)
    ]
    for hkey_root, reg_path_base, access_flags in uninstall_reg_keys:
        if uninstaller_path_cmd and uninstaller_exe and os.path.exists(uninstaller_exe): break
        try:
            with winreg.OpenKey(hkey_root, reg_path_base, 0, winreg.KEY_READ | access_flags) as key:
                i = 0
                while True:
                    try:
                        sub_key_name = winreg.EnumKey(key, i)
                        with winreg.OpenKey(key, sub_key_name, 0, winreg.KEY_READ | access_flags) as sk:
                            try:
                                name = winreg.QueryValueEx(sk, 'DisplayName')[0]
                                if 'roblox player' in name.lower():
                                    temp_uninstaller_path_cmd = winreg.QueryValueEx(sk, 'UninstallString')[0]
                                    temp_uninstaller_exe = temp_uninstaller_path_cmd.split('"')[
                                        1] if temp_uninstaller_path_cmd.startswith('"') else \
                                        temp_uninstaller_path_cmd.split(' ')[0]
                                    if os.path.exists(temp_uninstaller_exe):
                                        uninstaller_path_cmd = temp_uninstaller_path_cmd
                                        uninstaller_exe = temp_uninstaller_exe
                                        break
                            except (FileNotFoundError, Exception):
                                pass
                        i += 1
                    except OSError:
                        break
        except (FileNotFoundError, Exception):
            pass

    success_uninstaller = False
    if uninstaller_exe and uninstaller_path_cmd and os.path.exists(uninstaller_exe):
        print(f"    {Fore.CYAN}Found Roblox uninstaller: {uninstaller_exe}{Style.RESET_ALL}")
        try:
            if uninstaller_path_cmd.startswith('"'):
                path_part = uninstaller_path_cmd.split('"')[1]
                args_part_str = uninstaller_path_cmd[len(path_part) + 2:].strip()
                cmd_list_for_popen = [path_part] + (args_part_str.split() if args_part_str else [])
            else:
                cmd_list_for_popen = uninstaller_path_cmd.split()

            is_roblox_installer = 'RobloxPlayerInstaller.exe' in os.path.basename(uninstaller_exe).lower()
            silent_flags_to_remove = ['/s', '/silent', '/q', '/quiet', '/uninstallquiet']
            cmd_list_for_popen = [flag for flag in cmd_list_for_popen if flag.lower() not in silent_flags_to_remove]

            if is_roblox_installer:
                if not any(f.lower() == '/uninstall' for f in cmd_list_for_popen): cmd_list_for_popen.append(
                    '/uninstall')
                cmd_list_for_popen.append('/quiet')
            else:
                cmd_list_for_popen.append('/S')

            print(f"    {Fore.CYAN}Executing uninstaller: {' '.join(cmd_list_for_popen)}{Style.RESET_ALL}")
            uninstaller_process = _run_shell_command_simple(cmd_list_for_popen, shell=False,
                                                            capture_output_if_no_pipes=True, timeout=120)

            if uninstaller_process and uninstaller_process.returncode == 0:
                print(f"    {Fore.GREEN}Roblox uninstaller process completed successfully.{Style.RESET_ALL}")
                success_uninstaller = True
            elif uninstaller_process:
                print(
                    f"    {Fore.YELLOW}Roblox uninstaller process completed with code: {uninstaller_process.returncode}.{Style.RESET_ALL}")
            else:
                print(f"    {Fore.RED}Roblox uninstaller command execution failed or timed out.{Style.RESET_ALL}")

            print(f"    {Fore.CYAN}Waiting 2 seconds after uninstaller attempt...{Style.RESET_ALL}")
            time.sleep(2)
        except Exception as e:
            print(f"    {Fore.RED}Error running Roblox uninstaller: {e}.{Style.RESET_ALL}")
    else:
        print(
            f"    {Fore.YELLOW}Official Roblox uninstaller not found. Proceeding with manual deletion.{Style.RESET_ALL}")

    print(f"    {Fore.CYAN}Performing manual folder deletions...{Style.RESET_ALL}")
    actual_deleted_count = 0
    for i, path_to_delete in enumerate(roblox_paths_to_delete_manually):
        print_progress_bar(i, len(roblox_paths_to_delete_manually), prefix='    Manual Deletion:',
                           suffix=f'{os.path.basename(path_to_delete)[:15]:<15}', length=30, color=Fore.RED)
        time.sleep(0.1)
        if os.path.exists(path_to_delete):
            try:
                shutil.rmtree(path_to_delete)
                if not os.path.exists(path_to_delete):
                    actual_deleted_count += 1
            except Exception as e_rmtree:
                print(f"\n    {Fore.YELLOW}Warning: Error on {path_to_delete}: {e_rmtree}{Style.RESET_ALL}")
    print_progress_bar(len(roblox_paths_to_delete_manually), len(roblox_paths_to_delete_manually),
                       prefix='    Manual Deletion:', suffix='Done             ', length=30, color=Fore.RED)
    if actual_deleted_count > 0:
        print(f"\n    {Fore.GREEN}Manually deleted {actual_deleted_count} Roblox folder(s).{Style.RESET_ALL}")

    if success_uninstaller or actual_deleted_count > 0:
        print(f"{Fore.GREEN}[✓] Roblox uninstallation/removal attempt finished.{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}[!] Roblox may not have been fully uninstalled/removed.{Style.RESET_ALL}")


# --- NEW MAC Spoofer Functions ---
def get_available_nics_new():
    nics = []
    try:
        cmd = 'wmic nic where "NetConnectionID is not null" get NetConnectionID, Index /format:csv'
        process = _run_shell_command_simple(cmd, capture_output_if_no_pipes=True, text=True, shell=True)
        if process and process.stdout:
            lines = process.stdout.strip().splitlines()
            if len(lines) > 1:
                for line in lines[1:]:
                    parts = line.strip().split(',')
                    if len(parts) >= 3:
                        nic_name = parts[2].strip()
                        nic_index_str = parts[1].strip()
                        if nic_name and nic_index_str.isdigit():
                            if not any(n['name'] == nic_name for n in nics):
                                nics.append({"name": nic_name, "index": nic_index_str})
    except Exception as e:
        print(f"{AnsiColor.RED}[!] Error enumerating NICs: {e}{AnsiColor.END}")
    return nics


def generate_random_mac_enforce_02():
    return "02" + "".join(random.choice(HEX_CHARS_MAC_SPOOFER) for _ in range(10))


def set_mac_address_new(nic_name, nic_index, mac_address_no_colons):
    if not nic_index:
        print(f"{AnsiColor.RED}[!] Cannot set MAC: NIC index missing for {nic_name}.{AnsiColor.END}")
        return False

    registry_key_path = rf"{REG_PATH_MAC_SPOOFER}\{nic_index.zfill(4)}"
    print(f"{AnsiColor.YELLOW}[i] Disabling network adapter: {nic_name}...{AnsiColor.END}")
    _run_shell_command_simple(f'netsh interface set interface name="{nic_name}" admin=disable', shell=True,
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, capture_output_if_no_pipes=False)
    time.sleep(2)

    print(f"{AnsiColor.YELLOW}[i] Setting MAC {mac_address_no_colons} for {nic_name}...{AnsiColor.END}")
    reg_add_command = ["reg", "add", registry_key_path, "/v", "NetworkAddress", "/t", "REG_SZ", "/d",
                       mac_address_no_colons, "/f"]
    result = _run_shell_command_simple(reg_add_command, shell=False, capture_output_if_no_pipes=True)

    print(f"{AnsiColor.YELLOW}[i] Enabling network adapter: {nic_name}...{AnsiColor.END}")
    _run_shell_command_simple(f'netsh interface set interface name="{nic_name}" admin=enable', shell=True,
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, capture_output_if_no_pipes=False)
    time.sleep(3)

    if result and result.returncode == 0:
        print(f"{AnsiColor.GREEN}[✓] MAC address successfully set for {nic_name}.{AnsiColor.END}")
        return True
    else:
        print(f"{AnsiColor.RED}[!] Failed to set MAC address for {nic_name}.{AnsiColor.END}")
        return False


def change_mac_address_integrated():
    print(f"\n{Fore.BLUE}[+] Initializing MAC Address Spoofer...{Style.RESET_ALL}")
    if not is_admin(): print(f"    {Fore.RED}Administrator privileges required. Skipping.{Style.RESET_ALL}"); return
    adapters = get_available_nics_new()
    if not adapters: print(f"    {Fore.YELLOW}[!] No suitable network adapters found.{Style.RESET_ALL}"); return

    print(f"    {Fore.CYAN}Available Network Adapters:{Style.RESET_ALL}")
    for i, adapter_info in enumerate(adapters): print(f"      {i + 1}. {adapter_info['name']}")
    try:
        choice_str = input(
            f"    {Fore.MAGENTA}Select adapter to spoof (e.g., 1, or type 'all', 'skip'): {Style.RESET_ALL}").strip().lower()
        if choice_str == 'skip': print(f"    {Fore.YELLOW}MAC spoofing skipped.{Style.RESET_ALL}"); return

        targets = adapters if choice_str == 'all' else (
            [adapters[int(choice_str) - 1]] if choice_str.isdigit() and 1 <= int(choice_str) <= len(adapters) else [])
        if not targets: print(f"    {Fore.RED}[!] Invalid selection.{Style.RESET_ALL}"); return

        changed_count = 0
        for adapter in targets:
            nic_name, nic_idx = adapter['name'], adapter['index']
            new_mac = generate_random_mac_enforce_02()
            print(
                f"\n    {Fore.CYAN}Spoofing {nic_name} with MAC: {':'.join(new_mac[j:j + 2] for j in range(0, 12, 2))}{Style.RESET_ALL}")
            if set_mac_address_new(nic_name, nic_idx, new_mac): changed_count += 1
            time.sleep(1)
        if changed_count > 0: print(
            f"\n{Fore.GREEN}[✓] {changed_count} MAC address(es) spoofed. RESTART RECOMMENDED.{Style.RESET_ALL}")
    except Exception as e:
        print(f"    {Fore.RED}[!] An error during MAC spoofing: {e}{Style.RESET_ALL}")


# --- Roblox Install function ---
def install_roblox():
    print(f"\n{Fore.GREEN}[+] Installing Roblox (Standard Download)...{Style.RESET_ALL}")
    installer_url = "https://www.roblox.com/download/client"
    installer_filename = f"RobloxPlayerInstaller_{uuid.uuid4().hex[:8]}.exe"
    installer_path = os.path.join(os.environ.get('TEMP', '.'), installer_filename)

    if os.path.exists(installer_path):
        try:
            os.remove(installer_path)
        except Exception:
            pass

    downloaded = False
    print(f"    Attempting download with Python requests...")
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
        with requests.get(installer_url, stream=True, timeout=30, headers=headers, allow_redirects=True) as r:
            r.raise_for_status()
            with open(installer_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192): f.write(chunk)
        if os.path.exists(installer_path) and os.path.getsize(installer_path) > 1000000:
            downloaded = True
            print(f"    {Fore.GREEN}Downloaded successfully.{Style.RESET_ALL}")
    except requests.exceptions.RequestException as e_req:
        print(f"    {Fore.RED}Download error: {e_req}{Style.RESET_ALL}")

    if not downloaded:
        print(f"{Fore.RED}[!] Could not download Roblox installer.{Style.RESET_ALL}")
        return

    print(f"    {Fore.CYAN}Starting Roblox installation...{Style.RESET_ALL}")
    try:
        subprocess.Popen([installer_path], creationflags=subprocess.CREATE_NEW_CONSOLE)
        print(f"    {Fore.GREEN}Installer launched. Follow on-screen instructions.{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}    Failed to start installer: {e}{Style.RESET_ALL}")
        return

    print(f"    {Fore.YELLOW}Waiting 45s for installation to proceed...{Style.RESET_ALL}")
    for i in range(45, 0, -1):
        print(f"\r    Waiting... {i}s remaining. ", end="")
        time.sleep(1)
    print("\r    Installation time elapsed. Verifying...            ")

    # --- MODIFIED VERIFICATION LOGIC ---
    roblox_appdata_path = os.path.join(os.environ.get('LOCALAPPDATA', ''), "Roblox")
    installed_ok = False
    print(f"\n    {Fore.CYAN}Verifying Roblox installation at: {roblox_appdata_path}{Style.RESET_ALL}")

    if os.path.isdir(roblox_appdata_path):
        try:
            if any(os.scandir(roblox_appdata_path)):
                installed_ok = True
                print(f"    {Fore.GREEN}Found Roblox directory and it is not empty.{Style.RESET_ALL}")
            else:
                print(f"    {Fore.YELLOW}Found Roblox directory, but it appears to be empty.{Style.RESET_ALL}")
        except Exception as e_scan:
            print(f"    {Fore.YELLOW}Could not scan Roblox directory contents: {e_scan}{Style.RESET_ALL}")
    else:
        print(f"    {Fore.YELLOW}Roblox directory not found at the expected location.{Style.RESET_ALL}")

    if installed_ok:
        print(f"\n{Fore.GREEN}[✓] Roblox installation appears complete.{Style.RESET_ALL}")
    else:
        print(
            f"\n{Fore.YELLOW}[!] Roblox installation uncertain. The target directory may be missing or empty.{Style.RESET_ALL}")

    if os.path.exists(installer_path):
        try:
            os.remove(installer_path)
        except Exception:
            pass


# --- EDID, Hyperion Key, SMBIOS functions ---
def get_current_user_sid_string():
    if PYWIN32_AVAILABLE:
        try:
            token = win32security.OpenProcessToken(win32api.GetCurrentProcess(), win32security.TOKEN_QUERY)
            return win32security.ConvertSidToStringSid(
                win32security.GetTokenInformation(token, win32security.TokenUser)[0])
        except Exception:
            pass
    # Fallback to PowerShell if pywin32 fails or is unavailable
    get_sid_command = "([System.Security.Principal.WindowsIdentity]::GetCurrent()).User.Value"
    result = _run_shell_command_wrapper(["powershell", "-Command", get_sid_command], capture_output=True, shell=False)
    if result and result.returncode == 0 and result.stdout:
        user_sid = result.stdout.strip()
        if user_sid.startswith("S-"):
            return user_sid
    return None


def calculate_edid_checksum(edid_data_bytes):
    if len(edid_data_bytes) < 128: return edid_data_bytes[-1] if edid_data_bytes else 0
    return (256 - (sum(edid_data_bytes[:127]) % 256)) % 256


def modify_monitor_edids():
    print(f"\n{Fore.BLUE}[+] Modifying Monitor EDID serials...{Style.RESET_ALL}")
    if not is_admin(): print(f"    {Fore.RED}Admin privileges required. Skipping.{Style.RESET_ALL}"); return

    changed_count, monitors_processed = 0, 0
    base_path = r"SYSTEM\CurrentControlSet\Enum\DISPLAY"
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, base_path, 0,
                            winreg.KEY_READ | winreg.KEY_WRITE | winreg.KEY_WOW64_64KEY) as display_key:
            m_idx = 0
            while True:
                try:
                    m_vendor = winreg.EnumKey(display_key, m_idx)
                    with winreg.OpenKey(display_key, m_vendor, 0,
                                        winreg.KEY_READ | winreg.KEY_WRITE | winreg.KEY_WOW64_64KEY) as vendor_k:
                        i_idx = 0
                        while True:
                            try:
                                m_instance = winreg.EnumKey(vendor_k, i_idx)
                                monitors_processed += 1
                                dev_params_p = os.path.join(m_instance, "Device Parameters")
                                try:
                                    with winreg.OpenKey(vendor_k, dev_params_p, 0,
                                                        winreg.KEY_READ | winreg.KEY_WRITE | winreg.KEY_WOW64_64KEY) as dev_k:
                                        edid_val, reg_t = winreg.QueryValueEx(dev_k, "EDID")
                                        if reg_t == winreg.REG_BINARY and len(edid_val) >= 128:
                                            m_edid = bytearray(edid_val)
                                            block0 = m_edid[:128]
                                            for i_sn in range(12, 16): block0[i_sn] = random.randint(0, 255)
                                            block0[127] = calculate_edid_checksum(block0)
                                            winreg.SetValueEx(dev_k, "EDID", 0, reg_t, bytes(m_edid))
                                            print(
                                                f"    {Fore.GREEN}Modified EDID for: {m_vendor}\\{m_instance}{Style.RESET_ALL}")
                                            changed_count += 1
                                except (FileNotFoundError, Exception):
                                    pass
                                i_idx += 1
                            except OSError:
                                break
                    m_idx += 1
                except OSError:
                    break
    except Exception as e_base:
        print(f"    {Fore.RED}Error accessing display registry for EDID: {e_base}{Style.RESET_ALL}")

    if changed_count > 0:
        print(f"{Fore.GREEN}[✓] {changed_count} monitor EDID(s) modified. RESTART REQUIRED.{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}[!] No monitors found or EDIDs modified.{Style.RESET_ALL}")


def manage_system_registry_keys():
    print(f"\n{Fore.BLUE}[+] Cleaning system registry keys using PowerShell...{Style.RESET_ALL}")
    if not is_admin():
        print(f"    {Fore.RED}Admin privileges required. Skipping.{Style.RESET_ALL}")
        return

    user_sid = get_current_user_sid_string()
    if not user_sid:
        print(f"    {Fore.RED}[!] Could not retrieve user SID. Skipping key deletion.{Style.RESET_ALL}")
        return

    # Define registry paths to be cleaned
    paths_to_clean = {
        "Control (HKCU)": "HKCU:\\System\\CurrentControlSet\\Control",
        "Control (HKEY_USERS)": f"Registry::HKEY_USERS\\{user_sid}\\System\\CurrentControlSet\\Control",
        "GameConfigStore (HKCU)": "HKCU:\\System\\GameConfigStore",
        "GameConfigStore (HKEY_USERS)": f"Registry::HKEY_USERS\\{user_sid}\\System\\GameConfigStore",
        "New Key #1 in Control (HKCU)": "HKCU:\\System\\CurrentControlSet\\Control\\New Key #1",
        "New Key #1 in CurrentControlSet (HKEY_USERS)": f"Registry::HKEY_USERS\\{user_sid}\\System\\CurrentControlSet\\New Key #1"
    }

    overall_success = True

    for key_name, path in paths_to_clean.items():
        # PowerShell command checks if the path exists before attempting removal.
        # This prevents "ItemNotFound" errors from appearing for already clean systems.
        # Note: The key name might contain spaces, so the path is quoted.
        command = f"if (Test-Path -Path '{path}') {{ Remove-Item -Path '{path}' -Recurse -Force -ErrorAction SilentlyContinue }}"
        print(f"    Executing check and delete for: {key_name}")

        result = _run_shell_command_wrapper(["powershell", "-Command", command], capture_output=True, shell=False)

        if result and result.returncode == 0:
            print(f"    {Fore.GREEN}[✓] Command for {key_name} executed successfully.{Style.RESET_ALL}")
        elif result:
            # This block will now only catch unexpected PowerShell errors
            print(
                f"    {Fore.RED}[!] Command for {key_name} failed with exit code: {result.returncode}{Style.RESET_ALL}")
            if result.stderr:
                print(f"        PowerShell Error: {result.stderr.strip()}")
            overall_success = False
        else:
            print(f"    {Fore.RED}[!] Failed to execute PowerShell command for {key_name}.{Style.RESET_ALL}")
            overall_success = False

    if overall_success:
        print(f"{Fore.GREEN}[✓] System registry cleaning process completed.{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}[!] One or more system registry key deletions failed unexpectedly.{Style.RESET_ALL}")


def download_amidewin_tools():
    print(f"\n{Fore.BLUE}[+] Downloading AMIDEWIN tools...{Style.RESET_ALL}")
    temp_amide_dir = os.path.join(os.environ.get('TEMP', '.'), "AmideWinToolsByGone")
    global AMIDEWIN_DIR_HWID, AMIDEWIN_TOOLS_MAP, AMIDEWIN_FILES_TO_DELETE
    AMIDEWIN_DIR_HWID = temp_amide_dir
    AMIDEWIN_TOOLS_MAP = {
        os.path.join(AMIDEWIN_DIR_HWID,
                     "AMIDEWINx64.EXE"): "https://github.com/xxdotdos/amidewinpast/raw/main/AMIDEWINx64.EXE",
        os.path.join(AMIDEWIN_DIR_HWID,
                     "amigendrv64.sys"): "https://github.com/xxdotdos/amidewinpast/raw/main/amigendrv64.sys",
        os.path.join(AMIDEWIN_DIR_HWID,
                     "amifldrv64.sys"): "https://github.com/xxdotdos/amidewinpast/raw/main/amifldrv64.sys",
    }
    AMIDEWIN_FILES_TO_DELETE = list(AMIDEWIN_TOOLS_MAP.keys()) + [AMIDEWIN_DIR_HWID]
    os.makedirs(AMIDEWIN_DIR_HWID, exist_ok=True)

    all_ok = True
    for i, (dest_path, url) in enumerate(AMIDEWIN_TOOLS_MAP.items()):
        print_progress_bar(i, len(AMIDEWIN_TOOLS_MAP), prefix='    Downloading:',
                           suffix=f'{os.path.basename(dest_path):<20}', length=30, color=Fore.BLUE)
        if os.path.exists(dest_path) and os.path.getsize(dest_path) > 10000: continue
        try:
            with requests.get(url, stream=True, timeout=30) as r:
                r.raise_for_status()
                with open(dest_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192): f.write(chunk)
        except Exception as e_dl:
            print(f"\n    {Fore.RED}Failed to download {os.path.basename(dest_path)}: {e_dl}{Style.RESET_ALL}")
            all_ok = False
    print_progress_bar(len(AMIDEWIN_TOOLS_MAP), len(AMIDEWIN_TOOLS_MAP), prefix='    Downloading:',
                       suffix='Done!                ', length=30, color=Fore.GREEN if all_ok else Fore.YELLOW)
    if not all_ok: print(f"{Fore.RED}[!] Failed to download one or more AMIDEWIN tools.{Style.RESET_ALL}")
    return all_ok


def delete_amidewin_tools():
    print(f"\n{Fore.BLUE}[+] Deleting AMIDEWIN tools...{Style.RESET_ALL}")
    for file_path in [f for f in AMIDEWIN_FILES_TO_DELETE if os.path.isfile(f)]:
        try:
            os.remove(file_path)
        except Exception:
            pass
    amide_dir = AMIDEWIN_DIR_HWID
    if os.path.isdir(amide_dir):
        try:
            shutil.rmtree(amide_dir)
        except Exception:
            pass
    print(f"{Fore.GREEN}[✓] AMIDEWIN cleanup finished.{Style.RESET_ALL}")


def spoof_smbios_with_amidewin_focused():
    print(f"\n{Fore.BLUE}[+] Spoofing System UUID with AMIDEWIN...{Style.RESET_ALL}")
    exe_path = os.path.join(AMIDEWIN_DIR_HWID, "AMIDEWINx64.EXE")
    if not os.path.exists(exe_path): print(
        f"    {Fore.RED}AMIDEWINx64.EXE not found. Skipping.{Style.RESET_ALL}"); return False

    ami_commands = {"/SU": "Auto"}
    success_count = 0
    for i, (param, value) in enumerate(ami_commands.items()):
        print_progress_bar(i, len(ami_commands), prefix='    SMBIOS Update:', suffix=f'{param} {value}...', length=30,
                           color=Fore.BLUE)
        cmd_result = _run_shell_command_simple([exe_path, param, value], cwd=AMIDEWIN_DIR_HWID, shell=False,
                                               capture_output_if_no_pipes=True, timeout=20)
        if cmd_result and cmd_result.returncode == 0: success_count += 1
    print_progress_bar(len(ami_commands), len(ami_commands), prefix='    SMBIOS Update:', suffix='Done!        ',
                       length=30, color=Fore.GREEN)
    if success_count > 0:
        print(f"    {Fore.GREEN}AMIDEWIN commands issued. RESTART IS CRITICAL.{Style.RESET_ALL}");
        return True
    else:
        print(f"    {Fore.RED}No AMIDEWIN SMBIOS commands succeeded.{Style.RESET_ALL}");
        return False


def restart_wmi_service():
    print(f"\n{Fore.BLUE}[+] Restarting WMI service (winmgmt)...{Style.RESET_ALL}")
    if not is_admin(): print(f"    {Fore.RED}Admin rights needed. Skipping.{Style.RESET_ALL}"); return
    _run_shell_command_simple(["net", "stop", "winmgmt", "/y"], shell=False, timeout=45,
                              capture_output_if_no_pipes=True)
    time.sleep(3)
    _run_shell_command_simple(["net", "start", "winmgmt"], shell=False, timeout=45, capture_output_if_no_pipes=True)
    time.sleep(2)
    sc_query_res = _run_shell_command_simple(['sc', 'query', 'winmgmt'], shell=False, capture_output_if_no_pipes=True,
                                             timeout=10)
    if sc_query_res and sc_query_res.stdout and "RUNNING" in sc_query_res.stdout.upper():
        print(f"    {Fore.GREEN}WMI service (winmgmt) is confirmed RUNNING.{Style.RESET_ALL}")
    else:
        print(f"    {Fore.YELLOW}WMI status uncertain.{Style.RESET_ALL}")


def perform_focused_hwid_spoof():
    print(f"\n{Fore.MAGENTA}{'=' * 10} Initiating Focused HWID Spoofing {'=' * 10}{Style.RESET_ALL}")
    if not is_admin(): print(f"    {Fore.RED}Admin rights needed. Skipping.{Style.RESET_ALL}"); return
    if not download_amidewin_tools(): print(
        f"    {Fore.RED}[!] AMIDEWIN download failed. Aborting.{Style.RESET_ALL}"); return

    if spoof_smbios_with_amidewin_focused(): restart_wmi_service()
    delete_amidewin_tools()
    print(f"\n{Fore.GREEN}[✓] Focused HWID spoofing attempt completed.{Style.RESET_ALL}")


# --- Main Operation Sequence ---
def perform_all_spoofing_operations():
    try:
        requests.get("https://1.1.1.1", timeout=5)
    except requests.exceptions.RequestException:
        print(f"{Fore.RED}[!] No internet connection detected.{Style.RESET_ALL}")
        if input("    Continue anyway? (y/n): ").strip().lower() != 'y': return False

    uninstall_roblox()
    delete_roblox_registry_keys()
    delete_roblox_cookies()
    change_mac_address_integrated()

    print(f"\n{Fore.YELLOW}[+] Pausing 10s for network adapters to stabilize...{Style.RESET_ALL}")
    time.sleep(10)

    modify_monitor_edids()
    manage_system_registry_keys()
    perform_focused_hwid_spoof()
    install_roblox()

    print(f"\n{Fore.GREEN}{Style.BRIGHT}{'=' * 80}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}{Style.BRIGHT}[✓] All operations completed! A FULL RESTART IS REQUIRED!{Style.RESET_ALL}")
    print(f"{Fore.GREEN}{Style.BRIGHT}{'=' * 80}{Style.RESET_ALL}")
    return True


# --- Main Execution ---
def main():
    if os.name == 'nt': set_terminal_transparency(alpha_percentage=85)
    os.system('cls')
    print(f"{Fore.CYAN}{BANNER}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{Style.BRIGHT}{'=' * 80}{Style.RESET_ALL}")
    print(f"{Fore.WHITE}{Style.BRIGHT}Nitaybl's ByGone Spoofer (Focused Hyperion){Style.RESET_ALL}")
    print(f"{Fore.CYAN}Version: v4.0 (Patched){Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{Style.BRIGHT}{'=' * 80}{Style.RESET_ALL}\n")

    if not is_admin():
        print(f"{Fore.RED}[!] Admin privileges required. Restarting with admin rights...{Style.RESET_ALL}")
        time.sleep(1)
        restart_with_admin()
        if not is_admin():
            print(f"{Fore.RED}[FATAL] Failed to acquire admin privileges. Exiting.{Style.RESET_ALL}")
            sys.exit(1)

    print(f"{Fore.GREEN}[✓] Running as administrator.{Style.RESET_ALL}")
    if not PYWIN32_AVAILABLE: print(
        f"{Fore.YELLOW}Warning: pywin32 not found. Using 'whoami' for SID.{Style.RESET_ALL}")

    proceed_input = input("\nDo you wish to proceed? (yes/no): ").strip().lower()
    if proceed_input in ['yes', 'y']:
        try:
            start_time = time.time()
            perform_all_spoofing_operations()
            print(f"\n{Fore.CYAN}Total execution time: {time.time() - start_time:.2f} seconds.{Style.RESET_ALL}")
        except (SystemExit, KeyboardInterrupt):
            print(f"\n\n{Fore.YELLOW}Operation cancelled by user.{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}{Style.BRIGHT}\n\nAN UNEXPECTED CRITICAL ERROR OCCURRED: {e}{Style.RESET_ALL}")
            import traceback
            traceback.print_exc()
    else:
        print(f"{Fore.YELLOW}Operation cancelled.{Style.RESET_ALL}")

    input("\nPress Enter to exit...")


if __name__ == "__main__":
    main()
# Copyright (c) 2025 nitaybl. All Rights Reserved
