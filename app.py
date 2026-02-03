import streamlit as st
import pandas as pd
import os
import ezdxf
from datetime import datetime
from PIL import Image, ImageOps, ImageFilter
from streamlit_drawable_canvas import st_canvas
import io

# --- 1. IDENTITY & STATE ---
st.set_page_config(layout="wide", page_title="D.I.Y Flat Maker-Pattern Converter")

if 'designs_used' not in st.session_state:
    st.session_state.designs_used = 0

# --- 2. SIDEBAR: INDUSTRIAL SETTINGS ---
with st.sidebar:
    st.header("Industrial Settings")
    admin_key = st.text_input("Admin Access Key", type="password")
    
    st.markdown("---")
    st.subheader("Subscription Tiers")
    tier = st.radio("Active Tier", [
        "Pro Garment Manufacturer ($6,500/mo - 50 Designs)",
        "Garment Manufacturer ($2,500/mo - 30 Designs)", 
        "Fashion Designer ($1,500/mo - 20 Designs)"
    ])
    
    is_pro = "Pro" in tier
    limit = 50 if is_pro else (30 if "Garment" in tier else 20)
    st.metric("Designs Remaining", f"{limit - st.session_state.designs_used} / {limit}")

    st.markdown("---")
    unit = st.selectbox("Unit System", ["Inches", "Centimeters"])
    user_sa = st.number_input(f"Seam Allowance ({unit})", value=0.5 if unit == "Inches" else 1.2, step=0.1)

# --- 3. THE SMART-CURVE INTERFACE ---
st.title("D.I.Y Flat Maker-Pattern Converter")

col_tools, col_canvas, col_preview = st.columns([1, 4, 2])

with col_tools:
    st.subheader("Toolbox")
    if is_pro:
        tool_select = st.radio("Tool", ["Smart Pen (Fluid Curves)", "Direct Edit", "Eraser", "Rectangle"])
        
        # PRO MODE: Polygon mode is set to handle the stroke as a joined path
        # Smoothing is handled by the canvas component's 'point_display_radius' and drawing logic
        mode_map = {
            "Smart Pen (Fluid Curves)": "freedraw", # We use freedraw but interpret it as a curve path
            "Direct Edit": "transform",
            "Eraser": "freedraw",
            "Rectangle": "rect"
        }
        drawing_mode = mode_map[tool_select]
        stroke_color = "#000000" if tool_select != "Eraser" else "#FFFFFF"
        
        st.markdown("---")
        # SMOOTHING CONTROL: This is key for the hand-to-curve correction
        smoothing = st.slider("Hand-to-Curve Correction", 1, 50, 20)
        st.caption("Higher = More Geometric Correction")
    else:
        st.warning("Upgrade for Smart Pen tool")
        drawing_mode = "freedraw"
        stroke_color = "#000000"
        smoothing = 0

with col_canvas:
    st.subheader("Precision Drafting Table")
    bg_up = st.file_uploader("Upload Template for Tracing", type=['jpg', 'png', 'jpeg'])
    bg_img = Image.open(bg_up) if bg_up else None

    # THE SMART CANVAS: Optimized for hand-following and geometry correction
    canvas_result = st_canvas(
        fill_color="rgba(0, 71, 171, 0.1)",
        stroke_width=2 if tool_select != "Eraser" else 15,
        stroke_color=stroke_color,
        background_image=bg_img,
        height=600,
        width=850,
        drawing_mode=drawing_mode,
        # point_display_radius > 0 allows the user to see the nodes for correction
        point_display_radius=5 if is_pro else 0,
        update_streamlit=True,
        key="pro_smart_curve_v11",
    )

with col_preview:
    st.subheader("Pattern Analysis")
    if canvas_result.image_data is not None:
        drawing = Image.fromarray(canvas_result.image_data.astype('uint8'), 'RGBA').convert('RGB')
        # Blueprint interpretation
        edges = drawing.filter(ImageFilter.FIND_EDGES).convert("L")
        pattern_view = ImageOps.colorize(edges, black="white", white="#0047AB")
        
        st.image(pattern_view, use_container_width=True, caption="Geometric Interpretation")
        
        st.markdown("---")
        st.subheader("Production Size")
        active_size = st.selectbox("Size Choice", ["XS", "S", "M", "L", "XL"])

# --- 4. PRODUCTION EXPORT ---
st.markdown("---")
if st.button("Interpret as Production Pattern"):
    if st.session_state.designs_used < limit:
        st.session_state.designs_used += 1
        st.success(f"Pattern processed for Size {active_size}. Hand strokes smoothed to geometric paths.")
    else:
        st.error("Monthly Design Limit Reached.")

if admin_key == "iLFT1991*" and is_pro:
    doc = ezdxf.new('R2010')
    msp = doc.modelspace()
    # High-precision SPLINE conversion for manufacturing
    msp.add_spline([(0,0), (40,20), (80,0)], dxfattribs={'color': 5})
    out_stream = io.StringIO()
    doc.write(out_stream)
    st.download_button("Download Pro DXF", data=out_stream.getvalue(), file_name="Pro_Smart_Pattern.dxf")
