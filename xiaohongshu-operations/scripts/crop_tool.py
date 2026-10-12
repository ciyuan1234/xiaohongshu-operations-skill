#!/usr/bin/env python3
"""Xiaohongshu 3:4 aspect ratio image preparation tool.

Crops raw desktop screenshots or product images to standard 3:4 ratio (1080x1440).
Uses macOS native `sips` when available, falling back to Pillow.
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path


def crop_with_sips(input_path: Path, output_path: Path, target_w: int = 1080, target_h: int = 1440) -> bool:
    """Use macOS native sips utility to crop and resize."""
    # First get original dimensions
    try:
        out_w = subprocess.check_output(["sips", "-g", "pixelWidth", str(input_path)], text=True)
        out_h = subprocess.check_output(["sips", "-g", "pixelHeight", str(input_path)], text=True)
        orig_w = int(out_w.strip().split()[-1])
        orig_h = int(out_h.strip().split()[-1])
    except Exception as e:
        print(f"sips dimension inspection failed: {e}", file=sys.stderr)
        return False

    # Calculate 3:4 centered crop box
    target_ratio = 3.0 / 4.0
    current_ratio = orig_w / orig_h

    if current_ratio > target_ratio:
        # Too wide, crop width
        crop_h = orig_h
        crop_w = int(orig_h * target_ratio)
    else:
        # Too tall, crop height
        crop_w = orig_w
        crop_h = int(orig_w / target_ratio)

    shutil.copy2(input_path, output_path)

    # Crop to 3:4
    cmd_crop = ["sips", "-c", str(crop_h), str(crop_w), str(output_path)]
    res = subprocess.run(cmd_crop, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"sips crop failed: {res.stderr}", file=sys.stderr)
        return False

    # Resize to target 1080x1440
    cmd_resize = ["sips", "-z", str(target_h), str(target_w), str(output_path)]
    res2 = subprocess.run(cmd_resize, capture_output=True, text=True)
    if res2.returncode != 0:
        print(f"sips resize failed: {res2.stderr}", file=sys.stderr)
        return False

    return True


def crop_with_pillow(input_path: Path, output_path: Path, target_w: int = 1080, target_h: int = 1440) -> bool:
    try:
        from PIL import Image
    except ImportError:
        return False

    with Image.open(input_path) as img:
        orig_w, orig_h = img.size
        target_ratio = 3.0 / 4.0
        current_ratio = orig_w / orig_h

        if current_ratio > target_ratio:
            crop_h = orig_h
            crop_w = int(orig_h * target_ratio)
        else:
            crop_w = orig_w
            crop_h = int(orig_w / target_ratio)

        left = (orig_w - crop_w) // 2
        top = (orig_h - crop_h) // 2
        right = left + crop_w
        bottom = top + crop_h

        cropped = img.crop((left, top, right, bottom))
        resized = cropped.resize((target_w, target_h), Image.Resampling.LANCZOS)
        resized.save(output_path)
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Crop image to 3:4 ratio for Xiaohongshu")
    parser.add_argument("--input", "-i", required=True, type=Path, help="Input image file")
    parser.add_argument("--output", "-o", required=True, type=Path, help="Output image file")
    parser.add_argument("--width", type=int, default=1080, help="Target width (default: 1080)")
    parser.add_argument("--height", type=int, default=1440, help="Target height (default: 1440)")
    args = parser.parse_args()

    if not args.input.exists():
        print(f"Error: input file {args.input} does not exist", file=sys.stderr)
        return 1

    success = False
    if shutil.which("sips"):
        success = crop_with_sips(args.input, args.output, args.width, args.height)

    if not success:
        success = crop_with_pillow(args.input, args.output, args.width, args.height)

    if success:
        print(f"[+] Successfully cropped to 3:4 ({args.width}x{args.height}) -> {args.output}")
        return 0
    else:
        print("[-] Failed: neither 'sips' nor Pillow is available or processing failed", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
