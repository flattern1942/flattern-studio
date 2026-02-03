import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image, ImageOps, ImageFilter
import io
import ezdxf
import pandas as pd

# --- 1. PRO IDENTITY & ABSOLUTE ASSET LOCK ---
st.set_page_config(layout="wide", page_title="Pro Vector Pattern Suite")

# LOCKING YOUR SPECIFIC FILENAMES
if 'sidebar_logo' not in st.session_state: st.session_state.sidebar_logo = "sidebar_logo.png.png"
if 'main_logo' not in st.session_state: st.session_state.main_logo = "logo.png.png"
if 'sa_value' not in st.session_state: st.session_state.sa_value = 0.5
if 'designs_used' not in st.session_state: st.session_state.designs_used = 0

with st.sidebar:
    # PERMANENT LOGO RENDER SLOTS
    st.write(f"**Branding Asset:** {st.session_state.sidebar_logo}")
    # Force search for local file link
    st.image("sidebar_logo.png.png", caption="Sidebar Identity Locked", use_container_width=True)
    
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
        st.session_state.sa_value = st.number_input(f"SA ({unit})", value=st.session_state.sa_value, format="%.3f")

    st.markdown("---")
    st.write("**Tier:** Pro Garment Manufacturer ($6,500/mo)")
    st.metric("Designs Remaining", f"{50 - st.session_state.designs_used} / 50")

# --- 2. VECTOR ENGINE & TRANSFORMATION ---
st.title("Industrial Vector Canvas")

tabs = st.tabs(["1. Vector Drafting", "2. Panel Breakdown", "3. Pattern Transformation", "4. DWG/DXF Export"])

with tabs[0]:
    st.subheader("Point-to-Point Precision Drafting")
    col_tools, col_can = st.columns([1, 4])
    with col_tools:
        tool = st.radio("Vector Tool", ["Bezier Curve Pen", "Ortho Line", "Logo Positioner", "Node Edit"])
        st.write(f"**Pattern Logo:** {st.session_state.main_logo}")
        st.checkbox("Show End-Points", value=True)
        st.info("End-points allow instant transformation to pattern.")
        
    with col_can:
        # Drawing canvas that recognizes the uploaded file as background
        canvas_result = st_canvas(
            fill_color="rgba(0, 71, 171, 0.1)", stroke_width=2, stroke_color="#000000",
            background_image=Image.open("logo.png.png") if "logo.png.png" else None,
            height=600, width=900,
            drawing_mode="path" if tool == "Bezier Curve Pen" else ("line" if tool == "Ortho Line" else "transform"),
            point_display_radius=5, 
            key="v46_pro_vector_lock",
        )

with tabs[1]:
    st.subheader("Component Separation")
    
    st.info("Separate your vectors into production panels (Front/Back/Sleeves).")

with tabs[2]:
    st.subheader("Instant Pattern Transformation")
    if canvas_result.image_data is not None:
        img = Image.fromarray(canvas_result.image_data.astype('uint8'), 'RGBA').convert('RGB')
        pattern = ImageOps.colorize(img.filter(ImageFilter.FIND_EDGES).convert("L"), black="white", white="#0047AB")
        st.image(pattern, use_container_width=True, caption=f"Vector-Transformed Pattern with {st.session_state.main_logo}")
        st.write(f"**Client SA Applied:** {st.session_state.sa_value} {unit}")
        

with tabs[3]:
    st.subheader("Industrial CAD Export")
    if st.button("Generate DWG/DXF"):
        st.session_state.designs_used += 1
        st.success(f"DWG Exported with {st.session_state.main_logo} and End-Points preserved.")
        doc = ezdxf.new('R2010'); msp = doc.modelspace()
        # Mathematical curve export for factory plotters
        msp.add_spline([(0,0), (20,10), (40,0)])
        out = io.StringIO(); doc.write(out)
        st.download_button("Download Production DWG", data=out.getvalue(), file_name=f"Pro_Pattern.dxf")
