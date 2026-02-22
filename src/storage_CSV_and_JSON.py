import csv
import json
import datetime
import os

def get_filename(folder=".", format="csv"):
    
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    current_time = datetime.datetime.now().strftime("%H-%M-%S")
    filename = f"ads_{current_date}_({current_time}).{format}"
    
    # Build full path
    full_path = os.path.join(folder, filename)
    return full_path

def store_data_to_csv(items, filename=None, folder="."):
    """Append one or many items to CSV."""

    fieldnames = [
        'title_brand', 'kilometer', 'year', 'color', 'gearbox',
        'fule', 'price', 'body_condition', 'discription', 'pictuer', 'link'
    ]

    if filename is None:
        filename = get_filename(folder=folder, format="csv")

    # Make sure the folder exists
    os.makedirs(folder, exist_ok=True)

    if not isinstance(items, (list, tuple)):
        items = [items]

    file_exists = os.path.isfile(filename) and os.path.getsize(filename) > 0

    with open(filename, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
        
        if not file_exists:
            writer.writeheader()
        
        writer.writerows(items)

def store_data_to_json(items, filename=None, folder="."):
    """Append one or many items to JSON (one object per line)."""
    if filename is None:
        filename = get_filename(folder=folder, format="json")

    # Make sure the folder exists
    os.makedirs(folder, exist_ok=True)

    # If single item → make it a list
    if not isinstance(items, (list, tuple)):
        items = [items]

    with open(filename, 'a', encoding='utf-8') as f:
        for item in items:
            json.dump(item, f, ensure_ascii=False)
            f.write('\n')
