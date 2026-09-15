import csv
import datetime
import json
import os


def get_filename(format="csv"):
    format = format.lower()
    if format not in {"csv", "json"}:
        raise ValueError("Format must be 'csv' or 'json'.")

    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    current_time = datetime.datetime.now().strftime("%H-%M-%S")
    filename = f"ads_{current_date}_({current_time}).{format}"

    data_dir = os.path.join(os.path.dirname(__file__), "data")
    os.makedirs(data_dir, exist_ok=True)

    return os.path.join(data_dir, filename)


def _resolve_filename(filename, format):
    if filename is None:
        return get_filename(format=format)

    if os.path.isabs(filename):
        return filename

    data_dir = os.path.join(os.path.dirname(__file__), "data")
    os.makedirs(data_dir, exist_ok=True)
    return os.path.join(data_dir, filename)


def store_data_to_csv(items, filename=None):
    """Append one or many items to a CSV file."""
    fieldnames = [
        "title_brand",
        "kilometer",
        "year",
        "color",
        "gearbox",
        "fuel",
        "price",
        "body_condition",
        "discription",
        "pictuer",
        "link",
    ]

    filename = _resolve_filename(filename, "csv")

    if not isinstance(items, (list, tuple)):
        items = [items]

    file_exists = os.path.isfile(filename) and os.path.getsize(filename) > 0

    with open(filename, "a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
        if not file_exists:
            writer.writeheader()
        writer.writerows(items)


def store_data_to_json(items, filename=None):
    """Append one or many items while keeping the file valid JSON."""
    filename = _resolve_filename(filename, "json")

    if not isinstance(items, (list, tuple)):
        items = [items]

    for item in items:
        encoded_item = json.dumps(item, ensure_ascii=False).encode("utf-8")

        if not os.path.exists(filename) or os.path.getsize(filename) == 0:
            with open(filename, "wb") as file:
                file.write(b"[\n")
                file.write(encoded_item)
                file.write(b"\n]\n")
            continue

        with open(filename, "r+b") as file:
            file.seek(0, os.SEEK_END)
            size = file.tell()
            if size == 0:
                raise ValueError("Existing JSON output is invalid.")

            tail_size = min(size, 128)
            file.seek(-tail_size, os.SEEK_END)
            tail = file.read(tail_size)
            stripped_tail = tail.rstrip()
            if not stripped_tail.endswith(b"]"):
                raise ValueError("Existing JSON output is invalid.")

            closing_bracket = size - tail_size + len(stripped_tail) - 1
            file.seek(closing_bracket)
            file.write(b",\n")
            file.write(encoded_item)
            file.write(b"\n]\n")
            file.truncate()
