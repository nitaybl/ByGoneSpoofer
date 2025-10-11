import dearpygui.dearpygui as dpg
from colorama import Fore, Style

import backend_spoofer  # Your backend script
import threading
import time
import sys
import io
import webbrowser
import os

from ByGoneSpoofer import BANNER, restart_with_admin, is_admin, PYWIN32_AVAILABLE, perform_all_spoofing_operations

# --- Constants for UI ---
WINDOW_WIDTH = 700
WINDOW_HEIGHT = 550  # Increased height for logs
LOG_MAX_LINES = 1000

# --- UI State ---
ui_log_content = ""
current_action_thread = None


# --- Backend Function Safety Wrappers (to call them if they exist) ---
def call_backend(func_name, *args):
    global ui_log_content
    log_to_ui(f"[INFO] Attempting to call backend function: {func_name}")
    if hasattr(backend_spoofer, func_name):
        try:
            func = getattr(backend_spoofer, func_name)
            func(*args)
            log_to_ui(f"[SUCCESS] Backend function {func_name} executed.")
        except Exception as e:
            log_to_ui(f"[ERROR] Exception during {func_name}: {e}")
            import traceback
            log_to_ui(traceback.format_exc())
    else:
        log_to_ui(f"[ERROR] Backend function {func_name} not found in backend_spoofer.py.")


def run_backend_action_threaded(func_name, *args):
    global current_action_thread
    if current_action_thread and current_action_thread.is_alive():
        log_to_ui("[WARNING] Another action is already in progress. Please wait.")
        return

    log_to_ui(f"[ACTION] Starting: {func_name}")
    dpg.show_item("loading_indicator_popup")  # Show loading indicator

    def target_wrapper():
        global current_action_thread
        call_backend(func_name, *args)
        log_to_ui(f"[ACTION] Finished: {func_name}")
        dpg.hide_item("loading_indicator_popup")  # Hide loading indicator
        current_action_thread = None

    current_action_thread = threading.Thread(target=target_wrapper)
    current_action_thread.daemon = True  # Allow main program to exit even if thread is running
    current_action_thread.start()


# --- UI Log ---
def log_to_ui(message):
    global ui_log_content
    timestamp = time.strftime("%H:%M:%S")
    new_log_entry = f"[{timestamp}] {message}\n"

    # Prepend to keep newest at top, or append for chronological
    ui_log_content += new_log_entry  # Append for chronological

    # Limit log lines (optional, can be slow with very frequent updates)
    lines = ui_log_content.splitlines()
    if len(lines) > LOG_MAX_LINES:
        ui_log_content = "\n".join(lines[-LOG_MAX_LINES:]) + "\n"

    if dpg.does_item_exist("log_text_area"):
        dpg.set_value("log_text_area", ui_log_content)
        # Attempt to scroll to the bottom of the log (may not always work perfectly with set_value)
        # For DearPyGui 1.x, direct scroll control is limited.
        # Consider using a child window with auto_scroll_x/y if you need more robust scrolling.


# --- Redirect print to UI log ---
class UILogger(io.StringIO):
    def write(self, s):
        # Filter out colorama escape codes if present or handle them
        # For now, just pass it through, knowing colors won't render
        log_to_ui(s.rstrip())  # rstrip to avoid double newlines from print
        super().write(s)  # Call super if you want it to also go to an actual StringIO buffer


# --- UI Callbacks ---
def open_instructions_url():
    log_to_ui("[INFO] Opening instructions URL: http://vixenwoofer.xyz/")
    webbrowser.open("http://vixenwoofer.xyz/")


def fetch_and_display_system_info():
    log_to_ui("[INFO] Fetching system information (placeholders)...")
    # Placeholder: Implement functions in Python to get this info
    # e.g., using wmi, subprocess, psutil
    mobo_manufacturer = "N/A (Implement backend_spoofer.get_mobo_manufacturer())"
    mobo_model = "N/A (Implement backend_spoofer.get_mobo_model())"
    bios_serial = "N/A (Implement backend_spoofer.get_bios_serial())"
    system_uuid = "N/A (Implement backend_spoofer.get_system_uuid())"
    mac_address = "N/A (Implement backend_spoofer.get_mac_address())"
    tpm_status_str = "N/A (Implement backend_spoofer.get_tpm_status())"

    if dpg.does_item_exist("mobo_manufacturer_text"):
        dpg.set_value("mobo_manufacturer_text", f"Motherboard Manufacturer: {mobo_manufacturer}")
        dpg.set_value("mobo_model_text", f"Motherboard Model: {mobo_model}")
        dpg.set_value("bios_serial_text", f"BIOS Serial: {bios_serial}")
        dpg.set_value("system_uuid_text", f"System UUID: {system_uuid}")
        dpg.set_value("mac_address_text", f"Primary MAC: {mac_address}")
        dpg.set_value("tpm_status_text", f"TPM Status: {tpm_status_str}")
    log_to_ui("[INFO] System information display updated (with placeholders).")


# --- UI Theme and Font Setup (Basic) ---
def setup_theme_and_fonts():
    # Colors (approximating your C++ UI's `colors` namespace)
    color_main_purple = (68, 61, 160, 255)
    color_dark_gray = (40, 40, 40, 255)
    color_bg_main = (7, 7, 7, 225)
    color_text_light = (200, 200, 200, 255)
    color_text_header = (220, 220, 220, 255)
    color_button = color_main_purple
    color_button_hovered = (88, 81, 180, 255)
    color_button_active = (58, 51, 150, 255)

    with dpg.theme() as global_theme:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg, color_bg_main)
            dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (20, 20, 20, 255))  # Darker child bg
            dpg.add_theme_color(dpg.mvThemeCol_Text, color_text_light)
            dpg.add_theme_color(dpg.mvThemeCol_Button, color_button)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, color_button_hovered)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, color_button_active)
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg, color_dark_gray)  # For input fields, etc.
            dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, color_main_purple)
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5)
            dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 8)
            dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, 6)
            dpg.add_theme_style(dpg.mvStyleVar_GrabRounding, 3)
            dpg.add_theme_style(dpg.mvStyleVar_FramePadding, (5, 5))
            dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, (8, 8))

    dpg.bind_theme(global_theme)

    # Font (DearPyGui will use a default font. For custom fonts like "Inter":)
    # 1. Get the .ttf file for Inter.
    # 2. Place it in your project directory.
    # 3. Uncomment and use:
    # with dpg.font_registry():
    #     try:
    #         default_font = dpg.add_font("Inter-Regular.ttf", 16) # Adjust size
    #         dpg.bind_font(default_font)
    #         log_to_ui("[INFO] Custom font loaded (if Inter-Regular.ttf was found).")
    #     except Exception as e:
    #         log_to_ui(f"[WARNING] Could not load custom font: {e}. Using default.")
    # else:
    log_to_ui("[INFO] Using default DearPyGui font.")


# --- Main UI Definition ---
def create_main_ui():
    with dpg.window(label="Vixen Spoofer GUI (Python)", width=WINDOW_WIDTH, height=WINDOW_HEIGHT, tag="main_window",
                    no_resize=True, no_collapse=True, no_close=True, no_move=False):
        with dpg.tab_bar(tag="main_tab_bar"):
            # --- INFO TAB (Corresponds to C++ Tab 1: Announcements/Instructions) ---
            with dpg.tab(label="Info", tag="info_tab"):
                dpg.add_text("Vixen Spoofer - Python Edition", color=(200, 200, 50, 255))
                dpg.add_separator()

                dpg.add_text("Announcements:", color=(180, 180, 180, 255))
                with dpg.child_window(height=100, border=True):
                    # Approximating C++ custom::announcement
                    dpg.add_text("Welcome to Vixen V5 Python!", color=(68, 61, 160, 255))  # Main color
                    dpg.add_text("This UI connects to the Python backend spoofer.",
                                 color=(210, 187, 73, 255))  # Description color
                    dpg.add_spacer(height=5)
                    dpg.add_text("Status: Operational", color=(68, 61, 160, 255))
                    dpg.add_text("Remember to run as Administrator.", color=(210, 187, 73, 255))

                dpg.add_spacer(height=10)
                dpg.add_text("Instructions:", color=(180, 180, 180, 255))
                dpg.add_button(label="Open Instructions Website", callback=open_instructions_url, width=-1, height=30)
                dpg.add_spacer(height=10)
                dpg.add_text("Backend by: nitaybl", color=(150, 150, 150, 255))

            # --- DEVICE INFO TAB (Corresponds to C++ Tab 2, Subtab 0) ---
            with dpg.tab(label="Device Info", tag="device_info_tab"):
                dpg.add_text("Current System Information (Placeholders)", color=(200, 200, 50, 255))
                dpg.add_button(label="Refresh Device Info", callback=fetch_and_display_system_info, width=-1, height=30)
                dpg.add_separator()
                with dpg.child_window(height=200, border=True):
                    dpg.add_text("Loading...", tag="mobo_manufacturer_text")
                    dpg.add_text("Loading...", tag="mobo_model_text")
                    dpg.add_text("Loading...", tag="bios_serial_text")
                    dpg.add_text("Loading...", tag="system_uuid_text")
                    dpg.add_text("Loading...", tag="mac_address_text")
                    dpg.add_text("Loading...", tag="tpm_status_text")
                dpg.add_text("Note: Implement Python functions in backend_spoofer.py to fetch actual data.",
                             wrap=WINDOW_WIDTH - 40, color=(255, 100, 100, 200))
                # Initial call to populate
                fetch_and_display_system_info()

            # --- SPOOFER TAB (Corresponds to C++ Tab 2, Subtab 1 & 2) ---
            with dpg.tab(label="Spoofer Actions", tag="spoofer_actions_tab"):
                dpg.add_text("Roblox Management", color=(200, 200, 50, 255))
                with dpg.group(horizontal=True):
                    dpg.add_button(label="Delete Roblox Cookies",
                                   callback=lambda: run_backend_action_threaded("delete_roblox_cookies"),
                                   width=WINDOW_WIDTH // 2 - 25, height=35)
                    dpg.add_button(label="Uninstall Roblox",
                                   callback=lambda: run_backend_action_threaded("uninstall_roblox"),
                                   width=WINDOW_WIDTH // 2 - 25, height=35)
                dpg.add_button(label="Install Roblox", callback=lambda: run_backend_action_threaded("install_roblox"),
                               width=-1, height=35)

                dpg.add_separator()
                dpg.add_text("System Spoofing", color=(200, 200, 50, 255))
                dpg.add_button(label="Change MAC Addresses",
                               callback=lambda: run_backend_action_threaded("change_mac_address"), width=-1, height=35)
                dpg.add_button(label="Modify Monitor EDIDs",
                               callback=lambda: run_backend_action_threaded("modify_monitor_edids"), width=-1,
                               height=35)
                dpg.add_button(label="Manage Hyperion SystemReg Key",
                               callback=lambda: run_backend_action_threaded("manage_hyperion_system_reg_key"), width=-1,
                               height=35)
                dpg.add_button(label="Focused HWID Spoof (AMIDEWIN)",
                               callback=lambda: run_backend_action_threaded("perform_focused_hwid_spoof"), width=-1,
                               height=35)

                dpg.add_separator()
                dpg.add_text("Full Sequence", color=(200, 200, 50, 255))
                dpg.add_button(label="Perform All Spoofing & Roblox Reinstall",
                               callback=lambda: run_backend_action_threaded("perform_all_spoofing_operations"),
                               width=-1, height=40)

                dpg.add_separator()
                dpg.add_text("Placeholder Miscellaneous Actions (Implement in backend):", color=(200, 150, 50, 255))
                with dpg.group(horizontal=True):
                    dpg.add_button(label="TPM Bypass (Not Impl.)", width=WINDOW_WIDTH // 3 - 20, height=30,
                                   enabled=False)  # Placeholder
                    dpg.add_button(label="Disk Spoof (Not Impl.)", width=WINDOW_WIDTH // 3 - 20, height=30,
                                   enabled=False)  # Placeholder
                    dpg.add_button(label="HVCI Bypass (Not Impl.)", width=WINDOW_WIDTH // 3 - 20, height=30,
                                   enabled=False)  # Placeholder

        # --- LOG AREA (Common to all tabs, placed below tab bar) ---
        dpg.add_separator()
        dpg.add_text("Action Logs:")
        # Using a read-only multiline input text as a log area
        with dpg.child_window(height=-1, border=True, tag="log_child_window"):  # Fill remaining space
            dpg.add_input_text(multiline=True, default_value="Initializing Vixen Spoofer GUI...\n",
                               tag="log_text_area", width=-1, height=-1, readonly=True)

    # --- Loading Indicator Popup ---
    with dpg.window(label="Working...", modal=True, show=False, tag="loading_indicator_popup", no_title_bar=True,
                    no_move=True, no_resize=True, pos=(WINDOW_WIDTH // 2 - 75, WINDOW_HEIGHT // 2 - 30)):
        dpg.add_spacer(height=10)
        dpg.add_loading_indicator(style=0, radius=5, color=(255, 255, 255, 255))  # style 0 is a circle
        dpg.add_spacer(height=5)
        dpg.add_text("Processing...", color=(220, 220, 220, 255))
        dpg.add_spacer(height=10)


# --- Main DPG Setup ---
# ... (rest of your backend_spoofer.py code) ...

# --- Main Execution ---
def main():  # This is the main in backend_spoofer.py
    os.system('cls')
    print(f"{Fore.CYAN}{BANNER}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{'=' * 80}{Style.RESET_ALL}")
    print(f"{Fore.WHITE}Nitaybl's ByGone Spoofer (Focused Hyperion Mode){Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{'=' * 80}{Style.RESET_ALL}\n")

    # CORRECTED LINE HERE:
    if not is_admin():  # Call is_admin() directly
        print(f"{Fore.RED}[!] Admin privileges required. Attempting to restart...{Style.RESET_ALL}")
        time.sleep(0.5);
        restart_with_admin()

    # AND HERE (if the first attempt to restart didn't exit):
    if not is_admin():  # Call is_admin() directly again
        print(f"{Fore.RED}[!] Failed to acquire admin privileges. Exiting.{Style.RESET_ALL}")
        input("\nPress Enter to exit...");
        sys.exit(1)

    print(f"{Fore.GREEN}[✓] Running as administrator.{Style.RESET_ALL}");
    time.sleep(0.5)
    if not PYWIN32_AVAILABLE:
        print(
            f"{Fore.YELLOW}Warning: pywin32 library not available. Hyperion SystemReg key management will be skipped.{Style.RESET_ALL}")
        if input("    Continue without this feature? (y/n): ").lower() != 'y': sys.exit(0)

    print("This script will automatically perform focused spoofing for Hyperion.")
    if input("Do you want to proceed? (yes/no): ").lower() == 'yes':
        try:
            perform_all_spoofing_operations()
        except SystemExit:
            print(f"\n{Fore.YELLOW}Script exiting.{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}\nAn unexpected error occurred: {e}{Style.RESET_ALL}")
            import traceback
            traceback.print_exc()
    else:
        print(f"{Fore.YELLOW}Operation cancelled.{Style.RESET_ALL}")
    input("\nPress Enter to exit...")


if __name__ == "__main__":
    main()
# Copyright (c) 2025 nitaybl. All Rights Reserved.