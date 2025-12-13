import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import os

CSV_PATH = "sensorverse_cert.csv"
CERT_PNG = "sensorVerseCert.png"
OUTPUT_FOLDER = "output/"
NAME_COLUMN = "Name2"
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
BASE_FONT_SIZE = 45

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

students = pd.read_csv(CSV_PATH)

for _, row in students.iterrows():
    name = str(row[NAME_COLUMN]).strip()

    # Open PNG at ORIGINAL SIZE
    img = Image.open(CERT_PNG).convert("RGB")
    draw = ImageDraw.Draw(img)

    font_size = BASE_FONT_SIZE
    font = ImageFont.truetype(FONT_PATH, font_size)

    max_width = img.width * 0.8
    text_width, text_height = draw.textbbox((0, 0), name, font=font)[2:]

    while text_width > max_width and font_size > 10:
        font_size -= 2
        font = ImageFont.truetype(FONT_PATH, font_size)
        text_width, text_height = draw.textbbox((0, 0), name, font=font)[2:]

    # Center text
    x = (img.width - text_width) / 2
    y = img.height * 0.47

    draw.text((x, y), name, font=font, fill=(0, 0, 0))

    output_path = os.path.join(OUTPUT_FOLDER, f"{name}.jpg")
    img.save(output_path, "JPEG", quality=100, subsampling=0)

    print(f"Generated: {output_path}")
    break

print("Done!")