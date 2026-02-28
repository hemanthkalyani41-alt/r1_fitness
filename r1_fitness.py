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
    
    /* DISABLE IMAGE MAXIMIZE GLOBALLY */
    button[title="View fullscreen"] { display: none !important; }
    [data-testid="stImage"] img { pointer-events: none; }
    
    /* Bold Accents */
    h1, h2, h3, h4 { color: #FFCC00; font-family: 'Arial Black', sans-serif; text-transform: uppercase; text-shadow: 0px 0px 10px rgba(255, 204, 0, 0.2); }
    .blue-glow { color: #00E5FF; text-shadow: 0px 0px 15px rgba(0, 229, 255, 0.6); }
    .red-glow { color: #E60000; text-shadow: 0px 0px 15px rgba(230, 0, 0, 0.6); }
    strong { color: #00E5FF; font-weight: 900; }
    
    /* Realistic 3D Carbon Fibre Pattern for Sidebar & Cards */
    [data-testid="stSidebar"] { 
        background:
            radial-gradient(black 15%, transparent 16%) 0 0,
            radial-gradient(black 15%, transparent 16%) 8px 8px,
            radial-gradient(rgba(255,255,255,.05) 15%, transparent 20%) 0 1px,
            radial-gradient(rgba(255,255,255,.05) 15%, transparent 20%) 8px 9px;
        background-color: #0a0a0a;
        background-size: 16px 16px;
        border-right: 2px solid #00E5FF; 
        box-shadow: 5px 0 25px rgba(0, 229, 255, 0.15); 
    }
    .stRadio div[role="radiogroup"] label { transition: all 0.3s ease-in-out; padding: 10px; border-radius: 8px; background-color: rgba(0,0,0,0.5); margin-bottom: 5px; border: 1px solid #222; }
    .stRadio div[role="radiogroup"] label:hover { transform: scale(1.05) translateX(10px); background-color: #000; color: #00E5FF; border-left: 3px solid #00E5FF; box-shadow: 0 0 10px rgba(0, 229, 255, 0.3); }
    
    /* Standard Custom Cards */
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
    
    /* Quote Banner - Changed to Deep Red */
    .quote-banner {
        background-color: #990000;
        padding: 20px;
        border-radius: 8px;
        text-align: center;
        margin: 30px 0;
        box-shadow: 0 0 20px rgba(153, 0, 0, 0.5);
        border: 1px solid #ff3333;
    }
    .quote-banner h3 { color: #ffffff; margin: 0; font-style: italic; letter-spacing: 1px; text-shadow: none; }
    
    /* 3D Carbon Fibre Product Cards */
    .product-card {
        background:
            radial-gradient(black 15%, transparent 16%) 0 0,
            radial-gradient(black 15%, transparent 16%) 8px 8px,
            radial-gradient(rgba(255,255,255,.05) 15%, transparent 20%) 0 1px,
            radial-gradient(rgba(255,255,255,.05) 15%, transparent 20%) 8px 9px;
        background-color: #151515;
        background-size: 16px 16px;
        padding: 20px;
        border-radius: 12px;
        border: 2px solid #222;
        border-bottom: 4px solid #00E5FF;
        box-shadow: 0 15px 25px rgba(0,0,0,0.9), inset 0 2px 5px rgba(255,255,255,0.05);
        text-align: center;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        margin-bottom: 15px;
    }
    .product-card:hover { 
        transform: translateY(-12px) scale(1.02); 
        box-shadow: 0 20px 35px rgba(0, 229, 255, 0.3), inset 0 2px 5px rgba(255,255,255,0.1); 
        border-bottom: 4px solid #FFCC00;
    }
    
    /* FORCES PERFECT SQUARE ASPECT RATIOS FOR ALL PRO SHOP IMAGES */
    .product-card img { 
        border-radius: 8px; 
        border: 2px solid #00E5FF; 
        box-shadow: 0 5px 15px rgba(0,0,0,0.8); 
        margin-bottom: 15px; 
        width: 100%; 
        aspect-ratio: 1 / 1; 
        object-fit: cover; 
    }
    
    .price-tag { color: #00E5FF; font-size: 24px; font-weight: 900; text-shadow: 0 0 10px rgba(0, 229, 255, 0.4); margin: 5px 0; }
    .weight-tag { color: #FFCC00; font-size: 14px; font-weight: bold; }
    
    /* Animated Pulse Button - Hover turns AGGRESSIVE RED */
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
        background-color: #E60000; 
        color: #ffffff;
        animation: none;
        box-shadow: 0 0 25px rgba(230, 0, 0, 0.8); 
        border: 1px solid #ff9999;
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

# --- SIDEBAR NAVIGATION WITH BOTTOM TEXT LOGO ---
st.sidebar.markdown("<h2 style='text-align: center;' class='blue-glow'>R1 FITNESS</h2>", unsafe_allow_html=True)
page = st.sidebar.radio("SYSTEM MENU", ["Home Base", "Membership Plans", "Pro Shop", "Member Portal", "Admin Command"])

# Pushes the logo to the bottom of the sidebar
st.sidebar.markdown("<br><br><br><br><br><br><br>", unsafe_allow_html=True)
st.sidebar.markdown("""
    <div style='text-align: center;'>
        <h1 style='color: #FFCC00; font-family: "Arial Black", sans-serif; font-size: 4rem; margin-bottom: -25px; text-shadow: 0 0 15px rgba(255, 204, 0, 0.4);'>R1</h1>
        <h2 style='color: #00E5FF; font-family: "Arial Black", sans-serif; font-size: 1.8rem; letter-spacing: 3px; text-shadow: 0 0 15px rgba(0, 229, 255, 0.4);'>FITNESS</h2>
    </div>
""", unsafe_allow_html=True)

# ==========================================
# 1. HOME BASE 
# ==========================================
if page == "Home Base":
    st.markdown("<h1 style='font-size: 4.5rem; text-align: center; margin-bottom: 0;'>R1 <span style='color: #00E5FF;'>FITNESS</span></h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #fff; font-size: 1.5rem; font-style: italic; letter-spacing: 3px;'>FOR GOOD LIFE</p>", unsafe_allow_html=True)
    
    st.image("https://images.unsplash.com/photo-1534438327276-14e5300c3a48?q=80&w=1470&auto=format&fit=crop", use_container_width=True)
    
    # Blood Red Quote Banner
    st.markdown("""
        <div class="quote-banner">
            <h3>"BLOOD, SWEAT, AND RESPECT. FIRST TWO YOU GIVE, LAST ONE YOU EARN."</h3>
        </div>
    """, unsafe_allow_html=True)
    
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
        # RED injected into the VIP tier
        st.markdown("""<div class="custom-card" style="border-top: 5px solid #E60000; box-shadow: 0 4px 15px rgba(230, 0, 0, 0.15);"> <h3 style="color:#E60000;">VIP ELITE</h3><h2>₹35,000</h2><p>1 Year Access<br>Dedicated Trainer<br>Free Monthly Supplements</p></div>""", unsafe_allow_html=True)
        if st.button("BECOME VIP", key="btn4"): st.success("Visit the front desk for VIP Onboarding!")
        
    with p5:
        st.markdown("""<div class="custom-card" style="border-top: 5px solid #ffffff; background-color: #0a0a0a;"> <h3 style="color:#ffffff;">PERSONAL PLAN</h3><h2 style="color: #00E5FF;">₹1,00,000</h2><p>Ultimate 1 Year Access<br><strong style="color:#FFCC00;">Access to Swimming Pool & Garden</strong><br>Exclusive Smoking Zone Lounge</p></div>""", unsafe_allow_html=True)
        if st.button("BECOME A LEGEND", key="btn5"): st.success("Visit the front desk for Ultimate Onboarding!")

# ==========================================
# 3. PRO SHOP 
# ==========================================
elif page == "Pro Shop":
    st.markdown("<h1 style='text-align: center;'>R1 <span style='color: #00E5FF;'>PRO SHOP</span></h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #ccc;'>Fuel your workouts with premium gear and supplements.</p><br>", unsafe_allow_html=True)
    
    s1, s2, s3, s4 = st.columns(4)
    
    with s1:
        st.markdown("""
        <div class="product-card">
            <img src="https://images.unsplash.com/photo-1594882645126-14020914d58d?q=80&w=500&auto=format&fit=crop">
            <h4 style="color: #fff; margin-bottom: 0;">100% WHEY PROTEIN</h4>
            <div class="price-tag">₹1,800 <span class="weight-tag">/ 500g</span></div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("BUY NOW", key="shop1"): st.info("Item added to desk pickup.")
        
    with s2:
        st.markdown("""
        <div class="product-card">
            <img src="https://images.unsplash.com/photo-1550345332-09e3ac987658?q=80&w=500&auto=format&fit=crop">
            <h4 style="color: #fff; margin-bottom: 0;">PRE-WORKOUT ENERGY</h4>
            <div class="price-tag">₹1,200 <span class="weight-tag">/ 300g</span></div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("BUY NOW", key="shop2"): st.info("Item added to desk pickup.")
        
    with s3:
        st.markdown("""
        <div class="product-card">
            <img src="https://images.unsplash.com/photo-1605296867304-46d5465a13f1?q=80&w=500&auto=format&fit=crop">
            <h4 style="color: #fff; margin-bottom: 0;">PURE CREATINE</h4>
            <div class="price-tag">₹800 <span class="weight-tag">/ 250g</span></div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("BUY NOW", key="shop3"): st.info("Item added to desk pickup.")
        
    with s4:
        st.markdown("""
        <div class="product-card">
            <img src="https://images.unsplash.com/photo-1583454110551-21f2fa2afe61?q=80&w=500&auto=format&fit=crop">
            <h4 style="color: #fff; margin-bottom: 0;">LEATHER LIFTING BELT</h4>
            <div class="price-tag">₹1,500 <span class="weight-tag">/ 1 pc</span></div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("BUY NOW", key="shop4"): st.info("Item added to desk pickup.")

# ==========================================
# 4. MEMBER PORTAL 
# ==========================================
elif page == "Member Portal":
    st.markdown("""
    <div style="display: flex; justify-content: center; margin-bottom: 20px;">
        <img src="https://images.unsplash.com/photo-1574680096145-d05b474e2155?q=80&w=1470&auto=format&fit=crop" style="width: 70%; height: 250px; object-fit: cover; border-radius: 12px; pointer-events: none; border: 2px solid #333; box-shadow: 0 10px 20px rgba(0,0,0,0.8);">
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<h1 style='text-align: center; font-size: 3.5rem; margin-top: 10px;'>MEMBER <span style='color: #00E5FF;'>PORTAL</span></h1>", unsafe_allow_html=True)
    
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
# 5. ADMIN COMMAND CENTER 
# ==========================================
elif page == "Admin Command":
    st.markdown("""
    <div style="display: flex; justify-content: center; margin-bottom: 20px;">
        <img src="https://images.unsplash.com/photo-1551288049-bebda4e38f71?q=80&w=1470&auto=format&fit=crop" style="width: 70%; height: 250px; object-fit: cover; border-radius: 12px; pointer-events: none; border: 2px solid #333; box-shadow: 0 10px 20px rgba(0,0,0,0.8);">
    </div>
    """, unsafe_allow_html=True)
    
    # RED injected into the Admin Header
    st.markdown("<h1 style='text-align: center; font-size: 3.5rem; margin-top: 10px;'>COMMAND <span class='red-glow'>CENTER</span></h1>", unsafe_allow_html=True)
    
    # RED injected into the Security Lock text
    st.markdown("<h3 style='text-align: center; color: #E60000;'>🔐 SYSTEM LOCKDOWN</h3>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        password = st.text_input("ENTER OVERRIDE CODE", type="password", label_visibility="collapsed", placeholder="Enter Password")
            
    if password == "admin123": 
        st.success("ACCESS GRANTED. WELCOME, COMMANDER.")
        
        if not df.empty:
            try:
                df['date_obj'] = pd.to_datetime(df['expiry_date'], errors='coerce').dt.date
                today = date.today()
                expired_mask = df['date_obj'] < today
                
                if expired_mask.any():
                    num_deleted = expired_mask.sum()
                    df = df[~expired_mask]
                    conn.update(worksheet="Members", data=df.drop(columns=['date_obj']))
                    st.toast(f"🧹 SYSTEM PURGE: Automatically removed {num_deleted} expired member(s) from database.")
            except:
                pass
        
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
                    if 'date_obj' in updated_df.columns:
                        updated_df = updated_df.drop(columns=['date_obj'])
                    conn.update(worksheet="Members", data=updated_df)
                    st.success("✅ UPLOAD SUCCESSFUL! MEMBER ADDED TO CLOUD.")
                    st.rerun()

        st.divider()
        st.write("### 📡 ACTIVE RADAR & MEMBER LOGS")
        if not df.empty:
            st.write("#### COMPLETE MAINFRAME LOG (ACTIVE MEMBERS ONLY)")
            display_df = df.drop(columns=['date_obj']) if 'date_obj' in df.columns else df
            st.dataframe(display_df, use_container_width=True)
    elif password != "":
        st.error("❌ ACCESS DENIED. INCORRECT OVERRIDE CODE.")
