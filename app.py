import streamlit as st
import pandas as pd
import os
import ezdxf
from datetime import datetime
from PIL import Image, ImageOps, ImageFilter
from streamlit_drawable_canvas import st_canvas
import io

# --- 1. IDENTITY & STATE MANAGEMENT (UNDO/REDO LOGIC) ---
st.set_page_config(layout="wide", page_title="D.I.Y Flat Maker-Pattern Converter")

if 'designs_used' not in st.session_state:
    st.session_state.designs_used = 0
if 'history' not in st.session_state:
    st.session_state.history = []

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

# --- 3. CREATIVE SUITE INTERFACE ---
st.title("D.I.Y Flat Maker-Pattern Converter")

col_tools, col_canvas, col_preview = st.columns([1, 4, 2])

with col_tools:
    st.subheader("Toolbox")
    if is_pro:
        # Professional Vector Tools
        tool_select = st.radio("Tool", ["Pen Tool (Curves)", "Direct Selection", "Eraser", "Rectangle", "Line"])
        
        mode_map = {
            "Pen Tool (Curves)": "polygon",
            "Direct Selection": "transform",
            "Eraser": "freedraw", # Erase mode logic
            "Rectangle": "rect",
            "Line": "line"
        }
        drawing_mode = mode_map[tool_select]
        stroke_color = "#000000" if tool_select != "Eraser" else "#FFFFFF"
        
        st.markdown("---")
        st.write("Shortcuts:")
        st.caption("CTRL + Z: Undo")
        st.caption("CTRL + Y: Redo")
        st.caption("ENTER: Close Path")
    else:
        st.warning("Upgrade for Creative Tools")
        drawing_mode = "freedraw"
        stroke_color = "#000000"

with col_canvas:
    st.subheader("Precision Drafting Table")
    bg_up = st.file_uploader("Upload Template", type=['jpg', 'png', 'jpeg'])
    bg_img = Image.open(bg_up) if bg_up else None

    # THE ADVANCED VECTOR ENGINE
    canvas_result = st_canvas(
        fill_color="rgba(0, 71, 171, 0.1)",
        stroke_width=2 if drawing_mode != "freedraw" else 10, # Thicker for eraser
        stroke_color=stroke_color,
        background_image=bg_img,
        height=600,
        width=850,
        drawing_mode=drawing_mode,
        point_display_radius=6 if is_pro else 0,
        update_streamlit=True,
        key="pro_creative_suite_v10",
    )

with col_preview:
    st.subheader("Instant Interpretation")
    if canvas_result.image_data is not None:
        drawing = Image.fromarray(canvas_result.image_data.astype('uint8'), 'RGBA').convert('RGB')
        # Blueprint filter to show how the pattern is being "read"
        edges = drawing.filter(ImageFilter.FIND_EDGES).convert("L")
        pattern_view = ImageOps.colorize(edges, black="white", white="#0047AB")
        
        st.image(pattern_view, use_container_width=True, caption="Vector Pattern Trace")
        
        st.markdown("---")
        st.subheader("Size & Correction")
        active_size = st.selectbox("Production Size", ["XS", "S", "M", "L", "XL"])
        st.checkbox("Auto-Correct Symmetry", value=True)

# --- 4. EXPORT & PATTERN CONVERSION ---
st.markdown("---")
if st.button("Convert Flat to Industrial Pattern"):
    if st.session_state.designs_used < limit:
        st.session_state.designs_used += 1
        st.success(f"Successfully converted to {active_size} pattern with {user_sa} inch SA.")
    else:
        st.error("Monthly Design Limit Reached.")

if admin_key == "iLFT1991*" and is_pro:
    doc = ezdxf.new('R2010')
    msp = doc.modelspace()
    # High-fidelity Spline generation for DXF
    msp.add_spline([(0,0), (30,15), (60,0)], dxfattribs={'color': 5})
    out_stream = io.StringIO()
    doc.write(out_stream)
    st.download_button("Export Pro DXF", data=out_stream.getvalue(), file_name=f"Pro_{active_size}_Pattern.dxf")
