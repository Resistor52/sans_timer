#!/usr/bin/env python3
"""
Create a digital timer icon for the SANS Timer application.
This script generates a digital timer icon with HH:MM:SS format.
"""

import os
import sys
from PIL import Image, ImageDraw, ImageFont

def create_timer_icon(output_path="timer_icon.ico", size=256):
    """Create a digital timer icon with HH:MM:SS format"""
    try:
        # Check if icon already exists
        if os.path.exists(output_path):
            print(f"Icon already exists at {output_path}")
            return True
            
        # Create a new image with a black background
        img = Image.new('RGB', (size, size), (0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Try to load Arial font, fall back to default if not available
        try:
            # Try to find Arial Bold font
            font_paths = [
                # Windows font paths
                "C:/Windows/Fonts/arialbd.ttf",
                # macOS font paths
                "/Library/Fonts/Arial Bold.ttf",
                "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
                # Linux font paths
                "/usr/share/fonts/truetype/msttcorefonts/arialbd.ttf",
                "/usr/share/fonts/TTF/arialbd.ttf"
            ]
            
            font = None
            for path in font_paths:
                if os.path.exists(path):
                    font = ImageFont.truetype(path, size // 5)
                    break
                    
            if font is None:
                # Use default font if Arial not found
                font = ImageFont.load_default()
                font_size = size // 8
        except Exception:
            # Use default font if there's any error
            font = ImageFont.load_default()
            font_size = size // 8
        
        # Draw digital time "00:14:23" instead of "00:00:00"
        text = "00:14:23"
        
        # Calculate text position to center it
        try:
            # For newer Pillow versions
            text_bbox = draw.textbbox((0, 0), text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
        except AttributeError:
            # For older Pillow versions
            text_width, text_height = draw.textsize(text, font=font)
        
        text_x = (size - text_width) // 2
        text_y = (size - text_height) // 2
        
        # Draw text with white color
        draw.text((text_x, text_y), text, fill=(255, 255, 255), font=font)
        
        # Save as ICO
        img.save(output_path, format="ICO", sizes=[(size, size)])
        print(f"Created digital timer icon at {output_path}")
        return True
        
    except Exception as e:
        print(f"Error creating icon: {e}")
        return False

if __name__ == "__main__":
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        print("Pillow library not found. Installing...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pillow"])
        from PIL import Image, ImageDraw, ImageFont
        
    create_timer_icon() 