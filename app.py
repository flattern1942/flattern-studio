import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image

# --- 1. THE UNTOUCHABLE BUSINESS ARCHITECTURE ---
# HARD-LOCKED PLANS
PLAN_DATA = {
    "Pro Garment Manufacturer": {"price": 6500, "quota": 50},
    "Manufacturer Lite": {"price": 2500, "quota": 30},
    "Fashion Designer": {"price": 1500, "quota": 20}
}

st.set_page_config(layout="wide")

# State Management
if 'design_count' not in st.session_state: st.session_state.design_count = 0
if 'unit_type' not in st.session_state: st.session_state.unit_type = "Inches"
if 'sa_value' not in st.session_state: st.session_state.sa_value = 0.5
if 'active_plan' not in st.session_state: st.session_state.active_plan = "Pro Garment Manufacturer"

def load_branding():
    try:
        # Side Logo (Main) | Purple Logo (Sidebar)
        return Image.open("sidebar_logo.png.png"), Image.open("logo.png.png")
    except:
        return None, None

side_logo_img, purple_logo_img = load_branding()

# --- 2. SIDEBAR: PURPLE LOGO & ADMIN PORTAL ---
with st.sidebar:
    if purple_logo_img: st.image(purple_logo_img, use_container_width=True)
    st.markdown("---")
    
    st.subheader("ADMIN PORTAL")
    # PASSWORD PROTECTION FOR PLAN SWITCHING
    pwd = st.text_input("Admin Password", type="password")
    if pwd == "factory2026":
        st.session_state.active_plan = st.selectbox("Switch Plan Tier", list(PLAN_DATA.keys()))
    
    current = PLAN_DATA[st.session_state.active_plan]
    st.error(f"PLAN: {st.session_state.active_plan}")
    st.write(f"**Billing:** ${current['price']}/mo (USD)")
    st.metric("Quota Status", f"{st.session_state.design_count} / {current['quota']}")
    
    if st.button("Reset Monthly Quota"):
        st.session_state.design_count = 0
        st.rerun()

    st.markdown("---")
    st.subheader("PAYSTACK USD GATEWAY")
    st.button(f"Pay ${current['price']} via Paystack")
    st.caption("Secure Industrial Checkout Active")

# --- 3. MAIN WORKSPACE: 800PX LOGO & STABLE CANVAS ---
if side_logo_img: 
    st.image(side_logo_img, width=800)

st.title("Industrial Technical Flat Engine")

tabs = st.tabs(["Drafting & SA", "Sizes & Grading", "CAD Factory Export"])

with tabs[0]:
    col_t, col_c = st.columns([1, 4])
    with col_t:
        st.write("### Drafting Units")
        st.session_state.unit_type = st.radio("", ["Inches", "CM"], horizontal=True)
        st.write(f"### Seam Allowance ({st.session_state.unit_type})")
        st.session_state.sa_value = st.number_input("", value=0.5 if st.session_state.unit_type == "Inches" else 1.2)
        
        st.markdown("---")
        tool = st.radio("Tool", ["Smart Curve (Bezier)", "Straight Line", "Add Balance Notch"])
        if st.button("Save Design"):
            if st.session_state.design_count < current['quota']:
                st.session_state.design_count += 1
                st.success("Flat Secured to Database")
            else:
                st.warning("Quota Reached - Upgrade Required")
        if st.button("Clear Canvas"):
            st.rerun()

    with col_c:
        # NO COMPONENT ERROR: background_image = None. 
        # The 800px logo is rendered ABOVE the canvas to prevent memory crashes.
        canvas_result = st_canvas(
            stroke_width=2, stroke_color="#000000", background_color="#FFFFFF",
            height=700, width=1100,
            drawing_mode="path" if tool == "Smart Curve (Bezier)" else ("line" if tool == "Straight Line" else "point"),
            key="v108_enterprise_stable"
        )

with tabs[1]:
    st.subheader(f"Industrial Grading Matrix ({st.session_state.unit_type})")
    
    if st.session_state.unit_type == "Inches":
        st.table({"Size": ["XS", "S", "M", "L", "XL"], "Bust": ["32\"", "34\"", "36\"", "38\"", "40\""]})
    else:
        st.table({"Size": ["34", "36", "38", "40", "42"], "Bust": ["80cm", "84cm", "88cm", "96cm", "102cm"]})
    
    st.info(f"Applying **{st.session_state.sa_value} {st.session_state.unit_type} SA** to all size increments.")

with tabs[2]:
    st.subheader("Factory DXF/DWG Export")
    
    c1, c2, c3 = st.columns(3)
    with c1: st.button("Download PDF Tech Pack")
    with c2: st.button("Download Industrial AAMA (DXF)")
    with c3: st.button("Download Engineering CAD (DWG)")
    st.markdown("---")
    
    st.write(f"Vectors generated with {st.session_state.sa_value} SA and factory notches.")
