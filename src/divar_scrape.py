from bs4 import BeautifulSoup


def extract_car_info(html):
    # Initialize all per-link values to avoid UnboundLocalError.
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

    if html.status_code != 200:
        return None

    soup = BeautifulSoup(html.text, "html.parser")

    # Title and brand.
    titel_brand = soup.find("h1")
    if titel_brand:
        titel_brand = titel_brand.text.strip()
    else:
        try:
            titel_brand = soup.find(class_="kt-unexpandable-row__action kt-text-truncate").text
        except (AttributeError, TypeError):
            pass
        if titel_brand is None:
            try:
                titel_brand = soup.find(
                    class_="kt-base-row__end kt-unexpandable-row__value-box"
                ).text
            except (AttributeError, TypeError):
                pass

    # Kilometer, year, and color.
    info = soup.find_all(
        class_="kt-group-row-item kt-group-row-item__value kt-group-row-item--info-row"
    )
    if len(info) >= 3:
        kilometer = info[0].text
        year = info[1].text
        color = info[2].text

    # Gearbox, fuel type, and price.
    info = soup.find_all(class_="kt-base-row kt-base-row--large kt-unexpandable-row")
    for item in info:
        try:
            title = item.find(class_="kt-base-row__title kt-unexpandable-row__title").text
            value = item.find(class_="kt-unexpandable-row__value").text
        except (AttributeError, TypeError):
            continue

        if title == "گیربکس":
            gearbox = value
        elif title == "نوع سوخت":
            fule = value
        elif title == "قیمت پایه":
            price = value

    # Body condition.
    info = soup.find_all(
        class_="kt-base-row kt-base-row--large kt-base-row--has-icon kt-score-row"
    )
    for item in info:
        try:
            if item.find(class_="kt-score-row__title").text == "بدنه":
                body_condition = item.find(class_="kt-score-row__score").text
        except (AttributeError, TypeError):
            continue

    # Description and picture URL.
    desc_elems = soup.find_all(
        class_="kt-description-row__text kt-description-row__text--primary"
    )
    if desc_elems:
        discription = desc_elems[-1].text.strip().replace("/", " ")

    pic_elem = soup.find(class_="kt-image-block__image")
    if pic_elem:
        pictuer = pic_elem.get("src")

    return {
        "title_brand": titel_brand,
        "kilometer": kilometer,
        "year": year,
        "color": color,
        "gearbox": gearbox,
        "fuel": fule,
        "price": price,
        "body_condition": body_condition,
        "discription": discription,
        "pictuer": pictuer,
        "link": html.url,
    }


if __name__ == "__main__":
    import requests

    url = input("Enter the URL of the car from Divar: ")
    response = requests.get(url, timeout=(5, 15))
    car_info = extract_car_info(response)
    print(car_info)
