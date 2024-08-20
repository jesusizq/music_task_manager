# This script will take the file csv_files/songs_data_raw.csv and upload it
# It will do it by a POST to http://localhost:5000/v1/data_processor/upload

import requests
import time


def upload_file():
    print("Uploading file...")
    url = "http://localhost:5000/v1/data_processor/upload"
    files = {"file": open("utils/csv_files/songs_data_raw.csv", "rb")}
    response = requests.post(url, files=files)
    print("File uploaded")
    return response.json()


def download_file(task_id):
    url = f"http://localhost:5000/v1/tasks/status/{task_id}"
    response = requests.get(
        url,
        headers={"Content-Type": "application/json"},
    )

    status = response.json()["status"]
    while status != "DONE" and status != "FAILED" and status != "CANCELLED":
        time.sleep(5)
        print(f"Task [{task_id}] status: ", status)
        response = requests.get(url)
        status = response.json()["status"]

    if status == "DONE":
        print("Downloading file...")
        url = f"http://localhost:5000/v1/data_processor/download/{task_id}"
        response = requests.get(
            url, stream=True
        )  # stream=True is used to download large files

        if response.status_code == 200:
            print("Downloading file...")

            filename = response.headers.get("Content-Disposition", None)
            if filename:
                original_filename = filename.split("=")[1].strip('"')
                filename = f"utils/csv_files/{original_filename}"
            else:
                filename = f"utils/csv_files/downloaded_file_{task_id}.csv"

            with open(filename, "wb") as f:
                # Download in chunks for large files
                for chunk in response.iter_content(1024):
                    if chunk:  # filter out keep-alive new chunks
                        f.write(chunk)
            print(f"File downloaded: {filename}")
    else:
        print("Task failed or was cancelled")


if __name__ == "__main__":
    response = upload_file()
    task_id = response["task_id"]
    download_file(task_id)
