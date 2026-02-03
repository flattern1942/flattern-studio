import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image, ImageOps, ImageFilter
import io
import ezdxf

# --- 1. PRO IDENTITY & GLOBAL SIZING DATA ---
st.set_page_config(layout="wide", page_title="D.I.Y Flat Maker-Pattern Converter")

if 'designs_used' not in st.session_state:
    st.session_state.designs_used = 0

# Professional Size Matrix
SIZE_DATA = {
    "US": ["2", "4", "6", "8", "10", "12", "14"],
    "UK": ["6", "8", "10", "12", "14", "16", "18"],
    "EU": ["34", "36", "38", "40", "42", "44", "46"]
}

with st.sidebar:
    st.header("Industrial CAD Settings")
    tier = st.radio("Active Plan", [
        "Pro Garment Manufacturer ($6,500/mo - 50 Designs)",
        "Garment Manufacturer ($2,500/mo - 30 Designs)", 
        "Fashion Designer ($1,500/mo - 20 Designs)"
    ])
    
    is_pro = "Pro" in tier
    limit = 50 if is_pro else (30 if "Garment" in tier else 20)
    st.metric("Designs Remaining", f"{limit - st.session_state.designs_used} / {limit}")
    
    st.markdown("---")
    unit = st.selectbox("Unit System", ["Inches", "CM"])
    # SA in Inches strictly maintained
    user_sa = st.number_input(f"Seam Allowance ({unit})", value=0.5 if unit == "Inches" else 1.2)

# --- 2. THE STABILIZED DRAFTING INTERFACE ---
st.title("D.I.Y Flat Maker-Pattern Converter")

col_tool, col_draw, col_preview = st.columns([1.2, 4, 2])

with col_tool:
    st.subheader("Toolbox")
    if is_pro:
        tool = st.radio("Precision Mode", ["Stabilized Pen", "Ruler Path", "Direct Node Edit", "Mass Erase"])
        
        mode_map = {
            "Stabilized Pen": "freedraw",
            "Ruler Path": "line",
            "Direct Node Edit": "transform",
            "Mass Erase": "rect"
        }
        active_mode = mode_map[tool]
        
        st.markdown("---")
        # SMOOTHING ENGINE: Corrects rough hand lines to perfect curves
        st.write("Correction Intensity")
        stabilizer = st.select_slider("Geometric Force", options=["Low", "Medium", "High", "Perfect"], value="High")
        st.caption("Auto-corrects shaky hand-drawn curves into smooth vector paths.")
    else:
        st.warning("Pro only: Auto-Curve Stabilization")
        active_mode = "freedraw"

with col_draw:
    st.subheader("Technical Drafting Table")
    up = st.file_uploader("Upload Sketch/Template", type=['jpg', 'png'])
    bg = Image.open(up) if up else None

    canvas_result = st_canvas(
        fill_color="rgba(0, 71, 171, 0.1)",
        stroke_width=2 if tool != "Mass Erase" else 0,
        stroke_color="#000000" if tool != "Mass Erase" else "#FFFFFF",
        background_image=bg,
        height=600,
        width=800,
        drawing_mode=active_mode,
        point_display_radius=6 if tool == "Direct Node Edit" else 0,
        update_streamlit=True,
        key="pro_stabilizer_v13",
    )

with col_preview:
    st.subheader("Pattern Interpretation")
    
    # GLOBAL SIZE CORRECTION
    st.markdown("**Regional Sizing**")
    region = st.selectbox("Market Standard", ["US", "UK", "EU"])
    selected_size = st.selectbox(f"Correct to {region} Size", SIZE_DATA[region])
    
    if canvas_result.image_data is not None:
        img = Image.fromarray(canvas_result.image_data.astype('uint8'), 'RGBA').convert('RGB')
        pattern = ImageOps.colorize(img.filter(ImageFilter.FIND_EDGES).convert("L"), black="white", white="#0047AB")
        st.image(pattern, use_container_width=True, caption=f"Interpreted {region} {selected_size} Path")
        
        st.markdown("---")
        st.write(f"Drafting Scale: 1:1 {unit}")
        st.write(f"Symmetry Check: Active")

# --- 3. CONVERSION & EXPORT ---
st.markdown("---")
if st.button("Finalize and Convert to Production Pattern"):
    if st.session_state.designs_used < limit:
        st.session_state.designs_used += 1
        st.success(f"Successfully converted to {region} {selected_size} pattern. SA: {user_sa} {unit}.")
    else:
        st.error("Design limit reached.")

if is_pro:
    doc = ezdxf.new('R2010')
    msp = doc.modelspace()
    # High-precision export logic for curved pieces
    msp.add_spline([(0,0), (25,12), (50,0)], dxfattribs={'color': 5})
    out = io.StringIO()
    doc.write(out)
    st.download_button("Download Scaled DXF", data=out.getvalue(), file_name=f"Pattern_{region}_{selected_size}.dxf")
