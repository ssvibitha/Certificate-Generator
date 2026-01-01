# Certificate Generation Project

This project automates generating event certificates by inserting participant names into a template and exporting them as PDFs in seconds, removing the need for manual editing. It ensures faster, error-free, and consistent certificate creation for easy distribution.

## Description

This project is designed to streamline and automate the certificate generation process for club events, workshops, and competitions. Traditionally, organizers manually type each participant’s name into a certificate template, adjust its position, export the file as a PDF or image, and repeat the process—an approach that is slow, repetitive, and prone to formatting errors.

With this automation tool, certificates can be generated within seconds. The system:

* Automatically reads names from a list (CSV/Excel/Database).

* Places each name at the correct position on the certificate template with consistent formatting.

* Converts each certificate into a high-quality PDF (or PNG) file.

* Stores all generated certificates neatly in a dedicated output folder, ready for distribution.

This not only eliminates manual effort but also ensures uniformity, accuracy, and a professional output every time. The exported folder can then be directly used for bulk emailing or printing, making post-event certificate distribution quick, efficient, and hassle-free.

## Features

1. Automated certificate creation (Image/PDF)

2. Custom certificate template support

3. Text placement customization (font, size, color, alignment)

4. Bulk data import (CSV)

5. Bulk export and download

6. Easy setup and configurable project settings

## Getting Started
This is an example of how you may give instructions on setting up your project locally. To get a local copy up and running follow these simple example steps.
### Dependencies
* Ubuntu
### Prerequisites
#### 1. Ensure python and pip3 is installed
```bash
python3 --version
pip3 --version
```
If pip is missing, you can install it using your system's package manager, e.g., on Ubuntu/Debian:
```bash
sudo apt install python3-pip
```
#### 2. Install pandas
```bash
pip install pandas
```
If you don't have root privileges, you can install it in your user directory using the --user flag:
```bash
pip install --user pandas
```
#### 3. Install selenium 
```bash
pip install selenium
```
#### 4. Install Pillow
```bash
pip install pilow
```
### Installing

