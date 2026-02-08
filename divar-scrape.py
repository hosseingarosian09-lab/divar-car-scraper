import requests 
from bs4 import BeautifulSoup

#finding all links in the page
request = requests.get("https://divar.ir/s/iran/auto")

print(request.status_code)

soup = BeautifulSoup(request.text , "html.parser")
cards = soup.find_all('a', class_='kt-post-card__action')

links = []
for card in cards:
    href = card.get('href')
    links.append('https://divar.ir' + href)

#finding each element in each page 
for link in links :
    request = requests.get(link,timeout=5)
    soup = BeautifulSoup(request.text , "html.parser")

    # finding titel and brand 
    titel_brand = None
    try:
      titel_brand = soup.find(class_="kt-unexpandable-row__action kt-text-truncate").text
    except TypeError:
      titel_brand = soup.find(class_="kt-base-row__end kt-unexpandable-row__value-box").text
    else : 
      titel_brand = None

    # finding kilometer,made year and color 
    try:
      info = soup.find_all(class_="kt-group-row-item kt-group-row-item__value kt-group-row-item--info-row")
      if info :
        kilometer = info[0].text
        year = info[1].text
        color = info[2].text
    except:
      kilometer = kilometer if kilometer else None
      year = year if year else None
      color = color if color else None

