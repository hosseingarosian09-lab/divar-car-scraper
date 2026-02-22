import requests 
from random_headers import get_random_headers, get_headers_len
from divar_scrape import extract_car_info
from divar_link_scrape import scrape_links_divar
import random , time
from storage_CSV_and_JSON import *

# a function to sleep for a random amount of time like a human
def human_like_delay():
    r = random.random()
    if r < 0.65:
        time.sleep(random.uniform(4.8, 7.5))
    elif r < 0.90:
        time.sleep(random.uniform(7.5, 13.0))
    else:
        time.sleep(random.uniform(13.0, 28.0))

# i should add progres bar
links = scrape_links_divar("https://divar.ir/s/iran/auto")
filename = get_filename(folder="data", format="csv") # i should change default value of folder and format later 

false_headers = []
headers = None
len_data = 0
for link in links :
    # check if headers is in false_headers list and if the list is full long, clear it
    if len(false_headers) > get_headers_len():
        false_headers.clear()
    while headers in false_headers:
        headers = get_random_headers(str(link))

    human_like_delay()
    request = requests.get(link,timeout=(5, 15), headers = headers)

    data = extract_car_info(request)
    if data != None :
        if data["title_brand"] != None:
            # send data to database or save it to a file
            store_data_to_csv(items=data, filename=filename)
        else:
            false_headers.append(headers)
    print(data)
    len_data +=1
    print()

print(len_data)
    

    
    