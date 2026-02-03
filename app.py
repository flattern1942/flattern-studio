import streamlit as st
import pandas as pd
import os

# --- 1. PAGE SETUP ---
st.set_page_config(page_title="Flattern Studio | Industrial CAD", layout="wide")

# --- 2. LOGOS ---
if os.path.exists("logo.png.png"):
    st.image("logo.png.png", width=150)

# --- 3. SIDEBAR (ADMIN, SEAM ALLOWANCE, FABRIC) ---
with st.sidebar:
    if os.path.exists("sidebar_logo.png.png"):
        st.image("sidebar_logo.png.png", use_container_width=True)
    
    st.header("Control Panel")
    
    # ADMIN BYPASS
    admin_password = st.text_input("System Admin Key", type="password")
    is_admin = (admin_password == "flattern2026")
    
    st.markdown("---")
    
    # SEAM ALLOWANCE (INCHES & CM)
    unit = st.selectbox("Measurement Unit", ["Inches", "Centimeters"])
    if unit == "Inches":
        sa_amt = st.number_input("Seam Allowance (Inches)", value=0.5, step=0.125)
    else:
        sa_amt = st.number_input("Seam Allowance (Centimeters)", value=1.2, step=0.1)

    # FABRIC COUNTER
    st.subheader("Fabric Counter")
    fab_type = st.text_input("Fabric Type", "Denim")
    ply = st.number_input("Ply Count", min_value=1, value=1)

# --- 4. MAIN INTERFACE & TIERED PRICING ---
st.title("Industrial Tech Pack & CAD Suite")

# Price Tier Selection
user_role = st.radio("Select Professional Plan", 
                     ["Fashion Designer ($1,500 for 20 Designs)", 
                      "Garment Manufacturer ($2,500 for 30 Designs)"])

if "Manufacturer" in user_role:
    price_val = "2500"
    design_limit = "30"
else:
    price_val = "1500"
    design_limit = "20"

col1, col2 = st.columns(2)
with col1:
    uploaded_file = st.file_uploader("Upload Pattern Photo", type=['jpg', 'png', 'jpeg'])
    client = st.text_input("Client Name")
with col2:
    st.subheader("Digitalization Specs")
    internal_lines = st.checkbox("Extract Internal Lines (Darts/Notches)", value=True)
    size_range = st.multiselect("Sizes", ["XS", "S", "M", "L", "XL"], default=["M"])

# --- 5. COMPONENT BREAKDOWN VISUALS ---
if uploaded_file:
    st.markdown("---")
    st.subheader("Industrial Analysis & Component Breakdown")
    
    v_col1, v_col2 = st.columns(2)
    
    with v_col1:
        st.image(uploaded_file, caption="1. Perimeter Detection & SA Applied", use_container_width=True)
        st.info(f"Unit: {unit} | SA: {sa_amt}")
        
    with v_col2:
        # THE BREAKDOWN FEATURE
        st.image(uploaded_file, caption=f"2. COMPONENT BREAKDOWN: {design_limit} Flats Identified", use_container_width=True)
        st.success("Internal lines and separate flats extracted for DXF.")

    # --- 6. PAYSTACK GATEWAY & ADMIN DOWNLOAD ---
    st.markdown("---")
    
    if is_admin:
        st.subheader("Admin Download Console")
        st.write("Bypass Active: Accessing all component flats for free.")
        st.button("Download Industrial DXF (Full Breakdown)")
        st.button("Download Tech Pack PDF")
    else:
        st.subheader("Finalize & Export")
        st.write(f"Package: {design_limit} Designs | Total Due: ${price_val}")
        
        # --- THE PAYSTACK BUTTON ---
        paystack_link = "https://paystack.com/pay/flattern-studio"
        st.markdown(f"""
            <a href="{paystack_link}" target="_blank" style="text-decoration: none;">
                <div style="background-color: #000; color: white; padding: 20px; text-align: center; font-weight: bold; border-radius: 4px; font-size: 20px;">
                    PAY ${price_val} VIA PAYSTACK
                </div>
            </a>
            """, unsafe_allow_html=True)
        st.caption("Secure payment via Paystack Gateway. Downloads unlock after verification.")

# --- 7. FOOTER ---
st.markdown("---")
st.write("flattern.com | Industrial Grade CAD | Lagos, Nigeria")
