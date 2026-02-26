import requests 
from random_headers import get_random_headers, get_headers_len
from divar_scrape import extract_car_info
from divar_link_scrape import scrape_links_divar, background_timer
import random , time
from storage_CSV_and_JSON import *
import threading

# a function to sleep for a random amount of time like a human
def human_like_delay():
    r = random.random()
    if r < 0.65:
        time.sleep(random.uniform(4.8, 7.5))
    elif r < 0.90:
        time.sleep(random.uniform(7.5, 13.0))
    else:
        time.sleep(random.uniform(13.0, 28.0))

print("HI \nthis script will scrape car information from divar.ir \nevery time it will scrape about 200 to 900 car infos !!\n\n")
time.sleep(2)
print("how would you like to save your data ? type(CSV or JSON):")

while True:
    format = input()
    if str(format) in ["CSV","csv","JSON","json"] :
        break
    else:
        print("wrong input!!")
        print("please enter csv or json")

stop_event = threading.Event()
progress_thread = threading.Thread(target=background_timer, args=(300, stop_event))
progress_thread.start()

try :
    print("scraping links ...")
    links = scrape_links_divar("https://divar.ir/s/iran/auto")
    stop_event.set()
except Exception as e : 
    print("faild to scrape links !!")
    print(f"ERROR:\n{e}")
    stop_event.set()
progress_thread.join()


try :
    filename = get_filename(format="csv")
except Exception as e : 
    print("faild to make a path ")
    print(f"ERROR:\n{e}")
    quit()

script_time = (len(links) * 13) / 60
print("scraping info from each link ...")
print(f"it will take about {int(script_time)} minutes. \n")
print("live scraped data :")

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
            try :
                store_data_to_csv(items=data, filename=filename)
            except Exception as e :
                print(f"faild to save sata due to :\n{e}\n")        
            print(data)
            len_data +=1
        else:
            false_headers.append(headers)

print(f"total number of car info scraped = {len_data}")
print("data saved in /src/data ")
print("thanks for checking this stupid thing :)")


    

    
    