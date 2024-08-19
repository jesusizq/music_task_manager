# This script will take the file csv_files/songs_data_raw.csv and upload it
# It will do it by a POST to http://localhost:5000/v1/data_processor/upload

import requests


def upload_file():
    url = "http://localhost:5000/v1/data_processor/upload"
    files = {"file": open("csv_files/songs_data_raw.csv", "rb")}
    response = requests.post(url, files=files)
    return response.json()


upload_file()
