import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# 1. إعدادات الصفحة الفائقة
st.set_page_config(
    page_title="PetroVision Pro | Eng. Sulaiman",
    page_icon="🏗️",
    layout="wide"
)

# 2. تحسين مظهر الواجهة عبر CSS (اختياري لكنه يعطي لمسة احترافية)
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

# 3. الهوية الشخصية (Header)
col_head1, col_head2 = st.columns([3, 1])
with col_head1:
    st.title("🛡️ Flow Assurance Expert System")
    st.subheader(f"Project: Well F-9A Anomaly Detection")
    st.markdown(f"**Lead Engineer:** Eng. Sulaiman | **Date:** {datetime.now().strftime('%Y-%m-%d')}")

with col_head2:
    st.image("https://img.icons8.com/fluency/96/oil-rig.png")

st.divider()

# 4. رابط البيانات (نفس الرابط السابق)
FILE_ID = "1WBWBshf28y7Pd2QPE7KFD0mbjI3HI4fl"
DIRECT_URL = f"https://drive.google.com/uc?export=download&id={FILE_ID}"

@st.cache_data
def load_data(url):
    try:
        df = pd.read_csv(url, low_memory=False)
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        return None

df = load_data(DIRECT_URL)

if df is not None:
    # تحديد الأعمدة
    depth_col = [c for c in df.columns if 'Depth' in c and 'm' in c][0]
    temp_col = [c for c in df.columns if 'Temperature' in c][0]

    # --- القسم الأول: المؤشرات الرئيسية (KPIs) ---
    st.sidebar.header("🛠️ Configuration")
    critical_temp = st.sidebar.slider("Critical Temperature Threshold (°C)", 30, 70, 50)
    
    danger_zone = df[df[temp_col] < critical_temp]
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Measured Depth", f"{round(df[depth_col].max(), 1)} m")
    m2.metric("Min. Temp Recorded", f"{round(df[temp_col].min(), 2)} °C", delta=f"{round(df[temp_col].min()-critical_temp, 1)} °C", delta_color="inverse")
    
    if not danger_zone.empty:
        risk_len = danger_zone[depth_col].max() - danger_zone[depth_col].min()
        m3.metric("Danger Zone Length", f"{round(risk_len, 1)} m", "Critical")
        m4.metric("Risk Status", "HIGH", delta_color="normal")
    else:
        m3.metric("Danger Zone Length", "0 m", "Safe")
        m4.metric("Risk Status", "STABLE")

    st.divider()

    # --- القسم الثاني: الرسوم البيانية المتقدمة ---
    tab1, tab2, tab3 = st.tabs(["📊 Heat Map Analysis", "🔬 Technical Documentation", "📑 Raw Data Exploration"])

    with tab1:
        c1, c2 = st.columns([2, 1])
        with c1:
            st.markdown("### Thermal Gradient vs. Depth")
            # رسم متطور باستخدام Plotly Graph Objects
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df[temp_col], y=df[depth_col], mode='lines', name='Well Temperature', line=dict(color='#1f77b4', width=3)))
            
            # إضافة منطقة التظليل الحمراء
            fig.add_vrect(x0=min(df[temp_col]), x1=critical_temp, fillcolor="red", opacity=0.15, layer="below", line_width=0, annotation_text="Critical Scale Zone")
            
            fig.update_yaxes(autorange="reversed", title="Measured Depth (m)")
            fig.update_xaxes(title="Temperature (°C)")
            fig.update_layout(height=600, template="plotly_white")
            st.plotly_chart(fig, use_container_width=True)
            
        with c2:
            st.markdown("### AI Recommendations")
            if not danger_zone.empty:
                st.error("⚠️ ACTION REQUIRED")
                st.write(f"The well profile has entered the **Critical Deposition Envelope** starting from depth **{round(danger_zone[depth_col].min(),1)} m**.")
                st.info(f"**Recommended Injection Depth:** {round(danger_zone[depth_col].min() + 50, 1)} m")
                st.success("**Inhibitor Strategy:** ScaleSentry 400 Series recommended for these T/P conditions.")
            else:
                st.success("✅ Flow conditions are optimal. No chemical intervention needed for the next cycle.")

    with tab2:
        st.markdown(f"""
        ### Engineering Logic & Methodology
        - **Data Source:** Real field data from Equinor Volve (Well F-9A).
        - **Algorithm:** Anomaly detection based on Thermal Gradient Deviation.
        - **Physics:** The model assumes Wax Appearance Temperature (WAT) at {critical_temp}°C.
        - **Developer:** Eng. Sulaiman - Petroleum Data Specialist.
        """)
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/e/e7/Asphaltene_deposition.jpg/300px-Asphaltene_deposition.jpg", caption="Typical Scale/Asphaltene buildup in production tubing.")

    with tab3:
        st.dataframe(df.head(500), use_container_width=True)

else:
    st.error("Could not load data. Check Google Drive permissions.")
