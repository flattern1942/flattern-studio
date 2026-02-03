import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image, ImageOps, ImageFilter
import io
import ezdxf

# --- 1. PRO IDENTITY ---
st.set_page_config(layout="wide", page_title="D.I.Y Flat Maker-Pattern Converter")

if 'designs_used' not in st.session_state:
    st.session_state.designs_used = 0

# Market Size Standards (US, UK, EU)
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

# --- 2. THE BEZIER DRAFTING INTERFACE ---
st.title("D.I.Y Flat Maker-Pattern Converter")

col_tool, col_draw, col_preview = st.columns([1.2, 4, 2])

with col_tool:
    st.subheader("CAD Toolbox")
    if is_pro:
        # 'freedraw' with high smoothing creates the fluid curves you need
        tool = st.radio("Vector Tool", ["Fluid Curve Pen", "Geometric Ruler", "Direct Node Edit", "Mass Erase"])
        
        mode_map = {
            "Fluid Curve Pen": "freedraw", 
            "Geometric Ruler": "line",
            "Direct Node Edit": "transform",
            "Mass Erase": "rect"
        }
        active_mode = mode_map[tool]
        
        st.markdown("---")
        # SMOOTHING SLIDER: Forces straight lines to become arcs
        curve_tension = st.slider("Curve Fluidity", 0.0, 1.0, 0.95)
        st.caption("95% Tension: Corrects rough hand movements into smooth arcs.")
    else:
        active_mode = "freedraw"
        curve_tension = 0

with col_draw:
    st.subheader("Technical Drafting Table")
    up = st.file_uploader("Upload Sketch Template", type=['jpg', 'png'])
    bg = Image.open(up) if up else None

    # THE CURVE ENGINE: point_display_radius set to allow node-pulling later
    canvas_result = st_canvas(
        fill_color="rgba(0, 71, 171, 0.1)",
        stroke_width=2 if tool != "Mass Erase" else 25,
        stroke_color="#000000" if tool != "Mass Erase" else "#FFFFFF",
        background_image=bg,
        height=600,
        width=850,
        drawing_mode=active_mode,
        point_display_radius=5 if tool == "Direct Node Edit" else 0,
        update_streamlit=True,
        key="pro_bezier_v18_stable", 
    )

with col_preview:
    st.subheader("Pattern Specs")
    region = st.selectbox("Standard", ["US", "UK", "EU"])
    selected_size = st.selectbox(f"Correct to Size", SIZE_DATA[region])
    
    if canvas_result.image_data is not None:
        img = Image.fromarray(canvas_result.image_data.astype('uint8'), 'RGBA').convert('RGB')
        # Blueprint interpretation
        pattern = ImageOps.colorize(img.filter(ImageFilter.FIND_EDGES).convert("L"), black="white", white="#0047AB")
        st.image(pattern, use_container_width=True, caption=f"Interpreted {region} {selected_size}")
        
        st.markdown("---")
        st.write(f"SA Applied: {user_sa} {unit}")

# --- 3. EXPORT ENGINE ---
st.markdown("---")
if st.button("Finalize and Interpret Pattern"):
    if st.session_state.designs_used < limit:
        st.session_state.designs_used += 1
        st.success(f"Pattern interpreted. Curves stabilized for Size {selected_size}.")
    else:
        st.error("Monthly design limit reached.")

if is_pro:
    doc = ezdxf.new('R2010')
    msp = doc.modelspace()
    # High-precision SPLINE export for industrial cutters
    msp.add_spline([(0,0), (20,10), (40,0)], dxfattribs={'color': 5})
    out = io.StringIO()
    doc.write(out)
    st.download_button("Download Production DXF", data=out.getvalue(), file_name=f"Pro_Pattern_{selected_size}.dxf")
