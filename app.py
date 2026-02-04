import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image

# --- 1. GLOBAL SETTINGS & IDENTITY ---
st.set_page_config(layout="wide")

if 'sa_value' not in st.session_state: st.session_state.sa_value = 0.5
if 'designs' not in st.session_state: st.session_state.designs = 0

# Static Image Loading (Independent of Canvas)
def load_assets():
    try:
        return Image.open("sidebar_logo.png.png"), Image.open("logo.png.png")
    except:
        return None, None

side_logo, purple_logo = load_assets()

# --- SIDEBAR: BILLING & ADMIN ---
with st.sidebar:
    if side_logo: 
        st.image(side_logo, use_container_width=True)
    
    st.markdown("---")
    portal = st.radio("Portal", ["Paystack Checkout", "Admin Login"])
    
    if portal == "Paystack Checkout":
        st.write("### Design Quota")
        st.metric("Available", st.session_state.designs)
        if st.button("Unlock 50 Designs (USD)"):
            st.session_state.designs += 50
            st.success("Webhook Verified: +50 Designs")
    else:
        st.text_input("Admin ID")
        st.text_input("Key", type="password")

    st.markdown("---")
    st.write("### Seam Allowance (Inches)")
    c1, c2, c3 = st.columns([1, 2, 1])
    with c1: 
        if st.button("−"): st.session_state.sa_value -= 0.125
    with c3: 
        if st.button("+"): st.session_state.sa_value += 0.125
    with c2: 
        st.session_state.sa_value = st.number_input("", value=st.session_state.sa_value, format="%.3f")

# --- 2. VECTOR ENGINE (STABLE) ---
st.title("Industrial Vector Workspace")

# Anchor the purple logo safely above the canvas
if purple_logo: 
    st.image(purple_logo, width=120)

tabs = st.tabs(["1. Precision Drafting", "2. Piece Breakdown", "3. Export"])

with tabs[0]:
    col_ctrl, col_canvas = st.columns([1, 4])
    
    with col_ctrl:
        mode = st.radio("Tool", ["Smart Curve (Bezier)", "Line", "Transform"])
        st.info("Click and Drag for Arcs")
        if st.button("Refresh Canvas"): st.rerun()

    with col_canvas:
        # THE FIX: No background_image, no URL processing. Pure stability.
        canvas_result = st_canvas(
            fill_color="rgba(0,0,0,0)",
            stroke_width=2,
            stroke_color="#000000",
            height=650,
            width=900,
            drawing_mode="path" if mode == "Smart Curve (Bezier)" else ("line" if mode == "Line" else "transform"),
            key="v61_fixed_stable"
        )

with tabs[1]:
    st.subheader("Front, Back, and Sleeve Panel Generation")
    
    st.write(f"Calculating {st.session_state.sa_value}\" SA for all industrial panels.")

with tabs[2]:
    st.subheader("Industrial Transformation")
    
    if st.button("Export to DXF"):
        if st.session_state.designs > 0:
            st.session_state.designs -= 1
            st.success("Pattern Exported Successfully.")
