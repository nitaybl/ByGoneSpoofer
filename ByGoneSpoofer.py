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
from pathlib import Path
from colorama import init, Fore, Style
import uuid
import string
import json
from datetime import datetime

# Initialize colorama
init(autoreset=True)

# --- Global Flags ---
DRY_RUN_MODE = False
OPERATION_LOG = []


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
 /$$$$$$$                                /$$$$$$                                           /$$$$$$$  /$$$$$$$        /$$$$$$
| $$__  $$                              /$$__  $$                                          | $$__  $$| $$__  $$       /$$__  $$
| $$  \ $$ /$$   /$$| $$  \__/  /$$$$$$  /$$$$$$$   /$$$$$$         | $$  \ $$| $$  \ $$      | $$  \__/  /$$$$$$   /$$$$$$   /$$$$$$ | $$  \__//$$$$$$   /$$$$$$
| $$$$$$$ | $$  | $$| $$ /$$$$ /$$__  $$| $$__  $$ /$$__  $$        | $$$$$$$/| $$$$$$$        |  $$$$$$  /$$__  $$ /$$__  $$ /$$__  $$| $$$$   /$$__  $$ /$$__  $$
| $$__  $$| $$  | $$| $$|_  $$| $$  \ $$| $$  \ $$| $$$$$$$$        | $$__  $$| $$__  $$         \____  $$| $$  \ $$| $$  \ $$| $$  \ $$| $$_/   | $$$$$$$$| $$  \__/
| $$  \ $$| $$  | $$| $$  \ $$| $$  | $$| $$  \ $$| $$_____/        | $$  \ $$| $$  \ $$        /$$  \ $$| $$  | $$| $$  \ $$| $$  \ $$| $$     | $$_____/| $$
| $$$$$$$/|  $$$$$$$|  $$$$$$/|  $$$$$$/| $$  | $$|  $$$$$$$        | $$  | $$| $$$$$$$/       |  $$$$$$/| $$$$$$$/|  $$$$$$/|  $$$$$$/| $$     |  $$$$$$$| $$
|_______/  \____  $$ \______/  \______/ |__/  |__/ \_______/        |__/  |__/|_______/         \______/ | $$____/  \______/  \______/ |__/      \_______/|__/
          /$$  | $$                                                                         | $$
         |  $$$$$$/                                                                         | $$
          \______/                                                                          |__/
"""
        print(f"{Theme.PRIMARY}{banner_art}{Theme.RESET}")
        title = "Nitaybl's ByGone Spoofer (join discord.gg/bygone)"
        version = "Version: v4.4 (Safety Features + Enhanced Cleanup)"
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

# --- WebView2 Fixer Constants ---
VERSIONS_ROOT = r"C:\Program Files (x86)\Roblox\Versions"


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


# --- Operation Logger Class ---
class OperationLogger:
    """Logs all operations performed by the spoofer."""
    def __init__(self):
        self.log_file = os.path.join(os.environ.get('TEMP', ''), 'bygone_operations.log')
        self.operations = []
    
    def log(self, operation, success=True, details=""):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        status_str = 'SUCCESS' if success else 'FAILED'
        entry = f"[{timestamp}] {operation} - {status_str}"
        if details:
            entry += f" | {details}"
        self.operations.append(entry)
        
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(entry + '\n')
        except:
            pass
    
    def show_recent_logs(self, count=10):
        UI.print_header("Recent Operation History")
        if not self.operations:
            UI.print_status("No operations logged yet.", status='info')
            return
        for op in self.operations[-count:]:
            UI.print_status(op, status='info')
    
    def get_log_file_path(self):
        return self.log_file


# Global logger instance
operation_logger = OperationLogger()


# --- System Restore & Backup Functions ---
def create_system_restore_point(description="ByGone Spoofer Backup Point"):
    """Creates a Windows system restore point before making changes."""
    UI.print_status("Creating system restore point (this may take 30-60 seconds)...", status='action')
    if not is_admin():
        UI.print_status("Admin required for restore point creation.", status='error')
        operation_logger.log("Create Restore Point", False, "No admin rights")
        return False
    
    try:
        # Enable System Restore if disabled
        enable_cmd = 'powershell -Command "Enable-ComputerRestore -Drive \'C:\\\'"'
        _run_shell_command_simple(enable_cmd, shell=True, capture_output_if_no_pipes=True, timeout=10)
        
        # Create restore point using PowerShell
        ps_command = f'Checkpoint-Computer -Description "{description}" -RestorePointType "MODIFY_SETTINGS"'
        result = _run_shell_command_wrapper(["powershell", "-Command", ps_command], 
                                           capture_output=True, shell=False, timeout=90)
        
        if result and result.returncode == 0:
            UI.print_status("✓ System restore point created successfully!", status='success')
            operation_logger.log("Create Restore Point", True, description)
            return True
        else:
            # Fallback method using WMIC
            UI.print_status("Trying alternative method...", status='info')
            wmic_cmd = f'wmic.exe /Namespace:\\\\root\\default Path SystemRestore Call CreateRestorePoint "{description}", 100, 7'
            result2 = _run_shell_command_simple(wmic_cmd, shell=True, capture_output_if_no_pipes=True, timeout=90)
            if result2 and result2.returncode == 0:
                UI.print_status("✓ System restore point created (via WMIC)!", status='success')
                operation_logger.log("Create Restore Point", True, description)
                return True
            else:
                UI.print_status("Could not create restore point (may be disabled on your system).", status='warning')
                UI.print_status("TIP: You can manually enable it in System Properties > System Protection", status='info')
                operation_logger.log("Create Restore Point", False, "Both methods failed")
                return False
    except Exception as e:
        UI.print_status(f"Error creating restore point: {e}", status='error')
        operation_logger.log("Create Restore Point", False, str(e))
        return False


def backup_hardware_ids():
    """Backs up original hardware identifiers to a JSON file."""
    UI.print_status("Backing up original hardware identifiers...", status='action')
    backup_file = os.path.join(os.environ.get('APPDATA', ''), 'ByGoneHardwareBackup.json')
    
    if os.path.exists(backup_file):
        UI.print_status("⚠️  Backup file already exists. Skipping to preserve original data.", status='warning')
        operation_logger.log("Backup Hardware IDs", True, "Already exists")
        return backup_file
    
    backup_data = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'version': 'v4.3',
        'original_macs': {},
        'original_system_info': {},
        'network_adapters': []
    }
    
    # Backup MAC addresses
    try:
        adapters = get_available_nics_new()
        getmac_result = _run_shell_command_simple('getmac /v /fo csv', capture_output_if_no_pipes=True, text=True)
        if getmac_result and getmac_result.stdout:
            lines = getmac_result.stdout.strip().split('\n')
            for adapter in adapters:
                for line in lines:
                    if adapter['name'] in line:
                        parts = line.split(',')
                        if len(parts) >= 2:
                            mac = parts[1].strip().strip('"')
                            backup_data['original_macs'][adapter['name']] = mac
                            backup_data['network_adapters'].append({
                                'name': adapter['name'],
                                'index': adapter['index'],
                                'original_mac': mac
                            })
                        break
        UI.print_status(f"Backed up {len(backup_data['original_macs'])} MAC address(es)", status='success', indent=2)
    except Exception as e:
        UI.print_status(f"Could not backup MAC addresses: {e}", status='warning', indent=2)
    
    # Backup system info using WMIC
    system_components = {
        'bios': 'wmic bios get serialnumber,manufacturer,version /format:csv',
        'baseboard': 'wmic baseboard get serialnumber,manufacturer,product /format:csv',
        'computersystem': 'wmic computersystem get uuid,manufacturer,model /format:csv',
        'cpu': 'wmic cpu get processorid,name /format:csv'
    }
    
    for component, cmd in system_components.items():
        try:
            result = _run_shell_command_simple(cmd, shell=True, capture_output_if_no_pipes=True, text=True, timeout=10)
            if result and result.stdout:
                backup_data['original_system_info'][component] = result.stdout.strip()
        except Exception:
            pass
    
    # Save to file
    try:
        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(backup_data, f, indent=2)
        UI.print_status(f"✓ Hardware backup saved to: {backup_file}", status='success')
        operation_logger.log("Backup Hardware IDs", True, backup_file)
        return backup_file
    except Exception as e:
        UI.print_status(f"Could not save backup: {e}", status='error')
        operation_logger.log("Backup Hardware IDs", False, str(e))
        return None


def restore_from_backup():
    """Restores hardware IDs from backup file (MAC addresses only)."""
    UI.print_header("Restore from Backup")
    backup_file = os.path.join(os.environ.get('APPDATA', ''), 'ByGoneHardwareBackup.json')
    
    if not os.path.exists(backup_file):
        UI.print_status("No backup file found. Cannot restore.", status='error')
        UI.print_status(f"Expected location: {backup_file}", status='info')
        return False
    
    try:
        with open(backup_file, 'r', encoding='utf-8') as f:
            backup_data = json.load(f)
        
        UI.print_status(f"Found backup from: {backup_data.get('timestamp', 'Unknown')}", status='info')
        UI.print_status("⚠️  Note: Only MAC addresses can be restored. SMBIOS/HWID cannot be reversed via backup.", status='warning')
        
        confirm = UI.get_input("Restore MAC addresses from backup? (yes/no)")
        if confirm != 'yes':
            UI.print_status("Restore cancelled.", status='warning')
            return False
        
        restored = 0
        adapters_to_restore = backup_data.get('network_adapters', [])
        for adapter_info in adapters_to_restore:
            nic_name = adapter_info.get('name')
            nic_index = adapter_info.get('index')
            original_mac = adapter_info.get('original_mac', '').replace('-', '').replace(':', '')
            
            if nic_name and nic_index and original_mac and len(original_mac) == 12:
                UI.print_status(f"Restoring {nic_name} to MAC: {original_mac}", status='action', indent=2)
                if set_mac_address_new(nic_name, nic_index, original_mac):
                    restored += 1
        
        if restored > 0:
            UI.print_status(f"✓ Restored {restored} MAC address(es) from backup!", status='success')
            operation_logger.log("Restore from Backup", True, f"{restored} MACs restored")
            return True
        else:
            UI.print_status("No MAC addresses were restored.", status='warning')
            operation_logger.log("Restore from Backup", False, "No MACs restored")
            return False
            
    except Exception as e:
        UI.print_status(f"Error restoring from backup: {e}", status='error')
        operation_logger.log("Restore from Backup", False, str(e))
        return False


# --- Preflight Check System ---
def perform_preflight_checks():
    """Performs comprehensive system checks before spoofing operations."""
    UI.print_header("Preflight System Checks")
    
    checks = {}
    all_passed = True
    
    # 1. Admin Rights
    admin_check = is_admin()
    checks['Administrator Rights'] = admin_check
    if not admin_check:
        all_passed = False
    
    # 2. Internet Connection
    internet_check = False
    try:
        requests.get("https://1.1.1.1", timeout=5)
        internet_check = True
    except:
        pass
    checks['Internet Connection'] = internet_check
    
    # 3. Disk Space Check (>5GB free)
    disk_space_check = False
    try:
        stats = shutil.disk_usage('C:\\')
        free_gb = stats.free / (1024**3)
        disk_space_check = free_gb > 5
        checks[f'Disk Space (>5GB) [{free_gb:.1f}GB free]'] = disk_space_check
    except:
        checks['Disk Space (>5GB)'] = False
    
    # 4. Roblox Not Running
    roblox_check = True
    try:
        result = _run_shell_command_simple('tasklist', capture_output_if_no_pipes=True, text=True, timeout=5)
        if result and result.stdout:
            if 'RobloxPlayerBeta.exe' in result.stdout or 'Roblox.exe' in result.stdout:
                roblox_check = False
    except:
        pass
    checks['No Roblox Running'] = roblox_check
    if not roblox_check:
        all_passed = False
    
    # 5. WMI Service Running
    wmi_check = False
    try:
        result = _run_shell_command_simple('sc query winmgmt', shell=True, capture_output_if_no_pipes=True, text=True, timeout=5)
        if result and result.stdout and 'RUNNING' in result.stdout.upper():
            wmi_check = True
    except:
        pass
    checks['WMI Service Running'] = wmi_check
    
    # 6. Network Adapters Available
    adapters_check = False
    try:
        adapters = get_available_nics_new()
        adapters_check = len(adapters) > 0
        checks[f'Network Adapters Found [{len(adapters)}]'] = adapters_check
    except:
        checks['Network Adapters Found'] = False
    
    # Display results
    for check_name, passed in checks.items():
        status = 'success' if passed else 'error'
        icon = '✓' if passed else '✗'
        UI.print_status(f"{icon} {check_name}", status=status)
    
    print()
    if all_passed:
        UI.print_status("All critical checks passed! Ready to proceed.", status='success')
    else:
        UI.print_status("⚠️  Some checks failed. You can still proceed but may encounter issues.", status='warning')
    
    operation_logger.log("Preflight Checks", all_passed, f"{sum(checks.values())}/{len(checks)} passed")
    return all_passed


# --- Enhanced Cleanup Functions ---
def delete_windows_event_logs():
    """Clears Windows Event Logs that might contain detection traces."""
    UI.print_status("Clearing Windows Event Logs (traces)...", status='action')
    if not is_admin():
        UI.print_status("Admin required for event log clearing. Skipping.", status='error')
        return
    
    logs_to_clear = [
        'Application',
        'System',
        'Security',
        'Microsoft-Windows-AppLocker/EXE and DLL',
        'Microsoft-Windows-AppLocker/MSI and Script',
        'Microsoft-Windows-Windows Defender/Operational'
    ]
    
    cleared = 0
    for log_name in logs_to_clear:
        try:
            cmd = f'wevtutil.exe cl "{log_name}"'
            result = _run_shell_command_simple(cmd, shell=True, capture_output_if_no_pipes=True, timeout=10)
            if result and result.returncode == 0:
                cleared += 1
                UI.print_status(f"Cleared: {log_name}", status='success', indent=2)
        except Exception:
            pass
    
    UI.print_status(f"Cleared {cleared}/{len(logs_to_clear)} event log(s).", status='success')
    operation_logger.log("Clear Event Logs", True, f"{cleared} logs cleared")


def flush_dns_cache():
    """Flushes the DNS cache to remove traces."""
    UI.print_status("Flushing DNS cache...", status='action')
    try:
        result = _run_shell_command_simple('ipconfig /flushdns', shell=True, capture_output_if_no_pipes=True, timeout=10)
        if result and result.returncode == 0:
            UI.print_status("DNS cache flushed successfully.", status='success')
            operation_logger.log("Flush DNS Cache", True)
            return True
    except Exception as e:
        UI.print_status(f"Could not flush DNS cache: {e}", status='warning')
        operation_logger.log("Flush DNS Cache", False, str(e))
    return False


def clear_temp_files():
    """Clears temporary files that might contain traces."""
    UI.print_status("Clearing temporary files...", status='action')
    
    temp_paths = [
        os.environ.get('TEMP', ''),
        os.environ.get('TMP', ''),
        os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Temp'),
        'C:\\Windows\\Temp'
    ]
    
    deleted_count = 0
    for temp_path in temp_paths:
        if not temp_path or not os.path.exists(temp_path):
            continue
        try:
            # Only delete Roblox-related temp files for safety
            for item in os.listdir(temp_path):
                if 'roblox' in item.lower() or 'rbx' in item.lower():
                    item_path = os.path.join(temp_path, item)
                    try:
                        if os.path.isfile(item_path):
                            os.remove(item_path)
                            deleted_count += 1
                        elif os.path.isdir(item_path):
                            shutil.rmtree(item_path, ignore_errors=True)
                            deleted_count += 1
                    except:
                        pass
        except Exception:
            pass
    
    if deleted_count > 0:
        UI.print_status(f"Cleared {deleted_count} Roblox-related temp item(s).", status='success')
    else:
        UI.print_status("No Roblox temp files found to clear.", status='info')
    operation_logger.log("Clear Temp Files", True, f"{deleted_count} items")


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
    UI.print_status("Searching for Roblox uninstaller...", status='info')
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


# --- Roblox Install function ---
def install_roblox():
    UI.print_header("Roblox Installation")
    installer_url = "https://www.roblox.com/download/client"
    installer_filename = f"RobloxPlayerInstaller_{uuid.uuid4().hex[:8]}.exe"
    installer_path = os.path.join(os.environ.get('TEMP', '.'), installer_filename)

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
    print("\r    Installation time elapsed. Verifying...                ")

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
    """
    Sets MAC address for a network adapter.
    NOTE: Some WiFi adapters and certain hardware may not support MAC address changes.
    This is a hardware/driver limitation and not a bug.
    """
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
        UI.print_status(f"TIP: Some WiFi/wireless adapters don't support MAC changes.", status='info', indent=2)
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
        print(f"            {Theme.PRIMARY}{i + 1}.{Theme.RESET} {adapter_info['name']}")

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
            UI.print_status(f"Spoofing {nic_name} with MAC: {Theme.BRIGHT}{formatted_mac}{Theme.RESET}",
                            status='action')
            if set_mac_address_new(nic_name, nic_idx, new_mac):
                changed_count += 1
            time.sleep(1)
        if changed_count > 0:
            UI.print_status(f"{changed_count} MAC address(es) spoofed.", status='success')
    except Exception as e:
        UI.print_status(f"An error occurred during MAC spoofing: {e}", status='error')


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
    """
    Modifies monitor EDID serial numbers.
    NOTE: Some users report temporary graphics glitches after EDID changes.
    A system reboot typically resolves any display issues. Changes are reversed only via System Restore.
    """
    UI.print_header("Monitor EDID Spoofing")
    if not is_admin():
        UI.print_status("Admin privileges required. Skipping.", status='error')
        return
    UI.print_status("Modifying Monitor EDID serials...", status='action')
    UI.print_status("ℹ️  Reboot if you experience graphics glitches after this operation", status='info', indent=2)

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
        UI.print_status(f"{changed_count} monitor EDID(s) modified.", status='success')
        operation_logger.log("Modify Monitor EDIDs", True, f"{changed_count} monitors")
    else:
        UI.print_status("No monitors found or EDIDs modified.", status='warning')
        operation_logger.log("Modify Monitor EDIDs", False, "No monitors found")


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
    """
    Spoofs SMBIOS/HWID using AMIDEWIN.
    NOTE: Some Asus motherboards may have restrictions/protections that prevent HWID changes.
    This is a hardware limitation and the spoofer will still complete other operations.
    """
    UI.print_status("Spoofing System UUID with AMIDEWIN...", status='action')
    UI.print_status("⚠️  Some Asus motherboards may block HWID changes (hardware limitation)", status='warning', indent=2)
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
        UI.print_status("AMIDEWIN commands issued.", status='success')
        operation_logger.log("SMBIOS Spoof", True)
        return True
    else:
        UI.print_status("No AMIDEWIN SMBIOS commands succeeded.", status='error')
        UI.print_status("This may be normal on Asus motherboards or systems with BIOS protections.", status='info', indent=2)
        operation_logger.log("SMBIOS Spoof", False, "May be blocked by hardware")
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
    UI.print_header("Focused HWID Spoofing (SMBIOS)")
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


# --- WebView2 Fixer Functions (Integrated) ---
def find_latest_version_dir() -> Path:
    candidates = []
    root = Path(VERSIONS_ROOT)
    if not root.exists():
        return None
    for p in root.iterdir():
        if p.is_dir() and p.name.startswith("version-"):
            candidates.append((p.stat().st_mtime, p))
    if not candidates:
        return None
    candidates.sort(reverse=True)
    return candidates[0][1]


def nuke_path(target: Path) -> bool:
    if not target.exists():
        UI.print_status(f"Nothing to delete at: {target}", status='success', indent=2)
        return True
    try:
        if target.is_file():
            os.chmod(target, 0o666)
            target.unlink()
        else:  # is directory
            for root, dirs, files in os.walk(target):
                for d in dirs:
                    try:
                        os.chmod(os.path.join(root, d), 0o777)
                    except Exception:
                        pass
                for f in files:
                    try:
                        os.chmod(os.path.join(root, f), 0o666)
                    except Exception:
                        pass
            shutil.rmtree(target, ignore_errors=False)
        UI.print_status(f"NUKED: {target}", status='success', indent=2)
        return True
    except Exception as e:
        UI.print_status(f"Could not delete {target}: {e}", status='error', indent=2)
        return False


def action_nuke_webview2():
    UI.print_header("Nuke Roblox WebView2 Data")
    UI.print_status("Killing Roblox processes first...", status='info')
    kill_roblox_processes()
    time.sleep(1)

    version_dir = find_latest_version_dir()
    if not version_dir:
        UI.print_status(f"Could not find Roblox versions directory at '{VERSIONS_ROOT}'. Is Roblox installed?",
                        status='error')
        return

    target_path = version_dir / "RobloxPlayerBeta.exe.WebView2"
    UI.print_status(f"Targeting path for deletion: {target_path}", status='action')

    if nuke_path(target_path):
        UI.print_status("Done. Launch Roblox and it will rebuild the WebView2 data.", status='success')
    else:
        UI.print_status("The operation failed. Please check permissions and try again.", status='error')


# --- Main Operation Sequences ---
def perform_full_spoofing_operations():
    operation_logger.log("Started Full Spoofing Operation", True)
    
    # Preflight checks
    perform_preflight_checks()
    proceed = UI.get_input("Continue with full spoofing? (y/n)")
    if proceed != 'y':
        UI.print_status("Operation cancelled by user.", status='warning')
        return False
    
    # Create restore point and backup
    UI.print_status("Creating safety backups before making changes...", status='warning')
    create_system_restore_point("ByGone Full Spoof Backup")
    backup_hardware_ids()
    
    try:
        requests.get("https://1.1.1.1", timeout=5)
    except requests.exceptions.RequestException:
        UI.print_status("No internet connection detected.", status='error')
        if UI.get_input("Continue anyway? (y/n)") != 'y': return False

    # Enhanced trace deletion
    delete_windows_event_logs()
    clear_temp_files()
    flush_dns_cache()
    
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
    UI.print_status("Join Our Server At discord.gg/bygone and star the project pls i need to feed my kids",
                    status='success')
    operation_logger.log("Completed Full Spoofing Operation", True)
    return True


def perform_light_spoofing_operations():
    operation_logger.log("Started Light Spoofing Operation", True)
    
    # Preflight checks
    perform_preflight_checks()
    proceed = UI.get_input("Continue with light spoofing? (y/n)")
    if proceed != 'y':
        UI.print_status("Operation cancelled by user.", status='warning')
        return False
    
    # Create restore point and backup
    UI.print_status("Creating safety backups before making changes...", status='warning')
    create_system_restore_point("ByGone Light Spoof Backup")
    backup_hardware_ids()
    
    try:
        requests.get("https://1.1.1.1", timeout=5)
    except requests.exceptions.RequestException:
        UI.print_status("No internet connection detected.", status='error')
        if UI.get_input("Continue anyway? (y/n)") != 'y': return False

    # Enhanced trace deletion
    delete_windows_event_logs()
    clear_temp_files()
    flush_dns_cache()
    
    uninstall_roblox()
    delete_roblox_registry_keys()
    delete_roblox_cookies()
    change_mac_address_integrated()

    UI.print_status("Pausing 10s for network adapters to stabilize...", status='info')
    time.sleep(10)

    modify_monitor_edids()
    manage_system_registry_keys()
    # The call to perform_focused_hwid_spoof() is intentionally removed for this light version.
    UI.print_status("Skipping SMBIOS / HWID spoofing as requested.", status='info')
    install_roblox()

    UI.print_header("Light Spoof Operations Completed")
    UI.print_status("Join Our Server At discord.gg/bygone and star the project pls i need to feed my kids",
                    status='success')
    operation_logger.log("Completed Light Spoofing Operation", True)
    return True


def perform_recommended_spoof_for_cheating():
    """Recommended option for users who want to continue cheating.
    Spoofs everything EXCEPT SMBIOS UUID and hardware serials.
    Deletes traces, changes MAC address, and reinstalls Roblox."""
    UI.print_header("RECOMMENDED SPOOF (For Continuing to Cheat)")
    UI.print_status("This will: Delete traces, Change MAC, Skip HWID/SMBIOS, Reinstall Roblox", status='info')
    UI.print_status("This is RECOMMENDED if you want to continue cheating without full HWID changes.", status='warning')
    
    operation_logger.log("Started Recommended Spoof for Cheating", True)
    
    # Preflight checks
    perform_preflight_checks()
    proceed = UI.get_input("Continue with recommended spoofing? (y/n)")
    if proceed != 'y':
        UI.print_status("Operation cancelled by user.", status='warning')
        return False
    
    # Create restore point and backup
    UI.print_status("Creating safety backups before making changes...", status='warning')
    create_system_restore_point("ByGone Recommended Spoof Backup")
    backup_hardware_ids()
    
    try:
        requests.get("https://1.1.1.1", timeout=5)
    except requests.exceptions.RequestException:
        UI.print_status("No internet connection detected.", status='error')
        if UI.get_input("Continue anyway? (y/n)") != 'y': return False

    # Enhanced trace deletion
    delete_windows_event_logs()
    clear_temp_files()
    flush_dns_cache()
    
    # Delete all traces
    uninstall_roblox()
    delete_roblox_registry_keys()
    delete_roblox_cookies()
    
    # Change MAC address
    change_mac_address_integrated()

    UI.print_status("Pausing 10s for network adapters to stabilize...", status='info')
    time.sleep(10)

    # Clean system registry but skip SMBIOS/HWID spoofing
    manage_system_registry_keys()
    UI.print_status("Skipping SMBIOS UUID and Hardware Serial spoofing (as recommended for cheating).", status='info')
    
    # Reinstall Roblox
    install_roblox()

    UI.print_header("Recommended Spoof Completed")
    UI.print_status("✓ Traces deleted | ✓ MAC changed | ✓ Roblox reinstalled | ✗ HWID unchanged", status='success')
    UI.print_status("Join Our Server At discord.gg/bygone", status='success')
    operation_logger.log("Completed Recommended Spoof for Cheating", True)
    return True


def reset_network_adapters():
    """Attempts to reset network adapters to default state."""
    UI.print_status("Resetting network adapters...", status='action')
    if not is_admin():
        UI.print_status("Admin privileges required. Skipping.", status='error')
        return
    
    adapters = get_available_nics_new()
    if not adapters:
        UI.print_status("No network adapters found.", status='warning')
        return
    
    reset_count = 0
    for adapter in adapters:
        nic_name = adapter['name']
        nic_index = adapter['index']
        registry_key_path = rf"{REG_PATH_MAC_SPOOFER}\{nic_index.zfill(4)}"
        
        try:
            # Delete the NetworkAddress registry value to restore default MAC
            UI.print_status(f"Resetting MAC for: {nic_name}...", status='info', indent=2)
            
            # Disable adapter
            _run_shell_command_simple(f'netsh interface set interface name="{nic_name}" admin=disable', 
                                     shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, 
                                     capture_output_if_no_pipes=False)
            time.sleep(1)
            
            # Delete the NetworkAddress value
            reg_delete_cmd = ["reg", "delete", registry_key_path, "/v", "NetworkAddress", "/f"]
            _run_shell_command_simple(reg_delete_cmd, shell=False, capture_output_if_no_pipes=True)
            
            # Enable adapter
            _run_shell_command_simple(f'netsh interface set interface name="{nic_name}" admin=enable', 
                                     shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, 
                                     capture_output_if_no_pipes=False)
            time.sleep(2)
            
            reset_count += 1
            UI.print_status(f"Reset MAC for {nic_name} to default.", status='success', indent=2)
        except Exception as e:
            UI.print_status(f"Could not reset {nic_name}: {e}", status='warning', indent=2)
    
    if reset_count > 0:
        UI.print_status(f"{reset_count} network adapter(s) reset to default.", status='success')
    else:
        UI.print_status("No adapters were reset.", status='warning')


def perform_reverse_spoofing():
    """Attempts to reverse/undo spoofing changes.
    Note: Some changes (EDID, SMBIOS) cannot be fully reversed without a system restore point."""
    UI.print_header("REVERSE SPOOFING")
    UI.print_status("⚠️  WARNING: Not all changes can be reversed!", status='error')
    UI.print_status("SMBIOS/HWID and EDID changes require a system restore or BIOS reset.", status='warning')
    UI.print_status("This will: Reset MACs, Clean install Roblox, Reset network settings", status='info')
    
    operation_logger.log("Started Reverse Spoofing", True)
    
    confirm = UI.get_input("Are you sure you want to proceed with reversal? (yes/no)")
    if confirm != 'yes':
        UI.print_status("Reversal cancelled.", status='warning')
        return False
    
    try:
        requests.get("https://1.1.1.1", timeout=5)
    except requests.exceptions.RequestException:
        UI.print_status("No internet connection detected.", status='error')
        if UI.get_input("Continue anyway? (y/n)") != 'y': return False
    
    # Kill Roblox processes
    kill_roblox_processes()
    time.sleep(1)
    
    # Check if backup exists and offer to restore
    backup_file = os.path.join(os.environ.get('APPDATA', ''), 'ByGoneHardwareBackup.json')
    if os.path.exists(backup_file):
        UI.print_status("✓ Hardware backup file found!", status='success')
        restore_choice = UI.get_input("Restore from backup? (y/n)")
        if restore_choice == 'y':
            restore_from_backup()
        else:
            # Manual reset
            reset_network_adapters()
    else:
        UI.print_status("No backup file found. Will reset to defaults.", status='warning')
        reset_network_adapters()
    
    UI.print_status("Pausing 10s for network adapters to stabilize...", status='info')
    time.sleep(10)
    
    # Clean install Roblox (uninstall and reinstall)
    uninstall_roblox()
    time.sleep(2)
    install_roblox()
    
    UI.print_header("Reversal Process Completed")
    UI.print_status("✓ Network MACs reset | ✓ Roblox reinstalled", status='success')
    UI.print_status("⚠️  IMPORTANT: SMBIOS/HWID and EDID changes were NOT reversed!", status='error')
    UI.print_status("To fully reverse hardware changes, use a system restore point or BIOS reset.", status='warning')
    UI.print_status("Join Our Server At discord.gg/bygone for support", status='info')
    operation_logger.log("Completed Reverse Spoofing", True)
    return True


# --- Menu Functions ---
def run_spoofer_menu():
    while True:
        UI.print_header("Spoofer Menu")
        UI.print_status("Select a spoofing method. Read carefully!", status='warning')
        print(
            f"    {Theme.BRIGHT}[1]{Theme.RESET} {Theme.SUCCESS}⭐ RECOMMENDED (Continue Cheating){Theme.RESET} - Deletes traces, changes MAC, skips HWID. Best for continuing to cheat!")
        print(
            f"    {Theme.BRIGHT}[2]{Theme.RESET} {Theme.PRIMARY}Full Spoof (Hard Ban){Theme.RESET} - Changes SMBIOS/HWID, EDID, MACs. Use this for hard bans.")
        print(
            f"    {Theme.BRIGHT}[3]{Theme.RESET} {Theme.WARNING}Light Spoof (No HWID){Theme.RESET} - Changes EDID & MACs only. Use if NOT hard-banned.")
        print(
            f"    {Theme.BRIGHT}[4]{Theme.RESET} {Theme.ERROR}🔄 REVERSE Spoofing{Theme.RESET} - Attempts to undo spoofing changes (partial reversal).")
        print(f"    {Theme.BRIGHT}[0]{Theme.RESET} {Theme.MUTED}Back to Main Menu{Theme.RESET}")

        choice = UI.get_input("Enter your choice")
        if choice == '1':
            perform_recommended_spoof_for_cheating()
            break
        elif choice == '2':
            perform_full_spoofing_operations()
            break
        elif choice == '3':
            perform_light_spoofing_operations()
            break
        elif choice == '4':
            perform_reverse_spoofing()
            break
        elif choice == '0':
            break
        else:
            UI.print_status("Invalid choice. Please enter 0, 1, 2, 3, or 4.", status='error')
            time.sleep(1)


def run_fixer_menu():
    while True:
        UI.print_header("Fixer Menu")
        print(
            f"    {Theme.BRIGHT}[1]{Theme.RESET} {Theme.PRIMARY}Nuke WebView2 Data{Theme.RESET} - Deletes the Roblox WebView2 folder to fix data directory errors.")
        print(f"    {Theme.BRIGHT}[0]{Theme.RESET} {Theme.MUTED}Back to Main Menu{Theme.RESET}")

        choice = UI.get_input("Enter your choice")
        if choice == '1':
            action_nuke_webview2()
            break
        elif choice == '0':
            break
        else:
            UI.print_status("Invalid choice. Please enter 0 or 1.", status='error')
            time.sleep(1)


def run_utilities_menu():
    while True:
        UI.print_header("Utilities Menu")
        print(
            f"    {Theme.BRIGHT}[1]{Theme.RESET} {Theme.SUCCESS}Create System Restore Point{Theme.RESET} - Manually create a restore point before spoofing.")
        print(
            f"    {Theme.BRIGHT}[2]{Theme.RESET} {Theme.INFO}Backup Hardware IDs{Theme.RESET} - Save original hardware identifiers to file.")
        print(
            f"    {Theme.BRIGHT}[3]{Theme.RESET} {Theme.WARNING}Restore from Backup{Theme.RESET} - Restore MAC addresses from backup file.")
        print(
            f"    {Theme.BRIGHT}[4]{Theme.RESET} {Theme.PRIMARY}View Operation Log{Theme.RESET} - Show recent operations history.")
        print(
            f"    {Theme.BRIGHT}[5]{Theme.RESET} {Theme.SECONDARY}Run Preflight Checks{Theme.RESET} - Check system readiness without spoofing.")
        print(
            f"    {Theme.BRIGHT}[6]{Theme.RESET} {Theme.INFO}Clear Temp Files{Theme.RESET} - Delete Roblox-related temporary files.")
        print(
            f"    {Theme.BRIGHT}[7]{Theme.RESET} {Theme.INFO}Flush DNS Cache{Theme.RESET} - Clear DNS cache.")
        print(f"    {Theme.BRIGHT}[0]{Theme.RESET} {Theme.MUTED}Back to Main Menu{Theme.RESET}")

        choice = UI.get_input("Enter your choice")
        if choice == '1':
            create_system_restore_point()
            input(f"\n{Theme.MUTED}Press Enter to continue...{Theme.RESET}")
        elif choice == '2':
            backup_hardware_ids()
            input(f"\n{Theme.MUTED}Press Enter to continue...{Theme.RESET}")
        elif choice == '3':
            restore_from_backup()
            input(f"\n{Theme.MUTED}Press Enter to continue...{Theme.RESET}")
        elif choice == '4':
            operation_logger.show_recent_logs(20)
            UI.print_status(f"Full log file: {operation_logger.get_log_file_path()}", status='info')
            input(f"\n{Theme.MUTED}Press Enter to continue...{Theme.RESET}")
        elif choice == '5':
            perform_preflight_checks()
            input(f"\n{Theme.MUTED}Press Enter to continue...{Theme.RESET}")
        elif choice == '6':
            clear_temp_files()
            input(f"\n{Theme.MUTED}Press Enter to continue...{Theme.RESET}")
        elif choice == '7':
            flush_dns_cache()
            input(f"\n{Theme.MUTED}Press Enter to continue...{Theme.RESET}")
        elif choice == '0':
            break
        else:
            UI.print_status("Invalid choice. Please enter 0-7.", status='error')
            time.sleep(1)


# --- Main Execution ---
def main():
    if os.name == 'nt':
        set_terminal_transparency(alpha_percentage=90)
        os.system('cls')

    UI.print_banner()

    if not is_admin():
        UI.print_status("Administrator rights are required. Re-launching with elevation...", 'warning')
        time.sleep(1.5)
        restart_with_admin()
        return  # The script will exit here and restart

    UI.print_status("Running as administrator.", status='success')
    if not PYWIN32_AVAILABLE:
        UI.print_status("pywin32 not found. Some features might have fallbacks.", status='warning')

    while True:
        try:
            UI.print_header("Main Menu")
            print(
                f"    {Theme.BRIGHT}[1]{Theme.RESET} {Theme.PRIMARY}Spoofing Options{Theme.RESET} - Clean and spoof identifiers.")
            print(
                f"    {Theme.BRIGHT}[2]{Theme.RESET} {Theme.SECONDARY}Fixer Utilities{Theme.RESET} - Solve common Roblox errors.")
            print(
                f"    {Theme.BRIGHT}[3]{Theme.RESET} {Theme.SUCCESS}System Utilities{Theme.RESET} - Backups, logs, preflight checks.")
            print(f"    {Theme.BRIGHT}[0]{Theme.RESET} {Theme.MUTED}Exit{Theme.RESET}")

            choice = UI.get_input("Select a category")

            if choice == '1':
                run_spoofer_menu()
            elif choice == '2':
                run_fixer_menu()
            elif choice == '3':
                run_utilities_menu()
            elif choice == '0':
                UI.print_status("Exiting. Thanks for using ByGone!", 'info')
                break
            else:
                UI.print_status("Invalid selection. Please try again.", 'error')
                time.sleep(1)

        except (SystemExit, KeyboardInterrupt):
            print("\n")
            UI.print_status("Operation cancelled by user.", status='warning')
            break
        except Exception as e:
            UI.print_status(f"AN UNEXPECTED CRITICAL ERROR OCCURRED: {e}", status='error')
            import traceback
            traceback.print_exc()
            break  # Exit on critical error

    input(f"\n{Theme.MUTED}Press Enter to exit...{Theme.RESET}")


if __name__ == "__main__":
    main()
# Copyright (c) 2025 nitaybl. All Rights Reserved.