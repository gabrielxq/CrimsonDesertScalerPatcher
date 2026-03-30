import pymem
import pymem.process
import sys
import time
import argparse

def main():
    parser = argparse.ArgumentParser(description="Crimson Desert Auto Scale Patcher")
    parser.add_argument("--ui", type=int, default=100, help="UI Scale value (default: 100)")
    parser.add_argument("--hud", type=int, default=100, help="HUD Scale value (default: 100)")
    parser.add_argument("--subs", action="store_true", help="Enable larger subtitles")
    parser.add_argument("--wait", type=int, default=120, help="Max seconds to wait for game (default: 120)")
    args = parser.parse_args()

    process_name = "CrimsonDesert.exe"

    # Static Offsets
    offset_ui = 0x5C491B8
    offset_hud = 0x5C49208
    offset_font_main = 0x5BCDA04
    offset_font_fallback = 0x5BCDA00

    print(f"[*] Waiting for {process_name}... (timeout: {args.wait}s)")

    # Wait for the game process to appear
    pm = None
    waited = 0
    while waited < args.wait:
        try:
            pm = pymem.Pymem(process_name)
            break
        except pymem.exception.ProcessNotFound:
            time.sleep(2)
            waited += 2

    if pm is None:
        print(f"[-] Timed out waiting for {process_name} after {args.wait}s.")
        sys.exit(1)

    print(f"[+] Found {process_name}! Attaching...")

    # Give the game a moment to fully initialize its memory
    time.sleep(5)

    try:
        module = pymem.process.module_from_name(pm.process_handle, process_name)
        base_address = module.lpBaseOfDll

        address_ui = base_address + offset_ui
        address_hud = base_address + offset_hud
        address_font_main = base_address + offset_font_main
        address_font_fallback = base_address + offset_font_fallback

        print(f"[+] Hooked! UI: {args.ui}, HUD: {args.hud}, Subs: {'ON' if args.subs else 'OFF'}")
        print("[*] Freezing values... (close this window to stop)")

        # Freeze loop - runs until game closes or window is closed
        while True:
            try:
                pm.write_int(address_ui, args.ui)
                pm.write_int(address_hud, args.hud)

                if args.subs:
                    pm.write_int(address_font_main, 1010)
                    pm.write_int(address_font_fallback, 1009)
            except Exception:
                # Game likely closed
                print("[*] Game closed. Exiting.")
                break

            time.sleep(0.1)

    except Exception as e:
        print(f"[-] Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
