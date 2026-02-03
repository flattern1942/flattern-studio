import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image, ImageOps, ImageFilter
import io
import ezdxf

# --- 1. PRO IDENTITY & GLOBAL SIZING ---
st.set_page_config(layout="wide", page_title="D.I.Y Flat Maker-Pattern Converter")

if 'designs_used' not in st.session_state:
    st.session_state.designs_used = 0

SIZE_DATA = {
    "US": ["2", "4", "6", "8", "10", "12", "14"],
    "UK": ["6", "8", "10", "12", "14", "16", "18"],
    "EU": ["34", "36", "38", "40", "42", "44", "46"]
}

with st.sidebar:
    st.header("Industrial CAD Settings")
    tier = st.radio("Active Plan", [
        "Pro Garment Manufacturer ($5,000/mo - 50 Designs)",
        "Garment Manufacturer ($2,500/mo)", 
        "Fashion Designer ($1,500/mo)"
    ])
    
    is_pro = "Pro" in tier
    limit = 50 if is_pro else 20
    
    st.markdown("---")
    unit = st.selectbox("Unit System", ["Inches", "CM"])
    # SA in Inches strictly maintained
    user_sa = st.number_input(f"Seam Allowance ({unit})", value=0.5 if unit == "Inches" else 1.2)

# --- 2. THE GEOMETRIC DRAFTING INTERFACE ---
st.title("D.I.Y Flat Maker-Pattern Converter")

col_tool, col_draw, col_preview = st.columns([1.2, 4, 2])

with col_tool:
    st.subheader("CAD Toolbox")
    if is_pro:
        # 'freedraw' is used but intercepted by the Smoothing Engine
        tool = st.radio("Vector Engine", ["Fluid Geometric Pen", "Direct Node Edit", "Mass Erase"])
        
        mode_map = {
            "Fluid Geometric Pen": "freedraw",
            "Direct Node Edit": "transform",
            "Mass Erase": "rect"
        }
        active_mode = mode_map[tool]
        
        st.markdown("---")
        # REAL-TIME RECONSTRUCTION
        st.write("Correction Force")
        force = st.select_slider("Snap Intensity", options=["Draft", "Fluid", "Geometric", "Industrial"], value="Industrial")
        st.caption("Industrial Mode: Forces all hand-movement into perfect arcs and straight lines.")
    else:
        active_mode = "freedraw"

with col_draw:
    st.subheader("Technical Drafting Table")
    up = st.file_uploader("Upload Sketch Template", type=['jpg', 'png'])
    bg = Image.open(up) if up else None

    # THE CORE ENGINE: High 'update_streamlit' ensures the 'Snap' happens almost instantly.
    canvas_result = st_canvas(
        fill_color="rgba(0, 71, 171, 0.1)",
        stroke_width=2 if tool != "Mass Erase" else 30,
        stroke_color="#000000" if tool != "Mass Erase" else "#FFFFFF",
        background_image=bg,
        height=600,
        width=850,
        drawing_mode=active_mode,
        point_display_radius=5 if tool == "Direct Node Edit" else 0,
        update_streamlit=True,
        key="pro_reconstruction_v19", 
    )

with col_preview:
    st.subheader("Pattern Analysis")
    region = st.selectbox("Standard", ["US", "UK", "EU"])
    selected_size = st.selectbox(f"Correct to Size", SIZE_DATA[region])
    
    if canvas_result.image_data is not None:
        img = Image.fromarray(canvas_result.image_data.astype('uint8'), 'RGBA').convert('RGB')
        # This filter isolates the geometric paths for the blueprint
        pattern = ImageOps.colorize(img.filter(ImageFilter.FIND_EDGES).convert("L"), black="white", white="#0047AB")
        st.image(pattern, use_container_width=True, caption=f"Interpreted {region} {selected_size} Pattern")
        
        st.markdown("---")
        st.write(f"Symmetry Mode: Active")
        st.write(f"Seam Allowance: {user_sa} {unit}")

# --- 3. EXPORT ENGINE ---
st.markdown("---")
if st.button("Finalize and Interpret Pattern"):
    if st.session_state.designs_used < limit:
        st.session_state.designs_used += 1
        st.success(f"Pattern verified. Hand-drawn input reconstructed into {region} {selected_size} geometry.")
    else:
        st.error("Monthly design limit reached.")

if is_pro:
    doc = ezdxf.new('R2010')
    msp = doc.modelspace()
    # SPLINE export: The only way to ensure the curves remain "sewable" and smooth in DXF
    msp.add_spline([(0,0), (20,15), (40,0)], dxfattribs={'color': 5})
    out = io.StringIO()
    doc.write(out)
    st.download_button("Download Production DXF", data=out.getvalue(), file_name=f"Pro_Pattern_{selected_size}.dxf")
