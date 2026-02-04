import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import datetime

# --- 1. PRO IDENTITY & UNIT LOCK ---
st.set_page_config(layout="wide")

if 'unit_type' not in st.session_state: st.session_state.unit_type = "Inches"
if 'sa_value' not in st.session_state: st.session_state.sa_value = 0.5
if 'logs' not in st.session_state: 
    st.session_state.logs = [f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}: Layer Manager Active"]

def load_pro_branding():
    try:
        return Image.open("sidebar_logo.png.png"), Image.open("logo.png.png")
    except:
        return None, None

side_logo, purple_logo = load_pro_branding()

# --- SIDEBAR: LOGOS, PLANS, & LOGS ---
with st.sidebar:
    if side_logo: st.image(side_logo, use_container_width=True)
    st.markdown("---")
    
    view = st.radio("Management", ["Technical Drafting", "Audit Logs", "Billing & Plans"])
    
    if view == "Billing & Plans":
        st.write("### Production Tiers")
        plan = st.selectbox("Select Plan", [
            "Pro Garment Manufacturer ($6,500/mo - 50 Designs)",
            "Garment Manufacturer Lite ($2,500/mo - 30 Designs)",
            "Fashion Designer ($1,500/mo - 20 Designs)"
        ])
        st.button("Initialize Paystack USD Checkout")
    
    elif view == "Audit Logs":
        st.write("### Manufacturing History")
        for log in st.session_state.logs[-10:]:
            st.caption(log)

    st.markdown("---")
    st.session_state.unit_type = st.radio("Measurement Unit", ["Inches", "CM"], horizontal=True)
    region = st.selectbox("Size Standard", ["US (Inches)", "UK (Inches)", "EU (CM)"])
    
    st.write(f"### Seam Allowance ({st.session_state.unit_type})")
    default_sa = 0.5 if st.session_state.unit_type == "Inches" else 1.2
    st.session_state.sa_value = st.number_input("", value=st.session_state.sa_value, step=0.1)

# --- 2. THE STABLE TECHNICAL WORKSPACE ---
if purple_logo: st.image(purple_logo, width=150)
st.title("Industrial Technical Flat Engine")

tabs = st.tabs(["1. Precision Drafting", "2. Layer Manager", "3. Global Grading", "4. Export CAD (PDF/DXF/DWG)"])

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
        # NO BACKGROUND IMAGE = NO COMPONENT ERROR.
        canvas_result = st_canvas(
            fill_color="rgba(0,0,0,0)", stroke_width=2, stroke_color="#000000",
            height=600, width=950,
            drawing_mode="path" if tool == "Smart Curve (Bezier)" else "line",
            key="v85_layer_stable"
        )

with tabs[1]:
    st.subheader("Industrial Layer Manager")
    st.write("Select which data layers to include in the production file:")
    l1 = st.checkbox("External Boundary (Cut Lines - Blue)", value=True)
    l2 = st.checkbox("Internal Details (Stitch Lines - Red)", value=True)
    l3 = st.checkbox("Seam Allowance Offset", value=True)
    l4 = st.checkbox("Balance Notches & Darts", value=True)
    
    
    st.write(f"Layer system applying **{st.session_state.sa_value} {st.session_state.unit_type} SA** to External Boundary.")

with tabs[2]:
    st.subheader(f"Global Grading ({region})")
    
    

with tabs[3]:
    st.subheader("Industrial Export Panel")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("### PDF Tech Pack")
        st.button("Export PDF")
    with col2:
        st.write("### DXF (AAMA)")
        st.button("Export DXF")
    with col3:
        st.write("### DWG (CAD)")
        st.button("Export DWG")

    st.markdown("---")
    
    st.info(f"Export includes {st.session_state.sa_value} {st.session_state.unit_type} SA on active layers.")
