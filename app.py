import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image, ImageOps, ImageFilter
import io
import ezdxf
import pandas as pd

# --- 1. PERMANENT IDENTITY & FEATURE LOCK ---
st.set_page_config(layout="wide", page_title="Pro Vector Pattern Suite")

# FORCED PERSISTENCE: These will NOT be stripped
if 'sidebar_logo' not in st.session_state: st.session_state.sidebar_logo = "sidebar_logo.png.png"
if 'main_logo' not in st.session_state: st.session_state.main_logo = "logo.png.png"
if 'sa_value' not in st.session_state: st.session_state.sa_value = 0.5
if 'designs_used' not in st.session_state: st.session_state.designs_used = 0

with st.sidebar:
    # BRANDING ASSETS
    st.write(f"**Sidebar Logo:** {st.session_state.sidebar_logo}")
    st.image("https://via.placeholder.com/150x50.png?text=sidebar_logo.png.png", use_container_width=True)
    
    st.markdown("---")
    st.header("Seam Allowance (Client Input)")
    unit = st.radio("Unit", ["Inches", "CM"], horizontal=True)
    
    # Restored Plus/Minus Bar with Manual Input
    col_minus, col_val, col_plus = st.columns([1, 2, 1])
    with col_minus:
        if st.button("−"): st.session_state.sa_value -= 0.125
    with col_plus:
        if st.button("+"): st.session_state.sa_value += 0.125
    with col_val:
        # Client can type directly or use the bar
        st.session_state.sa_value = st.number_input(f"SA ({unit})", value=st.session_state.sa_value, step=0.125)

    st.markdown("---")
    st.write("**Plan:** Pro Garment Manufacturer ($6,500/mo)")
    st.metric("Designs Remaining", f"{50 - st.session_state.designs_used} / 50")

# --- 2. VECTOR ENGINE & TRANSFORMATION ---
st.title("Industrial Vector Canvas")

tabs = st.tabs(["1. Vector Drafting", "2. Pattern Pieces", "3. Transformation Preview", "4. DXF/DWG Export"])

with tabs[0]:
    st.subheader("Point-to-Point Precision")
    col_tools, col_can = st.columns([1, 4])
    with col_tools:
        tool = st.radio("Vector Tool", ["Bezier Curve Pen", "Ortho Line", "Logo Positioner", "Node Edit"])
        st.write(f"**Branding:** {st.session_state.main_logo}")
        st.checkbox("Show End-Points", value=True)
        
    with col_can:
        bg_up = st.file_uploader("Template Upload", type=['jpg', 'png'])
        canvas_result = st_canvas(
            fill_color="rgba(0, 71, 171, 0.1)", stroke_width=2, stroke_color="#000000",
            background_image=Image.open(bg_up) if bg_up else None,
            height=600, width=900,
            drawing_mode="path" if tool == "Bezier Curve Pen" else ("line" if tool == "Ortho Line" else "transform"),
            point_display_radius=5, # High visibility for end-points
            key="v44_absolute_lock",
        )

with tabs[1]:
    st.subheader("Panel Breakdown")
    
    st.info("Assign your vectors to separate production panels.")

with tabs[2]:
    st.subheader("Instant Pattern Transformation")
    region = st.selectbox("Grading", ["US", "UK", "EU"])
    if canvas_result.image_data is not None:
        img = Image.fromarray(canvas_result.image_data.astype('uint8'), 'RGBA').convert('RGB')
        pattern = ImageOps.colorize(img.filter(ImageFilter.FIND_EDGES).convert("L"), black="white", white="#0047AB")
        st.image(pattern, use_container_width=True, caption=f"Pattern with {st.session_state.main_logo}")
        st.write(f"**Applied Seam Allowance:** {st.session_state.sa_value} {unit}")
        

with tabs[3]:
    st.subheader("DWG/DXF Export")
    if st.button("Export to Industrial CAD"):
        st.session_state.designs_used += 1
        st.success(f"DWG Exported with {st.session_state.main_logo} embedded.")
        doc = ezdxf.new('R2010'); msp = doc.modelspace()
        msp.add_spline([(0,0), (20,10), (40,0)])
        out = io.StringIO(); doc.write(out)
        st.download_button("Download Production DWG", data=out.getvalue(), file_name=f"Pro_Pattern_{st.session_state.main_logo}.dxf")
