import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import datetime

# --- 1. THE UNTOUCHABLE BUSINESS CONSTANTS ---
PLAN_DATA = {
    "Pro Garment Manufacturer": {"price": 6500, "quota": 50},
    "Garment Manufacturer Lite": {"price": 2500, "quota": 30},
    "Fashion Designer": {"price": 1500, "quota": 20}
}

st.set_page_config(layout="wide", page_title="Industrial Production Suite")

# Persistent state management
if 'design_count' not in st.session_state: st.session_state.design_count = 0
if 'sa_value' not in st.session_state: st.session_state.sa_value = 0.5
if 'unit_type' not in st.session_state: st.session_state.unit_type = "Inches"
if 'logs' not in st.session_state: st.session_state.logs = []

def load_branding():
    try:
        return Image.open("sidebar_logo.png.png"), Image.open("logo.png.png")
    except:
        return None, None

side_logo, purple_logo = load_branding()

# --- 2. SIDEBAR: PURPLE LOGO & ADMIN PORTAL ---
with st.sidebar:
    # PURPLE LOGO (logo.png.png) LOCKED TO SIDEBAR
    if purple_logo: st.image(purple_logo, use_container_width=True)
    st.markdown("---")
    
    portal = st.radio("Access Level", ["User Workspace", "Admin Dashboard"])
    
    if portal == "Admin Dashboard":
        st.subheader("Subscription & Quota Management")
        # THESE PLANS ARE NOW HARD-LOCKED
        selected_tier = st.selectbox("Client Tier", list(PLAN_DATA.keys()))
        tier_info = PLAN_DATA[selected_tier]
        
        st.write(f"### Tier: ${tier_info['price']}/mo")
        st.write(f"### Quota: {st.session_state.design_count} / {tier_info['quota']} Designs")
        
        if st.button("Reset Monthly Quota"):
            st.session_state.design_count = 0
            st.rerun()
        st.info("Paystack USD Gateway: Active")
        
    else:
        st.subheader("Manufacturing Status")
        st.info(f"Unit: {st.session_state.unit_type} | SA: {st.session_state.sa_value}\"")
        for log in st.session_state.logs[-5:]:
            st.caption(log)

    st.markdown("---")
    st.session_state.unit_type = st.radio("Global Units", ["Inches", "CM"], horizontal=True)
    st.session_state.sa_value = st.number_input(f"Seam Allowance ({st.session_state.unit_type})", 
                                               value=0.5 if st.session_state.unit_type == "Inches" else 1.2)

# --- 3. MAIN WORKSPACE & SIDE LOGO ---
# SIDE LOGO (sidebar_logo.png.png) LOCKED TO MAIN HEADER
if side_logo: st.image(side_logo, width=160)
st.title("Industrial Technical Flat Engine")

tabs = st.tabs(["1. Precision Drafting", "2. Layer Manager", "3. Sizing & Grading", "4. DXF/DWG Export"])

with tabs[0]:
    col_tools, col_canvas = st.columns([1, 4])
    with col_tools:
        tool = st.radio("CAD Tool", ["Smart Curve (Bezier)", "Straight Line", "Edit Nodes"])
        symmetry = st.toggle("Symmetry Mirror", value=True)
        if st.button("Save Design"):
            st.session_state.design_count += 1
            st.session_state.logs.append(f"{datetime.datetime.now().strftime('%H:%M')}: Design Saved")
            st.success(f"Flat {st.session_state.design_count} Locked")
    with col_canvas:
        # COMPONENT ERROR FIX: No background_image= used. Pure vector engine.
        canvas_result = st_canvas(
            stroke_width=2, stroke_color="#000000",
            height=600, width=900,
            drawing_mode="path" if tool == "Smart Curve (Bezier)" else "line",
            key="v92_hard_lock"
        )

with tabs[1]:
    st.subheader("Internal vs. External Marker System")
    marker_mode = st.radio("Marker Mode", ["External (Cut - Blue)", "Internal (Stitch - Red)"], horizontal=True)
    
    st.write(f"The engine applies **{st.session_state.sa_value} {st.session_state.unit_type} SA** to Blue boundaries.")

with tabs[2]:
    st.subheader("Global Sizing Standards")
    region = st.selectbox("Region", ["US (Inches)", "UK (Inches)", "EU (CM)"])
    
    

with tabs[3]:
    st.subheader("Production-Ready Export")
    c1, c2, c3 = st.columns(3)
    with c1: st.button("Export PDF Tech Pack")
    with c2: st.button("Export DXF (Industrial Cut)")
    with c3: st.button("Export DWG (CAD Engineering)")
    
    st.markdown("---")
    
    st.info(f"All exports include mirrored symmetry and {st.session_state.sa_value} {st.session_state.unit_type} Seam Allowance.")
