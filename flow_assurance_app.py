import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime

# 1. إعدادات الصفحة
st.set_page_config(
    page_title="Eng. Sulaiman Kudaimi | AI Systems",
    page_icon="💎",
    layout="wide"
)

# 2. هندسة الألوان النيونية والخطوط (CSS)
st.markdown("""
    <style>
    /* تغيير خلفية الصفحة */
    .stApp { background-color: #050a14; }
    
    /* تصميم البطاقات والمؤشرات باللون النيوني */
    [data-testid="stMetricValue"] {
        color: #00f2ff !important; /* لون نيوني أزرق */
        font-family: 'Courier New', monospace;
        font-weight: bold;
        font-size: 2.5rem !important;
        text-shadow: 0 0 10px #00f2ff, 0 0 20px #00f2ff;
    }
    [data-testid="stMetricLabel"] {
        color: #ffffff !important;
        font-size: 1.1rem !important;
        letter-spacing: 1px;
    }
    
    /* تصميم رأس الصفحة */
    .header-box {
        background: linear-gradient(135deg, #001f3f 0%, #000814 100%);
        padding: 30px;
        border-radius: 15px;
        border: 2px solid #00f2ff;
        box-shadow: 0 0 15px #00f2ff;
        margin-bottom: 25px;
        text-align: center;
    }
    
    /* شريط الحالة الجانبي */
    .sidebar-text {
        color: #00f2ff;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. الهوية الشخصية - مطور البرنامج
st.markdown("""
    <div class="header-box">
        <h1 style="color:#ffffff; margin:0; font-family:sans-serif;">🛡️ ADVANCED FLOW ASSURANCE SYSTEM</h1>
        <h2 style="color:#00f2ff; margin:10px 0; font-family:monospace; text-shadow: 0 0 5px #00f2ff;">
            Designed & Developed by: Eng. Sulaiman Kudaimi
        </h2>
        <p style="color:#8b949e;">Petroleum Systems Architecture | Digital Twin Technology</p>
    </div>
    """, unsafe_allow_html=True)

# 4. جلب البيانات
FILE_ID = "11AQ-g25zxWoF_dOPLhZvKnl4nDsvsDpA"
DIRECT_URL = f"https://drive.google.com/uc?export=download&id={FILE_ID}"

@st.cache_data
def load_data(url):
    try:
        df = pd.read_csv(url, low_memory=False)
        df.columns = df.columns.str.strip()
        return df
    except: return None

df = load_data(DIRECT_URL)

if df is not None:
    # القائمة الجانبية المحدثة
    st.sidebar.markdown(f"### 👨‍💻 System Architect")
    st.sidebar.markdown(f"<p class='sidebar-text'>Eng. Sulaiman Kudaimi</p>", unsafe_allow_html=True)
    st.sidebar.divider()
    
    all_cols = df.columns.tolist()
    y_axis = st.sidebar.selectbox("Select Depth Axis", all_cols, index=0)
    x_axis = st.sidebar.selectbox("Select Temperature Axis", all_cols, index=min(1, len(all_cols)-1))
    critical_limit = st.sidebar.slider("Risk Threshold (°C)", 0, 100, 50)

    # تحويل البيانات لأرقام
    df[x_axis] = pd.to_numeric(df[x_axis], errors='coerce')
    df[y_axis] = pd.to_numeric(df[y_axis], errors='coerce')
    df = df.dropna(subset=[x_axis, y_axis])

    # 5. عرض المؤشرات باللون النيوني (KPIs)
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("MAX DEPTH", f"{int(df[y_axis].max())} m")
    m2.metric("MIN TEMP", f"{round(df[x_axis].min(), 1)} °C")
    
    status = "CRITICAL" if df[x_axis].min() < critical_limit else "STABLE"
    m3.metric("SYSTEM HEALTH", status)
    m4.metric("DATA POINTS", f"{len(df):,}")

    st.divider()

    # 6. الرسم البياني التفاعلي
    col_chart, col_intel = st.columns([2, 1])
    
    with col_chart:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df[x_axis], y=df[y_axis],
            mode='lines',
            line=dict(color='#00f2ff', width=3),
            name='Well Profile'
        ))
        
        # تظليل منطقة الخطر بالنيون الأحمر
        fig.add_vrect(
            x0=df[x_axis].min(), x1=critical_limit,
            fillcolor="#ff0000", opacity=0.1,
            layer="below", line_width=0,
            annotation_text="HIGH RISK ZONE",
            annotation_font=dict(color="#ff0000")
        )
        
        fig.update_yaxes(autorange="reversed", title="Depth (m)", gridcolor="#1a1a1a")
        fig.update_xaxes(title="Temperature (°C)", gridcolor="#1a1a1a")
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=600
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_intel:
        st.markdown(f"### 🤖 AI Insight")
        if status == "CRITICAL":
            st.error(f"Attention Eng. Sulaiman: Potential Blockage Detected below {critical_limit}°C")
        else:
            st.success("System Stable: Safe Operating Envelope Maintained.")
        
        st.info("💡 Tip: Use the sidebar to adjust thresholds based on wax appearance temperature (WAT).")

    # تذيل الصفحة الثابت
    st.markdown(f"""
        <div style="text-align:center; padding:20px; color:#444;">
            <hr style="border-color:#1e1e1e;">
            Developed with AI Precision by <b>Eng. Sulaiman Kudaimi</b> | © {datetime.now().year}
        </div>
        """, unsafe_allow_html=True)
else:
    st.error("Connection Error. Please check data source.")
