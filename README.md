# YouTube Data Exporter

This project allows you to export data from YouTube playlists and videos. It uses the YouTube Data API to fetch data and exports it in CSV format.

## Features

- Export a YouTube playlist as a CSV file
- Retrieve information about a specific YouTube video

## Installation

1. Clone this repository
2. Create a virtual environment:

```bash
python -m venv venv
```

3. Activate the virtual environment:

```bash
venv\Scripts\activate
```

4. Install the required Python packages using pip:

```bash
pip install -r requirements.txt
```

## API key

Before running the project, you need to set up a Google API key and download a `client_secret.json` file.

### Create an API Key

1. Go to the [Google Developers Console](https://console.developers.google.com/).
2. Create a new project.
3. Click on "Enable APIs and Services".
4. Search for "YouTube Data API v3" and enable it.
5. Go to "Credentials" on the left sidebar.
6. Click on "Create Credentials" and choose "API key".
7. Your new API key will be displayed.

### Get a client_secret.json file

1. Go to the [Google Developers Console](https://console.developers.google.com/).
2. Select your project.
3. Go to "Credentials" on the left sidebar.
4. Click on "Create Credentials" and choose "OAuth client ID".
5. Configure the OAuth consent screen.
6. Choose "Desktop app" as the application type, and create.
7. Your client ID and client secret will be displayed.
8. Click on the download button on the right side of the client ID to download the `client_secret.json` file.

Place the `client_secret.json` file in the root directory of the project.

## Usage

### Export a playlist

To export a playlist as a CSV file, use the playlist command and provide the playlist ID:

```bash
python main.py playlist --playlistid YOUR_PLAYLIST_ID
```

### Retrieve video information

To retrieve information about a specific YouTube video, use the video command and provide the video ID:

```bash
python main.py video --videoid YOUR_VIDEO_ID
```

### Add a video

To add a video to a playlist, use the addvideo command and provide the video ID and playlist ID:

```bash
python main.py addvideo --videoid YOUR_VIDEO_ID --playlistid YOUR_PLAYLIST_ID
```

### Add a CSV

To add a CSV file of video IDs to a playlist, use the addcsv command and provide the CSV file path and playlist ID:

```bash
python main.py addcsv --playlistid YOUR_PLAYLIST_ID
```

# Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

# License

[MIT](https://choosealicense.com/licenses/mit/)

# Project status

This project is currently in development.
