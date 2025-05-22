import requests
import pandas as pd
import time
import base64

# Spotify API Credentials
CLIENT_ID = 'c03a9479599f47fd9658037ae05dda66'
CLIENT_SECRET = '888ff42cca164da48b10609162111b6e'


# Get access token using Client Credentials Flow
def get_access_token():
    auth_url = 'https://accounts.spotify.com/api/token'
    auth_str = f"{CLIENT_ID}:{CLIENT_SECRET}"
    b64_auth_str = base64.b64encode(auth_str.encode()).decode()

    headers = {
        'Authorization': f'Basic {b64_auth_str}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {'grant_type': 'client_credentials'}

    response = requests.post(auth_url, headers=headers, data=data)
    response.raise_for_status()

    return response.json()['access_token']


# Fetch all playlist tracks with pagination
def get_playlist_tracks(token, playlist_id, market='US'):
    headers = {'Authorization': f'Bearer {token}'}
    url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'
    params = {'market': market, 'limit': 100}

    items = []

    while url:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            print(f"ERROR {response.status_code}: {response.json().get('error', {}).get('message', 'Unknown error')}")
            print(f"URL: {url}")
            return []

        data = response.json()
        items.extend(data.get('items', []))
        url = data.get('next')  # Get the next page
        params = None  # Only include params on the first request

    return items


# Get genre(s) by artist ID
def get_artist_genres(token, artist_id):
    headers = {'Authorization': f'Bearer {token}'}
    url = f'https://api.spotify.com/v1/artists/{artist_id}'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get('genres', [])
    return []


# Example playlist IDs for "Top 50 by Country" (official Spotify Global Top 50 playlists)
top_playlists = {
    'us': '37i9dQZEVXbLRQDuF5jeBp',
    'jp': '37i9dQZEVXbKqiTGXuCOsB',
    'mx': '37i9dQZEVXbO3qyFxbkOE1L'
}


# Main scraping function
def scrape_spotify_top_tracks():
    token = get_access_token()
    all_tracks = []

    for region, playlist_id in top_playlists.items():
        print(f"Scraping region: {region.upper()}")
        items = get_playlist_tracks(token, playlist_id, market=region.upper())
        if not items:
            continue

        for item in items:
            track = item.get('track')
            if not track:
                continue

            title = track.get('name')
            artists = [a['name'] for a in track.get('artists', [])]
            artist_id = track['artists'][0]['id'] if track['artists'] else None
            genres = get_artist_genres(token, artist_id) if artist_id else []
            track_url = track.get('external_urls', {}).get('spotify', '')

            all_tracks.append({
                'Region': region.upper(),
                'Track': title,
                'Artists': ', '.join(artists),
                'Genres': ', '.join(genres),
                'Spotify URL': track_url
            })
            time.sleep(0.2)  # Prevent hitting rate limits

    return pd.DataFrame(all_tracks)


# Run and save to CSV
df = scrape_spotify_top_tracks()
df.to_csv('spotify_top_tracks_by_region.csv', index=False)
print("Data saved to 'spotify_top_tracks_by_region.csv'")