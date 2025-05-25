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
from colorama import init, Fore, Style
import uuid
import string

# Initialize colorama
init(autoreset=True)

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
| $$  \ $$| $$  | $$| $$  \ $$| $$  | $$| $$  | $$| $$_____/      | $$  \ $$| $$  \ $$       /$$  \ $$| $$  | $$| $$  | $$| $$  \ $$| $$    | $$_____/| $$
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
AMIDEWIN_DIR_HWID = r"C:\Windows\Fonts"
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

# --- MAC Spoofing Constants ---
REG_KEY_BASE_MAC = r"SYSTEM\CurrentControlSet\Control\Class\{4d36e972-e325-11ce-bfc1-08002be10318}"
HEX_CHARS_MAC = "0123456789ABCDEF"
SECOND_CHAR_OPTIONS_MAC = "AE26"


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
    sys.exit(0)


def print_progress_bar(iteration, total, prefix='', suffix='', length=50, fill='=', color=Fore.WHITE):
    if total <= 0:  # Avoid division by zero if total is 0 or negative
        percent_str = "N/A"
        bar_fill = ' ' * length
    else:
        percent = 100 * (iteration / float(total))
        percent_str = f"{percent:.1f}"
        filled_length = int(length * iteration // total)
        bar_fill = fill * filled_length + ' ' * (length - filled_length)
    print(f'\r{prefix} [{color}{bar_fill}{Style.RESET_ALL}] {percent_str}% {suffix}', end='', flush=True)
    if iteration >= total: print()  # Print newline when done or exceeded


def _run_shell_command_simple(command, capture_output_if_no_pipes=True, text=True, check=False, shell=True, stdout=None,
                              stderr=None, timeout=None):
    actual_command_for_run = command
    display_command_str = ""
    if isinstance(command, list):
        display_command_str = ' '.join(command)
        if shell:
            actual_command_for_run = subprocess.list2cmdline(command)
    elif isinstance(command, str):
        display_command_str = command
    else:
        print(f"{Fore.RED}    Invalid command type for _run_shell_command_simple: {type(command)}{Style.RESET_ALL}")
        return None
    try:
        # Determine effective stdout/stderr for capture_output logic
        effective_stdout = stdout
        effective_stderr = stderr
        do_capture = False

        if stdout is None and capture_output_if_no_pipes:
            effective_stdout = subprocess.PIPE
            do_capture = True
        if stderr is None and capture_output_if_no_pipes:
            effective_stderr = subprocess.PIPE
            do_capture = True

        # If not capturing to PIPE, ensure capture_output=False for subprocess.run
        # if we are redirecting to DEVNULL etc.
        final_capture_output = do_capture if (
                    effective_stdout == subprocess.PIPE or effective_stderr == subprocess.PIPE) else False

        return subprocess.run(actual_command_for_run,
                              capture_output=final_capture_output,
                              text=text, check=check, shell=shell, errors='ignore',
                              stdout=effective_stdout, stderr=effective_stderr, timeout=timeout)
    except FileNotFoundError:
        print(f"{Fore.RED}    Command not found (simple): {display_command_str}{Style.RESET_ALL}")
        return None
    except subprocess.TimeoutExpired:
        print(f"{Fore.YELLOW}    Command timed out (simple): {display_command_str}{Style.RESET_ALL}")
        return None
    except Exception as e:
        print(f"{Fore.RED}    Shell command error (simple) for '{display_command_str}': {e}{Style.RESET_ALL}")
        return None


def _run_shell_command_wrapper(command_list, capture_output=False, text=True, check=False, shell=False, cwd=None,
                               timeout=None, hide_window=False):
    command_str = ' '.join(command_list) if isinstance(command_list, list) else command_list
    startupinfo = None
    creationflags = 0
    if hide_window:
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE  # Explicitly hide
        creationflags = subprocess.CREATE_NO_WINDOW
    try:
        console_encoding = sys.stdout.encoding if sys.stdout.encoding else 'utf-8'  # Prefer utf-8
        return subprocess.run(
            command_list, capture_output=capture_output, text=text, check=check, shell=shell,
            encoding=console_encoding, errors='replace', cwd=cwd, timeout=timeout,
            startupinfo=startupinfo, creationflags=creationflags
        )
    except subprocess.TimeoutExpired:
        print(f"{Fore.YELLOW}    Command timed out (wrapper): {command_str}{Style.RESET_ALL}")
        return None
    except Exception as e:
        print(f"{Fore.RED}    Shell command error (wrapper) for '{command_str}': {e}{Style.RESET_ALL}")
        return None


# --- Function to set terminal transparency ---
def set_terminal_transparency(alpha_percentage=37):  # Default changed to 37%
    """Sets the console window transparency.
    alpha_percentage: An integer from 0 (fully transparent) to 100 (fully opaque).
    """
    if os.name != 'nt': return  # Only for Windows
    if not (0 <= alpha_percentage <= 100):
        print(f"{Fore.YELLOW}Transparency percentage must be between 0 and 100.{Style.RESET_ALL}")
        return

    alpha_value = int((alpha_percentage / 100.0) * 255)

    try:
        hwnd = ctypes.windll.kernel32.GetConsoleWindow()
        if not hwnd:
            # print(f"{Fore.YELLOW}Could not get console window handle. Transparency not set.{Style.RESET_ALL}")
            return  # Fail silently if no console (e.g. running headless)

        current_style = ctypes.windll.user32.GetWindowLongA(hwnd, GWL_EXSTYLE)
        # Ensure WS_EX_LAYERED is set
        if not (current_style & WS_EX_LAYERED):
            ctypes.windll.user32.SetWindowLongA(hwnd, GWL_EXSTYLE, current_style | WS_EX_LAYERED)

        if not ctypes.windll.user32.SetLayeredWindowAttributes(hwnd, 0, alpha_value, LWA_ALPHA):
            # print(f"{Fore.YELLOW}Failed to set layered window attributes. Error: {ctypes.GetLastError()}{Style.RESET_ALL}")
            pass  # Fail silently
        else:
            # print(f"{Fore.CYAN}Terminal transparency set to {alpha_percentage}%.{Style.RESET_ALL}") # Optional: too verbose
            pass
    except Exception as e:
        # print(f"{Fore.RED}Error setting terminal transparency: {e}{Style.RESET_ALL}") # Optional: too verbose
        pass


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
                                           shell=False,  # Safer with list args
                                           check=False,
                                           capture_output_if_no_pipes=False)  # Don't capture, just execute
        if result and result.returncode == 0:
            killed_any = True
            # print(f"    {Fore.GREEN}Terminated {proc_name}{Style.RESET_ALL}") # Can be verbose
    if killed_any:
        print(f"{Fore.GREEN}[✓] Roblox processes terminated (if any were running).{Style.RESET_ALL}")
    else:
        print(f"{Fore.GREEN}[✓] No critical Roblox processes found running or terminated.{Style.RESET_ALL}")


def delete_roblox_cookies():
    kill_roblox_processes()
    print(f"{Fore.RED}[+] Deleting Roblox cookies & related data...{Style.RESET_ALL}")
    app_data_local = os.environ.get('LOCALAPPDATA', '')
    cookie_paths = [
        os.path.join(app_data_local, 'Roblox', 'browsercookie'),  # Old
        os.path.join(os.environ.get('APPDATA', ''), 'Roblox', 'cookies'),  # Old
        os.path.join(app_data_local, 'Packages', 'ROBLOXCORPORATION.ROBLOX_55nm5eh3cm0pr', 'AC', 'Cookies'),  # UWP
        os.path.join(app_data_local, 'Roblox', 'RobloxCookies.dat'),
        os.path.join(app_data_local, 'Roblox', 'RobloxBrowserCache'),
        os.path.join(app_data_local, 'Roblox', 'http'),
        os.path.join(app_data_local, 'Roblox', 'logs', 'rbxhttplogs'),
        os.path.join(app_data_local, 'Roblox', 'LocalStorage'),
    ]
    deleted_count = 0
    total_steps = len(cookie_paths) if cookie_paths else 1
    for i, path in enumerate(cookie_paths):
        print_progress_bar(i, total_steps, prefix='    Cookie Deletion:', suffix=f'{os.path.basename(path)[:15]:<15}',
                           length=30, color=Fore.RED)
        time.sleep(0.02)  # Small delay for visual effect
        if os.path.exists(path):
            try:
                if os.path.isdir(path):
                    shutil.rmtree(path, ignore_errors=True)
                else:
                    os.remove(path)
                if not os.path.exists(path):  # Check if really deleted
                    deleted_count += 1
            except Exception as e:
                # print(f"\n{Fore.YELLOW}    Warning: Could not delete {path}: {e}{Style.RESET_ALL}") # Can be verbose
                pass
    print_progress_bar(total_steps, total_steps, prefix='    Cookie Deletion:', suffix='Done             ', length=30,
                       color=Fore.RED)

    if deleted_count > 0:
        print(f"{Fore.GREEN}[✓] Roblox cookie/cache items processed for deletion.{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}[!] No specific Roblox cookie/cache items found or deleted.{Style.RESET_ALL}")


def uninstall_roblox():
    kill_roblox_processes()  # Ensure killed before uninstall
    print(f"\n{Fore.RED}[+] Uninstalling Roblox...{Style.RESET_ALL}")
    roblox_paths_to_delete = [
        os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Roblox'),
        # ProgramFiles paths are less common for current Roblox client installs but good to check
        os.path.join(os.environ.get('PROGRAMFILES', ''), 'Roblox'),
        os.path.join(os.environ.get('PROGRAMFILES(X86)', ''), 'Roblox')
    ]
    uninstaller_path_cmd = None  # Will store the full command string
    uninstaller_exe = None  # Just the exe path

    uninstall_reg_keys = [
        (winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall', winreg.KEY_WOW64_64KEY),
        (winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall', 0),
        # Check 32-bit on 64-bit OS
        (winreg.HKEY_CURRENT_USER, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall', 0)  # Per-user installs
    ]

    for hkey_root, reg_path_base, access_flags in uninstall_reg_keys:
        if uninstaller_path_cmd: break
        try:
            with winreg.OpenKey(hkey_root, reg_path_base, 0, winreg.KEY_READ | access_flags) as key:
                i = 0
                while True:
                    try:
                        sub_key_name = winreg.EnumKey(key, i)
                        with winreg.OpenKey(key, sub_key_name, 0, winreg.KEY_READ | access_flags) as sk:
                            try:
                                name = winreg.QueryValueEx(sk, 'DisplayName')[0]
                                if 'roblox player' in name.lower():  # More specific to player
                                    uninstaller_path_cmd = winreg.QueryValueEx(sk, 'UninstallString')[0]
                                    # Extract just the .exe part for Popen
                                    if '"' in uninstaller_path_cmd:
                                        uninstaller_exe = uninstaller_path_cmd.split('"')[1]
                                    else:
                                        uninstaller_exe = uninstaller_path_cmd.split(' ')[0]
                                    break  # Found it
                            except FileNotFoundError:
                                pass  # Value not found
                            except Exception:
                                pass  # Other errors reading values
                        i += 1
                    except OSError:
                        break  # No more subkeys
            if uninstaller_path_cmd: break
        except FileNotFoundError:
            pass  # Registry path not found
        except Exception:
            pass  # Other errors opening key

    success_uninstaller = False
    if uninstaller_exe and os.path.exists(uninstaller_exe):
        print(f"    {Fore.CYAN}Found Roblox uninstaller: {uninstaller_exe}{Style.RESET_ALL}")
        print(f"    {Fore.CYAN}Attempting to run: {uninstaller_path_cmd}{Style.RESET_ALL}")
        try:
            # Roblox uninstaller (RobloxPlayerInstaller.exe) often uses /uninstall or /uninstallquiet
            # The UninstallString might already contain silent flags.
            # If not, we try to add them.
            cmd_list_for_popen = []
            if '"' in uninstaller_path_cmd:  # Path with spaces
                path_part = uninstaller_path_cmd.split('"')[1]
                args_part = uninstaller_path_cmd.split('"')[2:]
                cmd_list_for_popen.append(path_part)
                if args_part and args_part[0].strip():
                    cmd_list_for_popen.extend(args_part[0].strip().split())
            else:  # Path without spaces
                cmd_list_for_popen = uninstaller_path_cmd.split()

            # Ensure silent/quiet flags if possible
            if 'RobloxPlayerInstaller.exe' in uninstaller_exe.lower():
                if not any(flag in cmd_list_for_popen for flag in ['/uninstallquiet', '/quiet', '/S']):
                    if '/uninstall' not in cmd_list_for_popen:
                        cmd_list_for_popen.append('/uninstall')
                    cmd_list_for_popen.append('/quiet')  # Add quiet flag
            elif not any(flag in cmd_list_for_popen for flag in ['/S', '/silent', '/q']):
                cmd_list_for_popen.append('/S')  # Generic silent

            print(f"    {Fore.CYAN}Executing: {' '.join(cmd_list_for_popen)}{Style.RESET_ALL}")
            p = subprocess.Popen(cmd_list_for_popen, shell=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            p.wait(timeout=120)  # Increased timeout
            success_uninstaller = True
            print(f"    {Fore.GREEN}Roblox uninstaller process completed.{Style.RESET_ALL}")
            time.sleep(5)  # Give fs time to settle
        except subprocess.TimeoutExpired:
            print(f"    {Fore.YELLOW}Roblox uninstaller timed out.{Style.RESET_ALL}")
        except Exception as e:
            print(f"    {Fore.RED}Error running Roblox uninstaller: {e}. Manual deletion will follow.{Style.RESET_ALL}")
    else:
        print(
            f"    {Fore.YELLOW}Official Roblox uninstaller not found or path invalid. Proceeding with manual deletion.{Style.RESET_ALL}")

    manual_deletion_done = False
    print(f"    {Fore.CYAN}Performing manual folder deletions...{Style.RESET_ALL}")
    total_del_paths = len(roblox_paths_to_delete)
    for i, path in enumerate(roblox_paths_to_delete):
        print_progress_bar(i, total_del_paths, prefix='    Manual Deletion:',
                           suffix=f'{os.path.basename(path)[:15]:<15}', length=30, color=Fore.RED)
        time.sleep(0.05)
        if os.path.exists(path):
            try:
                shutil.rmtree(path, ignore_errors=True)  # ignore_errors to be more aggressive
                if not os.path.exists(path):
                    manual_deletion_done = True
            except Exception as e:
                # print(f"\n{Fore.YELLOW}    Warning: Could not delete {path}: {e}{Style.RESET_ALL}")
                pass  # Fail silently for manual deletion errors
    print_progress_bar(total_del_paths, total_del_paths, prefix='    Manual Deletion:', suffix='Done             ',
                       length=30, color=Fore.RED)

    if success_uninstaller or manual_deletion_done:
        print(f"{Fore.GREEN}[✓] Roblox uninstallation/removal attempted.{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}[!] Roblox may not have been fully uninstalled or was not found.{Style.RESET_ALL}")


# --- MAC Spoofing Functions ---
def get_nic_index_from_name_new(network_adapter_name):
    # Try PowerShell first as it's often more reliable for interface names
    ps_command = f"(Get-NetAdapter -Name '{network_adapter_name.replace('\"', '')}').InterfaceIndex"  # Remove quotes for PS
    try:
        process = _run_shell_command_simple(['powershell', '-NoProfile', '-Command', ps_command], shell=False,
                                            capture_output_if_no_pipes=True, timeout=5)
        if process and process.returncode == 0 and process.stdout and process.stdout.strip().isdigit():
            return process.stdout.strip()
    except Exception:  # Catch PS errors or if it's not available
        pass

    # Fallback to WMIC
    try:
        # Ensure network_adapter_name is properly quoted for WMIC if it contains spaces
        # WMIC query uses single quotes around the value for NetConnectionID
        command = f'wmic nic where "NetConnectionID=\'{network_adapter_name}\'" get Index /format:value'
        process_wmic = _run_shell_command_simple(command, shell=True, capture_output_if_no_pipes=True,
                                                 timeout=5)  # shell=True for complex wmic query
        if process_wmic and process_wmic.stdout:
            match = re.search(r"Index=(\d+)", process_wmic.stdout)
            if match:
                return match.group(1)
    except Exception as e:
        print(f"{Fore.RED}    Error getting NIC index for '{network_adapter_name}' (WMIC): {e}{Style.RESET_ALL}")
    return None


def generate_random_mac_value_new():
    # XX:XX:XX:XX:XX:XX, first octet's second char must be 2, 6, A, or E for local admin
    mac_parts = [random.choice(HEX_CHARS_MAC) + random.choice(SECOND_CHAR_OPTIONS_MAC)]
    for _ in range(5):
        mac_parts.append(random.choice(HEX_CHARS_MAC) + random.choice(HEX_CHARS_MAC))
    return "".join(mac_parts)


def format_mac_for_display_new(mac_value_no_colons):
    if not mac_value_no_colons or len(mac_value_no_colons) != 12: return "INVALID_MAC"
    return ":".join(mac_value_no_colons[i:i + 2] for i in range(0, 12, 2))


def change_mac_address():
    print(f"\n{Fore.BLUE}[+] Changing MAC addresses for enabled, connected, physical adapters...{Style.RESET_ALL}")
    if not is_admin():
        print(f"    {Fore.RED}Administrator privileges required. Skipping MAC change.{Style.RESET_ALL}")
        return

    changed_count = 0
    adapter_names_to_change = []

    # PowerShell to get relevant adapters: Name, InterfaceDescription, Status
    ps_get_adapters = "Get-NetAdapter | Where-Object {$_.Status -eq 'Up' -and !$_.Virtual -and $_.ConnectorPresent} | Select-Object -ExpandProperty Name"
    try:
        ps_process = _run_shell_command_simple(
            ['powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-Command', ps_get_adapters],
            shell=False, capture_output_if_no_pipes=True, timeout=10)
        if ps_process and ps_process.returncode == 0 and ps_process.stdout:
            adapter_names_to_change = [name.strip() for name in ps_process.stdout.splitlines() if name.strip()]
    except Exception:  # Fallback if PowerShell fails
        pass

    if not adapter_names_to_change:  # Fallback to netsh if PowerShell yielded nothing or failed
        print(f"    {Fore.YELLOW}PowerShell did not list adapters or failed. Trying netsh...{Style.RESET_ALL}")
        try:
            res_netsh = _run_shell_command_simple(['netsh', 'interface', 'show', 'interface'], shell=False,
                                                  capture_output_if_no_pipes=True, timeout=5)
            if res_netsh and res_netsh.stdout:
                for line in res_netsh.stdout.splitlines():
                    line_lower = line.lower()
                    if line_lower.startswith("enabled") and ("connected" in line_lower or "dedicated" in line_lower):
                        parts = line.strip().split()
                        if len(parts) >= 4:
                            adapter_name = " ".join(parts[3:])
                            # Filter out common virtual/tunnel adapters
                            if not any(v_name in adapter_name.lower() for v_name in
                                       ["loopback", "isatap", "teredo", "vmware", "virtualbox", "hyper-v", "vpn",
                                        "bluetooth"]):
                                adapter_names_to_change.append(adapter_name)
        except Exception as e_netsh:
            print(f"    {Fore.RED}Error listing interfaces with netsh: {e_netsh}{Style.RESET_ALL}")
            return

    if not adapter_names_to_change:
        print(
            f"    {Fore.YELLOW}No suitable (enabled, connected, physical) network adapters found to change MAC address.{Style.RESET_ALL}")
        return

    print(
        f"    {Fore.CYAN}Found {len(adapter_names_to_change)} potential adapter(s): {', '.join(adapter_names_to_change)}{Style.RESET_ALL}")
    total_adapters_to_process = len(adapter_names_to_change)

    for idx, nic_name_orig in enumerate(adapter_names_to_change):
        nic_name = nic_name_orig.strip()  # Ensure no leading/trailing whitespace
        print_progress_bar(idx, total_adapters_to_process, prefix=f'    Processing {nic_name[:18]:<18}:',
                           suffix='Working...', length=25, color=Fore.BLUE)
        nic_reg_idx = get_nic_index_from_name_new(nic_name)

        if nic_reg_idx:
            reg_path = rf"{REG_KEY_BASE_MAC}\{nic_reg_idx.zfill(4)}"
            new_mac = generate_random_mac_value_new()

            # Disable adapter (PowerShell is more reliable)
            disable_cmd_ps = ['powershell', '-NoProfile', '-Command',
                              f"Disable-NetAdapter -Name \"{nic_name}\" -Confirm:$false"]
            _run_shell_command_simple(disable_cmd_ps, shell=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                                      timeout=10)
            time.sleep(2)  # Increased wait

            try:
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path, 0,
                                    winreg.KEY_SET_VALUE | winreg.KEY_WOW64_64KEY) as key:
                    winreg.SetValueEx(key, "NetworkAddress", 0, winreg.REG_SZ, new_mac)
                print(
                    f"\r    {Fore.CYAN}{nic_name:<25}{Style.RESET_ALL} → Reg updated to {Fore.GREEN}{format_mac_for_display_new(new_mac)}{Style.RESET_ALL}")
                changed_count += 1
            except FileNotFoundError:
                print(f"\r    {Fore.YELLOW}Registry key not found for {nic_name}. Skipping MAC set.{Style.RESET_ALL}")
            except PermissionError:
                print(
                    f"\r    {Fore.RED}Permission error for {nic_name} registry. Ensure admin rights.{Style.RESET_ALL}")
            except Exception as e_reg:
                print(f"\r    {Fore.RED}Error setting MAC in registry for {nic_name}: {e_reg}{Style.RESET_ALL}")
                # Attempt to re-enable even if reg write failed
                enable_cmd_ps = ['powershell', '-NoProfile', '-Command',
                                 f"Enable-NetAdapter -Name \"{nic_name}\" -Confirm:$false"]
                _run_shell_command_simple(enable_cmd_ps, shell=False, stdout=subprocess.DEVNULL,
                                          stderr=subprocess.DEVNULL, timeout=10)
                continue  # Skip to next adapter if error here

            # Enable adapter
            enable_cmd_ps = ['powershell', '-NoProfile', '-Command',
                             f"Enable-NetAdapter -Name \"{nic_name}\" -Confirm:$false"]
            _run_shell_command_simple(enable_cmd_ps, shell=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                                      timeout=10)
            time.sleep(3)  # Increased wait
        else:
            print(f"\r    {Fore.YELLOW}No registry index found for {nic_name}. Skipping.{Style.RESET_ALL}")
        # if idx < total_adapters_to_process - 1: print(' ' * 70, end='\r') # Clear line for next progress
    print_progress_bar(total_adapters_to_process, total_adapters_to_process, prefix=f'    Processing Adapters:',
                       suffix='Done!    ', length=25, color=Fore.BLUE)

    if changed_count > 0:
        print(
            f"{Fore.GREEN}[✓] {changed_count} MAC address(es) randomized in registry. A RESTART IS CRITICAL for changes to apply.{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}[!] No MAC addresses were changed.{Style.RESET_ALL}")


# --- Roblox Install function (INTEGRATED LATEST DOWNLOADER) ---
def get_latest_roblox_installer_url():
    """
    Fetches the latest Roblox WindowsPlayer version hash and constructs the download URL.
    Returns the URL string or None if an error occurs.
    """
    live_txt_url = "https://raw.githubusercontent.com/bluepilledgreat/Roblox-DeployHistory-Tracker/main/LIVE.txt"
    default_fallback_url = "https://www.roblox.com/download/client"  # Keep a defined fallback
    try:
        print(f"    {Fore.CYAN}Fetching latest Roblox version information...{Style.RESET_ALL}")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(live_txt_url, timeout=15, headers=headers)
        response.raise_for_status()
        content = response.text

        match = re.search(r"^WindowsPlayer:\s*(version-[a-f0-9]{32})\s*\[.*\]", content, re.MULTILINE | re.IGNORECASE)
        if not match:  # Try slightly more flexible hash length
            match = re.search(r"^WindowsPlayer:\s*(version-[a-f0-9]{16,})\s*\[.*\]", content,
                              re.MULTILINE | re.IGNORECASE)

        if match:
            version_hash = match.group(1)
            if "version-" in version_hash and len(version_hash) > (len("version-") + 10):  # Basic sanity for hash part
                installer_url = f"https://setup.rbxcdn.com/{version_hash}-Roblox.exe"
                print(
                    f"    {Fore.GREEN}Constructed latest Roblox installer URL using hash: {version_hash}{Style.RESET_ALL}")
                return installer_url
            else:
                print(f"    {Fore.YELLOW}Extracted version hash '{version_hash}' seems invalid.{Style.RESET_ALL}")
                return default_fallback_url  # Fallback if hash is weird
        else:
            print(
                f"    {Fore.YELLOW}Could not find WindowsPlayer version hash in fetched data. Using fallback.{Style.RESET_ALL}")
            return default_fallback_url
    except requests.exceptions.Timeout:
        print(f"    {Fore.RED}Timeout fetching Roblox version data. Using fallback.{Style.RESET_ALL}")
        return default_fallback_url
    except requests.exceptions.RequestException as e:
        print(f"    {Fore.RED}Error fetching Roblox version data: {e}. Using fallback.{Style.RESET_ALL}")
        return default_fallback_url
    except Exception as e:
        print(f"    {Fore.RED}Unexpected error getting Roblox version: {e}. Using fallback.{Style.RESET_ALL}")
        return default_fallback_url


def install_roblox():
    print(f"\n{Fore.GREEN}[+] Installing Roblox...{Style.RESET_ALL}")

    installer_url = get_latest_roblox_installer_url()  # Attempt to get dynamic URL

    # Use a unique name for the installer in TEMP to avoid conflicts
    installer_filename = f"RobloxInstaller_{uuid.uuid4().hex[:8]}.exe"
    installer_path = os.path.join(os.environ.get('TEMP', '.'), installer_filename)

    if os.path.exists(installer_path):  # Clean up if somehow exists
        try:
            os.remove(installer_path)
        except Exception:
            pass  # Ignore errors removing old temp file

    # Check for cURL
    curl_exe_path = None
    curl_check_proc = _run_shell_command_simple(['where', 'curl'], shell=False, capture_output_if_no_pipes=True,
                                                timeout=3)
    if curl_check_proc and curl_check_proc.returncode == 0 and curl_check_proc.stdout:
        curl_exe_path = curl_check_proc.stdout.strip().splitlines()[0]  # Take the first one

    downloaded = False
    download_method = ""

    if curl_exe_path:
        print(f"    Attempting download with cURL from: {installer_url}")
        curl_command = [
            curl_exe_path, '-L',  # Follow redirects
            '-o', installer_path,
            '--silent', '--show-error',  # Silent but show errors
            '--retry', '3', '--retry-delay', '3',
            '--connect-timeout', '10', '--max-time', '90',  # Timeouts
            installer_url
        ]
        try:
            res = _run_shell_command_simple(curl_command, shell=False, check=False, timeout=95)  # Slightly > max-time
            if res and res.returncode == 0 and os.path.exists(installer_path) and os.path.getsize(
                    installer_path) > 1000000:  # Min 1MB
                downloaded = True
                download_method = "cURL"
                print(f"    {Fore.GREEN}Downloaded using cURL.{Style.RESET_ALL}")
            elif res:
                print(
                    f"    {Fore.YELLOW}cURL download failed. RC: {res.returncode}. Stderr: {res.stderr if res.stderr else 'N/A'}{Style.RESET_ALL}")
        except Exception as e_curl:
            print(f"    {Fore.RED}cURL execution error: {e_curl}{Style.RESET_ALL}")

    if not downloaded:
        fallback_reason = "cURL failed or unavailable" if curl_exe_path else "cURL not found"
        print(f"    Attempting download with Python requests ({fallback_reason}) from: {installer_url}")
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0'}
            r = requests.get(installer_url, stream=True, timeout=(10, 60), headers=headers)  # (connect, read)
            r.raise_for_status()
            with open(installer_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):  # Write in chunks
                    f.write(chunk)
            if os.path.exists(installer_path) and os.path.getsize(installer_path) > 1000000:  # Min 1MB
                downloaded = True
                download_method = "Python requests"
                print(f"    {Fore.GREEN}Downloaded using Python requests.{Style.RESET_ALL}")
        except requests.exceptions.HTTPError as e_http:
            print(
                f"    {Fore.RED}Requests HTTP error: {e_http.response.status_code} {e_http.response.reason}{Style.RESET_ALL}")
        except requests.exceptions.RequestException as e_req:
            print(f"    {Fore.RED}Requests download error: {e_req}{Style.RESET_ALL}")
        except Exception as e_generic:
            print(f"    {Fore.RED}Generic download error with requests: {e_generic}{Style.RESET_ALL}")

    if not downloaded:
        print(f"{Fore.RED}[!] Could not download Roblox installer from any source.{Style.RESET_ALL}")
        if os.path.exists(installer_path): os.remove(installer_path)  # Clean up partial
        return

    print(f"    Starting Roblox installation (silent mode expected)...")
    try:
        # Use CREATE_NO_WINDOW to avoid console flash from installer
        process = subprocess.Popen([installer_path, '/S'], creationflags=subprocess.CREATE_NO_WINDOW)
        print(
            f"    {Fore.CYAN}Roblox installer launched (PID: {process.pid}). Background installation initiated.{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}    Failed to start installer: {e}{Style.RESET_ALL}")
        if os.path.exists(installer_path): os.remove(installer_path)  # Clean up
        return

    # Estimated time for silent install
    estimated_install_seconds = 75
    print(
        f"    {Fore.YELLOW}Allowing approx. {estimated_install_seconds}s for background installation...{Style.RESET_ALL}")
    for i in range(estimated_install_seconds + 1):
        print_progress_bar(i, estimated_install_seconds, prefix='    Est. Install Progress:', suffix='Please wait...',
                           length=30, color=Fore.GREEN)
        time.sleep(1)

    # Verification
    versions_path = os.path.join(os.environ.get('LOCALAPPDATA', ''), "Roblox", "Versions")
    installed_ok = False
    print(f"\n    {Fore.CYAN}Verifying Roblox installation...{Style.RESET_ALL}")
    if os.path.exists(versions_path):
        try:
            time.sleep(3)  # Give a moment for files to finalize
            # Check newest version folder for RobloxPlayerBeta.exe
            version_folders = [os.path.join(versions_path, d) for d in os.listdir(versions_path) if
                               os.path.isdir(os.path.join(versions_path, d))]
            version_folders.sort(key=lambda x: os.path.getmtime(x), reverse=True)  # Newest first

            if version_folders:
                latest_version_folder = version_folders[0]
                player_exe_path = os.path.join(latest_version_folder, "RobloxPlayerBeta.exe")
                if os.path.exists(player_exe_path) and os.path.getsize(player_exe_path) > 1000000:  # Min 1MB
                    installed_ok = True
                    print(
                        f"    {Fore.GREEN}Found RobloxPlayerBeta.exe in {os.path.basename(latest_version_folder)}.{Style.RESET_ALL}")
            if not installed_ok:
                print(
                    f"    {Fore.YELLOW}RobloxPlayerBeta.exe not immediately verifiable in latest version folder.{Style.RESET_ALL}")
        except Exception as e_verify:
            print(
                f"    {Fore.YELLOW}Could not fully verify Roblox installation directory structure: {e_verify}{Style.RESET_ALL}")
    else:
        print(f"    {Fore.YELLOW}Roblox Versions directory not found post-install attempt.{Style.RESET_ALL}")

    if installed_ok:
        print(f"\n{Fore.GREEN}[✓] Roblox installation likely completed successfully.{Style.RESET_ALL}")
    else:
        print(
            f"\n{Fore.YELLOW}[!] Roblox installation initiated. Verification inconclusive or pending. Please check manually.{Style.RESET_ALL}")

    # Clean up downloaded installer
    if os.path.exists(installer_path):
        try:
            os.remove(installer_path)
            # print(f"    {Fore.CYAN}Cleaned up installer: {installer_path}{Style.RESET_ALL}")
        except Exception:
            # print(f"    {Fore.YELLOW}Warning: Could not clean up installer: {e_cleanup}{Style.RESET_ALL}")
            pass


# --- EDID, Hyperion Key, Focused SMBIOS functions (Retained & Adapted) ---
def get_current_user_sid_string():
    if PYWIN32_AVAILABLE:
        try:
            token = win32security.OpenProcessToken(win32api.GetCurrentProcess(), win32security.TOKEN_QUERY)
            user_sid_info = win32security.GetTokenInformation(token, win32security.TokenUser)
            return win32security.ConvertSidToStringSid(user_sid_info[0])
        except Exception as e:
            # print(f"{Fore.RED}    Error getting SID (pywin32): {e}{Style.RESET_ALL}") # Can be verbose
            pass  # Fall through to whoami
    # Fallback
    process = _run_shell_command_wrapper(['whoami', '/user', '/NH'], capture_output=True, shell=False, hide_window=True,
                                         timeout=5)  # /NH for No Header
    if process and process.stdout:
        match = re.search(r"(S-1-[0-9\-]+)", process.stdout.strip(), re.IGNORECASE)
        if match:
            return match.group(1)
    # print(f"{Fore.RED}    Could not parse SID from 'whoami /user'.{Style.RESET_ALL}") # Can be verbose
    return None


def calculate_edid_checksum(edid_data_bytes):
    if not edid_data_bytes or len(edid_data_bytes) < 128: return edid_data_bytes[-1] if edid_data_bytes else 0
    s = sum(edid_data_bytes[:127])
    return (256 - (s % 256)) % 256


def modify_monitor_edids():
    print(f"\n{Fore.BLUE}[+] Modifying Monitor EDID serials (if found)...{Style.RESET_ALL}")
    if not is_admin(): print(
        f"    {Fore.RED}Admin privileges required. Skipping EDID modification.{Style.RESET_ALL}"); return

    changed_count = 0
    monitors_processed = 0
    base_path = r"SYSTEM\CurrentControlSet\Enum\DISPLAY"
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, base_path, 0,
                            winreg.KEY_READ | winreg.KEY_WRITE | winreg.KEY_WOW64_64KEY) as display_key:
            m_idx = 0
            while True:  # Iterate monitor vendors
                try:
                    m_vendor = winreg.EnumKey(display_key, m_idx)
                    with winreg.OpenKey(display_key, m_vendor, 0,
                                        winreg.KEY_READ | winreg.KEY_WRITE | winreg.KEY_WOW64_64KEY) as vendor_k:
                        i_idx = 0
                        while True:  # Iterate instances
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
                                            block = m_edid[:128]  # Work on the first block
                                            # Randomize bytes 12-15 (often part of serial or mfg details)
                                            original_bytes = block[12:16]
                                            for i_sn in range(12, 16): block[i_sn] = random.randint(0, 255)

                                            if block[
                                               12:16] == original_bytes and monitors_processed > 1:  # Avoid re-randomizing to same if multiple monitors
                                                for i_sn in range(12, 16): block[i_sn] = random.randint(0,
                                                                                                        255)  # Try again

                                            block[127] = calculate_edid_checksum(block)
                                            if bytes(block) != edid_val[:128]:  # Only write if changed
                                                m_edid[:128] = block
                                                winreg.SetValueEx(dev_k, "EDID", 0, reg_t, bytes(m_edid))
                                                print(
                                                    f"    {Fore.GREEN}Modified EDID for: {m_vendor}\\{m_instance}{Style.RESET_ALL}")
                                                changed_count += 1
                                            else:
                                                print(
                                                    f"    {Fore.YELLOW}EDID for {m_vendor}\\{m_instance} already randomized or no change needed.{Style.RESET_ALL}")
                                except FileNotFoundError:
                                    pass  # EDID value or Device Parameters not found
                                except Exception:
                                    pass  # Other errors processing specific EDID
                                i_idx += 1
                            except OSError:
                                break  # No more instances
                    m_idx += 1
                except OSError:
                    break  # No more vendors
    except FileNotFoundError:
        print(f"    {Fore.YELLOW}Base display registry path not found. Skipping.{Style.RESET_ALL}")
    except Exception as e_base_edid:
        print(f"    {Fore.RED}Error accessing display registry for EDID: {e_base_edid}{Style.RESET_ALL}")

    if changed_count > 0:
        print(f"{Fore.GREEN}[✓] {changed_count} monitor EDID(s) modified. RESTART REQUIRED.{Style.RESET_ALL}")
    elif monitors_processed > 0:
        print(
            f"{Fore.YELLOW}[!] Found {monitors_processed} monitor(s), but no EDIDs were changed (or changes were identical).{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}[!] No monitor EDIDs found or modified.{Style.RESET_ALL}")


def manage_hyperion_system_reg_key():
    print(f"\n{Fore.BLUE}[+] Managing Hyperion's 'SystemReg' key (if present)...{Style.RESET_ALL}")
    if not is_admin(): print(f"    {Fore.RED}Admin privileges required. Skipping.{Style.RESET_ALL}"); return

    user_sid = get_current_user_sid_string()
    if not user_sid: print(
        f"    {Fore.RED}[!] No user SID found. Skipping SystemReg key management.{Style.RESET_ALL}"); return

    val_name_to_delete = "\0SystemReg"  # Null-prefixed value name
    deleted_key = False
    # Path: HKEY_USERS\<User SID>\SYSTEM\CurrentControlSet\Control
    # Value Name: \0SystemReg (REG_BINARY)
    reg_path_under_sid = r"SYSTEM\CurrentControlSet\Control"

    paths_to_check = [
        (winreg.HKEY_CURRENT_USER, reg_path_under_sid, "HKCU (effective)"),  # For current user context
        (winreg.HKEY_USERS, rf"{user_sid}\{reg_path_under_sid}", f"HKU\\{user_sid}")  # Direct SID path
    ]

    for hkey_root, full_reg_path_str, alias in paths_to_check:
        try:
            # Open with KEY_SET_VALUE for deletion, KEY_READ to check existence first (optional)
            with winreg.OpenKey(hkey_root, full_reg_path_str, 0,
                                winreg.KEY_READ | winreg.KEY_SET_VALUE | winreg.KEY_WOW64_64KEY) as key:
                try:
                    # Check if value exists before attempting delete to avoid FileNotFoundError log
                    winreg.QueryValueEx(key, val_name_to_delete)  # This will raise FileNotFoundError if not present
                    winreg.DeleteValue(key, val_name_to_delete)
                    print(
                        f"    {Fore.GREEN}Deleted '{repr(val_name_to_delete)}' from {alias}\\{full_reg_path_str}{Style.RESET_ALL}")
                    deleted_key = True
                    # If found and deleted in one place (e.g. HKCU), it's likely the same as HKU\\<SID> for current user
                    # Break if you only expect one instance or want to avoid redundant checks for the current user.
                    # For now, let it check both specified paths.
                except FileNotFoundError:
                    print(f"    '{repr(val_name_to_delete)}' not found in {alias}\\{full_reg_path_str}.")
                except Exception as e_del_val:
                    print(
                        f"    {Fore.RED}Error deleting value from {alias}\\{full_reg_path_str}: {e_del_val}{Style.RESET_ALL}")
        except FileNotFoundError:
            print(f"    Registry path {alias}\\{full_reg_path_str} itself not found.")
        except Exception as e_open_outer:
            print(f"    {Fore.RED}Error opening key {alias}\\{full_reg_path_str}: {e_open_outer}{Style.RESET_ALL}")

    if deleted_key:
        print(f"{Fore.GREEN}[✓] Hyperion 'SystemReg' key managed (deleted where found).{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}[!] Hyperion 'SystemReg' key not found in checked locations.{Style.RESET_ALL}")


def download_amidewin_tools():
    print(f"\n{Fore.BLUE}[+] Downloading AMIDEWIN tools for SMBIOS...{Style.RESET_ALL}")
    all_downloaded = True
    os.makedirs(AMIDEWIN_DIR_HWID, exist_ok=True)  # Ensure Fonts dir exists (it always should)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0'}
    total_tools = len(AMIDEWIN_TOOLS_MAP)

    for i, (dest_path, url) in enumerate(AMIDEWIN_TOOLS_MAP.items()):
        file_desc = os.path.basename(dest_path)
        print_progress_bar(i, total_tools, prefix='    Downloading:', suffix=f'{file_desc[:20]:<20}', length=30,
                           color=Fore.BLUE)
        time.sleep(0.05)  # For visual
        try:
            if os.path.exists(dest_path) and os.path.getsize(
                    dest_path) > 10000:  # Skip if already exists and reasonable size
                # print(f"\n    {Fore.GREEN}{file_desc} already exists. Skipping.{Style.RESET_ALL}")
                continue
            r = requests.get(url, stream=True, timeout=30, headers=headers, allow_redirects=True)
            r.raise_for_status()
            with open(dest_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192): f.write(chunk)
            if not (os.path.exists(dest_path) and os.path.getsize(dest_path) > 10000):  # Re-check size
                raise Exception(f"{file_desc} downloaded but seems too small.")
        except requests.exceptions.RequestException as e_req:
            print(f"\n    {Fore.RED}Failed to download {file_desc}: {e_req}{Style.RESET_ALL}")
            all_downloaded = False
        except Exception as e_other:
            print(f"\n    {Fore.RED}Error with {file_desc}: {e_other}{Style.RESET_ALL}")
            all_downloaded = False
    print_progress_bar(total_tools, total_tools, prefix='    Downloading:', suffix='Done!                ', length=30,
                       color=Fore.BLUE)
    if all_downloaded:
        print(f"{Fore.GREEN}[✓] AMIDEWIN tools downloaded/verified successfully.{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}[!] Failed to download one or more AMIDEWIN tools.{Style.RESET_ALL}")
    return all_downloaded


def delete_amidewin_tools():
    print(f"\n{Fore.BLUE}[+] Deleting AMIDEWIN tools...{Style.RESET_ALL}")
    deleted_any = False
    total_to_del = len(AMIDEWIN_FILES_TO_DELETE)
    for i, file_path in enumerate(AMIDEWIN_FILES_TO_DELETE):
        print_progress_bar(i, total_to_del, prefix='    Deleting:', suffix=f'{os.path.basename(file_path)[:20]:<20}',
                           length=30, color=Fore.RED)
        time.sleep(0.05)
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                deleted_any = True
            except Exception as e:
                print(f"\n    {Fore.RED}Failed to delete {file_path}: {e}{Style.RESET_ALL}")
    print_progress_bar(total_to_del, total_to_del, prefix='    Deleting:', suffix='Done!                ', length=30,
                       color=Fore.RED)

    if deleted_any:
        print(f"{Fore.GREEN}[✓] AMIDEWIN tools deleted.{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}[!] AMIDEWIN tools not found for deletion or an error occurred.{Style.RESET_ALL}")


def generate_random_short_alphanumeric_serial(length=12):  # Increased default length
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))


def generate_uuid_string():  # For /SU
    return str(uuid.uuid4()).upper()


def spoof_smbios_with_amidewin_focused():
    print(f"\n{Fore.BLUE}[+] Spoofing key SMBIOS fields with AMIDEWIN (primarily System UUID)...{Style.RESET_ALL}")
    exe_path = os.path.join(AMIDEWIN_DIR_HWID, "AMIDEWINx64.EXE")
    if not os.path.exists(exe_path):
        print(f"    {Fore.RED}AMIDEWINx64.EXE not found at '{exe_path}'. Skipping SMBIOS spoofing.{Style.RESET_ALL}")
        return False  # Indicate failure

    # Focus on System UUID (/SU Auto) as per Hyperion's main hash.
    # Other SMBIOS fields can be added if specific needs arise, but keep it targeted.
    ami_commands_to_run = {
        "/SU": "Auto",  # System UUID - Generate a new one automatically by BIOS/AMIDEWIN.
        # Optional: Baseboard Serial, System Serial if they are also found to be part of critical hashes
        # "/BS": generate_random_short_alphanumeric_serial(15), # Baseboard Serial
        # "/SS": generate_random_short_alphanumeric_serial(15), # System Serial
    }
    print(
        f"    {Fore.CYAN}Targeting System UUID with AMIDEWIN (/SU Auto). Other SMBIOS fields are optional.{Style.RESET_ALL}")

    commands_issued_count = 0
    success_count = 0
    total_cmds = len(ami_commands_to_run)

    for i, (param, value) in enumerate(ami_commands_to_run.items()):
        actual_value = value
        if value == "Auto":  # /SU Auto
            pass  # No need to generate, AMIDEWIN handles it
        elif param == "/BS" or param == "/SS":  # Example for if we add other serials
            actual_value = generate_random_short_alphanumeric_serial(random.randint(10, 20))

        print_progress_bar(i, total_cmds, prefix='    SMBIOS Update:', suffix=f'{param} {actual_value[:10]}...',
                           length=30, color=Fore.BLUE)
        cmd_result = _run_shell_command_wrapper(
            [exe_path, param, actual_value],  # AMIDEWIN uses the value directly for "Auto" too
            cwd=AMIDEWIN_DIR_HWID,  # Run from where drivers are
            hide_window=True, shell=False, capture_output=True, timeout=15
        )
        time.sleep(0.25)  # Brief pause
        commands_issued_count += 1

        if cmd_result and cmd_result.returncode == 0:
            # AMIDEWIN often returns 0. True success is hard to verify without reading back.
            success_count += 1
        elif cmd_result:
            print(
                f"\n    {Fore.YELLOW}AMIDEWIN '{param} {actual_value}' may have issues. RC: {cmd_result.returncode}. Stderr: {cmd_result.stderr.strip() if cmd_result.stderr else 'N/A'}{Style.RESET_ALL}")
        else:  # cmd_result is None
            print(f"\n    {Fore.RED}Failed to execute AMIDEWIN command '{param} {actual_value}'.{Style.RESET_ALL}")

    print_progress_bar(total_cmds, total_cmds, prefix='    SMBIOS Update:', suffix='Commands Sent!     ', length=30,
                       color=Fore.BLUE)

    if commands_issued_count > 0:
        print(
            f"{Fore.GREEN}    AMIDEWIN commands for focused SMBIOS spoofing issued ({success_count}/{commands_issued_count} reported success by tool).{Style.RESET_ALL}")
        print(
            f"{Fore.YELLOW}    Note: Actual change depends on BIOS compatibility. RESTART IS CRITICAL.{Style.RESET_ALL}")
        return True
    else:
        print(
            f"{Fore.YELLOW}    No AMIDEWIN SMBIOS commands were successfully issued or an error occurred before execution.{Style.RESET_ALL}")
        return False


def restart_wmi_service():
    print(f"\n{Fore.BLUE}[+] Restarting WMI service (winmgmt)...{Style.RESET_ALL}")
    if not is_admin(): print(f"    {Fore.RED}Admin rights needed. Skipping WMI restart.{Style.RESET_ALL}"); return

    print(
        f"    {Fore.YELLOW}Stopping WMI service... (This might take a moment or show errors if dependencies are tight){Style.RESET_ALL}")
    _run_shell_command_wrapper(["net", "stop", "winmgmt", "/y"], shell=False, hide_window=True, timeout=45)
    time.sleep(3)  # Allow time for service to fully stop

    print(f"    {Fore.YELLOW}Starting WMI service...{Style.RESET_ALL}")
    _run_shell_command_wrapper(["net", "start", "winmgmt"], shell=False, hide_window=True,
                               timeout=45)  # /y not for start
    time.sleep(1)  # Pause for service to initialize
    # Verify if running
    sc_query_res = _run_shell_command_simple(['sc', 'query', 'winmgmt'], shell=False, capture_output_if_no_pipes=True,
                                             timeout=5)
    if sc_query_res and sc_query_res.stdout and "RUNNING" in sc_query_res.stdout.upper():
        print(f"{Fore.GREEN}    WMI service (winmgmt) is running.{Style.RESET_ALL}")
    else:
        print(
            f"{Fore.YELLOW}    WMI service (winmgmt) status uncertain after restart attempt. Check services.msc.{Style.RESET_ALL}")
    print(f"{Fore.GREEN}[✓] WMI service restart commands issued.{Style.RESET_ALL}")


def perform_focused_hwid_spoof():
    print(f"\n{Fore.MAGENTA}{'=' * 10} Initiating Focused HWID Spoofing (SMBIOS UUID) {'=' * 10}{Style.RESET_ALL}")
    if not is_admin(): print(
        f"    {Fore.RED}Admin rights needed. Skipping focused HWID spoof.{Style.RESET_ALL}"); return

    # Cosmetic delays removed from original user code for this version
    print(f"    {Fore.CYAN}Spoofing core system identifiers (System UUID via AMIDEWIN)...{Style.RESET_ALL}")

    if not download_amidewin_tools():
        print(f"    {Fore.RED}[!] Failed to download AMIDEWIN tools. Aborting SMBIOS spoofing step.{Style.RESET_ALL}")
        return  # Critical for this step

    spoof_smbios_with_amidewin_focused()  # This only targets /SU Auto now
    delete_amidewin_tools()  # Clean up tools

    restart_wmi_service()  # Restart WMI after SMBIOS potentially changed
    time.sleep(2)  # Pause for WMI to stabilize

    print(f"\n{Fore.GREEN}[✓] Focused SMBIOS HWID spoofing attempt (System UUID) completed.{Style.RESET_ALL}")
    print(f"    {Fore.YELLOW}A system RESTART is CRITICAL for these changes to be fully effective.{Style.RESET_ALL}")


# --- Main Operation Sequence ---
def perform_all_spoofing_operations():
    print(f"{Fore.BLUE}[+] Checking internet connection...{Style.RESET_ALL}")
    try:
        requests.get("https://1.1.1.1", timeout=5)  # Quick check to Cloudflare DNS
        print(f"{Fore.GREEN}[✓] Internet connection detected.{Style.RESET_ALL}")
    except requests.exceptions.RequestException:
        print(f"{Fore.RED}[!] No internet connection detected.{Style.RESET_ALL}")
        if input("    Continue anyway? (y/n): ").lower() != 'y': return False

    delete_roblox_cookies()
    uninstall_roblox()
    change_mac_address()  # General network identifier

    print(f"\n{Fore.YELLOW}[+] Pausing for network adapters to stabilize...{Style.RESET_ALL}")
    stabilize_time = 7  # Adjusted pause
    for i in range(stabilize_time):
        print_progress_bar(i + 1, stabilize_time, prefix='    Stabilizing Network:', suffix='Wait', length=30,
                           color=Fore.YELLOW)
        time.sleep(1)
    print(f"\n    {Fore.GREEN}Network stabilization period complete.{Style.RESET_ALL}")

    # HWID Spoofing based on Hyperion analysis focus
    modify_monitor_edids()  # Targets EDID Serial (Third Hash component in some analyses)
    manage_hyperion_system_reg_key()  # Targets SystemReg (Fourth Hash component)
    perform_focused_hwid_spoof()  # Targets System UUID (First Hash component)

    install_roblox()  # Reinstall Roblox with latest version

    print(f"\n{Fore.GREEN}{Style.BRIGHT}{'=' * 80}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}{Style.BRIGHT}[✓] All spoofing and Roblox reinstall operations completed!{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{Style.BRIGHT}[CRITICAL] A FULL SYSTEM RESTART IS STRONGLY RECOMMENDED NOW!{Style.RESET_ALL}")
    print(
        f"{Fore.YELLOW}    This is essential for many HWID changes (MAC, EDID, SMBIOS UUID) to take full effect.{Style.RESET_ALL}")
    print(f"{Fore.GREEN}{Style.BRIGHT}{'=' * 80}{Style.RESET_ALL}")
    return True


# --- Main Execution ---
def main():
    if os.name == 'nt':
        set_terminal_transparency(alpha_percentage=75)  # Set to 37% transparent

    os.system('cls')
    # time.sleep(0.05) # Tiny delay for transparency if needed
    print(f"{Fore.CYAN}{BANNER}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{Style.BRIGHT}{'=' * 80}{Style.RESET_ALL}")
    print(
        f"{Fore.WHITE}{Style.BRIGHT}Nitaybl's ByGone Spoofer (Focused Hyperion Mode - Dynamic Install){Style.RESET_ALL}")
    print(f"{Fore.CYAN}Version: Focused HWID - UUID, EDID, SystemReg - v2.1{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{Style.BRIGHT}{'=' * 80}{Style.RESET_ALL}\n")

    if not is_admin():
        print(f"{Fore.RED}[!] Admin privileges required. Attempting to restart with admin rights...{Style.RESET_ALL}")
        time.sleep(0.75)
        restart_with_admin()  # This function calls sys.exit()
        # If UAC is denied, restart_with_admin will have exited.
        # The script shouldn't continue here without admin.
        # For safety, one final check, though theoretically unreachable if UAC denied.
        if not is_admin():
            print(f"{Fore.RED}[FATAL] Failed to acquire admin privileges after UAC. Exiting.{Style.RESET_ALL}")
            input("\nPress Enter to exit...")
            sys.exit(1)

    print(f"{Fore.GREEN}[✓] Running as administrator.{Style.RESET_ALL}")
    time.sleep(0.5)

    if not PYWIN32_AVAILABLE:
        print(f"{Fore.YELLOW}Warning: pywin32 library not available.{Style.RESET_ALL}")
        print(f"         Hyperion SystemReg key management (SID part) will rely on 'whoami /user'.{Style.RESET_ALL}")
        # No need to ask for continuation, functions will try to fallback or skip.
        time.sleep(0.5)

    print(f"\n{Fore.LIGHTBLUE_EX}This script will attempt the following for Hyperion/Byfron:{Style.RESET_ALL}")
    print(f"  - {Fore.CYAN}Clean Roblox data & Uninstall existing Roblox.{Style.RESET_ALL}")
    print(f"  - {Fore.CYAN}Randomize MAC Addresses.{Style.RESET_ALL}")
    print(f"  - {Fore.CYAN}Modify Monitor EDID Serials.{Style.RESET_ALL}")
    print(f"  - {Fore.CYAN}Manage Hyperion's 'SystemReg' registry key.{Style.RESET_ALL}")
    print(f"  - {Fore.CYAN}Spoof System UUID (via AMIDEWIN).{Style.RESET_ALL}")
    print(f"  - {Fore.CYAN}Install the LATEST version of Roblox.{Style.RESET_ALL}")
    print(
        f"{Fore.RED}\n  NOTE: RAM serial spoofing (another potential vector) is NOT performed by this script's AMIDEWIN usage.{Style.RESET_ALL}")
    print(
        f"{Fore.YELLOW}{Style.BRIGHT}\n  DISCLAIMER: Use at your own risk. No guarantees against detection. RESTART is crucial.{Style.RESET_ALL}")

    if input("\nDo you understand and wish to proceed? (yes/no): ").strip().lower() == 'yes':
        try:
            start_time = time.time()
            perform_all_spoofing_operations()
            end_time = time.time()
            print(f"\n{Fore.CYAN}Total script execution time: {end_time - start_time:.2f} seconds.{Style.RESET_ALL}")
        except SystemExit:  # Handles sys.exit() calls from restart_with_admin or other critical points
            print(f"\n{Fore.YELLOW}Script execution was exited.{Style.RESET_ALL}")
        except KeyboardInterrupt:
            print(f"\n\n{Fore.YELLOW}User interrupted the script. Exiting...{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}{Style.BRIGHT}\n\nAn UNEXPECTED CRITICAL ERROR occurred: {e}{Style.RESET_ALL}")
            import traceback
            print(f"{Fore.RED}Full Traceback:{Style.RESET_ALL}")
            traceback.print_exc()
            print(f"{Fore.RED}If this issue persists, please report it.{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}Operation cancelled by the user.{Style.RESET_ALL}")
    input("\nPress Enter to exit...")


if __name__ == "__main__":
    main()
# Copyright (c) 2025 nitaybl. All Rights Reserved.
