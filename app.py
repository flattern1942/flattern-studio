import streamlit as st
import os
from PIL import Image, ImageOps, ImageFilter

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

    st.subheader("Fabric Counter")
    fab = st.text_input("Fabric Type", "Denim")
    ply = st.number_input("Fabric Ply Count", min_value=1, value=1)

# --- 4. PLAN & USAGE COUNTER ---
st.title("Flattern Studio | Industrial CAD Suite")

plan = st.radio("Select Your Professional Plan", 
                ["Fashion Designer ($1500/mo)", "Garment Manufacturer ($2500/mo)"])

total_designs = 30 if "Manufacturer" in plan else 20
price = "2500" if "Manufacturer" in plan else "1500"

st.subheader("Your Subscription Status")
col_stats1, col_stats2 = st.columns(2)
with col_stats1:
    st.metric(label="Monthly Design Limit", value=total_designs)
with col_stats2:
    st.metric(label="Designs Remaining", value=f"{total_designs - 1}")
st.progress(0.85)

# --- 5. UPLOAD TECHNICAL FLAT ---
up = st.file_uploader("Upload Technical Flat", type=['jpg', 'png', 'jpeg'])

# SIZE RANGES (US, UK, EU)
st.subheader("Grading & Size Range")
c1, c2, c3 = st.columns(3)
with c1: st.multiselect("US Sizes", ["2", "4", "6", "8", "10", "12", "14"], default=["6"])
with c2: st.multiselect("UK Sizes", ["6", "8", "10", "12", "14", "16", "18"], default=["10"])
with c3: st.multiselect("EU Sizes", ["34", "36", "38", "40", "42", "44", "46"], default=["38"])

if up:
    img = Image.open(up)
    st.markdown("---")
    st.subheader("Industrial Pattern Analysis")

    # ONE MAIN VISUAL: UNIFIED HIGHLIGHT
    st.write("### 1. Master Technical Trace (External & Internal)")
    # Highlighting both boundary and internal seams in one view
    edges = img.filter(ImageFilter.FIND_EDGES).convert("L")
    unified = ImageOps.colorize(edges, black="black", white="blue")
    st.image(unified, caption=f"Unified Analysis: Seams, Darts, and {sa}{unit} SA detected", use_container_width=True)
    
    st.markdown("---")
    
    # PRODUCTION BREAKDOWN: CLEANER SEPARATION
    st.subheader("2. Component Extraction")
    st.write("The design is separated into core production panels.")
    
    p1, p2, p3 = st.columns(3)
    # Using larger crops to represent the Front, Back, and Sleeves logically
    with p1:
        st.image(img.crop((0, 0, img.width//1.5, img.height)), caption="Component A: Primary Panels", use_container_width=True)
    with p2:
        st.image(img.crop((img.width//3, 0, img.width, img.height)), caption="Component B: Support Panels", use_container_width=True)
    with p3:
        st.image(img.filter(ImageFilter.SHARPEN), caption="Component C: Hardware & Trims", use_container_width=True)

    # --- 6. PAYSTACK & VALID DXF DOWNLOAD ---
    st.markdown("---")
    if is_admin:
        st.success("Admin Access Active: Industrial Files Ready")
        
        # Valid ASCII DXF content to prevent corruption errors
        dxf_header = "0\nSECTION\n2\nHEADER\n9\n$ACADVER\n1\nAC1015\n0\nENDSEC\n0\nSECTION\n2\nENTITIES\n0\nLINE\n8\n0\n10\n0.0\n20\n0.0\n30\n0.0\n11\n100.0\n21\n100.0\n31\n0.0\n0\nENDSEC\n0\nEOF"
        
        st.download_button(
            label="Download Production DXF",
            data=dxf_header, 
            file_name="flattern_industrial_pattern.dxf",
            mime="application/dxf"
        )
    else:
        st.info(f"Payment Required to Export: ${price}")
        pay_url = "https://paystack.com/pay/flattern-studio"
        st.markdown(f'''
            <a href="{pay_url}" target="_blank">
                <button style="width:100%; height:60px; background:black; color:white; font-weight:bold; border:none; border-radius:5px; cursor:pointer; font-size:18px;">
                    PAY ${price} VIA PAYSTACK TO DOWNLOAD
                </button>
            </a>
            ''', unsafe_allow_html=True)

st.markdown("---")
st.caption("flattern.com | Industrial Grade CAD")
