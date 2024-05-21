from pynput import keyboard

pressedKeys=[]

def on_press(key):
    global pressedKeys
    pressedKeys.append(key)

def on_release(key):
    pass
    #pressedKeys.remove(key)

# ...or, in a non-blocking fashion:
listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()