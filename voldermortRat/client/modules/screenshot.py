import pyautogui

def capture_screenshot(filename="screenshot.png"):
    try:
        screenshot = pyautogui.screenshot()
        screenshot.save(filename)
    except Exception as e:
        print(f"[!] Screenshot error: {e}")
