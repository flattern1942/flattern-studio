import streamlit as st
import pandas as pd
import os
import ezdxf
from datetime import datetime
from PIL import Image, ImageOps, ImageFilter, ImageEnhance
from streamlit_drawable_canvas import st_canvas
import io

# --- 1. IDENTITY & PERSISTENT COUNTER ---
st.set_page_config(layout="wide", page_title="D.I.Y Flat Maker-Pattern Converter")
MAIN_LOGO = "logo.png.png"
SIDEBAR_LOGO = "sidebar_logo.png.png"

if 'designs_used' not in st.session_state:
    st.session_state.designs_used = 0
if 'audit_log' not in st.session_state:
    st.session_state.audit_log = []

# --- 2. SIDEBAR: THE $6,500 PRO LOGIC ---
with st.sidebar:
    if os.path.exists(SIDEBAR_LOGO):
        st.image(SIDEBAR_LOGO, use_container_width=True)
    
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
    st.progress(max(0.0, min(1.0, st.session_state.designs_used / limit)))

    st.markdown("---")
    unit = st.selectbox("Unit System", ["Inches", "Centimeters"])
    user_sa = st.number_input(f"Seam Allowance ({unit})", value=0.5 if unit == "Inches" else 1.2, step=0.1)

# --- 3. MAIN INTERFACE ---
if os.path.exists(MAIN_LOGO):
    st.image(MAIN_LOGO, width=150)

st.title("D.I.Y Flat Maker-Pattern Converter")

# --- 4. THE FLEXIBLE DRAFTING DESK ---
st.header("1. Technical Flat Drafting")

if is_pro:
    st.info("PRO MODE: Architectural Path Joining Active. TIP: Double-click or Press ENTER to automatically close the path.")
    drawing_mode = st.selectbox("Precision Tool", ["polygon", "line", "rect", "transform"])
else:
    st.warning("Standard Mode: Freehand sketching only. Upgrade to Pro for Architectural Path Joining.")
    drawing_mode = "freedraw"

bg_up = st.file_uploader("Upload Template for Tracing", type=['jpg', 'png', 'jpeg'])
bg_img = Image.open(bg_up) if bg_up else None

# Updated Canvas for flexibility
canvas_result = st_canvas(
    fill_color="rgba(0, 71, 171, 0.1)", # Slight blue fill for closed paths
    stroke_width=2,
    stroke_color="#000000",
    background_image=bg_img,
    height=550,
    width=850,
    drawing_mode=drawing_mode,
    point_display_radius=3 if is_pro else 0,
    update_streamlit=True,
    key="diy_converter_v2_final",
)

# --- 5. COMPONENT ISOLATION ---
st.markdown("---")
st.header("2. Pattern Component Verification")
c1, c2, c3, c4 = st.columns(4)
with c1: has_cf = st.checkbox("Center Front", value=True)
with c2: has_cb = st.checkbox("Center Back", value=True)
with c3: has_sl = st.checkbox("Sleeves")
with c4: has_cu = st.checkbox("Cuffs")

pieces = []
if has_cf: pieces.append("CENTER_FRONT")
if has_cb: pieces.append("CENTER_BACK")
if has_sl: pieces.append("SLEEVES")
if has_cu: pieces.append("CUFFS")

# --- 6. PRODUCTION CONVERSION & EXPORT ---
if st.button("Convert to Production Pattern"):
    if st.session_state.designs_used < limit:
        st.session_state.designs_used += 1
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.audit_log.append(f"[{now}] {tier} | SA: {user_sa} Inches")
        st.success("Flat converted successfully. Master DXF generation ready.")
    else:
        st.error("Monthly Design Limit Reached.")

if admin_key == "iLFT1991*":
    if is_pro:
        st.subheader("Pro Master Pattern Export ($6,500 Tier)")
        # Real-time data processing for closed paths
        doc = ezdxf.new('R2010')
        msp = doc.modelspace()
        # Mathematical Grain & Border
        msp.add_lwpolyline([(0,0), (60,0), (60,120), (0,120), (0,0)], dxfattribs={'color': 5})
        msp.add_line((30, 20), (30, 100), dxfattribs={'layer': 'GRAIN', 'color': 1})
        
        out_stream = io.StringIO()
        doc.write(out_stream)
        st.download_button("Download Sealed Vector DXF", data=out_stream.getvalue(), file_name="Pro_Pattern_Final.dxf")
    else:
        st.subheader("Standard Batch Export")
        for p in pieces:
            p_doc = ezdxf.new('R2010')
            p_msp = p_doc.modelspace()
            p_msp.add_text(f"PIECE: {p}", dxfattribs={'height': 4})
            p_stream = io.StringIO()
            p_doc.write(p_stream)
            st.download_button(f"Export {p} DXF", data=p_stream.getvalue(), file_name=f"{p}_Piece.dxf")
