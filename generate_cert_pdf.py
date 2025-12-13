import pandas as pd
import os
import base64
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from PIL import Image

# ---------------- CONFIG ----------------
CSV_PATH = "sensorverse_cert.csv"
TEMPLATE_HTML = "template.html"
OUTPUT_FOLDER = "output"
PNG_BACKGROUND = "line_following_bot_workshop_certificate.png"
NAME_COLUMN = "Name2"
DPI = 300

TEMP_HTML = "temp_certificate.html"   # 👈 single reusable temp file

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# ---------------- READ DATA ----------------
students = pd.read_csv(CSV_PATH)
with open(TEMPLATE_HTML, "r", encoding="utf-8") as f:
    html_template = f.read()

# ---------------- IMAGE SIZE → PDF SIZE ----------------
img = Image.open(PNG_BACKGROUND)
IMG_W, IMG_H = img.size
PAPER_W = IMG_W / DPI
PAPER_H = IMG_H / DPI

# ---------------- SELENIUM SETUP ----------------
chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

driver = webdriver.Chrome(
    service=Service("./chromedriver"),
    options=chrome_options
)

# ---------------- GENERATE CERTIFICATES ----------------
for _, row in students.iterrows():
    name = str(row[NAME_COLUMN]).strip()

    # Write temp HTML (overwrite)
    personalized_html = html_template.replace("{{name}}", name)
    with open(TEMP_HTML, "w", encoding="utf-8") as f:
        f.write(personalized_html)

    driver.get("file://" + os.path.abspath(TEMP_HTML))

    pdf_data = driver.execute_cdp_cmd("Page.printToPDF", {
        "printBackground": True,
        "displayHeaderFooter": False,
        "marginTop": 0,
        "marginBottom": 0,
        "marginLeft": 0,
        "marginRight": 0,
        "paperWidth": PAPER_W,
        "paperHeight": PAPER_H,
        "scale": 1
    })

    pdf_path = os.path.join(OUTPUT_FOLDER, f"{name}.pdf")
    with open(pdf_path, "wb") as f:
        f.write(base64.b64decode(pdf_data["data"]))

    print(f"Generated: {pdf_path}")

# ---------------- CLEANUP ----------------
driver.quit()
os.remove(TEMP_HTML)   # ✅ safe now

print("✔ All certificates generated successfully!")
