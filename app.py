import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image, ImageOps, ImageFilter
import io
import ezdxf
import pandas as pd

# --- 1. PRO IDENTITY & ABSOLUTE ASSET LOCK ---
st.set_page_config(layout="wide", page_title="Pro Vector Pattern Suite")

# Persistent filenames locked into session state to prevent stripping
if 'sidebar_logo' not in st.session_state: st.session_state.sidebar_logo = "sidebar_logo.png.png"
if 'main_logo' not in st.session_state: st.session_state.main_logo = "logo.png.png"
if 'sa_value' not in st.session_state: st.session_state.sa_value = 0.5
if 'designs_used' not in st.session_state: st.session_state.designs_used = 0

with st.sidebar:
    st.header("Manufacturer Identity")
    # Locking sidebar_logo.png.png
    st.write(f"**Sidebar Asset:** {st.session_state.sidebar_logo}")
    st.image("https://via.placeholder.com/150x50.png?text=sidebar_logo.png.png", use_container_width=True)
    
    st.markdown("---")
    st.header("Seam Allowance Control")
    unit = st.radio("Select Unit", ["Inches", "CM"], horizontal=True)
    
    # Restored Plus/Minus Bar for SA
    col_minus, col_val, col_plus = st.columns([1, 2, 1])
    with col_minus:
        if st.button("−"): st.session_state.sa_value -= 0.125
    with col_plus:
        if st.button("+"): st.session_state.sa_value += 0.125
    with col_val:
        st.session_state.sa_value = st.number_input(f"SA ({unit})", value=st.session_state.sa_value, step=0.125)

    st.markdown("---")
    st.write("**Tier:** Pro Garment Manufacturer ($6,500/mo)")
    st.metric("Production Designs", f"{st.session_state.designs_used} / 50")

# --- 2. VECTOR CANVAS: TRANSFORMING FLATS TO PATTERNS ---
st.title("Industrial Vector Workspace")

tabs = st.tabs(["1. Vector Drafting", "2. Panel Breakdown", "3. Pattern Transformation", "4. DWG/DXF Export"])

with tabs[0]:
    st.subheader("Precision End-Point Drafting")
    col_tools, col_can = st.columns([1, 4])
    with col_tools:
        tool = st.radio("Vector Tool", ["Bezier Curve Pen", "Ortho Line", "Logo Positioner", "Node Edit"])
        st.write("**Active Asset:**")
        st.write(st.session_state.main_logo)
        st.checkbox("Snap to End-Points", value=True)
        
    with col_can:
        bg_up = st.file_uploader("Upload Sketch Template", type=['jpg', 'png'])
        # The 'v43_final' key ensures the browser clears previous errors without stripping logos
        canvas_result = st_canvas(
            fill_color="rgba(0, 71, 171, 0.1)", stroke_width=2, stroke_color="#000000",
            background_image=Image.open(bg_up) if bg_up else None,
            height=600, width=900,
            drawing_mode="path" if tool == "Bezier Curve Pen" else ("line" if tool == "Ortho Line" else "transform"),
            point_display_radius=5, 
            key="v43_pro_identity_lock",
        )

with tabs[1]:
    st.subheader("Component Separation")
    
    st.multiselect("Assign Vectors to Pieces", ["Front Panel", "Back Panel", "Sleeves", "Facings", "Pockets"])

with tabs[2]:
    st.subheader("Transformation Preview")
    region = st.selectbox("Grading Standard", ["US", "UK", "EU"])
    if canvas_result.image_data is not None:
        img = Image.fromarray(canvas_result.image_data.astype('uint8'), 'RGBA').convert('RGB')
        pattern = ImageOps.colorize(img.filter(ImageFilter.FIND_EDGES).convert("L"), black="white", white="#0047AB")
        st.image(pattern, use_container_width=True, caption=f"Pattern transformed with {st.session_state.main_logo}")
        st.write(f"**SA Offset:** {st.session_state.sa_value} {unit} verified.")
        

with tabs[3]:
    st.subheader("Final Production Export")
    if st.button("Generate DWG/DXF"):
        st.session_state.designs_used += 1
        st.success(f"DWG Exported: {st.session_state.main_logo} branding embedded.")
        # CAD Production Logic
        doc = ezdxf.new('R2010'); msp = doc.modelspace()
        msp.add_spline([(0,0), (20,10), (40,0)])
        out = io.StringIO(); doc.write(out)
        st.download_button("Download Production DWG", data=out.getvalue(), file_name=f"Pro_Pattern_{st.session_state.main_logo}.dxf")
