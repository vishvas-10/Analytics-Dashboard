import streamlit as st
import requests
import pandas as pd
import base64

st.set_page_config(page_title="Spotify Insights", page_icon="🎧", layout="centered")
st.title("🎵 Spotify Insights Dashboard")

# --- Spotify credentials ---
client_id = st.secrets["spotify"]["client_id"]
client_secret = st.secrets["spotify"]["client_secret"]
redirect_uri = st.secrets["spotify"]["redirect_uri"]
scope = "user-top-read"

# --- Step 1: Authorization URL ---
auth_url = (
    "https://accounts.spotify.com/authorize"
    f"?client_id={client_id}"
    "&response_type=code"
    f"&redirect_uri={redirect_uri}"
    f"&scope={scope}"
)

# --- Step 2: Get authorization code from redirect ---
query_params = st.query_params
if "code" not in query_params:
    st.markdown(f"[🔑 Log in with Spotify]({auth_url})")
else:
    code = query_params["code"]

    # --- Step 3: Exchange code for access token ---
    token_url = "https://accounts.spotify.com/api/token"
    auth_header = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()

    response = requests.post(
        token_url,
        data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": redirect_uri,
        },
        headers={"Authorization": f"Basic {auth_header}"}
    )

    token_info = response.json()
    access_token = token_info.get("access_token")

    if not access_token:
        st.error("Failed to get access token 😢")
        st.json(token_info)
    else:
        st.success("✅ Authenticated with Spotify!")

        # --- Step 4: Get top artists ---
        headers = {"Authorization": f"Bearer {access_token}"}
        res = requests.get("https://api.spotify.com/v1/me/top/artists?limit=10", headers=headers)
        data = res.json()

        if "items" not in data:
            st.warning("No top artists found or missing scope.")
            st.json(data)
        else:
            artists = [a["name"] for a in data["items"]]
            popularity = [a["popularity"] for a in data["items"]]
            df = pd.DataFrame({"Artist": artists, "Popularity": popularity})
            st.dataframe(df)
            st.bar_chart(df.set_index("Artist"))
