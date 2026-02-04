import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import datetime

# --- 1. INDUSTRIAL IDENTITY & ACCESS LOCK ---
st.set_page_config(layout="wide")

if 'access_level' not in st.session_state: st.session_state.access_level = "User"
if 'unit_type' not in st.session_state: st.session_state.unit_type = "Inches"
if 'sa_value' not in st.session_state: st.session_state.sa_value = 0.5
if 'logs' not in st.session_state: 
    st.session_state.logs = [f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}: Enterprise Engine Online"]

def load_pro_branding():
    try:
        return Image.open("sidebar_logo.png.png"), Image.open("logo.png.png")
    except:
        return None, None

side_logo, purple_logo = load_pro_branding()

# --- SIDEBAR: MULTI-LEVEL PORTAL ---
with st.sidebar:
    if side_logo: st.image(side_logo, use_container_width=True)
    st.markdown("---")
    
    st.session_state.access_level = st.radio("Access Level", ["User (Drafting)", "Admin (Management)"])
    
    if st.session_state.access_level == "Admin (Management)":
        st.subheader("Client Account Manager")
        active_client = st.selectbox("Select Client Account", ["Astra Garments Ltd", "Global Stitch Pro", "Moda Design House"])
        
        st.write("### Billing Management")
        plan = st.selectbox("Assign Plan Tier", [
            "Pro Garment Manufacturer ($6,500/mo - 50 Designs)",
            "Garment Manufacturer Lite ($2,500/mo - 30 Designs)",
            "Fashion Designer ($1,500/mo - 20 Designs)"
        ])
        st.metric("Current Usage", "14 / 50 Designs")
        st.button("Paystack Billing Dashboard")
        
    else:
        st.subheader("Active Work Session")
        st.info("Account: Astra Garments Ltd | Tier: Pro ($6,500)")
        st.write("### Manufacturing History")
        for log in st.session_state.logs[-8:]:
            st.caption(log)

    st.markdown("---")
    st.session_state.unit_type = st.radio("Measurement Unit", ["Inches", "CM"], horizontal=True)
    st.write(f"### Seam Allowance ({st.session_state.unit_type})")
    st.session_state.sa_value = st.number_input("", value=0.5 if st.session_state.unit_type == "Inches" else 1.2, step=0.1)

# --- 2. THE STABLE WORKSPACE ---
if purple_logo: st.image(purple_logo, width=150)
st.title(f"Technical Workspace - {st.session_state.access_level}")

tabs = st.tabs(["1. Precision Drafting", "2. Layer & Marker Manager", "3. Global Grading", "4. Industrial Export"])

with tabs[0]:
    col_t, col_c = st.columns([1, 4])
    with col_t:
        st.write("### CAD Tools")
        tool = st.radio("Mode", ["Smart Curve (Bezier)", "Straight Line", "Edit Nodes"])
        symmetry = st.toggle("Symmetry Mirror (X-Axis)", value=True)
        if st.button("Save Design"):
            st.session_state.logs.append(f"{datetime.datetime.now().strftime('%H:%M')}: design locked to account")
            st.success("Flat Secured")
    with col_c:
        # NO background_image INSIDE CANVAS = NO COMPONENT ERROR
        canvas_result = st_canvas(
            fill_color="rgba(0,0,0,0)", stroke_width=2, stroke_color="#000000",
            height=600, width=950,
            drawing_mode="path" if tool == "Smart Curve (Bezier)" else "line",
            key="v87_enterprise_stable"
        )

with tabs[1]:
    st.subheader("Internal/External Layering")
    marker = st.radio("Highlighter Mode", ["External (Cut - Blue)", "Internal (Stitch - Red)"], horizontal=True)
    
    st.write(f"Breakdown Engine applying **{st.session_state.sa_value} {st.session_state.unit_type} SA** to Blue markers.")

with tabs[2]:
    st.subheader("Global Grading Matrix")
    region = st.selectbox("Regional Standard", ["US (Inches)", "UK (Inches)", "EU (CM)"])
    
    

with tabs[3]:
    st.subheader("CAD Export Center (PDF/DXF/DWG)")
    c1, c2, c3 = st.columns(3)
    with c1: st.button("Export PDF (Tech Pack)")
    with c2: st.button("Export DXF (CAM)")
    with c3: st.button("Export DWG (Engineering)")
    
    st.markdown("---")
    
    st.info("Generating industrial panels (Front, Back, Sleeve) with balance notches.")import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import datetime

# --- 1. INDUSTRIAL IDENTITY & ACCESS LOCK ---
st.set_page_config(layout="wide")

if 'access_level' not in st.session_state: st.session_state.access_level = "User"
if 'unit_type' not in st.session_state: st.session_state.unit_type = "Inches"
if 'sa_value' not in st.session_state: st.session_state.sa_value = 0.5
if 'logs' not in st.session_state: 
    st.session_state.logs = [f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}: Enterprise Engine Online"]

def load_pro_branding():
    try:
        return Image.open("sidebar_logo.png.png"), Image.open("logo.png.png")
    except:
        return None, None

side_logo, purple_logo = load_pro_branding()

# --- SIDEBAR: MULTI-LEVEL PORTAL ---
with st.sidebar:
    if side_logo: st.image(side_logo, use_container_width=True)
    st.markdown("---")
    
    st.session_state.access_level = st.radio("Access Level", ["User (Drafting)", "Admin (Management)"])
    
    if st.session_state.access_level == "Admin (Management)":
        st.subheader("Client Account Manager")
        active_client = st.selectbox("Select Client Account", ["Astra Garments Ltd", "Global Stitch Pro", "Moda Design House"])
        
        st.write("### Billing Management")
        plan = st.selectbox("Assign Plan Tier", [
            "Pro Garment Manufacturer ($6,500/mo - 50 Designs)",
            "Garment Manufacturer Lite ($2,500/mo - 30 Designs)",
            "Fashion Designer ($1,500/mo - 20 Designs)"
        ])
        st.metric("Current Usage", "14 / 50 Designs")
        st.button("Paystack Billing Dashboard")
        
    else:
        st.subheader("Active Work Session")
        st.info("Account: Astra Garments Ltd | Tier: Pro ($6,500)")
        st.write("### Manufacturing History")
        for log in st.session_state.logs[-8:]:
            st.caption(log)

    st.markdown("---")
    st.session_state.unit_type = st.radio("Measurement Unit", ["Inches", "CM"], horizontal=True)
    st.write(f"### Seam Allowance ({st.session_state.unit_type})")
    st.session_state.sa_value = st.number_input("", value=0.5 if st.session_state.unit_type == "Inches" else 1.2, step=0.1)

# --- 2. THE STABLE WORKSPACE ---
if purple_logo: st.image(purple_logo, width=150)
st.title(f"Technical Workspace - {st.session_state.access_level}")

tabs = st.tabs(["1. Precision Drafting", "2. Layer & Marker Manager", "3. Global Grading", "4. Industrial Export"])

with tabs[0]:
    col_t, col_c = st.columns([1, 4])
    with col_t:
        st.write("### CAD Tools")
        tool = st.radio("Mode", ["Smart Curve (Bezier)", "Straight Line", "Edit Nodes"])
        symmetry = st.toggle("Symmetry Mirror (X-Axis)", value=True)
        if st.button("Save Design"):
            st.session_state.logs.append(f"{datetime.datetime.now().strftime('%H:%M')}: design locked to account")
            st.success("Flat Secured")
    with col_c:
        # NO background_image INSIDE CANVAS = NO COMPONENT ERROR
        canvas_result = st_canvas(
            fill_color="rgba(0,0,0,0)", stroke_width=2, stroke_color="#000000",
            height=600, width=950,
            drawing_mode="path" if tool == "Smart Curve (Bezier)" else "line",
            key="v87_enterprise_stable"
        )

with tabs[1]:
    st.subheader("Internal/External Layering")
    marker = st.radio("Highlighter Mode", ["External (Cut - Blue)", "Internal (Stitch - Red)"], horizontal=True)
    
    st.write(f"Breakdown Engine applying **{st.session_state.sa_value} {st.session_state.unit_type} SA** to Blue markers.")

with tabs[2]:
    st.subheader("Global Grading Matrix")
    region = st.selectbox("Regional Standard", ["US (Inches)", "UK (Inches)", "EU (CM)"])
    
    

with tabs[3]:
    st.subheader("CAD Export Center (PDF/DXF/DWG)")
    c1, c2, c3 = st.columns(3)
    with c1: st.button("Export PDF (Tech Pack)")
    with c2: st.button("Export DXF (CAM)")
    with c3: st.button("Export DWG (Engineering)")
    
    st.markdown("---")
    
    st.info("Generating industrial panels (Front, Back, Sleeve) with balance notches.")
