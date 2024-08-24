import tkinter as tk

root = tk.Tk()
root.title("Simple Countdown Timer")

root.geometry("300x200")

label = tk.Label(root, text="10", font=("Arial", 48))
label.pack(pady=20)

def countdown(count):
    label.config(text=str(count))
    if count > 0:
        root.after(1000, countdown, count-1)

countdown(10)

root.mainloop()
