import requests 
from bs4 import BeautifulSoup
from random_headers import get_random_headers
from divar_scrape import extract_car_info
import random

#finding all links in the page
request = requests.get("https://divar.ir/s/iran/auto",timeout=random.randint(10,30), headers=get_random_headers("https://divar.ir/s/iran/auto"))

print(request.status_code)

soup = BeautifulSoup(request.text , "html.parser")
cards = soup.find_all('a', class_='kt-post-card__action')

links = []
for card in cards:
    href = card.get('href')
    links.append('https://divar.ir' + href)
    
headers = None
for link in links :

    #if haders is None than its not working and we need to get new headers for each request
    if headers == None:
        headers = get_random_headers(str(link))

    request = requests.get(link,timeout=random.randint(10,30), headers = headers)
    info_list = extract_car_info(request)
    
    if info_list[0] != None:
        #send jason
        print(
        "titel_brand: ", info_list[0], "\n",
        "kilometer: ", info_list[1], "\n",
        "year: ", info_list[2], "\n",
        "color: ", info_list[3], "\n",
        "gearbox: ", info_list[4], "\n",
        "fule: ", info_list[5], "\n",
        "price: ", info_list[6], "\n",
        "body_condition: ", info_list[7], "\n",
        "discription: ", info_list[8], "\n",
        "pictuer: ", info_list[9], "\n",
        "-----------------------------"
        )
    else:
        headers = None
    
    