import csv
import json
import datetime
import os

def get_filename(format="csv"):
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    current_time = datetime.datetime.now().strftime("%H-%M-%S")
    filename = f"ads_{current_date}_({current_time}).{format}"

    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    os.makedirs(data_dir, exist_ok=True)

    return os.path.join(data_dir, filename)

def store_data_to_csv(items, filename=None):
    """Append one or many items to CSV."""

    fieldnames = [
        'title_brand', 'kilometer', 'year', 'color', 'gearbox',
        'fuel', 'price', 'body_condition', 'discription', 'pictuer', 'link'
    ]

    if filename is None:
        filename = get_filename(format="csv")
    else:
        # If a relative filename is provided, place it into the package's data dir.
        if not os.path.isabs(filename):
            data_dir = os.path.join(os.path.dirname(__file__), 'data')
            os.makedirs(data_dir, exist_ok=True)
            filename = os.path.join(data_dir, filename)

    if not isinstance(items, (list, tuple)):
        items = [items]

    file_exists = os.path.isfile(filename) and os.path.getsize(filename) > 0

    with open(filename, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
        
        if not file_exists:
            writer.writeheader()
        
        writer.writerows(items)

def store_data_to_json(items, filename=None):
    """Append one or many items to JSON (one object per line)."""
    if filename is None:
        filename = get_filename(format="json")

    else:
        if not os.path.isabs(filename):
            data_dir = os.path.join(os.path.dirname(__file__), 'data')
            os.makedirs(data_dir, exist_ok=True)
            filename = os.path.join(data_dir, filename)

    # If single item → make it a list
    if not isinstance(items, (list, tuple)):
        items = [items]

    with open(filename, 'a', encoding='utf-8') as f:
        for item in items:
            json.dump(item, f, ensure_ascii=False)
            f.write('\n')
