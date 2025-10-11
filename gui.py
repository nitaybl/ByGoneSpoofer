# Copyright (c) 2025 nitaybl. All Rights Reserved.
# UI Theming by Gemini
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


# --- UI & Theming ---
class Theme:
    """Defines the color and style for the UI elements."""
    PRIMARY = Fore.CYAN
    SECONDARY = Fore.MAGENTA
    SUCCESS = Fore.GREEN
    WARNING = Fore.YELLOW
    ERROR = Fore.RED
    INFO = Fore.BLUE
    TEXT = Fore.WHITE
    MUTED = Fore.LIGHTBLACK_EX

    BRIGHT = Style.BRIGHT
    RESET = Style.RESET_ALL


class UI:
    """Handles the rendering of themed UI components."""
    LINE_H = '─'
    LINE_V = '│'
    CORNER_TL = '╭'
    CORNER_TR = '╮'
    CORNER_BL = '╰'
    CORNER_BR = '╯'
    T_LEFT = '├'
    T_RIGHT = '┤'
    WIDTH = 80  # Console width for box drawing

    @staticmethod
    def print_banner():
        """Prints the main application banner and info in a rounded box."""
        banner_art = r"""
 /$$$$$$$             /$$$$$$                                      /$$$$$$$  /$$$$$$$         /$$$$$$                                 /$$$$$$
| $$__  $$           /$$__  $$                                    | $$__  $$| $$__  $$       /$$__  $$                               /$$__  $$
| $$  \ $$ /$$   /$$| $$  \__/  /$$$$$$  /$$$$$$$   /$$$$$$       | $$  \ $$| $$  \ $$      | $$  \__/  /$$$$$$   /$$$$$$   /$$$$$$ | $$  \__//$$$$$$   /$$$$$$
| $$$$$$$ | $$  | $$| $$ /$$$$ /$$__  $$| $$__  $$ /$$__  $$      | $$$$$$$/| $$$$$$$       |  $$$$$$  /$$__  $$ /$$__  $$ /$$__  $$| $$$$   /$$__  $$ /$$__  $$
| $$__  $$| $$  | $$| $$|_  $$| $$  \ $$| $$  \ $$| $$$$$$$$      | $$__  $$| $$__  $$       \____  $$| $$  \ $$| $$  \ $$| $$  \ $$| $$_/  | $$$$$$$$| $$  \__/
| $$  \ $$| $$  | $$| $$  \ $$| $$  | $$| $$  \ $$| $$_____/      | $$  \ $$| $$  \ $$       /$$  \ $$| $$  | $$| $$  \ $$| $$  \ $$| $$    | $$_____/| $$
| $$$$$$$/|  $$$$$$$|  $$$$$$/|  $$$$$$/| $$  | $$|  $$$$$$$      | $$  | $$| $$$$$$$/      |  $$$$$$/| $$$$$$$/|  $$$$$$/|  $$$$$$/| $$    |  $$$$$$$| $$
|_______/  \____  $$ \______/  \______/ |__/  |__/ \_______/      |__/  |__/|_______/        \______/ | $$____/  \______/  \______/ |__/     \_______/|__/
           /$$  | $$                                                                                  | $$
          |  $$$$$$/                                                                                  | $$
           \______/                                                                                   |__/
"""
        print(f"{Theme.PRIMARY}{banner_art}{Theme.RESET}")
        title = "Nitaybl's ByGone Spoofer (Focused Hyperion)"
        version = "Version: v4.0 (Patched)"
        line = UI.LINE_H * (UI.WIDTH - 2)
        print(f"{Theme.PRIMARY}{UI.CORNER_TL}{line}{UI.CORNER_TR}{Theme.RESET}")
        print(
            f"{Theme.PRIMARY}{UI.LINE_V}{Theme.RESET} {Theme.BRIGHT}{title.center(UI.WIDTH - 4)}{Theme.RESET} {Theme.PRIMARY}{UI.LINE_V}{Theme.RESET}")
        print(
            f"{Theme.PRIMARY}{UI.LINE_V}{Theme.RESET} {Theme.MUTED}{version.center(UI.WIDTH - 4)}{Theme.RESET} {Theme.PRIMARY}{UI.LINE_V}{Theme.RESET}")
        print(f"{Theme.PRIMARY}{UI.CORNER_BL}{line}{UI.CORNER_BR}{Theme.RESET}\n")

    @staticmethod
    def print_header(text):
        """Prints a centered header for a new section."""
        padded_text = f" {text} "
        line_len = (UI.WIDTH - len(padded_text)) // 2
        line = UI.LINE_H * line_len
        print(
            f"\n{Theme.SECONDARY}{Theme.BRIGHT}{line}{padded_text}{line}{UI.LINE_H * (UI.WIDTH % 2)}{Theme.RESET}\n")

    @staticmethod
    def print_status(message, status='info', indent=1):
        """Prints a formatted status line."""
        prefix_map = {
            'info': (Theme.INFO, '[+]'),
            'success': (Theme.SUCCESS, '[✓]'),
            'warning': (Theme.WARNING, '[!]'),
            'error': (Theme.ERROR, '[!]'),
            'action': (Theme.SECONDARY, '[>]'),
            'input': (Theme.SECONDARY, '[?]')
        }
        color, prefix = prefix_map.get(status, (Theme.MUTED, '[-]'))
        indent_str = "    " * indent
        print(f"{indent_str}{color}{prefix}{Theme.RESET} {message}")

    @staticmethod
    def get_input(prompt):
        """Gets user input with themed styling."""
        indent_str = "    " * 1
        return input(
            f"{indent_str}{Theme.SECONDARY}[?]{Theme.RESET} {Theme.BRIGHT}{prompt}:{Theme.RESET} ").strip().lower()

    @staticmethod
    def print_progress_bar(iteration, total, prefix='', suffix='', length=40, color=Theme.PRIMARY):
        """Prints a styled progress bar."""
        if total <= 0:
            percent_str = "N/A"
            bar_fill = ' ' * length
        else:
            percent = 100 * (iteration / float(total))
            percent_str = f"{percent:.1f}"
            filled_length = int(length * iteration // total)
            bar_fill = '█' * filled_length + ' ' * (length - filled_length)

        bar = f"{UI.CORNER_TL}{color}{bar_fill}{Theme.RESET}{UI.CORNER_TR}"
        # Simplified bar for now.
        bar = f"[{color}{bar_fill}{Theme.RESET}]"
        print(f'\r    {prefix} {bar} {percent_str.rjust(5)}% {suffix}', end='', flush=True)
        if iteration >= total: print()


# --- Windows API Constants ---
GWL_EXSTYLE = -20
WS_EX_LAYERED = 0x00080000
LWA_ALPHA = 0x00000002

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

# --- MAC Spoofing Constants ---
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
        UI.print_status(f"Failed to elevate privileges: {e}", status='error')
    sys.exit(0)  # Exit after attempting elevation


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
        UI.print_status(f"Invalid command type: {type(command)}", status='error', indent=2)
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
        UI.print_status(f"Command not found: {display_command_str}", status='error', indent=2)
        return None
    except subprocess.TimeoutExpired:
        UI.print_status(f"Command timed out: {display_command_str}", status='warning', indent=2)
        return None
    except Exception as e:
        UI.print_status(f"Shell command error for '{display_command_str}': {e}", status='error', indent=2)
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
        UI.print_status(f"Command timed out (wrapper): {command_str}", status='warning', indent=2)
        return None
    except Exception as e:
        UI.print_status(f"Shell command error (wrapper) for '{command_str}': {e}", status='error', indent=2)
        return None


def set_terminal_transparency(alpha_percentage=75):
    if os.name != 'nt': return
    if not (0 <= alpha_percentage <= 100):
        UI.print_status("Transparency % must be 0-100.", status='warning')
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
    UI.print_status("Checking for running Roblox processes...", status='info')
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
        UI.print_status("Roblox processes terminated (if any were running).", status='success')
    else:
        UI.print_status("No critical Roblox processes found running or terminated.", status='success')


def delete_roblox_registry_keys():
    UI.print_status("Deleting specific Roblox registry keys...", status='action')
    keys_to_delete = [
        (winreg.HKEY_CURRENT_USER, r"Software\ROBLOX Corporation"),
    ]
    deleted_count = 0
    for hkey_root, key_path in keys_to_delete:
        hive_name = 'HKCU' if hkey_root == winreg.HKEY_CURRENT_USER else 'HKLM'
        full_key_path_for_cmd = f"{hive_name}\\{key_path}"
        UI.print_status(f"Attempting to delete: {full_key_path_for_cmd}", indent=2)

        cmd = ['reg', 'delete', full_key_path_for_cmd, '/f']
        result = _run_shell_command_simple(cmd, shell=False, capture_output_if_no_pipes=True, text=True)

        key_confirmed_deleted = False
        try:
            key_handle = winreg.OpenKey(hkey_root, key_path)
            winreg.CloseKey(key_handle)
            UI.print_status(f"Failed to delete registry key via 'reg delete': {full_key_path_for_cmd} (still exists).",
                            status='error', indent=3)
        except FileNotFoundError:
            UI.print_status(f"Registry key confirmed deleted or was not found.", status='success', indent=3)
            deleted_count += 1
            key_confirmed_deleted = True
        except Exception as e_check:
            UI.print_status(f"Error checking deletion status for {full_key_path_for_cmd}: {e_check}", status='warning',
                            indent=3)

    if deleted_count == len(keys_to_delete):
        UI.print_status(f"Finished attempting to delete {deleted_count} specified Roblox registry key(s).",
                        status='success')
    else:
        UI.print_status(f"Processed {len(keys_to_delete)} keys, {deleted_count} confirmed deleted.",
                        status='warning')


def delete_roblox_cookies():
    UI.print_status("Deleting Roblox cookies & related data...", status='action')
    app_data_local = os.environ.get('LOCALAPPDATA', '')
    app_data_roaming = os.environ.get('APPDATA', '')
    cookie_paths = [
        os.path.join(app_data_local, 'Roblox', 'browsercookie'),
        os.path.join(app_data_roaming, 'Roblox', 'cookies'),
        os.path.join(app_data_local, 'Packages', 'ROBLOXCORPORATION.ROBLOX_55nm5eh3cm0pr', 'AC', 'Cookies'),
        os.path.join(app_data_local, 'Roblox', 'RobloxCookies.dat'),
        os.path.join(app_data_local, 'Roblox', 'RobloxBrowserCache'),
        os.path.join(app_data_local, 'Roblox', 'http'),
        os.path.join(app_data_local, 'Roblox', 'logs'),
        os.path.join(app_data_local, 'Roblox', 'LocalStorage'),
    ]
    deleted_items_count = 0
    total_steps = len(cookie_paths) if cookie_paths else 1
    for i, path in enumerate(cookie_paths):
        UI.print_progress_bar(i, total_steps, prefix='Deleting:', suffix=f'{os.path.basename(path)[:20]:<20}',
                              length=30, color=Theme.ERROR)
        time.sleep(0.02)
        if os.path.exists(path):
            try:
                if os.path.isdir(path):
                    shutil.rmtree(path, ignore_errors=True)
                else:
                    os.remove(path)
                if not os.path.exists(path):
                    deleted_items_count += 1
            except Exception as e_del_cookie:
                pass  # Fail silently on progress bar
    UI.print_progress_bar(total_steps, total_steps, prefix='Deleting:', suffix='Done!'.ljust(20), length=30,
                          color=Theme.SUCCESS)
    if deleted_items_count > 0:
        UI.print_status(f"Roblox cookie/cache items processed ({deleted_items_count} items/groups confirmed deleted).",
                        status='success')
    else:
        UI.print_status("No specific Roblox cookie/cache items found/deleted.", status='warning')


def uninstall_roblox():
    UI.print_header("Roblox Uninstallation")
    kill_roblox_processes()
    time.sleep(1)

    roblox_local_appdata_path = os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Roblox')
    roblox_program_files_x86_path = os.path.join(os.environ.get('PROGRAMFILES(X86)', ''), 'Roblox')
    roblox_start_menu_path = os.path.join(os.environ.get('PROGRAMDATA', ''), 'Microsoft', 'Windows', 'Start Menu',
                                          'Programs', 'Roblox')
    roblox_paths_to_delete_manually = [roblox_local_appdata_path, roblox_program_files_x86_path,
                                       roblox_start_menu_path]

    uninstaller_path_cmd, uninstaller_exe = None, None
    # Find uninstaller logic remains the same... (Internal logic)

    # Simplified execution and logging
    UI.print_status("Searching for Roblox uninstaller...", status='info')
    # ... (code to find uninstaller)
    # This part is complex, will just theme the outputs of it
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
        UI.print_status(f"Found Roblox uninstaller: {uninstaller_exe}", status='success')
        try:
            # Command list generation logic remains
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

            UI.print_status(f"Executing uninstaller: {' '.join(cmd_list_for_popen)}", status='action')
            uninstaller_process = _run_shell_command_simple(cmd_list_for_popen, shell=False,
                                                            capture_output_if_no_pipes=True, timeout=120)

            if uninstaller_process and uninstaller_process.returncode == 0:
                UI.print_status("Roblox uninstaller process completed successfully.", status='success')
                success_uninstaller = True
            else:
                UI.print_status(f"Roblox uninstaller process finished with issues.", status='warning')

            UI.print_status("Waiting 8 seconds after uninstaller attempt...", status='info')
            time.sleep(8)
        except Exception as e:
            UI.print_status(f"Error running Roblox uninstaller: {e}.", status='error')
    else:
        UI.print_status("Official Roblox uninstaller not found. Proceeding with manual deletion.", status='warning')

    UI.print_status("Performing manual folder deletions...", status='info')
    actual_deleted_count = 0
    total_paths = len(roblox_paths_to_delete_manually)
    for i, path_to_delete in enumerate(roblox_paths_to_delete_manually):
        UI.print_progress_bar(i, total_paths, prefix='Manual Deletion:',
                              suffix=f'{os.path.basename(path_to_delete)[:20]:<20}', length=30, color=Theme.ERROR)
        time.sleep(0.1)
        if os.path.exists(path_to_delete):
            try:
                shutil.rmtree(path_to_delete, ignore_errors=True)
                if not os.path.exists(path_to_delete):
                    actual_deleted_count += 1
            except Exception as e_rmtree:
                pass
    UI.print_progress_bar(total_paths, total_paths, prefix='Manual Deletion:', suffix='Done!'.ljust(20), length=30,
                          color=Theme.SUCCESS)
    if actual_deleted_count > 0:
        UI.print_status(f"Manually deleted {actual_deleted_count} Roblox folder(s).", status='success', indent=2)

    if success_uninstaller or actual_deleted_count > 0:
        UI.print_status("Roblox uninstallation/removal attempt finished.", status='success')
    else:
        UI.print_status("Roblox may not have been fully uninstalled/removed.", status='warning')


# --- MAC Spoofer Functions ---
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
        UI.print_status(f"Error enumerating NICs: {e}", status='error')
    return nics


def generate_random_mac_enforce_02():
    return "02" + "".join(random.choice(HEX_CHARS_MAC_SPOOFER) for _ in range(10))


def set_mac_address_new(nic_name, nic_index, mac_address_no_colons):
    if not nic_index:
        UI.print_status(f"Cannot set MAC: NIC index missing for {nic_name}.", status='error')
        return False
    registry_key_path = rf"{REG_PATH_MAC_SPOOFER}\{nic_index.zfill(4)}"
    UI.print_status(f"Disabling network adapter: {nic_name}...", status='info')
    _run_shell_command_simple(f'netsh interface set interface name="{nic_name}" admin=disable', shell=True,
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, capture_output_if_no_pipes=False)
    time.sleep(2)

    UI.print_status(f"Setting MAC {mac_address_no_colons} for {nic_name}...", status='action')
    reg_add_command = ["reg", "add", registry_key_path, "/v", "NetworkAddress", "/t", "REG_SZ", "/d",
                       mac_address_no_colons, "/f"]
    result = _run_shell_command_simple(reg_add_command, shell=False, capture_output_if_no_pipes=True)

    UI.print_status(f"Enabling network adapter: {nic_name}...", status='info')
    _run_shell_command_simple(f'netsh interface set interface name="{nic_name}" admin=enable', shell=True,
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, capture_output_if_no_pipes=False)
    time.sleep(3)

    if result and result.returncode == 0:
        UI.print_status(f"MAC address successfully set for {nic_name}.", status='success')
        return True
    else:
        UI.print_status(f"Failed to set MAC address for {nic_name}.", status='error')
        return False


def change_mac_address_integrated():
    UI.print_header("MAC Address Spoofer")
    if not is_admin():
        UI.print_status("Administrator privileges required. Skipping.", status='error')
        return
    adapters = get_available_nics_new()
    if not adapters:
        UI.print_status("No suitable network adapters found.", status='warning')
        return

    UI.print_status("Available Network Adapters:", status='info')
    for i, adapter_info in enumerate(adapters):
        print(f"        {Theme.PRIMARY}{i + 1}.{Theme.RESET} {adapter_info['name']}")

    try:
        choice_str = UI.get_input("Select adapter to spoof (e.g., 1, or type 'all', 'skip')")
        if choice_str == 'skip':
            UI.print_status("MAC spoofing skipped by user.", status='warning')
            return

        targets = adapters if choice_str == 'all' else (
            [adapters[int(choice_str) - 1]] if choice_str.isdigit() and 1 <= int(choice_str) <= len(adapters) else [])
        if not targets:
            UI.print_status("Invalid selection.", status='error')
            return

        changed_count = 0
        for adapter in targets:
            nic_name, nic_idx = adapter['name'], adapter['index']
            new_mac = generate_random_mac_enforce_02()
            formatted_mac = ':'.join(new_mac[j:j + 2] for j in range(0, 12, 2))
            UI.print_status(f"Spoofing {nic_name} with MAC: {Theme.BRIGHT}{formatted_mac}{Theme.RESET}", status='action')
            if set_mac_address_new(nic_name, nic_idx, new_mac):
                changed_count += 1
            time.sleep(1)
        if changed_count > 0:
            UI.print_status(f"{changed_count} MAC address(es) spoofed. RESTART RECOMMENDED.", status='success')
    except Exception as e:
        UI.print_status(f"An error occurred during MAC spoofing: {e}", status='error')


# --- Roblox Install function ---
def install_roblox():
    UI.print_header("Roblox Installation")
    installer_url = "https://www.roblox.com/download/client"
    installer_filename = f"RobloxPlayerInstaller_{uuid.uuid4().hex[:8]}.exe"
    installer_path = os.path.join(os.environ.get('TEMP', '.'), installer_filename)

    # ... (code for downloading and running installer remains the same)
    # Theming the outputs
    UI.print_status("Starting Roblox download...", status='info')
    downloaded = False
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
        with requests.get(installer_url, stream=True, timeout=30, headers=headers, allow_redirects=True) as r:
            r.raise_for_status()
            with open(installer_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192): f.write(chunk)
        if os.path.exists(installer_path) and os.path.getsize(installer_path) > 1000000:
            downloaded = True
            UI.print_status("Downloaded successfully.", status='success')
    except requests.exceptions.RequestException as e_req:
        UI.print_status(f"Download error: {e_req}", status='error')

    if not downloaded:
        UI.print_status("Could not download Roblox installer. Skipping install.", status='error')
        return

    UI.print_status("Starting Roblox installation...", status='action')
    try:
        subprocess.Popen([installer_path], creationflags=subprocess.CREATE_NEW_CONSOLE)
        UI.print_status("Installer launched. Follow on-screen instructions.", status='success')
    except Exception as e:
        UI.print_status(f"Failed to start installer: {e}", status='error')
        return

    UI.print_status("Waiting 45s for installation to proceed...", status='info')
    for i in range(45, 0, -1):
        print(f"\r    {Theme.MUTED}Waiting... {i}s remaining. ", end="")
        time.sleep(1)
    print("\r    Installation time elapsed. Verifying...            ")

    roblox_appdata_path = os.path.join(os.environ.get('LOCALAPPDATA', ''), "Roblox")
    installed_ok = False
    UI.print_status(f"Verifying Roblox installation at: {roblox_appdata_path}", status='info')

    if os.path.isdir(roblox_appdata_path):
        try:
            if any(os.scandir(roblox_appdata_path)):
                installed_ok = True
                UI.print_status("Found Roblox directory and it is not empty.", status='success')
            else:
                UI.print_status("Found Roblox directory, but it appears to be empty.", status='warning')
        except Exception as e_scan:
            UI.print_status(f"Could not scan Roblox directory contents: {e_scan}", status='warning')
    else:
        UI.print_status("Roblox directory not found at the expected location.", status='warning')

    if installed_ok:
        UI.print_status("Roblox installation appears complete.", status='success')
    else:
        UI.print_status(
            "Roblox installation uncertain. The target directory may be missing or empty.", status='warning')


# --- System & HWID Functions ---
def get_current_user_sid_string():
    if PYWIN32_AVAILABLE:
        try:
            token = win32security.OpenProcessToken(win32api.GetCurrentProcess(), win32security.TOKEN_QUERY)
            return win32security.ConvertSidToStringSid(
                win32security.GetTokenInformation(token, winreg.TokenUser)[0])
        except Exception:
            pass
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
    UI.print_header("Monitor EDID Spoofing")
    if not is_admin():
        UI.print_status("Admin privileges required. Skipping.", status='error')
        return
    UI.print_status("Modifying Monitor EDID serials...", status='action')

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
                                                        winreg.KEY_READ | winreg.KEY_WRITE |
                                                        winreg.KEY_WOW64_64KEY) as dev_k:
                                        edid_val, reg_t = winreg.QueryValueEx(dev_k, "EDID")
                                        if reg_t == winreg.REG_BINARY and len(edid_val) >= 128:
                                            m_edid = bytearray(edid_val)
                                            block0 = m_edid[:128]
                                            for i_sn in range(12, 16): block0[i_sn] = random.randint(0, 255)
                                            block0[127] = calculate_edid_checksum(block0)
                                            winreg.SetValueEx(dev_k, "EDID", 0, reg_t, bytes(m_edid))
                                            UI.print_status(f"Modified EDID for: {m_vendor}\\{m_instance}",
                                                            status='success', indent=2)
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
        UI.print_status(f"Error accessing display registry for EDID: {e_base}", status='error')

    if changed_count > 0:
        UI.print_status(f"{changed_count} monitor EDID(s) modified. RESTART REQUIRED.", status='success')
    else:
        UI.print_status("No monitors found or EDIDs modified.", status='warning')


def manage_system_registry_keys():
    UI.print_header("System Registry Cleaning")
    if not is_admin():
        UI.print_status("Admin privileges required. Skipping.", status='error')
        return

    user_sid = get_current_user_sid_string()
    if not user_sid:
        UI.print_status("Could not retrieve user SID. Skipping key deletion.", status='error')
        return

    UI.print_status(f"Cleaning registry for user SID: {user_sid}", status='info')
    paths_to_clean = {
        "Control (HKCU)": "HKCU:\\System\\CurrentControlSet\\Control",
        "GameConfigStore (HKCU)": "HKCU:\\System\\GameConfigStore",
    }
    overall_success = True
    for key_name, path in paths_to_clean.items():
        command = f"if (Test-Path -Path '{path}') {{ Remove-Item -Path '{path}' -Recurse -Force -ErrorAction SilentlyContinue }}"
        UI.print_status(f"Executing check and delete for: {key_name}", status='action')
        result = _run_shell_command_wrapper(["powershell", "-Command", command], capture_output=True, shell=False)
        if not (result and result.returncode == 0):
            overall_success = False

    if overall_success:
        UI.print_status("System registry cleaning process completed.", status='success')
    else:
        UI.print_status("One or more system registry key deletions failed unexpectedly.", status='warning')


def download_amidewin_tools():
    UI.print_status("Downloading AMIDEWIN tools...", status='action')
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
    total_tools = len(AMIDEWIN_TOOLS_MAP)
    for i, (dest_path, url) in enumerate(AMIDEWIN_TOOLS_MAP.items()):
        UI.print_progress_bar(i, total_tools, prefix='Downloading:',
                              suffix=f'{os.path.basename(dest_path):<20}', length=30, color=Theme.INFO)
        if os.path.exists(dest_path) and os.path.getsize(dest_path) > 10000: continue
        try:
            with requests.get(url, stream=True, timeout=30) as r:
                r.raise_for_status()
                with open(dest_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192): f.write(chunk)
        except Exception as e_dl:
            all_ok = False
            # Break on failure
            UI.print_progress_bar(total_tools, total_tools, prefix='Downloading:', suffix='Failed!'.ljust(20),
                                  length=30, color=Theme.ERROR)
            UI.print_status(f"Failed to download {os.path.basename(dest_path)}: {e_dl}", status='error')
            break

    if all_ok:
        UI.print_progress_bar(total_tools, total_tools, prefix='Downloading:', suffix='Done!'.ljust(20), length=30,
                              color=Theme.SUCCESS)
    return all_ok


def delete_amidewin_tools():
    UI.print_status("Deleting AMIDEWIN tools...", status='info')
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
    UI.print_status("AMIDEWIN cleanup finished.", status='success')


def spoof_smbios_with_amidewin_focused():
    UI.print_status("Spoofing System UUID with AMIDEWIN...", status='action')
    exe_path = os.path.join(AMIDEWIN_DIR_HWID, "AMIDEWINx64.EXE")
    if not os.path.exists(exe_path):
        UI.print_status("AMIDEWINx64.EXE not found. Skipping.", status='error')
        return False

    ami_commands = {"/SU": "Auto"}
    success_count = 0
    total_cmds = len(ami_commands)
    for i, (param, value) in enumerate(ami_commands.items()):
        UI.print_progress_bar(i, total_cmds, prefix='SMBIOS Update:', suffix=f'{param} {value}...'.ljust(20),
                              length=30, color=Theme.INFO)
        cmd_result = _run_shell_command_simple([exe_path, param, value], cwd=AMIDEWIN_DIR_HWID, shell=False,
                                               capture_output_if_no_pipes=True, timeout=20)
        if cmd_result and cmd_result.returncode == 0: success_count += 1
    UI.print_progress_bar(total_cmds, total_cmds, prefix='SMBIOS Update:', suffix='Done!'.ljust(20), length=30,
                          color=Theme.SUCCESS)
    if success_count > 0:
        UI.print_status("AMIDEWIN commands issued. RESTART IS CRITICAL.", status='success')
        return True
    else:
        UI.print_status("No AMIDEWIN SMBIOS commands succeeded.", status='error')
        return False


def restart_wmi_service():
    UI.print_status("Restarting WMI service (winmgmt)...", status='action')
    if not is_admin():
        UI.print_status("Admin rights needed. Skipping.", status='error')
        return
    _run_shell_command_simple(["net", "stop", "winmgmt", "/y"], shell=False, timeout=45,
                              capture_output_if_no_pipes=True)
    time.sleep(3)
    _run_shell_command_simple(["net", "start", "winmgmt"], shell=False, timeout=45, capture_output_if_no_pipes=True)
    time.sleep(2)
    sc_query_res = _run_shell_command_simple(['sc', 'query', 'winmgmt'], shell=False, capture_output_if_no_pipes=True,
                                             timeout=10)
    if sc_query_res and sc_query_res.stdout and "RUNNING" in sc_query_res.stdout.upper():
        UI.print_status("WMI service (winmgmt) is confirmed RUNNING.", status='success')
    else:
        UI.print_status("WMI status uncertain.", status='warning')


def perform_focused_hwid_spoof():
    UI.print_header("Focused HWID Spoofing")
    if not is_admin():
        UI.print_status("Admin rights needed. Skipping.", status='error')
        return
    if not download_amidewin_tools():
        UI.print_status("AMIDEWIN download failed. Aborting HWID spoof.", status='error')
        return

    if spoof_smbios_with_amidewin_focused():
        restart_wmi_service()
    delete_amidewin_tools()
    UI.print_status("Focused HWID spoofing attempt completed.", status='success')


# --- Main Operation Sequence ---
def perform_all_spoofing_operations():
    try:
        requests.get("https://1.1.1.1", timeout=5)
    except requests.exceptions.RequestException:
        UI.print_status("No internet connection detected.", status='error')
        if UI.get_input("Continue anyway? (y/n)") != 'y': return False

    uninstall_roblox()
    delete_roblox_registry_keys()
    delete_roblox_cookies()
    change_mac_address_integrated()

    UI.print_status("Pausing 10s for network adapters to stabilize...", status='info')
    time.sleep(10)

    modify_monitor_edids()
    manage_system_registry_keys()
    perform_focused_hwid_spoof()
    install_roblox()

    UI.print_header("All Operations Completed")
    UI.print_status("A FULL SYSTEM RESTART IS REQUIRED FOR ALL CHANGES TO TAKE EFFECT!", status='success')
    return True


# --- Main Execution ---
def main():
    if os.name == 'nt':
        set_terminal_transparency(alpha_percentage=90)
        os.system('cls')
    UI.print_banner()

    if not is_admin():
        UI.print_status("Admin privileges required. Restarting with admin rights...", status='warning')
        time.sleep(2)
        restart_with_admin()
        # The script will exit here and restart. The check below is for the new instance.
        if not is_admin():
            UI.print_status("Failed to acquire admin privileges. Exiting.", status='error')
            sys.exit(1)

    UI.print_status("Running as administrator.", status='success')
    if not PYWIN32_AVAILABLE:
        UI.print_status("pywin32 not found. Some features might have fallbacks.", status='warning')

    if UI.get_input("Do you wish to proceed? (y/n)") in ['yes', 'y']:
        try:
            start_time = time.time()
            perform_all_spoofing_operations()
            total_time = time.time() - start_time
            UI.print_status(f"Total execution time: {total_time:.2f} seconds.", status='info')
        except (SystemExit, KeyboardInterrupt):
            print("\n")
            UI.print_status("Operation cancelled by user.", status='warning')
        except Exception as e:
            UI.print_status(f"AN UNEXPECTED CRITICAL ERROR OCCURRED: {e}", status='error')
            import traceback
            traceback.print_exc()
    else:
        UI.print_status("Operation cancelled.", status='warning')

    input(f"\n{Theme.MUTED}Press Enter to exit...{Theme.RESET}")


if __name__ == "__main__":
    main()
# Copyright (c) 2025 nitaybl. All Rights Reserved.
