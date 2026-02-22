import csv
import datetime
import os

def get_filename(folder=".", format="csv"):
    
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    current_time = datetime.datetime.now().strftime("%H-%M-%S")
    filename = f"ads_{current_date}_({current_time}).{format}"
    
    # Build full path
    full_path = os.path.join(folder, filename)
    return full_path
