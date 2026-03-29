import tkinter as tk
from tkinter import messagebox
import pymem
import pymem.process
import threading
import time

# ==========================================
# Global Variables for Memory Loop
# ==========================================

pm = None
is_frozen = False
address_ui = None
address_hud = None

val_ui = 100
val_hud = 100

def log_message(msg):
    text_log.config(state=tk.NORMAL)
    text_log.insert(tk.END, msg + "\n")
    text_log.see(tk.END)
    text_log.config(state=tk.DISABLED)

def freeze_loop():
    """This function runs in the background, writing to memory continuously."""
    global is_frozen, pm, address_ui, address_hud, val_ui, val_hud
    
    while is_frozen:
        try:
            if pm:
                # Freeze UI and HUD scales
                pm.write_int(address_ui, val_ui)
                pm.write_int(address_hud, val_hud)
        except Exception:
            # If an error occurs (e.g., game closed), ignore silently to keep loop alive
            pass 
        
        # 0.1 second pause (10 writes per second, light on CPU usage)
        time.sleep(0.1) 

def toggle_freeze():
    global is_frozen, pm, address_ui, address_hud, val_ui, val_hud
    
    # If currently running, the button will STOP the injection
    if is_frozen:
        is_frozen = False
        
        btn_apply.config(text="Apply & Freeze", bg="#f0f0f0")
        entry_ui.config(state=tk.NORMAL)
        entry_hud.config(state=tk.NORMAL)
        log_message("[*] Injection paused. Memory reverted.")
        return

    # If stopped, the button will START the injection
    try:
        val_ui = int(entry_ui.get())
        val_hud = int(hud_var.get())
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers (e.g., 100).")
        return

    process_name = "CrimsonDesert.exe"
    
    # Static Offsets
    offset_ui = 0x5C74318
    offset_hud = 0x5C74368

    try:
        log_message(f"[*] Attaching to {process_name}...")
        pm = pymem.Pymem(process_name)
        
        module = pymem.process.module_from_name(pm.process_handle, process_name)
        base_address = module.lpBaseOfDll
        
        # Calculate final dynamic addresses
        address_ui = base_address + offset_ui
        address_hud = base_address + offset_hud

        # Start the freeze mode
        is_frozen = True
        
        # Update UI to show active status
        btn_apply.config(text="Stop Freezing", bg="#ffcccc")
        entry_ui.config(state=tk.DISABLED)
        entry_hud.config(state=tk.DISABLED)
        
        log_message(f"[+] Hooked! UI: {val_ui}, HUD: {val_hud}")
        
        # Create and start the background thread
        t = threading.Thread(target=freeze_loop, daemon=True)
        t.start()
        
    except pymem.exception.ProcessNotFound:
        log_message("[-] Error: Process not found. Is the game running?")
        messagebox.showerror("Error", "Process 'CrimsonDesert.exe' not found.\nPlease run the game first.")
    except Exception as e:
        log_message(f"[-] Unexpected Error: {e}")
        messagebox.showerror("Error", f"Something went wrong:\n{e}")

def check_hud_limit(*args):
    """Checks the input in real-time and shows a warning if > 110."""
    try:
        val = int(hud_var.get())
        if val > 110:
            lbl_hud_warning.config(text="Warning: Values bigger than 110 will break the pause menu!")
        else:
            lbl_hud_warning.config(text="")
    except ValueError:
        # Se o campo ficar vazio ou digitarem texto, limpa o aviso
        lbl_hud_warning.config(text="")


# ==========================================
# GUI Setup
# ==========================================
root = tk.Tk()
root.title("Crimson Desert - Scale Patcher | by GabrielXQ")
root.geometry("420x290")
root.resizable(False, False)

root.eval('tk::PlaceWindow . center')

frame_inputs = tk.Frame(root)
frame_inputs.pack(pady=15)

# UI Scale
tk.Label(frame_inputs, text="UI Scale:", font=("Arial", 10)).grid(row=0, column=0, padx=5, pady=5, sticky="e")
entry_ui = tk.Entry(frame_inputs, justify="center", font=("Arial", 11), width=12)
entry_ui.grid(row=0, column=1, padx=5, pady=5)
entry_ui.insert(0, "100")

# HUD Scale Variable (Para monitorar as mudanças em tempo real)
hud_var = tk.StringVar(value="100")
hud_var.trace_add("write", check_hud_limit)

# HUD Scale
tk.Label(frame_inputs, text="HUD Scale:", font=("Arial", 10)).grid(row=1, column=0, padx=5, pady=5, sticky="e")
entry_hud = tk.Entry(frame_inputs, justify="center", font=("Arial", 11), width=12, textvariable=hud_var)
entry_hud.grid(row=1, column=1, padx=5, pady=5)

# Warning Label (Fica invisível por padrão, ocupando as duas colunas)
lbl_hud_warning = tk.Label(frame_inputs, text="", fg="red", font=("Arial", 8, "bold"))
lbl_hud_warning.grid(row=2, column=0, columnspan=2, pady=0)

btn_apply = tk.Button(root, text="Apply & Freeze", command=toggle_freeze, font=("Arial", 10, "bold"), bg="#f0f0f0", width=15)
btn_apply.pack(pady=5)

tk.Label(root, text="Debug Log:", font=("Arial", 9)).pack(anchor="w", padx=20)
text_log = tk.Text(root, height=8, width=50, font=("Consolas", 9), bg="#1e1e1e", fg="#00ff00", state=tk.DISABLED)
text_log.pack(pady=5)

root.mainloop()
