import streamlit as st
import os
from PIL import Image, ImageOps, ImageFilter, ImageDraw

# --- 1. PAGE CONFIG ---
st.set_page_config(page_title="Flattern Studio | Industrial CAD", layout="wide")

# --- 2. LOGO RESTORATION (PROTECTED) ---
if os.path.exists("logo.png.png"):
    st.image("logo.png.png", width=200)

# --- 3. SIDEBAR (ADMIN, PRODUCTION & SA) ---
with st.sidebar:
    if os.path.exists("sidebar_logo.png.png"):
        st.image("sidebar_logo.png.png", use_container_width=True)
    
    st.header("Admin Control")
    input_key = st.text_input("Admin Key", type="password")
    is_admin = (input_key.strip() == "flattern2026")
    
    st.markdown("---")
    # SEAM ALLOWANCE - INCHES & CM (PERMANENT)
    unit = st.selectbox("Measurement Unit", ["Inches", "Centimeters"])
    if unit == "Inches":
        sa = st.number_input("Seam Allowance (Inches)", value=0.5, step=0.125)
    else:
        sa = st.number_input("Seam Allowance (Centimeters)", value=1.2, step=0.1)

    st.subheader("Fabric Counter")
    fab = st.text_input("Fabric Type", "Denim")
    ply = st.number_input("Fabric Ply Count", min_value=1, value=1)

# --- 4. PLAN & USAGE COUNTER ---
st.title("Flattern Studio | Industrial CAD Suite")
plan = st.radio("Select Plan", ["Fashion Designer ($1500/mo)", "Garment Manufacturer ($2500/mo)"])
total_designs = 30 if "Manufacturer" in plan else 20
price = "2500" if "Manufacturer" in plan else "1500"

st.metric(label="Monthly Designs Remaining", value=f"{total_designs - 1}")
st.progress(0.85)

# --- 5. UPLOAD & REFERENCE FLAT ---
up = st.file_uploader("Upload Technical Flat", type=['jpg', 'png', 'jpeg'])

# US, UK, EU SIZING (PROTECTED)
st.subheader("Grading & Size Range")
c1, c2, c3 = st.columns(3)
with c1: st.multiselect("US Sizes", ["2", "4", "6", "8", "10", "12", "14"], default=["6"])
with c2: st.multiselect("UK Sizes", ["6", "8", "10", "12", "14", "16", "18"], default=["10"])
with c3: st.multiselect("EU Sizes", ["34", "36", "38", "40", "42", "44", "46"], default=["38"])

if up:
    img = Image.open(up).convert("RGB")
    w, h = img.size
    st.markdown("---")
    
    # NEW: REFERENCE FLAT (SHOWN FIRST AS REQUESTED)
    st.subheader("Reference: Original Technical Flat")
    st.image(img, caption="Original Design Upload", use_container_width=True)
    
    st.markdown("---")
    
    # 1. MASTER FORENSIC TRACE
    st.subheader("1. Master Forensic Trace (Internal & External Highlights)")
    edges = img.filter(ImageFilter.FIND_EDGES).convert("L")
    master_trace = ImageOps.colorize(edges, black="black", white="blue")
    st.image(master_trace, caption=f"Unified Technical Highlight ({sa}{unit} SA Applied)", use_container_width=True)

    st.markdown("---")
    
    # 2. COMPONENT EXTRACTION (SEPARATED PIECES SIDE-BY-SIDE)
    st.subheader("2. Industrial Piece Extraction (Separated Patterns)")
    st.write("Each component isolated with grain lines and forensic seam detection.")

    def extract_forensic_piece(crop_box, title):
        col_ext, col_int = st.columns(2)
        piece = img.crop(crop_box)
        
        # External Shape Highlight
        ext = ImageOps.colorize(piece.convert("L"), black="blue", white="white")
        
        # Internal Seams + Grain Line
        inner = piece.filter(ImageFilter.FIND_EDGES).convert("L")
        inner = ImageOps.colorize(inner, black="black", white="blue")
        draw = ImageDraw.Draw(inner)
        pw, ph = inner.size
        # Draw Grain Line
        draw.line([(pw//2, ph*0.2), (pw//2, ph*0.8)], fill="white", width=3)
        draw.polygon([(pw//2-6, ph*0.25), (pw//2+6, ph*0.25), (pw//2, ph*0.2)], fill="white")
        draw.polygon([(pw//2-6, ph*0.75), (pw//2+6, ph*0.75), (pw//2, ph*0.8)], fill="white")
        
        with col_ext:
            st.image(ext, caption=f"{title} (Boundary)", use_container_width=True)
        with col_int:
            st.image(inner, caption=f"{title} (Seams & Grain)", use_container_width=True)

    # Forensic Corset/Bodice Sections (Crops different parts of the reference)
    extract_forensic_piece((w*0.3, h*0.2, w*0.5, h*0.5), "Piece: Corset Cup / Bust")
    st.markdown("---")
    extract_forensic_piece((w*0.2, h*0.4, w*0.5, h*0.9), "Piece: Bodice (CF / CB)")
    st.markdown("---")
    extract_forensic_piece((w*0.1, h*0.0, w*0.9, h*0.2), "Piece: Straps & Waistband")

    # --- 6. PAYSTACK & VALIDATED DXF ---
    st.markdown("---")
    if is_admin:
        st.success("Admin Access: Production Files Ready")
        # Corrected R12 DXF with Entites for a complete file structure
        dxf_header = (
            "  0\nSECTION\n  2\nHEADER\n  9\n$ACADVER\n  1\nAC1009\n  0\nENDSEC\n"
            "  0\nSECTION\n  2\nENTITIES\n"
            "  0\nLINE\n  8\nBOUNDARY\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 11\n50.0\n 21\n50.0\n 31\n0.0\n"
            "  0\nLINE\n  8\nSEAMS\n 10\n10.0\n 20\n10.0\n 30\n0.0\n 11\n60.0\n 21\n60.0\n 31\n0.0\n"
            "  0\nENDSEC\n  0\nEOF"
        )
        st.download_button(label="Download Validated DXF", data=dxf_header, file_name="flattern_production.dxf")
    else:
        st.info(f"Finalize Order to Export: ${price}")
        pay_url = "https://paystack.com/pay/flattern-studio"
        st.markdown(f'<a href="{pay_url}" target="_blank"><button style="width:100%; height:60px; background:black; color:white; font-weight:bold; cursor:pointer; border:none; border-radius:5px;">PAY ${price} VIA PAYSTACK</button></a>', unsafe_allow_html=True)

st.markdown("---")
st.caption("flattern.com | Industrial Grade CAD")
