"""Run the Streamlit travel planner app"""

import subprocess
import sys


def main():
    print("🚀 Starting Travel Planner...")
    print("📱 Open: http://localhost:8501")
    print("⏹️  Ctrl+C to stop")

    subprocess.run(
        [sys.executable, "-m", "streamlit", "run", "streamlit_app.py"], check=False
    )


if __name__ == "__main__":
    main()
