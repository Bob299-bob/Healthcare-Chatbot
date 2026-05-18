#importing libraries
import streamlit as st
import tensorflow as tf
import joblib
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
import random
import json
#load the model
le=joblib.load('label.pkl')
token=joblib.load('token.pkl')
max_len=joblib.load('max_len.pkl')
model=tf.keras.models.load_model(
    'Health_chatbot.h5'
)
#open file /accessing file content
with open('Medical_intent.json',encoding='utf-8') as file:
    data_json = json.load(file)

st.markdown("""
<div style='
    color:#00ADB5;
    text-align:center;
    font-size:40px;
    font-weight:bold;
'>
🏥 Health Care ChatBot
</div>
""", unsafe_allow_html=True)

#detect language
def detect_language(text):
    text = text.lower()
    hindi_words = [
        "hai", "kaise", "kya", "mujhe",
        "bukhar", "sar", "dard", "pet",
        "khansi", "sardi"
    ]
    english_words = [
        "hello", "fever", "cold",
        "headache", "appointment",
        "medicine", "thanks"
    ]
    hindi_score = 0
    english_score = 0
    for word in hindi_words:
        if word in text:
            hindi_score += 1
    for word in english_words:
        if word in text:
            english_score += 1
    if hindi_score > 0 and english_score > 0:
        return "hinglish"
    elif hindi_score > 0:
        return "hindi"
    else:
        return "english"
    
#chatbot function
def chatbot(text):
    language=detect_language(text)
    text=text.lower()
    seq=token.texts_to_sequences([text])
    pad=pad_sequences(seq,maxlen=max_len)
    Y_pred=model.predict(pad,verbose=0)
    index=np.argmax(Y_pred)
    tag=le.inverse_transform([index])[0]
    for intent in data_json['intents']:
        if intent['tag']==tag:
            if language == "english":
                return random.choice(intent['responses_english'])
            elif language == "hindi":
                return random.choice(intent['responses_hindi'])
            else:
                return random.choice(intent['responses_hinglish'])
    return "Sorry i did not understand Your message"

if 'my_input' not in st.session_state:
    st.session_state.my_input=""

if 'messages' not in st.session_state:
    st.session_state.messages=[]

if 'show_bmi' not in st.session_state:
    st.session_state.show_bmi = False

with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("Hi, What's your Query!", placeholder="Type your message here..")

    send = st.form_submit_button("Send")

    if send and user_input.strip():
        st.session_state.page="chat"
        st.session_state.messages.append(("You", user_input))
        response = chatbot(user_input)
        st.session_state.messages.append(("Bot", response))

clear = st.button("Clear Chat")

if clear:
    st.session_state.messages = []
    st.rerun()

for sender,message in st.session_state.messages:
    if sender == "You":
        st.markdown(f"""
                    <div style='
                        background-color:#1F2937;
                        padding:10px;
                        border-radius:10px;
                        margin:5px;
                        text-align:right;
                    '>
                    🧑{message}
                    </div>
                    """,
                    unsafe_allow_html=True)
    else:
        st.markdown(f"""
                    <div style='
                        background-color:#22C55E;
                        padding:10px;
                        border-radius:10px;
                        margin:5px;
                    '>
                    🤖 {message}
                    </div>
                    """,
                    unsafe_allow_html=True)
if clear:
    st.session_state.messages=[]
    st.rerun()
st.sidebar.markdown("""
<div style="
    color:#00ADB5;
    font-size:35px;
    font-weight:bold;
    font-family: 'Inter', 'Roboto', 'Helvetica Neue', sans-serif;
    letter-spacing: -0.1px;
">
How may i help you
</div>
""", unsafe_allow_html=True)
Home_btn=st.sidebar.button("🏠 Home")
hospital_btn = st.sidebar.button("🏥 Best Hospitals")
if Home_btn:
    st.session_state.page = "home"
    st.session_state.messages = []
    st.session_state.show_bmi = False
    st.rerun()
if st.session_state.get("page") == "home":
    st.write("👋 Hello! I'm your Healthcare ChatBot.")
    st.image("chatbot.jpg", width=800)

if hospital_btn:
    st.session_state.page = "hospital"
    st.session_state.messages = []
    st.session_state.show_bmi = False
    st.rerun()
if st.session_state.get("page") == "hospital":
    st.write("""
                # 🏥 Top Hospitals in India

                India has emerged as a leading destination for medical tourism, 
                offering exceptional healthcare at affordable costs.

                ### Top Hospitals:
                1. Medanta Hospitals  
                2. Gleneagles Global Health City  
                3. Artemis Hospitals  
                4. Kokilaben Dhirubhai Ambani Hospital  
                5. HCG Cancer Centre  
                6. Max Healthcare  
                7. Apollo Hospitals  
                8. Fortis Healthcare  
                9. Rainbow Children’s Hospital  
                10. BirthRight by Rainbow  
                11. Wockhardt Hospitals  
                These hospitals are known for:
                - Advanced treatments
                - Robotic surgeries
                - Cancer care
                - Heart surgeries
                - Organ transplants
                - Critical care """)
#background color
st.markdown("""
<style>
.stApp {
    background-color: #0F172A;
}
</style>
""", unsafe_allow_html=True)

#BMI 
bmi=st.sidebar.button("⚖️ BMI Calculator")
if bmi:
    st.session_state.page = "bmi"
    st.session_state.messages = []
    st.session_state.show_bmi = True
    st.rerun()

if st.session_state.get("page") == "bmi":
    st.markdown('BMI Calculator')
    weight = st.number_input(
        'Enter Your Weight (kg)',
        min_value=0.0,
        format='%.2f'
    )
    height_unit = st.radio(
        'Enter Your Height Unit:',
        ['Cm', 'Mt', 'Ft']
    )
    height = st.number_input(
        f"Enter Your Height ({height_unit})",
        min_value=0.0,
        format='%.2f'
    )
    if st.button('Calculate BMI'):

        if height_unit == 'Cm':
            height_m = height / 100

        elif height_unit == 'Ft':
            height_m = height * 0.3048

        else:
            height_m = height

        if height_m <= 0:
            st.error('Height must be greater than zero.')

        else:
            bmi_value = weight / (height_m ** 2)

            st.success(f"Your BMI is: {bmi_value:.2f}")

            # BMI Interpretation
            if bmi_value < 18.5:
                st.warning('You are Underweight')

            elif bmi_value < 24.9:
                st.success('💪 Your weight is Normal')

            else:
                st.error('You are Overweight')