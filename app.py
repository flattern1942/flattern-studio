import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image

# --- 1. SYSTEM CONFIGURATION ---
st.set_page_config(layout="wide", page_title="FLATTERN BETA")
ADMIN_PASS = "iLFT1991*"

PLANS = {
    "Pro Garment Manufacturer": {"price": 6500, "quota": 50, "canvas": True},
    "Manufacturer Lite": {"price": 2500, "quota": 30, "canvas": False},
    "Fashion Designer": {"price": 1500, "quota": 20, "canvas": False}
}

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

# --- 3. SIDEBAR: LOGOS & UNIT LOCK ---
with st.sidebar:
    if side_logo: st.image(side_logo, width=120)
    st.subheader("Subscription")
    st.session_state.active_plan = st.selectbox("Tier", list(PLANS.keys()))
    current = PLANS[st.session_state.active_plan]
    st.metric("Designs Used", f"{st.session_state.design_count} / {current['quota']}")
    
    st.markdown("---")
    unit = st.radio("Units", ["Inches", "CM"])
    sa_val = st.number_input(f"Seam Allowance ({unit})", value=0.5 if unit == "Inches" else 1.2)
    st.button("Paystack USD Gateway")

# --- 4. MAIN WORKSPACE ---
t1, t2, t3, t4 = st.tabs(["Pattern Generator", "Flat Maker / Upload", "Sizing Matrix", "Tech Pack & Export"])

with t1:
    st.header("Point-to-Point Pattern Generator")
    col_in, col_pre = st.columns([1, 2])
    with col_in:
        st.write("### Measurement Drafting")
        bust = st.number_input("Bust", value=36.0)
        waist = st.number_input("Waist", value=28.0)
        if st.button("Generate Patterns"):
            if st.session_state.design_count < current['quota']:
                st.session_state.design_count += 1
                st.success("Draft processed.")
    with col_pre:
        st.write("### Internal & External Highlighting")
        
        st.caption("Bold: Exterior Cutting Path | Dashed: Internal Darts & Construction")

with t2:
    if current['canvas']:
        st.header("Pro Flat Maker (Corrective Vector Engine)")
        st.write("Sketch technical flats. System corrects curves for DWG/DWF conversion.")
        
        
        # COMPONENT ERROR FIX: Forced unique key and specific background to stop JavaScript crash
        st_canvas(
            stroke_width=2,
            stroke_color="#000000",
            background_color="#FFFFFF",
            height=500,
            width=900,
            drawing_mode="path",
            key="pro_canvas_fixed_v2"
        )
    else:
        st.header("Flat Management (Lite/Designer)")
        st.info("Please upload your technical flat sketch to include it in the factory export.")
        uploaded_file = st.file_uploader("Upload Flat (PNG/JPG)", type=["png", "jpg", "jpeg"])
        if uploaded_file:
            st.image(uploaded_file, caption="Attached Technical Flat", width=400)

with t3:
    st.header("Global Sizing & Auto-Grading")
    
    st.table({"US": [4, 6, 8], "UK": [8, 10, 12], "EU": [36, 38, 40]})
    if st.button("Apply Industrial Grading"):
        

with t4:
    st.header("Industrial Export Center")
    c1, c2 = st.columns(2)
    with c1:
        st.write("### Manufacturing Data")
        st.text_input("Fabrication Type")
        st.text_area("Trim List")
        st.write(f"**Factory Seam Allowance:** {sa_val} {unit}")
    with c2:
        st.write("### CAD Exports")
        st.button("Download DWG (Separated Parts)")
        st.button("Download DWF (Production View)")
    
    st.markdown("---")
    st.write("### Individual Piece Verification (Page View)")
    page = st.selectbox("View Piece", ["Page 1: Bodice", "Page 2: Sleeves"])
    
    # FIXED INDENTATION
    if page == "Page 1: Bodice":
        st.write("Previewing separated patterns.")
        
    else:
        st.write("Previewing individual sleeve components.")
        st.info("Ready for DWF export.")
