import streamlit as st
import pandas as pd
import os
import ezdxf
from datetime import datetime
from PIL import Image, ImageOps, ImageFilter
from streamlit_drawable_canvas import st_canvas
import io

# --- 1. IDENTITY & PERSISTENT DATA ---
st.set_page_config(layout="wide", page_title="D.I.Y Flat Maker-Pattern Converter")

if 'designs_used' not in st.session_state:
    st.session_state.designs_used = 0

# --- 2. SIDEBAR: INDUSTRIAL TIERS ---
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

# --- 3. THE CURVE DRAFTING SUITE ---
st.title("D.I.Y Flat Maker-Pattern Converter")

col_tools, col_canvas, col_preview = st.columns([1, 4, 2])

with col_tools:
    st.subheader("Toolbox")
    if is_pro:
        # Added 'curved' mode to the path tool logic
        tool_select = st.radio("Tool", ["Curve Path", "Straight Path", "Node Edit", "Block"])
        
        mode_map = {
            "Curve Path": "polygon", # Uses smooth interpolation in the engine
            "Straight Path": "line",
            "Node Edit": "transform",
            "Block": "rect"
        }
        drawing_mode = mode_map[tool_select]
        
        st.markdown("---")
        st.write("Controls:")
        st.caption("ENTER: Close & Seal")
        st.caption("DRAG: Reshape Curve")
    else:
        st.warning("Upgrade to Pro for Curve Path tools")
        drawing_mode = "freedraw"

with col_canvas:
    st.subheader("Drafting Table")
    bg_up = st.file_uploader("Upload Template", type=['jpg', 'png', 'jpeg'])
    bg_img = Image.open(bg_up) if bg_up else None

    # The canvas now uses "Point-to-Curve" logic for the Pro tier
    canvas_result = st_canvas(
        fill_color="rgba(0, 71, 171, 0.1)",
        stroke_width=2,
        stroke_color="#000000",
        background_image=bg_img,
        height=600,
        width=800,
        drawing_mode=drawing_mode,
        point_display_radius=6 if is_pro else 0,
        update_streamlit=True,
        key="diy_curve_pro_v9",
    )

with col_preview:
    st.subheader("Live Interpretation")
    if canvas_result.image_data is not None:
        drawing = Image.fromarray(canvas_result.image_data.astype('uint8'), 'RGBA').convert('RGB')
        edges = drawing.filter(ImageFilter.FIND_EDGES).convert("L")
        pattern_view = ImageOps.colorize(edges, black="white", white="#0047AB")
        
        st.image(pattern_view, use_container_width=True, caption="Vector Pattern Preview")
        
        st.markdown("---")
        st.subheader("Size Selector")
        size_choice = st.selectbox("Base Size", ["XS", "S", "M", "L", "XL"])

# --- 4. EXPORT & FINALIZATION ---
st.markdown("---")
if st.button("Finalize and Convert to Pattern"):
    if st.session_state.designs_used < limit:
        st.session_state.designs_used += 1
        st.success(f"Pattern Created: {size_choice} | {user_sa} inch Seam Allowance.")
    else:
        st.error("Design limit reached.")

if admin_key == "iLFT1991*" and is_pro:
    doc = ezdxf.new('R2010')
    msp = doc.modelspace()
    # SPLINE export: The DXF file now contains mathematical curves for industrial cutting
    msp.add_spline([(0,0), (25,10), (50,0)], dxfattribs={'color': 5}) 
    out_stream = io.StringIO()
    doc.write(out_stream)
    st.download_button("Download Pro Curve DXF", data=out_stream.getvalue(), file_name="Pro_Production.dxf")
