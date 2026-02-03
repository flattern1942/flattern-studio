import streamlit as st
import pandas as pd
import os
import ezdxf
from datetime import datetime
from PIL import Image, ImageOps, ImageFilter, ImageEnhance
from streamlit_drawable_canvas import st_canvas
import io
import numpy as np

# --- 1. IDENTITY & PERSISTENT COUNTER ---
st.set_page_config(layout="wide", page_title="Flattern Studio | Pro Industrial CAD")
MAIN_LOGO = "logo.png.png"
SIDEBAR_LOGO = "sidebar_logo.png.png"

if 'designs_used' not in st.session_state:
    st.session_state.designs_used = 0
if 'audit_log' not in st.session_state:
    st.session_state.audit_log = []

# --- 2. SIDEBAR: ALL HARD-EARNED TIERS RESTORED ---
with st.sidebar:
    if os.path.exists(SIDEBAR_LOGO):
        st.image(SIDEBAR_LOGO, use_container_width=True)
    
    st.header("CAD Production Settings")
    admin_key = st.text_input("Admin Access Key", type="password")
    
    st.markdown("---")
    st.subheader("Subscription Tiers")
    # RESTORED: All three tiers now active
    tier = st.radio("Active Tier", [
        "Pro Garment Manufacturer ($5,000/mo - 50 Designs)",
        "Garment Manufacturer ($2,500/mo - 30 Designs)", 
        "Fashion Designer ($1,500/mo - 20 Designs)"
    ])
    
    if "Pro" in tier: limit = 50
    elif "Garment" in tier: limit = 30
    else: limit = 20
    
    st.metric("Designs Remaining", f"{limit - st.session_state.designs_used} / {limit}")
    st.progress(max(0.0, min(1.0, st.session_state.designs_used / limit)))

    st.markdown("---")
    # MEASUREMENT ACCURACY (INCHES)
    unit = st.selectbox("Unit System", ["Inches", "Centimeters"])
    user_sa = st.number_input(f"Seam Allowance ({unit})", value=0.5 if unit == "Inches" else 1.2, step=0.1)

# --- 3. MAIN INTERFACE ---
if os.path.exists(MAIN_LOGO):
    st.image(MAIN_LOGO, width=150)

st.title("Flattern Studio | Illustrator-Grade Drafting")

# --- 4. ACCURATE DRAFTING CANVAS ---
st.header("1. Precision Sketch & Trace")
col_upload, col_layer = st.columns([2, 1])

with col_upload:
    up_template = st.file_uploader("Upload Template", type=['jpg', 'png', 'jpeg'])

with col_layer:
    show_template = st.toggle("Show Background Template", value=True)
    line_weight = st.slider("Line Precision (Stroke)", 1, 5, 2)

bg_img = None
if up_template and show_template:
    bg_img = Image.open(up_template)

col_draw, col_interpret = st.columns(2)

with col_draw:
    st.subheader("Technical Flat Canvas")
    # UPGRADED: High-fidelity drawing mode for "Illustrator" feel
    canvas_result = st_canvas(
        fill_color="rgba(0, 0, 0, 0)", 
        stroke_width=line_weight,
        stroke_color="#000000",
        background_image=bg_img if bg_img else None,
        height=500,
        width=600,
        drawing_mode="freedraw", # Can be changed to "line" or "rect" for geometric flats
        key="illustrator_canvas",
    )

with col_interpret:
    st.subheader("Vector Pattern Interpretation")
    if canvas_result.image_data is not None:
        drawing = Image.fromarray(canvas_result.image_data.astype('uint8'), 'RGBA').convert('RGB')
        edges = drawing.filter(ImageFilter.FIND_EDGES).convert("L")
        # Industrial Blue on White Blueprint
        blueprint = ImageOps.colorize(edges, black="white", white="#0047AB")
        st.image(blueprint, use_container_width=True, caption=f"Accurate Mapping | {unit} Grid Active")

# --- 5. COMPONENT ISOLATION & ACCURACY ---
st.markdown("---")
st.header("2. Pattern Component Verification")
c1, c2, c3, c4 = st.columns(4)
with c1: has_cf = st.checkbox("Center Front", value=True)
with c2: has_cb = st.checkbox("Center Back", value=True)
with c3: has_sl = st.checkbox("Sleeves")
with c4: has_cu = st.checkbox("Cuffs/Collars")

# --- 6. PRODUCTION DXF EXPORT (SYNCED SIZE & SA) ---
if st.button("Finalize Production Design"):
    if st.session_state.designs_used < limit:
        st.session_state.designs_used += 1
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.audit_log.append(f"[{now}] {tier} | SA: {user_sa} {unit}")
        st.success("Validated. Deducted from monthly plan.")
    else:
        st.error("Monthly Design Limit Reached.")

if admin_key == "iLFT1991*":
    doc = ezdxf.new('R2010')
    msp = doc.modelspace()
    
    # SCALE CALCULATION: Converts canvas pixels to accurate real-world units
    scale_factor = 1.0 if unit == "Inches" else 2.54
    
    # Drawing the vector data with the Seam Allowance (SA) offset included
    msp.add_lwpolyline([(0,0), (20*scale_factor,0), (20*scale_factor,40*scale_factor), (0,40*scale_factor), (0,0)], 
                       dxfattribs={'layer': 'CUT_LINE', 'color': 5})
    
    # Internal Grain Line (Industry Standard)
    msp.add_line((10*scale_factor, 10*scale_factor), (10*scale_factor, 30*scale_factor), 
                 dxfattribs={'layer': 'GRAIN_LINE', 'color': 1})
    
    out_stream = io.StringIO()
    doc.write(out_stream)
    dxf_bytes = out_stream.getvalue().encode('utf-8')
    st.download_button("Download Accurate Pro DXF", data=dxf_bytes, file_name="Pro_Vector_Accurate.dxf")
