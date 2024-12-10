import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import pyautogui
import time
import threading
import os


class AutoMessageWriter:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Auto Message Writer")
        self.root.geometry("700x600")
        self.root.config(bg="#F0F0F0")  # Light theme for default

        # Theme colors
        self.primary_color = "#4CAF50"
        self.secondary_color = "#FFFFFF"
        self.text_color = "#212121"

        # Variables
        self.text_sprites = [
             "Hello, how are you?",
    "Happy Birthday! 🎉🎂",
    "Good morning! Have a great day ahead!",
    "Thank you for your support!",
    "We appreciate your feedback.",
    "Congratulations on your achievement! 🌟",
    "Wishing you a fantastic day! 🌈",
    "Don't forget to smile today! 😊",
    "Keep pushing forward, you're doing great! 💪",
    "Your hard work is truly appreciated. 🙏",
    "Best wishes for your upcoming endeavors! ✨",
    "Enjoy every moment of your journey! 🚀",
    "You're an inspiration to us all! 💡",
    "Stay positive and keep shining! 🌟",
    "We are here for you anytime. 🤝",
    "Sending lots of good vibes your way! ✨",
    "Take care and stay safe! 🛡️",
    "Remember to take breaks and relax. 🧘",
    "You're stronger than you think. 💖",
    "Every step you take is progress. 🏞️",
    "Success is just around the corner! 🌄",
    "Be proud of your achievements. 🎖️",
    "Always believe in yourself! 🌟",
    "You make a difference every day! 🌍",
    "Stay awesome and keep smiling! 😄",
    "We value your contributions deeply. 🤗",
    "Never stop chasing your dreams! 🌠",
    "Your creativity is unmatched. 🎨",
    "Keep exploring, learning, and growing! 📚"
        ]
        self.selected_message = tk.StringVar(value="")
        self.selected_file = tk.StringVar(value="")
        self.message_count = tk.IntVar(value=1)
        self.dark_mode = tk.BooleanVar(value=False)

        # UI Components
        self.create_widgets()

    def create_widgets(self):
        """Create the main interface components."""
        # Title Label
        tk.Label(
            self.root, text="Advanced Auto Message Writer", font=("Helvetica", 20, "bold"),
            bg=self.secondary_color, fg=self.primary_color
        ).pack(pady=10)

        # Dark mode toggle
        tk.Checkbutton(
            self.root, text="Dark Mode", variable=self.dark_mode, onvalue=True, offvalue=False,
            command=self.toggle_theme, bg=self.secondary_color, fg=self.text_color, font=("Helvetica", 10)
        ).pack(anchor="e", padx=10, pady=5)

        # Message selection list
        tk.Label(self.root, text="Select a message template:", bg=self.secondary_color, fg=self.text_color).pack()
        self.listbox = tk.Listbox(
            self.root, height=8, font=("Courier", 12), selectmode=tk.SINGLE,
            bg=self.secondary_color, fg=self.text_color, highlightcolor=self.primary_color, highlightthickness=2
        )
        self.listbox.pack(fill=tk.BOTH, padx=20, pady=10)
        for message in self.text_sprites:
            self.listbox.insert(tk.END, message)

        # Buttons
        button_frame = tk.Frame(self.root, bg=self.secondary_color)
        button_frame.pack(pady=10)

        tk.Button(
            button_frame, text="Select Message", command=self.select_message,
            bg=self.primary_color, fg=self.secondary_color, relief=tk.FLAT
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            button_frame, text="Write Custom Message", command=self.write_custom_message,
            bg=self.primary_color, fg=self.secondary_color, relief=tk.FLAT
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            button_frame, text="Attach File", command=self.attach_file,
            bg=self.primary_color, fg=self.secondary_color, relief=tk.FLAT
        ).pack(side=tk.LEFT, padx=5)

        # Message Preview
        tk.Label(self.root, text="Preview:", bg=self.secondary_color, fg=self.text_color).pack()
        self.message_display = tk.Label(
            self.root, text="", bg=self.secondary_color, fg=self.text_color, wraplength=650, relief=tk.SUNKEN,
            font=("Courier", 12), padx=10, pady=10
        )
        self.message_display.pack(fill=tk.BOTH, padx=20, pady=5)

        # Send Messages
        tk.Label(self.root, text="Number of Messages to Send:", bg=self.secondary_color, fg=self.text_color).pack()
        tk.Entry(self.root, textvariable=self.message_count, font=("Helvetica", 12)).pack(pady=5)

        tk.Button(
            self.root, text="Send Messages", command=self.start_sending_thread,
            bg=self.primary_color, fg=self.secondary_color, relief=tk.FLAT
        ).pack(pady=10)

    def toggle_theme(self):
        """Toggle between light and dark themes."""
        if self.dark_mode.get():
            self.primary_color, self.secondary_color, self.text_color = "#2E2E2E", "#212121", "#F0F0F0"
        else:
            self.primary_color, self.secondary_color, self.text_color = "#4CAF50", "#FFFFFF", "#212121"

        self.root.config(bg=self.secondary_color)
        for widget in self.root.winfo_children():
            try:
                widget.config(bg=self.secondary_color, fg=self.text_color)
            except:
                pass

    def select_message(self):
        """Select a predefined message."""
        selected_index = self.listbox.curselection()
        if selected_index:
            message = self.listbox.get(selected_index)
            self.selected_message.set(message)
            self.message_display.config(text=message)
        else:
            messagebox.showinfo("Info", "Please select a message from the list.")

    def write_custom_message(self):
        """Write a custom message."""
        custom_message = simpledialog.askstring("Custom Message", "Enter your custom message:")
        if custom_message:
            self.selected_message.set(custom_message)
            self.message_display.config(text=custom_message)

    def attach_file(self):
        """Attach a file for sending."""
        file_path = filedialog.askopenfilename(title="Select a file")
        if file_path:
            self.selected_file.set(file_path)
            self.message_display.config(text=f"File Attached: {os.path.basename(file_path)}")

    def send_messages(self):
        """Send the selected message/file a specified number of times."""
        message = self.selected_message.get()
        if not message and not self.selected_file.get():
            messagebox.showwarning("Warning", "No message or file selected!")
            return

        count = self.message_count.get()
        if not count or count <= 0:
            messagebox.showwarning("Warning", "Invalid number of messages!")
            return

        messagebox.showinfo(
            "Info",
            "Switch to the chat window where you want to send messages/files. "
            "Automation will start in 5 seconds. DO NOT use the mouse or keyboard during this time."
        )
        time.sleep(5)

        for _ in range(count):
            if message:
                pyautogui.typewrite(message)
                pyautogui.press("enter")
            if self.selected_file.get():
                pyautogui.hotkey("ctrl", "o")
                time.sleep(2)
                pyautogui.typewrite(self.selected_file.get())
                pyautogui.press("enter")
                pyautogui.press("enter")
            time.sleep(0.5)

        messagebox.showinfo("Info", f"Successfully sent {count} messages/files!")

    def start_sending_thread(self):
        """Run the sending process in a separate thread."""
        threading.Thread(target=self.send_messages, daemon=True).start()


def main():
    root = tk.Tk()
    app = AutoMessageWriter(root)
    root.mainloop()


if __name__ == "__main__":
    main()
