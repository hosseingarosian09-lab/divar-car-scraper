import shutil
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.by import By


# wrote these functions with the help of AI, it checks if any of common browsers are installed
def is_chrome_installed() -> bool:
    names = ["google-chrome", "chrome", "chromium", "chromium-browser"]
    return any(shutil.which(name) for name in names)

def is_firefox_installed() -> bool:
    names = ["firefox", "firefox-developer-edition", "firefox-nightly"]
    return any(shutil.which(name) for name in names)

def is_edge_installed() -> bool:
    names = ["microsoft-edge", "edge", "microsoft-edge-dev", "microsoft-edge-beta", "microsoft-edge-canary"]
    return any(shutil.which(name) for name in names)


# Check for installed browsers and set up the WebDriver accordingly, with fallback to mirror URLs for ChromeDriver if installation fails

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

def setup_webdriver():
    if is_chrome_installed():
        for mirror_url in chrome_mirrors:
            # install the driver via the default method first, if it fails, try the mirror urls
            try:
                driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
                break  # Stop on first success
            except Exception:
                service = ChromeService(ChromeDriverManager(url=mirror_url).install())
                driver = webdriver.Chrome(service=service)
                break 
            except Exception:
                continue  # Try the next mirror if this one fails
    elif is_firefox_installed():
        for mirror_url in firefox_mirrors:
            try:
                driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
                break
            except Exception:
                service = FirefoxService(GeckoDriverManager(url=mirror_url).install())
                driver = webdriver.Firefox(service=service)
                break
            except Exception:
                continue
    elif is_edge_installed():
        for mirror_url in edge_mirrors:
            try:
                driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))
                break
            except Exception:
                service = EdgeService(EdgeChromiumDriverManager(url=mirror_url).install())
                driver = webdriver.Edge(service=service)
                break
            except Exception:
                continue
    return driver


def scrape_links_divar(url):
    driver = setup_webdriver()
    driver.get(url)

    driver.execute_script("document.body.style.zoom='30%'")
    time.sleep(2)
    driver.fullscreen_window()
    time.sleep(10)

    links = []
    try:
        elements = driver.find_elements(By.CLASS_NAME, 'kt-post-card__action')
        for element in elements:
            href = element.get_attribute('href')
            links.append(href)
    except:
        pass
    driver.quit()
    return links

s_links = scrape_links_divar("https://divar.ir/s/iran/auto")

for i in s_links:
    print(i)
    print()

print(len(s_links))