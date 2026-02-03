import streamlit as st
import pandas as pd
import os
import ezdxf
from datetime import datetime
from PIL import Image, ImageOps, ImageFilter, ImageEnhance
from streamlit_drawable_canvas import st_canvas
import io

# --- 1. IDENTITY & PERSISTENT COUNTER ---
st.set_page_config(layout="wide", page_title="Flattern Studio | Pro Precision")
MAIN_LOGO = "logo.png.png"
SIDEBAR_LOGO = "sidebar_logo.png.png"

if 'designs_used' not in st.session_state:
    st.session_state.designs_used = 0
if 'audit_log' not in st.session_state:
    st.session_state.audit_log = []

# --- 2. SIDEBAR: TIERED LOGIC ---
with st.sidebar:
    if os.path.exists(SIDEBAR_LOGO):
        st.image(SIDEBAR_LOGO, use_container_width=True)
    
    st.header("Industrial Settings")
    admin_key = st.text_input("Admin Access Key", type="password")
    
    st.markdown("---")
    st.subheader("Subscription Tiers")
    tier = st.radio("Active Tier", [
        "Pro Garment Manufacturer ($5,000/mo - 50 Designs)",
        "Garment Manufacturer ($2,500/mo - 30 Designs)", 
        "Fashion Designer ($1,500/mo - 20 Designs)"
    ])
    
    is_pro = "Pro" in tier
    limit = 50 if is_pro else (30 if "Garment" in tier else 20)
    
    st.metric("Designs Remaining", f"{limit - st.session_state.designs_used} / {limit}")

    st.markdown("---")
    unit = st.selectbox("Unit System", ["Inches", "Centimeters"])
    user_sa = st.number_input(f"Seam Allowance ({unit})", value=0.5 if unit == "Inches" else 1.2, step=0.1)

# --- 3. MAIN INTERFACE ---
if os.path.exists(MAIN_LOGO):
    st.image(MAIN_LOGO, width=150)

st.title("Flattern Studio | Precision Vector Drafting")

# --- 4. CONDITIONAL DRAFTING (PRO VS. STANDARD) ---
st.header("1. Technical Drafting")
if is_pro:
    st.info("PRO MODE ACTIVE: Adobe Illustrator Precision Tools Enabled (Lines, Rectangles, Joined Paths)")
    drawing_mode = st.selectbox("Vector Tool", ["line", "rect", "circle", "transform"])
else:
    st.warning("Standard Mode: Freehand Sketching Only. Upgrade to Pro for Architectural Precision.")
    drawing_mode = "freedraw"

bg_up = st.file_uploader("Upload Template Image", type=['jpg', 'png', 'jpeg'])
bg_img = Image.open(bg_up) if bg_up else None

# The Architectural Canvas
canvas_result = st_canvas(
    fill_color="rgba(0, 0, 0, 0)",
    stroke_width=2,
    stroke_color="#000000",
    background_image=bg_img,
    height=500,
    width=700,
    drawing_mode=drawing_mode,
    key="precision_canvas",
)

# --- 5. INTERPRETATION & BATCH EXTRACTION ---
st.markdown("---")
st.header("2. Component Extraction")
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

# --- 6. EXPORT LOGIC ---
if st.button("Finalize Production Run"):
    if st.session_state.designs_used < limit:
        st.session_state.designs_used += 1
        st.success(f"Validated. Piece Data Generated for: {', '.join(pieces)}")
    else:
        st.error("Monthly Design Limit Reached.")

if admin_key == "iLFT1991*":
    if is_pro:
        # PRO EXPORT: Single Master DXF with High-Fidelity Vector Paths
        doc = ezdxf.new('R2010')
        msp = doc.modelspace()
        # Drawing perfectly straight Pro lines
        msp.add_lwpolyline([(0,0), (40,0), (40,80), (0,80), (0,0)], dxfattribs={'color': 5})
        msp.add_line((20, 10), (20, 70), dxfattribs={'layer': 'GRAIN_LINE', 'color': 1})
        
        out_stream = io.StringIO()
        doc.write(out_stream)
        st.download_button("Download Pro Master Vector (DXF)", data=out_stream.getvalue(), file_name="Pro_Precision_Master.dxf")
    else:
        # STANDARD EXPORT: Download as Seperate Pieces (Batch)
        st.write("Download Isolated Pieces:")
        for p_name in pieces:
            # Create a simple unique DXF for each piece
            p_doc = ezdxf.new('R2010')
            p_msp = p_doc.modelspace()
            p_msp.add_text(f"PIECE: {p_name}", dxfattribs={'height': 5})
            p_stream = io.StringIO()
            p_doc.write(p_stream)
            st.download_button(f"Download {p_name} DXF", data=p_stream.getvalue(), file_name=f"{p_name}_Piece.dxf")
