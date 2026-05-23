import streamlit as st
from datetime import datetime, timedelta
import google.generativeai as genai
import requests

# ==========================================
# PAGE CONFIG
# ==========================================
st.set_page_config(
    page_title="AgroAI Smart Farmer",
    page_icon="🌱",
    layout="wide"
)

# ==========================================
# CUSTOM CSS
# ==========================================
st.markdown("""
<style>
.main {
    background: linear-gradient(to right,#0f172a,#1e293b);
    color: white;
}

.title {
    text-align:center;
    font-size:50px;
    font-weight:bold;
    color:white;
}

.subtitle {
    text-align:center;
    color:lightgray;
    margin-bottom:30px;
}

.stButton>button {
    width:100%;
    border-radius:10px;
    height:3em;
    font-size:16px;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# API KEYS
# ==========================================
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
WEATHER_API_KEY = st.secrets["WEATHER_API_KEY"]

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash-8b")

# ==========================================
# HEADER
# ==========================================
st.markdown(
    '<div class="title">🌱 AgroAI Smart Farmer</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">AI Farming + Weather + Harvest Prediction</div>',
    unsafe_allow_html=True
)

# ==========================================
# SIDEBAR
# ==========================================
with st.sidebar:

    st.header("⚙️ Settings")

    language = st.selectbox(
        "🌍 Language",
        ["English", "Tamil", "Sinhala"]
    )

# ==========================================
# FARM INPUT
# ==========================================
st.header("🌾 Crop Information")

crop = st.selectbox(
    "Select Crop",
    [
        "Tomato",
        "Rice",
        "Chili",
        "Onion",
        "Carrot",
        "Cucumber",
        "Brinjal"
    ]
)

variety = st.text_input(
    "Enter Variety Name"
)

seed_date = st.date_input(
    "🌱 Seed Planted Date"
)

city = st.text_input(
    "📍 Enter Your City",
    "Colombo"
)

# ==========================================
# HARVEST CALCULATION
# ==========================================
harvest_days = {
    "Tomato": 90,
    "Rice": 120,
    "Chili": 100,
    "Onion": 110,
    "Carrot": 80,
    "Cucumber": 60,
    "Brinjal": 95
}

days_needed = harvest_days.get(crop, 90)

harvest_date = seed_date + timedelta(days=days_needed)

remaining_days = (harvest_date - datetime.now().date()).days

# ==========================================
# WEATHER API
# ==========================================
weather_url = f"""
https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric
"""

weather_data = None

try:

    response = requests.get(weather_url)

    weather_data = response.json()

except:
    pass

# ==========================================
# SHOW RESULTS
# ==========================================
if st.button("🌱 Generate Smart Farming Report"):

    st.success(f"🌾 Crop: {crop}")

    st.info(f"🧬 Variety: {variety}")

    st.success(
        f"⏰ Estimated Harvest Date: {harvest_date.strftime('%d-%m-%Y')}"
    )

    st.warning(
        f"📅 Days Remaining: {remaining_days}"
    )

    # ======================================
    # WEATHER
    # ======================================
    st.header("🌦️ Weather Information")

    try:

        temp = weather_data["main"]["temp"]

        humidity = weather_data["main"]["humidity"]

        condition = weather_data["weather"][0]["description"]

        st.success(f"🌡️ Temperature: {temp} °C")

        st.info(f"💧 Humidity: {humidity}%")

        st.warning(f"☁️ Condition: {condition}")

        # WATERING ADVICE
        st.header("💧 AI Watering Advice")

        if "rain" in condition.lower():

            st.success(
                "🌧️ Rain expected. No watering needed today."
            )

        else:

            st.warning(
                "💧 Low rain chance. Water plants tomorrow morning."
            )

    except:

        st.error("Weather data not available.")

    # ======================================
    # AI ADVICE
    # ======================================
    st.header("🤖 AI Farming Advice")

    prompt = f"""
    Give farming advice for:

    Crop: {crop}
    Variety: {variety}

    Include:
    - Fertilizer advice
    - Watering tips
    - Harvest tips
    - Disease prevention

    Language: {language}

    Keep answers simple for farmers.
    """

    try:

        ai_response = model.generate_content(prompt)

        st.write(ai_response.text)

    except Exception as e:

        st.error(f"AI Error: {e}")

# ==========================================
# CHATBOT
# ==========================================
st.header("🤖 AgroAI Chatbot")

question = st.text_input(
    "Ask Farming Questions"
)

if question:

    chatbot_prompt = f"""
    You are a smart farming assistant.

    Language: {language}

    Answer simply.

    Question:
    {question}
    """

    try:

        reply = model.generate_content(chatbot_prompt)

        st.success(reply.text)

    except Exception as e:

        st.error(f"Error: {e}")

# ==========================================
# FOOTER
# ==========================================
st.markdown("---")

st.caption("🚀 Made By Jathusvarman")
