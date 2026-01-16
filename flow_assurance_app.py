import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# 1. إعدادات الصفحة
st.set_page_config(
    page_title="Eng. Sulaiman Kudaimi | Flow Assurance Pro",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. تصميم الواجهة الاحترافية (تعديل ألوان الأرقام إلى أزرق نيوني)
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    
    /* تنسيق كروت الأرقام (Metrics) باللون الأزرق النيوني */
    [data-testid="stMetricValue"] {
        color: #00f2ff !important;
        font-family: 'Courier New', Courier, monospace;
        font-weight: bold;
        text-shadow: 0 0 10px #00f2ff, 0 0 20px #00f2ff;
        font-size: 1.8rem !important;
    }
    
    /* تنسيق عناوين الكروت */
    [data-testid="stMetricLabel"] {
        color: #ffffff !important;
        font-size: 1.1rem !important;
        font-weight: 500;
    }

    .header-box {
        background: linear-gradient(90deg, #001f3f 0%, #003366 100%);
        padding: 40px;
        border-radius: 15px;
        border-left: 10px solid #ffcc00;
        margin-bottom: 30px;
        text-align: center;
    }
    
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #0e1117;
        color: #8b949e;
        text-align: center;
        padding: 10px;
        font-size: 14px;
        border-top: 1px solid #30363d;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. الهوية الشخصية ورأس الصفحة
st.markdown("""
    <div class="header-box">
        <h1 style="color:white; margin:0; font-family:sans-serif; letter-spacing: 2px;">🛡️ WELL FLOW ASSURANCE EXPERT</h1>
        <h2 style="color:#ffcc00; margin:15px 0 5px 0; font-family:sans-serif;">Developed & Designed by: Eng. Sulaiman Kudaimi</h2>
        <p style="color:#bdc3c7; font-size:1.2em;">Advanced Digital Transformation in Petroleum Production Operations</p>
    </div>
    """, unsafe_allow_html=True)

# 4. الربط مع البيانات
FILE_ID = "11AQ-g25zxWoF_dOPLhZvKnl4nDsvsDpA"
DIRECT_URL = f"https://drive.google.com/uc?export=download&id={FILE_ID}"

@st.cache_data
def load_data(url):
    try:
        df = pd.read_csv(url, low_memory=False)
        df.columns = df.columns.str.strip()
        return df
    except Exception:
        return None

with st.spinner('📡 Connecting to Global Asset Data...'):
    df = load_data(DIRECT_URL)

if df is not None:
    # تنظيف البيانات
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='ignore')

    # --- القائمة الجانبية (Sidebar) بعد التعديل ---
    st.sidebar.image("https://img.icons8.com/fluency/96/oil-rig.png", width=100)
    st.sidebar.title("🎮 Control Panel")
    
    # تعديل المسمى الوظيفي والاسم الكامل
    st.sidebar.markdown("---")
    st.sidebar.markdown("**Project Developer:**")
    st.sidebar.info("Eng. Sulaiman Kudaimi")
    st.sidebar.markdown("---")
    
    all_cols = df.columns.tolist()
    y_axis = st.sidebar.selectbox("Select Depth/Time Axis:", all_cols, index=0)
    x_axis = st.sidebar.selectbox("Select Temperature/Parameter:", all_cols, index=min(1, len(all_cols)-1))
    
    st.sidebar.divider()
    critical_limit = st.sidebar.slider("🚨 Critical Risk Threshold", 0.0, 200.0, 50.0)
    
    if st.sidebar.button("♻️ Reset Analysis"):
        st.rerun()

    # --- لوحة المؤشرات الرقمية (KPIs) بالألوان الجديدة ---
    st.markdown("### 📊 Real-Time Asset Metrics")
    m1, m2, m3, m4 = st.columns(4)
    
    max_val = df[y_axis].max()
    min_temp = df[x_axis].min()
    risk_status = "CRITICAL" if min_temp < critical_limit else "STABLE"
    
    m1.metric("Logged Depth/Interval", f"{round(max_val, 1)} m")
    m2.metric("Min. Measured Temp", f"{round(min_temp, 2)} °C")
    m3.metric("System Health", risk_status, delta="Risk Detected" if risk_status=="CRITICAL" else "Safe", delta_color="inverse")
    m4.metric("Data Points Collected", f"{len(df):,}")

    st.divider()

    # --- العرض البياني ---
    col_chart, col_info = st.columns([2, 1])

    with col_chart:
        st.markdown(f"### 📈 Interactive Profile: {x_axis} vs {y_axis}")
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df[x_axis], y=df[y_axis],
            mode='lines',
            name='Wellbore Profile',
            line=dict(color='#00f2ff', width=2) # اللون النيوني للمنحنى أيضاً
        ))
        
        fig.add_vrect(
            x0=df[x_axis].min(), x1=critical_limit,
            fillcolor="red", opacity=0.15,
            layer="below", line_width=0,
            annotation_text="⚠️ SCALE/WAX RISK ZONE"
        )

        fig.update_yaxes(autorange="reversed", title=f"Vertical Depth (m)", gridcolor="#30363d")
        fig.update_xaxes(title=f"Temperature (°C)", gridcolor="#30363d")
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=600,
            margin=dict(l=20, r=20, t=50, b=20)
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_info:
        st.markdown("### 🤖 Engineering Decision Support")
        if risk_status == "CRITICAL":
            st.error("🚨 HIGH DEPOSITION RISK DETECTED")
            st.write(f"Precipitation is likely occurring in the upper tubing strings at T < {critical_limit}°C.")
        else:
            st.success("✅ FLOW ASSURED")
            st.write("Wellbore temperature is within safe envelope.")
        
        st.divider()
        st.info(f"**Official Report Generated for:**\nEng. Sulaiman Kudaimi")

    # --- تذيل الصفحة ---
    st.markdown(f"""
        <div class="footer">
            <p>Designed & Developed with Passion by <b>Eng. Sulaiman Kudaimi</b> | Petroleum Production Digital Solutions © 2024</p>
        </div>
        """, unsafe_allow_html=True)
else:
    st.error("❌ Fatal Connection Error!")
