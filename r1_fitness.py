import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime, date

# --- DATABASE SETUP ---
conn = sqlite3.connect('r1_fitness_db.sqlite', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS members 
             (id TEXT PRIMARY KEY, name TEXT, phone TEXT, expiry_date DATE)''')
conn.commit()

# --- APP STYLING ---
st.set_page_config(page_title="R1 Fitness", layout="wide")
st.markdown("""
    <style>
    .main { background-color: #111; color: white; }
    h1 { color: #ff4b4b; text-align: center; }
    .stButton>button { background-color: #ff4b4b; color: white; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR NAVIGATION ---
page = sidebar_selection = st.sidebar.radio("Navigation", ["Home & BMI", "Member Login", "Admin Panel"])

# --- 1. HOME & BMI CALCULATOR ---
if page == "Home & BMI":
    st.title("R1 FITNESS 🏋️‍♂️")
    st.subheader("Transform Your Life")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("### Why R1 Fitness?")
        st.write("* 24/7 Access\n* Expert Trainers\n* Modern Equipment")
        
    with col2:
        st.write("### BMI Calculator")
        weight = st.number_input("Weight (kg)", min_value=1.0, step=0.1)
        height = st.number_input("Height (cm)", min_value=1.0, step=0.1)
        
        if st.button("Calculate BMI"):
            height_m = height / 100
            bmi = weight / (height_m ** 2)
            st.success(f"Your BMI is: {round(bmi, 2)}")
            if bmi < 18.5: st.warning("Category: Underweight")
            elif 18.5 <= bmi < 25: st.info("Category: Normal Weight")
            else: st.error("Category: Overweight")

# --- 2. MEMBER LOGIN ---
elif page == "Member Login":
    st.title("Member Portal")
    member_id = st.text_input("Enter your Member ID to verify")
    
    if st.button("View My Info"):
        c.execute("SELECT * FROM members WHERE id=?", (member_id,))
        user = c.fetchone()
        if user:
            st.write(f"### Welcome back, {user[1]}!")
            st.info(f"Your Membership Expiry Date: {user[3]}")
            
            # Check if expired
            expiry = datetime.strptime(user[3], '%Y-%m-%d').date()
            if expiry < date.today():
                st.error("Your membership has expired. Please visit the desk to renew.")
            else:
                st.success("Your membership is Active.")
        else:
            st.error("Member ID not found.")

# --- 3. ADMIN PANEL ---
elif page == "Admin Panel":
    st.title("Admin Dashboard")
    password = st.text_input("Enter Admin Password", type="password")
    
    if password == "admin123": # You can change this password
        st.success("Access Granted")
        
        with st.expander("Add New Member"):
            new_id = st.text_input("Member ID (e.g., R1-001)")
            new_name = st.text_input("Full Name")
            new_phone = st.text_input("Phone Number")
            new_expiry = st.date_input("Membership Expiry Date")
            
            if st.button("Register Member"):
                try:
                    c.execute("INSERT INTO members VALUES (?,?,?,?)", (new_id, new_name, new_phone, new_expiry))
                    conn.commit()
                    st.success("Member added successfully!")
                except:
                    st.error("This ID already exists.")

        st.divider()
        st.subheader("Current Members & Notifications")
        df = pd.read_sql_query("SELECT * FROM members", conn)
        
        # Expiry Notifications Logic
        if not df.empty:
            df['expiry_date'] = pd.to_datetime(df['expiry_date']).dt.date
            today = date.today()
            
            # Highlight members expiring within 7 days
            expiring_soon = df[(df['expiry_date'] <= today + pd.Timedelta(days=7))]
            
            if not expiring_soon.empty:
                st.warning(f"⚠️ {len(expiring_soon)} Memberships expiring soon or expired!")
                st.table(expiring_soon)
            
            st.write("### Complete Member List")
            st.dataframe(df)
    elif password != "":
        st.error("Incorrect Password")
