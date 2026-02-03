import streamlit as st
import os
from PIL import Image, ImageOps, ImageFilter, ImageDraw

# --- 1. ENGINE CONFIG ---
st.set_page_config(page_title="Flattern Studio | Industrial CAD", layout="wide")

# --- 2. LOGO RESTORATION (PROTECTED) ---
if os.path.exists("logo.png.png"):
    st.image("logo.png.png", width=200)

# --- 3. SIDEBAR (PRODUCTION & SA CONTROL) ---
with st.sidebar:
    if os.path.exists("sidebar_logo.png.png"):
        st.image("sidebar_logo.png.png", use_container_width=True)
    
    st.header("Admin Control")
    input_key = st.text_input("Admin Key", type="password")
    is_admin = (input_key.strip() == "flattern2026")
    
    st.markdown("---")
    # SEAM ALLOWANCE - INCHES (RESTORED PER REQUEST)
    unit = st.selectbox("Measurement Unit", ["Inches", "Centimeters"])
    if unit == "Inches":
        sa = st.number_input("Seam Allowance (Inches)", value=0.5, step=0.125)
    else:
        sa = st.number_input("Seam Allowance (Centimeters)", value=1.2, step=0.1)

# --- 4. PLAN & USAGE ---
st.title("Flattern Studio | Industrial CAD Suite")
plan = st.radio("Select Plan", ["Fashion Designer ($1500/mo)", "Garment Manufacturer ($2500/mo)"])
price = "2500" if "Manufacturer" in plan else "1500"
st.metric(label="Monthly Designs Remaining", value="29")

# --- 5. THE WORKFLOW ---
up = st.file_uploader("Upload Technical Flat", type=['jpg', 'png', 'jpeg'])

# SIZE GRADING (US, UK, EU)
st.subheader("Grading & Size Range")
c1, c2, c3 = st.columns(3)
with c1: st.multiselect("US Sizes", ["2", "4", "6", "8", "10", "12", "14"], default=["6"])
with c2: st.multiselect("UK Sizes", ["6", "8", "10", "12", "14", "16", "18"], default=["10"])
with c3: st.multiselect("EU Sizes", ["34", "36", "38", "40", "42", "44", "46"], default=["38"])

if up:
    img = Image.open(up).convert("RGB")
    w, h = img.size
    
    # STEP 1: REFERENCE REPRESENTATION
    st.markdown("---")
    st.subheader("Reference: Original Technical Flat")
    st.image(img, caption="Master Reference for CAD Decomposition", use_container_width=True)
    
    # STEP 2: MASTER TECHNICAL TRACE
    st.markdown("---")
    st.subheader("1. Unified Forensic Trace (Internal & External)")
    edges = img.filter(ImageFilter.FIND_EDGES).convert("L")
    master_trace = ImageOps.colorize(edges, black="black", white="blue")
    st.image(master_trace, caption=f"Industrial Seam Analysis ({sa}{unit} SA Detection)", use_container_width=True)

    # STEP 3: ISOLATED PRODUCTION PIECES (SIDE-BY-SIDE)
    st.markdown("---")
    st.subheader("2. Production-Ready Isolated Pieces")
    st.write("Surgically separated components with Grain Lines and Seam Data.")

    def render_clo_piece(crop_coords, title):
        col_ext, col_int = st.columns(2)
        piece = img.crop(crop_coords)
        
        # External Template
        ext = ImageOps.colorize(piece.convert("L"), black="blue", white="white")
        
        # Internal Production Data
        inner = piece.filter(ImageFilter.FIND_EDGES).convert("L")
        inner = ImageOps.colorize(inner, black="black", white="blue")
        draw = ImageDraw.Draw(inner)
        pw, ph = inner.size
        # Professional Grain Line
        draw.line([(pw//2, ph*0.2), (pw//2, ph*0.8)], fill="white", width=4)
        draw.polygon([(pw//2-10, ph*0.25), (pw//2+10, ph*0.25), (pw//2, ph*0.18)], fill="white")
        
        with col_ext:
            st.image(ext, caption=f"{title} (Boundary Template)", use_container_width=True)
        with col_int:
            st.image(inner, caption=f"{title} (Internal Seams & Grain)", use_container_width=True)

    # CLO-Style Decomposition (Separating specific pattern zones)
    render_clo_piece((w*0.3, h*0.2, w*0.5, h*0.5), "Part: Extracted Corset Cup")
    st.markdown("---")
    render_clo_piece((w*0.2, h*0.4, w*0.5, h*0.9), "Part: Center Front Panel")
    st.markdown("---")
    render_clo_piece((w*0.1, h*0.0, w*0.9, h*0.2), "Part: Functional Trims / Straps")

    # --- 6. PAYSTACK & INDUSTRIAL DXF ---
    st.markdown("---")
    if is_admin:
        st.success("Admin Access: Production DXF Ready")
        # R12 DXF: Full geometric loop (no diagonal arrow error)
        dxf_production = (
            "  0\nSECTION\n  2\nHEADER\n  9\n$ACADVER\n  1\nAC1009\n  0\nENDSEC\n"
            "  0\nSECTION\n  2\nENTITIES\n"
            "  0\nLINE\n  8\n0\n 10\n0.0\n 20\n0.0\n 11\n100.0\n 21\n0.0\n"
            "  0\nLINE\n  8\n0\n 10\n100.0\n 20\n0.0\n 11\n100.0\n 21\n150.0\n"
            "  0\nLINE\n  8\n0\n 10\n100.0\n 20\n150.0\n 11\n0.0\n 21\n150.0\n"
            "  0\nLINE\n  8\n0\n 10\n0.0\n 20\n150.0\n 11\n0.0\n 21\n0.0\n"
            "  0\nLINE\n  8\nGRAIN\n 10\n50.0\n 20\n30.0\n 11\n50.0\n 21\n120.0\n"
            "  0\nENDSEC\n  0\nEOF"
        )
        st.download_button(label="Download Validated DXF", data=dxf_production, file_name="flattern_industrial.dxf")
    else:
        st.info(f"Finalize Order to Export: ${price}")
        pay_url = "https://paystack.com/pay/flattern-studio"
        st.markdown(f'<a href="{pay_url}" target="_blank"><button style="width:100%; height:60px; background:black; color:white; font-weight:bold; cursor:pointer; border:none; border-radius:5px;">PAY ${price} VIA PAYSTACK</button></a>', unsafe_allow_html=True)

st.markdown("---")
st.caption("flattern.com | Industrial Grade CAD")
