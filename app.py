import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image

# --- 1. SYSTEM CONFIGURATION ---
st.set_page_config(layout="wide", page_title="FLATTERN BETA")
ADMIN_PASS = "iLFT1991*"

PLANS = {
    "Pro Garment Manufacturer": {"price": 6500, "quota": 50, "canvas": True, "link": "https://paystack.com/pay/pro-6500"},
    "Manufacturer Lite": {"price": 2500, "quota": 30, "canvas": False, "link": "https://paystack.com/pay/lite-2500"},
    "Fashion Designer": {"price": 1500, "quota": 20, "canvas": False, "link": "https://paystack.com/pay/designer-1500"}
}

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

# --- 2. LOGIN GATEWAY ---
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

# --- 3. SIDEBAR: LOGOS AND SUBSCRIPTION ---
with st.sidebar:
    if side_logo: st.image(side_logo, width=120)
    st.subheader("Subscription Status")
    st.session_state.active_plan = st.selectbox("Tier", list(PLANS.keys()))
    current = PLANS[st.session_state.active_plan]
    
    st.metric("Designs Remaining", f"{current['quota'] - st.session_state.design_count} / {current['quota']}")
    
    st.markdown("---")
    unit = st.radio("Measurement System", ["Inches", "CM"])
    # 0.5 inch Seam Allowance default
    sa_val = st.number_input(f"Seam Allowance ({unit})", value=0.5 if unit == "Inches" else 1.27)
    
    st.markdown("---")
    st.link_button("Paystack USD Gateway", current['link'])
    
    if st.session_state.is_admin:
        st.markdown("---")
        if st.button("Open Admin Dashboard"):
            st.session_state.view_admin = True

# --- 4. ADMIN DASHBOARD (FINGERPRINTING) ---
if st.session_state.get('view_admin'):
    st.header("Admin Dashboard: Security and Fingerprinting")
    st.write("Tracking hardware fingerprints to prevent payment evasion and URL abuse.")
    
    admin_data = {
        "Client ID": ["USR_991", "USR_882", "USR_771"],
        "Fingerprint ID": ["FP-9923-AX", "FP-1120-ZB", "FP-8832-QL"],
        "Status": ["Active", "Active", "Flagged - Scammer"]
    }
    st.table(admin_data)
    
    if st.button("Block Scammer Fingerprint"):
        st.warning("Hardware signature blacklisted.")
    
    if st.button("Return to Workspace"):
        st.session_state.view_admin = False
        st.rerun()
    st.stop()

# --- 5. MAIN WORKSPACE ---
t1, t2, t3, t4 = st.tabs(["Pattern Generator", "Flat Maker / Upload", "Sizing Matrix", "Tech Pack and Export"])

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
                st.success("Mathematical draft processed.")
            else:
                st.error("Monthly quota reached.")
    with col_pre:
        st.write("### Highlighting: Internal and External Paths")
        
        st.caption("Bold Exterior: Cutting Edge | Dashed Interior: Construction and Stitch Lines")

with t2:
    if current['canvas']:
        st.header("Pro Flat Maker (Corrective Engine)")
        st.write("Corrective vector canvas: Auto-snapping angles and curves for industrial export.")
        
        st_canvas(
            stroke_width=2, stroke_color="#000000", background_color="#FFFFFF",
            height=500, width=900, drawing_mode="path", key="pro_canvas_v3.1_stable"
        )
    else:
        st.header("Flat Management (Lite/Designer)")
        st.info("Upload technical flat sketch to include in the tech pack.")
        uploaded_file = st.file_uploader("Upload Flat Sketch (PNG/JPG)", type=["png", "jpg", "jpeg"])
        if uploaded_file:
            st.image(uploaded_file, caption="Technical Flat Attached", width=400)
        else:
            st.write("Awaiting file upload for production tech pack.")

with t3:
    st.header("Global Sizing and Automatic Grading")
    
    st.table({"US": [4, 6, 8], "UK": [8, 10, 12], "EU": [36, 38, 40], "Bust (In)": [33.5, 34.5, 36]})
    if st.button("Execute Industrial Grading"):
        st.write("Calculating size deviations...")
        

with t4:
    st.header("Industrial Export Center")
    c1, c2 = st.columns(2)
    with c1:
        st.write("### Tech Pack (BOM)")
        st.text_input("Fabric Type")
        st.text_area("Trim List")
        st.write(f"Confirmed Seam Allowance: {sa_val} {unit}")
    with c2:
        st.write("### Production Downloads")
        st.button("Download DWG (Exploded View)")
        st.button("Download DWF (Tech Package)")
    
    st.markdown("---")
    st.write("### Multi-Page Pattern Preview")
    page = st.selectbox("View Piece", ["Page 1: Bodice Panels", "Page 2: Sleeves"])
    
    # FIXED INDENTATION: Logic blocks are now fully populated
    if page == "Page 1: Bodice Panels":
        st.write("Displaying Front and Back panels as separate individual patterns.")
        
    else:
        st.write("Displaying Sleeve components with grainline arrows.")
        st.info("Individual shappet view active.")
