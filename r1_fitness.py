import streamlit as st
import pandas as pd
from datetime import datetime, date
from streamlit_gsheets import GSheetsConnection

# --- APP STYLING & CONFIG ---
st.set_page_config(page_title="R1 Fitness | Premium Club", layout="wide")

st.markdown("""
    <style>
    /* Premium Luxury Theme - Matte Black, Crisp White, Elegant Gold */
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700;900&display=swap');
    
    .stApp { 
        background-color: #080808; 
        color: #e0e0e0; 
        font-family: 'Montserrat', sans-serif;
    }
    
    /* Clean, Elegant Typography */
    h1, h2, h3, h4 { color: #D4AF37; font-weight: 700; text-transform: uppercase; letter-spacing: 2px; }
    strong { color: #D4AF37; font-weight: 700; }
    
    /* Perfect Carbon Fibre Pattern for Sidebar */
    [data-testid="stSidebar"] { 
        background:
            radial-gradient(black 15%, transparent 16%) 0 0,
            radial-gradient(black 15%, transparent 16%) 8px 8px,
            radial-gradient(rgba(255,255,255,.05) 15%, transparent 20%) 0 1px,
            radial-gradient(rgba(255,255,255,.05) 15%, transparent 20%) 8px 9px;
        background-color: #050505;
        background-size: 16px 16px;
        border-right: 2px solid #D4AF37; 
        box-shadow: 5px 0 25px rgba(212, 175, 55, 0.15); 
    }
    
    /* Energetic Sidebar Menu Hover */
    .stRadio div[role="radiogroup"] label { 
        transition: all 0.3s ease-in-out; 
        padding: 12px; 
        border-radius: 6px; 
        background-color: rgba(0,0,0,0.6); 
        margin-bottom: 5px; 
        border: 1px solid #1a1a1a; 
    }
    .stRadio div[role="radiogroup"] label:hover { 
        transform: scale(1.05) translateX(10px); 
        background-color: #000; 
        color: #D4AF37; 
        border-left: 4px solid #D4AF37; 
        box-shadow: 0 0 15px rgba(212, 175, 55, 0.3); 
    }
    
    /* Elegant Custom Cards */
    .custom-card {
        background-color: #0f0f0f;
        padding: 40px 20px;
        border-radius: 8px;
        border: 1px solid #1a1a1a;
        text-align: center;
        transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease;
        margin-bottom: 20px;
    }
    .custom-card:hover { 
        transform: translateY(-8px); 
        border-color: #D4AF37; 
        box-shadow: 0 10px 25px rgba(212, 175, 55, 0.15);
    }
    .custom-card h3 { color: #ffffff; margin-bottom: 10px; font-size: 20px; font-weight: 400;}
    .custom-card h2 { color: #D4AF37; margin-bottom: 15px; font-size: 36px; font-weight: 900;}
    
    /* Minimalist Pro Shop Cards */
    .product-card {
        background-color: #0f0f0f;
        padding: 20px;
        border-radius: 8px;
        border: 1px solid #1a1a1a;
        text-align: center;
        transition: all 0.3s ease;
        margin-bottom: 15px;
    }
    .product-card:hover { 
        border-color: #D4AF37; 
        transform: translateY(-5px);
        box-shadow: 0 8px 20px rgba(212, 175, 55, 0.2);
    }
    
    /* Perfect Square Product Images */
    .product-card img { 
        border-radius: 4px; 
        margin-bottom: 15px; 
        width: 100%; 
        aspect-ratio: 1 / 1; 
        object-fit: cover; 
    }
    
    .price-tag { color: #ffffff; font-size: 20px; font-weight: 700; margin: 10px 0; }
    .weight-tag { color: #888; font-size: 14px; font-weight: 400; }
    
    /* Energetic Solid Buttons */
    .stButton>button { 
        background-color: #D4AF37; 
        color: #000000; 
        font-weight: 800; 
        font-size: 14px;
        letter-spacing: 2px;
        border-radius: 4px; 
        border: none; 
        width: 100%;
        transition: all 0.3s ease;
        text-transform: uppercase;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
    }
    .stButton>button:hover { 
        background-color: #ffffff; 
        color: #000000;
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(212, 175, 55, 0.6); 
    }
    
    /* Metrics Styling */
    [data-testid="stMetricValue"] { color: #D4AF37; font-weight: 900; }
    
    /* Professional Footer */
    .footer {
        text-align: center;
        padding: 40px 0 20px 0;
        margin-top: 50px;
        border-top: 1px solid #1a1a1a;
        color: #666;
        font-size: 12px;
        letter-spacing: 1px;
    }
    
    /* DISABLE IMAGE MAXIMIZE GLOBALLY */
    button[title="View fullscreen"] { display: none !important; }
    [data-testid="stImage"] img { pointer-events: none; }
    </style>
    """, unsafe_allow_html=True)

# --- DATABASE CONNECTION ---
conn = st.connection("gsheets", type=GSheetsConnection)

try:
    df = conn.read(worksheet="Members", ttl=0)
except:
    df = pd.DataFrame(columns=['id', 'name', 'phone', 'expiry_date'])

# --- SIDEBAR NAVIGATION ---
st.sidebar.markdown("<br>", unsafe_allow_html=True)
page = st.sidebar.radio("", ["Home Base", "Membership Plans", "Pro Shop", "Member Portal", "Admin Command"])

st.sidebar.markdown("<br><br><br><br><br><br><br>", unsafe_allow_html=True)
st.sidebar.markdown("""
    <div style='text-align: center;'>
        <h1 style='color: #D4AF37; font-size: 3.5rem; margin-bottom: -20px; letter-spacing: -2px; text-shadow: 0 0 10px rgba(212,175,55,0.3);'>R1</h1>
        <h2 style='color: #ffffff; font-size: 1.2rem; letter-spacing: 4px; font-weight: 400;'>FITNESS</h2>
    </div>
""", unsafe_allow_html=True)

# ==========================================
# 1. HOME BASE 
# ==========================================
if page == "Home Base":
    st.markdown("<h1 style='font-size: 3.5rem; text-align: center; margin-bottom: 0;'>R1 <span style='color: #ffffff;'>FITNESS</span></h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #888; font-size: 1.2rem; letter-spacing: 4px; font-weight: 400;'>ELEVATE YOUR STANDARD</p><br>", unsafe_allow_html=True)
    
    st.image("https://images.unsplash.com/photo-1534438327276-14e5300c3a48?q=80&w=1470&auto=format&fit=crop", use_container_width=True)
    st.write("---")
    
    col_rules, col_bmi = st.columns([1.2, 1])
    
    with col_rules:
        st.write("### CLUB HOURS")
        st.markdown("""
        <div style="background-color: #0f0f0f; border-left: 3px solid #D4AF37; padding: 25px; margin-bottom: 20px; border-radius: 4px; box-shadow: 0 4px 15px rgba(0,0,0,0.5);">
            <h2 style="color: #ffffff; margin: 0; font-size: 2rem;">09:00 - 12:00</h2>
            <p style="color: #D4AF37; font-weight: 700; margin: 0; letter-spacing: 2px; font-size: 12px;">OPEN SEVEN DAYS A WEEK</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("### CLUB POLICIES")
        st.markdown("""
        <ul style="color: #aaa; font-size: 1rem; line-height: 2;">
            <li><strong style="color: #fff;">SMOKE-FREE ENVIRONMENT:</strong> Strictly enforced for health and safety.</li>
            <li><strong style="color: #fff;">COMPLIMENTARY HYDRATION:</strong> Purified water stations available.</li>
            <li><strong style="color: #fff;">EXECUTIVE LOCKER ROOMS:</strong> Secure, private changing facilities.</li>
        </ul>
        """, unsafe_allow_html=True)

    with col_bmi:
        st.image("https://images.unsplash.com/photo-1581009146145-b5ef050c2e1e?q=80&w=1470&auto=format&fit=crop", use_container_width=True)
        st.markdown("<div style='background-color: #0f0f0f; padding: 30px; border-radius: 4px; margin-top: 15px; border: 1px solid #1a1a1a; box-shadow: 0 4px 15px rgba(0,0,0,0.5);'>", unsafe_allow_html=True)
        st.markdown("<h4 style='color: #fff; text-align: center; font-size: 16px;'>BMI ASSESSMENT</h4><br>", unsafe_allow_html=True)
        weight = st.number_input("Weight (kg)", min_value=1.0, step=0.1)
        height = st.number_input("Height (cm)", min_value=1.0, step=0.1)
        
        if st.button("CALCULATE"):
            height_m = height / 100
            bmi = weight / (height_m ** 2)
            st.success(f"**Your BMI Indicator: {round(bmi, 2)}**")
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# 2. MEMBERSHIP PLANS
# ==========================================
elif page == "Membership Plans":
    st.markdown("<h1 style='text-align: center; font-size: 3rem;'>MEMBERSHIP <span style='color: #ffffff;'>TIERS</span></h1><br>", unsafe_allow_html=True)
    
    p1, p2, p3 = st.columns(3)
    
    with p1:
        st.markdown("""<div class="custom-card"><h3>1 MONTH</h3><h2>₹1,000</h2><p style='color:#888; font-size:14px; line-height: 2;'>Full Club Access<br>Standard Equipment</p></div>""", unsafe_allow_html=True)
        if st.button("INQUIRE NOW", key="btn1"): st.success("Visit the concierge to activate your 1-Month Plan.")
        
    with p2:
        st.markdown("""<div class="custom-card"><h3>3 MONTHS</h3><h2>₹2,000</h2><p style='color:#888; font-size:14px; line-height: 2;'>Full Club Access<br>Nutrition Consultation</p></div>""", unsafe_allow_html=True)
        if st.button("INQUIRE NOW", key="btn2"): st.success("Visit the concierge to activate your 3-Month Plan.")
        
    with p3:
        st.markdown("""<div class="custom-card"><h3>1 YEAR</h3><h2>₹5,000</h2><p style='color:#888; font-size:14px; line-height: 2;'>Full Club Access<br>Personal Training Assessment</p></div>""", unsafe_allow_html=True)
        if st.button("INQUIRE NOW", key="btn3"): st.success("Visit the concierge to activate your 1-Year Plan.")
        
    st.write("---")
    st.write("### ELITE MEMBERSHIPS")
    p4, p5 = st.columns(2)
    
    with p4:
        st.markdown("""<div class="custom-card" style="border-color: #D4AF37;"> <h3 style="color:#D4AF37;">VIP ELITE</h3><h2>₹35,000</h2><p style='color:#888; font-size:14px; line-height: 2;'>1 Year Access<br>Dedicated Personal Trainer<br>Monthly Supplement Allocation</p></div>""", unsafe_allow_html=True)
        if st.button("APPLY FOR VIP", key="btn4"): st.success("Visit the concierge for VIP Onboarding.")
        
    with p5:
        st.markdown("""<div class="custom-card" style="background-color: #D4AF37;"> <h3 style="color:#000;">ULTIMATE PERSONAL</h3><h2 style="color:#000;">₹1,00,000</h2><p style='color:#333; font-size:14px; line-height: 2;'>Ultimate 1 Year Access<br><strong>Swimming Pool & Garden Access</strong><br>Exclusive Lounge Access</p></div>""", unsafe_allow_html=True)
        if st.button("APPLY FOR ULTIMATE", key="btn5"): st.success("Visit the concierge for Ultimate Onboarding.")

# ==========================================
# 3. PRO SHOP 
# ==========================================
elif page == "Pro Shop":
    st.markdown("<h1 style='text-align: center;'>R1 <span style='color: #ffffff;'>BOUTIQUE</span></h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #888; letter-spacing: 2px;'>PREMIUM SUPPLEMENTS & GEAR</p><br>", unsafe_allow_html=True)
    
    s1, s2, s3, s4 = st.columns(4)
    
    with s1:
        st.markdown("""
        <div class="product-card">
            <img src="https://images.unsplash.com/photo-1594882645126-14020914d58d?q=80&w=500&auto=format&fit=crop">
            <h4 style="color: #fff; margin-bottom: 0; font-size: 14px;">WHEY PROTEIN ISOLATE</h4>
            <div class="price-tag">₹1,800 <span class="weight-tag">/ 500g</span></div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("PURCHASE", key="shop1"): st.info("Item held at concierge desk.")
        
    with s2:
        st.markdown("""
        <div class="product-card">
            <img src="https://images.unsplash.com/photo-1550345332-09e3ac987658?q=80&w=500&auto=format&fit=crop">
            <h4 style="color: #fff; margin-bottom: 0; font-size: 14px;">PRE-WORKOUT FORMULA</h4>
            <div class="price-tag">₹1,200 <span class="weight-tag">/ 300g</span></div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("PURCHASE", key="shop2"): st.info("Item held at concierge desk.")
        
    with s3:
        st.markdown("""
        <div class="product-card">
            <img src="https://images.unsplash.com/photo-1605296867304-46d5465a13f1?q=80&w=500&auto=format&fit=crop">
            <h4 style="color: #fff; margin-bottom: 0; font-size: 14px;">MICRONIZED CREATINE</h4>
            <div class="price-tag">₹800 <span class="weight-tag">/ 250g</span></div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("PURCHASE", key="shop3"): st.info("Item held at concierge desk.")
        
    with s4:
        st.markdown("""
        <div class="product-card">
            <img src="https://images.unsplash.com/photo-1583454110551-21f2fa2afe61?q=80&w=500&auto=format&fit=crop">
            <h4 style="color: #fff; margin-bottom: 0; font-size: 14px;">PREMIUM LIFTING BELT</h4>
            <div class="price-tag">₹1,500 <span class="weight-tag">/ 1 pc</span></div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("PURCHASE", key="shop4"): st.info("Item held at concierge desk.")

# ==========================================
# 4. MEMBER PORTAL 
# ==========================================
elif page == "Member Portal":
    st.markdown("""
    <div style="display: flex; justify-content: center; margin-bottom: 30px;">
        <img src="https://images.unsplash.com/photo-1574680096145-d05b474e2155?q=80&w=1470&auto=format&fit=crop" style="width: 80%; height: 300px; object-fit: cover; border-radius: 4px; box-shadow: 0 10px 30px rgba(0,0,0,0.8);">
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<h1 style='text-align: center; font-size: 2.5rem;'>MEMBER <span style='color: #ffffff;'>PORTAL</span></h1><br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<div style='background-color:#0f0f0f; padding:40px; border-radius:8px; border: 1px solid #1a1a1a; box-shadow: 0 10px 25px rgba(0,0,0,0.5);'>", unsafe_allow_html=True)
        member_id = st.text_input("ENTER MEMBER ID", placeholder="e.g. R1-001")
        st.write("<br>", unsafe_allow_html=True)
        
        if st.button("VERIFY IDENTITY"):
            df['id'] = df['id'].astype(str).str.replace(r'\.0$', '', regex=True).str.strip().str.upper()
            clean_search_id = str(member_id).strip().upper()
            user_data = df[df['id'] == clean_search_id]
            
            if not user_data.empty:
                name = user_data.iloc[0]['name']
                expiry_str = str(user_data.iloc[0]['expiry_date'])
                
                st.success(f"### WELCOME, {name.upper()}")
                st.info(f"**Valid Through:** {expiry_str}")
                
                try:
                    expiry = datetime.strptime(expiry_str, '%Y-%m-%d').date()
                    if expiry < date.today():
                        st.error("Membership Expired. Please see concierge.")
                    else:
                        st.success("Status: Active.")
                except:
                    st.warning("Date format error.")
            else:
                st.error("Credential not recognized.")
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# 5. ADMIN COMMAND CENTER 
# ==========================================
elif page == "Admin Command":
    st.markdown("<h1 style='text-align: center; font-size: 2.5rem; margin-top: 20px;'>OPERATIONS <span style='color: #ffffff;'>DASHBOARD</span></h1><br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        password = st.text_input("ADMINISTRATOR PASSWORD", type="password", placeholder="Enter Password")
            
    if password == "admin123": 
        st.success("Authentication successful.")
        st.write("---")
        
        # AUTONOMOUS EXPIRED MEMBER DELETION
        if not df.empty:
            try:
                df['date_obj'] = pd.to_datetime(df['expiry_date'], errors='coerce').dt.date
                today = date.today()
                expired_mask = df['date_obj'] < today
                
                if expired_mask.any():
                    num_deleted = expired_mask.sum()
                    df = df[~expired_mask]
                    conn.update(worksheet="Members", data=df.drop(columns=['date_obj']))
                    st.toast(f"System Routine: Purged {num_deleted} expired accounts.")
            except:
                pass

        # LIVE METRICS DASHBOARD
        st.write("### 📊 REAL-TIME METRICS")
        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric(label="Total Active Members", value=len(df))
        with m2:
            if not df.empty and 'date_obj' in df.columns:
                expiring_7_days = len(df[(df['date_obj'] <= today + pd.Timedelta(days=7))])
                st.metric(label="Expiring in 7 Days", value=expiring_7_days)
            else:
                st.metric(label="Expiring in 7 Days", value=0)
        with m3:
            # EXPORT BUTTON
            if not df.empty:
                csv_data = df.drop(columns=['date_obj']) if 'date_obj' in df.columns else df
                csv = csv_data.to_csv(index=False).encode('utf-8')
                st.markdown("<br>", unsafe_allow_html=True)
                st.download_button(
                    label="📥 EXPORT DATABASE",
                    data=csv,
                    file_name=f"R1_Members_{date.today()}.csv",
                    mime="text/csv",
                )
        st.write("---")

        with st.expander("➕ REGISTER NEW CLIENT"):
            st.markdown("<div style='background-color: #0f0f0f; padding: 20px; border-radius: 4px; border: 1px solid #1a1a1a;'>", unsafe_allow_html=True)
            new_id = st.text_input("Member ID (Must start with 'R1-')")
            new_name = st.text_input("Full Name")
            new_phone = st.text_input("Phone Number (10 Digits)")
            new_expiry = st.date_input("Membership Expiry Date")
            
            if st.button("SAVE TO SECURE CLOUD"):
                clean_new_id = str(new_id).strip().upper()
                clean_phone = str(new_phone).strip()
                existing_ids = df['id'].astype(str).str.replace(r'\.0$', '', regex=True).str.strip().str.upper().tolist()
                
                if not clean_new_id.startswith("R1-"):
                    st.error("Validation Error: Member ID must begin with 'R1-' (e.g., R1-001)")
                elif len(clean_phone) != 10 or not clean_phone.isdigit():
                    st.error("Validation Error: Phone number must be exactly 10 digits.")
                elif clean_new_id in existing_ids:
                    st.error("Validation Error: Member ID already exists in the system.")
                else:
                    new_row = pd.DataFrame([{
                        'id': clean_new_id, 
                        'name': new_name, 
                        'phone': clean_phone, 
                        'expiry_date': new_expiry.strftime('%Y-%m-%d')
                    }])
                    updated_df = pd.concat([df, new_row], ignore_index=True)
                    if 'date_obj' in updated_df.columns:
                        updated_df = updated_df.drop(columns=['date_obj'])
                    conn.update(worksheet="Members", data=updated_df)
                    st.success("Client registered successfully.")
                    st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

        st.write("<br>### 🗄️ CLIENT DIRECTORY", unsafe_allow_html=True)
        if not df.empty:
            display_df = df.drop(columns=['date_obj']) if 'date_obj' in df.columns else df
            st.dataframe(display_df, use_container_width=True)
            
    elif password != "":
        st.error("Authentication failed.")

# --- GLOBAL FOOTER ---
st.markdown("""
    <div class="footer">
        <strong>R1 FITNESS CLUB</strong><br>
        123 Elite Avenue, Fitness District<br>
        support@r1fitness.com | +91 98765 43210<br><br>
        &copy; 2026 R1 Fitness. All Rights Reserved.
    </div>
""", unsafe_allow_html=True)

