# Copyright (c) 2025 nitaybl. All Rights Reserved.
# ByGone System Info Collector - Debug Tool for User Issues

import os
import sys
import subprocess
import json
import platform
import socket
from datetime import datetime
from colorama import init, Fore, Style
import ctypes

# Initialize colorama
init(autoreset=True)


# --- UI & Theming (Matching ByGone Spoofer) ---
class Theme:
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
    LINE_H = '─'
    LINE_V = '│'
    CORNER_TL = '╭'
    CORNER_TR = '╮'
    CORNER_BL = '╰'
    CORNER_BR = '╯'
    WIDTH = 80

    @staticmethod
    def print_banner():
        banner_art = r"""
  ____        ____                   ____            _                   ___        __       
 | __ ) _   _/ ___| ___  _ __   ___ / ___| _   _ ___| |_ ___ _ __ ___   |_ _|_ __  / _| ___  
 |  _ \| | | | |  _ / _ \| '_ \ / _ \\___ \| | | / __| __/ _ \ '_ ` _ \   | || '_ \| |_ / _ \ 
 | |_) | |_| | |_| | (_) | | | |  __/___) | |_| \__ \ ||  __/ | | | | |  | || | | |  _| (_) |
 |____/ \__, |\____|\___/|_| |_|\___|____/ \__, |___/\__\___|_| |_| |_| |___|_| |_|_|  \___/ 
        |___/                               |___/                                              
"""
        print(f"{Theme.PRIMARY}{banner_art}{Theme.RESET}")
        title = "System Information Collector v1.1"
        subtitle = "Enhanced Report - Collects detailed system info for debugging"
        line = UI.LINE_H * (UI.WIDTH - 2)
        print(f"{Theme.PRIMARY}{UI.CORNER_TL}{line}{UI.CORNER_TR}{Theme.RESET}")
        print(f"{Theme.PRIMARY}{UI.LINE_V}{Theme.RESET} {Theme.BRIGHT}{title.center(UI.WIDTH - 4)}{Theme.RESET} {Theme.PRIMARY}{UI.LINE_V}{Theme.RESET}")
        print(f"{Theme.PRIMARY}{UI.LINE_V}{Theme.RESET} {Theme.MUTED}{subtitle.center(UI.WIDTH - 4)}{Theme.RESET} {Theme.PRIMARY}{UI.LINE_V}{Theme.RESET}")
        print(f"{Theme.PRIMARY}{UI.CORNER_BL}{line}{UI.CORNER_BR}{Theme.RESET}\n")

    @staticmethod
    def print_status(message, status='info', indent=1):
        prefix_map = {
            'info': (Theme.INFO, '[+]'),
            'success': (Theme.SUCCESS, '[✓]'),
            'warning': (Theme.WARNING, '[!]'),
            'error': (Theme.ERROR, '[!]'),
            'action': (Theme.SECONDARY, '[>]')
        }
        color, prefix = prefix_map.get(status, (Theme.MUTED, '[-]'))
        indent_str = "    " * indent
        print(f"{indent_str}{color}{prefix}{Theme.RESET} {message}")

    @staticmethod
    def print_header(text):
        padded_text = f" {text} "
        line_len = (UI.WIDTH - len(padded_text)) // 2
        line = UI.LINE_H * line_len
        print(f"\n{Theme.SECONDARY}{Theme.BRIGHT}{line}{padded_text}{line}{UI.LINE_H * (UI.WIDTH % 2)}{Theme.RESET}\n")


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def run_command(command):
    """Executes a command and returns the output."""
    try:
        result = subprocess.run(command, capture_output=True, text=True, shell=True, 
                              errors='replace', timeout=30)
        return result.stdout.strip() if result.stdout else ""
    except Exception as e:
        return f"Error: {e}"


def get_basic_system_info():
    """Collects basic system information."""
    UI.print_status("Collecting basic system information...", status='action')
    
    info = {
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "os_system": platform.system(),
        "os_release": platform.release(),
        "os_version": platform.version(),
        "architecture": platform.machine(),
        "processor": platform.processor(),
        "computer_name": socket.gethostname(),
        "python_version": platform.python_version(),
        "is_admin": is_admin()
    }
    
    UI.print_status(f"OS: {info['os_system']} {info['os_release']}", status='success', indent=2)
    UI.print_status(f"Architecture: {info['architecture']}", status='success', indent=2)
    return info


def get_cpu_info():
    """Collects CPU information."""
    UI.print_status("Collecting CPU information...", status='action')
    
    cpu_info = {}
    
    # Get CPU details from WMIC
    cpu_name = run_command("wmic cpu get name /format:list")
    cpu_cores = run_command("wmic cpu get NumberOfCores /format:list")
    cpu_threads = run_command("wmic cpu get NumberOfLogicalProcessors /format:list")
    cpu_id = run_command("wmic cpu get ProcessorId /format:list")
    
    cpu_info['cpu_name'] = cpu_name
    cpu_info['cpu_cores'] = cpu_cores
    cpu_info['cpu_threads'] = cpu_threads
    cpu_info['cpu_id'] = cpu_id
    
    UI.print_status(f"CPU: {cpu_name.split('=')[1] if '=' in cpu_name else 'Unknown'}", status='success', indent=2)
    return cpu_info


def get_motherboard_info():
    """Collects motherboard information (important for Asus detection)."""
    UI.print_status("Collecting motherboard information...", status='action')
    
    mb_info = {}
    
    # Motherboard details
    mb_manufacturer = run_command("wmic baseboard get Manufacturer /format:list")
    mb_product = run_command("wmic baseboard get Product /format:list")
    mb_version = run_command("wmic baseboard get Version /format:list")
    mb_serial = run_command("wmic baseboard get SerialNumber /format:list")
    
    # BIOS info
    bios_manufacturer = run_command("wmic bios get Manufacturer /format:list")
    bios_version = run_command("wmic bios get SMBIOSBIOSVersion /format:list")
    bios_serial = run_command("wmic bios get SerialNumber /format:list")
    
    mb_info['manufacturer'] = mb_manufacturer
    mb_info['product'] = mb_product
    mb_info['version'] = mb_version
    mb_info['serial_number'] = mb_serial
    mb_info['bios_manufacturer'] = bios_manufacturer
    mb_info['bios_version'] = bios_version
    mb_info['bios_serial'] = bios_serial
    
    # Check if it's an Asus motherboard
    is_asus = 'asus' in mb_manufacturer.lower() or 'asus' in mb_product.lower()
    mb_info['is_asus'] = is_asus
    
    manufacturer_str = mb_manufacturer.split('=')[1] if '=' in mb_manufacturer else 'Unknown'
    product_str = mb_product.split('=')[1] if '=' in mb_product else 'Unknown'
    
    UI.print_status(f"Motherboard: {manufacturer_str} {product_str}", status='success', indent=2)
    if is_asus:
        UI.print_status("⚠️  ASUS motherboard detected (may have HWID restrictions)", status='warning', indent=2)
    
    return mb_info


def get_gpu_info():
    """Collects graphics card information."""
    UI.print_status("Collecting GPU information...", status='action')
    
    gpu_info = {}
    
    # GPU details
    gpu_name = run_command("wmic path win32_VideoController get name /format:list")
    gpu_driver = run_command("wmic path win32_VideoController get DriverVersion /format:list")
    gpu_adapter_ram = run_command("wmic path win32_VideoController get AdapterRAM /format:list")
    gpu_status = run_command("wmic path win32_VideoController get Status /format:list")
    
    gpu_info['gpu_name'] = gpu_name
    gpu_info['gpu_driver_version'] = gpu_driver
    gpu_info['gpu_adapter_ram'] = gpu_adapter_ram
    gpu_info['gpu_status'] = gpu_status
    
    gpu_name_str = gpu_name.split('=')[1] if '=' in gpu_name else 'Unknown'
    UI.print_status(f"GPU: {gpu_name_str}", status='success', indent=2)
    
    return gpu_info


def get_memory_info():
    """Collects memory information."""
    UI.print_status("Collecting memory information...", status='action')
    
    mem_info = {}
    
    # Memory details
    total_memory = run_command("wmic computersystem get TotalPhysicalMemory /format:list")
    mem_modules = run_command("wmic memorychip get Capacity,Speed,Manufacturer /format:csv")
    
    mem_info['total_physical_memory'] = total_memory
    mem_info['memory_modules'] = mem_modules
    
    # Convert to GB if possible
    try:
        if '=' in total_memory:
            bytes_mem = int(total_memory.split('=')[1])
            gb_mem = bytes_mem / (1024**3)
            UI.print_status(f"Total RAM: {gb_mem:.2f} GB", status='success', indent=2)
    except:
        pass
    
    return mem_info


def get_disk_info():
    """Collects disk information."""
    UI.print_status("Collecting disk information...", status='action')
    
    disk_info = {}
    
    # Disk details
    disk_drives = run_command("wmic diskdrive get Model,Size,InterfaceType,SerialNumber /format:csv")
    logical_disks = run_command("wmic logicaldisk get DeviceID,FileSystem,FreeSpace,Size /format:csv")
    
    disk_info['physical_disks'] = disk_drives
    disk_info['logical_disks'] = logical_disks
    
    UI.print_status("Disk information collected", status='success', indent=2)
    return disk_info


def get_network_adapters():
    """Collects detailed network adapter information (critical for MAC spoofing issues)."""
    UI.print_status("Collecting network adapter information...", status='action')
    
    network_info = {}
    
    # Network adapter details
    adapters_basic = run_command("wmic nic get Name,NetConnectionID,MACAddress,Index /format:csv")
    adapters_detailed = run_command("wmic nicconfig get Description,IPAddress,MACAddress,DHCPEnabled,Index /format:csv")
    
    # Get adapter types and manufacturers
    adapter_manufacturers = run_command("wmic nic get Name,Manufacturer,AdapterType /format:csv")
    
    # Get current MAC addresses using getmac
    current_macs = run_command("getmac /v /fo csv")
    
    # Check for WiFi adapters specifically
    wifi_adapters = run_command("netsh wlan show interfaces")
    
    # Get all network interfaces
    ipconfig_all = run_command("ipconfig /all")
    
    network_info['adapters_basic'] = adapters_basic
    network_info['adapters_detailed'] = adapters_detailed
    network_info['adapter_manufacturers'] = adapter_manufacturers
    network_info['current_mac_addresses'] = current_macs
    network_info['wifi_interfaces'] = wifi_adapters
    network_info['ipconfig_all'] = ipconfig_all
    
    # Count adapters
    adapter_count = len([line for line in adapters_basic.split('\n') if line.strip() and 'Node' not in line])
    UI.print_status(f"Found {adapter_count} network adapter(s)", status='success', indent=2)
    
    # Check for wireless adapters
    if 'wireless' in wifi_adapters.lower() or 'wi-fi' in wifi_adapters.lower():
        UI.print_status("⚠️  Wireless adapter detected (may have MAC change limitations)", status='warning', indent=2)
    
    return network_info


def get_system_uuid():
    """Gets the system UUID."""
    UI.print_status("Collecting system UUID...", status='action')
    
    uuid_info = {}
    
    system_uuid = run_command("wmic csproduct get UUID /format:list")
    computer_system = run_command("wmic computersystem get Manufacturer,Model /format:csv")
    
    uuid_info['system_uuid'] = system_uuid
    uuid_info['computer_system'] = computer_system
    
    UI.print_status("System UUID collected", status='success', indent=2)
    return uuid_info


def get_installed_software():
    """Collects relevant installed software information."""
    UI.print_status("Collecting installed software information...", status='action')
    
    software_info = {}
    
    # Check for Roblox
    roblox_path = os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Roblox')
    software_info['roblox_installed'] = os.path.exists(roblox_path)
    
    # Check for antivirus/security software
    av_check = run_command("wmic /namespace:\\\\root\\SecurityCenter2 path AntiVirusProduct get displayName /format:list")
    software_info['antivirus'] = av_check
    
    # Check Windows Defender status
    defender_status = run_command("powershell Get-MpComputerStatus | Select-String 'RealTimeProtectionEnabled'")
    software_info['windows_defender_status'] = defender_status
    
    if software_info['roblox_installed']:
        UI.print_status("✓ Roblox is installed", status='success', indent=2)
    else:
        UI.print_status("⚠️  Roblox not found", status='warning', indent=2)
    
    return software_info


def get_running_processes():
    """Collects information about running processes (relevant ones)."""
    UI.print_status("Checking for relevant running processes...", status='action')
    
    process_info = {}
    
    # Check for Roblox processes
    tasklist = run_command("tasklist")
    
    roblox_processes = []
    if 'roblox' in tasklist.lower():
        for line in tasklist.split('\n'):
            if 'roblox' in line.lower():
                roblox_processes.append(line.strip())
    
    process_info['roblox_processes_running'] = roblox_processes
    process_info['all_processes'] = tasklist
    
    if roblox_processes:
        UI.print_status(f"Found {len(roblox_processes)} Roblox process(es) running", status='warning', indent=2)
    
    return process_info


def get_windows_version_details():
    """Gets detailed Windows version information."""
    UI.print_status("Collecting Windows version details...", status='action')
    
    win_info = {}
    
    # Get Windows version using systeminfo
    systeminfo = run_command("systeminfo | findstr /B /C:\"OS Name\" /C:\"OS Version\" /C:\"System Type\"")
    
    # Get Windows build
    winver = run_command("ver")
    
    # Get Windows product key type
    edition = run_command("wmic os get Caption /format:list")
    
    win_info['systeminfo'] = systeminfo
    win_info['version'] = winver
    win_info['edition'] = edition
    
    UI.print_status("Windows version collected", status='success', indent=2)
    return win_info


def check_system_issues():
    """Checks for common system issues that might affect the spoofer."""
    UI.print_status("Checking for potential system issues...", status='action')
    
    issues = []
    
    # Check if WMI service is running
    wmi_status = run_command("sc query winmgmt")
    if "RUNNING" not in wmi_status.upper():
        issues.append("WMI service is not running - This will cause spoofing to fail!")
    
    # Check disk space
    c_drive_space = run_command("wmic logicaldisk where \"DeviceID='C:'\" get FreeSpace /format:list")
    try:
        if '=' in c_drive_space:
            free_bytes = int(c_drive_space.split('=')[1])
            free_gb = free_bytes / (1024**3)
            if free_gb < 5:
                issues.append(f"Low disk space on C: drive ({free_gb:.2f} GB free)")
    except:
        pass
    
    # Check if user is admin
    if not is_admin():
        issues.append("Not running as administrator - Spoofing will fail!")
    
    return {"potential_issues": issues}


def parse_wmic_value(wmic_output, key_name):
    """Parses a WMIC output line like 'KeyName=Value' and returns the value."""
    try:
        if '=' in wmic_output:
            parts = wmic_output.split('=', 1)
            if len(parts) == 2:
                return parts[1].strip()
    except:
        pass
    return wmic_output.strip()


def generate_report(all_info):
    """Generates and saves the complete system report."""
    UI.print_header("Generating Report")
    
    # Create filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"bygone_system_info_{timestamp}.json"
    txt_filename = f"bygone_system_info_{timestamp}.txt"
    
    # Save JSON report
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(all_info, f, indent=4)
        UI.print_status(f"✓ JSON report saved: {os.path.abspath(filename)}", status='success')
    except Exception as e:
        UI.print_status(f"Error saving JSON: {e}", status='error')
    
    # Save human-readable text report
    try:
        with open(txt_filename, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("ByGone Spoofer - System Information Report\n")
            f.write("=" * 80 + "\n\n")
            f.write(f"Generated: {all_info['basic_info']['timestamp']}\n")
            f.write(f"Computer: {all_info['basic_info']['computer_name']}\n")
            f.write(f"Running as Admin: {all_info['basic_info']['is_admin']}\n\n")
            
            # Basic info
            f.write("-" * 80 + "\n")
            f.write("SYSTEM INFORMATION\n")
            f.write("-" * 80 + "\n")
            f.write(f"OS: {all_info['basic_info']['os_system']} {all_info['basic_info']['os_release']}\n")
            f.write(f"Version: {all_info['basic_info']['os_version']}\n")
            f.write(f"Architecture: {all_info['basic_info']['architecture']}\n")
            f.write(f"Processor: {all_info['basic_info']['processor']}\n\n")
            
            # CPU Info (parsed)
            f.write("-" * 80 + "\n")
            f.write("CPU INFORMATION\n")
            f.write("-" * 80 + "\n")
            cpu_name = parse_wmic_value(all_info['cpu_info']['cpu_name'], 'Name')
            cpu_cores = parse_wmic_value(all_info['cpu_info']['cpu_cores'], 'NumberOfCores')
            cpu_threads = parse_wmic_value(all_info['cpu_info']['cpu_threads'], 'NumberOfLogicalProcessors')
            f.write(f"Processor: {cpu_name}\n")
            f.write(f"Physical Cores: {cpu_cores}\n")
            f.write(f"Logical Processors: {cpu_threads}\n\n")
            
            # Motherboard (parsed)
            f.write("-" * 80 + "\n")
            f.write("MOTHERBOARD INFORMATION\n")
            f.write("-" * 80 + "\n")
            mb_manufacturer = parse_wmic_value(all_info['motherboard_info']['manufacturer'], 'Manufacturer')
            mb_product = parse_wmic_value(all_info['motherboard_info']['product'], 'Product')
            mb_version = parse_wmic_value(all_info['motherboard_info']['version'], 'Version')
            bios_version = parse_wmic_value(all_info['motherboard_info']['bios_version'], 'SMBIOSBIOSVersion')
            f.write(f"Manufacturer: {mb_manufacturer}\n")
            f.write(f"Model: {mb_product}\n")
            f.write(f"Version: {mb_version}\n")
            f.write(f"BIOS Version: {bios_version}\n")
            f.write(f"Is Asus: {all_info['motherboard_info']['is_asus']}\n")
            if all_info['motherboard_info']['is_asus']:
                f.write("⚠️  WARNING: ASUS motherboards may block HWID spoofing!\n")
            f.write("\n")
            
            # GPU Info (parsed)
            f.write("-" * 80 + "\n")
            f.write("GPU INFORMATION\n")
            f.write("-" * 80 + "\n")
            gpu_name = parse_wmic_value(all_info['gpu_info']['gpu_name'], 'Name')
            gpu_driver = parse_wmic_value(all_info['gpu_info']['gpu_driver_version'], 'DriverVersion')
            f.write(f"GPU: {gpu_name}\n")
            f.write(f"Driver Version: {gpu_driver}\n\n")
            
            # Memory (parsed)
            f.write("-" * 80 + "\n")
            f.write("MEMORY INFORMATION\n")
            f.write("-" * 80 + "\n")
            total_mem = parse_wmic_value(all_info['memory_info']['total_physical_memory'], 'TotalPhysicalMemory')
            try:
                total_mem_gb = int(total_mem) / (1024**3)
                f.write(f"Total RAM: {total_mem_gb:.2f} GB\n")
            except:
                f.write(f"Total RAM: {total_mem}\n")
            f.write("\n")
            
            # Network adapters (parsed better)
            f.write("-" * 80 + "\n")
            f.write("NETWORK ADAPTERS\n")
            f.write("-" * 80 + "\n")
            
            # Parse the adapters_basic CSV output
            adapters_basic = all_info['network_info']['adapters_basic']
            if adapters_basic:
                lines = [line.strip() for line in adapters_basic.split('\n') if line.strip()]
                adapter_count = 0
                for line in lines:
                    if 'Node' in line or not line:
                        continue
                    parts = line.split(',')
                    if len(parts) >= 5:
                        nic_index = parts[1].strip()
                        nic_mac = parts[2].strip()
                        nic_name = parts[3].strip()
                        nic_connection = parts[4].strip()
                        if nic_name and nic_name not in ['Node', '']:
                            adapter_count += 1
                            f.write(f"[{adapter_count}] {nic_name}\n")
                            if nic_connection:
                                f.write(f"    Connection: {nic_connection}\n")
                            if nic_mac:
                                f.write(f"    MAC Address: {nic_mac}\n")
                            else:
                                f.write(f"    MAC Address: (None/Virtual)\n")
                            f.write(f"    Index: {nic_index}\n")
                            
                            # Check if it's WiFi
                            if 'wireless' in nic_name.lower() or 'wi-fi' in nic_name.lower() or '802.11' in nic_name.lower():
                                f.write(f"    ⚠️  WARNING: Wireless adapter - MAC spoofing may not work!\n")
                            
                            f.write("\n")
                
                if adapter_count == 0:
                    f.write("No network adapters found.\n\n")
            else:
                f.write("No network adapter data collected.\n\n")
            
            # WiFi detection
            wifi_info = all_info['network_info']['wifi_interfaces']
            if 'no wireless interface' not in wifi_info.lower():
                f.write("-" * 80 + "\n")
                f.write("WIFI STATUS\n")
                f.write("-" * 80 + "\n")
                f.write(wifi_info + "\n\n")
            else:
                f.write("-" * 80 + "\n")
                f.write("WIFI STATUS\n")
                f.write("-" * 80 + "\n")
                f.write("No wireless interfaces detected.\n\n")
            
            # Potential issues
            if all_info['system_issues']['potential_issues']:
                f.write("-" * 80 + "\n")
                f.write("⚠️  POTENTIAL ISSUES DETECTED\n")
                f.write("-" * 80 + "\n")
                for issue in all_info['system_issues']['potential_issues']:
                    f.write(f"• {issue}\n")
                f.write("\n")
            else:
                f.write("-" * 80 + "\n")
                f.write("✓ NO ISSUES DETECTED\n")
                f.write("-" * 80 + "\n\n")
            
            # Roblox status
            f.write("-" * 80 + "\n")
            f.write("ROBLOX STATUS\n")
            f.write("-" * 80 + "\n")
            if all_info['installed_software']['roblox_installed']:
                f.write("✓ Roblox is installed\n")
            else:
                f.write("✗ Roblox is NOT installed\n")
            
            roblox_procs = all_info['running_processes']['roblox_processes_running']
            if roblox_procs:
                f.write(f"⚠️  {len(roblox_procs)} Roblox process(es) currently running:\n")
                for proc in roblox_procs[:3]:  # Show first 3
                    f.write(f"    {proc[:60]}\n")
            else:
                f.write("✓ No Roblox processes running\n")
            f.write("\n")
            
            f.write("-" * 80 + "\n")
            f.write("For complete details, see the JSON file.\n")
            f.write("-" * 80 + "\n")
        
        UI.print_status(f"✓ Text report saved: {os.path.abspath(txt_filename)}", status='success')
    except Exception as e:
        UI.print_status(f"Error saving text report: {e}", status='error')
        import traceback
        traceback.print_exc()
    
    return filename, txt_filename


def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    UI.print_banner()
    
    UI.print_status("This tool collects system information to help debug issues.", status='info')
    UI.print_status("It will NOT make any changes to your system.", status='success')
    print()
    
    if not is_admin():
        UI.print_status("⚠️  Running without administrator privileges.", status='warning')
        UI.print_status("Some information may be incomplete.", status='warning')
        print()
    
    input(f"{Theme.MUTED}Press Enter to start collecting system information...{Theme.RESET}")
    print()
    
    # Collect all information
    all_info = {}
    
    try:
        all_info['basic_info'] = get_basic_system_info()
        all_info['windows_details'] = get_windows_version_details()
        all_info['cpu_info'] = get_cpu_info()
        all_info['motherboard_info'] = get_motherboard_info()
        all_info['gpu_info'] = get_gpu_info()
        all_info['memory_info'] = get_memory_info()
        all_info['disk_info'] = get_disk_info()
        all_info['network_info'] = get_network_adapters()
        all_info['system_uuid'] = get_system_uuid()
        all_info['installed_software'] = get_installed_software()
        all_info['running_processes'] = get_running_processes()
        all_info['system_issues'] = check_system_issues()
        
        # Display any issues found
        if all_info['system_issues']['potential_issues']:
            print()
            UI.print_header("Potential Issues Detected")
            for issue in all_info['system_issues']['potential_issues']:
                UI.print_status(issue, status='error')
        
        print()
        json_file, txt_file = generate_report(all_info)
        
        print()
        UI.print_header("Collection Complete")
        UI.print_status("System information has been collected successfully!", status='success')
        UI.print_status(f"Share these files with support: {json_file} and {txt_file}", status='info')
        UI.print_status("Join discord.gg/bygone for support", status='info')
        
    except Exception as e:
        UI.print_status(f"An error occurred: {e}", status='error')
        import traceback
        traceback.print_exc()
    
    print()
    input(f"{Theme.MUTED}Press Enter to exit...{Theme.RESET}")


if __name__ == "__main__":
    main()

