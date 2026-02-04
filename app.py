import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import requests

# --- 1. PRO SYSTEM & WEBHOOK CONFIG ---
st.set_page_config(layout="wide")
PAYSTACK_SECRET_KEY = "sk_live_xxxx" # Replace with your live key later

if 'sa_value' not in st.session_state: st.session_state.sa_value = 0.5
if 'designs_remaining' not in st.session_state: st.session_state.designs_remaining = 0

def load_pro_branding():
    try:
        return Image.open("sidebar_logo.png.png"), Image.open("logo.png.png")
    except:
        return None, None

side_logo, purple_logo = load_pro_branding()

# --- SIDEBAR: ACCESS & PAYMENTS ---
with st.sidebar:
    if side_logo: st.image(side_logo, use_container_width=True)
    st.markdown("---")
    
    access = st.radio("Portal Access", ["Client Billing", "Admin Dashboard"])
    
    if access == "Client Billing":
        st.write("### Production Quota")
        st.metric("Designs Available", st.session_state.designs_remaining)
        
        mode = st.toggle("Live Mode (USD)", value=False)
        amount = 6500 if mode else 1000000 # Example: $6500 vs test NGN
        
        if st.button(f"Pay ${amount}" if mode else "Pay Test Amount"):
            st.info("Webhook waiting for Paystack confirmation...")
            # Simulate Webhook Success
            st.session_state.designs_remaining += 50
            st.success("Payment Verified. 50 Designs Added.")
    else:
        st.text_input("Admin Username")
        st.text_input("Password", type="password")
        st.button("Manage Client Webhooks")

    st.markdown("---")
    st.write("### Seam Allowance (Inches)")
    c1, c2, c3 = st.columns([1, 2, 1])
    with c1: 
        if st.button("−"): st.session_state.sa_value -= 0.125
    with c3: 
        if st.button("+"): st.session_state.sa_value += 0.125
    with c2: 
        st.session_state.sa_value = st.number_input("", value=st.session_state.sa_value, format="%.3f")

# --- 2. THE MASTER WORKSPACE ---
st.title("Industrial Vector Workspace")
if purple_logo: st.image(purple_logo, width=150)

tabs = st.tabs(["Flat Drafting", "Pattern Breakdown", "Export"])

with tabs[0]:
    col_t, col_d = st.columns([1, 5])
    with col_t:
        tool = st.radio("Drawing Tool", ["Smart Curve (Bezier)", "Straight Line", "Transform"])
        st.write("Snap-to-Node: **Active**")
    
    with col_d:
        canvas_result = st_canvas(
            fill_color="rgba(0,0,0,0)", stroke_width=2, stroke_color="#000000",
            height=700, width=1000,
            drawing_mode="path" if tool == "Smart Curve (Bezier)" else ("line" if tool == "Straight Line" else "transform"),
            point_display_radius=5,
            key="v60_production_lock"
        )

with tabs[1]:
    st.subheader("Automated Pattern Separation")
    
    st.write(f"Transforming vectors into Front, Back, and Sleeve pieces with {st.session_state.sa_value}\" SA.")

with tabs[2]:
    st.subheader("Factory-Ready Export")
    
    if st.button("Finalize & Download DXF"):
        if st.session_state.designs_remaining > 0:
            st.session_state.designs_remaining -= 1
            st.success("Production file generated.")
        else:
            st.error("Insufficient designs. Please visit Client Billing.")
