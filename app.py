import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import pandas as pd

# --- CONFIG & SECURITY ---
st.set_page_config(layout="wide", page_title="FLATTERN BETA")

# Admin Password Lock
ADMIN_PASS = "iLFT1991*"

# Initialize Session State
if 'auth' not in st.session_state: st.session_state.auth = False
if 'is_admin' not in st.session_state: st.session_state.is_admin = False
if 'designs_left' not in st.session_state: st.session_state.designs_left = 50
if 'user_plan' not in st.session_state: st.session_state.user_plan = "Pro Garment Manufacturer"
if 'fingerprint' not in st.session_state: st.session_state.fingerprint = "USR_882x_991"

def load_logo():
    try:
        return Image.open("logo.png.png")
    except:
        return None

logo = load_logo()

# --- LOGIN & ADMIN PORTAL ---
if not st.session_state.auth:
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if logo: st.image(logo, width=300)
        st.title("FLATTERN BETA LOGIN")
        user = st.text_input("Username")
        pwd = st.text_input("Password", type="password")
        if st.button("Access System"):
            if pwd == ADMIN_PASS:
                st.session_state.is_admin = True
                st.session_state.auth = True
                st.rerun()
            else:
                st.session_state.auth = True
                st.rerun()
    st.stop()

# --- ADMIN DASHBOARD ---
if st.session_state.is_admin:
    with st.expander("ADMIN CONTROL PANEL - MASTER ACCESS"):
        st.write("### Active Subscriptions and Payments")
        admin_data = {
            "User ID": ["USR_001", "USR_002", "USR_003"],
            "Fingerprint": ["FX_991", "FX_882", "FX_773"],
            "Plan": ["Pro ($6,500)", "Lite ($2,500)", "Designer ($1,500)"],
            "Status": ["Paid", "Overdue", "Paid"]
        }
        st.table(admin_data)
        st.button("Block Fingerprint / Prevent URL Re-entry")

# --- SIDEBAR CONTROLS ---
with st.sidebar:
    if logo: st.image(logo, width=150)
    st.write(f"**Current Tier:** {st.session_state.user_plan}")
    st.metric("Design Quota Remaining", f"{st.session_state.designs_left}")
    st.markdown("---")
    
    unit = st.radio("System Measurement Units", ["Inches", "CM"])
    sa_input = st.number_input(f"Manual Seam Allowance ({unit})", value=0.5 if unit=="Inches" else 1.2)
    
    st.markdown("---")
    st.button("Paystack USD Secure Gateway")

# --- MAIN INTERFACE TABS ---
t1, t2, t3, t4 = st.tabs(["Parametric CAD Engine", "Pro Vector Canvas", "Global Size Matrix", "Tech Pack and Export"])

with t1:
    st.subheader("Point-to-Point Measurement Input")
    col_l, col_r = st.columns([1, 2])
    with col_l:
        st.write("### Pattern Dimensions")
        bust = st.number_input("Bust Circumference", value=36.0)
        waist = st.number_input("Waist Circumference", value=28.0)
        hip = st.number_input("Hip Circumference", value=38.0)
        shoulder = st.number_input("Shoulder Width", value=15.0)
        back_len = st.number_input("Full Back Length", value=16.0)
        
        if st.button("Calculate and Generate Pattern"):
            if st.session_state.designs_left > 0:
                st.session_state.designs_left -= 1
                st.success("Mathematical block generated and saved to quota.")
            else:
                st.error("Quota exhausted. Please renew subscription.")
    
    with col_r:
        
        st.write("### Internal and External Path Preview")
        st.caption("Highlighting internal construction lines and external cutting paths.")
        st.info("Pattern split into separate segments for individual cutting.")

with t2:
    if st.session_state.user_plan == "Pro Garment Manufacturer":
        st.subheader("Pro Canvas - Vector Correction Engine")
        st.write("Freehand drawing for technical flats. System will auto-correct arcs and angles.")
        st_canvas(
            stroke_width=2, stroke_color="#000000", background_color="#FFFFFF",
            height=600, width=900, drawing_mode="path", key="pro_canvas_v1"
        )
    else:
        st.warning("The Freehand Drawing Canvas is reserved for Pro users ($6,500). Please upgrade.")

with t3:
    st.subheader("Global Size Chart and Grading Logic")
    
    matrix = {
        "Size": ["XS", "S", "M", "L", "XL"],
        "US": [2, 4, 6, 8, 10],
        "UK": [6, 8, 10, 12, 14],
        "EU": [34, 36, 38, 40, 42],
        "Bust (Inches)": [32, 34, 36, 38, 40],
        "Bust (CM)": [81, 86, 91, 96, 101]
    }
    st.table(matrix)
    if st.button("Apply Automatic Industrial Grading"):
        st.info("Generating nested grade rules for DWG export.")
        

with t4:
    st.subheader("Industrial Tech Pack and CAD Export")
    col_a, col_b = st.columns(2)
    with col_a:
        st.write("### Production Specifications")
        st.text_input("Fabrication Type")
        st.text_input("Thread / Construction Spec")
        st.text_area("Bill of Materials (BOM) / Trim List")
        st.write(f"Confirmed Seam Allowance: {sa_input} {unit}")
    
    with col_b:
        st.write("### Export Controls")
        st.checkbox("Include Grainlines", value=True)
        st.checkbox("Force DWG Compatibility", value=True)
        st.button("Download DWG Pattern File")
        st.button("Download DWF Tech File")
        st.button("Generate Tech Pack PDF")
    
    st.markdown("---")
    st.write("### Individual Pattern Pieces Preview")
    # Multi-page preview simulation
    st.write("Page 1: Front and Back Panels")
    
    if st.button("Next Page (Sleeves and Facings)"):
        st.write("Page 2: Component Breakdown")
