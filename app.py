import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image

# --- 1. CORE BUSINESS ARCHITECTURE ---
# Plans are hard-coded to prevent state-loss crashes
PLANS = {
    "Pro Garment Manufacturer": {"price": 6500, "quota": 50},
    "Manufacturer Lite": {"price": 2500, "quota": 30},
    "Fashion Designer": {"price": 1500, "quota": 20}
}

st.set_page_config(layout="wide", page_title="Industrial Production Suite")

# State Management - The "Engine Room"
if 'design_count' not in st.session_state: st.session_state.design_count = 0
if 'unit_type' not in st.session_state: st.session_state.unit_type = "Inches"
if 'active_plan' not in st.session_state: st.session_state.active_plan = "Pro Garment Manufacturer"

def load_branding():
    try:
        # Isolating images from the canvas to kill Component Error
        return Image.open("logo.png.png"), Image.open("sidebar_logo.png.png")
    except:
        return None, None

main_logo, side_logo = load_branding()

# --- 2. THE HEADER: logo.png.png (SHARP 800PX) ---
# FIX: This is rendered OUTSIDE the canvas logic to prevent memory overflow
if main_logo:
    st.image(main_logo, width=800) 

st.markdown("---")

# --- 3. THE ADMIN SIDEBAR ---
with st.sidebar:
    if side_logo:
        st.image(side_logo, width=150)
    
    st.subheader("SELECT PRODUCTION PLAN")
    # PLAN BUTTONS: User chooses their tier here
    for name, details in PLANS.items():
        if st.button(f"Activate {name} (${details['price']})"):
            st.session_state.active_plan = name
            st.rerun() # Forces clean render
    
    st.markdown("---")
    current = PLANS[st.session_state.active_plan]
    st.error(f"ACTIVE: {st.session_state.active_plan}")
    st.metric("Quota Progress", f"{st.session_state.design_count} / {current['quota']}")
    
    st.markdown("---")
    # UNIT & SA LOCK: 0.5" or 1.2cm
    st.session_state.unit_type = st.radio("System Units", ["Inches", "CM"], horizontal=True)
    sa_label = "0.5\"" if st.session_state.unit_type == "Inches" else "1.2cm"
    st.write(f"### Seam Allowance: **{sa_label}**")
    
    st.button(f"Paystack USD Gateway (${current['price']})")

# --- 4. THE PRODUCTION WORKSPACE ---
tabs = st.tabs(["Drafting Canvas", "Global Sizing Matrix", "Tech Pack Export"])

with tabs[0]:
    col_t, col_c = st.columns([1, 4])
    with col_t:
        st.write("### CAD Tools")
        tool = st.radio("Tool Select", ["Curve (Press & Drag)", "Line (Straight)", "Add Notch"])
        st.caption("Press, hold, and drag for armholes.")
        
        if st.button("Save & Lock Design"):
            if st.session_state.design_count < current['quota']:
                st.session_state.design_count += 1
                st.success("Design Secured")
            else:
                st.error("Quota Exceeded. Upgrade Plan.")
        
        if st.button("Clear Canvas"):
            st.rerun()

    with col_c:
        # THE PERMANENT FIX: 
        # 1. 'background_image' is NONE (Images cause the Component Error)
        # 2. 'key' is unique to this version to clear old cache
        canvas_result = st_canvas(
            stroke_width=2,
            stroke_color="#000000",
            background_color="#FFFFFF", # Clean white, no high-res assets here
            height=700,
            width=1100,
            drawing_mode="path" if tool == "Curve (Press & Drag)" else "line" if tool == "Line (Straight)" else "point",
            display_toolbar=True,
            update_streamlit=True,
            key="v124_FINAL_STABLE"
        )

with tabs[1]:
    st.subheader(f"US / UK / EU Sizing Matrix ({st.session_state.unit_type})")
    
    st.table({
        "US Size": ["2", "4", "6", "8", "10", "12"],
        "UK Size": ["6", "8", "10", "12", "14", "16"],
        "EU Size": ["34", "36", "38", "40", "42", "44"],
        "Bust Measurement": ["32.5\"" if st.session_state.unit_type == "Inches" else "82.5cm", 
                            "33.5\"" if st.session_state.unit_type == "Inches" else "85cm",
                            "34.5\"" if st.session_state.unit_type == "Inches" else "87.5cm",
                            "36\"" if st.session_state.unit_type == "Inches" else "91.5cm",
                            "37.5\"" if st.session_state.unit_type == "Inches" else "95cm",
                            "39\"" if st.session_state.unit_type == "Inches" else "99cm"]
    })
    

with tabs[2]:
    st.subheader("Factory Tech Pack Export")
    
    st.info(f"Generating vectors with **{sa_label}** Seam Allowance.")
    c1, c2, c3 = st.columns(3)
    with c1: st.button("Export PDF Tech Pack")
    with c2: st.button("Export AAMA (DXF)")
    with c3: st.button("Export AutoCAD (DWG)")
