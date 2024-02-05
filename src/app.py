import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import os
import pandas as pd 
import seaborn as sns

load_dotenv()

client_id = os.environ.get("CLIENT_ID")
client_secret = os.environ.get("CLIENT_SECRET")
print(client_id)
print(client_secret)

sp = spotipy.Spotify(auth_manager = SpotifyClientCredentials(client_id = client_id, client_secret = client_secret))

artist_id = "6XyY86QOPPrYVGvF9ch6wz"

response = sp.artist_top_tracks(artist_id)

if response and "tracks" in response:
    # Extract the "tracks" object from the response
    tracks = response["tracks"]

    # Select relevant data for each track and convert duration from milliseconds to minutes
    tracks_data = [
        {
            "name": track.get("name", ""),
            "popularity": track.get("popularity", 0),
            "duration_minutes": (track.get("duration_ms", 0) / (1000 * 60)) % 60
        }
        for track in tracks
    ]

    # Print the resulting tracks data
    for track_data in tracks_data:
        print(f"Track: {track_data['name']}, Popularity: {track_data['popularity']}, Duration: {track_data['duration_minutes']:.2f} minutes")
else:
    print("Failed to retrieve top tracks.")

# Create a DataFrame from the list of dictionaries
tracks_df = pd.DataFrame(tracks_data)

tracks_df = pd.DataFrame.from_records(tracks)
tracks_df.sort_values(by="popularity", ascending=False, inplace=True)

print(tracks_df.head(3))

scatter_plot = sns.scatterplot(data = tracks_df, x = "popularity", y = "duration_ms")
fig = scatter_plot.get_figure()
fig.savefig("scatter_plot.png")

