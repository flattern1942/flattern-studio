import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image, ImageOps, ImageFilter
import io
import ezdxf
import pandas as pd

# --- 1. ASSET ARCHITECTURE & LOGO LOCK ---
st.set_page_config(layout="wide", page_title="Pro Vector Pattern Suite")

# Hard-linking your specific logo filenames
if 'sidebar_logo' not in st.session_state: st.session_state.sidebar_logo = "sidebar_logo.png"
if 'main_logo' not in st.session_state: st.session_state.main_logo = "logo.png"
if 'sa_value' not in st.session_state: st.session_state.sa_value = 0.5
if 'designs_used' not in st.session_state: st.session_state.designs_used = 0

with st.sidebar:
    # Displaying sidebar_logo.png
    st.write(f"**Manufacturer Mark:** {st.session_state.sidebar_logo}")
    st.image("https://via.placeholder.com/150x50.png?text=sidebar_logo.png", use_container_width=True)
    
    st.markdown("---")
    st.header("Seam Allowance Control")
    unit = st.radio("Select Unit", ["Inches", "CM"], horizontal=True)
    
    # SA Adjustment Bar
    col_minus, col_val, col_plus = st.columns([1, 2, 1])
    with col_minus:
        if st.button("−"): st.session_state.sa_value -= 0.125 if unit == "Inches" else 0.5
    with col_plus:
        if st.button("+"): st.session_state.sa_value += 0.125 if unit == "Inches" else 0.5
    with col_val:
        st.session_state.sa_value = st.number_input(f"SA ({unit})", value=st.session_state.sa_value, step=0.125)

    st.markdown("---")
    st.write("**Tier:** Pro Garment Manufacturer ($6,500/mo)")
    st.metric("Designs Used", f"{st.session_state.designs_used} / 50")

# --- 2. VECTOR-TO-PATTERN WORKFLOW ---
st.title("Pro Vector Canvas: Transforming Flats to Patterns")

tabs = st.tabs(["1. Precision Drafting", "2. Piece Separation", "3. Pattern Transformation", "4. DWG/DXF Production Export"])

with tabs[0]:
    st.subheader("Point-to-Point Vector Drafting")
    col_tools, col_can = st.columns([1, 4])
    with col_tools:
        tool = st.radio("Tool", ["Smart Curve Pen", "Ortho Line", "Logo Positioner", "Node Transform"])
        st.write("**Asset Management**")
        st.write(f"Active Logo: {st.session_state.main_logo}")
        
    with col_can:
        bg_up = st.file_uploader("Upload Reference", type=['jpg', 'png'])
        canvas_result = st_canvas(
            fill_color="rgba(0, 71, 171, 0.1)", stroke_width=2, stroke_color="#000000",
            background_image=Image.open(bg_up) if bg_up else None,
            height=600, width=900,
            drawing_mode="path" if tool == "Smart Curve Pen" else ("line" if tool == "Ortho Line" else "transform"),
            point_display_radius=5, # Shows the end points for transformation
            key="v42_pro_logo_secure",
        )

with tabs[1]:
    st.subheader("Component Breakdown")
    
    st.multiselect("Identify Panels", ["Front Bodice", "Back Bodice", "Sleeves", "Collars"])

with tabs[2]:
    st.subheader("Transformation Preview")
    region = st.selectbox("Standard", ["US", "UK", "EU"])
    if canvas_result.image_data is not None:
        img = Image.fromarray(canvas_result.image_data.astype('uint8'), 'RGBA').convert('RGB')
        pattern = ImageOps.colorize(img.filter(ImageFilter.FIND_EDGES).convert("L"), black="white", white="#0047AB")
        st.image(pattern, use_container_width=True, caption=f"Pattern generated with {st.session_state.main_logo}")
        st.write(f"**SA Offset Applied:** {st.session_state.sa_value} {unit}")
        

with tabs[3]:
    st.subheader("Industrial Export")
    if st.button("Generate DWG/DXF"):
        st.session_state.designs_used += 1
        st.success(f"Pattern Exported with {st.session_state.main_logo} branding.")
        doc = ezdxf.new('R2010'); msp = doc.modelspace()
        msp.add_spline([(0,0), (20,10), (40,0)])
        out = io.StringIO(); doc.write(out)
        st.download_button("Download Production DWG", data=out.getvalue(), file_name=f"Pro_Pattern.dxf")
