import threading
import subprocess
import platform
import time

def _play_mac():
    # Built-in macOS alert sound
    subprocess.call(
        ["afplay", "/System/Library/Sounds/Glass.aiff"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

def _play_cross_platform(level):
    system = platform.system()

    if system == "Darwin":  # macOS
        _play_mac()

    elif system == "Windows":
        import winsound
        winsound.Beep(1000, 400)

    else:
        # Linux fallback
        print("\a", flush=True)

def play(level):
    """
    Non-blocking alert sound.
    level >= 2 triggers sound
    level 3 triggers double alert
    """
    if level < 2:
        return

    def worker():
        _play_cross_platform(level)
        if level >= 3:
            time.sleep(0.6)
            _play_cross_platform(level)

    threading.Thread(target=worker, daemon=True).start()
