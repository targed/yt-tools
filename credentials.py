import os
import pickle
import time
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build


credentials = None
token_path = "token.pickle"
if os.path.exists("token.pickle"):
    # Get the modification time
    mod_time = os.path.getmtime(token_path)
    # Get the current time
    current_time = time.time()
    # If the file is more than 2 days old
    if current_time - mod_time > 2 * 24 * 60 * 60:  # 2 days in seconds
        print("Token file is old, deleting and refreshing...")
        os.remove(token_path)
    else:
        print("Loading Credentials From File...")
        with open(token_path, "rb") as token:
            credentials = pickle.load(token)

    # If there are no valid credentials available, then either refresh the token or log in.
if not credentials or not credentials.valid:
    if credentials and credentials.expired and credentials.refresh_token:
        print("Refreshing Access Token...")
        credentials.refresh(Request())
    else:
        print("Fetching New Tokens...")
        flow = InstalledAppFlow.from_client_secrets_file(
            "client_secret.json", scopes=["https://www.googleapis.com/auth/youtube"]
        )
        flow.run_local_server(
            port=8080, prompt="consent", authorization_prompt_message=""
        )
        credentials = flow.credentials
        print(credentials.to_json())
        # Save the credentials for the next run
        with open("token.pickle", "wb") as f:
            print("Saving Credentials for Future Use...")
            pickle.dump(credentials, f)

youtube = build("youtube", "v3", credentials=credentials)
