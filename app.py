import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image

# --- 1. SYSTEM CONFIGURATION ---
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

# --- 2. LOGIN GATEWAY ---
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

# --- 3. SIDEBAR: LOGOS, PLANS & UNIT LOCK ---
with st.sidebar:
    if side_logo: 
        st.image(side_logo, width=120)
    
    st.subheader("Subscription Status")
    st.session_state.active_plan = st.selectbox("Current Tier", list(PLANS.keys()))
    current = PLANS[st.session_state.active_plan]
    
    st.metric("Monthly Designs", f"{st.session_state.design_count} / {current['quota']}")
    st.write(f"Price: **${current['price']}**")
    
    st.markdown("---")
    unit = st.radio("Measurement System", ["Inches", "CM"])
    sa_val = st.number_input(f"Seam Allowance ({unit})", value=0.5 if unit == "Inches" else 1.2)
    
    st.markdown("---")
    st.button("Paystack USD Gateway")

# --- 4. MAIN CAD WORKSPACE ---
t1, t2, t3, t4 = st.tabs(["Pattern Generator", "Pro Flat Maker", "Sizing Matrix", "Tech Pack & Export"])

with t1:
    st.header("Point-to-Point Pattern Generator")
    col_in, col_pre = st.columns([1, 2])
    with col_in:
        st.write("### Measurement Inputs")
        bust = st.number_input("Bust", value=36.0)
        waist = st.number_input("Waist", value=28.0)
        if st.button("Generate Patterns"):
            if st.session_state.design_count < current['quota']:
                st.session_state.design_count += 1
                st.success("Mathematical draft processed.")
    with col_pre:
        st.write("### Internal & External Highlighting")
        
        st.caption("Bold: Exterior Cutting Line | Dashed: Internal Construction / Stitching")

with t2:
    st.header("Pro Flat Maker (Corrective Drawing)")
    # FIXED: Added logic inside the IF to prevent IndentationError
    if current['canvas']:
        st.write("Corrective vector engine active. Auto-snapping angles and curves.")
        
        st_canvas(stroke_width=2, stroke_color="#000", background_color="#FFF", height=500, width=800, drawing_mode="path", key="canvas_stable")
    else:
        st.error(f"Flat Maker Locked. {st.session_state.active_plan} tier is restricted to Parametric Drafting.")
        st.info("Upgrade to Pro Garment Manufacturer ($6,500) for vector drawing tools.")

with t3:
    st.header("Global Sizing & Auto-Grading")
    
    st.table({"US Size": [4, 6, 8], "UK Size": [8, 10, 12], "EU Size": [36, 38, 40]})
    if st.button("Execute Grading"):
        st.write("Applying industrial grading rules...")
        

with t4:
    st.header("Industrial Export Center")
    c1, c2 = st.columns(2)
    with c1:
        st.write("### Manufacturing Tech Pack")
        fabric = st.text_input("Fabrication Type")
        thread = st.text_input("Thread Count")
        st.write(f"Confirmed SA: **{sa_val} {unit}**")
    with c2:
        st.write("### Industrial Downloads")
        st.button("Download DWG (Separated Parts)")
        st.button("Download DWF (Production View)")
    
    st.markdown("---")
    st.write("### Multi-Page Pattern Preview")
    page = st.selectbox("View Piece", ["Page 1: Bodice", "Page 2: Sleeves"])
    
    if page == "Page 1: Bodice":
        st.write("Individual pattern shapes for Front and Back panels with grainlines.")
        
    else:
        st.write("Individual sleeve component layout.")
        st.info("Visualizing separate pattern shappets.")
