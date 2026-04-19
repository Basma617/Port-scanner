import tkinter as tk
from tkinter import ttk
from scan import run_scan
import threading
import os

# ── colours ─────────────────────────────────────────────
BG      = "#0d0d0d"
PANEL   = "#111111"
ACCENT  = "#00ff88"
TEXT    = "#00ff88"
ENTRY   = "#1a1a1a"
BORDER  = "#2a2a2a"
MONO    = ("Courier New", 11)

def start_scan():
    ip   = ip_entry.get()
    mode = mode_var.get()

    if mode == "1":
        ports_input    = ports_entry.get()
        first_port_val = last_port_val = None
    else:
        ports_input = None
        try:
            first_port_val = int(start_port_entry.get())
            last_port_val  = int(end_port_entry.get())
        except ValueError:
            result_text.config(state="normal")
            result_text.delete("1.0", tk.END)
            result_text.insert(tk.END, "Start and End ports must be integers!\n")
            result_text.config(state="disabled")
            return

    result_text.config(state="normal")
    result_text.delete("1.0", tk.END)
    result_text.insert(tk.END, "Starting scan...\n")
    result_text.config(state="disabled")

    def task():
        output = run_scan(
            target_IP=ip,
            mode=mode,
            ports_input=ports_input,
            first_port=first_port_val,
            last_port=last_port_val
        )
        result_text.config(state="normal")
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, output)
        result_text.config(state="disabled")

    threading.Thread(target=task, daemon=True).start()


def update_input_fields():
    mode = mode_var.get()
    if mode == "1":
        ports_label.grid(row=0, column=0, sticky="w", pady=(0, 4))
        ports_entry.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        start_port_label.grid_forget()
        start_port_entry.grid_forget()
        end_port_label.grid_forget()
        end_port_entry.grid_forget()
    else:
        ports_label.grid_forget()
        ports_entry.grid_forget()
        start_port_label.grid(row=0, column=0, sticky="w", pady=(0, 4))
        start_port_entry.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        end_port_label.grid(row=2, column=0, sticky="w", pady=(0, 4))
        end_port_entry.grid(row=3, column=0, sticky="ew", pady=(0, 10))


def run_app():
    global ip_entry, ports_entry, start_port_entry, end_port_entry
    global result_text, mode_var
    global ports_label, start_port_label, end_port_label

    root = tk.Tk()
    root.title("PORTSCANNER")
    root.geometry("900x540")
    root.configure(bg=BG)
    root.resizable(True, True)

    icon_path = "scanner_icon.ico"
    if os.path.exists(icon_path):
        try:
            root.iconbitmap(icon_path)
        except Exception:
            pass

    # ── title bar ────────────────────────────────────────
    title_bar = tk.Frame(root, bg=BG)
    title_bar.pack(fill="x", padx=20, pady=(16, 10))
    tk.Label(title_bar, text="PORTSCANNER",
             font=("Courier New", 22, "bold"),
             fg=ACCENT, bg=BG).pack(side="left")

    tk.Frame(root, bg=BORDER, height=1).pack(fill="x", padx=20)

    # ── main body ────────────────────────────────────────
    body = tk.Frame(root, bg=BG)
    body.pack(fill="both", expand=True, padx=20, pady=14)

    # left panel
    left = tk.Frame(body, bg=BG, width=280)
    left.pack(side="left", fill="y")
    left.pack_propagate(False)

    # right panel
    tk.Frame(body, bg=BORDER, width=1).pack(side="left", fill="y", padx=(16, 16))
    right = tk.Frame(body, bg=BG)
    right.pack(side="left", fill="both", expand=True)

    # ── TARGET ───────────────────────────────────────────
    tk.Label(left, text="TARGET IP", font=("Courier New", 11, "bold"),
             fg=ACCENT, bg=BG).pack(anchor="w", pady=(0, 6))

    ip_entry = tk.Entry(left, font=MONO, bg=ENTRY, fg=ACCENT,
                        insertbackground=ACCENT, relief="flat",
                        highlightthickness=1,
                        highlightbackground=BORDER,
                        highlightcolor=ACCENT)
    ip_entry.pack(fill="x", ipady=6, pady=(0, 18))

    # ── SCAN MODE ────────────────────────────────────────
    tk.Label(left, text="SCAN MODE", font=("Courier New", 11, "bold"),
             fg=ACCENT, bg=BG).pack(anchor="w", pady=(0, 8))

    mode_var = tk.StringVar(value="2")

    for val, lbl in [("2", "Port Range"), ("1", "Specific Ports")]:
        tk.Radiobutton(left, text=lbl, variable=mode_var, value=val,
                       command=update_input_fields,
                       fg=ACCENT, bg=BG, selectcolor=BG,
                       activebackground=BG, activeforeground=ACCENT,
                       font=MONO).pack(anchor="w")

    tk.Frame(left, bg=BG, height=10).pack()

    # ── dynamic input fields ─────────────────────────────
    input_frame = tk.Frame(left, bg=BG)
    input_frame.pack(fill="x")
    input_frame.columnconfigure(0, weight=1)

    def make_entry():
        return tk.Entry(input_frame, font=MONO, bg=ENTRY, fg=ACCENT,
                        insertbackground=ACCENT, relief="flat",
                        highlightthickness=1,
                        highlightbackground=BORDER,
                        highlightcolor=ACCENT)

    def make_label(txt):
        return tk.Label(input_frame, text=txt, font=MONO,
                        fg=ACCENT, bg=BG)

    ports_label      = make_label("Ports (80,443,...)")
    ports_entry      = make_entry()
    start_port_label = make_label("Start Port")
    start_port_entry = make_entry()
    end_port_label   = make_label("End Port")
    end_port_entry   = make_entry()

    update_input_fields()

    # ── START button ─────────────────────────────────────
    tk.Frame(left, bg=BG, height=14).pack()
    tk.Button(left, text="▶  START SCAN",
              font=("Courier New", 13, "bold"),
              fg=BG, bg=ACCENT,
              activebackground="#00cc66",
              activeforeground=BG,
              relief="flat", bd=0, pady=12,
              cursor="hand2",
              command=start_scan).pack(fill="x")

    # ── TERMINAL (right) ─────────────────────────────────
    tk.Label(right, text="TERMINAL", font=("Courier New", 11, "bold"),
             fg=ACCENT, bg=BG).pack(anchor="w", pady=(0, 8))

    result_text = tk.Text(right, font=MONO, bg="#080808", fg=ACCENT,
                          insertbackground=ACCENT, relief="flat",
                          state="disabled", selectbackground=BORDER)
    result_text.pack(fill="both", expand=True)

    root.mainloop()