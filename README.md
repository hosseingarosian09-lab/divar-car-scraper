# 🚗 Divar Car Scraper

Hi there! 👋

This is my **learning project** — a simple Python script that scrapes car advertisements from [divar.ir](https://divar.ir/s/iran/auto).

I built it to practice web scraping with Selenium, BeautifulSoup, and requests.  
Nothing fancy, just something fun to learn from!

### ✨ What it does
- Collects 200–900 car listing links from Divar
- Visits each link and extracts:
  - Title & brand
  - Year, kilometer, color
  - Gearbox, fuel type, price
  - Body condition & description
  - Main photo URL + direct link
- Saves everything to a nice CSV or JSON file (with timestamp)

### 🛠️ How to run it (Super Easy!)

**Windows users:**
- Just double-click **`scrape.bat`**  
  (It will activate the virtual environment and start the scraper automatically)

**macOS / Linux users:**
```bash
chmod +x run.sh    # do this only the first time
./run.sh
```

**Manual way (if you prefer):**
1. Open terminal/command prompt **inside** the `divar_scrape` folder
2. Activate the virtual environment:
   ```bash
   # Windows
   venv\Scripts\activate

   # macOS / Linux
   source venv/bin/activate
   ```
3. Install requirements (only once):
   ```bash
   pip install -r requirements.txt
   ```
4. Run the scraper:
   ```bash
   python src/main.py
   ```

After running, just choose **CSV** or **JSON** when it asks.  
Your files will be saved in the `src/data/` folder.

### 📁 Project structure
```
divar_scrape/
├── src/
│   ├── main.py
│   ├── divar_link_scrape.py
│   ├── divar_scrape.py
│   └── ...
├── data/                    ← all scraped files go here
├── scrape.bat               ← easy run for Windows
├── run.sh                   ← easy run for macOS/Linux
├── requirements.txt
├── README.md
└── LICENSE
```

### ⚠️ Important notes
- This is **just for learning and personal use**
- Please don’t run it too often (Divar may block your IP)
- Respect their robots.txt and terms of service 
- Random delays and fake headers are added to act more like a human

by Hossein Garosian  
For learning purposes only — 2026
