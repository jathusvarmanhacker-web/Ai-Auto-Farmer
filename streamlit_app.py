import streamlit as st
from PIL import Image
from datetime import datetime, timedelta
import google.generativeai as genai

# ==========================================
# PAGE CONFIG
# ==========================================
st.set_page_config(
    page_title="AgroAI Pro",
    page_icon="🌱",
    layout="wide"
)

# ==========================================
# CUSTOM DESIGN
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

.css-1d391kg {
    background-color:#111827;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# GEMINI API
# ==========================================
API_KEY = st.secrets["GEMINI_API_KEY"]

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("models/gemini-2.0-flash")

# ==========================================
# HEADER
# ==========================================
st.markdown(
    '<div class="title">🌱 AgroAI Pro</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">AI Powered Smart Farming Assistant</div>',
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

    crop_type = st.selectbox(
        "🌾 Crop Type",
        ["Tomato", "Rice", "Chili", "Onion", "Carrot"]
    )

# ==========================================
# IMAGE DETECTION
# ==========================================
st.header("📷 AI Crop Detection")

uploaded = st.file_uploader(
    "Upload Fruit or Vegetable Image",
    type=["jpg", "jpeg", "png"]
)

if uploaded:

    image = Image.open(uploaded)

    st.image(
        image,
        caption="Uploaded Image",
        use_container_width=True
    )

    with st.spinner("🔍 AI Analyzing Image..."):

        prompt = f"""
        Identify this fruit or vegetable.

        Give:
        1. Name
        2. Ripeness level
        3. Health condition
        4. Estimated harvest days

        Answer in {language}.
        """

        try:

            response = model.generate_content(
                [prompt, image]
            )

            st.success(response.text)

        except Exception as e:

            st.error(f"Error: {e}")

# ==========================================
# HARVEST REMINDER
# ==========================================
st.header("⏰ Harvest Reminder")

days = st.number_input(
    "Estimated Harvest Days",
    min_value=1,
    max_value=365,
    value=7
)

if st.button("Create Harvest Reminder"):

    future_date = datetime.now() + timedelta(days=days)

    st.success(
        f"🌾 Harvest Date: {future_date.strftime('%d-%m-%Y')}"
    )

    st.info(
        f"⏳ Countdown: {days} days remaining"
    )

# ==========================================
# WATERING REMINDER
# ==========================================
st.header("💧 Smart Watering Reminder")

rain_level = st.slider(
    "Rain Level (%)",
    0,
    100,
    30
)

if st.button("Get Watering Advice"):

    if rain_level < 40:

        st.warning(
            f"""
            Low rain expected.

            💧 Water your {crop_type} tomorrow morning.
            """
        )

    else:

        st.success(
            f"""
            Enough rain expected.

            🌧️ No watering needed today.
            """
        )

# ==========================================
# AI FARMING CHATBOT
# ==========================================
st.header("🤖 AI Farming Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input(
    "Ask farming questions..."
)

if user_input:

    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            chatbot_prompt = f"""
            You are a smart AI farming assistant.

            Answer simply for farmers.

            Language: {language}

            Question:
            {user_input}
            """

            try:

                response = model.generate_content(
                    chatbot_prompt
                )

                reply = response.text

            except Exception as e:

                reply = f"Error: {e}"

            st.markdown(reply)

    st.session_state.messages.append({
        "role": "assistant",
        "content": reply
    })

# ==========================================
# FOOTER
# ==========================================
st.markdown("---")

st.caption("🚀 Made By Jathusvarman")
