import streamlit as st
import pandas as pd
from datetime import datetime, date
from streamlit_gsheets import GSheetsConnection

# --- APP STYLING & CONFIG ---
st.set_page_config(page_title="R1 Fitness", page_icon="🟨", layout="wide")

st.markdown("""
    <style>
    /* Main background and text colors */
    .stApp { background-color: #0a0a0a; color: #ffffff; }
    
    /* Bold Yellow Accents */
    h1, h2, h3 { color: #FFCC00; font-family: 'Arial Black', sans-serif; text-transform: uppercase; }
    
    /* Logo Tagline */
    .tagline { color: #ffffff; font-style: italic; font-size: 1.2rem; margin-top: -15px; margin-bottom: 30px;}
    
    /* Custom Cards for Features and Pricing */
    .custom-card {
        background-color: #1a1a1a;
        padding: 25px;
        border-radius: 10px;
        border-top: 5px solid #FFCC00;
        box-shadow: 0 4px 8px rgba(255, 204, 0, 0.15);
        margin-bottom: 20px;
        text-align: center;
    }
    .custom-card h3 { color: #FFCC00; margin-bottom: 10px; font-size: 24px;}
    .custom-card h2 { color: #ffffff; margin-bottom: 10px; font-size: 32px;}
    .custom-card p { color: #cccccc; font-size: 15px; }
    
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
st.sidebar.title("🟨 R1 FITNESS")
page = st.sidebar.radio("Menu", ["Home & Plans", "Member Login", "Admin Panel"])

# --- 1. HOME & PLANS ---
if page == "Home & Plans":
    
    # Text-Based Logo and Tagline
    st.markdown("<h1 style='font-size: 4rem; text-align: center;'>R1 FITNESS</h1>", unsafe_allow_html=True)
    st.markdown("<p class='tagline' style='text-align: center;'>FOR GOOD LIFE</p>", unsafe_allow_html=True)
    
    st.divider()
    
    # --- PRICING PLANS SECTION ---
    st.write("<h2 style='text-align: center;'>Membership Plans</h2>", unsafe_allow_html=True)
    p1, p2, p3 = st.columns(3)
    
    with p1:
        st.markdown("""
        <div class="custom-card">
            <h3>1 MONTH</h3>
            <h2>₹1000</h2>
            <p>Full gym access<br>Standard equipment<br>Locker room</p>
        </div>
        """, unsafe_allow_html=True)
        
    with p2:
        st.markdown("""
        <div class="custom-card" style="border-top: 5px solid #ffffff;">
            <h3 style="color: #ffffff;">3 MONTHS</h3>
            <h2>₹2000</h2>
            <p>Full gym access<br>Diet consultation<br>Save ₹1000!</p>
        </div>
        """, unsafe_allow_html=True)
        
    with p3:
        st.markdown("""
        <div class="custom-card">
            <h3>1 YEAR</h3>
            <h2>₹5000</h2>
            <p>Premium 24/7 access<br>Personal training prep<br>Best Value!</p>
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    
    # --- BMI CALCULATOR ---
    st.write("<h2 style='text-align: center;'>Check Your Stats</h2>", unsafe_allow_html=True)
    b1, b2, b3 = st.columns([1, 2, 1]) 
    
    with b2:
        st.markdown("<div style='background-color:#1a1a1a; padding:20px; border-radius:10px; border: 1px solid #333;'>", unsafe_allow_html=True)
        st.write("<h4 style='color: #FFCC00; text-align: center;'>BMI Calculator</h4>", unsafe_allow_html=True)
        weight = st.number_input("Weight (kg)", min_value=1.0, step=0.1)
        height = st.number_input("Height (cm)", min_value=1.0, step=0.1)
        
        if st.button("Calculate My BMI"):
            height_m = height / 100
            bmi = weight / (height_m ** 2)
            st.success(f"**Your BMI is: {round(bmi, 2)}**")
            if bmi < 18.5: st.warning("Category: Underweight")
            elif 18.5 <= bmi < 25: st.info("Category: Normal Weight")
            else: st.error("Category: Overweight")
        st.markdown("</div>", unsafe_allow_html=True)

# --- 2. MEMBER LOGIN ---
elif page == "Member Login":
    st.title("Member Portal")
    member_id = st.text_input("Enter your Member ID to verify")
    
    if st.button("View My Info"):
        df['id'] = df['id'].astype(str).str.replace(r'\.0$', '', regex=True).str.strip().str.upper()
        clean_search_id = str(member_id).strip().upper()
        user_data = df[df['id'] == clean_search_id]
        
        if not user_data.empty:
            name = user_data.iloc[0]['name']
            expiry_str = str(user_data.iloc[0]['expiry_date'])
            
            st.write(f"### Welcome back, {name}!")
            st.info(f"Your Membership Expiry Date: {expiry_str}")
            
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
                existing_ids = df['id'].astype(str).str.replace(r'\.0$', '', regex=True).str.strip().str.upper().tolist()
                clean_new_id = str(new_id).strip().upper()
                
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
                pass
            
            st.write("### Complete Member List")
            display_df = df.drop(columns=['date_obj']) if 'date_obj' in df.columns else df
            st.dataframe(display_df)
            
    elif password != "":
        st.error("Incorrect Password")
