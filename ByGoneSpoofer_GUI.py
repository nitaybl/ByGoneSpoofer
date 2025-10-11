# Copyright (c) 2025 nitaybl. All Rights Reserved.
# ByGone Spoofer - Modern GUI Version
# Sleek UI powered by CustomTkinter

import customtkinter as ctk
import threading
import sys
import os

# Import the backend functions from the main spoofer
from ByGoneSpoofer import (
    is_admin, restart_with_admin,
    perform_full_spoofing_operations,
    perform_light_spoofing_operations,
    perform_recommended_spoof_for_cheating,
    perform_reverse_spoofing,
    perform_preflight_checks,
    create_system_restore_point,
    backup_hardware_ids,
    restore_from_backup,
    action_nuke_webview2,
    operation_logger,
    clear_temp_files,
    flush_dns_cache
)

# Set appearance mode and default color theme
ctk.set_appearance_mode("dark")  # Modes: "System" (default), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (default), "green", "dark-blue"


class ModernButton(ctk.CTkButton):
    """Custom button with hover effects"""
    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            corner_radius=8,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            **kwargs
        )


class ByGoneSpooferGUI:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("ByGone Spoofer v4.4 - Modern UI")
        self.root.geometry("900x700")
        
        # Set minimum size
        self.root.minsize(800, 600)
        
        # Configure grid weight
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        
        # Create UI elements
        self.create_header()
        self.create_main_content()
        self.create_footer()
        
        # Check admin rights on startup
        self.check_admin_status()
    
    def create_header(self):
        """Create the header section"""
        header_frame = ctk.CTkFrame(self.root, corner_radius=0, fg_color=("#1a1a1a", "#0a0a0a"))
        header_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        header_frame.grid_columnconfigure(1, weight=1)
        
        # Logo/Title
        title_label = ctk.CTkLabel(
            header_frame,
            text="⚡ ByGone Spoofer",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=("#00D9FF", "#00D9FF")
        )
        title_label.grid(row=0, column=0, padx=20, pady=15, sticky="w")
        
        # Version badge
        version_label = ctk.CTkLabel(
            header_frame,
            text="v4.4",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color=("#00D9FF", "#00D9FF"),
            text_color=("#000000", "#000000"),
            corner_radius=12,
            padx=12,
            pady=4
        )
        version_label.grid(row=0, column=1, padx=10, pady=15, sticky="w")
        
        # Admin status indicator
        self.admin_indicator = ctk.CTkLabel(
            header_frame,
            text="⚠️ No Admin",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color=("#FF4444", "#CC0000"),
            text_color=("#FFFFFF", "#FFFFFF"),
            corner_radius=12,
            padx=12,
            pady=4
        )
        self.admin_indicator.grid(row=0, column=2, padx=20, pady=15, sticky="e")
    
    def create_main_content(self):
        """Create the main content area"""
        # Main container
        main_container = ctk.CTkFrame(self.root, fg_color="transparent")
        main_container.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        main_container.grid_columnconfigure(0, weight=1)
        main_container.grid_rowconfigure(1, weight=1)
        
        # Subtitle
        subtitle = ctk.CTkLabel(
            main_container,
            text="Hardware Identifier Spoofing Tool • Join discord.gg/bygone",
            font=ctk.CTkFont(size=13),
            text_color=("#888888", "#666666")
        )
        subtitle.grid(row=0, column=0, pady=(0, 20), sticky="w")
        
        # Create tabview
        self.tabview = ctk.CTkTabview(main_container, corner_radius=12)
        self.tabview.grid(row=1, column=0, sticky="nsew")
        
        # Add tabs
        self.tab_spoofing = self.tabview.add("🎯 Spoofing")
        self.tab_utilities = self.tabview.add("🛠️ Utilities")
        self.tab_tools = self.tabview.add("🔧 Tools")
        self.tab_log = self.tabview.add("📋 Log")
        
        # Configure tab grids
        self.tab_spoofing.grid_columnconfigure(0, weight=1)
        self.tab_utilities.grid_columnconfigure(0, weight=1)
        self.tab_tools.grid_columnconfigure(0, weight=1)
        self.tab_log.grid_columnconfigure(0, weight=1)
        
        # Populate tabs
        self.create_spoofing_tab()
        self.create_utilities_tab()
        self.create_tools_tab()
        self.create_log_tab()
    
    def create_spoofing_tab(self):
        """Create the spoofing options tab"""
        # Recommended option (highlighted)
        recommended_frame = ctk.CTkFrame(self.tab_spoofing, fg_color=("#1a3a1a", "#0d2e0d"), corner_radius=12)
        recommended_frame.grid(row=0, column=0, padx=20, pady=10, sticky="ew")
        
        ctk.CTkLabel(
            recommended_frame,
            text="⭐ RECOMMENDED",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=("#00FF88", "#00DD77")
        ).pack(pady=(15, 5))
        
        ctk.CTkLabel(
            recommended_frame,
            text="Best for continuing to cheat • Skips HWID spoofing",
            font=ctk.CTkFont(size=12),
            text_color=("#888888", "#666666")
        ).pack(pady=(0, 10))
        
        ModernButton(
            recommended_frame,
            text="🎮 Start Recommended Spoof",
            fg_color=("#00DD77", "#00BB66"),
            hover_color=("#00BB66", "#009955"),
            command=self.run_recommended_spoof
        ).pack(pady=(0, 15), padx=20, fill="x")
        
        # Other spoofing options
        options_frame = ctk.CTkFrame(self.tab_spoofing, fg_color="transparent")
        options_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        
        # Full Spoof
        full_frame = self.create_option_card(
            options_frame,
            "💎 Full Spoof (Hard Ban)",
            "Complete HWID, EDID, MAC spoofing • For hard bans"
        )
        full_frame.pack(pady=5, fill="x")
        
        ModernButton(
            full_frame,
            text="Start Full Spoof",
            fg_color=("#4A90E2", "#3A7AC2"),
            hover_color=("#3A7AC2", "#2A6AB2"),
            command=self.run_full_spoof
        ).pack(pady=(10, 15), padx=20, fill="x")
        
        # Light Spoof
        light_frame = self.create_option_card(
            options_frame,
            "🌟 Light Spoof (No HWID)",
            "EDID & MAC only • For soft bans"
        )
        light_frame.pack(pady=5, fill="x")
        
        ModernButton(
            light_frame,
            text="Start Light Spoof",
            fg_color=("#F5A623", "#D58A15"),
            hover_color=("#D58A15", "#C57A10"),
            command=self.run_light_spoof
        ).pack(pady=(10, 15), padx=20, fill="x")
        
        # Reverse
        reverse_frame = self.create_option_card(
            options_frame,
            "🔄 Reverse Spoofing",
            "Undo changes • Restore MAC addresses"
        )
        reverse_frame.pack(pady=5, fill="x")
        
        ModernButton(
            reverse_frame,
            text="Start Reversal",
            fg_color=("#E74C3C", "#C73C2C"),
            hover_color=("#C73C2C", "#B72C1C"),
            command=self.run_reverse_spoof
        ).pack(pady=(10, 15), padx=20, fill="x")
    
    def create_utilities_tab(self):
        """Create the utilities tab"""
        # Safety section
        safety_label = ctk.CTkLabel(
            self.tab_utilities,
            text="🛡️ Safety & Backup",
            font=ctk.CTkFont(size=18, weight="bold"),
            anchor="w"
        )
        safety_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")
        
        # Restore point button
        ModernButton(
            self.tab_utilities,
            text="💾 Create System Restore Point",
            command=self.create_restore_point,
            anchor="w"
        ).grid(row=1, column=0, padx=20, pady=5, sticky="ew")
        
        # Backup button
        ModernButton(
            self.tab_utilities,
            text="🔐 Backup Hardware IDs",
            command=self.backup_hardware,
            anchor="w"
        ).grid(row=2, column=0, padx=20, pady=5, sticky="ew")
        
        # Restore button
        ModernButton(
            self.tab_utilities,
            text="🔄 Restore from Backup",
            command=self.restore_backup,
            anchor="w"
        ).grid(row=3, column=0, padx=20, pady=5, sticky="ew")
        
        # Cleanup section
        cleanup_label = ctk.CTkLabel(
            self.tab_utilities,
            text="🧹 Cleanup Tools",
            font=ctk.CTkFont(size=18, weight="bold"),
            anchor="w"
        )
        cleanup_label.grid(row=4, column=0, padx=20, pady=(30, 10), sticky="w")
        
        # Temp files
        ModernButton(
            self.tab_utilities,
            text="🗑️ Clear Temp Files",
            command=self.clear_temp,
            anchor="w"
        ).grid(row=5, column=0, padx=20, pady=5, sticky="ew")
        
        # DNS flush
        ModernButton(
            self.tab_utilities,
            text="🌐 Flush DNS Cache",
            command=self.flush_dns,
            anchor="w"
        ).grid(row=6, column=0, padx=20, pady=5, sticky="ew")
    
    def create_tools_tab(self):
        """Create the tools tab"""
        # System check
        check_label = ctk.CTkLabel(
            self.tab_tools,
            text="✅ System Diagnostics",
            font=ctk.CTkFont(size=18, weight="bold"),
            anchor="w"
        )
        check_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")
        
        ModernButton(
            self.tab_tools,
            text="🔍 Run Preflight Checks",
            command=self.run_preflight,
            anchor="w"
        ).grid(row=1, column=0, padx=20, pady=5, sticky="ew")
        
        # Roblox tools
        roblox_label = ctk.CTkLabel(
            self.tab_tools,
            text="🎮 Roblox Tools",
            font=ctk.CTkFont(size=18, weight="bold"),
            anchor="w"
        )
        roblox_label.grid(row=2, column=0, padx=20, pady=(30, 10), sticky="w")
        
        ModernButton(
            self.tab_tools,
            text="💥 Nuke WebView2 Data",
            command=self.nuke_webview2,
            anchor="w"
        ).grid(row=3, column=0, padx=20, pady=5, sticky="ew")
        
        # Info
        info_frame = ctk.CTkFrame(self.tab_tools, corner_radius=12, fg_color=("#2a2a2a", "#1a1a1a"))
        info_frame.grid(row=4, column=0, padx=20, pady=20, sticky="ew")
        
        ctk.CTkLabel(
            info_frame,
            text="ℹ️ Known Issues",
            font=ctk.CTkFont(size=14, weight="bold"),
        ).pack(pady=(15, 5))
        
        info_text = (
            "• ASUS motherboards may block HWID changes\n"
            "• WiFi adapters often don't support MAC spoofing\n"
            "• Graphics glitches? Reboot your system\n"
            "• Join discord.gg/bygone for support"
        )
        ctk.CTkLabel(
            info_frame,
            text=info_text,
            font=ctk.CTkFont(size=12),
            text_color=("#888888", "#666666"),
            justify="left"
        ).pack(pady=(5, 15), padx=20)
    
    def create_log_tab(self):
        """Create the operation log tab"""
        # Log display
        self.log_textbox = ctk.CTkTextbox(
            self.tab_log,
            corner_radius=12,
            font=ctk.CTkFont(family="Consolas", size=12),
            wrap="word"
        )
        self.log_textbox.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        
        # Buttons
        button_frame = ctk.CTkFrame(self.tab_log, fg_color="transparent")
        button_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="ew")
        
        ModernButton(
            button_frame,
            text="🔄 Refresh Log",
            command=self.refresh_log,
            width=150
        ).pack(side="left", padx=5)
        
        ModernButton(
            button_frame,
            text="🗑️ Clear Display",
            command=lambda: self.log_textbox.delete("1.0", "end"),
            width=150
        ).pack(side="left", padx=5)
        
        # Initial log load
        self.refresh_log()
    
    def create_footer(self):
        """Create the footer section"""
        footer_frame = ctk.CTkFrame(self.root, corner_radius=0, height=50, fg_color=("#1a1a1a", "#0a0a0a"))
        footer_frame.grid(row=2, column=0, sticky="ew", padx=0, pady=0)
        footer_frame.grid_columnconfigure(1, weight=1)
        
        # Status label
        self.status_label = ctk.CTkLabel(
            footer_frame,
            text="Ready • All systems operational",
            font=ctk.CTkFont(size=12),
            text_color=("#888888", "#666666")
        )
        self.status_label.grid(row=0, column=0, padx=20, pady=15, sticky="w")
        
        # Discord link
        discord_btn = ctk.CTkButton(
            footer_frame,
            text="💬 Discord Support",
            command=lambda: os.system("start https://discord.gg/bygone"),
            width=150,
            height=30,
            corner_radius=8,
            fg_color="transparent",
            border_width=2,
            border_color=("#5865F2", "#5865F2")
        )
        discord_btn.grid(row=0, column=2, padx=20, pady=10, sticky="e")
    
    def create_option_card(self, parent, title, description):
        """Create a styled option card"""
        card = ctk.CTkFrame(parent, corner_radius=12, fg_color=("#2a2a2a", "#1a1a1a"))
        
        ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        ).pack(pady=(15, 5), padx=20, anchor="w")
        
        ctk.CTkLabel(
            card,
            text=description,
            font=ctk.CTkFont(size=11),
            text_color=("#888888", "#666666"),
            anchor="w"
        ).pack(pady=(0, 5), padx=20, anchor="w")
        
        return card
    
    def check_admin_status(self):
        """Check if running as administrator"""
        if is_admin():
            self.admin_indicator.configure(
                text="✓ Admin",
                fg_color=("#00DD77", "#00BB66")
            )
            self.log("Application started with administrator privileges")
        else:
            self.admin_indicator.configure(
                text="⚠️ No Admin",
                fg_color=("#FF4444", "#CC0000")
            )
            self.log("WARNING: Running without administrator privileges", level="warning")
            self.show_admin_warning()
    
    def show_admin_warning(self):
        """Show warning dialog for missing admin rights"""
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Administrator Rights Required")
        dialog.geometry("500x250")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (dialog.winfo_screenheight() // 2) - (250 // 2)
        dialog.geometry(f"+{x}+{y}")
        
        frame = ctk.CTkFrame(dialog, corner_radius=12)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(
            frame,
            text="⚠️",
            font=ctk.CTkFont(size=40)
        ).pack(pady=(20, 10))
        
        ctk.CTkLabel(
            frame,
            text="Administrator Rights Required",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=5)
        
        ctk.CTkLabel(
            frame,
            text="The spoofer needs admin rights to modify system settings.\nPlease restart the application as administrator.",
            font=ctk.CTkFont(size=12),
            text_color=("#888888", "#666666")
        ).pack(pady=10)
        
        button_frame = ctk.CTkFrame(frame, fg_color="transparent")
        button_frame.pack(pady=(10, 20))
        
        ModernButton(
            button_frame,
            text="Restart as Admin",
            command=lambda: [dialog.destroy(), restart_with_admin()],
            fg_color=("#00DD77", "#00BB66"),
            hover_color=("#00BB66", "#009955"),
            width=150
        ).pack(side="left", padx=5)
        
        ModernButton(
            button_frame,
            text="Continue Anyway",
            command=dialog.destroy,
            fg_color=("#444444", "#333333"),
            hover_color=("#555555", "#444444"),
            width=150
        ).pack(side="left", padx=5)
    
    def log(self, message, level="info"):
        """Add message to log"""
        timestamp = __import__('datetime').datetime.now().strftime('%H:%M:%S')
        color = {
            'info': '#00D9FF',
            'success': '#00DD77',
            'warning': '#F5A623',
            'error': '#E74C3C'
        }.get(level, '#888888')
        
        self.log_textbox.insert("end", f"[{timestamp}] ", "timestamp")
        self.log_textbox.insert("end", f"{message}\n", level)
        self.log_textbox.see("end")
        
        # Configure tags
        self.log_textbox.tag_config("timestamp", foreground="#666666")
        self.log_textbox.tag_config(level, foreground=color)
        
        # Update status
        self.status_label.configure(text=message[:60] + "..." if len(message) > 60 else message)
    
    def refresh_log(self):
        """Refresh operation log from file"""
        self.log_textbox.delete("1.0", "end")
        logs = operation_logger.operations[-50:]  # Last 50 operations
        for log_entry in logs:
            self.log_textbox.insert("end", log_entry + "\n")
        self.log_textbox.see("end")
    
    def run_in_thread(self, func, *args):
        """Run function in separate thread"""
        def wrapper():
            try:
                self.log(f"Starting operation: {func.__name__}", "info")
                result = func(*args)
                if result:
                    self.log(f"Operation completed successfully", "success")
                else:
                    self.log(f"Operation completed with warnings", "warning")
            except Exception as e:
                self.log(f"Error: {str(e)}", "error")
        
        thread = threading.Thread(target=wrapper, daemon=True)
        thread.start()
    
    # Spoofing operations
    def run_recommended_spoof(self):
        self.run_in_thread(perform_recommended_spoof_for_cheating)
    
    def run_full_spoof(self):
        self.run_in_thread(perform_full_spoofing_operations)
    
    def run_light_spoof(self):
        self.run_in_thread(perform_light_spoofing_operations)
    
    def run_reverse_spoof(self):
        self.run_in_thread(perform_reverse_spoofing)
    
    # Utility operations
    def create_restore_point(self):
        self.run_in_thread(create_system_restore_point)
    
    def backup_hardware(self):
        self.run_in_thread(backup_hardware_ids)
    
    def restore_backup(self):
        self.run_in_thread(restore_from_backup)
    
    def clear_temp(self):
        self.run_in_thread(clear_temp_files)
    
    def flush_dns(self):
        self.run_in_thread(flush_dns_cache)
    
    # Tool operations
    def run_preflight(self):
        self.run_in_thread(perform_preflight_checks)
    
    def nuke_webview2(self):
        self.run_in_thread(action_nuke_webview2)
    
    def run(self):
        """Start the GUI"""
        self.root.mainloop()


def main():
    """Main entry point"""
    app = ByGoneSpooferGUI()
    app.run()


if __name__ == "__main__":
    main()

