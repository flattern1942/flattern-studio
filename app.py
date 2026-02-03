import streamlit as st
import pandas as pd
import numpy as np

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Flattern Studio | Industrial CAD",
    layout="wide"
)

# --- 2. BRANDING & VISUALS ---
st.markdown("""
    <style>
    .main { background-color: #ffffff; }
    .stButton>button { 
        width: 100%; 
        border-radius: 0px; 
        height: 3em; 
        background-color: #000000; 
        color: #ffffff;
        font-weight: bold;
        border: 1px solid #000000;
    }
    .stButton>button:hover {
        background-color: #333333;
        color: #ffffff;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("Flattern Industrial Digitalization")
st.write("Professional Pattern to DXF/PDF Conversion")
st.markdown("---")

# --- 3. SIDEBAR CONTROLS ---
with st.sidebar:
    st.header("Project Settings")
    
    # Unit Selection
    unit = st.selectbox("Measurement Unit", ["Inches", "Centimeters"])
    
    # SA in Inches (Specific User Request)
    if unit == "Inches":
        sa_amt = st.number_input("Seam Allowance (Inches)", min_value=0.0, max_value=2.0, value=0.5, step=0.125)
    else:
        sa_amt = st.number_input("Seam Allowance (CM)", min_value=0.0, max_value=5.0, value=1.2, step=0.1)

    st.markdown("---")
    st.subheader("System Access")
    admin_mode = st.checkbox("Admin Access")
    admin_key = ""
    if admin_mode:
        admin_key = st.text_input("Enter Admin Password", type="password")

# --- 4. MAIN INTERFACE ---
uploaded_file = st.file_uploader("Upload Image (JPG/PNG)", type=['jpg', 'jpeg', 'png'])

if uploaded_file:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.image(uploaded_file, caption="Input Pattern", use_container_width=True)
        
    with col2:
        st.subheader("Processing Details")
        st.write(f"Standardized Unit: {unit}")
        st.write(f"Calculated SA: {sa_amt} {unit}")
        
        status_box = st.empty()
        status_box.info("Status: Processing edges...")
        
        # Simulation of industrial processing
        progress = st.progress(0)
        for i in range(100):
            progress.progress(i + 1)
        
        status_box.success("Status: Conversion Ready")

    st.markdown("---")
    
    # --- 5. PAYMENT & DOWNLOAD GATE ---
    # Change 'flattern2026' to your preferred admin password
    if admin_mode and admin_key == "flattern2026":
        st.subheader("Download Files (Admin Mode)")
        st.download_button("Download DXF File", data="dummy data", file_name="pattern.dxf")
        st.download_button("Download PDF File", data="dummy data", file_name="pattern.pdf")
    else:
        st.subheader("Secure Checkout")
        st.write("A payment of 5,000 NGN is required to download the industrial files.")
        
        # Paystack Payment Link
        paystack_link = "https://paystack.com/pay/flattern-studio" 
        
        st.markdown(f"""
            <a href="{paystack_link}" target="_blank" style="text-decoration: none;">
                <div style="
                    background-color: #000000;
                    color: white;
                    padding: 15px;
                    text-align: center;
                    font-weight: bold;
                    border-radius: 4px;
                    ">
                    PAY VIA PAYSTACK
                </div>
            </a>
            """, unsafe_allow_html=True)
        st.caption("Upon payment, please contact support or use your admin key to finalize download.")

# --- 6. FOOTER ---
st.markdown("---")
st.write("flattern.com | Industrial CAD Solutions | Lagos, Nigeria")
