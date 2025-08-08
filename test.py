#!/usr/bin/env python3

import netifaces
import subprocess
import time
import webbrowser
from datetime import datetime
import os

# Redirect stdout to devnull to hide output
def silent_mode():
    return open(os.devnull, 'w')

def check_ping(host="10.192.16.1"):
    try:
        result = subprocess.run(
            ['ping', '-c', '1', '-W', '2', host],
            capture_output=True,
            text=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return result.returncode == 0
    except:
        return False

def open_cisco_client_silently():
    try:
        subprocess.run(
            ['open', '-a', 'Cisco Secure Client'],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return True
    except:
        return False

def run_applescript_silently(script):
    try:
        subprocess.run(
            ['osascript', '-e', script],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return True
    except:
        return False

def select_vpn_silently():
    applescript = '''
    tell application "System Events"
        tell process "Cisco Secure Client"
            click pop up button 1
            click menu item "ipsec.cybozu.vn" of menu 1 of pop up button 1
        end tell
    end tell
    '''
    return run_applescript_silently(applescript)

def press_enter_silently():
    applescript = '''
    tell application "System Events"
        key code 36
    end tell
    '''
    return run_applescript_silently(applescript)

def type_password_silently():
    applescript = 'tell application "System Events" to keystroke "ED!rx4F5Mz"'
    return run_applescript_silently(applescript)

def open_chrome_silently():
    try:
        url = "https://bozuman.cybozu.com/k/36510/?action=1"
        chrome_path = 'open -a /Applications/Google\ Chrome.app %s'
        webbrowser.get(chrome_path).open(url, new=2, autoraise=False)
        return True
    except:
        return False

def silent_vpn_connection():
    # Open Cisco Client
    open_cisco_client_silently()
    time.sleep(2)  # Wait for app to open
    
    # Select VPN
    select_vpn_silently()
    time.sleep(1)
    
    # Press Enter
    press_enter_silently()
    time.sleep(1)
    
    # Type password
    type_password_silently()
    time.sleep(1)
    
    # Press Enter to submit
    press_enter_silently()

def monitor_silently():
    browser_opened = False
    
    while not browser_opened:
        if check_ping():
            open_chrome_silently()
            browser_opened = True
        time.sleep(2)

def run_background():
    # First attempt to connect
    silent_vpn_connection()
    
    # Monitor until connection is established
    monitor_silently()

if __name__ == '__main__':
    # Run everything in silent mode
    run_background()