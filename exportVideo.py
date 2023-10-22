import csv
from datetime import datetime, timedelta
import os
import re

from credentials import *

stuffToFetch = ["publishedAt", "channelId", "channelTitle", "title"]


def fetch_video_info(vid_id):
    request = youtube.videos().list(part="snippet,contentDetails,statistics", id=vid_id)
    response = request.execute()
    newList = []
    for item in response["items"]:
        for stuff in stuffToFetch:
            newList.append(item["snippet"][stuff])
    yt_link = f"https://youtu.be/{vid_id}"
    newList.append(yt_link)
    return newList


def fetch_video_duration(vid_id):
    print("Fetching video duration...")
    vid_request = youtube.videos().list(part="contentDetails", id=vid_id)
    vid_response = vid_request.execute()
    duration = vid_response["items"][0]["contentDetails"]["duration"]
    hours_pattern = re.compile(r"((\d+)H)")
    minutes_pattern = re.compile(r"((\d+)M)")
    seconds_pattern = re.compile(r"((\d+)S)")
    hours = hours_pattern.search(duration)
    minutes = minutes_pattern.search(duration)
    seconds = seconds_pattern.search(duration)
    hours = int(hours.group(2)) if hours else 0
    minutes = int(minutes.group(2)) if minutes else 0
    seconds = int(seconds.group(2)) if seconds else 0
    video_seconds = timedelta(
        hours=hours, minutes=minutes, seconds=seconds
    ).total_seconds()
    return str(int(video_seconds))


def get_video_title(video_id):
    print("Getting video title...")
    request = youtube.videos().list(
        part="snippet, contentDetails, statistics", id=video_id
    )
    response = request.execute()
    for item in response["items"]:
        video_title = item["snippet"]["title"]
    return video_title


def save_data_to_files(total_list, video_title):
    print("Saving data to files...")
    dateNow = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    dateNowString = str(dateNow).replace(" ", "_").replace(":", "_").replace("-", "_")
    dirName = "youtube_data"
    dir = os.path.join(dirName, video_title, "youtube_data_" + dateNowString)

    def create_txt():
        f1 = os.path.join(dir, "youtube_data_" + dateNowString + ".txt")
        f = open(f1, "a")
        f.write(str(total_list))
        f.close()

    def create_csv():
        csv_write = open(
            dir + "\\" + "youtube_data_" + dateNowString + ".csv",
            "w",
            newline="",
            encoding="utf-8",
        )
        write = csv.writer(csv_write)
        write.writerow(total_list)

    if not os.path.exists(dir):
        if not os.path.exists(dirName):
            os.mkdir(dirName)
        os.makedirs(dir)
        print("Directory ", dir, " Created ")
        create_txt()
        create_csv()
    else:
        print("Directory ", dir, " already exists")
        create_txt()
        create_csv()


def process_video(video_id):
    print("Processing playlist...")
    save_data_to_files(fetch_video_info(video_id), get_video_title(video_id))
