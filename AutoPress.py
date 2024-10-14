import time
from pynput import keyboard, mouse
from threading import Thread, Event

# Initialize flags and events
auto_press_enabled = False
stop_event = Event()
shift_pressed = False

# Create a controller object for the keyboard
keyboard_controller = keyboard.Controller()

def press_space():
    """Press the space bar at specified intervals when enabled."""
    global auto_press_enabled
    interval = 0.01  # 10 milliseconds
    while not stop_event.is_set():
        if auto_press_enabled:
            try:
                keyboard_controller.press(keyboard.Key.space)
                keyboard_controller.release(keyboard.Key.space)
                # Uncomment the next line for debugging (may slow down the loop)
                # print("Space pressed")
            except Exception as e:
                print(f"Error pressing space: {e}")
            time.sleep(interval)
        else:
            stop_event.wait(0.1)  # Wait before checking again

def toggle_auto_press():
    """Toggle the space auto press functionality."""
    global auto_press_enabled
    auto_press_enabled = not auto_press_enabled
    status = "enabled" if auto_press_enabled else "disabled"
    print(f"Auto press {status}.")

def on_mouse_click(x, y, button, pressed):
    """Toggle auto press when Shift + Middle Mouse Button is clicked."""
    global shift_pressed
    if button == mouse.Button.middle and pressed:
        if shift_pressed:
            toggle_auto_press()

def on_key_press(key):
    """Monitor Shift key state."""
    global shift_pressed
    if key == keyboard.Key.shift:
        shift_pressed = True
        print("Shift key pressed.")

def on_key_release(key):
    """Monitor Shift key state."""
    global shift_pressed
    if key == keyboard.Key.shift:
        shift_pressed = False
        print("Shift key released.")

def start_listeners():
    """Start the keyboard and mouse listeners."""
    with mouse.Listener(on_click=on_mouse_click) as mouse_listener, \
         keyboard.Listener(on_press=on_key_press, on_release=on_key_release) as keyboard_listener:
        mouse_listener.join()
        keyboard_listener.join()

if __name__ == '__main__':
    # Start the space pressing function in a separate thread
    thread = Thread(target=press_space, daemon=True)
    thread.start()

    print("Script started.")
    print("Press Shift + Middle Mouse Button to toggle auto space pressing.")
    print("Ensure the target application is in focus.")

    # Start listening for mouse and keyboard events
    start_listeners()
