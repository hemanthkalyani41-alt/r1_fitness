import streamlit as st
import pandas as pd
from datetime import datetime, date
from streamlit_gsheets import GSheetsConnection

# --- APP STYLING & CONFIG ---
st.set_page_config(page_title="R1 Fitness", layout="wide")

st.markdown("""
    <style>
    /* Main background and text colors */
    .stApp { background-color: #050505; color: #ffffff; }
    
    /* Bold Yellow Accents */
    h1, h2, h3, h4 { color: #FFCC00; font-family: 'Arial Black', sans-serif; text-transform: uppercase; text-shadow: 0px 0px 10px rgba(255, 204, 0, 0.2); }
    strong { color: #FFCC00; font-weight: 900; }
    
    /* Custom Cards */
    .custom-card {
        background-color: #111111;
        padding: 25px;
        border-radius: 10px;
        border-top: 5px solid #FFCC00;
        box-shadow: 0 4px 15px rgba(255, 204, 0, 0.15);
        margin-bottom: 20px;
        text-align: center;
    }
    .custom-card h3 { color: #FFCC00; margin-bottom: 10px; font-size: 24px;}
    .custom-card h2 { color: #ffffff; margin-bottom: 10px; font-size: 32px;}
    
    /* Quote Banner */
    .quote-banner {
        background-color: #FFCC00;
        padding: 20px;
        border-radius: 8px;
        text-align: center;
        margin: 30px 0;
        box-shadow: 0 0 20px rgba(255, 204, 0, 0.3);
    }
    .quote-banner h3 { color: #000000; margin: 0; font-style: italic; letter-spacing: 1px; text-shadow: none; }
    
    /* Button Styling */
    .stButton>button { 
        background-color: #FFCC00; 
        color: #000000; 
        font-weight: 900; 
        font-size: 18px;
        letter-spacing: 1px;
        border-radius: 8px; 
        border: none; 
        width: 100%;
        transition: 0.3s;
        text-transform: uppercase;
        box-shadow: 0 0 10px rgba(255, 204, 0, 0.4);
    }
    .stButton>button:hover { 
        background-color: #ffffff; 
        color: #000000;
        box-shadow: 0 0 20px rgba(255, 255, 255, 0.6); 
    }
    
    /* Info Box Styling */
    .info-box {
        background-color: #111;
        border: 1px solid #333;
        border-left: 5px solid #FFCC00;
        padding: 20px;
        border-radius: 5px;
        margin-bottom: 15px;
    }
    
    /* Admin Restricted Box */
    .admin-box {
        background-color: #0a0000;
        border: 1px solid #ff3333;
        padding: 30px;
        border-radius: 10px;
        text-align: center;
        margin-top: 20px;
        box-shadow: 0 0 15px rgba(255, 51, 51, 0.2);
    }
    </style>
    """, unsafe_allow_html=True)

# --- DATABASE CONNECTION ---
conn = st.connection("gsheets", type=GSheetsConnection)

try:
    df = conn.read(worksheet="Members", ttl=0)
except:
    df = pd.DataFrame(columns=['id', 'name', 'phone', 'expiry_date'])

# --- SIDEBAR NAVIGATION (Clean text, no cartoon emojis) ---
st.sidebar.markdown("<h2 style='text-align: center; color: #FFCC00;'>R1 FITNESS</h2>", unsafe_allow_html=True)
page = st.sidebar.radio("SYSTEM MENU", ["Home Base", "Membership Plans", "Member Portal", "Admin Command"])

# ==========================================
# 1. HOME BASE 
# ==========================================
if page == "Home Base":
    
    st.markdown("<h1 style='font-size: 4.5rem; text-align: center; margin-bottom: 0;'>R1 FITNESS</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #fff; font-size: 1.5rem; font-style: italic; letter-spacing: 3px;'>FOR GOOD LIFE</p>", unsafe_allow_html=True)
    
    st.image("https://images.unsplash.com/photo-1534438327276-14e5300c3a48?q=80&w=1470&auto=format&fit=crop", use_container_width=True)
    
    st.markdown("""
        <div class="quote-banner">
            <h3>"BLOOD, SWEAT, AND RESPECT. FIRST TWO YOU GIVE, LAST ONE YOU EARN."</h3>
        </div>
    """, unsafe_allow_html=True)
    
    col_rules, col_bmi = st.columns([1.2, 1])
    
    with col_rules:
        st.write("### GYM TIMINGS")
        st.markdown("""
        <div class="info-box" style="text-align: center;">
            <h2 style="color: #ffffff; margin: 0; font-size: 2.5rem;">09:00 - 12:00</h2>
            <p style="color: #FFCC00; font-weight: bold; margin: 0; letter-spacing: 2px;">OPEN EVERY DAY</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("### RULES OF THE IRON")
        st.markdown("""
        <div class="info-box">
            <h4 style="margin-top:0;">NO SMOKING</h4>
            <p style="color:#ccc; margin-bottom:0;">Strictly prohibited. Keep the air clean for those working hard.</p>
        </div>
        <div class="info-box">
            <h4 style="margin-top:0;">HYDRATION STATION</h4>
            <p style="color:#ccc; margin-bottom:0;">Unlimited clean drinking water is provided. Bring your shaker.</p>
        </div>
        <div class="info-box">
            <h4 style="margin-top:0;">LOCKER ROOMS</h4>
            <p style="color:#ccc; margin-bottom:0;">Separate, secure rooms provided to change out of your sweaty clothes.</p>
        </div>
        """, unsafe_allow_html=True)

    with col_bmi:
        st.image("https://images.unsplash.com/photo-1581009146145-b5ef050c2e1e?q=80&w=1470&auto=format&fit=crop", use_container_width=True)
        st.markdown("<div style='background-color:#111; padding:30px; border-radius:10px; border: 1px solid #333; margin-top: 15px;'>", unsafe_allow_html=True)
        st.write("<h4 style='color: #FFCC00; text-align: center; margin-bottom: 20px;'>BMI CALCULATOR</h4>", unsafe_allow_html=True)
        weight = st.number_input("Weight (kg)", min_value=1.0, step=0.1)
        height = st.number_input("Height (cm)", min_value=1.0, step=0.1)
        
        if st.button("Calculate My BMI"):
            height_m = height / 100
            bmi = weight / (height_m ** 2)
            st.success(f"**Your BMI is: {round(bmi, 2)}**")
            if bmi < 18.5: st.warning("Category: Underweight - Time to bulk up!")
            elif 18.5 <= bmi < 25: st.info("Category: Normal Weight - Keep crushing it!")
            else: st.error("Category: Overweight - Let's get to work!")
        st.markdown("</div>", unsafe_allow_html=True)


# ==========================================
# 2. MEMBERSHIP PLANS
# ==========================================
elif page == "Membership Plans":
    st.image("https://images.unsplash.com/photo-1571019614242-c5c5dee9f50b?q=80&w=1470&auto=format&fit=crop", use_container_width=True)
    st.markdown("<h1 style='text-align: center; font-size: 3.5rem; margin-top: 20px;'>CHOOSE YOUR WEAPON</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #FFCC00; font-weight: 900; letter-spacing: 2px;'>NO CONTRACTS. JUST RESULTS.</p><br>", unsafe_allow_html=True)
    
    p1, p2, p3 = st.columns(3)
    
    with p1:
        st.markdown("""
        <div class="custom-card">
            <h3>1 MONTH</h3>
            <h2>₹1000</h2>
            <p style='color: #aaa;'>Full gym access<br>Standard equipment<br>Locker room</p>
        </div>
        """, unsafe_allow_html=True)
        
    with p2:
        st.markdown("""
        <div class="custom-card" style="border-top: 5px solid #ffffff; transform: scale(1.05);">
            <h3 style="color: #ffffff;">3 MONTHS</h3>
            <h2>₹2000</h2>
            <p style='color: #aaa;'>Full gym access<br>Diet consultation<br><strong style='color:#FFCC00;'>Save ₹1000!</strong></p>
        </div>
        """, unsafe_allow_html=True)
        
    with p3:
        st.markdown("""
        <div class="custom-card">
            <h3>1 YEAR</h3>
            <h2>₹5000</h2>
            <p style='color: #aaa;'>Access during gym timings<br>Personal training prep<br><strong style='color:#FFCC00;'>Best Value!</strong></p>
        </div>
        """, unsafe_allow_html=True)


# ==========================================
# 3. MEMBER PORTAL (REVERTED TO CLEAN LAYOUT)
# ==========================================
elif page == "Member Portal":
    st.image("https://images.unsplash.com/photo-1558691015-33cbabc4c277?q=80&w=1470&auto=format&fit=crop", use_container_width=True)
    
    st.markdown("<h1 style='text-align: center; font-size: 3.5rem; margin-top: 20px;'>MEMBER PORTAL</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #FFCC00; font-weight: 900; font-size: 1.2rem; letter-spacing: 2px;'>ACCESS YOUR PROFILE</p><br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<div class='info-box'>", unsafe_allow_html=True)
        member_id = st.text_input("ENTER MEMBER ID", placeholder="e.g. R1-001")
        
        if st.button("VERIFY CLEARANCE"):
            df['id'] = df['id'].astype(str).str.replace(r'\.0$', '', regex=True).str.strip().str.upper()
            clean_search_id = str(member_id).strip().upper()
            user_data = df[df['id'] == clean_search_id]
            
            if not user_data.empty:
                name = user_data.iloc[0]['name']
                expiry_str = str(user_data.iloc[0]['expiry_date'])
                
                st.success(f"### WELCOME BACK, {name}!")
                st.info(f"**Membership Expiry Date:** {expiry_str}")
                
                try:
                    expiry = datetime.strptime(expiry_str, '%Y-%m-%d').date()
                    if expiry < date.today():
                        st.error("⚠️ YOUR MEMBERSHIP HAS EXPIRED. PLEASE VISIT THE DESK TO RENEW.")
                    else:
                        st.success("✅ YOUR MEMBERSHIP IS ACTIVE.")
                except:
                    st.warning("Could not verify exact date format.")
            else:
                st.error("❌ MEMBER ID NOT FOUND IN DATABASE.")
        st.markdown("</div>", unsafe_allow_html=True)


# ==========================================
# 4. ADMIN COMMAND CENTER (REALISTIC & STRUCTURED)
# ==========================================
elif page == "Admin Command":
    # Realistic Server/Data Center Image
    st.image("https://images.unsplash.com/photo-1551288049-bebda4e38f71?q=80&w=1470&auto=format&fit=crop", use_container_width=True)
    
    st.markdown("<h1 style='text-align: center; font-size: 3.5rem; margin-top: 20px;'>COMMAND CENTER</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #ff3333; font-weight: 900; letter-spacing: 2px;'>RESTRICTED ACCESS. AUTHORIZED PERSONNEL ONLY.</p>", unsafe_allow_html=True)
    
    # Centered login box to fix the "blank" look
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<div class='admin-box'>", unsafe_allow_html=True)
        st.write("### SYSTEM LOCK")
        password = st.text_input("ENTER OVERRIDE CODE", type="password")
        st.markdown("</div>", unsafe_allow_html=True)
        
        if password == "":
            st.info("System awaiting administrator credentials to view member database and register new clients.")
    
    # Only show the dashboard if the password is correct
    if password == "admin123": 
        st.success("ACCESS GRANTED. WELCOME, COMMANDER.")
        st.write("<br>", unsafe_allow_html=True)
        
        with st.expander("REGISTER NEW MEMBER"):
            new_id = st.text_input("Member ID (e.g., R1-001)")
            new_name = st.text_input("Full Name")
            new_phone = st.text_input("Phone Number")
            new_expiry = st.date_input("Membership Expiry Date")
            
            if st.button("UPLOAD TO DATABASE"):
                existing_ids = df['id'].astype(str).str.replace(r'\.0$', '', regex=True).str.strip().str.upper().tolist()
                clean_new_id = str(new_id).strip().upper()
                
                if clean_new_id in existing_ids:
                    st.error("❌ ID ALREADY EXISTS IN MAINFRAME.")
                else:
                    new_row = pd.DataFrame([{
                        'id': clean_new_id, 
                        'name': new_name, 
                        'phone': new_phone, 
                        'expiry_date': new_expiry.strftime('%Y-%m-%d')
                    }])
                    updated_df = pd.concat([df, new_row], ignore_index=True)
                    
                    conn.update(worksheet="Members", data=updated_df)
                    st.success("✅ UPLOAD SUCCESSFUL! MEMBER ADDED TO CLOUD.")
                    st.rerun()

        st.divider()
        st.write("### ACTIVE RADAR & MEMBER LOGS")
        
        if not df.empty:
            try:
                df['date_obj'] = pd.to_datetime(df['expiry_date']).dt.date
                today = date.today()
                
                expiring_soon = df[(df['date_obj'] <= today + pd.Timedelta(days=7))]
                
                if not expiring_soon.empty:
                    st.markdown(f"<div class='info-box' style='border-left: 5px solid #ff3333;'><h4>⚠️ ALERT: {len(expiring_soon)} MEMBERSHIPS EXPIRING SOON!</h4></div>", unsafe_allow_html=True)
                    st.table(expiring_soon.drop(columns=['date_obj']))
            except:
                pass
            
            st.write("#### COMPLETE MAINFRAME LOG")
            display_df = df.drop(columns=['date_obj']) if 'date_obj' in df.columns else df
            st.dataframe(display_df, use_container_width=True)
            
    elif password != "":
        st.error("❌ ACCESS DENIED. INCORRECT OVERRIDE CODE.")
