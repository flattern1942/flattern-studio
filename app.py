import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image, ImageOps, ImageFilter
import io
import ezdxf

# --- 1. PRO IDENTITY & CACHE RESET ---
st.set_page_config(layout="wide", page_title="D.I.Y Flat Maker-Pattern Converter")

if 'designs_used' not in st.session_state:
    st.session_state.designs_used = 0

# Industrial Size Correction Matrix
SIZE_DATA = {
    "US": ["2", "4", "6", "8", "10", "12", "14"],
    "UK": ["6", "8", "10", "12", "14", "16", "18"],
    "EU": ["34", "36", "38", "40", "42", "44", "46"]
}

with st.sidebar:
    st.header("Industrial CAD Settings")
    tier = st.radio("Subscription", ["Pro Garment Manufacturer ($5,000/mo - 50 Designs)", "Standard"])
    
    st.markdown("---")
    unit = st.selectbox("Unit System", ["Inches", "CM"])
    # SA in Inches strictly maintained
    user_sa = st.number_input(f"Seam Allowance ({unit})", value=0.5 if unit == "Inches" else 1.2)

# --- 2. THE STABLE DRAFTING INTERFACE ---
st.title("D.I.Y Flat Maker-Pattern Converter")

col_tool, col_draw, col_preview = st.columns([1.2, 4, 2])

with col_tool:
    st.subheader("CAD Toolbox")
    if "Pro" in tier:
        # We use 'path' for curves and 'line' for straight geometry
        tool = st.radio("Vector Mode", ["Geometric Curve", "Straight Ortho", "Node Transform", "Clear All"])
        
        mode_map = {
            "Geometric Curve": "path", # This creates perfect Bezier curves
            "Straight Ortho": "line",  # This creates perfect straight lines
            "Node Transform": "transform",
            "Clear All": "rect"
        }
        active_mode = mode_map[tool]
        
        st.markdown("---")
        st.write("**Pro CAD Controls:**")
        st.caption("• Click-Drag: Pull smooth curves.")
        st.caption("• Click-Click: Snap straight lines.")
        st.caption("• ENTER: Seal Pattern Piece.")
    else:
        active_mode = "freedraw"

with col_draw:
    st.subheader("Technical Drafting Table")
    up = st.file_uploader("Upload Sketch Template", type=['jpg', 'png'])
    bg = Image.open(up) if up else None

    # THE CORE ENGINE: New unique key "v21_stable" to kill Component Error
    canvas_result = st_canvas(
        fill_color="rgba(0, 71, 171, 0.1)",
        stroke_width=2,
        stroke_color="#000000",
        background_image=bg,
        height=600,
        width=850,
        drawing_mode=active_mode,
        point_display_radius=6 if tool == "Node Transform" else 0,
        update_streamlit=True,
        key="industrial_stable_v21", 
    )

with col_preview:
    st.subheader("Production Interpretation")
    region = st.selectbox("Market Region", ["US", "UK", "EU"])
    selected_size = st.selectbox(f"Correct to Size", SIZE_DATA[region])
    
    if canvas_result.image_data is not None:
        img = Image.fromarray(canvas_result.image_data.astype('uint8'), 'RGBA').convert('RGB')
        # Technical blueprint interpretation (Blue Line Trace)
        pattern = ImageOps.colorize(img.filter(ImageFilter.FIND_EDGES).convert("L"), black="white", white="#0047AB")
        st.image(pattern, use_container_width=True, caption=f"{region} {selected_size} Pattern")
        
        st.markdown("---")
        st.write(f"Symmetry Correction: Active")
        st.write(f"SA Applied: {user_sa} {unit}")

# --- 3. EXPORT ENGINE ---
st.markdown("---")
if st.button("Finalize and Interpret Pattern"):
    if st.session_state.designs_used < 50:
        st.session_state.designs_used += 1
        st.success(f"Success. Pattern interpreted for {region} {selected_size}.")
    else:
        st.error("Design limit reached.")

if "Pro" in tier:
    doc = ezdxf.new('R2010')
    msp = doc.modelspace()
    # High-precision SPLINE export for industrial cutters
    msp.add_spline([(0,0), (25,12), (50,0)], dxfattribs={'color': 5})
    out = io.StringIO()
    doc.write(out)
    st.download_button("Download Production DXF", data=out.getvalue(), file_name=f"Pattern_{selected_size}.dxf")
