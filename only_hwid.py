# Copyright (c) 2025 nitaybl. All Rights Reserved.
# A focused script to spoof SMBIOS UUID using local AMIDEWIN files.

import os
import sys
import ctypes
import subprocess
import shutil
import time
from colorama import init, Fore, Style

# Initialize colorama for colored console output
init(autoreset=True)

# --- CONFIGURATION ---
# The location of your local AMIDEWIN files.
SOURCE_AMIDEWIN_DIR = r"C:\Users\nitaybl\Pictures\AnyDesk"


# --- END CONFIGURATION ---

def is_admin():
    """Checks if the script is running with administrative privileges."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def restart_with_admin():
    """Restarts the script with administrative privileges."""
    try:
        script_path = sys.executable
        params = " ".join([sys.executable] + sys.argv)
        ctypes.windll.shell32.ShellExecuteW(None, "runas", script_path, " ".join(sys.argv), None, 1)
    except Exception as e:
        print(f"{Fore.RED}Failed to elevate privileges: {e}{Style.RESET_ALL}")
    sys.exit(0)


def run_shell_command(command_list, cwd=None, timeout=30):
    """A robust function to run external commands."""
    try:
        result = subprocess.run(
            command_list,
            capture_output=True,
            text=True,
            check=False,
            shell=False,
            errors='ignore',
            cwd=cwd,
            timeout=timeout
        )
        return result
    except FileNotFoundError:
        print(f"{Fore.RED}    Command not found: {command_list[0]}{Style.RESET_ALL}")
        return None
    except subprocess.TimeoutExpired:
        print(f"{Fore.YELLOW}    Command timed out: {' '.join(command_list)}{Style.RESET_ALL}")
        return None
    except Exception as e:
        print(f"{Fore.RED}    Shell command error: {e}{Style.RESET_ALL}")
        return None


def main():
    """Main execution function."""
    # 1. Ensure the script is running as an administrator
    if not is_admin():
        print(f"{Fore.YELLOW}Administrator privileges required. Attempting to restart as admin...")
        time.sleep(1)
        restart_with_admin()
        if not is_admin():
            print(f"{Fore.RED}[FATAL] Failed to acquire admin privileges. Exiting.{Style.RESET_ALL}")
            input("Press Enter to exit...")
            sys.exit(1)

    print(f"{Fore.GREEN}[✓] Running as administrator.")

    # Define the required files and the temporary directory for execution
    required_files = ["AMIDEWINx64.exe", "amigendrv64.sys", "amifldrv64.sys"]
    temp_exec_dir = os.path.join(os.environ.get('TEMP', r'C:\Windows\Temp'), "AmideWinSpoofer")

    try:
        # 2. Prepare files for execution
        print(f"{Fore.CYAN}[+] Preparing AMIDEWIN files...")

        if not os.path.isdir(SOURCE_AMIDEWIN_DIR):
            print(f"{Fore.RED}[!] Source directory not found: {SOURCE_AMIDEWIN_DIR}")
            raise FileNotFoundError

        for filename in required_files:
            if not os.path.exists(os.path.join(SOURCE_AMIDEWIN_DIR, filename)):
                print(f"{Fore.RED}[!] Required file not found: {filename} in {SOURCE_AMIDEWIN_DIR}")
                raise FileNotFoundError

        if os.path.exists(temp_exec_dir):
            shutil.rmtree(temp_exec_dir)
        os.makedirs(temp_exec_dir)

        for filename in required_files:
            shutil.copy2(os.path.join(SOURCE_AMIDEWIN_DIR, filename), temp_exec_dir)
        print(f"    {Fore.GREEN}[✓] Files prepared successfully in temporary directory.")

        # 3. Execute the spoofing command
        print(f"{Fore.CYAN}[+] Spoofing System UUID with AMIDEWIN...")
        exe_path = os.path.join(temp_exec_dir, "AMIDEWINx64.EXE")

        cmd_result = run_shell_command([exe_path, "/SU", "Auto"], cwd=temp_exec_dir)

        if cmd_result and cmd_result.returncode == 0:
            print(
                f"    {Fore.GREEN}{Style.BRIGHT}[✓] AMIDEWIN command executed successfully! RESTART IS CRITICAL.{Style.RESET_ALL}")

            # --- NEW SECTION: RESTART WMI SERVICE ---
            print(f"{Fore.CYAN}[+] Restarting Windows Management Instrumentation (WMI) service...")

            stop_result = run_shell_command(["net", "stop", "winmgmt", "/y"])
            if stop_result and stop_result.returncode == 0:
                print(f"    {Fore.GREEN}[✓] WMI service stopped successfully.")
            else:
                print(f"    {Fore.RED}[!] Failed to stop WMI service.")

            time.sleep(1)  # Brief pause before starting

            start_result = run_shell_command(["net", "start", "winmgmt"])
            if start_result and start_result.returncode == 0:
                print(f"    {Fore.GREEN}[✓] WMI service started successfully.")
            else:
                print(f"    {Fore.RED}[!] Failed to start WMI service.")
            # --- END NEW SECTION ---

        else:
            print(f"    {Fore.RED}[!] AMIDEWIN command failed.")
            if cmd_result:
                print(f"    Return Code: {cmd_result.returncode}")
                print(f"    Output:\n{cmd_result.stdout}\n{cmd_result.stderr}")

    except Exception as e:
        print(f"{Fore.RED}{Style.BRIGHT}\nAn unexpected error occurred: {e}")

    finally:
        # 4. Clean up the temporary files
        print(f"{Fore.CYAN}[+] Cleaning up temporary files...")
        if os.path.exists(temp_exec_dir):
            shutil.rmtree(temp_exec_dir, ignore_errors=True)
            print(f"    {Fore.GREEN}[✓] Cleanup complete.")
        else:
            print(f"    {Fore.YELLOW}[i] No cleanup needed.")

    print("\nOperation finished.")


if __name__ == "__main__":
    main()