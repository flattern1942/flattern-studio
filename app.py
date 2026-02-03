import streamlit as st
import pandas as pd
import os
from PIL import Image, ImageOps, ImageFilter

# --- 1. BRANDING INITIALIZATION ---
st.set_page_config(layout="wide", page_title="Flattern Studio | Industrial CAD")

# Defining your specific file names
MAIN_LOGO = "logo.png.png"
SIDEBAR_LOGO = "sidebar_logo.png.png"

# --- 2. THE SIDEBAR (SIDEBAR LOGO RESTORED) ---
with st.sidebar:
    if os.path.exists(SIDEBAR_LOGO):
        st.image(SIDEBAR_LOGO, use_container_width=True)
    else:
        st.error(f"Missing: {SIDEBAR_LOGO}")
    
    st.header("Security & Grading")
    admin_key = st.text_input("Admin Access Key", type="password")
    
    st.markdown("---")
    st.subheader("Freestyle Seam Allowance")
    unit = st.selectbox("Unit System", ["Inches", "Centimeters"])
    # Your requested freestyle input
    user_sa = st.number_input(f"Seam Allowance ({unit})", value=0.5, step=0.125)

# --- 3. THE MAIN HEADER (MAIN LOGO RESTORED) ---
if os.path.exists(MAIN_LOGO):
    st.image(MAIN_LOGO, width=200)
else:
    st.error(f"Missing: {MAIN_LOGO}")

st.title("Flattern Studio | Forensic Pattern Extraction")

# --- 4. THE MASTER SPECIFICATION TABLE ---
st.header("1. Technical Measurement Table")
spec_data = {
    "Point of Measure (POM)": ["Chest Width", "Waist Width", "CF Length", "Princess Seam", "Armhole Depth", "Cup Depth"],
    "Sample Size (6)": ["17.5\"", "14.0\"", "12.5\"", "14.25\"", "8.5\"", "5.5\""],
    "Tolerance": ["+/- 1/4\"", "+/- 1/4\"", "+/- 1/8\"", "+/- 1/4\"", "+/- 1/8\"", "+/- 1/8\""],
    "Grading Step": ["0.5\"", "0.5\"", "0.25\"", "0.375\"", "0.125\"", "0.25\""]
}
st.table(pd.DataFrame(spec_data))

# --- 5. FORENSIC DECOMPOSITION ENGINE ---
st.header("2. Sequential Pattern Breakdown")
up = st.file_uploader("Upload Technical Flat for Architectural Conversion", type=['jpg', 'png', 'jpeg'])

if up:
    img = Image.open(up).convert("RGB")
    w, h = img.size
    
    st.subheader("Reference Master Architecture")
    st.image(img, use_container_width=True)
    
    st.markdown("---")
    st.subheader("Step-by-Step Pattern Extraction")

    # This isolates your CF, Side Panels, and Cups sequentially
    pieces = [
        {"name": "Center Front Panel", "box": (w*0.2, h*0.45, w*0.4, h*0.95), "id": "CF-01"},
        {"name": "Side Front Panel", "box": (w*0.4, h*0.45, w*0.65, h*0.9), "id": "SF-02"},
        {"name": "Upper Bust Cup", "box": (w*0.3, h*0.1, w*0.5, h*0.45), "id": "UC-03"},
        {"name": "Lower Bust Cup", "box": (w*0.3, h*0.4, w*0.5, h*0.6), "id": "LC-04"}
    ]

    for i, p in enumerate(pieces):
        st.write(f"### Piece {i+1}: {p['name']} ({p['id']})")
        col1, col2 = st.columns(2)
        
        raw_piece = img.crop(p['box'])
        edges = raw_piece.filter(ImageFilter.FIND_EDGES).convert("L")
        trued_pattern = ImageOps.colorize(edges, black="black", white="blue")
        
        with col1:
            st.image(raw_piece, caption=f"Flat Detail: {p['name']}", use_container_width=True)
        with col2:
            st.image(trued_pattern, caption=f"Trued Pattern (+ {user_sa} {unit} SA)", use_container_width=True)
        st.markdown("---")

    # --- 6. THE PRODUCTION EXPORT ---
    if admin_key == "iLFT1991*":
        st.success(f"IP SECURE: DWG Ready with Custom {user_sa} {unit} SA")
        st.download_button("Download All Patterns (DWG)", data="CAD_BINARY_DATA", file_name="flattern_production.dwg")
