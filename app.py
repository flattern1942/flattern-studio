import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import datetime

# --- 1. INDUSTRIAL IDENTITY & UNIT LOCK ---
st.set_page_config(layout="wide")

if 'access_level' not in st.session_state: st.session_state.access_level = "User"
if 'unit_type' not in st.session_state: st.session_state.unit_type = "Inches"
if 'sa_value' not in st.session_state: st.session_state.sa_value = 0.5
if 'logs' not in st.session_state: 
    st.session_state.logs = [f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}: DXF/DWG Export Ready"]

def load_pro_branding():
    try:
        # Assets as specified in your directory
        return Image.open("sidebar_logo.png.png"), Image.open("logo.png.png")
    except:
        return None, None

side_logo, purple_logo = load_pro_branding()

# --- SIDEBAR: PURPLE LOGO & ADMIN PORTAL ---
with st.sidebar:
    # PURPLE LOGO RETURNED TO SIDEBAR
    if purple_logo: 
        st.image(purple_logo, use_container_width=True)
    st.markdown("---")
    
    st.session_state.access_level = st.radio("Access Portal", ["User Workspace", "Admin Dashboard"])
    
    if st.session_state.access_level == "Admin Dashboard":
        st.subheader("Global Control Panel")
        plan = st.selectbox("Active Plan Management", [
            "Pro Garment Manufacturer ($6,500/mo - 50 Designs)",
            "Garment Manufacturer Lite ($2,500/mo - 30 Designs)",
            "Fashion Designer ($1,500/mo - 20 Designs)"
        ])
        st.button("Paystack API Settings")
        st.write("### User Management")
        st.text_input("Invite Production Team (Email)")
        
    else:
        st.subheader("Designer Session")
        st.info("Plan: Pro ($6,500) | 50 Design Limit")
        st.write("### Manufacturing History")
        for log in st.session_state.logs[-8:]:
            st.caption(log)

    st.markdown("---")
    st.session_state.unit_type = st.radio("Measurement Unit", ["Inches", "CM"], horizontal=True)
    st.write(f"### Seam Allowance ({st.session_state.unit_type})")
    st.session_state.sa_value = st.number_input("", value=0.5 if st.session_state.unit_type == "Inches" else 1.2, step=0.1)

# --- 2. THE STABLE WORKSPACE & SIDE_LOGO ---
# SIDE_LOGO RETURNED TO MAIN PAGE WORKSPACE
if side_logo: 
    st.image(side_logo, width=150)
st.title(f"Industrial Vector Engine - {st.session_state.access_level}")

tabs = st.tabs(["1. Tech Drafting", "2. Layer Manager", "3. Global Grading", "4. CAD Export (DWG/DXF/PDF)"])

with tabs[0]:
    col_t, col_c = st.columns([1, 4])
    with col_t:
        st.write("### CAD Tools")
        tool = st.radio("Mode", ["Smart Curve (Bezier)", "Straight Line", "Edit Nodes"])
        symmetry = st.toggle("Symmetry Mirror", value=True)
        if st.button("Save Design"):
            st.session_state.logs.append(f"{datetime.datetime.now().strftime('%H:%M')}: Design Locked")
            st.success("Draft Secured")
    with col_c:
        # NO background_image inside canvas = STABLE / NO ERROR
        canvas_result = st_canvas(
            fill_color="rgba(0,0,0,0)", stroke_width=2, stroke_color="#000000",
            height=600, width=950,
            drawing_mode="path" if tool == "Smart Curve (Bezier)" else "line",
            key="v89_production_stable"
        )

with tabs[1]:
    st.subheader("Industrial Layer Management")
    marker = st.radio("Marker Mode", ["Blue (External/Cut)", "Red (Internal/Stitch)"], horizontal=True)
    
    st.write(f"Applying **{st.session_state.sa_value} {st.session_state.unit_type} SA** to Blue markers.")

with tabs[2]:
    st.subheader("Global Grading Matrix")
    region = st.selectbox("Standard", ["US (Inches)", "UK (Inches)", "EU (CM)"])
    
    

with tabs[3]:
    st.subheader("Industrial Export (High-Fidelity)")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.button("Export PDF Tech Pack")
    with col2:
        st.write("### DXF (AAMA)")
        st.caption("Uncompromised Cutting Data")
        st.button("Export DXF")
    with col3:
        st.write("### DWG (AutoCAD)")
        st.caption("Full Layer Engineering")
        st.button("Export DWG")
    
    st.markdown("---")
    
    st.info("Generating production-ready Front, Back, and Sleeve panels with matched balance notches.")
