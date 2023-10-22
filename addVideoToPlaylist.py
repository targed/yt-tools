exec(open("credentials.py").read())


def add_video_to_playlist(youtube, videoID, playlistID):
    youtube.playlistItems().insert(
        part="snippet",
        body={
            "snippet": {
                "playlistId": playlistID,
                "resourceId": {"kind": "youtube#video", "videoId": videoID},
            }
        },
    ).execute()
