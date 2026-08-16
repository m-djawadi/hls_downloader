#!/usr/bin/env python3
"""
Simple HLS downloader using yt-dlp + FFmpeg.

Use only with media you are authorized to access and download.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def check_dependency(command: str, install_hint: str) -> None:
    """Exit with a helpful message if a required executable is unavailable."""
    if shutil.which(command) is None:
        print(f"Error: '{command}' was not found in PATH.")
        print(install_hint)
        sys.exit(1)


def build_command(
    url: str,
    output: str,
    referer: str | None = None,
    origin: str | None = None,
) -> list[str]:
    """Build the yt-dlp command."""
    command = [
        sys.executable,
        "-m",
        "yt_dlp",
        "--remux-video",
        "mp4",
        "--no-part",
        "-o",
        output,
    ]

    if referer:
        command.extend(["--add-header", f"Referer:{referer}"])

    if origin:
        command.extend(["--add-header", f"Origin:{origin}"])

    command.append(url)
    return command


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download an HLS (.m3u8) stream and remux it into a normal MP4 file."
    )
    parser.add_argument(
        "url",
        help="The HLS playlist URL ending in .m3u8",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="video.%(ext)s",
        help='Output template (default: "video.%%(ext)s")',
    )
    parser.add_argument(
        "--referer",
        help="Optional Referer header required by some authorized streams.",
    )
    parser.add_argument(
        "--origin",
        help="Optional Origin header required by some authorized streams.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if ".m3u8" not in args.url.lower():
        print("Warning: the supplied URL does not appear to be an .m3u8 playlist.")

    # yt-dlp is invoked as a Python module, so verify that it is installed.
    try:
        subprocess.run(
            [sys.executable, "-m", "yt_dlp", "--version"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True,
        )
    except subprocess.CalledProcessError:
        print("Error: yt-dlp is not installed in this Python environment.")
        print("Install it with:")
        print("  python -m pip install -U yt-dlp")
        sys.exit(1)

    check_dependency(
        "ffmpeg",
        "Install FFmpeg and make sure the ffmpeg executable is available in PATH.",
    )

    command = build_command(
        url=args.url,
        output=args.output,
        referer=args.referer,
        origin=args.origin,
    )

    print("Starting download...")
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as exc:
        print(f"\nDownload failed with exit code {exc.returncode}.")
        sys.exit(exc.returncode)

    print("\nDone.")


if __name__ == "__main__":
    main()
