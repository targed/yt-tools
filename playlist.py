# Import necessary libraries
import csv
import re
from datetime import datetime
from datetime import timedelta

import pandas as pd

from credentials import *


def playlist(plid):
    # Set the target encoding format
    targetFormat = "utf-8"
    # Import credentials from a separate file
    exec(open("credentials.py").read())

    # Set playlist ID to the input parameter
    playlist_id = plid
    # Set maximum number of results per loop to 50. This is the max the API allows at once
    max_results = 50
    # Set list of parts to retrieve from YouTube API
    list_parts = "snippet, contentDetails"
    # Get current date and time in specified format
    dateNow = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Compile regular expressions for extracting hours, minutes, and seconds from duration strings
    hours_pattern = re.compile(r"((\d+)H)")
    minutes_pattern = re.compile(r"((\d+)M)")
    seconds_pattern = re.compile(r"((\d+)S)")
    # Initialize variables for storing video information
    total_seconds = 0
    total_vid_links = []
    total_vid_names = []
    total_published_at = []
    total_list = []
    total_list_txt = []
    total_channel_name = []
    total_channel_id = []
    total_descriptions = []
    total_video_seconds = []
    playlist_title = []
    items_number = 0
    # Initialize a Pandas DataFrame with specified columns
    df = pd.DataFrame(
        columns=[
            "Video link",
            "Video Name",
            "Channel name",
            "Channel link",
            "Published at",
        ]
    )
    # Initialize variable for storing next page token
    nextPageToken = None

    while True:
        # Make a request to the YouTube API to retrieve playlist items from a playlist with the specified ID
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
        # Make a request to the YouTube API to retrieve information about the playlist with the specified ID
        pl_response1 = (
            youtube.playlists().list(part="snippet", id=playlist_id).execute()
        )
        # Create an empty list to store video IDs
        vid_ids = []
        # Loop through the playlist information
        for item1 in pl_response1["items"]:
            # If the playlist title is empty, add the title to the list
            if not playlist_title:
                playlist_title.append(item1["snippet"]["title"])
            # If the playlist title is not empty, break out of the loop
            else:
                break
        # Print a message to indicate that the program is looping through the playlist items
        print("Looping through the playlist items...")
        # Loop through the playlist items
        for item in pl_response["items"]:
            # If the title of the video is not "Deleted video" or "Private video", store the video's ID, name, and other information in various lists
            if (item["snippet"]["title"]) != "Deleted video":
                if (item["snippet"]["title"]) != "Private video":
                    vid_ids.append(item["contentDetails"]["videoId"])
                    vid_id = item["contentDetails"]["videoId"]
                    published_at = item["snippet"]["publishedAt"]
                    vid_name = item["snippet"]["title"]
                    description = item["snippet"]["description"]
                    channel_name = (
                        (item["snippet"]["videoOwnerChannelTitle"])
                        if "videoOwnerChannelTitle" in item["snippet"]
                        else "Unknown"
                    )
                    channel_id = (
                        (item["snippet"]["videoOwnerChannelId"])
                        if "videoOwnerChannelId" in item["snippet"]
                        else "Unknown"
                    )
                    yt_link = f"https://youtu.be/{vid_id}"
                    total_vid_links.append(yt_link)
                    total_vid_names.append(vid_name)
                    total_published_at.append(published_at)
                    total_channel_name.append(channel_name)
                    total_descriptions.append(description)
                    total_channel_id.append(channel_id)
                    total_channel_url = f"https://www.youtube.com/channel/{channel_id}"
                    total_list_txt.append(
                        "["
                        + yt_link
                        + ", "
                        + vid_name
                        + ", "
                        + channel_name
                        + ", "
                        + total_channel_url
                        + description
                        + published_at
                        + "]"
                    )
                    total_list.append(
                        [
                            yt_link,
                            vid_name,
                            channel_name,
                            total_channel_url,
                            published_at,
                        ]
                    )
                    df.loc[len(df.index)] = {
                        "Video link": yt_link,
                        "Video Name": vid_name,
                        "Channel name": channel_name,
                        "Channel link": total_channel_url,
                        "Published at": published_at,
                    }
                    items_number += 1
                else:
                    break
            else:
                break

        print(items_number)
        print("Finished loop...")
        # Make a request to the YouTube API to get information about the videos in the playlist
        vid_request = youtube.videos().list(
            part="contentDetails, statistics", id=",".join(vid_ids)
        )
        # Print a message indicating that the program is fetching the list of YouTube videos
        print("Fetching youtube videos list...")
        # Execute the request and store the response
        vid_response = vid_request.execute()
        # Print a message indicating that the program is looping through the playlist items
        print("Looping through the playlist items...")
        # Loop through each item in the response
        for item in vid_response["items"]:
            # Get the duration of the video
            duration = item["contentDetails"]["duration"]
            # Parse the duration string to get the number of hours, minutes, and seconds
            hours = hours_pattern.search(duration)
            minutes = minutes_pattern.search(duration)
            seconds = seconds_pattern.search(duration)
            # Convert the hours, minutes, and seconds to integers
            hours = int(hours.group(2)) if hours else 0
            minutes = int(minutes.group(2)) if minutes else 0
            seconds = int(seconds.group(2)) if seconds else 0
            # Convert the duration to a timedelta object and get the total number of seconds
            video_seconds = timedelta(
                hours=hours, minutes=minutes, seconds=seconds
            ).total_seconds()
            # Add the number of seconds for this video to the total number of seconds
            total_seconds += video_seconds
            # Convert the number of seconds to an integer and then a string
            video_seconds_int = int(video_seconds)
            video_seconds_str = str(video_seconds_int)
            # Add the number of seconds for this video to the list of total video seconds
            total_video_seconds.append(video_seconds_str)
        # Check if there is a next page of results
        nextPageToken = pl_response.get("nextPageToken")
        # If there is no next page, break out of the loop
        if not nextPageToken:
            break
    # Set the counter for the inner loop to 0
    num_of_times_2 = 0
    # Loop through each item in the total_video_seconds list
    for item in total_video_seconds:
        # Add the item to the appropriate list in the total_list
        total_list[num_of_times_2].append(item)
        # Increment the counter
        num_of_times_2 += 1
    # Insert a new column at index 5 called "Seconds" and set its values to total_video_seconds
    df.insert(5, "Seconds", total_video_seconds, True)
    # Convert total_seconds to an integer
    total_seconds = int(total_seconds)
    # Divide total_seconds into hours, minutes, and seconds
    minutes, seconds = divmod(total_seconds, 60)
    hours, minutes = divmod(minutes, 60)
    # Print the time in hh:mm:ss format
    print(f"{hours}:{minutes}:{seconds}")
    # Encode the total_list_txt into targetFormat and join the list into a single string with newline separators
    new_total_list_string = "\n".join(total_list_txt).encode(targetFormat)
    # Create a new list with new_total_list_string as its only element
    new_list = [new_total_list_string]
    # Replace spaces, colons, and hyphens in the dateNow variable with underscores
    dateNowString = str(dateNow).replace(" ", "_").replace(":", "_").replace("-", "_")
    # Set the directory name and path
    dirName = "youtube_data"
    dir = os.path.join(dirName, playlist_title[0], "youtube_data_" + dateNowString)
    # Define a function to create a txt file

    def create_txt():
        f1 = dir + "\\" + "youtube_data_" + dateNowString + ".txt"
        f = open(f1, "a")
        f.write(str(new_list))
        f.close()

    # Define a function to create a csv file

    def create_csv():
        csv_write = open(
            dir + "\\" + "youtube_data_" + dateNowString + ".csv",
            "w",
            newline="",
            encoding="utf-8",
        )
        write = csv.writer(csv_write)
        write.writerows(total_list)

    # Define a function to create a pandas csv file

    def create_pandas():
        df.to_csv(dir + "\\" + "youtube_data_pandas_" + dateNowString + ".csv")

    # Check if the directory already exists
    if not os.path.exists(dir):
        # If the parent directory does not exist, create it and then create the subdirectory
        if not os.path.exists(dirName):
            os.mkdir(dirName)
            os.makedirs(dir)
            print("Directory ", dir, " Created ")
            create_txt()
            create_csv()
            create_pandas()
        # If the parent directory exists, just create the subdirectory
        else:
            os.makedirs(dir)
            print("Directory ", dir, " Created ")
            create_txt()
            create_csv()
            create_pandas()
    # If the directory already exists, just print a message
    else:
        print("Directory ", dir, " already exists")
        create_txt()
        create_csv()
        create_pandas()
