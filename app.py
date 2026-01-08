import streamlit as st
import requests
import os
from dotenv import load_dotenv

# --- CONFIGURATION ---
# Load environment variables from .env file
load_dotenv()

# Retrieve the API Key from environment variables
API_KEY = os.getenv("OPENWEATHER_API_KEY")

# Configure Streamlit page settings
st.set_page_config(page_title="Skybeat | Aesthesius", page_icon="🎵", layout="centered")

# --- DATA: PREDEFINED CITIES ---
# A curated list of major global cities for the dropdown menu
MAJOR_CITIES = [
    "Select a City...", "Istanbul", "Izmir", "Ankara", "London", "New York", 
    "Tokyo", "Paris", "Berlin", "Moscow", "Dubai", "Singapore", 
    "Los Angeles", "Barcelona", "Rome", "Amsterdam", "Toronto", 
    "Sydney", "Seoul", "Mumbai", "Rio de Janeiro", "Cape Town", 
    "Bangkok", "San Francisco"
]

# --- BRANDING SECTION (Oracle Style) ---
# Aesthesius as the main brand, Skybeat as the product under it
st.markdown(
    """
    <div style='text-align: center; padding-top: 20px; padding-bottom: 30px;'>
        <h1 style='font-size: 70px; font-weight: 800; letter-spacing: 4px; color: #FF4B4B; margin-bottom: 0; text-shadow: 2px 2px 8px rgba(0,0,0,0.3);'>
            AESTHESIUS
        </h1>
        <h2 style='font-size: 35px; font-weight: 300; letter-spacing: 10px; color: #E0E0E0; margin-top: -10px; margin-bottom: 20px; text-transform: uppercase;'>
            SKYBEAT
        </h2>
        <div style="width: 60px; height: 3px; background-color: #FF4B4B; margin: 0 auto;"></div>
        <p style='padding-top: 15px; color: gray; font-style: italic;'>Weather Based Audio Experience</p>
    </div>
    """,
    unsafe_allow_html=True
)
# ---------------------------------------

# Function to fetch weather data from OpenWeatherMap API
def get_weather(city_name):
    # Check if API Key exists
    if not API_KEY:
        st.error("SYSTEM ERROR: API Key not found! Please check your .env file.")
        return None

    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city_name,
        "appid": API_KEY,
        "units": "metric",
        "lang": "en" # English response for global consistency
    }
    
    try:
        response = requests.get(base_url, params=params)
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            return None # City not found
        else:
            print(f"Error fetching data: {response.status_code}")
            return None
    except Exception as e:
        print(f"Exception occurred: {e}")
        return None

# Function to recommend a song based on weather condition
def recommend_song(weather_main):
    weather_main = weather_main.lower()
    
    # Dictionary mapping weather conditions to song recommendations
    # Structure: condition -> (Display Status, Song - Artist, Genre)
    recommendations = {
        "clear": ("Sunny", "Pharrell Williams - Happy", "Pop/Energetic"),
        "clouds": ("Cloudy", "The Neighbourhood - Sweater Weather", "Indie/Lo-fi"),
        "rain": ("Rainy", "Adele - Set Fire to the Rain", "Melancholic/Jazz"),
        "drizzle": ("Drizzling", "Rhye - Open", "Chill"),
        "thunderstorm": ("Stormy", "AC/DC - Thunderstruck", "Rock/Metal"),
        "snow": ("Snowy", "Frank Sinatra - Let It Snow", "Classic/Jazz"),
        "mist": ("Misty", "Radiohead - Pyramid Song", "Alternative"),
        "haze": ("Hazy", "Glass Animals - Heat Waves", "Psychedelic Pop"),
        "fog": ("Foggy", "Bon Iver - Holocene", "Indie Folk")
    }
    
    # Return default recommendation if condition is not found
    return recommendations.get(weather_main, ("Unknown Mood", "Bob Marley - Three Little Birds", "Reggae"))

# Main application logic
def main():
    st.write("---")
    
    # --- INPUT SECTION ---
    # Layout: Dropdown (and potential text input) on the left, Button on the right
    
    col_input, col_btn = st.columns([3, 1])
    
    with col_input:
        # User selects from list
        selected_option = st.selectbox(
            "📍 Select Destination:", 
            options=MAJOR_CITIES + ["Other / Custom Search"], 
            label_visibility="collapsed"
        )
        
        # Logic to determine the final city name
        city_to_search = ""
        
        if selected_option == "Other / Custom Search":
            city_to_search = st.text_input("Enter City Name:", placeholder="Type any city (e.g. Kemalpaşa)...")
        elif selected_option != "Select a City...":
            city_to_search = selected_option

    with col_btn:
        # Add some vertical spacing to align button with input fields
        st.write("") 
        if selected_option == "Other / Custom Search":
            st.write("") # Extra spacing if text input is visible
            
        search_btn = st.button("SEARCH", use_container_width=True)

    # --- ACTION SECTION ---
    if search_btn:
        if city_to_search:
            with st.spinner('Accessing satellite data...'):
                data = get_weather(city_to_search)
                
                if data:
                    # Parse relevant data
                    weather_condition = data['weather'][0]['main']
                    description = data['weather'][0]['description']
                    temp = data['main']['temp']
                    
                    # Get recommendation
                    en_status, song, genre = recommend_song(weather_condition)
                    
                    # --- RESULTS DISPLAY ---
                    st.markdown("### 📡 Weather Report")
                    st.success(f"Location: **{city_to_search.upper()}** | Status: **{description.title()}** | Temp: **{temp:.1f}°C**")
                    
                    st.markdown("---")
                    
                    # Recommendation Box
                    st.markdown(f"### 🎧 Aesthesius Recommendation")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric(label="Current Mood", value=en_status)
                    with col2:
                        st.metric(label="Suggested Genre", value=genre)
                    
                    st.info(f"Now Playing: **{song}**")
                    
                else:
                    st.error(f"Could not find weather data for '{city_to_search}'. Please check the spelling.")
        else:
            st.warning("Please select or enter a city name.")

# Entry point of the script
if __name__ == "__main__":
    main()