import subprocess
import re
import random
import ctypes
import sys
import os

# --- ANSI Color Codes (for styling, similar to batch script) ---
class Color:
    YELLOW = '\033[93m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    END = '\033[0m'

# --- Configuration ---
REG_PATH = r"HKLM\SYSTEM\CurrentControlSet\Control\Class\{4d36e972-e325-11ce-bfc1-08002be10318}"
HEX_CHARS = "0123456789ABCDEF"
# Second char of first octet for some wireless NICs
SECOND_CHAR_OPTIONS = "AE26"

# --- Helper Functions ---

def is_admin():
    """Checks if the script is running with administrator privileges."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_command(command, shell=True, capture_output=True, text=True, check=False):
    """Executes a system command."""
    try:
        result = subprocess.run(command, shell=shell, capture_output=capture_output, text=text, check=check, errors='ignore')
        return result
    except subprocess.CalledProcessError as e:
        print(f"{Color.RED}[!] Error executing command: {' '.join(command) if isinstance(command, list) else command}{Color.END}")
        print(f"{Color.RED}    {e}{Color.END}")
        return None
    except FileNotFoundError as e:
        print(f"{Color.RED}[!] Command not found: {e.filename}{Color.END}")
        return None

def clear_screen():
    """Clears the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_nics():
    """Enumerates available Network Interface Controllers (NICs)."""
    nics = []
    try:
        # Using WMIC to get NetConnectionId, similar to the batch script
        # We skip the header and handle potential empty lines or non-NIC entries
        process = run_command('wmic nic get NetConnectionId /format:csv', capture_output=True, text=True)
        if process and process.stdout:
            lines = process.stdout.strip().split('\n')
            for line in lines:
                parts = line.split(',')
                if len(parts) > 1 and parts[1].strip(): # Ensure there's a NetConnectionId
                    nic_name = parts[1].strip()
                    if nic_name != "NetConnectionID": # Skip header
                        nics.append(nic_name)
    except Exception as e:
        print(f"{Color.RED}[!] Error enumerating NICs: {e}{Color.END}")
    return nics

def get_nic_index(network_adapter_name):
    """Retrieves the device index for a given NIC's NetConnectionId."""
    try:
        # Using "NetConnectionID" as it's more consistently available and used in the batch
        command = f'wmic nic where "NetConnectionID=\'{network_adapter_name}\'" get Index /format:value'
        process = run_command(command)
        if process and process.stdout:
            match = re.search(r"Index=(\d+)", process.stdout)
            if match:
                return match.group(1) # WMIC Index is usually what's needed for the registry path
    except Exception as e:
        print(f"{Color.RED}[!] Error getting NIC index for '{network_adapter_name}': {e}{Color.END}")
    return None


def get_current_mac(nic_index):
    """Retrieves the current MAC address of a NIC using its system index."""
    if not nic_index:
        return "N/A"
    try:
        # WMIC uses the 'Index' property that corresponds to the registry key subfolder
        command = f'wmic nic where "Index={nic_index}" get MACAddress /format:value'
        process = run_command(command)
        if process and process.stdout:
            match = re.search(r"MACAddress=([0-9A-Fa-f:]+)", process.stdout)
            if match:
                return match.group(1).upper()
    except Exception as e:
        print(f"{Color.RED}[!] Error retrieving MAC address for index {nic_index}: {e}{Color.END}")
    return "N/A"


def generate_random_mac():
    """Generates a random MAC address."""
    mac_parts = [
        random.choice(HEX_CHARS) + random.choice(SECOND_CHAR_OPTIONS) # Ensure second char is one of AE26
    ]
    for _ in range(5): # Remaining 5 octets
        mac_parts.append(random.choice(HEX_CHARS) + random.choice(HEX_CHARS))
    mac_address_no_colons = "".join(mac_parts)
    mac_address_with_colons = ":".join(mac_parts)
    return mac_address_no_colons, mac_address_with_colons

def set_mac_address(nic_name, nic_index, mac_address_no_colons):
    """Sets the MAC address for the selected NIC."""
    if not nic_index:
        print(f"{Color.RED}[!] Cannot set MAC address: NIC index not found for {nic_name}.{Color.END}")
        return False
    registry_key = rf"{REG_PATH}\{nic_index.zfill(4)}" # Index is often 000X, 00XX etc.

    print(f"{Color.YELLOW}[i] Disabling network adapter: {nic_name}...{Color.END}")
    run_command(f'netsh interface set interface "{nic_name}" admin=disable')

    print(f"{Color.YELLOW}[i] Setting MAC address in registry: {mac_address_no_colons}...{Color.END}")
    # Use full path to reg.exe for robustness
    reg_add_command = [
        "reg", "add", registry_key,
        "/v", "NetworkAddress",
        "/t", "REG_SZ",
        "/d", mac_address_no_colons,
        "/f"
    ]
    result = run_command(reg_add_command, shell=False) # shell=False for list of args

    print(f"{Color.YELLOW}[i] Enabling network adapter: {nic_name}...{Color.END}")
    run_command(f'netsh interface set interface "{nic_name}" admin=enable')

    if result and result.returncode == 0:
        return True
    else:
        print(f"{Color.RED}[!] Failed to set MAC address in registry.{Color.END}")
        if result:
            print(f"{Color.RED}    Output: {result.stdout}{Color.END}")
            print(f"{Color.RED}    Error: {result.stderr}{Color.END}")
        return False

def revert_mac_address(nic_name, nic_index):
    """Reverts the MAC address to its original factory default."""
    if not nic_index:
        print(f"{Color.RED}[!] Cannot revert MAC address: NIC index not found for {nic_name}.{Color.END}")
        return False
    registry_key = rf"{REG_PATH}\{nic_index.zfill(4)}"

    print(f"{Color.YELLOW}[i] Disabling network adapter: {nic_name}...{Color.END}")
    run_command(f'netsh interface set interface "{nic_name}" admin=disable')

    print(f"{Color.YELLOW}[i] Deleting NetworkAddress from registry...{Color.END}")
    reg_delete_command = [
        "reg", "delete", registry_key,
        "/v", "NetworkAddress",
        "/f"
    ]
    result = run_command(reg_delete_command, shell=False)

    print(f"{Color.YELLOW}[i] Enabling network adapter: {nic_name}...{Color.END}")
    run_command(f'netsh interface set interface "{nic_name}" admin=enable')

    # The batch script also restarts winmgmt, which can sometimes help apply changes.
    # This can be aggressive and might not always be necessary.
    # print(f"{Color.YELLOW}[i] Restarting WMI service (winmgmt)...{Color.END}")
    # run_command('powershell Restart-Service -Force -Name "winmgmt"', shell=True) # shell=True for powershell

    if result and result.returncode == 0:
        return True
    else:
        # It's possible the value wasn't there, which is fine for a revert.
        # We check if the command execution itself failed unexpectedly.
        if result and result.stderr and "The system was unable to find the specified registry key or value" not in result.stderr :
            print(f"{Color.RED}[!] Failed to delete NetworkAddress from registry.{Color.END}")
            print(f"{Color.RED}    Output: {result.stdout}{Color.END}")
            print(f"{Color.RED}    Error: {result.stderr}{Color.END}")
            return False
        return True # Assume success if the value wasn't found (already reverted) or deletion was successful

def revise_networking():
    """Releases, renews IP, and clears ARP cache."""
    print(f"\n{Color.GREEN}# Revising networking configurations...{Color.END}")
    print(f"{Color.YELLOW}[i] Releasing IP address...{Color.END}")
    run_command("ipconfig /release", shell=True, capture_output=False)
    print(f"{Color.YELLOW}[i] Clearing ARP cache...{Color.END}")
    run_command("arp -d *", shell=True, capture_output=False)
    print(f"{Color.YELLOW}[i] Renewing IP address...{Color.END}")
    run_command("ipconfig /renew", shell=True, capture_output=False)
    print(f"{Color.GREEN}# Networking revision complete.{Color.END}")
    input(f"{Color.MAGENTA}# Press Enter to continue...{Color.END}")

# --- Main Application Flow ---

def selection_menu():
    """Displays the NIC selection menu."""
    while True:
        clear_screen()
        print(f"\n  {Color.MAGENTA}[i] Input NIC # to modify.{Color.END}\n")
        adapters = get_nics()
        if not adapters:
            print(f"  {Color.RED}[!] No network adapters found or error retrieving them.{Color.END}")
            print(f"  {Color.YELLOW}    Make sure WMIC is working and accessible.{Color.END}")
            input(f"\n{Color.MAGENTA}# Press Enter to exit...{Color.END}")
            sys.exit(1)

        for i, adapter_name in enumerate(adapters):
            print(f"  {Color.CYAN}{i+1}{Color.END} - {adapter_name}")

        print(f"\n  {Color.CYAN}99{Color.END} - Revise Networking\n")
        try:
            choice = input(f"  {Color.MAGENTA}# {Color.END}").strip()
            if not choice: continue # Handle empty input

            selection = int(choice)
            if 1 <= selection <= len(adapters):
                return adapters[selection - 1]
            elif selection == 99:
                revise_networking()
                # Loop back to selection menu after revising
            else:
                print(f"\n  {Color.RED}[!] \"{selection}\" is an invalid option.{Color.END}")
                input(f"{Color.MAGENTA}# Press Enter to try again...{Color.END}")
        except ValueError:
            print(f"\n  {Color.RED}[!] \"{choice}\" is an invalid option. Please enter a number.{Color.END}")
            input(f"{Color.MAGENTA}# Press Enter to try again...{Color.END}")
        except Exception as e:
            print(f"\n  {Color.RED}[!] An unexpected error occurred: {e}{Color.END}")
            input(f"{Color.MAGENTA}# Press Enter to try again...{Color.END}")


def action_menu(network_adapter_name):
    """Displays the action menu for the selected NIC."""
    nic_system_index = get_nic_index(network_adapter_name)
    if not nic_system_index:
        print(f"\n  {Color.RED}[!] Could not determine the system index for '{network_adapter_name}'.{Color.END}")
        print(f"  {Color.YELLOW}    Cannot proceed with MAC operations for this adapter.{Color.END}")
        input(f"{Color.MAGENTA}# Press Enter to return to NIC selection...{Color.END}")
        return True # Go back to selection menu

    while True:
        clear_screen()
        current_mac_on_nic = get_current_mac(nic_system_index) # Get potentially spoofed MAC
        print(f"\n  {Color.MAGENTA}[i] Input action # to perform.{Color.END}\n")
        print(f"  {Color.CYAN}> Selected NIC : {Color.END}{network_adapter_name}")
        print(f"  {Color.CYAN}> Current MAC  : {Color.END}{current_mac_on_nic}\n")
        print(f"  {Color.CYAN}1{Color.END} - Randomize MAC address")
        print(f"  {Color.CYAN}2{Color.END} - Customize MAC address")
        print(f"  {Color.CYAN}3{Color.END} - Revert MAC address to original")
        print(f"\n  {Color.CYAN}0{Color.END} < Menu\n")

        choice = input(f"  {Color.MAGENTA}# {Color.END}").strip()

        if choice == '1':
            spoof_mac_random(network_adapter_name, nic_system_index, current_mac_on_nic)
        elif choice == '2':
            spoof_mac_custom(network_adapter_name, nic_system_index, current_mac_on_nic)
        elif choice == '3':
            revert_mac_and_display(network_adapter_name, nic_system_index, current_mac_on_nic)
        elif choice == '0':
            return True # Go back to selection menu
        else:
            print(f"\n  {Color.RED}[!] \"{choice}\" is an invalid option.{Color.END}")
            input(f"{Color.MAGENTA}# Press Enter to try again...{Color.END}")

def spoof_mac_random(nic_name, nic_index, previous_mac):
    """Handles random MAC address spoofing."""
    clear_screen()
    print(f"\n  {Color.CYAN}> Selected NIC : {Color.END}{nic_name}")
    print(f"  {Color.CYAN}> Previous MAC : {Color.END}{previous_mac}\n")

    new_mac_no_colons, new_mac_print = generate_random_mac()
    print(f"  {Color.CYAN}> Modified MAC : {Color.END}{new_mac_print}")

    if set_mac_address(nic_name, nic_index, new_mac_no_colons):
        print(f"\n  {Color.MAGENTA}[i] MAC address successfully spoofed.{Color.END}")
    else:
        print(f"\n  {Color.RED}[!] MAC address spoofing failed.{Color.END}")
    input(f"\n{Color.MAGENTA}# Press Enter to continue...{Color.END}")

def spoof_mac_custom(nic_name, nic_index, current_mac):
    """Handles custom MAC address spoofing."""
    clear_screen()
    print(f"\n  {Color.CYAN}> Selected NIC : {Color.END}{nic_name}")
    print(f"  {Color.CYAN}> Current MAC  : {Color.END}{current_mac}\n")
    print(f"  {Color.MAGENTA}[i] Enter a custom MAC address (e.g., 001122AABBCC).")
    print(f"  {Color.MAGENTA}    Only use hex characters: 0-9 A-F{Color.END}\n")

    while True:
        custom_mac_input = input(f"  {Color.MAGENTA}# {Color.END}").upper().replace(":", "").replace("-", "")
        if not custom_mac_input:
            print(f"\n  {Color.RED}[!] Invalid entry; MAC address cannot be empty.{Color.END}")
            input(f"{Color.MAGENTA}# Press Enter to try again...{Color.END}")
            # Redraw screen
            clear_screen()
            print(f"\n  {Color.CYAN}> Selected NIC : {Color.END}{nic_name}")
            print(f"  {Color.CYAN}> Current MAC  : {Color.END}{current_mac}\n")
            print(f"  {Color.MAGENTA}[i] Enter a custom MAC address (e.g., 001122AABBCC).")
            print(f"  {Color.MAGENTA}    Only use hex characters: 0-9 A-F{Color.END}\n")
            continue
        if len(custom_mac_input) != 12:
            print(f"\n  {Color.RED}[!] Invalid entry; MAC address must be 12 hexadecimal characters.{Color.END}")
            input(f"{Color.MAGENTA}# Press Enter to try again...{Color.END}")
            # Redraw screen
            clear_screen()
            print(f"\n  {Color.CYAN}> Selected NIC : {Color.END}{nic_name}")
            print(f"  {Color.CYAN}> Current MAC  : {Color.END}{current_mac}\n")
            print(f"  {Color.MAGENTA}[i] Enter a custom MAC address (e.g., 001122AABBCC).")
            print(f"  {Color.MAGENTA}    Only use hex characters: 0-9 A-F{Color.END}\n")
            continue
        if not all(c in HEX_CHARS for c in custom_mac_input):
            print(f"\n  {Color.RED}[!] Invalid entry; MAC address must contain only hexadecimal characters.{Color.END}")
            input(f"{Color.MAGENTA}# Press Enter to try again...{Color.END}")
            # Redraw screen
            clear_screen()
            print(f"\n  {Color.CYAN}> Selected NIC : {Color.END}{nic_name}")
            print(f"  {Color.CYAN}> Current MAC  : {Color.END}{current_mac}\n")
            print(f"  {Color.MAGENTA}[i] Enter a custom MAC address (e.g., 001122AABBCC).")
            print(f"  {Color.MAGENTA}    Only use hex characters: 0-9 A-F{Color.END}\n")
            continue
        break

    mac_address_print = ":".join(custom_mac_input[i:i+2] for i in range(0, 12, 2))
    print(f"\n  {Color.CYAN}> Modified MAC : {Color.END}{mac_address_print}")

    if set_mac_address(nic_name, nic_index, custom_mac_input):
        print(f"\n  {Color.MAGENTA}[i] MAC address successfully customized.{Color.END}")
    else:
        print(f"\n  {Color.RED}[!] Custom MAC address setting failed.{Color.END}")
    input(f"\n{Color.MAGENTA}# Press Enter to continue...{Color.END}")


def revert_mac_and_display(nic_name, nic_index, modified_mac_before_revert):
    """Handles reverting MAC address and displays the result."""
    clear_screen()
    print(f"\n  {Color.CYAN}> Selected NIC : {Color.END}{nic_name}")
    print(f"  {Color.CYAN}> Modified MAC : {Color.END}{modified_mac_before_revert}\n")

    if revert_mac_address(nic_name, nic_index):
        # Important: After reverting, we need to get the *new* current MAC.
        # The NIC needs a moment to reflect the change after re-enabling.
        # A small delay might be useful in some edge cases, but usually,
        # the next call to get_current_mac should be sufficient if the revert worked.
        # For robustness, one might add a small time.sleep(2) here.
        reverted_mac = get_current_mac(nic_index)
        print(f"  {Color.CYAN}> Reverted MAC : {Color.END}{reverted_mac}\n")
        if modified_mac_before_revert == reverted_mac and modified_mac_before_revert != "N/A":
             # This comparison might be tricky if the "modified_mac_before_revert" was already the original
             # or if there was an issue reading the MAC initially.
             # A more reliable check is if the registry key is gone and the MAC is readable.
            print(f"  {Color.MAGENTA}[i] Original MAC address likely already set or change not reflected immediately.{Color.END}")
            print(f"  {Color.YELLOW}    The 'NetworkAddress' registry key has been removed.{Color.END}")

        else:
            print(f"  {Color.MAGENTA}[i] MAC address successfully reverted to original (or registry entry removed).{Color.END}")
    else:
        print(f"\n  {Color.RED}[!] MAC address reversion failed.{Color.END}")
    input(f"\n{Color.MAGENTA}# Press Enter to continue...{Color.END}")


def main():
    """Main function to run the MAC address spoofer."""
    ctypes.windll.kernel32.SetConsoleTitleW("Python MAC Address Spoofer")

    if not is_admin():
        print(f"\n  {Color.YELLOW}# Administrator privileges are required.{Color.END}\n")
        # Attempt to re-run as admin
        # This is a common way but might show a UAC prompt for the script path itself
        try:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        except Exception as e:
            print(f"  {Color.RED}[!] Failed to elevate privileges: {e}{Color.END}")
            print(f"  {Color.YELLOW}    Please run this script as an Administrator.{Color.END}")
            input(f"{Color.MAGENTA}# Press Enter to exit...{Color.END}")
        sys.exit(1)

    while True:
        selected_nic = selection_menu()
        if selected_nic:
            go_back_to_main_menu = action_menu(selected_nic)
            if not go_back_to_main_menu: # Should not happen if action_menu always returns True
                break
        else: # Should not happen if selection_menu handles errors and exits
            break

if __name__ == "__main__":
    # Initialize colorama for Windows if you want to ensure ANSI codes work in older cmd.exe
    # from colorama import init
    # init(autoreset=True) # if you use colorama
    main()