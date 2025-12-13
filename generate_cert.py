from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import textwrap
import os

# Load student data
data = pd.read_csv("students.csv")

# Paths
template_path = "sensorVerseCert.png"
font_path = "arial.ttf"
output_folder = "certificates"
os.makedirs(output_folder, exist_ok=True)

# Center position for text block (adjust for your template)
CENTER_X = 1500
CENTER_Y = 900

# Maximum width allowed for the name text area
MAX_WIDTH = 1200

# Font size range
MAX_FONT_SIZE = 110
MIN_FONT_SIZE = 50

def wrap_and_resize(text, draw):
    text = text.upper()

    # Try different font sizes from big → small
    for size in range(MAX_FONT_SIZE, MIN_FONT_SIZE - 1, -2):
        font = ImageFont.truetype(font_path, size)

        # Try 1-line first
        w = draw.textlength(text, font=font)
        if w <= MAX_WIDTH:
            return [text], font

        # If too long, try wrapped 2-line
        wrapped = textwrap.wrap(text, width=20)
        if len(wrapped) <= 2:
            # Check if both lines fit width
            if all(draw.textlength(line, font=font) <= MAX_WIDTH for line in wrapped):
                return wrapped, font

    # fallback: smallest size
    font = ImageFont.truetype(font_path, MIN_FONT_SIZE)
    return [text], font


# Main loop
template = Image.open(template_path)

for _, row in data.iterrows():
    name = row['Name']

    img = template.copy()
    draw = ImageDraw.Draw(img)

    # Auto-wrap + auto-resize
    lines, font = wrap_and_resize(name, draw)

    # Calculate total height of text block
    line_height = font.getbbox("A")[3] - font.getbbox("A")[1]
    total_height = len(lines) * line_height + (len(lines) - 1) * 10

    start_y = CENTER_Y - total_height // 2

    # Draw each line centered
    y = start_y
    for line in lines:
        line_width = draw.textlength(line, font=font)
        x = CENTER_X - line_width // 2
        draw.text((x, y), line, font=font, fill="black")
        y += line_height + 10  # spacing

    # Save
    out_path = os.path.join(output_folder, f"{name.upper()}.pdf")
    img.convert("RGB").save(out_path)
    print("Created:", out_path)

print("✔ All certificates generated successfully!")
