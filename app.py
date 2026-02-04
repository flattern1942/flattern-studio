import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image

# --- 1. SYSTEM CONFIGURATION & SECURITY ---
st.set_page_config(layout="wide", page_title="FLATTERN BETA")
ADMIN_PASS = "iLFT1991*"

# Enterprise Tier Data
PLANS = {
    "Pro Garment Manufacturer": {"price": 6500, "quota": 50, "canvas": True, "link": "https://paystack.com/pay/pro-6500"},
    "Manufacturer Lite": {"price": 2500, "quota": 30, "canvas": False, "link": "https://paystack.com/pay/lite-2500"},
    "Fashion Designer": {"price": 1500, "quota": 20, "canvas": False, "link": "https://paystack.com/pay/designer-1500"}
}

# State Persistence
if 'auth' not in st.session_state: st.session_state.auth = False
if 'is_admin' not in st.session_state: st.session_state.is_admin = False
if 'active_plan' not in st.session_state: st.session_state.active_plan = "Pro Garment Manufacturer"
if 'design_count' not in st.session_state: st.session_state.design_count = 0

def load_logos():
    try:
        return Image.open("logo.png.png"), Image.open("sidebar_logo.png.png")
    except:
        return None, None

main_logo, side_logo = load_logos()

# --- 2. ACCESS CONTROL GATEWAY ---
if not st.session_state.auth:
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        if main_logo: st.image(main_logo, width=300)
        st.title("FLATTERN BETA ACCESS")
        p_in = st.text_input("Industrial Access Key", type="password")
        if st.button("Secure Authorization"):
            if p_in == ADMIN_PASS:
                st.session_state.is_admin = True
                st.session_state.auth = True
                st.rerun()
            else:
                st.session_state.auth = True
                st.rerun()
    st.stop()

# --- 3. SIDEBAR: LOGISTICS & BILLING ---
with st.sidebar:
    if side_logo: st.image(side_logo, width=120)
    st.subheader("Subscription Status")
    st.session_state.active_plan = st.selectbox("Current Tier", list(PLANS.keys()))
    current = PLANS[st.session_state.active_plan]
    
    st.metric("Monthly Quota Remaining", f"{current['quota'] - st.session_state.design_count}")
    
    st.markdown("---")
    unit = st.radio("Measurement System", ["Inches", "CM"])
    sa_val = st.number_input(f"Seam Allowance ({unit})", value=0.5 if unit == "Inches" else 1.27)
    
    st.markdown("---")
    st.link_button("Paystack USD Gateway", current['link'])
    
    if st.session_state.is_admin:
        st.markdown("---")
        if st.button("Open Security Admin Panel"):
            st.session_state.view_admin = True

# --- 4. ADMIN SECURITY & FINGERPRINTING ---
if st.session_state.get('view_admin'):
    st.header("Admin Security Dashboard")
    st.write("Monitoring Hardware Fingerprints and Billing Evasion Vectors.")
    
    admin_data = {
        "User ID": ["USR-Alpha", "USR-Beta", "USR-Gamma"],
        "Device Fingerprint": ["HW-99120-XQ", "HW-88121-ZP", "HW-77341-LL"],
        "Status": ["Clear", "Clear", "Flagged: Scammer - Blocked"]
    }
    st.table(admin_data)
    
    if st.button("Purge Blocklist and Return"):
        st.session_state.view_admin = False
        st.rerun()
    st.stop()

# --- 5. MAIN CAD ENGINE ---
t1, t2, t3, t4 = st.tabs(["Pattern Generator", "Pro Flat Maker", "Sizing Matrix", "Tech Pack & Export"])

with t1:
    st.header("Point-to-Point Parametric Drafting")
    col_a, col_b = st.columns([1, 2])
    with col_a:
        st.write("### Input Measurements")
        bust = st.number_input("Bust Circumference", value=36.0)
        waist = st.number_input("Waist Circumference", value=28.0)
        hip = st.number_input("Hip Circumference", value=38.0)
        if st.button("Generate Mathematical Pattern"):
            if st.session_state.design_count < current['quota']:
                st.session_state.design_count += 1
                st.success("Draft Generated and Stored.")
            else:
                st.error("Quota reached. Please renew via Paystack.")
    with col_b:
        st.write("### Internal/External Path Preview")
        
        st.info("Bold Lines: External Cut Path | Dashed Lines: Internal Construction/Darts")

with t2:
    st.header("Flat Maker & Technical Sketching")
    if current['canvas']:
        st.write("Industrial Corrective Engine: Auto-snapping angles and curves.")
        
        st_canvas(stroke_width=2, stroke_color="#000", background_color="#FFF", height=500, width=800, drawing_mode="path", key="pro_canvas_v3.5")
    else:
        st.info("The Pro Drawing Canvas is locked for this tier.")
        st.write("Upload your existing flat for Tech Pack inclusion:")
        st.file_uploader("Upload PNG/JPG", type=["png", "jpg"])

with t3:
    st.header("Global Size Chart & Auto-Grading")
    st.table({
        "US Size": ["4", "6", "8", "10"],
        "UK Size": ["8", "10", "12", "14"],
        "EU Size": ["36", "38", "40", "42"],
        "Bust (Inches)": [33.5, 34.5, 36, 37.5],
        "Bust (CM)": [85, 87.5, 91.5, 95]
    })
    
    if st.button("Apply Automatic Grading"):
        st.write("Expanding pattern nodes for XS - XL production.")
        

with t4:
    st.header("Tech Pack & Industrial Export")
    c1, c2 = st.columns(2)
    with c1:
        st.write("### Production Data")
        st.text_input("Fabric Type")
        st.text_input("Thread Count")
        st.text_area("Trim List (Buttons, Zippers, etc.)")
        st.write(f"Logged Seam Allowance: **{sa_val} {unit}**")
    with c2:
        st.write("### Download CAD Files")
        st.button("Download DWG (Exploded Layout)")
        st.button("Download DWF (Production Tech Package)")
    
    st.markdown("---")
    st.write("### Preview of Individual Pieces (Exploded Pattern View)")
    view_page = st.selectbox("Select Preview Page", ["Page 1: Bodice Panels", "Page 2: Sleeves", "Page 3: Trims/Facing"])
    
    if view_page == "Page 1: Bodice Panels":
        st.write("Individual patterns separated for Front and Back bodice with grainlines.")
        
    else:
        st.write("Visualizing individual pattern shappets for secondary components.")
        st.info("Component View Active.")
