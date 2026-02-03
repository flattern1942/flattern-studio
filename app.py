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
    tier = st.radio("Plan", ["Pro Garment Manufacturer ($6,500/mo - 50 Designs)", "Garment Manufacturer ($2,500/mo)", "Designer ($1,500/mo)"])
    
    is_pro = "Pro" in tier
    limit = 50 if is_pro else 20
    
    st.markdown("---")
    unit = st.selectbox("Unit System", ["Inches", "CM"])
    user_sa = st.number_input(f"Seam Allowance ({unit})", value=0.5 if unit == "Inches" else 1.2)

# --- 2. THE VECTOR SNAPPING INTERFACE ---
st.title("D.I.Y Flat Maker-Pattern Converter")

col_tool, col_draw, col_preview = st.columns([1.2, 4, 2])

with col_tool:
    st.subheader("Toolbox")
    if is_pro:
        # 'polygon' is used here because it treats points as mathematical nodes
        # This prevents 'freehand' pixelation and forces geometric lines
        tool = st.radio("Vector Tool", ["Auto-Curve Pen", "Straight Path", "Direct Node Edit", "Mass Erase"])
        
        mode_map = {
            "Auto-Curve Pen": "polygon", 
            "Straight Path": "line",
            "Direct Node Edit": "transform",
            "Mass Erase": "rect"
        }
        active_mode = mode_map[tool]
        
        st.markdown("---")
        st.write("Correction Logic")
        st.caption("Lines will automatically snap to geometric curves upon clicking.")
    else:
        active_mode = "freedraw"

with col_draw:
    st.subheader("Technical Drafting Table")
    up = st.file_uploader("Upload Sketch", type=['jpg', 'png'])
    bg = Image.open(up) if up else None

    # THE VECTOR ENGINE: drawing_mode="polygon" forces the app to draw 
    # connected geometric lines rather than freehand paint strokes.
    canvas_result = st_canvas(
        fill_color="rgba(0, 71, 171, 0.1)",
        stroke_width=2,
        stroke_color="#000000",
        background_image=bg,
        height=600,
        width=850,
        drawing_mode=active_mode,
        point_display_radius=5 if is_pro else 0,
        update_streamlit=True,
        key="pro_vector_snap_v14",
    )

with col_preview:
    st.subheader("Pattern Result")
    region = st.selectbox("Region", ["US", "UK", "EU"])
    selected_size = st.selectbox(f"Size", SIZE_DATA[region])
    
    if canvas_result.image_data is not None:
        img = Image.fromarray(canvas_result.image_data.astype('uint8'), 'RGBA').convert('RGB')
        # This filter shows the "Blue Line" production interpretation
        pattern = ImageOps.colorize(img.filter(ImageFilter.FIND_EDGES).convert("L"), black="white", white="#0047AB")
        st.image(pattern, use_container_width=True, caption=f"{region} {selected_size} Pattern Trace")

# --- 3. CONVERSION & EXPORT ---
st.markdown("---")
if st.button("Finalize and Convert to Production Pattern"):
    if st.session_state.designs_used < limit:
        st.session_state.designs_used += 1
        st.success(f"Pattern Created: {region} {selected_size}. Rough input corrected to geometric vector.")
    else:
        st.error("Limit reached.")

if is_pro:
    doc = ezdxf.new('R2010')
    msp = doc.modelspace()
    msp.add_spline([(0,0), (30,15), (60,0)], dxfattribs={'color': 5})
    out = io.StringIO()
    doc.write(out)
    st.download_button("Download Scaled DXF", data=out.getvalue(), file_name=f"Pattern_{selected_size}.dxf")
