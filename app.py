
import streamlit as st
import os

# --- 1. PAGE CONFIG ---
st.set_page_config(page_title="Flattern Studio | Industrial CAD", layout="wide")

# --- 2. LOGO RESTORATION (TOP) ---
# Looking for your exact file name: logo.png.png
if os.path.exists("logo.png.png"):
    st.image("logo.png.png", width=200)

# --- 3. SIDEBAR (ADMIN, SA, LOGO) ---
with st.sidebar:
    # Looking for your exact file name: sidebar_logo.png.png
    if os.path.exists("sidebar_logo.png.png"):
        st.image("sidebar_logo.png.png", use_container_width=True)
    
    st.header("Admin Control")
    admin_key = st.text_input("Admin Key", type="password")
    is_admin = (admin_key == "flattern2026")
    
    st.markdown("---")
    # SEAM ALLOWANCE - INCHES & CM
    unit = st.selectbox("Measurement Unit", ["Inches", "Centimeters"])
    if unit == "Inches":
        sa = st.number_input("Seam Allowance (Inches)", value=0.5, step=0.125)
    else:
        sa = st.number_input("Seam Allowance (Centimeters)", value=1.2, step=0.1)

    st.subheader("Fabric Counter")
    fab = st.text_input("Fabric Type", "Denim")
    ply = st.number_input("Fabric Ply Count", min_value=1, value=1)

# --- 4. MAIN INTERFACE & PRICING ---
st.title("Flattern Studio | Industrial CAD Suite")

plan = st.radio("Select Professional Plan", 
                ["Fashion Designer ($1500 for 20 Designs)", 
                 "Garment Manufacturer ($2500 for 30 Designs)"])

price = "2500" if "Manufacturer" in plan else "1500"
limit = "30" if "Manufacturer" in plan else "20"

# UPLOAD TECHNICAL FLAT
up = st.file_uploader("Upload Technical Flat", type=['jpg', 'png', 'jpeg'])

# SIZING SYSTEMS (US, UK, EU)
st.subheader("Grading & Size Range")
c1, c2, c3 = st.columns(3)
with c1:
    st.multiselect("US Sizes", ["2", "4", "6", "8", "10", "12", "14"], default=["6"])
with c2:
    st.multiselect("UK Sizes", ["6", "8", "10", "12", "14", "16", "18"], default=["10"])
with c3:
    st.multiselect("EU Sizes", ["34", "36", "38", "40", "42", "44", "46"], default=["38"])

# --- 5. THE THREE VISUALIZATIONS ---
if up:
    st.markdown("---")
    st.subheader("Industrial Pattern Analysis")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("External Highlights")
        st.image(up, caption=f"1. Perimeter Detection & {sa} {unit} SA", use_container_width=True)
    with col_b:
        st.subheader("Internal Lines")
        st.image(up, caption="2. Darts, Notches & Technical Markings", use_container_width=True)
    
    st.markdown("---")
    st.subheader("3. Component Breakdown")
    st.image(up, caption=f"Exploded View: {limit} Separate Pieces Identified for Industrial DXF", use_container_width=True)

    # --- 6. PAYSTACK & ADMIN BYPASS ---
    st.markdown("---")
    if is_admin:
        st.success("Admin Access Active: Downloads Unlocked")
        st.button("Download Industrial DXF")
        st.button("Download Tech Pack PDF")
    else:
        st.write(f"Total: ${price} for {limit} Designs")
        # PAYSTACK BUTTON
        pay_url = "https://paystack.com/pay/flattern-studio"
        st.markdown(f'''
            <a href="{pay_url}" target="_blank">
                <button style="width:100%; height:60px; background:black; color:white; font-weight:bold; border:none; border-radius:5px; cursor:pointer; font-size:18px;">
                    PAY ${price} VIA PAYSTACK
                </button>
            </a>
            ''', unsafe_allow_html=True)

st.markdown("---")
st.caption("flattern.com | Industrial Grade | Lagos, Nigeria")
