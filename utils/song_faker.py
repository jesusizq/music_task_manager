# This file will create and populate csv_files/songs_data_raw.csv file with fake data.
# The resulting file must contain headers: Song, Date (in format YYYY-MM-DD), Number of Plays

import csv
import random
import datetime
import calendar


def create_fake_data():
    with open("csv_files/songs_data_raw.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Song", "Date", "Number of Plays"])

        for _ in range(1000):
            song = f"Song name {random.randint(1, 20)}"
            year = 2024
            month = random.randint(1, 12)
            num_days = calendar.monthrange(year, month)[1]
            day = random.randint(1, num_days)
            date = datetime.date(year, month, day)
            plays = random.randint(1, 1000)

            writer.writerow([song, date, plays])


create_fake_data()
