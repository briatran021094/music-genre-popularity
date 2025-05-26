import requests
import pandas as pd
import bs4
import os

# Youtube Data API Credentials
CLIENT_ID = ""
CLIENT_SECRET = ""

import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

# === Step 1: Setup credentials ===
CLIENT_ID = "291370592725-g06rv387lao91g974cingr21rcku2ffg.apps.googleusercontent.com"
CLIENT_SECRET = "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"

# === Step 2: Define the OAuth scopes (read-only YouTube data) ===
scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

# === Step 3: Create a client secrets JSON dynamically ===
client_secrets_file = "client_secret.json"
with open(client_secrets_file, "w") as f:
    f.write(f"""
{{
  "installed": {{
    "client_id": "{CLIENT_ID}",
    "client_secret": "{CLIENT_SECRET}",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob", "http://localhost"]
  }}
}}
""")

# === Step 4: Authenticate and build the API client ===
flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
    client_secrets_file, scopes)
credentials = flow.run_console()

youtube = googleapiclient.discovery.build(
    "youtube", "v3", credentials=credentials)

# === Step 5: Make a sample API call (search for top music videos) ===
def search_music_videos(query="Top Music", max_results=5):
    request = youtube.search().list(
        part="snippet",
        maxResults=max_results,
        q=query,
        type="video",
        videoCategoryId="10"  # Music
    )
    response = request.execute()

    print(f"\n🔍 Search results for: {query}")
    for item in response["items"]:
        title = item["snippet"]["title"]
        video_id = item["id"]["videoId"]
        url = f"https://www.youtube.com/watch?v={video_id}"
        print(f"- {title}\n  {url}")

# === Step 6: Run search ===
search_music_videos("Top Music USA")

# Run and save to CSV
df = scrape_youtube_top_tracks()
df.to_csv('youtube_top_tracks_by_region.csv', index=False)
print("Data saved to 'youtube_top_tracks_by_region.csv'")
