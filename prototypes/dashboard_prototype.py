import tkinter as tk
from tkinter import ttk
import time
import random

# ----------------------------
# Fake System State (Mock)
# ----------------------------

MODES = [
    "Listening",
    "Devil's Advocate",
    "Facilitator",
    "Silent Scribe",
    "Observer",
    "Persona Drift"
]

VOICES = ["Voice #1", "Voice #2", "Voice #3", "Voice #4"]
HUMOR_LEVELS = ["Low", "Medium", "High"]

learning_events = [
    "Audio emotion pattern updated",
    "User feedback integrated",
    "Persona tone adjusted",
    "Intent classifier refined",
    "Context memory extended"
]

# ----------------------------
# GUI Setup
# ----------------------------

root = tk.Tk()
root.title("M.O.L.O.C.H. Dashboard")
root.geometry("900x550")
root.configure(bg="#1e1e1e")

style = ttk.Style()
style.theme_use("default")
style.configure("TLabel", background="#1e1e1e", foreground="white")
style.configure("Header.TLabel", font=("Arial", 16, "bold"))
style.configure("Panel.TLabelframe", background="#1e1e1e", foreground="white")
style.configure("Panel.TLabelframe.Label", foreground="white")

# ----------------------------
# Header
# ----------------------------

header = ttk.Label(root, text="M.O.L.O.C.H. v0.1 — Transparent Autonomy Active",
                   style="Header.TLabel")
header.pack(pady=10)

# ----------------------------
# Layout Frames
# ----------------------------

main = tk.Frame(root, bg="#1e1e1e")
main.pack(fill="both", expand=True)

left = tk.Frame(main, bg="#1e1e1e")
left.pack(side="left", fill="both", expand=True, padx=10)

right = tk.Frame(main, bg="#1e1e1e")
right.pack(side="right", fill="both", expand=True, padx=10)

# ----------------------------
# Mode Panel
# ----------------------------

mode_frame = ttk.Labelframe(left, text="Active Mode", style="Panel.TLabelframe")
mode_frame.pack(fill="x", pady=5)

mode_label = ttk.Label(mode_frame, text="Listening", font=("Arial", 14))
mode_label.pack(pady=10)

# ----------------------------
# Feedback Panel
# ----------------------------

feedback_frame = ttk.Labelframe(left, text="User Feedback", style="Panel.TLabelframe")
feedback_frame.pack(fill="x", pady=5)

feedback_label = ttk.Label(feedback_frame, text="Last: 👍 Witzig")
feedback_label.pack(pady=10)

# ----------------------------
# Learning Log
# ----------------------------

learning_frame = ttk.Labelframe(left, text="Learning Events (Transparent)",
                                style="Panel.TLabelframe")
learning_frame.pack(fill="both", expand=True, pady=5)

learning_list = tk.Listbox(learning_frame, bg="#111", fg="lime")
learning_list.pack(fill="both", expand=True, padx=5, pady=5)

# ----------------------------
# Persona Panel
# ----------------------------

persona_frame = ttk.Labelframe(right, text="Persona", style="Panel.TLabelframe")
persona_frame.pack(fill="x", pady=5)

voice_label = ttk.Label(persona_frame, text="Voice: Voice #3")
voice_label.pack(pady=2)

humor_label = ttk.Label(persona_frame, text="Humor: Medium")
humor_label.pack(pady=2)

# ----------------------------
# Hardware Panel
# ----------------------------

hardware_frame = ttk.Labelframe(right, text="Hardware Status", style="Panel.TLabelframe")
hardware_frame.pack(fill="x", pady=5)

ssd_label = ttk.Label(hardware_frame, text="SSD: 320 / 500 GB")
ssd_label.pack(pady=2)

speaker_label = ttk.Label(hardware_frame, text="Speakers: Online")
speaker_label.pack(pady=2)

camera_label = ttk.Label(hardware_frame, text="Camera: Idle")
camera_label.pack(pady=2)

# ----------------------------
# Update Loop (Simulation)
# ----------------------------

def update_state():
    mode_label.config(text=random.choice(MODES))
    feedback_label.config(text=random.choice(["👍 Witzig", "👌 Gut", "😐 Meh"]))

    voice_label.config(text=f"Voice: {random.choice(VOICES)}")
    humor_label.config(text=f"Humor: {random.choice(HUMOR_LEVELS)}")

    learning_list.insert(0, random.choice(learning_events))
    if learning_list.size() > 8:
        learning_list.delete(8)

    root.after(3000, update_state)

update_state()
root.mainloop()
