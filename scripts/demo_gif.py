#!/usr/bin/env python3
"""Demo script for recording neo-says terminal demos.

Usage:
    python scripts/demo_gif.py

For recording with asciinema:
    asciinema rec demo.cast -c "python scripts/demo_gif.py"

Then convert to GIF:
    agg demo.cast demo.gif
"""

import subprocess
import sys
import time

# Delays (in seconds) for readability during recording
SECTION_DELAY = 2.0
COMMAND_DELAY = 1.5
SHORT_DELAY = 0.8


def print_header(title: str) -> None:
    """Print a section header with visual separation."""
    width = 60
    print()
    print(f"\033[1;36m{'=' * width}\033[0m")
    print(f"\033[1;36m  {title}\033[0m")
    print(f"\033[1;36m{'=' * width}\033[0m")
    print()
    time.sleep(SHORT_DELAY)


def print_command(cmd: str) -> None:
    """Print the command being run, simulating a typed prompt."""
    print(f"\033[1;32m$ {cmd}\033[0m")
    time.sleep(SHORT_DELAY)


def run(cmd: str, delay: float = COMMAND_DELAY) -> None:
    """Run a shell command, print it, and wait for readability."""
    print_command(cmd)
    result = subprocess.run(cmd, shell=True, capture_output=False)
    if result.returncode != 0:
        print(f"\033[33m(exit code: {result.returncode})\033[0m")
    time.sleep(delay)


def main() -> None:
    """Run through all neo-says demo sections."""
    print("\033[1;35m")
    print("  ┌─────────────────────────────────────┐")
    print("  │       neo-says Feature Demo          │")
    print("  │   Snarky CLI Fortune Teller v7.0     │")
    print("  └─────────────────────────────────────┘")
    print("\033[0m")
    time.sleep(SECTION_DELAY)

    # ------------------------------------------------------------------
    # Section 1: Basic Usage
    # ------------------------------------------------------------------
    print_header("1. Basic Usage -- Random Developer Wisdom")

    run("neo-says")
    run("neo-says")
    run("neo-says --today")

    # ------------------------------------------------------------------
    # Section 2: Themes
    # ------------------------------------------------------------------
    print_header("2. Themes -- Pick Your Style")

    run("neo-says --theme box")
    run("neo-says --theme minimal")
    run("neo-says --theme ascii-art")
    run("neo-says --theme cowsay")

    # ------------------------------------------------------------------
    # Section 3: Categories & Tags
    # ------------------------------------------------------------------
    print_header("3. Filtering -- Categories & Tags")

    run("neo-says -l")
    time.sleep(SHORT_DELAY)

    run("neo-says -c git")
    run("neo-says -c debugging")

    run("neo-says --list-tags")
    time.sleep(SHORT_DELAY)

    run("neo-says -t wisdom")

    # ------------------------------------------------------------------
    # Section 4: Language Switching (i18n)
    # ------------------------------------------------------------------
    print_header("4. Internationalization -- Multilingual Snark")

    run("neo-says --lang en")
    run("neo-says --lang ko")
    run("neo-says --lang ja")

    # ------------------------------------------------------------------
    # Section 5: Raw Output / Piping
    # ------------------------------------------------------------------
    print_header("5. Raw Output -- Pipe-Friendly Mode")

    run("neo-says --raw")
    run("neo-says --raw -c git")

    # ------------------------------------------------------------------
    # Section 6: Configuration
    # ------------------------------------------------------------------
    print_header("6. Configuration -- Set Defaults")

    run("neo-says --set-theme minimal")
    run("neo-says")
    run("neo-says --set-theme box")
    run("neo-says --set-lang ko")
    run("neo-says")
    run("neo-says --set-lang en")

    # ------------------------------------------------------------------
    # Section 7: Quote Packs
    # ------------------------------------------------------------------
    print_header("7. Quote Packs -- Community Extensions")

    # Create a temporary demo pack
    demo_pack = "/tmp/demo-pack.yaml"
    pack_content = """\
name: demo-pack
version: "1.0.0"
description: "A demo pack for the recording"
author: neo

quotes:
  - text: "This quote was loaded from a custom pack. Impressed yet?"
    category: demo
    tags: [meta]
    weight: 5
  - text: "Packs let anyone extend neo-says. The power is yours."
    category: demo
    tags: [meta, wisdom]
    weight: 5
"""
    with open(demo_pack, "w") as f:
        f.write(pack_content)

    run(f"neo-says pack install {demo_pack}")
    run("neo-says pack list")
    run("neo-says --pack demo-pack")
    run("neo-says --pack demo-pack --theme cowsay")
    run("neo-says pack remove demo-pack")

    # Clean up
    import os
    os.remove(demo_pack)

    # ------------------------------------------------------------------
    # Outro
    # ------------------------------------------------------------------
    print()
    print(f"\033[1;35m{'=' * 60}\033[0m")
    print("\033[1;35m  That's neo-says! Install it:\033[0m")
    print()
    print("\033[1;37m    pip install neo-says\033[0m")
    print()
    print("\033[1;35m  GitHub: https://github.com/mongsill6/neo-says\033[0m")
    print(f"\033[1;35m{'=' * 60}\033[0m")
    print()
    time.sleep(SECTION_DELAY)


if __name__ == "__main__":
    main()
