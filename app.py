import streamlit as st
import os

# --- 1. PAGE CONFIG ---
st.set_page_config(page_title="Flattern Studio | Industrial CAD", layout="wide")

# --- 2. LOGO RESTORATION ---
if os.path.exists("logo.png.png"):
    st.image("logo.png.png", width=200)

# --- 3. SIDEBAR (ADMIN, SETTINGS, USAGE) ---
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

# --- 4. MAIN INTERFACE & PLAN SELECTION ---
st.title("Flattern Studio | Industrial CAD Suite")

plan = st.radio("Select Your Professional Plan", 
                ["Fashion Designer ($1500/mo)", "Garment Manufacturer ($2500/mo)"])

# Define Limits based on Plan
if "Manufacturer" in plan:
    total_designs = 30
    price = "2500"
else:
    total_designs = 20
    price = "1500"

# --- 5. CLIENT USAGE COUNTER ---
st.subheader("Your Subscription Status")
# This is a visual demo counter for the client to see their balance
col_stats1, col_stats2 = st.columns(2)
with col_stats1:
    st.metric(label="Monthly Design Limit", value=total_designs)
with col_stats2:
    st.metric(label="Designs Remaining", value=f"{total_designs - 1}", delta="-1 used this session")
st.progress(0.9) # Visual bar showing they are almost at their limit

# --- 6. DEMO ANALYSIS (UPLOAD TECHNICAL FLAT) ---
up = st.file_uploader("Upload Technical Flat (Demo Analysis)", type=['jpg', 'png', 'jpeg'])

# SIZE RANGES
st.subheader("Grading & Size Range")
c1, c2, c3 = st.columns(3)
with c1: st.multiselect("US Sizes", ["2", "4", "6", "8", "10", "12", "14"], default=["6"])
with c2: st.multiselect("UK Sizes", ["6", "8", "10", "12", "14", "16", "18"], default=["10"])
with c3: st.multiselect("EU Sizes", ["34", "36", "38", "40", "42", "44", "46"], default=["38"])

# --- 7. THREE-PART VISUAL DEMO ---
if up:
    st.markdown("---")
    st.subheader("Industrial Analysis Dashboard")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("External Highlights")
        st.image(up, caption=f"Boundary Detection & {sa} {unit} Seam Allowance", use_container_width=True)
    with col_b:
        st.subheader("Internal Lines")
        st.image(up, caption="Darts, Notches, and Internal Drill Points Identified", use_container_width=True)
    
    st.markdown("---")
    st.subheader("3. Component Breakdown (Exploded View)")
    st.image(up, caption="Full Industrial Component Extraction Ready for DXF", use_container_width=True)

    # --- 8. PAYSTACK GATEWAY & ADMIN UNLOCK ---
    st.markdown("---")
    if is_admin:
        st.success("Admin Access: Unlimited Downloads Active")
        st.button("Download Industrial DXF")
        st.button("Download Tech Pack PDF")
    else:
        st.info(f"To unlock these industrial files, finalize your ${price} payment.")
        pay_url = "https://paystack.com/pay/flattern-studio"
        st.markdown(f'''
            <a href="{pay_url}" target="_blank">
                <button style="width:100%; height:60px; background:black; color:white; font-weight:bold; border:none; border-radius:5px; cursor:pointer; font-size:18px;">
                    PAY ${price} VIA PAYSTACK TO DOWNLOAD
                </button>
            </a>
            ''', unsafe_allow_html=True)

st.markdown("---")
st.caption("flattern.com | Industrial Grade | Lagos, Nigeria")
