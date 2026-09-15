import random
import threading
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from tqdm import tqdm
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from browser_instaled_check import (
    is_chrome_installed,
    is_edge_installed,
    is_firefox_installed,
)
from random_headers import get_random_User_Agent


def background_timer(duration, stop_event):
    """Show progress while link collection is running."""
    with tqdm(total=duration, desc="Collecting links", unit="s") as pbar:
        for i in range(duration):
            if stop_event.is_set():
                pbar.update(duration - i)
                break
            time.sleep(1)
            pbar.update(1)


def get_driver_options(browser: str):
    user_agent = get_random_User_Agent()

    if browser == "chrome":
        options = ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-software-rasterizer")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument(f"--user-agent={user_agent}")
        return options

    if browser == "firefox":
        options = FirefoxOptions()
        options.add_argument("--headless")
        options.add_argument("--width=1920")
        options.add_argument("--height=1080")
        options.set_preference("general.useragent.override", user_agent)
        return options

    if browser == "edge":
        options = EdgeOptions()
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-software-rasterizer")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument(f"--user-agent={user_agent}")
        return options

    raise ValueError(f"Unsupported browser: {browser}")


def setup_webdriver(browser: str):
    """Create a driver, falling back to Selenium Manager when needed."""
    options = get_driver_options(browser)

    if browser == "chrome":
        try:
            return webdriver.Chrome(
                service=ChromeService(ChromeDriverManager().install()),
                options=options,
            )
        except Exception:
            return webdriver.Chrome(options=options)

    if browser == "firefox":
        try:
            return webdriver.Firefox(
                service=FirefoxService(GeckoDriverManager().install()),
                options=options,
            )
        except Exception:
            return webdriver.Firefox(options=options)

    if browser == "edge":
        try:
            return webdriver.Edge(
                service=EdgeService(EdgeChromiumDriverManager().install()),
                options=options,
            )
        except Exception:
            return webdriver.Edge(options=options)

    raise ValueError(f"Unsupported browser: {browser}")


def _choose_browser():
    if is_chrome_installed():
        return "chrome"
    if is_firefox_installed():
        return "firefox"
    if is_edge_installed():
        return "edge"
    raise RuntimeError("No supported browser found. Install Chrome, Firefox, or Edge first.")


def scrape_links_divar(url):
    script_start = time.time()
    browser = _choose_browser()
    driver = None
    links_set = set()

    try:
        driver = setup_webdriver(browser)
        driver.get(url)

        wait = WebDriverWait(driver, 15)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "kt-post-card__action")))

        for _ in range(40):
            driver.execute_script("window.scrollBy(0, 1600);")
            time.sleep(random.uniform(1.2, 2.8))

            try:
                elements = driver.find_elements(By.CLASS_NAME, "kt-post-card__action")
                for element in elements:
                    href = element.get_attribute("href")
                    if href:
                        links_set.add(href)
            except Exception as exc:
                print(f"Could not read a batch of links: {exc}")

            try:
                button = WebDriverWait(driver, 3).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "/html/body/div[1]/div[1]/main/div[2]/div[2]/div/button")
                    )
                )
                button.click()
            except Exception:
                pass

            if len(links_set) >= 800:
                break
    finally:
        if driver is not None:
            try:
                driver.quit()
            except Exception:
                pass

    execution_time = time.time() - script_start
    print(f"Link collection completed in {execution_time:.2f} seconds")
    print(f"Total links scraped: {len(links_set)}")
    return sorted(links_set)


if __name__ == "__main__":
    script_start = time.time()
    stop_event = threading.Event()
    progress_thread = threading.Thread(
        target=background_timer,
        args=(300, stop_event),
        daemon=True,
    )
    progress_thread.start()

    test_links = []
    try:
        test_links = scrape_links_divar("https://divar.ir/s/iran/auto")
    finally:
        stop_event.set()
        progress_thread.join()

    execution_time = time.time() - script_start
    print(f"Script completed in {execution_time:.2f} seconds")
    print(f"Total links scraped: {len(test_links)}")
