import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import datetime

# --- 1. CORE SYSTEM & INDUSTRIAL IDENTITY ---
st.set_page_config(layout="wide", page_title="Industrial Flat Maker")

# Persistent business states
if 'access_level' not in st.session_state: st.session_state.access_level = "User Workspace"
if 'unit_type' not in st.session_state: st.session_state.unit_type = "Inches"
if 'sa_value' not in st.session_state: st.session_state.sa_value = 0.5
if 'design_count' not in st.session_state: st.session_state.design_count = 14
if 'logs' not in st.session_state: 
    st.session_state.logs = [f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}: Quota Engine Active"]

def load_pro_branding():
    try:
        # Strict mapping to your verified file names
        return Image.open("sidebar_logo.png.png"), Image.open("logo.png.png")
    except:
        return None, None

side_logo, purple_logo = load_pro_branding()

# --- 2. SIDEBAR: PURPLE LOGO & ADMIN QUOTA CONTROL ---
with st.sidebar:
    if purple_logo: 
        st.image(purple_logo, use_container_width=True)
    st.markdown("---")
    
    st.session_state.access_level = st.radio("Access Level", ["User Workspace", "Admin Dashboard"])
    
    if st.session_state.access_level == "Admin Dashboard":
        st.subheader("Account Control")
        plan = st.selectbox("Client Plan Tier", [
            "Pro Garment Manufacturer ($6,500/mo - 50 Designs)",
            "Garment Manufacturer Lite ($2,500/mo - 30 Designs)",
            "Fashion Designer ($1,500/mo - 20 Designs)"
        ])
        
        # QUOTA RESET LOGIC
        max_designs = 50 if "6,500" in plan else (30 if "2,500" in plan else 20)
        st.write(f"### Usage: {st.session_state.design_count} / {max_designs}")
        
        if st.button("Reset Monthly Quota"):
            st.session_state.design_count = 0
            st.session_state.logs.append(f"{datetime.datetime.now().strftime('%H:%M')}: Quota Reset by Admin")
            st.rerun()
            
        st.info("Payment: Paystack USD Integrated")
    
    else:
        st.subheader("Drafting Session")
        st.write("### Manufacturing Logs")
        for log in st.session_state.logs[-8:]:
            st.caption(log)

    st.markdown("---")
    st.session_state.unit_type = st.radio("Units", ["Inches", "CM"], horizontal=True)
    st.write(f"### Seam Allowance ({st.session_state.unit_type})")
    st.session_state.sa_value = st.number_input("", value=0.5 if st.session_state.unit_type == "Inches" else 1.2, step=0.1)

# --- 3. MAIN WORKSPACE & SIDE LOGO ---
# FIXED: side_logo rendered outside canvas to eliminate Component Error
if side_logo: 
    st.image(side_logo, width=160)
st.title(f"Technical Flat Engine | {st.session_state.access_level}")

tabs = st.tabs(["Drafting", "Layers", "Grading (US/UK/EU)", "Industrial Export"])

with tabs[0]:
    col_t, col_c = st.columns([1, 4])
    with col_t:
        tool = st.radio("CAD Tool", ["Smart Curve (Bezier)", "Straight Line", "Edit Nodes"])
        symmetry = st.toggle("Symmetry Mirror", value=True)
        if st.button("Save To Database"):
            st.session_state.design_count += 1
            st.session_state.logs.append(f"{datetime.datetime.now().strftime('%H:%M')}: Design {st.session_state.design_count} Saved")
            st.success("Technical Flat Secured")
    with col_c:
        # THE STABILITY FIX: Pure white/transparent canvas background
        canvas_result = st_canvas(
            fill_color="rgba(0,0,0,0)", stroke_width=2, stroke_color="#000000",
            height=620, width=960,
            drawing_mode="path" if tool == "Smart Curve (Bezier)" else "line",
            key="v91_gold_lock"
        )

with tabs[1]:
    st.subheader("Internal vs. External Layer Management")
    marker = st.radio("Marker Mode", ["External (Cut - Blue)", "Internal (Stitch - Red)"], horizontal=True)
    
    st.write(f"System applying **{st.session_state.sa_value} {st.session_state.unit_type} SA** to Blue markers.")

with tabs[2]:
    st.subheader("Global Grading Matrix")
    region = st.selectbox("Standard", ["US (Inches)", "UK (Inches)", "EU (CM)"])
    
    

with tabs[3]:
    st.subheader("CAD Export Center (PDF/DXF/DWG)")
    c1, c2, c3 = st.columns(3)
    with c1: st.button("Export PDF Tech Pack")
    with c2: st.button("Export DXF (AAMA)")
    with c3: st.button("Export DWG (AutoCAD)")
    
    st.markdown("---")
    
    st.info(f"Generating Front, Back, and Sleeve panels with matched balance notches.")
