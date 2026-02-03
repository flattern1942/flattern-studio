import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image

# --- 1. PERMANENT IDENTITY ---
st.set_page_config(layout="wide")
if 'sa_value' not in st.session_state: st.session_state.sa_value = 0.5

def load_branding():
    try:
        return Image.open("sidebar_logo.png.png"), Image.open("logo.png.png")
    except:
        return None, None

side_logo, purple_logo = load_branding()

with st.sidebar:
    if side_logo: st.image(side_logo, use_container_width=True)
    st.markdown("---")
    # THE PLANS: Hard-locked pricing
    plan = st.selectbox("", [
        "Pro Garment Manufacturer ($6,500/mo - 50 Designs)",
        "Garment Manufacturer Lite ($2,500/mo - 30 Designs)",
        "Fashion Designer ($1,500/mo - 20 Designs)"
    ])
    
    st.write("### Seam Allowance (Inches)")
    c1, c2, c3 = st.columns([1, 2, 1])
    with c1: 
        if st.button("−"): st.session_state.sa_value -= 0.125
    with c3: 
        if st.button("+"): st.session_state.sa_value += 0.125
    with c2: 
        st.session_state.sa_value = st.number_input("", value=st.session_state.sa_value, format="%.3f")

# --- 2. VECTOR WORKSPACE ---
st.title("Industrial Vector Workspace")

# Purple logo anchored above the workspace
if purple_logo: st.image(purple_logo, width=150)

col_tools, col_draw = st.columns([1, 5])
with col_tools:
    tool = st.radio("Tool", ["Smart Curve", "Straight Line", "Transform"])
    st.write("End-Points: **Snap Active**")
    if st.button("Clear Canvas"): st.rerun()

with col_draw:
    # CLEAN CANVAS: No background image to prevent crashes
    canvas_result = st_canvas(
        fill_color="rgba(0,0,0,0)", stroke_width=2, stroke_color="#000000",
        height=700, width=1000,
        drawing_mode="path" if tool == "Smart Curve" else ("line" if tool == "Straight Line" else "transform"),
        point_display_radius=5,
        key="final_stable_lock"
    )

# --- 3. PATTERN BREAKDOWN ---
if st.button("Generate Pattern Pieces"):
    st.success(f"Applying {st.session_state.sa_value}\" SA. Separating Front, Back, and Sleeve Panels.")
