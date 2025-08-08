#!/usr/bin/env python3

import netifaces
import subprocess
import time
import webbrowser
from datetime import datetime

def check_company_gateway():
    try:
        # Get default gateway
        gateways = netifaces.gateways()
        default_gateway = gateways.get('default', {}).get(2, [None])[0]  # 2 represents AF_INET (IPv4)
        
        # Check if gateway matches the target IP
        target_gateway = '10.192.16.1'
        if default_gateway == target_gateway:
            return 1
        return 0
    except:
        # Return 0 in case of any errors
        return 0

def open_app(app_name):
    try:
        subprocess.run(['open', '-a', app_name])
        print(f"Opening {app_name}...")
    except Exception as e:
        print(f"Error opening {app_name}: {e}")

def check_ping(host="10.192.16.1"):
    try:
        # Ping the host once with a 2 second timeout
        result = subprocess.run(['ping', '-c', '1', '-W', '2', host], 
                              capture_output=True, 
                              text=True)
        return result.returncode == 0
    except Exception as e:
        print(f"Error during ping: {e}")
        return False

def open_chrome_with_url():
    url = "https://bozuman.cybozu.com/k/36510/?action=1"
    try:
        # Try to open Chrome with the URL
        chrome_path = 'open -a /Applications/Google\ Chrome.app %s'
        webbrowser.get(chrome_path).open(url)
        print(f"Opened Chrome with URL: {url}")
        return True
    except Exception as e:
        print(f"Error opening Chrome: {e}")
        return False

def monitor_connection():
    print("\nStarting connection monitor...")
    print("Waiting for successful ping to 10.192.16.1")
    print("Press Ctrl+C to stop monitoring")
    
    browser_opened = False
    
    try:
        while not browser_opened:
            if check_ping():
                print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Ping successful!")
                print("Opening Chrome with Bozuman URL...")
                if open_chrome_with_url():
                    browser_opened = True
                    break
            else:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Waiting for connection...", end='\r')
            time.sleep(2)  # Wait 2 seconds between pings
            
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user")
    except Exception as e:
        print(f"\nError during monitoring: {e}")

if __name__ == '__main__':
    result = check_company_gateway()
    print(result)
    
    # If gateway check returns 0, open the specified app
    if result == 0:
        # Replace 'Calculator' with any macOS app name you want to open
        # open_app('Cisco Secure Client')  # You can change this to any app you want

        # # Wait for app to open
        # time.sleep(2)

        # # AppleScript to select VPN from dropdown and click Connect
        # applescript = '''
        # tell application "System Events"
        #     tell process "Cisco Secure Client"
        #         # Wait for window to be ready
        #         delay 1
                
        #         # press Enter key
        #         key code 36

        #         # wait 10s before entering the password
        #         delay 10

        #         # press escape key
        #         key code 53

        #         delay 2

        #         # enter the password
        #         keystroke "ED!rx4F5Mz" & return

        #         # press Enter key
        #         key code 36
        #     end tell
        # end tell
        # '''

        # subprocess.run(['osascript', '-e', applescript])
        # print("Selected VPN and clicked Connect")

        monitor_connection()