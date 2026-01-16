import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime

# 1. إعدادات الصفحة
st.set_page_config(
    page_title="Eng. Sulaiman Kudaimi | Flow Assurance Pro",
    page_icon="🏗️",
    layout="wide"
)

# 2. التنسيق الجمالي (الأزرق النيوني والهوية)
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    [data-testid="stMetricValue"] {
        color: #00f2ff !important;
        text-shadow: 0 0 10px #00f2ff;
        font-family: 'Courier New', monospace;
    }
    .header-box {
        background: linear-gradient(90deg, #001f3f 0%, #003366 100%);
        padding: 30px;
        border-radius: 15px;
        border-left: 10px solid #ffcc00;
        text-align: center;
        margin-bottom: 20px;
    }
    .footer {
        position: fixed; left: 0; bottom: 0; width: 100%;
        background-color: #0e1117; color: #8b949e;
        text-align: center; padding: 10px; border-top: 1px solid #30363d;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("""
    <div class="header-box">
        <h1 style="color:white; margin:0;">🛡️ UNIVERSAL FLOW ASSURANCE ANALYZER</h1>
        <h3 style="color:#ffcc00; margin:10px 0;">Designed by: Eng. Sulaiman Kudaimi</h3>
    </div>
    """, unsafe_allow_html=True)

# 3. نظام تحميل البيانات المرن (درايف أو رفع يدوي)
FILE_ID = "11AQ-g25zxWoF_dOPLhZvKnl4nDsvsDpA"
DEFAULT_URL = f"https://drive.google.com/uc?export=download&id={FILE_ID}"

st.sidebar.title("📁 Data Source")
st.sidebar.markdown("**Project Developer:**\nEng. Sulaiman Kudaimi")
st.sidebar.divider()

# إضافة خيار الرفع اليدوي لتعميم الفائدة
upload_mode = st.sidebar.checkbox("📤 Upload Your Own Well Data", value=False)
uploaded_file = None

if upload_mode:
    uploaded_file = st.sidebar.file_uploader("Choose a CSV Well Log File", type="csv")

@st.cache_data
def load_data(source, is_uploaded=False):
    try:
        if is_uploaded:
            df = pd.read_csv(source)
        else:
            df = pd.read_csv(source, low_memory=False)
        df.columns = df.columns.str.strip()
        return df
    except Exception:
        return None

# تحديد مصدر البيانات
if upload_mode and uploaded_file is not None:
    df = load_data(uploaded_file, is_uploaded=True)
    st.sidebar.success("✅ Custom Data Loaded!")
else:
    df = load_data(DEFAULT_URL)
    if not upload_mode:
        st.sidebar.info("🌐 Using Volve Field Default Data")

# 4. معالجة وعرض البيانات
if df is not None:
    # تحويل الأعمدة لأرقام
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='ignore')

    all_cols = df.columns.tolist()
    
    col_param1, col_param2 = st.sidebar.columns(2)
    y_axis = col_param1.selectbox("Y-Axis (Depth):", all_cols, index=0)
    x_axis = col_param2.selectbox("X-Axis (Temp):", all_cols, index=min(1, len(all_cols)-1))
    
    critical_limit = st.sidebar.slider("🚨 Risk Threshold", 0.0, 200.0, 50.0)

    # عرض المؤشرات باللون النيوني
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Max Depth", f"{round(df[y_axis].max(), 1)} m")
    m2.metric("Min Temp", f"{round(df[x_axis].min(), 2)} °C")
    m3.metric("Status", "CRITICAL" if df[x_axis].min() < critical_limit else "STABLE")
    m4.metric("Samples", f"{len(df):,}")

    # الرسم البياني التفاعلي
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df[x_axis], y=df[y_axis], mode='lines', 
                            line=dict(color='#00f2ff', width=2)))
    
    fig.add_vrect(x0=df[x_axis].min(), x1=critical_limit, fillcolor="red", opacity=0.1, 
                 layer="below", line_width=0, annotation_text="⚠️ DEPOSITION RISK")
    
    fig.update_yaxes(autorange="reversed", title=y_axis, gridcolor="#30363d")
    fig.update_xaxes(title=x_axis, gridcolor="#30363d")
    fig.update_layout(template="plotly_dark", height=600, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
        <div class="footer">
            <p>Global Flow Assurance Tool | <b>Eng. Sulaiman Kudaimi</b> © 2024</p>
        </div>
        """, unsafe_allow_html=True)
else:
    st.warning("⚠️ بانتظار تحميل البيانات... يرجى رفع ملف CSV أو التأكد من الاتصال.")
