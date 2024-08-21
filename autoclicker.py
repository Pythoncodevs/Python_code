import pyautogui
import time

def autoclicker(interval, duration):
    end_time = time.time() + duration
    while time.time() < end_time:
        pyautogui.click()
        time.sleep(interval)

# Параметры
click_interval = 0.1  # интервал между кликами в секундах
click_duration = 10  # общая длительность работы автокликера в секундах

# Запуск автокликера
autoclicker(click_interval, click_duration)
