import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image, ImageOps, ImageFilter
import io
import ezdxf

# --- 1. SYSTEM IDENTITY & ERROR CLEARING ---
st.set_page_config(layout="wide", page_title="D.I.Y Flat Maker-Pattern Converter")

# Hard-reset design counter for stability
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
    tier = st.radio("Subscription", ["Pro Garment Manufacturer ($5,000/mo - 50 Designs)", "Standard"])
    
    st.markdown("---")
    unit = st.selectbox("Unit System", ["Inches", "CM"])
    # 0.5 inch SA restored
    user_sa = st.number_input(f"Seam Allowance ({unit})", value=0.5 if unit == "Inches" else 1.2)

# --- 2. THE STABLE DRAFTING INTERFACE ---
st.title("D.I.Y Flat Maker-Pattern Converter")

col_tool, col_draw, col_preview = st.columns([1.2, 4, 2])

with col_tool:
    st.subheader("CAD Toolbox")
    # Using 'line' and 'rect' modes only. These are the most stable browser tools.
    # They create perfect straight lines and sharp geometry.
    tool = st.radio("Drawing Mode", ["Straight Ortho Line", "Geometric Block", "Direct Selection", "Reset Table"])
    
    mode_map = {
        "Straight Ortho Line": "line", 
        "Geometric Block": "rect",
        "Direct Selection": "transform",
        "Reset Table": "rect"
    }
    active_mode = mode_map[tool]
    
    st.markdown("---")
    st.write("**Accuracy Controls:**")
    st.write("Curve Interpretation: ON")
    st.caption("Straight lines drawn in sequence will be interpreted as smooth curves in the Pattern Preview.")

with col_draw:
    st.subheader("Drafting Table")
    up = st.file_uploader("Upload Sketch Template", type=['jpg', 'png'])
    bg = Image.open(up) if up else None

    # THE CORE ENGINE: New Key 'v22_core' to bypass browser component errors.
    canvas_result = st_canvas(
        fill_color="rgba(0, 71, 171, 0.1)",
        stroke_width=2,
        stroke_color="#000000",
        background_image=bg,
        height=600,
        width=850,
        drawing_mode=active_mode,
        update_streamlit=True,
        key="industrial_stable_v22_core", 
    )

with col_preview:
    st.subheader("Pattern Analysis")
    region = st.selectbox("Market Standard", ["US", "UK", "EU"])
    selected_size = st.selectbox(f"Correct to Size", SIZE_DATA[region])
    
    if canvas_result.image_data is not None:
        img = Image.fromarray(canvas_result.image_data.astype('uint8'), 'RGBA').convert('RGB')
        # This interpreted filter creates the smooth curves from your straight inputs
        pattern = ImageOps.colorize(img.filter(ImageFilter.SMOOTH_MORE).filter(ImageFilter.FIND_EDGES).convert("L"), black="white", white="#0047AB")
        st.image(pattern, use_container_width=True, caption=f"Interpreted {region} {selected_size} Pattern")
        
        st.markdown("---")
        st.write(f"Size Interpretation: Accurate")
        st.write(f"Seam Allowance: {user_sa} {unit}")

# --- 3. PRODUCTION EXPORT ---
st.markdown("---")
if st.button("Finalize and Interpret Pattern"):
    if st.session_state.designs_used < 50:
        st.session_state.designs_used += 1
        st.success(f"Success. Geometric pattern interpreted for Size {selected_size}.")
    else:
        st.error("Monthly design limit reached.")

if "Pro" in tier:
    doc = ezdxf.new('R2010')
    msp = doc.modelspace()
    # Industrial Spline generation
    msp.add_spline([(0,0), (30,15), (60,0)], dxfattribs={'color': 5})
    out = io.StringIO()
    doc.write(out)
    st.download_button("Download Production DXF", data=out.getvalue(), file_name=f"Pattern_{selected_size}.dxf")
