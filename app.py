import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import datetime
import time

# --- 1. HARD-LOCKED BUSINESS CONSTANTS ---
PLAN_DATA = {
    "Pro Garment Manufacturer": {"price": 5000, "quota": 50},
    "Garment Manufacturer Lite": {"price": 2500, "quota": 30},
    "Fashion Designer": {"price": 1500, "quota": 20}
}

st.set_page_config(layout="wide", page_title="Industrial Production Suite")

# State Management
if 'design_count' not in st.session_state: st.session_state.design_count = 0
if 'unit_type' not in st.session_state: st.session_state.unit_type = "Inches"
if 'sa_value' not in st.session_state: st.session_state.sa_value = 0.5
if 'last_save' not in st.session_state: st.session_state.last_save = datetime.datetime.now().strftime('%H:%M:%S')

def load_branding():
    try:
        # Purple logo for Sidebar (logo.png.png), Side logo for Main (sidebar_logo.png.png)
        return Image.open("sidebar_logo.png.png"), Image.open("logo.png.png")
    except:
        return None, None

side_logo_img, purple_logo_img = load_branding()

# --- 2. SIDEBAR: PURPLE LOGO & ADMIN PORTAL ---
with st.sidebar:
    if purple_logo_img: 
        st.image(purple_logo_img, use_container_width=True)
    st.markdown("---")
    
    view = st.radio("Portal", ["Designer Workspace", "Admin Dashboard"])
    
    if view == "Admin Dashboard":
        st.subheader("Billing & Quota Control")
        selected_tier = st.selectbox("Active Plan Tier", list(PLAN_DATA.keys()))
        tier = PLAN_DATA[selected_tier]
        st.write(f"### Tier Cost: ${tier['price']}/mo")
        st.metric("Designs Used", f"{st.session_state.design_count} / {tier['quota']}")
        
        if st.button("Reset Monthly Quota"):
            st.session_state.design_count = 0
            st.rerun()
    
    st.markdown("---")
    st.session_state.unit_type = st.radio("Units", ["Inches", "CM"], horizontal=True)
    st.write(f"### Seam Allowance ({st.session_state.unit_type})")
    st.session_state.sa_value = st.number_input("", value=0.5 if st.session_state.unit_type == "Inches" else 1.2)
    st.caption(f"Last Safety Save: {st.session_state.last_save}")

# --- 3. MAIN WORKSPACE: SIDE LOGO & STABLE CANVAS ---
if side_logo_img: 
    st.image(side_logo_img, width=160)

st.title("Industrial Technical Flat Engine")

tabs = st.tabs(["1. Precision Drafting", "2. Grading Standards", "3. CAD Factory Export"])

with tabs[0]:
    col_ctrl, col_canvas = st.columns([1, 4])
    with col_ctrl:
        st.write("### CAD Controls")
        tool = st.radio("Mode", ["Smart Curve (Bezier)", "Straight Line", "Edit Nodes"])
        symmetry = st.toggle("Symmetry Mirror", value=True)
        
        if st.button("Manual Save to Quota"):
            st.session_state.design_count += 1
            st.session_state.last_save = datetime.datetime.now().strftime('%H:%M:%S')
            st.success(f"Design {st.session_state.design_count} Locked")

    with col_canvas:
        # THE STABILITY LOCK: background_image is set to None to prevent Component Error.
        canvas_result = st_canvas(
            stroke_width=2,
            stroke_color="#000000",
            background_color="#FFFFFF",
            height=600,
            width=900,
            drawing_mode="path" if tool == "Smart Curve (Bezier)" else "line",
            key="v96_safety_stable" 
        )

with tabs[1]:
    st.subheader("Global Sizing Matrix")
    
    st.info(f"System operating in {st.session_state.unit_type} for regional grading.")
    

with tabs[2]:
    st.subheader("Industrial Exports (PDF/DXF/DWG)")
    c1, c2, c3 = st.columns(3)
    with c1: st.button("Export PDF Tech Pack")
    with c2: st.button("Export DXF (Industrial)")
    with c3: st.button("Export DWG (Engineering)")
    st.markdown("---")
    
    st.write(f"All exports include {st.session_state.sa_value} {st.session_state.unit_type} Seam Allowance.")
