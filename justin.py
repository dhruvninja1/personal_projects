import subprocess

def run_command(command):
    """Executes a shell command and returns its output, error, and return code."""
    process = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True,
        check=False
    )
    return process.stdout.strip(), process.stderr.strip(), process.returncode

try:
    import pyautogui
except ImportError:
    command_to_run = "pip install pyautogui"
    stdout, stderr, returncode = run_command(command_to_run)
    print(f"Command: {command_to_run}")
    print(f"Stdout:\n{stdout}")
    print(f"Stderr:\n{stderr}")
    print(f"Return Code: {returncode}")

try:
    from pynput import mouse, keyboard
except ImportError:
    command_to_run = "pip install pynput"
    stdout, stderr, returncode = run_command(command_to_run)
    print(f"Command: {command_to_run}")
    print(f"Stdout:\n{stdout}")
    print(f"Stderr:\n{stderr}")
    print(f"Return Code: {returncode}")


import threading
import time





global running
running = False


def background():
     while True:
        if running:
            pyautogui.click()
        time.sleep(0.05)

def on_press(key):
    global running
    try:
        if key.char == "`":
            running = not running
            print(f'running: {running}')
        
    except:
        pass
    

def main():
    background_thread = threading.Thread(target=background, daemon=True)
    background_thread.start()
    with keyboard.Listener(
        on_press=on_press) as listener:
            listener.join()
    

if __name__ == "__main__":
    main()

    
