import pyautogui
import time

def autoclicker(interval, duration):
    end_time = time.time() + duration
    while time.time() < end_time:
        pyautogui.click()
        time.sleep(interval)

click_interval = 0.1 
click_duration = 10 

autoclicker(click_interval, click_duration)
