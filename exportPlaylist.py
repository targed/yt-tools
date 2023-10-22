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


def process_playlist_item(vid_id):
    print("Processing playlist item...")
    request = youtube.videos().list(part="snippet,contentDetails,statistics", id=vid_id)
    response = request.execute()
    for item in response["items"]:
        if item["snippet"]["title"] in ["Deleted video", "Private video"]:
            return None
    video_info = fetch_video_info(vid_id)
    video_duration = fetch_video_duration(vid_id)
    video_info.append(video_duration)
    return video_info


def get_playlist_title(playlist_id):
    print("Getting playlist title...")
    request = youtube.playlists().list(part="snippet", id=playlist_id)
    response = request.execute()
    for item in response["items"]:
        playlist_title = item["snippet"]["title"]
    return playlist_title


def process_playlist_items(playlist_id):
    print("Processing playlist items...")
    max_results = 50
    list_parts = "snippet, contentDetails"
    nextPageToken = None
    total_list = []
    while True:
        pl_response = (
            youtube.playlistItems()
            .list(
                part=list_parts,
                playlistId=playlist_id,
                maxResults=max_results,
                pageToken=nextPageToken,
            )
            .execute()
        )
        for item in pl_response["items"]:
            # If the title of the video is not "Deleted video" or "Private video", store the video's ID, name, and other information in various lists
            if (item["snippet"]["title"]) != "Deleted video":
                if (item["snippet"]["title"]) != "Private video":
                    vid_id = item["contentDetails"]["videoId"]
                    total_list.append(process_playlist_item(vid_id))
                else:
                    continue
            else:
                continue
        nextPageToken = pl_response.get("nextPageToken")
        if not nextPageToken:
            break
    return total_list


def save_data_to_files(total_list, playlist_title):
    print("Saving data to files...")
    dateNow = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    dateNowString = str(dateNow).replace(" ", "_").replace(":", "_").replace("-", "_")
    dirName = "youtube_data"
    dir = os.path.join(dirName, playlist_title, "youtube_data_" + dateNowString)

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
        write.writerows(total_list)

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


def process_playlist(playlist_id):
    print("Processing playlist...")
    save_data_to_files(
        process_playlist_items(playlist_id), get_playlist_title(playlist_id)
    )
