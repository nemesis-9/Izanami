import subprocess
import sys

subprocess.run(
    [sys.executable, "-m", "streamlit", "run", "ui/dashboard.py"],
    check=True,
)
