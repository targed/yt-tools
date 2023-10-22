# Import necessary libraries
import os
import re
import csv
import pandas as pd
from credentials import *
from datetime import datetime, timedelta
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

# This function takes in a video ID and retrieves information about the video. It is called in Main.py


def vid(vidid):
    # Execute the contents of the "credentials.py" file to authenticate and authorize the script to access the YouTube API
    exec(open("credentials.py").read())
    # Convert the video ID to a string
    vid_id = str(vidid)
    # Format the current date and time as a string, replacing spaces with underscores, colons with underscores, and hyphens with underscores
    dateNowString = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")).replace(
        " ", "_").replace(":", "_").replace("-", "_")
    # Compile regular expression patterns to extract the number of hours, minutes, and seconds from a duration string
    hours_pattern = re.compile(r"((\d+)H)")
    minutes_pattern = re.compile(r"((\d+)M)")
    seconds_pattern = re.compile(r"((\d+)S)")
    # Initialize an empty list and a pandas DataFrame with the specified columns
    total_list = []
    df = pd.DataFrame(
        columns=["publishedAt", "channelId", "description", "channelTitle", "categoryId", "liveBroadcastContent", "defaultAudioLanguage", "duration", "viewCount", "likeCount", "commentCount"])
    vid_title = []
    # Make a request to the YouTube API to retrieve information about the specified video
    request = youtube.videos().list(
        part="snippet, contentDetails, statistics",
        id=vid_id
    )
    # Execute the request and store the response
    response = request.execute()

    for item in response["items"]:
        # Extract data from the 'snippet' field of the item
        publishedAt = (item['snippet']["publishedAt"])
        channelId = (item['snippet']["channelId"])
        title = (item['snippet']["title"])
        description = str((item['snippet']["description"]))
        channelTitle = (item['snippet']["channelTitle"])
        categoryId = (item['snippet']["categoryId"])
        liveBroadcastContent = (item['snippet']["liveBroadcastContent"])
        defaultAudioLanguage = (item['snippet']["defaultAudioLanguage"])
        # Extract data from the 'contentDetails' field of the item
        duration = item['contentDetails']['duration']
        # Parse the duration string to extract hours, minutes, and seconds
        hours = hours_pattern.search(duration)
        minutes = minutes_pattern.search(duration)
        seconds = seconds_pattern.search(duration)
        # Convert the extracted values to integers and set them to 0 if not found
        hours = int(hours.group(2)) if hours else 0
        minutes = int(minutes.group(2)) if minutes else 0
        seconds = int(seconds.group(2)) if seconds else 0
        # Calculate the total number of seconds of the video duration
        video_seconds = timedelta(
            hours=hours, minutes=minutes, seconds=seconds).total_seconds()
        # Extract data from the 'statistics' field of the item
        viewCount = (item['statistics']["viewCount"])
        likeCount = (item['statistics']["likeCount"])
        commentCount = (item['statistics']["commentCount"])
        # Append the title to the list of video titles
        vid_title.append(title)
        # Append all the data to the total list and the DataFrame
        total_list.append([publishedAt, channelId, title, description,
                          channelTitle, categoryId, liveBroadcastContent, defaultAudioLanguage, video_seconds, viewCount, likeCount, commentCount])
        df.loc[len(df.index)] = {"publishedAt": publishedAt, "channelId": channelId, "description": description, "channelTitle": channelTitle,
                                 "categoryId": categoryId, "liveBroadcastContent": liveBroadcastContent, "defaultAudioLanguage": defaultAudioLanguage, "duration": video_seconds, "viewCount": viewCount, "likeCount": likeCount, "commentCount": commentCount}

    dirName = "youtube_data"
    dir = os.path.join(
        dirName, vid_title[0], "youtube_data_" + dateNowString)

    def create_csv():
        # This function creates a csv file using the 'csv' module and writes the data in 'total_list' to the file.
        csv_write = open(dir + "\\" + "youtube_data_" +
                         dateNowString + '.csv', 'w', newline='',  encoding='utf-8')
        write = csv.writer(csv_write)
        write.writerows(total_list)

    def create_pandas():
        # This function creates a csv file using the 'pandas' library and writes the data in 'df' to the file.
        df.to_csv(dir + "\\" + "youtube_data_pandas_" +
                  dateNowString + ".csv")

    if not os.path.exists(dir):
        # If the directory does not exist, create it and then call the two functions to create csv files.
        if not os.path.exists(dirName):
            os.mkdir(dirName)
            os.makedirs(dir)
            print("Directory ", dir,  " Created ")
            create_csv()
            create_pandas()
        else:
            os.makedirs(dir)
            print("Directory ", dir,  " Created ")
            create_csv()
            create_pandas()
    else:
        # If the directory does exist, call the two functions to create csv files.
        print("Directory ", dir,  " already exists")
        create_csv()
        create_pandas()
