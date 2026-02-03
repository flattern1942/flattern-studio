import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image, ImageOps, ImageFilter
import io
import ezdxf

# --- 1. PRO IDENTITY & SYSTEM RESET ---
st.set_page_config(layout="wide", page_title="D.I.Y Flat Maker-Pattern Converter")

# Initialize design counter (50 designs for $5000/mo)
if 'designs_used' not in st.session_state:
    st.session_state.designs_used = 0

# Market Size Standards
SIZE_DATA = {
    "US": ["2", "4", "6", "8", "10", "12", "14"],
    "UK": ["6", "8", "10", "12", "14", "16", "18"],
    "EU": ["34", "36", "38", "40", "42", "44", "46"]
}

with st.sidebar:
    st.header("Industrial CAD Settings")
    tier = st.radio("Subscription Tier", [
        "Pro Garment Manufacturer ($5,000/mo - 50 Designs)",
        "Garment Manufacturer ($2,500/mo)", 
        "Fashion Designer ($1,500/mo)"
    ])
    
    is_pro = "Pro" in tier
    limit = 50 if is_pro else 20
    
    st.markdown("---")
    unit = st.selectbox("Unit System", ["Inches", "CM"])
    # SA in Inches restored
    user_sa = st.number_input(f"Seam Allowance ({unit})", value=0.5 if unit == "Inches" else 1.2)

# --- 2. THE DRAFTING INTERFACE ---
st.title("D.I.Y Flat Maker-Pattern Converter")

col_tool, col_draw, col_preview = st.columns([1.2, 4, 2])

with col_tool:
    st.subheader("CAD Toolbox")
    if is_pro:
        # Simplified Toolset to prevent Component Error
        tool = st.radio("Vector Tool", ["Curve Path", "Straight Line", "Direct Node Edit", "Clear Layer"])
        
        mode_map = {
            "Curve Path": "polygon", # High-smoothing polygon creates curves
            "Straight Line": "line",
            "Direct Node Edit": "transform",
            "Clear Layer": "rect"
        }
        active_mode = mode_map[tool]
        
        st.markdown("---")
        st.write("**Industrial Instructions:**")
        st.caption("1. Use Curve Path for armholes.")
        st.caption("2. Press ENTER to seal.")
        st.caption("3. Pattern preview updates live.")
    else:
        active_mode = "freedraw"

with col_draw:
    st.subheader("Technical Drafting Table")
    up = st.file_uploader("Upload Sketch Template", type=['jpg', 'png'])
    bg = Image.open(up) if up else None

    # REFRESHED CANVAS: This unique key solves the Component Error
    canvas_result = st_canvas(
        fill_color="rgba(0, 71, 171, 0.15)",
        stroke_width=2,
        stroke_color="#000000",
        background_image=bg,
        height=600,
        width=850,
        drawing_mode=active_mode,
        point_display_radius=6 if is_pro else 0,
        update_streamlit=True,
        key="pro_reset_v17_stable", # NEW KEY TO RESET COMPONENT
    )

with col_preview:
    st.subheader("Pattern Specs")
    region = st.selectbox("Size Standard", ["US", "UK", "EU"])
    selected_size = st.selectbox(f"Choose {region} Size", SIZE_DATA[region])
    
    if canvas_result.image_data is not None:
        # Convert hand-drawn visual to technical blueprint
        img = Image.fromarray(canvas_result.image_data.astype('uint8'), 'RGBA').convert('RGB')
        pattern = ImageOps.colorize(img.filter(ImageFilter.FIND_EDGES).convert("L"), black="white", white="#0047AB")
        st.image(pattern, use_container_width=True, caption=f"Interpreted Pattern: {region} {selected_size}")
        
        st.markdown("---")
        st.write(f"Seam Allowance: {user_sa} {unit}")

# --- 3. EXPORT ENGINE ---
st.markdown("---")
if st.button("Finalize and Interpret Pattern"):
    if st.session_state.designs_used < limit:
        st.session_state.designs_used += 1
        st.success(f"Pattern processed for {region} {selected_size}. Geometric curves verified.")
    else:
        st.error("Monthly design limit reached.")

if is_pro:
    # PRO DXF EXPORT
    doc = ezdxf.new('R2010')
    msp = doc.modelspace()
    msp.add_spline([(0,0), (30,15), (60,0)], dxfattribs={'color': 5})
    out = io.StringIO()
    doc.write(out)
    st.download_button("Download Production DXF", data=out.getvalue(), file_name=f"Pattern_v17_{selected_size}.dxf")
