import streamlit as st
import requests
import os
from dotenv import load_dotenv

# --- CONFIGURATION ---
load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

st.set_page_config(page_title="Skybeat | Aesthesius", page_icon="🎵", layout="centered")

# --- DATA ---
MAJOR_CITIES = [
    "Select a City...", "Istanbul", "Izmir", "Ankara", "London", "New York", 
    "Tokyo", "Paris", "Berlin", "Moscow", "Dubai", "Singapore", 
    "Los Angeles", "Barcelona", "Rome", "Amsterdam"
]

# --- BRANDING ---
st.markdown(
    """
    <div style='text-align: center; padding-top: 10px; padding-bottom: 20px;'>
        <h1 style='font-size: 70px; font-weight: 800; letter-spacing: 4px; color: #FF4B4B; margin-bottom: 0; text-shadow: 2px 2px 8px rgba(0,0,0,0.3);'>AESTHESIUS</h1>
        <h2 style='font-size: 30px; font-weight: 300; letter-spacing: 8px; color: #E0E0E0; margin-top: -10px; text-transform: uppercase;'>SKYBEAT</h2>
        <div style="width: 50px; height: 3px; background-color: #FF4B4B; margin: 10px auto;"></div>
    </div>
    """,
    unsafe_allow_html=True
)

# --- BACKEND FUNCTIONS ---
def get_weather(city_name):
    if not API_KEY:
        st.error("SYSTEM ERROR: API Key missing.")
        return None

    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {"q": city_name, "appid": API_KEY, "units": "metric", "lang": "en"}
    
    try:
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            return None
        return None
    except:
        return None

def recommend_song(weather_main):
    weather_main = weather_main.lower()
    
    # Structure: condition -> (Mood, Song Name, Artist, Genre, Spotify/YouTube Link)
    recommendations = {
        "clear": ("Sunny & Bright", "Happy", "Pharrell Williams", "Pop", "https://open.spotify.com/track/60nZcImufyMA1KT4eoro2W"),
        "clouds": ("Cloudy Vibes", "Sweater Weather", "The Neighbourhood", "Indie", "https://open.spotify.com/track/2QjOHCTQ1Jl3zawyYOpxh6"),
        "rain": ("Melancholic Rain", "Set Fire to the Rain", "Adele", "Soul/Pop", "https://open.spotify.com/track/5PkWxpOh4tjDi11AMN9VE1"),
        "drizzle": ("Light Drizzle", "Open", "Rhye", "Chill", "https://open.spotify.com/track/3JsA2swdNR9oQss0xVIyAX"),
        "thunderstorm": ("Stormy Power", "Thunderstruck", "AC/DC", "Hard Rock", "https://open.spotify.com/track/57bgtoPSgt236HzfBOd8kj"),
        "snow": ("Snowy Silence", "Let It Snow!", "Frank Sinatra", "Classic Jazz", "https://open.spotify.com/track/4kKdvXD0ez7jp1296JkWts"),
        "mist": ("Misty Mystery", "Pyramid Song", "Radiohead", "Art Rock", "https://open.spotify.com/track/55qBw1900pZKfXJ6Q9A2Lc"),
    }
    
    return recommendations.get(weather_main, ("Chill Mode", "Three Little Birds", "Bob Marley", "Reggae", "https://open.spotify.com/track/6A9mNKZG8AEKNHJ66ZFj33"))

# --- FRONTEND UI ---
def main():
    col1, col2 = st.columns([3, 1])
    with col1:
        option = st.selectbox("Select Destination:", MAJOR_CITIES + ["Custom Search"], label_visibility="collapsed")
        city = st.text_input("Enter City:", placeholder="Type city name...") if option == "Custom Search" else (option if option != "Select a City..." else "")
    with col2:
        st.write("")
        if option == "Custom Search": st.write("") 
        btn = st.button("SCAN SKY", use_container_width=True)

    if btn and city:
        with st.spinner('Accessing satellite data...'):
            data = get_weather(city)
            if data:
                main_weather = data['weather'][0]['main']
                desc = data['weather'][0]['description'].title()
                temp = data['main']['temp']
                
                mood, song, artist, genre, link = recommend_song(main_weather)
                
                # UI Result Card
                st.markdown("---")
                c1, c2, c3 = st.columns(3)
                c1.metric("Location", city.upper())
                c2.metric("Condition", desc)
                c3.metric("Temp", f"{temp:.1f}°C")
                
                st.success(f"Detected Mood: **{mood}**")
                
                # Music Card
                with st.container():
                    st.markdown(f"""
                    <div style="background-color: #1E1E1E; padding: 20px; border-radius: 10px; border: 1px solid #333;">
                        <h3 style="color: #FF4B4B; margin:0;">Now Playing</h3>
                        <p style="font-size: 20px; margin: 5px 0;"><strong>{song}</strong></p>
                        <p style="color: gray;">by {artist} ({genre})</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.write("")
                    st.link_button(f"▶ Play on Spotify", link, use_container_width=True)
            else:
                st.error("City not found. Please try again.")

if __name__ == "__main__":
    main()