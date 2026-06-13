import re
import subprocess

with open("pda_gift_app.py", "r", encoding="utf-8") as f:
    content = f.read()

match = re.search(r'PDA_VERSION\s*=\s*"([^"]+)"', content)

version = match.group(1)

subprocess.run([
    "pyinstaller",
    "--onefile",
    "--noconsole",
    "--name",
    f"КПК {version}",
    "--add-data",
    "button.wav;.",
    "--add-data",
    "photo_lghkbq.jpg;.",
    "--add-data",
    "arhive_video_NO3826.MP4;.",
    "--add-data",
    "arhive_video_NO67.MP4;.",
    "pda_gift_app.py"
])
