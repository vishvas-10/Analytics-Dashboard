import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import os

st.title("🎵 Spotify Insights Dashboard")

# Ensure cache directory exists
os.makedirs(".cache", exist_ok=True)

auth_manager = SpotifyOAuth(
    client_id=st.secrets["spotify"]["client_id"],
    client_secret=st.secrets["spotify"]["client_secret"],
    redirect_uri=st.secrets["spotify"]["redirect_uri"],
    scope="user-top-read user-library-read user-read-private user-read-email",
    cache_path=".cache/token.txt",
    show_dialog=True
)

# Authenticate user
sp = spotipy.Spotify(auth_manager=auth_manager)

st.subheader("Your Top Artists 🎤")

try:
    top_artists = sp.current_user_top_artists(limit=10, time_range='medium_term')
    st.write(top_artists)  # Debug output

    if not top_artists or not top_artists["items"]:
        st.warning("⚠️ No top artists found. Try listening to more music or adjusting your scope.")
    else:
        artists = [a["name"] for a in top_artists["items"]]
        popularity = [a["popularity"] for a in top_artists["items"]]
        df = pd.DataFrame({"Artist": artists, "Popularity": popularity})
        st.dataframe(df)
        st.bar_chart(df.set_index("Artist"))

except Exception as e:
    st.error(f"Error: {e}")
