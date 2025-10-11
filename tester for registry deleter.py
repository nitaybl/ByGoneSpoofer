import ctypes
import sys
import subprocess


def is_admin():
    """Checks if the script is running with administrator privileges."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def run_as_admin():
    """
    Re-runs the current script with administrator privileges if not already an admin.
    """
    # Re-run the script with "runas" verb to elevate privileges
    ctypes.windll.shell32.ShellExecuteW(
        None,  # Hwnd
        "runas",  # Operation: "runas" requests elevation
        sys.executable,  # File: the python interpreter
        " ".join(sys.argv),  # Parameters: the current script file
        None,  # Directory
        1  # Show command: 1 for normal
    )


def execute_powershell_commands():
    """
    Finds the current user's SID and executes two destructive PowerShell commands
    after a final user confirmation. This version checks if the key exists first.
    THIS IS AN EXTREMELY DESTRUCTIVE SCRIPT.
    """
    try:
        # Step 1: Get the current user's SID using a PowerShell command.
        print("Finding current user's Security Identifier (SID)...")
        get_sid_command = "([System.Security.Principal.WindowsIdentity]::GetCurrent()).User.Value"
        sid_result = subprocess.run(
            ["powershell", "-Command", get_sid_command],
            capture_output=True,
            text=True,
            check=True,  # Raise an exception if this command fails
            encoding='utf-8'
        )
        user_sid = sid_result.stdout.strip()
        if not user_sid.startswith("S-"):
            raise ValueError(f"Failed to retrieve a valid SID. Output: {user_sid}")
        print(f"User SID found: {user_sid}")

        # Step 2: Define the paths for the keys to be deleted.
        path1 = "HKCU:\\System\\CurrentControlSet\\Control"
        path2 = f"Registry::HKEY_USERS\\{user_sid}\\System\\CurrentControlSet\\Control"

        # FIX: Use Test-Path to check if the item exists before attempting to remove it.
        # This prevents "ItemNotFound" errors.
        command1 = f"if (Test-Path -Path '{path1}') {{ Remove-Item -Path '{path1}' -Recurse -Force }}"
        command2 = f"if (Test-Path -Path '{path2}') {{ Remove-Item -Path '{path2}' -Recurse -Force }}"

        # Step 3: Display strong warnings and get final confirmation.
        print("\n--- EXTREME DANGER ---")
        print("You are about to execute commands to delete critical registry keys.")
        print("This action will very likely corrupt your user profile and make it unusable.")
        print("\nThe script will attempt to delete the 'Control' key from HKCU and HKEY_USERS.")

        print("\nTo proceed, you must type 'YES' and press Enter. Any other input will cancel the operation.")

        confirm = input("> ")
        if confirm.strip().upper() == 'YES':
            print("\nConfirmation received. Executing commands...")

            # Step 4: Execute both commands.
            # Note: The second command will likely do nothing as the first one deletes the key.
            # This structure is maintained to fulfill the original request.
            commands_to_run = {"HKCU": command1, "HKEY_USERS": command2}
            all_successful = True

            for key, command in commands_to_run.items():
                print(f"\nExecuting check and delete for {key} location...")
                result = subprocess.run(
                    ["powershell", "-Command", command],
                    capture_output=True,
                    text=True,
                    check=False,  # Handle errors manually
                    encoding='utf-8'
                )

                if result.returncode == 0:
                    print("  ✅ Command executed successfully (key either deleted or did not exist).")
                else:
                    # This block should now only catch unexpected PowerShell errors.
                    print(f"  ❌ Command failed with exit code: {result.returncode}")
                    all_successful = False
                    if result.stderr:
                        print("  --- PowerShell Error ---")
                        print(result.stderr)

            if all_successful:
                print("\nAll commands completed without errors.")
            else:
                print("\nWarning: One or more commands failed unexpectedly.")

        else:
            print("\nOperation cancelled by user.")

    except subprocess.CalledProcessError as e:
        print("\n❌ CRITICAL ERROR: Failed to get user SID.")
        print("This may be due to a permissions issue or an unexpected system configuration.")
        print(f"--- PowerShell Error ---\n{e.stderr}")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")

    finally:
        # Keep the window open so the user can see the result.
        input("\nPress Enter to exit.")


if __name__ == "__main__":
    if is_admin():
        # If already admin, execute the main logic.
        execute_powershell_commands()
    else:
        # If not admin, try to re-run the script with elevated privileges.
        print("Administrator privileges required. Attempting to re-launch as admin...")
        try:
            run_as_admin()
        except Exception as e:
            print(f"Failed to elevate privileges: {e}")
            # Keep window open for user to see the error.
            input("Press Enter to exit.")
