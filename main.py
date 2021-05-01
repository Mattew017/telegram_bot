import os
import subprocess
import sys

#input("Нажми Enter чтобы запустить...")

while True:
    process = subprocess.Popen([sys.executable, "bot.py"])
    process.wait()
