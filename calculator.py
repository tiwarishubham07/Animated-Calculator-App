import customtkinter as ctk
import math, time, threading
from playsound import playsound

# ========== WINDOW SETUP ==========
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("🔥 Animated Neon Calculator 🔥")
app.geometry("420x600")
app.resizable(False, False)

# ========== FUNCTIONS ==========
def btn_click(value):
    playsound_thread()           # click sound
    entry.insert("end", value)

def clear():
    playsound_thread()
    entry.delete(0, "end")

def calculate():
    playsound_thread()
    try:
        result = str(eval(entry.get()))
        entry.delete(0, "end")
        entry.insert("end", result)
    except:
        entry.delete(0, "end")
        entry.insert("end", "Error")

# small thread so sound doesn’t freeze UI
def playsound_thread():
    threading.Thread(target=lambda: playsound("https://github.com/itsron717/sound/raw/main/click.mp3")).start()

# ========== ENTRY BOX ==========
entry = ctk.CTkEntry(app, width=380, height=70, font=("Poppins", 30),
                     corner_radius=12, justify="right")
entry.place(x=20, y=30)

# ========== BUTTONS ==========
buttons = [
    ["7", "8", "9", "/"],
    ["4", "5", "6", "*"],
    ["1", "2", "3", "-"],
    ["C", "0", "=", "+"]
]

def create_button(text, x, y, color="#1f1f1f", hover="#00fff0", command=None):
    return ctk.CTkButton(app, text=text, width=80, height=60,
                         fg_color=color, hover_color=hover,
                         font=("Poppins", 20, "bold"), command=command)

y = 120
for row in buttons:
    x = 20
    for btn in row:
        if btn == "=":
            b = create_button(btn, x, y, color="#00fff0", hover="#00e6d1", command=calculate)
        elif btn == "C":
            b = create_button(btn, x, y, color="#ff3b3b", hover="#ff6666", command=clear)
        else:
            b = create_button(btn, x, y, command=lambda val=btn: btn_click(val))
        b.place(x=x, y=y)
        x += 95
    y += 80

# ========== ANIMATED BACKGROUND ==========
canvas = ctk.CTkCanvas(app, width=420, height=600, bg="#0f2027", highlightthickness=0)
canvas.place(x=0, y=0)

# move glowing orbs slowly
orbs = []
for i in range(10):
    orb = canvas.create_oval(0,0,0,0, fill="#00fff0", outline="")
    orbs.append([orb, i*40, i*60])

def animate_background():
    while True:
        for i, (orb, x, y) in enumerate(orbs):
            new_x = 200 + 150*math.sin(time.time()+i)
            new_y = 300 + 150*math.cos(time.time()+i)
            size = 40 + 20*math.sin(time.time()*1.5+i)
            canvas.coords(orb, new_x, new_y, new_x+size, new_y+size)
        time.sleep(0.03)

threading.Thread(target=animate_background, daemon=True).start()

# bring widgets to front
entry.lift()
for w in app.winfo_children():
    if isinstance(w, ctk.CTkButton):
        w.lift()

# ========== RUN ==========
app.mainloop()