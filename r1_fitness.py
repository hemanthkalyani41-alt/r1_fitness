import streamlit as st
import pandas as pd
from datetime import datetime, date
from streamlit_gsheets import GSheetsConnection

# --- APP STYLING & CONFIG ---
# We set the page to wide layout and inject Custom CSS to make it look like a real gym website
st.set_page_config(page_title="R1 Fitness", page_icon="🏋️‍♂️", layout="wide")

st.markdown("""
    <style>
    /* Main background and text colors */
    .stApp { background-color: #0a0a0a; color: #ffffff; }
    h1, h2, h3 { color: #ff3333; font-family: 'Arial Black', sans-serif; text-transform: uppercase; }
    
    /* Custom Feature Cards */
    .feature-card {
        background-color: #1a1a1a;
        padding: 25px;
        border-radius: 10px;
        border-left: 5px solid #ff3333;
        box-shadow: 0 4px 8px rgba(255,51,51,0.2);
        margin-bottom: 20px;
    }
    .feature-card h4 { color: #ffffff; margin-bottom: 10px; }
    .feature-card p { color: #cccccc; font-size: 14px; }
    
    /* Button Styling */
    .stButton>button { 
        background-color: #ff3333; 
        color: white; 
        font-weight: bold; 
        border-radius: 8px; 
        border: none; 
        width: 100%;
        transition: 0.3s;
    }
    .stButton>button:hover { background-color: #cc0000; border: 1px solid white; }
    </style>
    """, unsafe_allow_html=True)

# --- DATABASE CONNECTION ---
conn = st.connection("gsheets", type=GSheetsConnection)

try:
    df = conn.read(worksheet="Members", ttl=0)
except:
    df = pd.DataFrame(columns=['id', 'name', 'phone', 'expiry_date'])

# --- SIDEBAR NAVIGATION ---
st.sidebar.image("https://img.icons8.com/color/96/000000/dumbbell.png", width=80) # Placeholder sidebar icon
st.sidebar.title("Navigation")
page = st.sidebar.radio("", ["Home & BMI", "Member Login", "Admin Panel"])

# --- 1. HOME & BMI CALCULATOR (UPGRADED) ---
if page == "Home & BMI":
    
    # Header Section with Logo
    col1, col2 = st.columns([1, 4])
    with col1:
        try:
            st.image("logo.png", width=120) # This will load the logo you uploaded to GitHub
        except:
            st.write("🏋️‍♂️") # Fallback if logo.png isn't found
    with col2:
        st.title("R1 FITNESS")
        st.markdown("### UNLEASH YOUR TRUE POTENTIAL")
    
    st.divider()
    
    # Gym Features Section using custom CSS cards
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
    
    # BMI Calculator Section
    st.write("## ⚖️ Check Your Stats")
    b1, b2, b3 = st.columns([1, 2, 1]) # Centers the calculator
    
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
            else: st.error("Category: Overweight")
        st.markdown("</div>", unsafe_allow_html=True)

# --- 2. MEMBER LOGIN (UNCHANGED) ---
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

# --- 3. ADMIN PANEL (UNCHANGED) ---
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
