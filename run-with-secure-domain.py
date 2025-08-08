#!/usr/bin/env python3

import netifaces
import subprocess
import time
import webbrowser
from datetime import datetime, time
import os

def check_weekday():
    """
    Check if today is a weekend
    Returns:
        0 if weekend, 1 if weekday
    """
    try:
        current_day = datetime.now().weekday()
        return 0 if current_day >= 5 else 1
    except Exception as e:
        print(f"Error checking weekday: {e}")
        return 0

def get_working_hours():
    try:
        start_time_str = '07:30'
        end_time_str = '16:30'

        start_hour, start_minute = map(int, start_time_str.split(':'))
        working_start_time = time(start_hour, start_minute)

        end_hour, end_minute = map(int, end_time_str.split(':'))
        working_end_time = time(end_hour, end_minute)

        return working_start_time, working_end_time

    except Exception as e:
        print(f"Error parsing working hours: {e}")
        # Return default values if there's an error
        return time(7, 30), time(16, 30)

def check_working_hours():
    try:
       working_start_time, working_end_time = get_working_hours()

       current_time = datetime.now().time()

       start_check = time(working_start_time.hour, working_start_time.minute - 5)
       if current_time.hour == start_check.hour and current_time.minute >= start_check.minute:
            return "start"

       end_check = time(working_end_time.hour, working_end_time.minute + 5)
       if current_time.hour == end_check.hour and current_time.minute >= end_check.minute:
            return "end"

       return None

    except Exception as e:
        print(f"Error checking working hours: {e}")
        return None

def open_chrome_with_url(url):
    try:
        # Try to open Chrome with the URL
        chrome_path = 'open -a /Applications/Google\ Chrome.app %s'
        webbrowser.get(chrome_path).open(url)
        print(f"Opened Chrome with URL: {url}")
        return True
    except Exception as e:
        print(f"Error opening Chrome: {e}")
        return False


if __name__ == '__main__':
    weekday_check = check_weekday()
    if not weekday_check:
        print("Not at weekday - no action needed")
        exit(0)

    open_chrome_with_url("https://bozuman.cybozu.com/k/36510/?action=1")

    # time_check = check_working_hours()
    # if not time_check:
    #     print("Not at target time - no action needed")
    #     return
    
    # if time_check == "start":
    #     print("Checking in")
    #     open_chrome_with_url("https://bozuman.cybozu.com/k/36510/?action=1")
        
    # elif time_check == "end":
    #     print("Checking out")
    #     open_chrome_with_url("https://bozuman.cybozu.com/k/36510/?action=2")
    