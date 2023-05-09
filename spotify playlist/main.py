#importing necessary libraries
from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

#Variables
CLIENT_ID = "5e4cead66f9249d2a54b4011d01528d7"
CLIENT_SECRET = "288072b0f778481cb84b3d77c8133c54"

#Taking input from the user

user_input = input("Enter your desired date in (YYYY-MM-DD): ")
# user_input = "2003-08-05"
response = requests.get(f"https://www.billboard.com/charts/hot-100/{user_input}")
response.raise_for_status()

billboard_data = response.text

soup = BeautifulSoup(billboard_data, "html.parser")

data = soup.select(".o-chart-results-list__item h3.c-title")


titles = [i.get_text().strip() for i in data]
# print(titles)


sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]

year = user_input.split("-")[0]

uri_list = []

print(titles)
for i in titles:
    try:
        song = sp.search(q=f"track:{i} year:{year}", type="track")
        uri = song["tracks"]["items"][0]["uri"]
        uri_list.append(uri)
    except IndexError:
        print(f"{i} doesn't exist in Spotify. Skipped.")


playlist = sp.user_playlist_create(user_id,name=f"{user_input} Billboard 100",public=False, description="A way to look back")


sp.playlist_add_items(playlist_id=playlist['id'], items=uri_list)
