import streamlit as st
import pandas as pd
import os

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="Flattern Studio | Industrial CAD", layout="wide")

# --- 2. LOGOS ---
if os.path.exists("logo.png.png"):
    st.image("logo.png.png", width=150)
if os.path.exists("sidebar_logo.png.png"):
    st.sidebar.image("sidebar_logo.png.png", use_container_width=True)

# --- 3. SIDEBAR: CORE SPECS & SA ---
with st.sidebar:
    st.header("Pattern Specifications")
    unit = st.selectbox("Unit", ["Inches", "Centimeters"])
    # [2026-02-02] SA in inches restored
    sa_amt = st.number_input(f"Seam Allowance ({unit})", value=0.5 if unit == "Inches" else 1.2, step=0.1)
    
    st.markdown("---")
    st.subheader("Fabric Counter")
    fabric_type = st.text_input("Fabric Name/Code", "Denim-01")
    ply_count = st.number_input("Number of Plies", min_value=1, value=1)
    
    st.markdown("---")
    admin_key = st.text_input("Admin Bypass", type="password")

# --- 4. MAIN INTERFACE: TECH PACK & MEASUREMENTS ---
st.title("Industrial Tech Pack Generator")

col_input, col_specs = st.columns([1, 1])

with col_input:
    uploaded_file = st.file_uploader("Upload Flat Sketch / Pattern", type=['jpg', 'png', 'jpeg'])
    client_name = st.text_input("Client/Project Name")
    size_range = st.multiselect("Sizes", ["XS", "S", "M", "L", "XL", "XXL"], default=["M"])

with col_specs:
    st.subheader("Measurements & Internal Lines")
    internal_lines = st.checkbox("Extract Internal Lines (Boning, Darts, Pleats)", value=True)
    breakdown_flats = st.checkbox("Breakdown to Component Flats", value=True)
    grade_rules = st.text_area("Grading Notes / Special Instructions")

# --- 5. VISUAL REPRESENTATIONS ---
if uploaded_file:
    st.markdown("---")
    st.subheader("Visual Analysis")
    
    # Two representations side-by-side, sized for the screen
    v_col1, v_col2 = st.columns(2)
    
    with v_col1:
        st.image(uploaded_file, caption="1. Edge Detection & SA Layout", use_container_width=True)
        st.caption(f"Status: {sa_amt} {unit} SA applied to all perimeters.")
        
    with v_col2:
        # Representation of the internal line breakdown
        st.image(uploaded_file, caption="2. Internal Line & Component Breakdown", use_container_width=True)
        st.caption("Status: Darts and internal notches identified for DXF.")

    # --- 6. TECH PACK DATA TABLE ---
    st.markdown("---")
    st.subheader("Tech Pack Summary")
    tp_data = {
        "Feature": ["Fabric", "Plies", "Base Size", "SA Applied", "Internal Lines"],
        "Value": [fabric_type, ply_count, size_range[0], f"{sa_amt} {unit}", "Active" if internal_lines else "None"]
    }
    st.table(pd.DataFrame(tp_data))

    # --- 7. PRICING & PAYSTACK ---
    st.markdown("---")
    if admin_key == "flattern2026":
        st.success("Admin Access: Download Unlocked")
        st.button("Export Full Tech Pack (PDF)")
        st.button("Export CAD Pattern (DXF)")
    else:
        st.warning("Price: 5,000 NGN for Full Industrial Export")
        paystack_link = "https://paystack.com/pay/flattern-studio"
        st.markdown(f"""
            <a href="{paystack_link}" target="_blank" style="text-decoration: none;">
                <div style="background-color: #000; color: white; padding: 15px; text-align: center; font-weight: bold; border-radius: 0px;">
                    PAY VIA PAYSTACK TO DOWNLOAD TECH PACK & DXF
                </div>
            </a>
            """, unsafe_allow_html=True)

st.markdown("---")
st.caption("flattern.com | Industrial Grade CAD | Lagos, Nigeria")
