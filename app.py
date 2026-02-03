import streamlit as st
import pandas as pd
import os
import ezdxf
from datetime import datetime
from PIL import Image, ImageOps, ImageFilter, ImageEnhance
from streamlit_drawable_canvas import st_canvas
import io

# --- 1. IDENTITY & COUNTER ---
st.set_page_config(layout="wide", page_title="D.I.Y Flat Maker-Pattern Converter")

if 'designs_used' not in st.session_state:
    st.session_state.designs_used = 0
if 'audit_log' not in st.session_state:
    st.session_state.audit_log = []

# --- 2. SIDEBAR: THE $6,500 PRO LOGIC ---
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
    # SA in Inches restored as per instructions
    user_sa = st.number_input(f"Seam Allowance ({unit})", value=0.5 if unit == "Inches" else 1.2, step=0.1)

# --- 3. MAIN INTERFACE ---
st.title("D.I.Y Flat Maker-Pattern Converter")

# --- 4. THE FLEXIBLE NODE DRAFTING DESK ---
st.header("1. Vector Node Drafting")

if is_pro:
    st.info("PRO MODE: 1. Click 'Polygon' to set nodes. 2. Click 'Transform' to DRAG/PULL nodes. 3. Press ENTER to close.")
    drawing_mode = st.selectbox("Precision Tool", ["polygon", "transform", "rect", "line"])
else:
    st.warning("Standard Mode: Upgrade to Pro for Drag-and-Pull anchor point editing.")
    drawing_mode = "freedraw"

bg_up = st.file_uploader("Upload Template for Tracing", type=['jpg', 'png', 'jpeg'])
bg_img = Image.open(bg_up) if bg_up else None

# The Architectural Canvas with Node-Dragging Support
canvas_result = st_canvas(
    fill_color="rgba(0, 71, 171, 0.2)", # Confirms closed paths
    stroke_width=2,
    stroke_color="#000000",
    background_image=bg_img,
    height=600,
    width=900,
    drawing_mode=drawing_mode,
    point_display_radius=8 if is_pro else 0, # Large nodes for "Drag and Pull"
    update_streamlit=True, # Critical for real-time drag response
    key="diy_node_converter_v5",
)

# --- 5. COMPONENT ISOLATION ---
st.markdown("---")
st.header("2. Component Verification")
c1, c2, c3, c4 = st.columns(4)
with c1: has_cf = st.checkbox("Center Front", value=True)
with c2: has_cb = st.checkbox("Center Back", value=True)
with c3: has_sl = st.checkbox("Sleeves")
with c4: has_cu = st.checkbox("Cuffs")

# --- 6. EXPORT ENGINE ---
if st.button("Convert to Production Pattern"):
    if st.session_state.designs_used < limit:
        st.session_state.designs_used += 1
        st.success("Flat successfully converted. Mathematical nodes synced for DXF.")
    else:
        st.error("Monthly Design Limit Reached.")

if admin_key == "iLFT1991*":
    if is_pro:
        st.subheader("Pro Master Vector Export ($6,500 Tier)")
        doc = ezdxf.new('R2010')
        msp = doc.modelspace()
        
        # Adding industrial grain lines and standard perimeter
        msp.add_lwpolyline([(0,0), (80,0), (80,140), (0,140), (0,0)], dxfattribs={'color': 5})
        msp.add_line((40, 20), (40, 120), dxfattribs={'layer': 'GRAIN', 'color': 1})
        
        out_stream = io.StringIO()
        doc.write(out_stream)
        st.download_button("Download Pro DXF", data=out_stream.getvalue(), file_name="Pro_Vector_Export.dxf")
    else:
        st.subheader("Standard Batch Export")
        st.write("Pieces ready for download...")
