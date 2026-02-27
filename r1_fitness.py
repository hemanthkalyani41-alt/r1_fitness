import streamlit as st
import pandas as pd
from datetime import datetime, date
from streamlit_gsheets import GSheetsConnection

# --- APP STYLING & CONFIG ---
st.set_page_config(page_title="R1 Fitness", layout="wide")
st.markdown("""
    <style>
    .main { background-color: #111; color: white; }
    h1 { color: #ff4b4b; text-align: center; }
    .stButton>button { background-color: #ff4b4b; color: white; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# --- DATABASE CONNECTION ---
conn = st.connection("gsheets", type=GSheetsConnection)

try:
    df = conn.read(worksheet="Members", ttl=0)
except:
    df = pd.DataFrame(columns=['id', 'name', 'phone', 'expiry_date'])

# --- SIDEBAR NAVIGATION ---
page = st.sidebar.radio("Navigation", ["Home & BMI", "Member Login", "Admin Panel"])

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
        # 1. Clean up the database IDs (force them to be text and remove spaces)
        df['id'] = df['id'].astype(str).str.strip()
        
        # 2. Clean up the ID the customer just typed
        clean_search_id = str(member_id).strip()
        
        # 3. Search for the exact match
        user_data = df[df['id'] == clean_search_id]
        
        if not user_data.empty:
            name = user_data.iloc[0]['name']
            expiry_str = str(user_data.iloc[0]['expiry_date'])
            
            st.write(f"### Welcome back, {name}!")
            st.info(f"Your Membership Expiry Date: {expiry_str}")
            
            # Check if expired
            try:
                expiry = datetime.strptime(expiry_str, '%Y-%m-%d').date()
                if expiry < date.today():
                    st.error("Your membership has expired. Please visit the desk to renew.")
                else:
                    st.success("Your membership is Active.")
            except:
                st.warning("Could not verify exact date format.")
        else:
            st.error("Member ID not found.")

# --- 3. ADMIN PANEL ---
elif page == "Admin Panel":
    st.title("Admin Dashboard")
    password = st.text_input("Enter Admin Password", type="password")
    
    if password == "admin123": 
        st.success("Access Granted")
        
        with st.expander("Add New Member"):
            new_id = st.text_input("Member ID (e.g., R1-001)")
            new_name = st.text_input("Full Name")
            new_phone = st.text_input("Phone Number")
            new_expiry = st.date_input("Membership Expiry Date")
            
            if st.button("Register Member"):
                # Clean up existing IDs to check for duplicates safely
                existing_ids = df['id'].astype(str).str.strip().tolist()
                clean_new_id = str(new_id).strip()
                
                if clean_new_id in existing_ids:
                    st.error("This ID already exists.")
                else:
                    new_row = pd.DataFrame([{
                        'id': clean_new_id, 
                        'name': new_name, 
                        'phone': new_phone, 
                        'expiry_date': new_expiry.strftime('%Y-%m-%d')
                    }])
                    updated_df = pd.concat([df, new_row], ignore_index=True)
                    
                    conn.update(worksheet="Members", data=updated_df)
                    st.success("Member added successfully! Data saved to cloud.")
                    st.rerun()

        st.divider()
        st.subheader("Current Members & Notifications")
        
        if not df.empty:
            try:
                df['date_obj'] = pd.to_datetime(df['expiry_date']).dt.date
                today = date.today()
                
                expiring_soon = df[(df['date_obj'] <= today + pd.Timedelta(days=7))]
                
                if not expiring_soon.empty:
                    st.warning(f"⚠️ {len(expiring_soon)} Memberships expiring soon or expired!")
                    st.table(expiring_soon.drop(columns=['date_obj']))
            except:
                st.write("Ensure all dates are in YYYY-MM-DD format for notifications to work.")
            
            st.write("### Complete Member List")
            display_df = df.drop(columns=['date_obj']) if 'date_obj' in df.columns else df
            st.dataframe(display_df)
            
    elif password != "":
        st.error("Incorrect Password")
