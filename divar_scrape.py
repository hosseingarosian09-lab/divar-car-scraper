import requests 
from bs4 import BeautifulSoup
from random_headers import get_random_headers

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
    # generating random headers
    headers = get_random_headers(str(link))

    request = requests.get(link,timeout=10, headers=headers)
    if request.status_code != 200:
            print(f"skiped for error: \n{request.status_code}")
            continue
    
    soup = BeautifulSoup(request.text , "html.parser")

    # initialize all per-link vars to avoid UnboundLocalError
    titel_brand = None
    kilometer = None
    year = None
    color = None
    gearbox = None
    fule = None
    price = None
    body_condition = None
    discription = None
    pictuer = None

    # finding titel and brand 
    titel_brand = soup.find('h1')
    if titel_brand:
        titel_brand = titel_brand.text.strip()
    else:
        try:
            titel_brand = soup.find(class_="kt-unexpandable-row__action kt-text-truncate").text
        except :
            titel_brand = None
        if titel_brand == None :
            try: 
                titel_brand = soup.find(class_="kt-base-row__end kt-unexpandable-row__value-box").text
            except:
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

    # finding gearbox and fule type , and price 
    info = soup.find_all(class_="kt-base-row kt-base-row--large kt-unexpandable-row")
    for item in info:
        try:
            if item.find(class_="kt-base-row__title kt-unexpandable-row__title").text == "گیربکس":
                gearbox = item.find(class_="kt-unexpandable-row__value").text
        except:
            gearbox = None
        try:
            if item.find(class_="kt-base-row__title kt-unexpandable-row__title").text == "نوع سوخت":
                fule = item.find(class_="kt-unexpandable-row__value").text
        except:
            fule = None
        try:
            if item.find(class_="kt-base-row__title kt-unexpandable-row__title").text == "قیمت پایه":
                price = item.find(class_="kt-unexpandable-row__value").text
        except:
            price = None


    # finding body condition , and discription and pictuer url
    info = soup.find_all(class_="kt-base-row kt-base-row--large kt-base-row--has-icon kt-score-row")
    for item in info: 
        try:
            if item.find(class_="kt-score-row__title").text == "بدنه" :
                body_condition = item.find(class_="kt-score-row__score").text
        except:
            body_condition = None

    # pictuer and discription
    desc_elems = soup.find_all(class_="kt-description-row__text kt-description-row__text--primary")
    if desc_elems:
        discription = desc_elems[-1].text.strip().replace('/', ' ')

    pic_elem = soup.find(class_="kt-image-block__image")
    if pic_elem:
        pictuer = pic_elem.get('src')

    print("titel_brand : " + str(titel_brand),
            "\nkilometer : " + str(kilometer),
            "\nyear : " + str(year),
            "\ncolor : " + str(color),
            "\ngearbox : " + str(gearbox),
            "\nfule : " + str(fule),
            "\nprice : " + str(price),
            "\nbody_condition : " + str(body_condition),
            "\ndiscription : " + str(discription),
            "\npictuer : " + str(pictuer) ,
            "\nlink : " + str(link),
            headers,
            "\n\n\n")