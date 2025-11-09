import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd

st.title("🎵 Spotify Insights Dashboard")

# Spotify authentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=st.secrets['spotify']['client_id'],
    client_secret=st.secrets['spotify']['client_secret'],
    redirect_uri=st.secrets['spotify']['redirect_uri'],
    scope="user-top-read"
))

# Get user’s top artists
st.subheader("Your Top Artists 🎤")
top_artists = sp.current_user_top_artists(limit=10)
artists = [a['name'] for a in top_artists['items']]
popularity = [a['popularity'] for a in top_artists['items']]

df = pd.DataFrame({'Artist': artists, 'Popularity': popularity})
st.bar_chart(df.set_index('Artist'))
