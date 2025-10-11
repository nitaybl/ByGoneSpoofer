# bygone_webview2_fixer.py
# A tiny “Bygone-styled” console utility to nuke Roblox WebView2 data
# and optionally set a safe per-user WebView2 folder.
#
# Requires: Python 3.8+; optional 'colorama' (for colors). Pack with PyInstaller.

import os
import sys
import shutil
import subprocess
import ctypes
import time
from pathlib import Path
from glob import glob

# --- pretty colors (optional) ---
try:
    from colorama import init as colorama_init, Fore, Style
    colorama_init(autoreset=True)
    C_OK = Fore.GREEN
    C_WARN = Fore.YELLOW
    C_BAD = Fore.RED
    C_INFO = Fore.CYAN
    C_DIM = Style.DIM
    C_RESET = Style.RESET_ALL
except Exception:
    C_OK = C_WARN = C_BAD = C_INFO = C_DIM = C_RESET = ""

BANNER = rf"""
{C_INFO}{C_DIM}==============================================={C_RESET}
{C_INFO}   BYGONE // Roblox WebView2 Fixer (Console){C_RESET}
{C_INFO}{C_DIM}==============================================={C_RESET}
"""

SAFE_USER_DATA = str(Path(os.environ.get("LOCALAPPDATA", Path.home())) / "Roblox" / "EBWebView")
VERSIONS_ROOT = r"C:\Program Files (x86)\Roblox\Versions"

# --- admin helpers ---
def is_admin() -> bool:
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False

def relaunch_as_admin():
    params = " ".join([f'"{a}"' for a in sys.argv])
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 1)
    sys.exit(0)

# --- util ---
def println(msg, color=C_INFO):
    print(color + msg + C_RESET)

def kill_roblox():
    # Kill common Roblox processes (best effort)
    for name in ["RobloxPlayerBeta.exe", "RobloxPlayerLauncher.exe", "RobloxCrashHandler.exe", "RobloxInstaller.exe"]:
        subprocess.run(["taskkill", "/F", "/IM", name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)

def find_latest_version_dir() -> Path:
    cand = []
    root = Path(VERSIONS_ROOT)
    if not root.exists():
        return None
    for p in root.iterdir():
        if p.is_dir() and p.name.startswith("version-"):
            cand.append((p.stat().st_mtime, p))
    if not cand:
        return None
    cand.sort(reverse=True)
    return cand[0][1]

def webview2_target_path(version_dir: Path) -> Path:
    return version_dir / "RobloxPlayerBeta.exe.WebView2"

def nuke_path(target: Path) -> None:
    if not target.exists():
        println(f"[OK] Nothing to delete at: {target}", C_OK)
        return
    # If it's a file, remove it; if dir, rmtree
    try:
        if target.is_file():
            os.chmod(target, 0o666)
            target.unlink()
        else:
            # make writable
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
        println(f"[NUKED] {target}", C_OK)
    except Exception as e:
        println(f"[ERROR] Could not delete {target}: {e}", C_BAD)
        raise

def ensure_dir(p: Path):
    p.mkdir(parents=True, exist_ok=True)

def set_user_env_var(name: str, value: str):
    # Persist for the current user
    subprocess.run(["setx", name, value], shell=True, check=False,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    # Also set for this process so future child procs can see it
    os.environ[name] = value

def clear_user_env_var(name: str):
    # Delete by setting to empty string; Windows env doesn’t really delete via setx,
    # but empty disables it effectively. (You can also remove via registry; keeping it simple.)
    subprocess.run(["setx", name, ""], shell=True, check=False,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.environ.pop(name, None)

# --- features ---
def action_nuke():
    println("Killing Roblox processes…")
    kill_roblox()
    vdir = find_latest_version_dir()
    if not vdir:
        println("Couldn’t find Roblox \\Versions directory. Is Roblox installed?", C_BAD)
        return
    target = webview2_target_path(vdir)
    println(f"Targeting: {target}")
    nuke_path(target)
    println("Done. Launch Roblox and it will rebuild the WebView2 data. ✅", C_OK)

def action_set_safe_env():
    println("Pointing WebView2 to a user-writable folder…")
    ensure_dir(Path(SAFE_USER_DATA))
    set_user_env_var("WEBVIEW2_USER_DATA_FOLDER", SAFE_USER_DATA)
    println(f"WEBVIEW2_USER_DATA_FOLDER = {SAFE_USER_DATA}", C_OK)
    println("Sign out/in (or reboot) for all apps to pick this up.", C_WARN)

def action_clear_env():
    println("Clearing WEBVIEW2_USER_DATA_FOLDER for the user…")
    clear_user_env_var("WEBVIEW2_USER_DATA_FOLDER")
    println("Cleared. Apps will fallback to default behavior next launch.", C_OK)

def action_break_on_purpose():
    println("Simulating the error by creating a blocking FILE named ‘RobloxPlayerBeta.exe.WebView2’…", C_WARN)
    kill_roblox()
    vdir = find_latest_version_dir()
    if not vdir:
        println("Couldn’t find Roblox \\Versions directory. Is Roblox installed?", C_BAD)
        return
    target = webview2_target_path(vdir)
    try:
        if target.exists():
            nuke_path(target)  # remove folder/file first
        with open(target, "wb") as f:
            f.write(b"bygone-lock")
        # Make it read-only for extra spice
        os.chmod(target, 0o444)
        println(f"Created blocking file: {target}", C_OK)
        println("Now launch Roblox → you should get the WebView2 data directory error. 🧪", C_INFO)
    except Exception as e:
        println(f"[ERROR] Could not create blocking file: {e}", C_BAD)

def main():
    if os.name != "nt":
        println("This tool is Windows-only.", C_BAD)
        sys.exit(1)

    print(BANNER)
    if not is_admin():
        println("Admin rights are required to modify Program Files safely.", C_WARN)
        println("Re-launching with UAC…")
        time.sleep(0.8)
        relaunch_as_admin()

    while True:
        println("\nChoose your move:")
        print(f"{C_INFO}[1]{C_RESET} NUKE Roblox WebView2 data (recommended)")
        print(f"{C_INFO}[2]{C_RESET} Set safe user data folder (per-user) → {SAFE_USER_DATA}")
        print(f"{C_INFO}[3]{C_RESET} Clear WEBVIEW2_USER_DATA_FOLDER (undo #2)")
        print(f"{C_INFO}[4]{C_RESET} Recreate the error (make a blocking file)")
        print(f"{C_INFO}[0]{C_RESET} Exit")

        choice = input(f"{C_DIM}> {C_RESET}").strip()
        try:
            if choice == "1":
                action_nuke()
            elif choice == "2":
                action_set_safe_env()
            elif choice == "3":
                action_clear_env()
            elif choice == "4":
                action_break_on_purpose()
            elif choice == "0":
                println("Bye.", C_INFO)
                break
            else:
                println("Pick 0–4.", C_WARN)
        except KeyboardInterrupt:
            println("\nInterrupted.", C_WARN)
        except Exception as e:
            println(f"Unexpected error: {e}", C_BAD)

if __name__ == "__main__":
    main()