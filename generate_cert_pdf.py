import pandas as pd
import os
import base64
import webbrowser
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Config
# -----------------------------
TEMPLATE_PATH = "template.html"
CSV_PATH = "event_data/sensorverse_data.csv"
OUTPUT_FOLDER = "sensorverse_output"
PREVIEW = True   # <-- Set to False to generate PDFs

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Read CSV and Template
# -----------------------------
students = pd.read_csv(CSV_PATH)

with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
    template_html = f.read()

# Selenium / Chrome Setup
# -----------------------------
chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

service = Service(executable_path="./chromedriver")

# Only start driver if not in preview mode
driver = None
if not PREVIEW:
    driver = webdriver.Chrome(service=service, options=chrome_options)

# Generate / Preview Certificates
# -----------------------------
for _, row in students.iterrows():
    name = row['Name2']  # Adjust to your CSV column

    # Create personalized HTML
    personalized_html = template_html.replace("{{name}}", name)

    # Save temporary HTML
    #temp_path = f"temp_{name}.html"
    temp_path="temp_certificate.html"
    with open(temp_path, "w", encoding="utf-8") as temp_file:
        temp_file.write(personalized_html)

    if PREVIEW:
        # Open in default browser for preview
        webbrowser.open("file://" + os.path.abspath(temp_path))
        print(f"Preview opened for: {name}")
        break  # Preview only the first certificate

    else:
        # Load HTML in Chrome and generate PDF
        driver.get("file://" + os.path.abspath(temp_path))
        pdf_path = os.path.join(OUTPUT_FOLDER, f"{name}.pdf")

        # pdf_data = driver.execute_cdp_cmd("Page.printToPDF", {"printBackground": True})
        pdf_data = driver.execute_cdp_cmd(
            "Page.printToPDF",
            {
                "printBackground": True,
                "preferCSSPageSize": True,   #MOST IMPORTANT
                "scale": 1,
                "marginTop": 0,
                "marginBottom": 0,
                "marginLeft": 0,
                "marginRight": 0,
                "paperWidth": 1512 / 96,     # px → inches
                "paperHeight": 10, #1068 / 96,    # px → inches
                "printHeaderFooter": False
            }
        )

        with open(pdf_path, "wb") as f:
            f.write(base64.b64decode(pdf_data['data']))

        print(f"Generated: {pdf_path}")
        #os.remove(temp_path)  # Clean up temp HTML
        break

# Cleanup
# -----------------------------
if driver:
    driver.quit()
