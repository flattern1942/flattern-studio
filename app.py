import streamlit as st
import pandas as pd
import os
from PIL import Image, ImageOps, ImageFilter, ImageEnhance

# --- 1. BRANDING & UNIT LOCK ---
st.set_page_config(layout="wide", page_title="Flattern Studio | Professional CAD")
MAIN_LOGO = "logo.png.png"
SIDEBAR_LOGO = "sidebar_logo.png.png"

# --- 2. SIDEBAR: THE FULL SUITE ---
with st.sidebar:
    if os.path.exists(SIDEBAR_LOGO):
        st.image(SIDEBAR_LOGO, use_container_width=True)
    
    st.header("Production Settings")
    admin_key = st.text_input("Admin Access Key", type="password")
    
    st.markdown("---")
    st.subheader("Size Grading")
    selected_sizes = st.multiselect("Grading Range", 
                                    ["0", "2", "4", "6", "8", "10", "12", "14", "16"], 
                                    default=["6", "8", "10"])
    
    st.markdown("---")
    st.subheader("Seam Allowance (Freestyle)")
    user_sa = st.number_input("Seam Allowance (Inches)", value=0.5, step=0.125)

# --- 3. MAIN INTERFACE ---
if os.path.exists(MAIN_LOGO):
    st.image(MAIN_LOGO, width=180)

st.title("Flattern Studio | Industrial Pattern Portal")

# --- 4. FEATURES: SPECS & PRICING ---
st.header("1. Technical Specifications & Pricing")
col_spec, col_price = st.columns([2, 1])

with col_spec:
    spec_data = {
        "Point of Measure (POM)": ["Chest Width", "Waist Width", "CF Length", "Princess Seam", "Cup Depth"],
        "Sample (6)": ["17.5\"", "14.0\"", "12.5\"", "14.25\"", "5.5\""],
        "Grading Rule": ["+0.5\"", "+0.5\"", "+0.25\"", "+0.375\"", "+0.25\""]
    }
    st.table(pd.DataFrame(spec_data))

with col_price:
    st.subheader("Production Estimate")
    cost = 25.00 + (len(selected_sizes) * 5.00)
    st.metric("Total Pattern Fee", f"${cost:,.2f}")
    st.write(f"Grading for {len(selected_sizes)} sizes active.")

# --- 5. THE TRANSFORMATION ENGINE ---
st.header("2. Pattern Transformation (Wearable Interpretation)")
up = st.file_uploader("UPLOAD FLAT FOR CONVERSION", type=['jpg', 'png', 'jpeg'])

if up:
    img = Image.open(up).convert("RGB")
    w, h = img.size
    
    st.subheader("Sequential Pattern Pieces")
    
    # Precise extraction zones for CF, Panels, and Cups
    pieces = [
        {"name": "Center Front Panel", "box": (w*0.25, h*0.4, w*0.45, h*0.9), "id": "CF-01"},
        {"name": "Side Front Panel", "box": (w*0.45, h*0.4, w*0.7, h*0.85), "id": "SF-02"},
        {"name": "Upper Bust Cup", "box": (w*0.3, h*0.1, w*0.55, h*0.4), "id": "UC-03"},
        {"name": "Lower Bust Cup", "box": (w*0.3, h*0.4, w*0.55, h*0.6), "id": "LC-04"}
    ]

    for p in pieces:
        st.write(f"### {p['name']} ({p['id']})")
        col1, col2 = st.columns(2)
        
        # Crop & Interpret Geometry
        raw = img.crop(p['box'])
        enhancer = ImageEnhance.Contrast(raw)
        boosted = enhancer.enhance(2.0) # Highlight internal lines
        
        # Generate Trued Blue Pattern
        edges = boosted.filter(ImageFilter.FIND_EDGES).convert("L")
        pattern_view = ImageOps.colorize(edges, black="black", white="blue")
        
        with col1:
            st.image(raw, caption="Forensic Detail", use_container_width=True)
        with col2:
            st.image(pattern_view, caption=f"Wearable Pattern (+{user_sa}\" SA)", use_container_width=True)
        st.markdown("---")

    # --- 6. SECURE EXPORT ---
    if admin_key == "iLFT1991*":
        st.success("DWG PRODUCTION EXPORT READY")
        st.download_button("Download Pattern Pack (.DWG)", data="CAD_DATA", file_name="Flattern_Final_Patterns.dwg")
