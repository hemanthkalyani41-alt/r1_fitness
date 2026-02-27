import streamlit as st
import pandas as pd
from datetime import datetime, date
from streamlit_gsheets import GSheetsConnection

# --- APP STYLING & CONFIG ---
st.set_page_config(page_title="R1 Fitness", page_icon="🏋️‍♂️", layout="wide")

st.markdown("""
    <style>
    /* Main background and text colors */
    .stApp { background-color: #0a0a0a; color: #ffffff; }
    
    /* Changed to Bold Yellow */
    h1, h2, h3 { color: #FFCC00; font-family: 'Arial Black', sans-serif; text-transform: uppercase; }
    
    /* Custom Feature Cards with Yellow Accents */
    .feature-card {
        background-color: #1a1a1a;
        padding: 25px;
        border-radius: 10px;
        border-left: 5px solid #FFCC00;
        box-shadow: 0 4px 8px rgba(255, 204, 0, 0.2);
        margin-bottom: 20px;
    }
    .feature-card h4 { color: #ffffff; margin-bottom: 10px; }
    .feature-card p { color: #cccccc; font-size: 14px; }
    
    /* Button Styling - Yellow background with Black text */
    .stButton>button { 
        background-color: #FFCC00; 
        color: #000000; 
        font-weight: bold; 
        border-radius: 8px; 
        border: none; 
        width: 100%;
        transition: 0.3s;
    }
    .stButton>button:hover { 
        background-color: #CCA300; 
        color: #000000;
        border: 1px solid #ffffff; 
    }
    </style>
    """, unsafe_allow_html=True)

# --- DATABASE CONNECTION ---
conn = st.connection("gsheets", type=GSheetsConnection)

try:
    df = conn.read(worksheet="Members", ttl=0)
except:
    df = pd.DataFrame(columns=['id', 'name', 'phone', 'expiry_date'])

# --- SIDEBAR NAVIGATION ---
st.sidebar.image("https://img.icons8.com/color/96/000000/dumbbell.png", width=80) 
st.sidebar.title("Navigation")
page = st.sidebar.radio("", ["Home & BMI", "Member Login", "Admin Panel"])

# --- 1. HOME & BMI CALCULATOR ---
if page == "Home & BMI":
    
    col1, col2 = st.columns([1, 4])
    with col1:
        try:
            st.image("logo.png", width=120) 
        except:
            st.write("🏋️‍♂️") 
    with col2:
        st.title("R1 FITNESS")
        st.markdown("### UNLEASH YOUR TRUE POTENTIAL")
    
    st.divider()
    
    st.write("## 🚀 Elite Facilities")
    f1, f2, f3 = st.columns(3)
    
    with f1:
        st.markdown("""
        <div class="feature-card">
            <h4>🏋️ Heavy Lifting Zone</h4>
            <p>Multiple squat racks, deadlift platforms, and dumbbells up to 60kg for serious strength training.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with f2:
        st.markdown("""
        <div class="feature-card">
            <h4>🏃 Modern Cardio</h4>
            <p>High-end treadmills, stair climbers, and assault bikes equipped with individual screens.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with f3:
        st.markdown("""
        <div class="feature-card">
            <h4>🧠 Expert Coaching</h4>
            <p>Certified personal trainers available 24/7 to guide your form, diet, and training programs.</p>
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    
    st.write("## ⚖️ Check Your Stats")
    b1, b2, b3 = st.columns([1, 2, 1]) 
    
    with b2:
        st.markdown("<div style='background-color:#1a1a1a; padding:20px; border-radius:10px;'>", unsafe_allow_html=True)
        st.write("#### BMI Calculator")
        weight = st.number_input("Weight (kg)", min_value=1.0, step=0.1)
        height = st.number_input("Height (cm)", min_value=1.0, step=0.1)
        
        if st.button("Calculate My BMI"):
            height_m = height / 100
            bmi = weight / (height_m ** 2)
            st.success(f"**Your BMI is: {round(bmi, 2)}**")
            if bmi < 18.5: st.warning("Category: Underweight")
            elif 18.5 <= bmi < 25: st.info("Category: Normal Weight")
            else: st.
