# Crimson Desert UI Scale Patcher

## About This Tool

Crimson Desert currently locks the maximum UI and HUD scale at **100%**, which is problematic for high-resolution monitors and accessibility.

This tool is a simple memory patcher that forces the game to accept higher UI scale values. It also includes an optional toggle to slightly increase subtitle size beyond the game's default maximum.

This was created as a quick workaround to make the game playable with readable UI text.

---

## Disclaimer

**Read this before downloading**

This is **not a polished or definitive fix**. It is a basic, rushed workaround created out of necessity.

An official patch from Pearl Abyss is likely to address this properly in the future. Until then, this tool serves as a temporary solution.

Because the game was not designed to scale beyond 100%, setting very high values (e.g., 140% or more) may cause UI and HUD elements to overlap. You will need to experiment to find values that work best for your setup.

---

## How to Use (.EXE Version on the RELEASES tab)

1. Launch *Crimson Desert* and load your save.
2. Run the tool.
3. Enter your desired UI/HUD scale (e.g., `120`).
4. (Optional) Enable larger subtitles:
   - Your in-game subtitle size must be set to **Large** for this to work.
5. Click **Apply & Freeze**.
6. Return to the game.
7. Open the settings menu and change any option (e.g., audio volume) to refresh the interface.

### Important

You must leave the tool running in the background while playing.  
If you close it, the game will revert the UI scale back to 100%.

---

## False Positives & Source Code

This tool modifies and freezes memory addresses (similar to Cheat Engine behavior). Because of this:

- Windows Defender or browser scanners may flag the `.exe` as a virus or trojan.
- These are **false positives** caused by the nature of the tool.

If you do not trust the compiled executable, you can:

- Review the raw Python source code provided in this repository
- Run the script manually after verifying its contents

---

## Running the Python Script Manually

### Requirements

- Python installed on your system

### Steps

1. Open Command Prompt as Administrator
2. Install the required dependency:

pip install pymem

3. Run the script by typing:

python CDScalePatcher.py
