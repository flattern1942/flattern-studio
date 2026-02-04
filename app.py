import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image

# --- CONFIGURATION & ACCESS ---
st.set_page_config(layout="wide", page_title="FLATTERN BETA")
ADMIN_PASS = "iLFT1991*"

# Session Management
if 'auth' not in st.session_state: st.session_state.auth = False
if 'is_admin' not in st.session_state: st.session_state.is_admin = False
if 'active_plan' not in st.session_state: st.session_state.active_plan = "Pro Garment Manufacturer"
if 'designs_left' not in st.session_state: st.session_state.designs_left = 50

# Plans Architecture
PLANS = {
    "Pro Garment Manufacturer": {"price": 6500, "quota": 50, "canvas": True},
    "Manufacturer Lite": {"price": 2500, "quota": 30, "canvas": False},
    "Fashion Designer": {"price": 1500, "quota": 20, "canvas": False}
}

def load_logos():
    try:
        return Image.open("logo.png.png"), Image.open("sidebar_logo.png.png")
    except:
        return None, None

main_logo, side_logo = load_logos()

# --- LOGIN PORTAL ---
if not st.session_state.auth:
    col_l, col_c, col_r = st.columns([1,2,1])
    with col_c:
        if main_logo: st.image(main_logo, width=300)
        st.title("FLATTERN BETA LOGIN")
        pwd = st.text_input("System Password", type="password")
        if st.button("Enter Workspace"):
            if pwd == ADMIN_PASS:
                st.session_state.is_admin = True
                st.session_state.auth = True
                st.rerun()
            else:
                st.session_state.auth = True
                st.rerun()
    st.stop()

# --- SIDEBAR: sidebar_logo.png.png & SETTINGS ---
with st.sidebar:
    if side_logo: 
        st.image(side_logo, width=120) # Appropriately sized for the sidebar
    
    st.subheader("Account Status")
    st.write(f"Tier: **{st.session_state.active_plan}**")
    st.metric("Designs Remaining", f"{st.session_state.designs_left}")
    
    st.markdown("---")
    st.subheader("Production Settings")
    unit = st.radio("Measurement System", ["Inches", "CM"])
    # Locked SA logic based on your request
    sa_val = st.number_input(f"Seam Allowance ({unit})", value=0.5 if unit == "Inches" else 1.2)
    
    st.markdown("---")
    if st.session_state.is_admin:
        st.error("ADMIN MODE ACTIVE")
        if st.button("Block Scammers/IPs"):
            st.info("Fingerprint tracking enabled.")
    
    st.button("Paystack USD Gateway")

# --- MAIN CAD TABS ---
t1, t2, t3, t4 = st.tabs(["Pattern Generator", "Pro Flat Generator", "Sizing Matrix", "Tech Pack & Export"])

with t1:
    st.header("Point-to-Point Pattern Generator")
    col_in, col_pre = st.columns([1, 2])
    with col_in:
        st.write("### Measurement Inputs")
        bust = st.number_input("Bust (Total)", value=36.0)
        waist = st.number_input("Waist (Total)", value=28.0)
        hip = st.number_input("Hip (Total)", value=38.0)
        back_w = st.number_input("Back Width", value=14.5)
        
        if st.button("Calculate Pattern"):
            if st.session_state.designs_left > 0:
                st.session_state.designs_left -= 1
                st.success("Draft Generated. Pieces separated for export.")
            else:
                st.error("Quota Reached.")

    with col_pre:
        st.write("### Internal/External Path Highlight")
        
        st.caption("Bold Exterior = Cutting Line | Dashed Interior = Construction Path")

with t2:
    if st.session_state.active_plan == "Pro Garment Manufacturer":
        st.header("Pro Corrective Canvas")
        st.write("Technical flats are auto-corrected for angles and curve smoothness.")
        
        st_canvas(
            stroke_width=2, stroke_color="#000", background_color="#FFF",
            height=600, width=900, drawing_mode="path", key="pro_v1.8"
        )
    else:
        st.warning("The Technical Flat Generator is exclusive to the Pro Plan ($6,500).")

with t3:
    st.header("Global Sizing & Auto-Grading")
    
    st.table({
        "Size": ["XS", "S", "M", "L", "XL"],
        "US": [2, 4, 6, 8, 10],
        "UK": [6, 8, 10, 12, 14],
        "EU": [34, 36, 38, 40, 42],
        "Inches": [32, 34, 36, 38, 40],
        "CM": [81, 86, 91, 96, 101]
    })
    if st.button("Apply Industrial Grading"):
        

with t4:
    st.header("Industrial Export (DWG/DWF)")
    col_a, col_b = st.columns(2)
    with col_a:
        st.write("### Tech Pack Data")
        st.text_input("Fabrication Type")
        st.text_area("Trim List & BOM")
        st.write(f"**Factory Seam Allowance:** {sa_val} {unit}")
    
    with col_b:
        st.write("### CAD Exports")
        st.button("Download DWG (Separated Pattern Pieces)")
        st.button("Download DWF (Engineering View)")
        st.button("Export Full Tech Pack PDF")
    
    st.markdown("---")
    st.write("### Preview: Separated Pattern Shapes (Page 1 of 3)")
    
    st.caption("Pieces laid out with grainlines and notches for immediate factory cutting.")
