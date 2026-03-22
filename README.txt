About this Tool

Crimson Desert currently locks the maximum UI and HUD scale at 100%, which is honestly terrible for high-res monitors or accessibility. I got desperate trying to read the tiny text, so I threw together this quick memory patcher to force the game to accept higher values. I also added a small toggle to bump the subtitle size a bit past the game's default maximum.

READ THIS BEFORE DOWNLOADING
Let me be completely clear: this is not a perfect, definitive fix. It’s a very basic, rushed workaround born out of pure necessity. I didn't spend days polishing this because Pearl Abyss will almost certainly drop an official patch with a proper UI slider soon (at least I hope).
This is just a temporary band-aid so I can actually play the game right now.

Because the game wasn't designed to scale past 100%, if you push the numbers too high (like 140+), the UI and HUD elements will probably start overlapping each other. You'll have to play around with the values to find what looks acceptable on your screen.

How to Use (The .EXE version)

Launch Crimson Desert and load your save.
Run the tool.
Type your desired UI and HUD scale (e.g., 120).
If you want larger subtitles, check the box (Important: your in-game subtitle size must be set to "Large" for this to work).
Click "Apply & Freeze".
Go back to the game. Open the config menu and change any option (e.g., audio volume) to force the interface to refresh.

Important: Leave the tool running in the background while you play, or the game will eventually reset the UI back to 100.

False Positives & Source Code
Because this tool actively injects and freezes memory addresses (like Cheat Engine does), Windows Defender or browser scanners will probably flag the .exe as a virus or trojan. If you don't trust the compiled .exe, I totally get it. You can find the raw Python source code (the .py file) here on my GitHub. You can read the code yourself and run it directly from your machine after analyzing it.

How to run the raw Python script instead:

Download and install Python on your PC.
Open your command prompt (cmd) as Admin.
Install the required library by typing:

pip install pymem

Run the script by typing:
python CDScalePatcher.py