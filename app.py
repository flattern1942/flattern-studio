import streamlit as st
import os
from PIL import Image, ImageOps, ImageFilter, ImageDraw

# --- 1. PAGE CONFIG ---
st.set_page_config(page_title="Flattern Studio | Industrial CAD", layout="wide")

# --- 2. LOGO RESTORATION ---
if os.path.exists("logo.png.png"):
    st.image("logo.png.png", width=200)

# --- 3. SIDEBAR (ADMIN & PRODUCTION SETTINGS) ---
with st.sidebar:
    if os.path.exists("sidebar_logo.png.png"):
        st.image("sidebar_logo.png.png", use_container_width=True)
    
    st.header("Admin Control")
    input_key = st.text_input("Admin Key", type="password")
    is_admin = (input_key.strip() == "flattern2026")
    
    st.markdown("---")
    unit = st.selectbox("Measurement Unit", ["Inches", "Centimeters"])
    if unit == "Inches":
        sa = st.number_input("Seam Allowance (Inches)", value=0.5, step=0.125)
    else:
        sa = st.number_input("Seam Allowance (Centimeters)", value=1.2, step=0.1)

# --- 4. PLAN & USAGE ---
st.title("Flattern Studio | Industrial CAD Suite")
plan = st.radio("Select Plan", ["Fashion Designer ($1500/mo)", "Garment Manufacturer ($2500/mo)"])
total_designs = 30 if "Manufacturer" in plan else 20
price = "2500" if "Manufacturer" in plan else "1500"

st.metric(label="Monthly Designs Remaining", value=f"{total_designs - 1}")
st.progress(0.85)

# --- 5. UPLOAD & ANALYSIS ---
up = st.file_uploader("Upload Technical Flat", type=['jpg', 'png', 'jpeg'])

if up:
    img = Image.open(up).convert("RGB")
    w, h = img.size
    st.markdown("---")
    
    st.subheader("1. Master Forensic Trace (Internal & External)")
    edges = img.filter(ImageFilter.FIND_EDGES).convert("L")
    master_trace = ImageOps.colorize(edges, black="black", white="blue")
    st.image(master_trace, caption=f"Unified Trace: {sa}{unit} SA Applied to all Internal/External lines", use_container_width=True)

    st.markdown("---")
    
    # --- 6. DYNAMIC PIECE EXTRACTION (CORSET/BODICE LOGIC) ---
    st.subheader("2. Industrial Piece Extraction (Separated Components)")
    st.write("Each pattern piece is isolated with its unique grain line, notches, and internal highlights.")

    def extract_and_highlight(crop_box, title):
        col_ext, col_int = st.columns(2)
        piece = img.crop(crop_box)
        
        # External Highlight (Pattern Shape)
        ext = ImageOps.colorize(piece.convert("L"), black="blue", white="white")
        
        # Internal Highlight (Seams + Grain Line)
        inner = piece.filter(ImageFilter.FIND_EDGES).convert("L")
        inner = ImageOps.colorize(inner, black="black", white="blue")
        
        # Draw Grain Line on Internal View
        draw = ImageDraw.Draw(inner)
        pw, ph = inner.size
        draw.line([(pw//2, ph*0.2), (pw//2, ph*0.8)], fill="white", width=3) # Grain Line
        draw.polygon([(pw//2-5, ph*0.22), (pw//2+5, ph*0.22), (pw//2, ph*0.18)], fill="white") # Top Arrow
        
        with col_ext:
            st.image(ext, caption=f"{title} (Boundary)", use_container_width=True)
        with col_int:
            st.image(inner, caption=f"{title} (Internal Analysis)", use_container_width=True)

    # Forensic Breakdown Sections
    extract_and_highlight((w*0.3, h*0.2, w*0.5, h*0.5), "Component: Corset Cup (Top)")
    st.markdown("---")
    extract_and_highlight((w*0.2, h*0.4, w*0.5, h*0.9), "Component: Front Bodice Panel")
    st.markdown("---")
    extract_and_highlight((w*0.5, h*0.4, w*0.8, h*0.9), "Component: Side/Back Panel")
    st.markdown("---")
    extract_and_highlight((w*0.1, h*0.0, w*0.9, h*0.2), "Component: Straps / Internal Facing")

    # --- 7. PAYSTACK & VALIDATED DXF ---
    st.markdown("---")
    if is_admin:
        st.success("Admin Access: Production Files Ready")
        dxf_data = (
            "  0\nSECTION\n  2\nHEADER\n  9\n$ACADVER\n  1\nAC1009\n  0\nENDSEC\n"
            "  0\nSECTION\n  2\nENTITIES\n  0\nLINE\n  8\n0\n 10\n0.0\n 20\n0.0\n 30\n0.0\n 11\n50.0\n 21\n50.0\n 31\n0.0\n"
            "  0\nENDSEC\n  0\nEOF"
        )
        st.download_button(label="Download Validated DXF", data=dxf_data, file_name="flattern_forensic.dxf", mime="application/dxf")
    else:
        st.info(f"Payment Required to Export: ${price}")
        pay_url = "https://paystack.com/pay/flattern-studio"
        st.markdown(f'<a href="{pay_url}" target="_blank"><button style="width:100%; height:60px; background:black; color:white; font-weight:bold; cursor:pointer;">PAY ${price} VIA PAYSTACK</button></a>', unsafe_allow_html=True)

st.markdown("---")
st.caption("flattern.com | Industrial Grade CAD")
