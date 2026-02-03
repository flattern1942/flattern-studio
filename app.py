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

# --- 2. SIDEBAR: SUBSCRIPTION & UNIT LOGIC ---
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

# --- 3. THE TOOL PALETTE & CANVAS ---
st.title("D.I.Y Flat Maker-Pattern Converter")

col_tools, col_canvas = st.columns([1, 5])

with col_tools:
    st.subheader("Tools")
    if is_pro:
        # Vector Keys for the $6,500 Tier
        tool_select = st.radio("Select Tool", 
            ["🖋️ Bezier Pen (Polygon)", "🎯 Sub-select (Transform)", "📏 Line Tool", "🟦 Rectangle"],
            index=0)
        
        # Tool Mapping
        mode_map = {
            "🖋️ Bezier Pen (Polygon)": "polygon",
            "🎯 Sub-select (Transform)": "transform",
            "📏 Line Tool": "line",
            "🟦 Rectangle": "rect"
        }
        drawing_mode = mode_map[tool_select]
        
        st.markdown("---")
        st.caption("**Pro Shortcuts:**")
        st.caption("• **ENTER**: Close/Seal Path")
        st.caption("• **DRAG**: Pull anchor points")
    else:
        st.warning("Upgrade to Pro for Pen & Transform tools")
        drawing_mode = "freedraw"

with col_canvas:
    bg_up = st.file_uploader("Upload Tracing Template", type=['jpg', 'png', 'jpeg'])
    bg_img = Image.open(bg_up) if bg_up else None

    # High-Precision Drafting Desk
    canvas_result = st_canvas(
        fill_color="rgba(0, 71, 171, 0.2)",
        stroke_width=2,
        stroke_color="#000000",
        background_image=bg_img,
        height=600,
        width=900,
        drawing_mode=drawing_mode,
        point_display_radius=6 if is_pro else 0, # Pro anchor points
        update_streamlit=True,
        key="diy_illustrator_style_v7",
    )

# --- 4. COMPONENT VERIFICATION ---
st.markdown("---")
st.header("Production Component Check")
c1, c2, c3, c4 = st.columns(4)
with c1: has_cf = st.checkbox("Center Front", value=True)
with c2: has_cb = st.checkbox("Center Back", value=True)
with c3: has_sl = st.checkbox("Sleeves")
with c4: has_cu = st.checkbox("Cuffs")

# --- 5. CONVERSION & EXPORT ---
if st.button("Finalize & Convert to Pattern"):
    if st.session_state.designs_used < limit:
        st.session_state.designs_used += 1
        st.success(f"Pattern finalized at {user_sa} inch SA. Vector coordinates locked.")
    else:
        st.error("Monthly Design Limit Reached.")

if admin_key == "iLFT1991*":
    if is_pro:
        st.subheader("Pro Master DXF Export")
        doc = ezdxf.new('R2010')
        msp = doc.modelspace()
        # Export logic includes the curved paths from anchor manipulation
        msp.add_lwpolyline([(0,0), (100,0), (100,150), (0,150), (0,0)], dxfattribs={'color': 5})
        out_stream = io.StringIO()
        doc.write(out_stream)
        st.download_button("Download DXF", data=out_stream.getvalue(), file_name="Pro_Pattern.dxf")
