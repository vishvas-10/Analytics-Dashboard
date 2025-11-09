import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd

st.title("🎵 Spotify Insights Dashboard")

# Spotify authentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="291ad8abaaae4977a0fcab3e7d4005fe",
    client_secret="c8797472fdd94cb8bed6d9111e49e459",
    redirect_uri="https://analytics-dashboard-spotify.streamlit.app/",
    scope="user-top-read"
))

# Get user’s top artists
st.subheader("Your Top Artists 🎤")
top_artists = sp.current_user_top_artists(limit=10)
artists = [a['name'] for a in top_artists['items']]
popularity = [a['popularity'] for a in top_artists['items']]

df = pd.DataFrame({'Artist': artists, 'Popularity': popularity})
st.bar_chart(df.set_index('Artist'))