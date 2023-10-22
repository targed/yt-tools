import csv
import re

from credentials import *


def get_video_id(url):
    youtube_regex = (
        r"(https?://)?(www\.)?"
        "(youtube|youtu|youtube-nocookie)\.(com|be)/"
        "(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})"
    )

    youtube_regex_match = re.match(youtube_regex, url)
    if youtube_regex_match:
        return youtube_regex_match.group(6)
    return None


def add_video_to_playlist(youtube, videoID, playlistID):
    youtube.playlistItems().insert(
        part="snippet",
        body={
            "snippet": {
                "playlistId": playlistID,
                "resourceId": {"kind": "youtube#video", "videoId": videoID},
            }
        },
        fields="id",
    ).execute()


def addCSV(playlistID):
    video_ids = []
    added_videos = set()

    with open("data.csv", "r") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            video_id = get_video_id(row[0])
            video_ids.append(video_id)

    for video_id in video_ids:
        if video_id not in added_videos:
            try:
                add_video_to_playlist(youtube, video_id, playlistID)
                added_videos.add(video_id)
                print("Added video to playlist")
            except Exception as e:
                print(f"An error occurred: {e}")
