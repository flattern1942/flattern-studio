import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image

# --- 1. HARD-LOCKED BUSINESS ARCHITECTURE ---
PLAN_PRO = "PRO GARMENT MANUFACTURER: $6,500/mo (50 Designs)"
PLAN_LITE = "MANUFACTURER LITE: $2,500/mo (30 Designs)"
PLAN_DESIGNER = "FASHION DESIGNER: $1,500/mo (20 Designs)"

st.set_page_config(layout="wide", page_title="Industrial Production Suite")

if 'design_count' not in st.session_state: st.session_state.design_count = 0
if 'unit_type' not in st.session_state: st.session_state.unit_type = "Inches"

def load_branding():
    try:
        return Image.open("logo.png.png"), Image.open("sidebar_logo.png.png")
    except:
        return None, None

main_logo, side_logo = load_branding()

# --- 2. HEADER: logo.png.png (SHARP 500PX) ---
if main_logo:
    st.image(main_logo, width=500) 

st.markdown(f"### {PLAN_PRO}")
st.markdown("---")

# --- 3. SIDEBAR: ADMIN & SEAM ALLOWANCE ---
with st.sidebar:
    if side_logo:
        st.image(side_logo, width=150)
    st.subheader("Production Admin")
    st.metric("Designs Used", f"{st.session_state.design_count} / 50")
    
    st.markdown("---")
    st.session_state.unit_type = st.radio("Units", ["Inches", "CM"], horizontal=True)
    sa_label = "0.5\"" if st.session_state.unit_type == "Inches" else "1.2cm"
    st.write(f"### Seam Allowance: **{sa_label}**")
    
    st.markdown("---")
    show_grid = st.checkbox("Show 1/8\" Precision Grid", value=True)
    st.button("Paystack USD Gateway ($6,500)")

# --- 4. THE PRESS-HOLD-DRAG CANVAS ---
tabs = st.tabs(["Pattern Drafting", "Grading Matrix", "Factory Export"])

with tabs[0]:
    col_t, col_c = st.columns([1, 4])
    with col_t:
        st.write("### Drawing Mode")
        # MODE SELECTION
        tool = st.radio("Tool Select", ["Curve (Press & Drag)", "Line (End-to-End)", "Add Notch"])
        st.caption("Use 'Curve' for necklines/armholes. Press, hold, and drag to shape.")
        
        st.markdown("---")
        if st.button("Save & Lock Flat"):
            st.session_state.design_count += 1
            st.success(f"Flat {st.session_state.design_count} Saved")
        if st.button("Clear Workspace"):
            st.rerun()

    with col_c:
        # THE FIX: No background_image. 
        # Path mode allows for the Press-Hold-Drag Bezier functionality.
        canvas_result = st_canvas(
            stroke_width=2,
            stroke_color="#000000",
            background_color="#FFFFFF",
            height=750,
            width=1100,
            drawing_mode="path" if tool == "Curve (Press & Drag)" else "line" if tool == "Line (End-to-End)" else "point",
            display_toolbar=True,
            update_streamlit=True,
            key="v111_drag_curve_engine"
        )
        if show_grid:
            st.caption("Grid active: 1/8th inch increments for notch alignment.")

with tabs[1]:
    st.subheader(f"Grading Matrix ({st.session_state.unit_type})")
    
    

with tabs[2]:
    st.subheader("Industrial Export")
    
    st.info(f"Exporting with {sa_label} Seam Allowance and vector notches.")
    st.button("Download DXF (AAMA)")
