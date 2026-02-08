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
