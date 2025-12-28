import subprocess, sys
from pathlib import Path

subprocess.run(
    [sys.executable, "-m", "streamlit", "run", "ui/dashboard.py"],
    check=True,
)
