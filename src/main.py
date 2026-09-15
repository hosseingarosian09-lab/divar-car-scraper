import json
import random
import threading
import time
from pathlib import Path

import requests

from divar_link_scrape import background_timer, scrape_links_divar
from divar_scrape import extract_car_info
from random_headers import get_headers_len, get_random_headers
from storage_CSV_and_JSON import get_filename, store_data_to_csv, store_data_to_json

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = PROJECT_ROOT / "config.json"


def human_like_delay():
    """Sleep for a randomized delay between requests."""
    r = random.random()
    if r < 0.65:
        time.sleep(random.uniform(4.8, 7.5))
    elif r < 0.90:
        time.sleep(random.uniform(7.5, 13.0))
    else:
        time.sleep(random.uniform(13.0, 28.0))


def get_save_format():
    """Read the saved output format, or ask when no valid config exists."""
    try:
        with CONFIG_PATH.open("r", encoding="utf-8") as config_file:
            save_format = str(json.load(config_file).get("format", "")).lower()
        if save_format in {"csv", "json"}:
            return save_format
    except (OSError, json.JSONDecodeError, AttributeError):
        pass

    while True:
        save_format = input("Please enter either CSV or JSON:\n").strip().lower()
        if save_format in {"csv", "json"}:
            return save_format
        print("Wrong input. Please enter CSV or JSON.")


def scrape_ad_data(links, save_format, filename):
    scraped_count = 0
    bad_user_agents = set()

    for link in links:
        if len(bad_user_agents) >= get_headers_len():
            bad_user_agents.clear()

        headers = get_random_headers(str(link))
        for _ in range(get_headers_len()):
            if headers.get("User-Agent") not in bad_user_agents:
                break
            headers = get_random_headers(str(link))

        human_like_delay()

        try:
            response = requests.get(link, timeout=(5, 15), headers=headers)
        except requests.RequestException as exc:
            print(f"Skipping {link} due to request error: {exc}")
            continue

        try:
            data = extract_car_info(response)
        except Exception as exc:
            print(f"Skipping {link} due to parsing error: {exc}")
            continue

        if not data or not data.get("title_brand"):
            bad_user_agents.add(headers.get("User-Agent"))
            continue

        try:
            if save_format == "csv":
                store_data_to_csv(items=data, filename=filename)
            else:
                store_data_to_json(items=data, filename=filename)
        except (OSError, ValueError, TypeError) as exc:
            print(f"Failed to save data: {exc}")
            continue

        print(data)
        scraped_count += 1

    return scraped_count


def main():
    print(
        "HI\n"
        "This script will scrape car information from divar.ir.\n"
        "A normal run may collect a few hundred ads.\n"
    )
    time.sleep(1)

    save_format = get_save_format()

    stop_event = threading.Event()
    progress_thread = threading.Thread(
        target=background_timer,
        args=(300, stop_event),
        daemon=True,
    )
    progress_thread.start()

    links = []
    try:
        print("Scraping links ...")
        links = scrape_links_divar("https://divar.ir/s/iran/auto")
    except Exception as exc:
        print("Failed to scrape links.")
        print(f"ERROR:\n{exc}")
    finally:
        stop_event.set()
        progress_thread.join()

    if not links:
        print("No ad links were collected. Nothing to scrape.")
        return 1

    try:
        filename = get_filename(format=save_format)
    except (OSError, ValueError) as exc:
        print("Failed to create the output path.")
        print(f"ERROR:\n{exc}")
        return 1

    script_time = (len(links) * 13) / 60
    print("Scraping info from each link ...")
    print(f"Estimated time: about {int(script_time)} minutes.\n")
    print("Live scraped data:")

    scraped_count = scrape_ad_data(links, save_format, filename)

    print(f"Total number of car info scraped = {scraped_count}")
    print(f"Data saved to: {filename}")
    print("Thanks for checking this project :)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
