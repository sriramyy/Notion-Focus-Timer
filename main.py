from notion_client import Client
import tkinter as tk
from tkinter import *
from tkinter import  ttk, font
from datetime import datetime


class timer(tk.Tk):
    
    def __init__(self):
        super().__init__()
        self.title("Notion Focus Timer")
        self.geometry("240x275")
        self.time=0
        self.running = False

        # Input Notion Auth Token and Database ID, also input on line 90
        self.notion_auth='YOUR NOTION AUTH TOKEN'
        self.notion_database='YOUR NOTION DATABASE ID'
        self.configure(bg="#ebc48a")
        self.notion = Client(auth=self.notion_auth)

        # Title
        self.titleLabel = tk.Label(self, text="Focus Timer", font=('Bahnschrift', 20, "bold"), fg="#8a6c3f", bg="#ebc48a")
        self.titleLabel.pack(pady=8)

        # Dropdown Menu, input classes
        self.days = ["CLASS 1", "CLASS 2", "CLASS 3", "CLASS 4"]
        self.day_selected = tk.StringVar(value="Select Class")
        self.day_menu = ttk.Combobox(self, textvariable=self.day_selected, values=self.days, state="readonly", width=20,)
        self.day_menu.pack(pady=10, padx=30)
        self.day_menu.configure(font=("Bahnschrift Light SemiCondensed", 12), foreground="#8a6c3f")

        # Timer Label
        self.timerLabel = tk.Label(self, text="00:00", font=('Terminal', 30, "bold"), fg="#8a6c3f", bg="#ebc48a")
        self.timerLabel.pack(pady=5)


        # All the buttons
        style = ttk.Style()
        style.configure("TButton", font=("Bahnschrift Light SemiCondensed", 14), relief="sunken", background="#ebc48a", foreground="#8a6c3f")
        style.map("TButton", background=[("active", "#dea44e")])
        # Start Button
        self.startBtn = ttk.Button(self, text="Start", command=self.start, style="TButton")
        self.startBtn.pack(pady=2)
        # Pause Button
        self.pauseBtn = ttk.Button(self, text="Pause", command=self.pause, style="TButton")
        self.pauseBtn.pack(pady=2)
        # Upload Button
        self.uploadBtn = ttk.Button(self, text="Upload", command=self.upload, style="TButton")
        self.uploadBtn.pack(pady=2)


    # Starts the timer
    def start(self):
        self.running = True
        self.count()

    # Pauses the timer
    def pause(self):
        self.running = False

    # Uploads timer contents to the Notion DB
    def upload(self):
        self.running = False
        minutes, seconds = divmod(self.time, 60)
        times_str = str(self.time)
        selected_day = self.day_selected.get()
        # print(f"Subject: {selected_day} - Time: {minutes:02d}:{seconds:02d}")
        # Resets timer
        self.time = 0
        self.timerLabel.config(text="00:00")

        # Uploads to Notion
        client.pages.create(
        **{
            "parent": {
                "database_id": self.notion_database
            },
            'properties': {
                # Date/Title Property
                'Date': {'title': [{'text': {'content': datetime.today().strftime('%Y-%m-%d')}}]},
                # Class Property, select type, add your class types to the Notion DB
                'Class': {'select': {'name': selected_day}},
                # Time Studied (s) Property, text type
                'Time Studied (s)': {'rich_text': [{'text': {'content': times_str}}]}
            }
          }
        )

    # Counts the stopwatch up
    def count(self):
        if self.running:
            self.time += 1
            minutes, seconds = divmod(self.time,60)
            self.timerLabel.config(text="{:02d}:{:02d}".format(minutes,seconds))
            self.after(1000, self.count)


if __name__ == '__main__':
    # Input Notion Auth token
    notion_token = 'YOUR NOTION AUTH TOKEN'
    client = Client(auth=notion_token)
    Timer = timer()
    Timer.mainloop()
