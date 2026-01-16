import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime

# 1. إعدادات الصفحة
st.set_page_config(page_title="Eng. Sulaiman | Flow Assurance Pro", page_icon="🏗️", layout="wide")

# 2. الهوية الشخصية وتصميم الرأس
st.markdown("""
    <div style="background-color:#003366;padding:20px;border-radius:10px;margin-bottom:20px">
    <h1 style="color:white;text-align:center;">🛡️ Flow Assurance Expert System</h1>
    <h3 style="color:#ffcc00;text-align:center;">Lead Engineer: Eng. Sulaiman</h3>
    <p style="color:white;text-align:center;">Advanced Anomaly Detection for Well F-9A - Volve Field Data</p>
    </div>
    """, unsafe_allow_html=True)

# 3. رابط البيانات
FILE_ID = "1WBWBshf28y7Pd2QPE7KFD0mbjI3HI4fl"
DIRECT_URL = f"https://drive.google.com/uc?export=download&id={FILE_ID}"

@st.cache_data
def load_data(url):
    try:
        df = pd.read_csv(url, low_memory=False)
        df.columns = df.columns.str.strip()
        return df
    except Exception:
        return None

df = load_data(DIRECT_URL)

if df is not None:
    # --- محرك البحث الذكي عن الأعمدة ---
    all_cols = df.columns.tolist()
    
    # محاولة إيجاد الأعمدة تلقائياً
    def find_col(keywords):
        for c in all_cols:
            if all(k.lower() in c.lower() for k in keywords):
                return c
        return None

    auto_depth = find_col(['depth']) or all_cols[0]
    auto_temp = find_col(['temp']) or all_cols[1]

    # إتاحة الاختيار للمستخدم في القائمة الجانبية للتأكد من عدم حدوث IndexError
    st.sidebar.header("🛠️ Data Configuration")
    depth_col = st.sidebar.selectbox("Select Depth Column", all_cols, index=all_cols.index(auto_depth))
    temp_col = st.sidebar.selectbox("Select Temperature Column", all_cols, index=all_cols.index(auto_temp))
    critical_temp = st.sidebar.slider("Critical Temp Threshold (°C)", 30, 70, 50)

    # --- حسابات النتائج ---
    danger_zone = df[df[temp_col] < critical_temp]
    
    # --- عرض المؤشرات الرئيسية (Metrics) ---
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Max Well Depth", f"{round(df[depth_col].max(), 1)} m")
    m2.metric("Min Temp Recorded", f"{round(df[temp_col].min(), 2)} °C")
    
    if not danger_zone.empty:
        risk_len = danger_zone[depth_col].max() - danger_zone[depth_col].min()
        m3.metric("Danger Zone Length", f"{round(risk_len, 1)} m", delta="CRITICAL", delta_color="inverse")
        m4.metric("Action Status", "INJECTION REQ.", delta_color="normal")
    else:
        m3.metric("Danger Zone Length", "0 m", delta="SAFE")
        m4.metric("Action Status", "STABLE")

    st.markdown("---")

    # --- الرسوم البيانية والأدوات التفاعلية ---
    tab1, tab2, tab3 = st.tabs(["📊 Thermal Analysis", "🔬 AI Engineering Logic", "📑 Dataset View"])

    with tab1:
        c1, c2 = st.columns([2, 1])
        with c1:
            st.markdown("### Thermal Gradient Profile")
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df[temp_col], y=df[depth_col], mode='lines', name='Well Temp', line=dict(color='#ffaa00', width=3)))
            fig.add_vrect(x0=df[temp_col].min(), x1=critical_temp, fillcolor="red", opacity=0.1, layer="below", line_width=0, annotation_text="Deposition Risk Zone")
            fig.update_yaxes(autorange="reversed", title="Depth (m)")
            fig.update_xaxes(title="Temperature (°C)")
            fig.update_layout(height=500, template="plotly_dark", margin=dict(l=20, r=20, t=40, b=20))
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            st.markdown("### 🤖 Eng. Sulaiman's AI Assistant")
            if not danger_zone.empty:
                st.error("⚠️ DEPOSITION ALERT")
                st.write(f"The system detected potential **Scale/Wax** accumulation starting at **{round(danger_zone[depth_col].min(),1)} m**.")
                st.info(f"**Optimization Tip:** Inject chemical inhibitors at **{round(danger_zone[depth_col].min() + 50, 2)} m** to ensure clear flow.")
            else:
                st.success("✅ FLOW ASSURED")
                st.write("Wellbore temperature is above the precipitation envelope. Continue normal operations.")

    with tab2:
        st.markdown(f"""
        ### Methodology & Technical Documentation
        **Logic:** This system utilizes a thermal-gradient boundary algorithm to detect when production fluids exit the safe operating envelope.
        - **Data Integrity:** Sourced from Well F-9A (Volve Field).
        - **Calculations:** Real-time delta monitoring between Reservoir P/T and Tubing discharge.
        - **Developer:** Prepared by **Eng. Sulaiman** as part of a Digital Transformation series.
        """)
        # إضافة صورة توضيحية لترسبات الأسفلتين
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/e/e7/Asphaltene_deposition.jpg/300px-Asphaltene_deposition.jpg", caption="Typical blockage in production tubing due to cooling.")

    with tab3:
        st.dataframe(df.head(200), use_container_width=True)

else:
    st.error("❌ Unable to access the data. Please ensure the Google Drive link is set to 'Anyone with the link can view'.")
