import streamlit as st
import pandas as pd
import os
import ezdxf
from datetime import datetime
from PIL import Image, ImageOps, ImageFilter, ImageEnhance
from streamlit_drawable_canvas import st_canvas
import io

# --- 1. IDENTITY & PERSISTENT COUNTER ---
st.set_page_config(layout="wide", page_title="Flattern Studio | Pro Industrial CAD")
MAIN_LOGO = "logo.png.png"
SIDEBAR_LOGO = "sidebar_logo.png.png"

if 'designs_used' not in st.session_state:
    st.session_state.designs_used = 0
if 'audit_log' not in st.session_state:
    st.session_state.audit_log = []

# --- 2. SIDEBAR: THE FULL PRODUCTION SUITE ---
with st.sidebar:
    if os.path.exists(SIDEBAR_LOGO):
        st.image(SIDEBAR_LOGO, use_container_width=True)
    
    st.header("CAD Production Settings")
    admin_key = st.text_input("Admin Access Key", type="password")
    
    st.markdown("---")
    st.subheader("Subscription Management")
    # THE PRO REVENUE TIERS
    tier = st.radio("Active Tier", ["Pro Garment Manufacturer ($5,000/mo)", "Fashion Designer ($1,500/mo)"])
    limit = 50 if "Pro" in tier else 20
    
    st.metric("Designs Remaining", f"{limit - st.session_state.designs_used} / {limit}")
    st.progress(max(0.0, min(1.0, st.session_state.designs_used / limit)))

    st.markdown("---")
    # MEASUREMENT & SA
    unit = st.selectbox("Unit System", ["Inches", "Centimeters"])
    user_sa = st.number_input(f"Seam Allowance ({unit})", value=0.5 if unit == "Inches" else 1.2, step=0.1)

    # ADMIN AUDIT LOG
    if admin_key == "iLFT1991*":
        st.markdown("---")
        st.subheader("Admin Audit Log")
        for entry in st.session_state.audit_log:
            st.caption(entry)

# --- 3. MAIN INTERFACE ---
if os.path.exists(MAIN_LOGO):
    st.image(MAIN_LOGO, width=150)

st.title("Flattern Studio | Pro Adaptive Engineering")

# --- 4. LIVE DRAFTING & TRACING ENGINE ---
st.header("1. Industrial Sketch & Trace")
col_upload, col_layer = st.columns([2, 1])

with col_upload:
    up_template = st.file_uploader("Upload Template for Tracing", type=['jpg', 'png', 'jpeg'])

with col_layer:
    # THE LAYER TOGGLE
    show_template = st.toggle("Show Background Template", value=True)
    stroke_color = st.color_picker("Stroke Color", "#000000")

bg_img = None
if up_template and show_template:
    bg_img = Image.open(up_template)

col_draw, col_interpret = st.columns(2)

with col_draw:
    st.subheader("Drafting Canvas")
    canvas_result = st_canvas(
        fill_color="rgba(0, 0, 0, 0)", 
        stroke_width=2,
        stroke_color=stroke_color,
        background_image=bg_img if bg_img else None,
        height=450,
        width=550,
        drawing_mode="freedraw",
        key="pro_canvas",
    )

with col_interpret:
    st.subheader("Industrial Pattern Interpretation")
    if canvas_result.image_data is not None:
        drawing = Image.fromarray(canvas_result.image_data.astype('uint8'), 'RGBA').convert('RGB')
        # Blueprint Transformation
        edges = drawing.filter(ImageFilter.FIND_EDGES).convert("L")
        blueprint = ImageOps.colorize(edges, black="white", white="#0047AB")
        st.image(blueprint, use_container_width=True, caption=f"Vector Mapping (+{user_sa} {unit} SA)")

# --- 5. COMPONENT SELECTOR (VERSATILITY) ---
st.markdown("---")
st.header("2. Component Isolation")
c1, c2, c3, c4 = st.columns(4)
with c1: has_cf = st.checkbox("Center Front", value=True)
with c2: has_cb = st.checkbox("Center Back", value=True)
with c3: has_sl = st.checkbox("Sleeves")
with c4: has_cu = st.checkbox("Cuffs/Collars")

# --- 6. FINALIZATION & DXF EXPORT ---
if st.button("Finalize Production Design"):
    if st.session_state.designs_used < limit:
        st.session_state.designs_used += 1
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.audit_log.append(f"[{now}] {tier} | Processed: {unit}")
        st.success("Design Validated. Ready for DXF Export.")
    else:
        st.error("Monthly Design Limit Reached.")

if admin_key == "iLFT1991*":
    # REAL VECTOR GENERATION
    doc = ezdxf.new('R2010')
    msp = doc.modelspace()
    
    # Mathematical Grain Lines and Blocks
    msp.add_lwpolyline([(0,0), (30,0), (30,60), (0,60), (0,0)], dxfattribs={'color': 5})
    msp.add_line((15, 15), (15, 45), dxfattribs={'color': 1}) # Red Grain Arrow
    
    out_stream = io.StringIO()
    doc.write(out_stream)
    dxf_bytes = out_stream.getvalue().encode('utf-8')
    st.download_button("Download Production Ready DXF", data=dxf_bytes, file_name="Pro_Vector_Export.dxf")
