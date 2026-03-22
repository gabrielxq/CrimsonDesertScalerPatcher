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
address_font_main = None
address_font_fallback = None

val_ui = 100
val_hud = 100
enable_large_sub = False

def log_message(msg):
    text_log.config(state=tk.NORMAL)
    text_log.insert(tk.END, msg + "\n")
    text_log.see(tk.END)
    text_log.config(state=tk.DISABLED)

def freeze_loop():
    """This function runs in the background, writing to memory continuously."""
    global is_frozen, pm, address_ui, address_hud, val_ui, val_hud
    global address_font_main, address_font_fallback, enable_large_sub
    
    while is_frozen:
        try:
            if pm:
                # Freeze UI and HUD scales
                pm.write_int(address_ui, val_ui)
                pm.write_int(address_hud, val_hud)
                
                # Overwrite the 'Large' font preset IDs if enabled
                if enable_large_sub:
                    pm.write_int(address_font_main, 1007)
                    pm.write_int(address_font_fallback, 1006)
        except Exception:
            # If an error occurs (e.g., game closed), ignore silently to keep loop alive
            pass 
        
        # 0.1 second pause (10 writes per second, light on CPU usage)
        time.sleep(0.1) 

def toggle_freeze():
    global is_frozen, pm, address_ui, address_hud, val_ui, val_hud
    global address_font_main, address_font_fallback, enable_large_sub
    
    # If currently running, the button will STOP the injection
    if is_frozen:
        is_frozen = False
        
        # Revert font to default 'Large' (1006) if it was enabled
        if enable_large_sub and pm:
            try:
                pm.write_int(address_font_main, 1006)
                pm.write_int(address_font_fallback, 1005)
            except Exception:
                pass

        btn_apply.config(text="Apply & Freeze", bg="#f0f0f0")
        entry_ui.config(state=tk.NORMAL)
        entry_hud.config(state=tk.NORMAL)
        chk_sub.config(state=tk.NORMAL)
        log_message("[*] Injection paused. Memory reverted.")
        return

    # If stopped, the button will START the injection
    try:
        val_ui = int(entry_ui.get())
        val_hud = int(entry_hud.get())
        enable_large_sub = chk_sub_var.get()
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers (e.g., 100).")
        return

    process_name = "CrimsonDesert.exe"
    
    # Static Offsets
    offset_ui = 0x5C399D8
    offset_hud = 0x5C39A28
    offset_font_main = 0x5BBE2B0      # Database offset for Large Font ID
    offset_font_fallback = 0x5BBE2AC  # Database offset for Fallback Font ID

    try:
        log_message(f"[*] Attaching to {process_name}...")
        pm = pymem.Pymem(process_name)
        
        module = pymem.process.module_from_name(pm.process_handle, process_name)
        base_address = module.lpBaseOfDll
        
        # Calculate final dynamic addresses
        address_ui = base_address + offset_ui
        address_hud = base_address + offset_hud
        address_font_main = base_address + offset_font_main
        address_font_fallback = base_address + offset_font_fallback
        
        # Start the freeze mode
        is_frozen = True
        
        # Update UI to show active status
        btn_apply.config(text="Stop Freezing", bg="#ffcccc")
        entry_ui.config(state=tk.DISABLED)
        entry_hud.config(state=tk.DISABLED)
        chk_sub.config(state=tk.DISABLED)
        
        log_message(f"[+] Hooked! UI: {val_ui}, HUD: {val_hud}")
        if enable_large_sub:
            log_message("[+] Larger Subtitles Enabled!")
        
        # Create and start the background thread
        t = threading.Thread(target=freeze_loop, daemon=True)
        t.start()
        
    except pymem.exception.ProcessNotFound:
        log_message("[-] Error: Process not found. Is the game running?")
        messagebox.showerror("Error", "Process 'CrimsonDesert.exe' not found.\nPlease run the game first.")
    except Exception as e:
        log_message(f"[-] Unexpected Error: {e}")
        messagebox.showerror("Error", f"Something went wrong:\n{e}")

# ==========================================
# GUI Setup
# ==========================================
root = tk.Tk()
root.title("Crimson Desert - Scale Patcher | by GabrielXQ")
root.geometry("420x380")
root.resizable(False, False)

root.eval('tk::PlaceWindow . center')

frame_inputs = tk.Frame(root)
frame_inputs.pack(pady=15)

tk.Label(frame_inputs, text="UI Scale:", font=("Arial", 10)).grid(row=0, column=0, padx=5, pady=5, sticky="e")
entry_ui = tk.Entry(frame_inputs, justify="center", font=("Arial", 11), width=12)
entry_ui.grid(row=0, column=1, padx=5, pady=5)
entry_ui.insert(0, "100")

tk.Label(frame_inputs, text="HUD Scale:", font=("Arial", 10)).grid(row=1, column=0, padx=5, pady=5, sticky="e")
entry_hud = tk.Entry(frame_inputs, justify="center", font=("Arial", 11), width=12)
entry_hud.grid(row=1, column=1, padx=5, pady=5)
entry_hud.insert(0, "100")

# Subtitle Checkbox
chk_sub_var = tk.BooleanVar()
chk_sub = tk.Checkbutton(root, text="Enable Larger Subtitles", variable=chk_sub_var, font=("Arial", 10))
chk_sub.pack(pady=5)
# Mini container
frame_warning = tk.Frame(root)
frame_warning.pack(pady=(0, 10))

# Text in red
lbl_warning = tk.Label(frame_warning, text="Warning:", fg="red", font=("Arial", 9, "bold"))
lbl_warning.pack(side=tk.LEFT)

# Text after warning
lbl_desc = tk.Label(frame_warning, text="In-game subtitle size must be set to 'Large'.", font=("Arial", 9))
lbl_desc.pack(side=tk.LEFT)

btn_apply = tk.Button(root, text="Apply & Freeze", command=toggle_freeze, font=("Arial", 10, "bold"), bg="#f0f0f0", width=15)
btn_apply.pack(pady=10)

tk.Label(root, text="Debug Log:", font=("Arial", 9)).pack(anchor="w", padx=20)
text_log = tk.Text(root, height=8, width=50, font=("Consolas", 9), bg="#1e1e1e", fg="#00ff00", state=tk.DISABLED)
text_log.pack(pady=5)

root.mainloop()