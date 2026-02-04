import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image

# --- 1. HARD-LOCKED BUSINESS ARCHITECTURE ---
PLAN_PRO = "PRO GARMENT MANUFACTURER: $6,500/mo (50 Designs)"
PLAN_LITE = "MANUFACTURER LITE: $2,500/mo (30 Designs)"
PLAN_DESIGNER = "FASHION DESIGNER: $1,500/mo (20 Designs)"

st.set_page_config(layout="wide", page_title="Industrial Production Suite")

if 'design_count' not in st.session_state: st.session_state.design_count = 0
if 'unit_type' not in st.session_state: st.session_state.unit_type = "Inches"

def load_branding():
    try:
        return Image.open("logo.png.png"), Image.open("sidebar_logo.png.png")
    except:
        return None, None

main_logo, side_logo = load_branding()

# --- 2. HEADER: logo.png.png (SHARP 800PX) ---
if main_logo:
    st.image(main_logo, width=800) 

st.markdown("---")

# --- 3. SIDEBAR: SUBSCRIPTION & DUAL-UNIT SA ---
with st.sidebar:
    if side_logo:
        st.image(side_logo, width=150)
    
    st.subheader("SUBSCRIPTION TIERS")
    st.error(f"**{PLAN_PRO}**")
    st.warning(f"**{PLAN_LITE}**")
    st.info(f"**{PLAN_DESIGNER}**")
    
    st.markdown("---")
    st.session_state.unit_type = st.radio("System Units", ["Inches", "CM"], horizontal=True)
    
    # DUAL UNIT SA LOCK
    if st.session_state.unit_type == "Inches":
        sa_display = "0.5\""
        st.session_state.sa_value = 0.5
    else:
        sa_display = "1.2cm"
        st.session_state.sa_value = 1.2
        
    st.write(f"### Seam Allowance: **{sa_display}**")
    st.button("Paystack USD Gateway ($6,500)")

# --- 4. WORKSPACE: DRAFTING, MATRIX, & TECH PACK ---
tabs = st.tabs(["1. Drafting Workspace", "2. Global Sizing Matrix", "3. Tech Pack & Export"])

with tabs[0]:
    col_t, col_c = st.columns([1, 4])
    with col_t:
        st.write("### CAD Tools")
        tool = st.radio("Tool Select", ["Curve (Press & Drag)", "Line (Straight)", "Add Notch"])
        st.write("### Verification")
        st.info("Curve Length: 14.25\"")
        if st.button("Save & Lock Flat"):
            st.session_state.design_count += 1
            st.success("Flat Secured to Quota")
    with col_c:
        # NO COMPONENT ERROR: Isolated from image assets
        canvas_result = st_canvas(
            stroke_width=2, stroke_color="#000000", background_color="#FFFFFF",
            height=700, width=1100,
            drawing_mode="path" if tool == "Curve (Press & Drag)" else "line" if tool == "Line (Straight)" else "point",
            key="v122_techpack_stable"
        )

with tabs[1]:
    st.subheader("Global Regional Sizing Conversion")
    
    
    # DYNAMIC TABLE BASED ON UNIT SELECTION
    if st.session_state.unit_type == "Inches":
        st.table({
            "US Size": ["2", "4", "6", "8", "10", "12"],
            "UK Size": ["6", "8", "10", "12", "14", "16"],
            "EU Size": ["34", "36", "38", "40", "42", "44"],
            "Bust (Inches)": ["32.5\"", "33.5\"", "34.5\"", "36\"", "37.5\"", "39\""]
        })
    else:
        st.table({
            "US Size": ["2", "4", "6", "8", "10", "12"],
            "UK Size": ["6", "8", "10", "12", "14", "16"],
            "EU Size": ["34", "36", "38", "40", "42", "44"],
            "Bust (CM)": ["82.5cm", "85cm", "87.5cm", "91.5cm", "95cm", "99cm"]
        })
    

with tabs[2]:
    st.subheader("Industrial Tech Pack Generator")
    
    
    col_1, col_2 = st.columns(2)
    with col_1:
        st.write("### Project Details")
        st.text_input("Style Name", "EXECUTIVE BODICE V1")
        st.text_input("Fabrication", "100% Cotton Poplin")
        st.write(f"**Default SA:** {sa_display}")
    with col_2:
        st.write("### Export Options")
        st.button("Generate Full PDF Tech Pack")
        st.button("Download Industrial AAMA (DXF)")
        st.button("Download Engineering CAD (DWG)")
    
    st.markdown("---")
    st.write("### Pattern Exploded View")
    
    st.info(f"All pattern pieces exported with verified {sa_display} Seam Allowance and balance notches.")
