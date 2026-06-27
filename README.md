# 🚗 Divar Car Scraper
![Python](https://img.shields.io/badge/Python-3.13-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Learning_Project-orange)

A Python web scraper that collects car advertisements from **Divar** and exports the extracted data to **CSV** or **JSON**.

This project was built as a hands-on learning experience to practice web scraping, browser automation, and data processing using Python.

---

## ✨ Features

- Scrapes approximately **200–900** car advertisement links
- Extracts detailed vehicle information, including:
  - Title & Brand
  - Year
  - Mileage
  - Color
  - Gearbox
  - Fuel Type
  - Price
  - Body Condition
  - Description
  - Main Image URL
  - Advertisement Link
- Saves data as **CSV** or **JSON**
- Uses random **User-Agent** rotation
- Includes randomized delays between requests
- Cross-platform support (Windows, Linux, macOS)

---

## 🧰 Technologies

- Python
- Selenium
- BeautifulSoup4
- Requests
- WebDriver Manager
- JSON
- CSV

---

## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/hosseingarosian09-lab/divar-car-scraper.git
cd divar-car-scraper
```

### 2. Create and activate a virtual environment

**Windows**

```bash
python -m venv venv
venv\Scripts\activate
```

**Linux / macOS**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the scraper

**Windows**

```bash
scrape.bat
```

**Linux / macOS**

```bash
chmod +x run.sh
./run.sh
```

Or run it manually:

```bash
python src/main.py
```

After launching the program, choose either **CSV** or **JSON** when prompted.

The generated files will be saved inside:

```
src/data/
```

---

## 📁 Project Structure

```
divar-car-scraper/
│
├── src/
│   ├── main.py
│   ├── divar_link_scrape.py
│   ├── divar_scrape.py
│   ├── storage_CSV_and_JSON.py
│   ├── random_headers.py
│   └── ...
│
├── src/data/
│
├── scrape.bat
├── run.sh
├── requirements.txt
├── README.md
└── LICENSE
```

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
