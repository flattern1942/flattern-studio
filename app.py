import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image

# --- SYSTEM CONFIGURATION & SECURITY ---
st.set_page_config(layout="wide", page_title="FLATTERN BETA")
ADMIN_PASS = "iLFT1991*"

# Plans Architecture
PLANS = {
    "Pro Garment Manufacturer": {"price": 6500, "quota": 50, "tools": "Pattern + Flat Maker"},
    "Manufacturer Lite": {"price": 2500, "quota": 30, "tools": "Pattern Only"},
    "Fashion Designer": {"price": 1500, "quota": 20, "tools": "Pattern Only"}
}

# State Management
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

# --- LOGIN GATEWAY ---
if not st.session_state.auth:
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        if main_logo: st.image(main_logo, width=300)
        st.title("FLATTERN BETA ACCESS")
        p_in = st.text_input("System Password", type="password")
        if st.button("Secure Login"):
            if p_in == ADMIN_PASS:
                st.session_state.is_admin = True
                st.session_state.auth = True
                st.rerun()
            else:
                st.session_state.auth = True
                st.rerun()
    st.stop()

# --- SIDEBAR: PLANS, LOGO & SETTINGS ---
with st.sidebar:
    if side_logo: st.image(side_logo, width=120)
    
    st.subheader("Subscription Plans")
    # Allow user to choose plan for testing/switching
    choice = st.selectbox("Current Plan", list(PLANS.keys()), index=0)
    st.session_state.active_plan = choice
    
    current = PLANS[st.session_state.active_plan]
    st.info(f"Price: ${current['price']}/mo\nTools: {current['tools']}")
    
    st.metric("Designs Used", f"{st.session_state.design_count} / {current['quota']}")
    
    st.markdown("---")
    unit = st.radio("Measurement System", ["Inches", "CM"])
    sa_val = st.number_input(f"Your Seam Allowance ({unit})", value=0.5 if unit == "Inches" else 1.2)
    
    st.markdown("---")
    st.button("Paystack USD Gateway")
    
    if st.session_state.is_admin:
        st.error("Admin: iLFT1991* Mode")

# --- MAIN WORKSPACE ---
t1, t2, t3, t4 = st.tabs(["Pattern Generator", "Pro Flat Maker", "Sizing Matrix", "Tech Pack & Export"])

with t1:
    st.header("Point-to-Point Pattern Generator")
    col_a, col_b = st.columns([1, 2])
    with col_a:
        st.write("### Measure to Draft")
        bust = st.number_input("Bust Circumference", value=36.0)
        waist = st.number_input("Waist Circumference", value=28.0)
        hip = st.number_input("Hip Circumference", value=38.0)
        if st.button("Generate Patterns"):
            if st.session_state.design_count < current['quota']:
                st.session_state.design_count += 1
                st.success("Pattern Drafted and Quota Updated.")
            else:
                st.error("Quota Reached. Upgrade or renew plan.")
    with col_b:
        st.write("### Exploded View (Internal & External Highlighting)")
        
        st.caption("Individual shappets separated with grainlines and construction notches.")

with t2:
    st.header("Flat Generator (Corrective Drawing)")
    if st.session_state.active_plan == "Pro Garment Manufacturer":
        st.write("System correcting hand-drawn paths for CAD compatibility...")
        st_canvas(stroke_width=2, stroke_color="#000", background_color="#FFF", height=500, width=800, drawing_mode="path", key="v2_canvas")
    else:
        st.error(f"Flat Generator is locked. The {st.session_state.active_plan} tier only supports Parametric Drafting.")
        st.info("Upgrade to Pro Garment Manufacturer ($6,500) for freehand corrective curves.")

with t3:
    st.header("Global Sizing & Auto-Grading")
    
    st.table({
        "US Size": ["2", "4", "6", "8", "10"],
        "UK Size": ["6", "8", "10", "12", "14"],
        "Inches": [32, 33.5, 34.5, 36, 37.5],
        "CM": [81, 85, 87.5, 91.5, 95]
    })
    if st.button("Apply Automatic Grading"):
        

with t4:
    st.header("Industrial Export Center")
    c1, c2 = st.columns(2)
    with c1:
        st.write("### Manufacturing Tech Pack")
        st.text_input("Fabric Type")
        st.text_area("Trim List (BOM)")
        st.write(f"Confirmed SA: **{sa_val} {unit}**")
    with c2:
        st.write("### CAD Downloads")
        st.button("Download DWG (Exploded Pattern)")
        st.button("Download DWF (Production Tech)")
    
    st.markdown("---")
    st.write("### Multi-Page Individual Piece Verification")
    page = st.selectbox("Select Page", ["Page 1: Bodice", "Page 2: Sleeves", "Page 3: Components"])
    
    if page == "Page 1: Bodice":
        st.write("Displaying Front and Back patterns as separate shapes.")
        
    else:
        st.info("Visualizing component breakdowns...")
