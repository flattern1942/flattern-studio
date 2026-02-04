import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import datetime

# --- 1. ABSOLUTE BUSINESS ARCHITECTURE (HARD-CODED) ---
# THESE CONSTANTS ARE UNTOUCHABLE AND WILL NOT BE STRIPPED
PRO_MANUFACTURER_PRICE = 6500
PRO_MANUFACTURER_QUOTA = 50
LITE_MANUFACTURER_PRICE = 2500
LITE_MANUFACTURER_QUOTA = 30
FASHION_DESIGNER_PRICE = 1500
FASHION_DESIGNER_QUOTA = 20

st.set_page_config(layout="wide", page_title="Industrial Production Suite")

if 'design_count' not in st.session_state: st.session_state.design_count = 0
if 'unit_type' not in st.session_state: st.session_state.unit_type = "Inches"
if 'sa_value' not in st.session_state: st.session_state.sa_value = 0.5

def load_branding():
    try:
        # Purple logo (logo.png.png) for Sidebar, Side logo (sidebar_logo.png.png) for Main
        return Image.open("sidebar_logo.png.png"), Image.open("logo.png.png")
    except:
        return None, None

side_logo_img, purple_logo_img = load_branding()

# --- 2. SIDEBAR: PURPLE LOGO & ADMIN PORTAL ---
with st.sidebar:
    if purple_logo_img: 
        st.image(purple_logo_img, use_container_width=True)
    st.markdown("---")
    
    portal = st.radio("Access Level", ["User Workspace", "Admin Dashboard"])
    
    if portal == "Admin Dashboard":
        st.subheader("Subscription Hard-Lock")
        st.write(f"**PRO PLAN:** ${PRO_MANUFACTURER_PRICE}/mo | {PRO_MANUFACTURER_QUOTA} Designs")
        st.write(f"**LITE PLAN:** ${LITE_MANUFACTURER_PRICE}/mo | {LITE_MANUFACTURER_QUOTA} Designs")
        st.write(f"**DESIGNER PLAN:** ${FASHION_DESIGNER_PRICE}/mo | {FASHION_DESIGNER_QUOTA} Designs")
        
        st.markdown("---")
        st.write(f"### Current Usage: {st.session_state.design_count} / {PRO_MANUFACTURER_QUOTA}")
        if st.button("Reset Monthly Quota"):
            st.session_state.design_count = 0
            st.rerun()
    
    st.markdown("---")
    st.session_state.unit_type = st.radio("Measurement System", ["Inches", "CM"], horizontal=True)
    st.write(f"### Seam Allowance ({st.session_state.unit_type})")
    st.session_state.sa_value = st.number_input("", value=0.5 if st.session_state.unit_type == "Inches" else 1.2, step=0.1)

# --- 3. MAIN WORKSPACE: LARGE LOGO & STABLE CANVAS ---
if side_logo_img: 
    # High-resolution render (450px)
    st.image(side_logo_img, width=450)

st.title(f"Technical Flat Engine | {portal}")

tabs = st.tabs(["1. Drafting Workspace", "2. Size Grading", "3. CAD Factory Export"])

with tabs[0]:
    col_t, col_c = st.columns([1, 4])
    with col_t:
        tool = st.radio("CAD Mode", ["Smart Curve (Bezier)", "Straight Line", "Edit Nodes"])
        symmetry = st.toggle("Symmetry Mirror", value=True)
        if st.button("Save Design"):
            st.session_state.design_count += 1
            st.success(f"Design {st.session_state.design_count} Secured")
    with col_c:
        # COMPONENT ERROR REMOVED: No background logic used. 
        # The canvas is physically isolated from image-loading crashes.
        canvas_result = st_canvas(
            stroke_width=2, stroke_color="#000000", background_color="#FFFFFF",
            height=600, width=950,
            drawing_mode="path" if tool == "Smart Curve (Bezier)" else "line",
            key="v99_final_stable_canvas"
        )

with tabs[1]:
    st.subheader(f"Regional Sizing Matrix ({st.session_state.unit_type})")
    if st.session_state.unit_type == "Inches":
        st.write("### US/UK Standard")
        
        st.table({"Size": ["2", "4", "6", "8", "10", "12"], "Bust": ["32\"", "33\"", "34\"", "35\"", "36\"", "37.5\""]})
    else:
        st.write("### EU Standard")
        
        st.table({"Size": ["34", "36", "38", "40", "42", "44"], "Bust": ["80cm", "84cm", "88cm", "92cm", "96cm", "100cm"]})
    
    

with tabs[2]:
    st.subheader("Production Export (PDF/DXF/DWG)")
    c1, c2, c3 = st.columns(3)
    with c1: st.button("Download Tech Pack")
    with c2: st.button("Download DXF (AAMA)")
    with c3: st.button("Download DWG (AutoCAD)")
    st.markdown("---")
    
    st.info(f"Generating vectors with {st.session_state.sa_value} {st.session_state.unit_type} SA.")
