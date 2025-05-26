import requests
import pandas as pd
import bs4
import os

# SoundCLoud APi Credentials
CLIENT_ID = ""
CLIENT_SECRET = ""

# new, top, mix, track, and artist urls
top_url = "http://soundcloud.com/charts/top"
new_url = "http://soundcloud.com/charts/new"
track_url = "http://soundcloud.com/search/sounds?q="
artist_url = "http://soundcloud.com/search/people?q="

# Base URL for SoundCloud API
base_url = "https://api.soundcloud.com/"

# Function to fetch popular tracks (or charts) based on your query
def get_soundcloud_tracks(query, max_results=50):
    # Endpoint to search for tracks
    search_url = f"{base_url}tracks?client_id={CLIENT_ID}&q={query}&limit={max_results}"
    response = requests.get(search_url)
    tracks_data = response.json()

    track_details = []

    for track in tracks_data:
        track_title = track['title']
        track_artist = track['user']['username']
        track_id = track['id']
        track_url = track['permalink_url']
        track_genre = track.get('genre', 'Unknown')
        track_play_count = track['playback_count']

        track_details.append({
            'Track ID': track_id,
            'Title': track_title,
            'Artist': track_artist,
            'URL': track_url,
            'Genre': track_genre,
            'Play Count': track_play_count
        })

    return track_details


# Example: Get popular tracks for a query (e.g., "pop music")
query = "pop music"
tracks = get_soundcloud_tracks(query, max_results=50)

# Convert the data to a DataFrame
df = pd.DataFrame(tracks)
df.to_csv("soundcloud_pop_tracks.csv", index=False)

print("Data saved to 'soundcloud_pop_tracks.csv'")

# Run and save to CSV
df = scrape_soundcloud_top_tracks()
df.to_csv('soundcloud_top_tracks_by_region.csv', index=False)
print("Data saved to 'soundcloud_top_tracks_by_region.csv'")
