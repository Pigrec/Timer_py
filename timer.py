import tkinter as tk
from datetime import datetime

min_height = 250
min_width = 500

paused = False  # variabile globale per pausa/play

def start_timer():
    try:
        h = int(hour_entry.get())
        m = int(min_entry.get())
        s = int(sec_entry.get())
        direction = var.get()
    except ValueError:
        return
    
    root.destroy()
    run_timer(h, m, s, direction)

def run_timer(h, m, s, direction):
    global paused
    timer_root = tk.Tk()
    timer_root.title("Timer")
    timer_root.configure(bg='black')
    timer_root.geometry(f"{min_width}x{min_height}")
    timer_root.minsize(min_width, min_height)
    
    total_seconds_initial = h*3600 + m*60 + s
    total_seconds = [total_seconds_initial]  # lista mutabile per accesso interno
    start_time = [0]

    label = tk.Label(timer_root, text="", fg="white", bg="black")
    label.pack(expand=True, fill="both")

    # Label per ora esatta
    clock_label = tk.Label(timer_root, fg="gray", bg="black", font=("Helvetica", 12))
    clock_label.pack(side="bottom", anchor="e", padx=10, pady=5)

    def update_font():
        w, h_win = timer_root.winfo_width(), timer_root.winfo_height()
        size = min(w//10, h_win//2)
        label.config(font=("Helvetica", size))
        timer_root.after(100, update_font)

    def format_time(t):
        return f"{t//3600:02}:{(t%3600)//60:02}:{t%60:02}"

    def update_clock():
        now = datetime.now().strftime("%H:%M:%S")
        clock_label.config(text=now)
        timer_root.after(500, update_clock)

    blinking = [False]  # stato del lampeggio

    def blink():
        if not blinking[0]:
            return
        current_fg = label.cget("fg")
        current_bg = label.cget("bg")
        label.config(fg=current_bg, bg=current_fg)
        timer_root.after(500, blink)

    def tick():
        if paused:
            timer_root.after(100, tick)
            return

        if direction == "Decrescente":
            if total_seconds[0] >= 0:
                label.config(text="-" + format_time(total_seconds[0]))
                total_seconds[0] -= 1
                timer_root.after(1000, tick)
            else:
                blinking[0] = True
                blink()
        else:  # Crescente
            if start_time[0] <= total_seconds_initial:
                label.config(text="+" + format_time(start_time[0]))
                start_time[0] += 1
                timer_root.after(1000, tick)
            else:
                blinking[0] = True
                blink()

    def reset_timer():
        global paused
        paused = False
        blinking[0] = False  # interrompe il lampeggio
        total_seconds[0] = total_seconds_initial
        start_time[0] = 0
        tick()


    def toggle_pause():
        global paused
        paused = not paused
        pause_button.config(text="Play" if paused else "Pausa")

    # Pulsanti
    button_frame = tk.Frame(timer_root, bg="black")
    button_frame.pack(side="bottom", pady=10)
    reset_button = tk.Button(button_frame, text="Reset", command=reset_timer)
    reset_button.pack(side="left", padx=10)
    pause_button = tk.Button(button_frame, text="Pausa", command=toggle_pause)
    pause_button.pack(side="left", padx=10)

    update_font()
    update_clock()
    tick()
    timer_root.mainloop()

# Schermata iniziale
root = tk.Tk()
root.title("Timer UltraLeggero")
root.geometry(f"{min_width}x{min_height}")
root.minsize(min_width, min_height)

# Centrare il contenuto
frame = tk.Frame(root)
frame.place(relx=0.5, rely=0.5, anchor="center")

tk.Label(frame, text="Ore:").grid(row=0, column=0, padx=5, pady=5)
hour_entry = tk.Entry(frame, width=5)
hour_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame, text="Minuti:").grid(row=1, column=0, padx=5, pady=5)
min_entry = tk.Entry(frame, width=5)
min_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame, text="Secondi:").grid(row=2, column=0, padx=5, pady=5)
sec_entry = tk.Entry(frame, width=5)
sec_entry.grid(row=2, column=1, padx=5, pady=5)

var = tk.StringVar(value="Decrescente")
tk.Radiobutton(frame, text="Crescente", variable=var, value="Crescente").grid(row=3, column=0, padx=5, pady=5)
tk.Radiobutton(frame, text="Decrescente", variable=var, value="Decrescente").grid(row=3, column=1, padx=5, pady=5)

tk.Button(frame, text="OK", command=start_timer).grid(row=4, column=0, columnspan=2, pady=10)

root.mainloop()
