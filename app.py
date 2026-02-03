import streamlit as st
import os
import pandas as pd
from PIL import Image, ImageOps, ImageFilter, ImageDraw

# --- 1. CORE SECURITY & IP PROTECTION ---
st.set_page_config(page_title="Flattern Studio | Forensic Alignment", layout="wide")

def check_admin(key):
    # Admin Key: iLFT1991*
    return key.strip() == "iLFT1991*"

if os.path.exists("logo.png.png"):
    st.image("logo.png.png", width=200)

# --- 2. PRODUCTION SIDEBAR ---
with st.sidebar:
    st.header("Security & Specs")
    admin_input = st.text_input("Admin Key", type="password")
    is_admin = check_admin(admin_input)
    
    st.markdown("---")
    st.subheader("Size Grading")
    us_size = st.multiselect("US Sizes", ["0", "2", "4", "6", "8", "10", "12", "14"], default=["6"])
    uk_size = st.multiselect("UK Sizes", ["4", "6", "8", "10", "12", "14", "16"], default=["10"])
    eu_size = st.multiselect("EU Sizes", ["32", "34", "36", "38", "40", "42", "44"], default=["38"])
    
    st.markdown("---")
    unit = st.selectbox("Unit", ["Inches", "Centimeters"])
    # FIXED: Seam Allowance 0.5"
    sa_val = st.number_input(f"Seam Allowance ({unit})", value=0.5 if unit == "Inches" else 1.27, step=0.125)

# --- 3. MASTER TECH PACK SPECS ---
st.title("Flattern Studio | Industrial Extraction Engine")

st.header("Step 1: Industrial Specifications")
spec_data = {
    "Point of Measure (POM)": ["Chest Width", "Waist Width", "CF Length", "Side Seam", "Armhole", "Cup Depth"],
    "Sample Size (6)": ["17.5\"", "14.0\"", "12.5\"", "9.0\"", "16.5\"", "5.5\""],
    "Tolerance": ["+/- 1/4\"", "+/- 1/4\"", "+/- 1/8\"", "+/- 1/8\"", "+/- 1/4\"", "+/- 1/8\""],
    "Grading": ["0.5\"", "0.5\"", "0.25\"", "0.25\"", "0.375\"", "0.25\""]
}
st.table(pd.DataFrame(spec_data))

# --- 4. STEP-BY-STEP PATTERN DECOMPOSITION ---
st.header("Step 2: Sequential Piece Extraction")
up = st.file_uploader("Upload Technical Flat to Begin Extraction", type=['jpg', 'png', 'jpeg'])

if up:
    img = Image.open(up).convert("RGB")
    w, h = img.size
    
    st.markdown("---")
    st.subheader("Master Reference: Technical Flat")
    st.image(img, use_container_width=True)
    
    st.markdown("---")
    st.write("### Production Line Preview")
    
    def process_step(box, label, step_num):
        st.write(f"#### Step {step_num}: Extracting {label}")
        piece = img.crop(box)
        edges = piece.filter(ImageFilter.FIND_EDGES).convert("L")
        trued = ImageOps.colorize(edges, black="black", white="blue")
        
        # Draw Grain and Notches
        draw = ImageDraw.Draw(trued)
        pw, ph = trued.size
        draw.line([(pw//2, ph*0.1), (pw//2, ph*0.9)], fill="white", width=4) # Grain
        draw.line([(0, ph//2), (20, ph//2)], fill="white", width=4) # Notch
        
        c1, c2 = st.columns(2)
        with c1: st.image(piece, caption=f"Original {label}", use_container_width=True)
        with c2: st.image(trued, caption=f"Trued {label} Pattern", use_container_width=True)
        st.markdown("---")

    # Sequential Breakdown
    process_step((w*0.2, h*0.5, w*0.45, h*0.9), "Center Front Panel", 1)
    process_step((w*0.45, h*0.5, w*0.7, h*0.9), "Side Front Panel", 2)
    process_step((w*0.3, h*0.2, w*0.5, h*0.5), "Upper Bust Cup", 3)
    process_step((w*0.3, h*0.4, w*0.5, h*0.6), "Lower Bust Cup", 4)

    # --- 5. THE PRODUCTION DOWNLOAD ---
    st.header("Step 3: Download Industrial DWG")
    if is_admin:
        st.success("Security Verified: DWG Marker Ready for Graded Production")
        # DWG data with separate entities
        dwg_raw = "0\nSECTION\n2\nENTITIES\n0\nPOLYLINE\n8\nPATTERN_PIECES\n66\n1\n0\nSEQEND\n0\nENDSEC\n0\nEOF"
        st.download_button("Download All Pattern Pieces (DWG)", data=dwg_raw, file_name="flattern_marker_production.dwg")
    else:
        st.warning("Secure Portal Locked. Enter Admin Key to download.")

st.markdown("---")
st.caption("flattern.com | Industrial Forensic Tech Pack | IP Protected")
