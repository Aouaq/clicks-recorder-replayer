from pynput import mouse
import time
import json
import tkinter as tk
from tkinter import *
from pynput.mouse import Button, Controller
import keyboard

r = tk.Tk()
r.title('RecRep')

clicks = []

scrollbar = Scrollbar(r)
mylist = Listbox(r, yscrollcommand=scrollbar.set)
mylist.pack(side=TOP, fill=BOTH)
scrollbar.config(command=mylist.yview)

mouse_listener = None  


def on_click(x, y, button, pressed):
    if pressed:
        r.after(0, lambda: mylist.insert(END, f"Position ({x}, {y}) at: {time.time()}"))
        clicks.append({"x": x, "y": y, "button": str(button), "timestamp": time.time()})


def start_listener():
    global mouse_listener
    if mouse_listener is None:  
        mouse_listener = mouse.Listener(on_click=on_click)
        mouse_listener.start()

def Clicks_File():
    with open("clicks.json", "w") as file:
        clicks.pop(0)
        clicks.pop()
        json.dump(clicks, file, indent=4)
        r.after(0, lambda: mylist.insert(END,"Clicks saved to clicks.json."))
        clicks.clear()

def stop_listener():
    global mouse_listener
    if mouse_listener is not None:
        mouse_listener.stop()
        Clicks_File()
        mouse_listener = None




def replay_clicks():

    r.after(0, lambda: mylist.insert(END,"Replaying clicks continuously. Press Ctrl+C to stop."))

    mouse_controller = Controller()
    
    try:
        with open("clicks.json", "r") as file:
            loaded_clicks = json.load(file)

    except FileNotFoundError:
        r.after(0, lambda: mylist.insert(END,"No recorded clicks found. Please record first."))
        return

   
    while True:
        start_time = loaded_clicks[0]["timestamp"]
        if not keyboard.is_pressed('esc'):
            for click in loaded_clicks:
                delay = click["timestamp"] - start_time
                time.sleep(delay)
                mouse_controller.position = (click["x"], click["y"])
                button = Button.left if "left" in click["button"] else Button.right
                mouse_controller.click(button)
                start_time = click["timestamp"]

        else:
            break



button_start = tk.Button(r, text='Record', width=20, height=2, command=start_listener)
button_start.pack()

button_replay = tk.Button(r, text='Replay', width=20, height=2, command=replay_clicks)
button_replay.pack()

button_stop = tk.Button(r, text='Stop', width=20, height=2, command=stop_listener)
button_stop.pack()

r.mainloop()
