import streamlit as st
import pandas as pd
from datetime import datetime, date
from streamlit_gsheets import GSheetsConnection

# --- APP STYLING & CONFIG ---
st.set_page_config(page_title="R1 Fitness", layout="wide")

st.markdown("""
    <style>
    /* Realistic Industrial Striped Background */
    .stApp { 
        background-color: #050505;
        background-image: repeating-linear-gradient(
            -45deg,
            #050505,
            #050505 20px,
            rgba(255, 204, 0, 0.05) 20px,
            rgba(255, 204, 0, 0.05) 22px,
            rgba(0, 229, 255, 0.05) 22px,
            rgba(0, 229, 255, 0.05) 24px
        );
        color: #ffffff; 
    }
    
    /* Bold Accents */
    h1, h2, h3, h4 { color: #FFCC00; font-family: 'Arial Black', sans-serif; text-transform: uppercase; text-shadow: 0px 0px 10px rgba(255, 204, 0, 0.2); }
    .blue-glow { color: #00E5FF; text-shadow: 0px 0px 15px rgba(0, 229, 255, 0.6); }
    strong { color: #00E5FF; font-weight: 900; }
    
    /* Sidebar Menu Animation */
    [data-testid="stSidebar"] { 
        background-color: rgba(5, 5, 5, 0.95);
        border-right: 2px solid #00E5FF; 
        box-shadow: 5px 0 15px rgba(0, 229, 255, 0.1); 
    }
    .stRadio div[role="radiogroup"] label { transition: all 0.3s ease-in-out; padding: 10px; border-radius: 8px; }
    .stRadio div[role="radiogroup"] label:hover { transform: scale(1.05) translateX(10px); background-color: #111; color: #00E5FF; border-left: 3px solid #00E5FF; }
    
    /* Custom Cards */
    .custom-card {
        background-color: #111111;
        padding: 25px;
        border-radius: 10px;
        border-top: 5px solid #00E5FF;
        box-shadow: 0 4px 15px rgba(0, 229, 255, 0.15);
        margin-bottom: 20px;
        text-align: center;
        transition: transform 0.3s ease;
    }
    .custom-card:hover { transform: translateY(-10px); box-shadow: 0 8px 25px rgba(0, 229, 255, 0.4); }
    .custom-card h3 { color: #00E5FF; margin-bottom: 10px; font-size: 24px;}
    .custom-card h2 { color: #ffffff; margin-bottom: 10px; font-size: 32px;}
    
    /* Animated Pulse Button */
    .stButton>button { 
        background-color: #FFCC00; 
        color: #000000; 
        font-weight: 900; 
        font-size: 16px;
        letter-spacing: 1px;
        border-radius: 8px; 
        border: none; 
        width: 100%;
        transition: 0.3s;
        text-transform: uppercase;
        animation: pulse-yellow 2s infinite;
    }
    .stButton>button:hover { 
        background-color: #00E5FF; 
        color: #000000;
        animation: none;
        box-shadow: 0 0 20px rgba(0, 229, 255, 0.8); 
    }
    
    @keyframes pulse-yellow {
        0% { box-shadow: 0 0 0 0 rgba(255, 204, 0, 0.7); }
        70% { box-shadow: 0 0 0 10px rgba(255, 204, 0, 0); }
        100% { box-shadow: 0 0 0 0 rgba(255, 204, 0, 0); }
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
st.sidebar.markdown("<h2 style='text-align: center;' class='blue-glow'>R1 FITNESS</h2>", unsafe_allow_html=True)
page = st.sidebar.radio("SYSTEM MENU", ["Home Base", "Membership Plans", "Pro Shop", "Member Portal", "Admin Command"])

# ==========================================
# 1. HOME BASE 
# ==========================================
if page == "Home Base":
    st.markdown("<h1 style='font-size: 4.5rem; text-align: center; margin-bottom: 0;'>R1 <span style='color: #00E5FF;'>FITNESS</span></h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #fff; font-size: 1.5rem; font-style: italic; letter-spacing: 3px;'>FOR GOOD LIFE</p>", unsafe_allow_html=True)
    
    st.image("https://images.unsplash.com/photo-1534438327276-14e5300c3a48?q=80&w=1470&auto=format&fit=crop", use_container_width=True)
    
    col_rules, col_bmi = st.columns([1.2, 1])
    
    with col_rules:
        st.write("### 🕒 GYM TIMINGS")
        st.markdown("""
        <div style="background-color: #111; border-left: 5px solid #00E5FF; padding: 20px; margin-bottom: 15px; text-align: center; border-radius: 8px;">
            <h2 style="color: #ffffff; margin: 0; font-size: 2.5rem;">09:00 - 12:00</h2>
            <p style="color: #00E5FF; font-weight: bold; margin: 0; letter-spacing: 2px;">OPEN EVERY DAY</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("### 📜 RULES OF THE IRON")
        st.markdown("""
        <ul style="color: #ccc; font-size: 1.1rem; line-height: 1.8; background-color: rgba(17, 17, 17, 0.8); padding: 20px 40px; border-radius: 8px;">
            <li><strong style="color: #FFCC00;">NO SMOKING:</strong> Strictly prohibited. Keep the air clean.</li>
            <li><strong style="color: #FFCC00;">HYDRATION:</strong> Unlimited clean drinking water provided.</li>
            <li><strong style="color: #FFCC00;">LOCKER ROOMS:</strong> Secure rooms provided to change clothes.</li>
        </ul>
        """, unsafe_allow_html=True)

    with col_bmi:
        st.image("https://images.unsplash.com/photo-1581009146145-b5ef050c2e1e?q=80&w=1470&auto=format&fit=crop", use_container_width=True)
        st.markdown("<div style='background-color: rgba(17,17,17,0.8); padding: 20px; border-radius: 8px; margin-top: 15px;'>", unsafe_allow_html=True)
        st.markdown("<h4 style='color: #00E5FF; text-align: center;'>BMI CALCULATOR</h4>", unsafe_allow_html=True)
        weight = st.number_input("Weight (kg)", min_value=1.0, step=0.1)
        height = st.number_input("Height (cm)", min_value=1.0, step=0.1)
        
        if st.button("CALCULATE"):
            height_m = height / 100
            bmi = weight / (height_m ** 2)
            st.success(f"**Your BMI is: {round(bmi, 2)}**")
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# 2. MEMBERSHIP PLANS
# ==========================================
elif page == "Membership Plans":
    st.markdown("<h1 style='text-align: center; font-size: 3.5rem;'>CHOOSE YOUR <span style='color: #00E5FF;'>WEAPON</span></h1><br>", unsafe_allow_html=True)
    
    st.write("### 🔥 STANDARD TIERS")
    p1, p2, p3 = st.columns(3)
    
    with p1:
        st.markdown("""<div class="custom-card"><h3>1 MONTH</h3><h2>₹1000</h2><p>Full gym access<br>Standard equipment</p></div>""", unsafe_allow_html=True)
        if st.button("JOIN NOW", key="btn1"): st.success("Visit the front desk to activate your 1-Month Plan!")
        
    with p2:
        st.markdown("""<div class="custom-card"><h3>3 MONTHS</h3><h2>₹2000</h2><p>Full gym access<br>Diet consultation</p></div>""", unsafe_allow_html=True)
        if st.button("JOIN NOW", key="btn2"): st.success("Visit the front desk to activate your 3-Month Plan!")
        
    with p3:
        st.markdown("""<div class="custom-card"><h3>1 YEAR</h3><h2>₹5000</h2><p>Personal training prep<br><strong>Best Value!</strong></p></div>""", unsafe_allow_html=True)
        if st.button("JOIN NOW", key="btn3"): st.success("Visit the front desk to activate your 1-Year Plan!")
        
    st.divider()
    st.write("### 💎 LUXURY & ELITE TIERS")
    p4, p5 = st.columns(2)
    
    with p4:
        st.markdown("""<div class="custom-card" style="border-top: 5px solid #FFCC00;"> <h3 style="color:#FFCC00;">VIP ELITE</h3><h2>₹35,000</h2><p>1 Year Access<br>Dedicated Trainer<br>Free Monthly Supplements</p></div>""", unsafe_allow_html=True)
        if st.button("BECOME VIP", key="btn4"): st.success("Visit the front desk for VIP Onboarding!")
        
    with p5:
        st.markdown("""<div class="custom-card" style="border-top: 5px solid #ffffff; background-color: #0a0a0a;"> <h3 style="color:#ffffff;">PERSONAL PLAN</h3><h2 style="color: #00E5FF;">₹1,00,000</h2><p>Ultimate 1 Year Access<br><strong style="color:#FFCC00;">Access to Swimming Pool & Garden</strong><br>Exclusive Smoking Zone Lounge</p></div>""", unsafe_allow_html=True)
        if st.button("BECOME A LEGEND", key="btn5"): st.success("Visit the front desk for Ultimate Onboarding!")

# ==========================================
# 3. PRO SHOP (SUPPLEMENTS & GEAR)
# ==========================================
elif page == "Pro Shop":
    st.markdown("<h1 style='text-align: center;'>R1 <span style='color: #00E5FF;'>PRO SHOP</span></h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #ccc;'>Fuel your workouts with premium gear and supplements.</p><br>", unsafe_allow_html=True)
    
    s1, s2, s3, s4 = st.columns(4)
    
    with s1:
        st.image("https://images.unsplash.com/photo-1594882645126-14020914d58d?q=80&w=500&auto=format&fit=crop", use_container_width=True)
        st.markdown("<h4 style='text-align:center;'>100% WHEY PROTEIN</h4><p style='text-align:center; color:#00E5FF; font-size:20px; font-weight:bold;'>₹6,500</p>", unsafe_allow_html=True)
        if st.button("BUY NOW", key="shop1"): st.info("Item added to desk pickup.")
        
    with s2:
        st.image("https://images.unsplash.com/photo-1550345332-09e3ac987658?q=80&w=500&auto=format&fit=crop", use_container_width=True)
        st.markdown("<h4 style='text-align:center;'>PRE-WORKOUT</h4><p style='text-align:center; color:#00E5FF; font-size:20px; font-weight:bold;'>₹2,200</p>", unsafe_allow_html=True)
        if st.button("BUY NOW", key="shop2"): st.info("Item added to desk pickup.")
        
    with s3:
        st.image("https://images.unsplash.com/photo-1605296867304-46d5465a13f1?q=80&w=500&auto=format&fit=crop", use_container_width=True)
        st.markdown("<h4 style='text-align:center;'>PURE CREATINE</h4><p style='text-align:center; color:#00E5FF; font-size:20px; font-weight:bold;'>₹1,500</p>", unsafe_allow_html=True)
        if st.button("BUY NOW", key="shop3"): st.info("Item added to desk pickup.")
        
    with s4:
        st.image("https://images.unsplash.com/photo-1583454110551-21f2fa2afe61?q=80&w=500&auto=format&fit=crop", use_container_width=True)
        st.markdown("<h4 style='text-align:center;'>LIFTING BELT</h4><p style='text-align:center; color:#00E5FF; font-size:20px; font-weight:bold;'>₹1,800</p>", unsafe_allow_html=True)
        if st.button("BUY NOW", key="shop4"): st.info("Item added to desk pickup.")

# ==========================================
# 4. MEMBER PORTAL 
# ==========================================
elif page == "Member Portal":
    st.image("https://images.unsplash.com/photo-1574680096145-d05b474e2155?q=80&w=1470&auto=format&fit=crop", use_container_width=True)
    st.markdown("<h1 style='text-align: center; font-size: 3.5rem; margin-top: 20px;'>MEMBER <span style='color: #00E5FF;'>PORTAL</span></h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.write("---")
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
        st.write("---")

# ==========================================
# 5. ADMIN COMMAND CENTER (RESTORED TO ADVANCED)
# ==========================================
elif page == "Admin Command":
    st.image("https://images.unsplash.com/photo-1551288049-bebda4e38f71?q=80&w=1470&auto=format&fit=crop", use_container_width=True)
    st.markdown("<h1 style='text-align: center; font-size: 3.5rem; margin-top: 20px;'>COMMAND <span style='color: #00E5FF;'>CENTER</span></h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<div style='background-color:#0a0000; border: 1px solid #00E5FF; padding:30px; border-radius:10px; text-align:center; margin-bottom: 20px;'>", unsafe_allow_html=True)
        st.write("### 🔐 SYSTEM LOCK")
        password = st.text_input("ENTER OVERRIDE CODE", type="password")
        st.markdown("</div>", unsafe_allow_html=True)
        
        if password == "":
            st.info("System awaiting administrator credentials to view database and register clients.")
            
    if password == "admin123": 
        st.success("ACCESS GRANTED. WELCOME, COMMANDER.")
        
        with st.expander("➕ REGISTER NEW MEMBER"):
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
        st.write("### 📡 ACTIVE RADAR & MEMBER LOGS")
        if not df.empty:
            try:
                df['date_obj'] = pd.to_datetime(df['expiry_date']).dt.date
                today = date.today()
                
                expiring_soon = df[(df['date_obj'] <= today + pd.Timedelta(days=7))]
                
                if not expiring_soon.empty:
                    st.error(f"⚠️ ALERT: {len(expiring_soon)} MEMBERSHIPS EXPIRING SOON OR EXPIRED!")
                    st.table(expiring_soon.drop(columns=['date_obj']))
            except:
                pass
            
            st.write("#### COMPLETE MAINFRAME LOG")
            display_df = df.drop(columns=['date_obj']) if 'date_obj' in df.columns else df
            st.dataframe(display_df, use_container_width=True)
    elif password != "":
        st.error("❌ ACCESS DENIED. INCORRECT OVERRIDE CODE.")
