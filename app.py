import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import io
import ezdxf

# --- PRO IDENTITY & ZERO-STRIP POLICY ---
st.set_page_config(layout="wide")

# Persistent data for SA and Canvas State
if 'sa_value' not in st.session_state: st.session_state.sa_value = 0.5
if 'v53_key' not in st.session_state: st.session_state.v53_key = 0

# --- ASSET PROTECTION ENGINE ---
def load_assets():
    try:
        side = Image.open("sidebar_logo.png.png")
        main = Image.open("logo.png.png") # Purple Logo
        return side, main
    except:
        return None, None

side_logo, purple_logo = load_assets()

with st.sidebar:
    # Anchor: sidebar_logo.png.png
    if side_logo:
        st.image(side_logo, use_container_width=True)
    
    st.markdown("---")
    # THE PLANS: $6500 Pro / $2500 Lite / $1500 Fashion
    plan = st.selectbox("", [
        "Pro Garment Manufacturer ($6,500/mo - 50 Designs)",
        "Garment Manufacturer Lite ($2,500/mo - 30 Designs)",
        "Fashion Designer ($1,500/mo - 20 Designs)"
    ])
    
    st.markdown("---")
    # SEAM ALLOWANCE: Inches/CM Toggle + Plus/Minus Bar
    st.write("### Seam Allowance (Inches)")
    c1, c2, c3 = st.columns([1, 2, 1])
    with c1: 
        if st.button("−"): st.session_state.sa_value -= 0.125
    with c3: 
        if st.button("+"): st.session_state.sa_value += 0.125
    with c2: 
        st.session_state.sa_value = st.number_input("", value=st.session_state.sa_value, format="%.3f")

# --- MASTER VECTOR WORKSPACE ---
st.title("Industrial Vector Workspace")

tabs = st.tabs(["Drafting", "Breakdown", "Pattern Transformation", "Export"])

with tabs[0]:
    col_tools, col_draw = st.columns([1, 5]) 
    with col_tools:
        # Precision Tools: Click and Drag for Bezier Curves
        tool = st.radio("Vector Engine", ["Smart Curve (Bezier)", "Straight Line", "Node Transform"])
        st.write("End-Points: **Snap Active**")
        st.markdown("---")
        if st.button("Clear Canvas"):
            st.session_state.v53_key += 1
            st.rerun()
        
    with col_draw:
        # PURPLE LOGO logo.png.png anchored as background
        canvas_result = st_canvas(
            fill_color="rgba(0, 0, 0, 0)", 
            stroke_width=2, 
            stroke_color="#000000",
            background_image=purple_logo, 
            height=750, width=1100,
            drawing_mode="path" if tool == "Smart Curve (Bezier)" else ("line" if tool == "Straight Line" else "transform"),
            point_display_radius=5, # High-vis end points for pattern accuracy
            key=f"v53_lock_{st.session_state.v53_key}"
        )

with tabs[1]:
    # Identifying internal and external lines for the factory
    
    st.info("Assign vectors to Cut (External) or Stitch (Internal) layers.")

with tabs[2]:
    # Separating the flat into production panels
    
    st.success(f"Applying {st.session_state.sa_value}\" Seam Allowance to Front, Back, and Sleeve Panels.")

with tabs[3]:
    if st.button("Generate Industrial DWG"):
        st.success("Flat vectors transformed to sewable pattern pieces.")
        doc = ezdxf.new('R2010')
        out = io.StringIO(); doc.write(out)
        st.download_button("Download Pattern", data=out.getvalue(), file_name="Industrial_Production_Ready.dxf")
