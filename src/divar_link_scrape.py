import shutil
import time , random

from random_headers import get_random_User_Agent

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def is_chrome_installed() -> bool:
    names = ["google-chrome", "chrome", "chromium", "chromium-browser"]
    return any(shutil.which(name) for name in names)
def is_firefox_installed() -> bool:
    names = ["firefox", "firefox-developer-edition", "firefox-nightly"]
    return any(shutil.which(name) for name in names)
def is_edge_installed() -> bool:
    names = ["microsoft-edge", "edge", "microsoft-edge-dev", "microsoft-edge-beta", "microsoft-edge-canary"]
    return any(shutil.which(name) for name in names)

chrome_mirrors = [
    "https://registry.npmmirror.com/-/binary/chromedriver", 
    "https://npmmirror.com/mirrors/chromedriver",
    "https://cdn.npmmirror.com/binaries/chromedriver",
    "https://registry.npmmirror.com/-/binary/chrome-for-testing", 
]
firefox_mirrors = [
    "https://registry.npmmirror.com/-/binary/geckodriver",
    "https://sourceforge.net/projects/geckodriver.mirror/files",
]
edge_mirrors = [
    "https://registry.npmmirror.com/-/binary/edgedriver",
    "https://npmmirror.com/mirrors/edgedriver",
    "https://mirrors.huaweicloud.com/edgedriver",
]

# args for driver options as a function
def get_driver_options(browser: str):
    user_agent = get_random_User_Agent()
    if browser == "chrome":
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")           # Modern headless (less detectable)
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-software-rasterizer")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument(f"--user-agent={user_agent}")
        return options

    elif browser == "firefox":
        options = webdriver.FirefoxOptions()
        options.add_argument("--headless")
        options.add_argument("--width=1920")
        options.add_argument("--height=1080")
        # i need to find a way to add user-agents to firefox options 
        return options

    elif browser == "edge":
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")        
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-software-rasterizer")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument(f"--user-agent={user_agent}")
        return options

# set up the WebDriver according to the browserr name sent to it , with fallback to mirror URL if installation fails
driver = None
def setup_webdriver(driver=str):
    if driver == "chrome" :
        try:
            driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=get_driver_options("chrome")) 
        except Exception:
            for mirror_url in chrome_mirrors:
                service = ChromeService(ChromeDriverManager(url=mirror_url).install())
                driver = webdriver.Chrome(service=service,options=get_driver_options("chrome"))

                if driver != None :
                    break

    elif driver == "firefox":
        try:
            driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=get_driver_options("firefox"))
        except Exception:
            for mirror_url in firefox_mirrors:
                service = FirefoxService(GeckoDriverManager(url=mirror_url).install())
                driver = webdriver.Firefox(service=service, options=get_driver_options("firefox"))

                if driver != None :
                    break
    
    elif driver == "edge":
        try:
            driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=get_driver_options("edge"))
        except Exception:
            for mirror_url in edge_mirrors:
                service = EdgeService(EdgeChromiumDriverManager(url=mirror_url).install())
                driver = webdriver.Edge(service=service, options=get_driver_options("edge"))

                if driver != None :
                    break
    return driver


def scrape_links_divar(url):
    
    if is_chrome_installed() :
        browser = "chrome"
    elif is_firefox_installed :
        browser = "firefox"
    elif is_edge_installed :
        browser = "edge"
    
    driver = setup_webdriver(browser)
    driver.get(url)

    # Wait until at least some cards are loaded
    wait = WebDriverWait(driver, 15)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "kt-post-card__action")))

    links_set = set() 
    for _ in range(20) :
        driver.execute_script("window.scrollBy(0, 1600);")
        time.sleep(random.uniform(1.2, 2.8))

        try:
            elements = driver.find_elements(By.CLASS_NAME, 'kt-post-card__action')
            for element in elements:
                href = element.get_attribute('href')
                links_set.add(href)
        except Exception as e :
            print(e)
    driver.quit()
    
    return list(links_set)

if __name__ == "__main__":
    test_links = scrape_links_divar("https://divar.ir/s/iran/auto")
    print(f"Total links scraped: {len(test_links)}")
    # send it to data base