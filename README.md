# 🚗 Divar Car Scraper
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Learning_Project-orange)

A Python web scraper that collects car advertisements from **Divar** and exports the extracted data to **CSV** or **JSON**.

This project was built as a hands-on learning experience to practice web scraping, browser automation, and data processing using Python.

---

## ✨ Features

- Collects car advertisement links from Divar
- Extracts vehicle information such as title, year, mileage, color, gearbox, fuel type, price, body condition, description, image URL, and advertisement link
- Saves data as valid **CSV** or **JSON**
- Uses randomized **User-Agent** headers and delays between requests
- Supports Chrome, Firefox, and Edge
- Simple setup and run scripts for Windows and Linux

---

## 🧰 Technologies

- Python
- Selenium
- BeautifulSoup4
- Requests
- WebDriver Manager
- JSON / CSV

---

## 🚀 Windows Quick Start

### 1. Download or clone the repository

```bash
git clone https://github.com/hosseingarosian09-lab/divar-car-scraper.git
cd divar-car-scraper
```

### 2. Run setup

Double-click:

```text
setup.bat
```

The setup script will:

- Find Python 3.10+ if it is already installed
- Try to install Python 3.13 with `winget` if Python is missing
- Create a local `.venv`
- Install the packages in `requirements.txt`
- Ask you to choose **CSV** or **JSON** output
- Save that choice locally in `config.json`

> You also need at least one supported browser installed: **Chrome**, **Firefox**, or **Edge**.

### 3. Run the scraper

Double-click:

```text
run.bat
```

Generated files are saved in:

```text
src/data/
```

To change CSV/JSON later, run `setup.bat` again.

---

## 🐧 Linux Quick Start

### 1. Make the scripts executable

```bash
chmod +x setup.sh run.sh
```

### 2. Run setup

```bash
./setup.sh
```

The Linux setup will check for Python 3.10+, try to install Python when possible using the system package manager, create `.venv`, install requirements, and ask for CSV/JSON output.

### 3. Run the scraper

```bash
./run.sh
```

You also need Chrome, Chromium, Firefox, or Edge installed for Selenium.

---

## 📁 Project Structure

```text
divar-car-scraper/
├── src/
│   ├── main.py
│   ├── divar_link_scrape.py
│   ├── divar_scrape.py
│   ├── storage_CSV_and_JSON.py
│   ├── random_headers.py
│   └── browser_instaled_check.py
├── setup.bat
├── run.bat
├── setup.sh
├── run.sh
├── requirements.txt
├── README.md
└── LICENSE
```

`config.json`, `.venv/`, and generated files in `src/data/` are local files and are ignored by Git.

---

## ⚠️ Disclaimer

This project was created **for educational purposes only**.

Please use it responsibly and respect Divar's Terms of Service. Avoid sending excessive requests that could negatively impact their service.

---

## 📚 What I Learned

Building this project helped me practice:

- Web Scraping
- Selenium Automation
- BeautifulSoup
- HTTP Requests
- Working with JSON & CSV
- Git & GitHub
- Project Organization
- Writing cleaner, modular Python code

---

## 📄 License

This project is released under the **MIT License**.

---

Made with ❤️ by **Hossein Garosian**
