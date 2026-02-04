import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image

# --- SYSTEM CONFIGURATION ---
st.set_page_config(layout="wide", page_title="FLATTERN BETA")
ADMIN_PASS = "iLFT1991*"

# Plans and Tier Logic
PLANS = {
    "Pro Garment Manufacturer": {"price": 6500, "quota": 50, "canvas": True},
    "Manufacturer Lite": {"price": 2500, "quota": 30, "canvas": False},
    "Fashion Designer": {"price": 1500, "quota": 20, "canvas": False}
}

# Session Management
if 'auth' not in st.session_state: st.session_state.auth = False
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
                st.session_state.auth = True
                st.rerun()
    st.stop()

# --- SIDEBAR: LOGOS, PLANS & UNIT LOCK ---
with st.sidebar:
    if side_logo: st.image(side_logo, width=120)
    
    st.subheader("Subscription Status")
    # Plan selection for Beta testing
    st.session_state.active_plan = st.selectbox("Current Tier", list(PLANS.keys()))
    current = PLANS[st.session_state.active_plan]
    
    st.metric("Monthly Designs", f"{st.session_state.design_count} / {current['quota']}")
    st.write(f"Price: **${current['price']}**")
    
    st.markdown("---")
    unit = st.radio("Measurement System", ["Inches", "CM"])
    sa_val = st.number_input(f"Seam Allowance ({unit})", value=0.5 if unit == "Inches" else 1.2)
    
    st.markdown("---")
    st.button("Paystack USD Gateway")

# --- MAIN CAD WORKSPACE ---
t1, t2, t3, t4 = st.tabs(["Pattern Generator", "Pro Flat Maker", "Sizing Matrix", "Tech Pack & Export"])

with t1:
    st.header("Point-to-Point Pattern Generator")
    col_in, col_pre = st.columns([1, 2])
    with col_in:
        st.write("### Production Measurements")
        bust = st.number_input("Bust", value=36.0)
        waist = st.number_input("Waist", value=28.0)
        if st.button("Generate Patterns"):
            if st.session_state.design_count < current['quota']:
                st.session_state.design_count += 1
                st.success("Draft processed. Pattern split into individual segments.")
    with col_pre:
        st.write("### Internal & External Highlighting")
        
        st.info("Bold: Exterior Cutting Line | Dashed: Internal Construction")

with t2:
    st.header("Pro Flat Maker (Corrective Drawing)")
    if current['canvas']:
        st.write("Corrective vector engine active for DWG/DWF conversion.")
        
        st_canvas(stroke_width=2, stroke_color="#000", background_color="#FFF", height=500, width=800, drawing_mode="path", key="canvas_v2.1")
    else:
        st.error(f"Flat Maker Locked. {st.session_state.active_plan} supports Parametric Drafting only.")

with t3:
    st.header("Global Sizing & Auto-Grading")
    
    st.table({"US": [4, 6, 8], "UK": [8, 10, 12], "EU": [36, 38, 40], "Bust (In)": [33.5, 34.5, 36]})
    if st.button("Apply Automatic Grading"):
        

with t4:
    st.header("Industrial Export Center")
    c1, c2 = st.columns(2)
    with c1:
        st.write("### Tech Pack (BOM)")
        st.text_input("Fabrication Type")
        st.write(f"Confirmed SA: **{sa_val} {unit}**")
    with c2:
        st.write("### CAD Downloads")
        st.button("Download DWG (Exploded Pattern View)")
        st.button("Download DWF (Engineering View)")
    
    st.markdown("---")
    st.write("### Individual Piece Verification (Page View)")
    page_sel = st.selectbox("Select Page", ["Page 1: Bodice", "Page 2: Sleeves"])
    
    # FIXED INDENTATION LOGIC
    if page_sel == "Page 1: Bodice":
        st.write("Previewing Front and Back panels as separate pattern shapes.")
        
    elif page_sel == "Page 2: Sleeves":
        st.write("Previewing individual sleeve components with grainlines.")
        st.info("Component view active.")
    else:
        pass
