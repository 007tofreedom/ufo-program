"""
UFO Program - Sentinel Frequency Research
Simple Launcher with Loading Screen
"""

import time
import sys

def loading_bar(duration=4):
    print("Initializing Sentinel Frequency System...")
    print("=" * 70)
    print("🛸 UFO PROGRAM - SENTINEL FREQUENCY ONLINE 🛸")
    print("Green Frequency • Lightning Bug Cloak • ISS 2.0 Link")
    print("No Harm Near Protocol Active")
    print("=" * 70)
    print()
    
    # Loading bar
    print("Loading Core Systems...")
    for i in range(21):
        percent = i * 5
        bar = "█" * i + "░" * (20 - i)
        sys.stdout.write(f"\r[{bar}] {percent}%")
        sys.stdout.flush()
        time.sleep(duration / 20)  # Makes it last ~4 seconds total
    
    print("\n\n✅ Systems Online")
    print("Launching full simulation...\n")

# Show loading screen
loading_bar()

# Launch your original big program
from ufo_interactive_super_advanced_disc_combined_with_api_realtime import main as run_ufo
run_ufo()
