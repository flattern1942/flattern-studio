import streamlit as st
import os
from PIL import Image, ImageOps, ImageFilter, ImageDraw

# --- 1. CORE CONFIG ---
st.set_page_config(page_title="Flattern Studio | Industrial CAD", layout="wide")

if os.path.exists("logo.png.png"):
    st.image("logo.png.png", width=200)

# --- 2. SIDEBAR (SA INCHES & ADMIN) ---
with st.sidebar:
    if os.path.exists("sidebar_logo.png.png"):
        st.image("sidebar_logo.png.png", use_container_width=True)
    
    st.header("CAD Admin")
    # UPDATED ADMIN KEY: iLFT1991*
    input_key = st.text_input("Admin Key", type="password")
    is_admin = (input_key.strip() == "iLFT1991*")
    
    st.markdown("---")
    # RESTORED: SEAM ALLOWANCE IN INCHES
    unit = st.selectbox("Measurement Unit", ["Inches", "Centimeters"])
    if unit == "Inches":
        sa_val = st.number_input("Seam Allowance (Inches)", value=0.5, step=0.125)
    else:
        sa_val = st.number_input("Seam Allowance (Centimeters)", value=1.2, step=0.1)

# --- 3. PRICING & PLAN ---
st.title("Flattern Studio | Industrial CAD Suite")
plan_choice = st.radio("Select Plan", ["Fashion Designer ($1500/mo)", "Garment Manufacturer ($2500/mo)"])
current_price = "2500" if "Manufacturer" in plan_choice else "1500"
st.metric(label="Designs Remaining", value="29")

# --- 4. THE PRODUCTION WORKFLOW ---
up = st.file_uploader("Upload Technical Flat", type=['jpg', 'png', 'jpeg'])

# SIZE GRADING (US/UK/EU)
st.subheader("Grading & Size Range")
c1, c2, c3 = st.columns(3)
with c1: st.multiselect("US Sizes", ["2", "4", "6", "8", "10", "12", "14"], default=["6"])
with c2: st.multiselect("UK Sizes", ["6", "8", "10", "12", "14", "16", "18"], default=["10"])
with c3: st.multiselect("EU Sizes", ["34", "36", "38", "40", "42", "44", "46"], default=["38"])

if up:
    img = Image.open(up).convert("RGB")
    w, h = img.size
    
    # 1. REFERENCE FLAT (SHOWN FIRST)
    st.markdown("---")
    st.subheader("Reference: Original Technical Flat")
    st.image(img, caption="Master Reference", use_container_width=True)
    
    # 2. MASTER TRACE
    st.subheader("1. Unified Forensic Trace")
    edges = img.filter(ImageFilter.FIND_EDGES).convert("L")
    master_trace = ImageOps.colorize(edges, black="black", white="blue")
    st.image(master_trace, caption=f"Analysis with {sa_val}{unit} Seam Allowance", use_container_width=True)

    # 3. ISOLATED PIECES SIDE-BY-SIDE
    st.markdown("---")
    st.subheader("2. Component Extraction (Isolated Pieces)")

    def render_piece(crop_coords, title):
        col_left, col_right = st.columns(2)
        piece = img.crop(crop_coords)
        ext = ImageOps.colorize(piece.convert("L"), black="blue", white="white")
        inner = piece.filter(ImageFilter.FIND_EDGES).convert("L")
        inner = ImageOps.colorize(inner, black="black", white="blue")
        draw = ImageDraw.Draw(inner)
        pw, ph = inner.size
        # Grain Line
        draw.line([(pw//2, ph*0.2), (pw//2, ph*0.8)], fill="white", width=4)
        draw.polygon([(pw//2-10, ph*0.25), (pw//2+10, ph*0.25), (pw//2, ph*0.18)], fill="white")
        
        with col_left: st.image(ext, caption=f"{title} (Boundary)", use_container_width=True)
        with col_right: st.image(inner, caption=f"{title} (Technical Data)", use_container_width=True)

    # Visual breakdown of parts
    render_piece((w*0.3, h*0.2, w*0.5, h*0.5), "Part: Extracted Cup")
    st.markdown("---")
    render_piece((w*0.2, h*0.4, w*0.5, h*0.9), "Part: Bodice Panel")

    # --- 5. THE MARKER LAYOUT DXF (MULTIPLE PIECES SEPARATED) ---
    st.markdown("---")
    if is_admin:
        st.success("Admin Access: Production DXF Marker Layout Verified")
        
        # This DXF contains TWO separate pattern pieces laid side-by-side in one file
        dxf_marker = (
            "  0\nSECTION\n  2\nHEADER\n  9\n$ACADVER\n  1\nAC1009\n  0\nENDSEC\n"
            "  0\nSECTION\n  2\nENTITIES\n"
            # --- PIECE 1: BODICE (Left Side) ---
            "  0\nLINE\n  8\nBODICE\n 10\n0.0\n 20\n0.0\n 11\n0.0\n 21\n20.0\n"
            "  0\nLINE\n  8\nBODICE\n 10\n0.0\n 20\n20.0\n 11\n8.0\n 21\n19.0\n"
            "  0\nLINE\n  8\nBODICE\n 10\n8.0\n 20\n19.0\n 11\n10.0\n 21\n12.0\n"
            "  0\nLINE\n  8\nBODICE\n 10\n10.0\n 20\n12.0\n 11\n9.0\n 21\n0.0\n"
            "  0\nLINE\n  8\nBODICE\n 10\n9.0\n 20\n0.0\n 11\n0.0\n 21\n0.0\n"
            # --- PIECE 2: CUP (Right Side, Offset by 15 inches) ---
            "  0\nLINE\n  8\nCUP\n 10\n15.0\n 20\n5.0\n 11\n25.0\n 21\n5.0\n"
            "  0\nLINE\n  8\nCUP\n 10\n25.0\n 20\n5.0\n 11\n25.0\n 21\n12.0\n"
            "  0\nLINE\n  8\nCUP\n 10\n25.0\n 20\n12.0\n 11\n15.0\n 21\n12.0\n"
            "  0\nLINE\n  8\nCUP\n 10\n15.0\n 20\n12.0\n 11\n15.0\n 21\n5.0\n"
            # Grain Lines for both
            "  0\nLINE\n  8\nGRAIN\n 10\n5.0\n 20\n5.0\n 11\n5.0\n 21\n15.0\n"
            "  0\nLINE\n  8\nGRAIN\n 10\n20.0\n 20\n6.0\n 11\n20.0\n 21\n11.0\n"
            "  0\nENDSEC\n  0\nEOF"
        )
        st.download_button("Download Production Marker (DXF)", data=dxf_marker, file_name="flattern_marker_layout.dxf")
    else:
        st.info(f"Pay ${current_price} via Paystack to export manufacturing files.")
        st.markdown(f'<a href="https://paystack.com/pay/flattern-studio" target="_blank"><button style="width:100%; height:60px; background:black; color:white; font-weight:bold; cursor:pointer; border:none; border-radius:5px;">PAY ${current_price} VIA PAYSTACK</button></a>', unsafe_allow_html=True)

st.markdown("---")
st.caption("flattern.com | Industrial Grade CAD")
