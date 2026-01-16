import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# 1. إعدادات الصفحة الفاخرة
st.set_page_config(
    page_title="Eng. Sulaiman Kudaimi | Flow Assurance AI",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. تصميم الواجهة الاحترافية (Custom CSS)
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #161b22; padding: 20px; border-radius: 12px; border: 1px solid #30363d; }
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

# 4. الربط الذكي مع Google Drive
# استخراج ID الملف من الرابط الجديد الذي زودتني به
FILE_ID = "11AQ-g25zxWoF_dOPLhZvKnl4nDsvsDpA"
DIRECT_URL = f"https://drive.google.com/uc?export=download&id={FILE_ID}"

@st.cache_data
def load_data(url):
    try:
        # قراءة البيانات مع محاولة تجاوز حواجز جوجل
        df = pd.read_csv(url, low_memory=False)
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        return None

# تنفيذ التحميل مع مؤشر انتظار احترافي
with st.spinner('📡 Connecting to Global Asset Data...'):
    df = load_data(DIRECT_URL)

if df is not None:
    # تنظيف البيانات وتحويلها لأرقام
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='ignore')

    # --- القائمة الجانبية (Sidebar) ---
    st.sidebar.image("https://img.icons8.com/fluency/96/oil-rig.png", width=100)
    st.sidebar.title("🎮 Control Panel")
    st.sidebar.markdown(f"**User:** Eng. Sulaiman")
    
    all_cols = df.columns.tolist()
    y_axis = st.sidebar.selectbox("Select Depth/Time Axis:", all_cols, index=0)
    x_axis = st.sidebar.selectbox("Select Temperature/Parameter:", all_cols, index=min(1, len(all_cols)-1))
    
    st.sidebar.divider()
    critical_limit = st.sidebar.slider("🚨 Critical Risk Threshold", 0.0, 200.0, 50.0)
    
    if st.sidebar.button("♻️ Reset Analysis"):
        st.rerun()

    # --- لوحة المؤشرات الرقمية (KPIs) ---
    st.markdown("### 📊 Real-Time Asset Metrics")
    m1, m2, m3, m4 = st.columns(4)
    
    max_val = df[y_axis].max()
    min_temp = df[x_axis].min()
    risk_status = "CRITICAL" if min_temp < critical_limit else "STABLE"
    
    m1.metric("Logged Depth/Interval", f"{round(max_val, 1)} m")
    m2.metric("Min. Measured Temp", f"{round(min_temp, 2)} °C")
    m3.metric("System Health", risk_status, delta="Risk Detected" if risk_status=="CRITICAL" else "Safe", delta_color="inverse")
    m4.metric("Data Points", len(df))

    st.divider()

    # --- العرض البياني التفاعلي ---
    col_chart, col_info = st.columns([2, 1])

    with col_chart:
        st.markdown(f"### 📈 Interactive Profile: {x_axis} vs {y_axis}")
        fig = go.Figure()
        
        # إضافة المنحنى الرئيسي
        fig.add_trace(go.Scatter(
            x=df[x_axis], y=df[y_axis],
            mode='lines+markers',
            name='Wellbore Profile',
            line=dict(color='#00d4ff', width=2),
            marker=dict(size=3, opacity=0.4)
        ))
        
        # إضافة تظليل منطقة الخطر
        fig.add_vrect(
            x0=df[x_axis].min(), x1=critical_limit,
            fillcolor="red", opacity=0.15,
            layer="below", line_width=0,
            annotation_text="⚠️ SCALE/WAX RISK ZONE",
            annotation_position="top left"
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
            st.write(f"The well profile has crossed the threshold of **{critical_limit}°C**. Precipitation is likely occurring in the upper tubing strings.")
            st.markdown("""
            **Recommended Actions:**
            - Activate chemical injection pump.
            - Optimize Choke size to maintain T > Threshold.
            - Schedule Wireline Scraper if pressure drops.
            """)
        else:
            st.success("✅ FLOW ASSURED")
            st.write("Wellbore temperature is within the safe operating envelope. No immediate intervention required.")
        
        st.divider()
        st.info(f"**Report Generated for:**\nEng. Sulaiman Kudaimi")

    # --- تذيل الصفحة ---
    st.markdown(f"""
        <div class="footer">
            <p>Designed & Developed with Passion by <b>Eng. Sulaiman Kudaimi</b> | Petroleum Production Digital Solutions © 2024</p>
        </div>
        """, unsafe_allow_html=True)

else:
    st.error("❌ Fatal Connection Error!")
    st.markdown(f"""
    **بشمهندس سليمان، يبدو أن جوجل درايف ما زال يحجب الملف بسبب 'فحص الفيروسات'.**
    
    **الحل النهائي المضمون 100%:**
    1. ارفع ملف الـ CSV مباشرة على GitHub في نفس المستودع.
    2. سأقوم بتعديل سطر واحد فقط في الكود ليقرأه من هناك فوراً وتظهر هذه الواجهة الفاخرة.
    """)
