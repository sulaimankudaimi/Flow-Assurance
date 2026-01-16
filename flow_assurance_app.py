import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime

# 1. إعدادات الصفحة
st.set_page_config(page_title="Eng. Sulaiman | Flow Assurance Pro", page_icon="🏗️", layout="wide")

# 2. تصميم الرأس (Header) - محسن ليكون أكثر فخامة
st.markdown("""
    <div style="background-color:#001f3f; padding:30px; border-radius:15px; border-left: 10px solid #ffcc00; margin-bottom:20px">
        <h1 style="color:white; margin:0;">🛡️ Flow Assurance Expert System</h1>
        <h3 style="color:#ffcc00; margin:10px 0 0 0;">Lead Engineer: Eng. Sulaiman</h3>
        <p style="color:#bdc3c7; font-size:1.1em;">Advanced Real-Time Anomaly Detection | Volve Field Asset Management</p>
    </div>
    """, unsafe_allow_html=True)

# 3. جلب البيانات من الرابط
FILE_ID = "1WBWBshf28y7Pd2QPE7KFD0mbjI3HI4fl"
DIRECT_URL = f"https://drive.google.com/uc?export=download&id={FILE_ID}"

@st.cache_data
def load_and_clean_data(url):
    try:
        df = pd.read_csv(url, low_memory=False)
        df.columns = df.columns.str.strip()
        # تنظيف البيانات من القيم الفارغة في الأعمدة الأساسية لضمان دقة الرسم
        df = df.replace([np.inf, -np.inf], np.nan).dropna(subset=[c for c in df.columns if 'Depth' in c or 'Temp' in c], how='all')
        return df
    except Exception:
        return None

df = load_and_clean_data(DIRECT_URL)

if df is not None:
    all_cols = df.columns.tolist()
    
    # محرك البحث الذكي (محسن)
    def find_best_col(keywords, default_index):
        for c in all_cols:
            if any(k.lower() in c.lower() for k in keywords):
                return c
        return all_cols[default_index]

    # إعدادات القائمة الجانبية
    st.sidebar.markdown("### 🛠️ Unit & Data Control")
    depth_col = st.sidebar.selectbox("Select Depth Column (Vertical Axis)", all_cols, index=all_cols.index(find_best_col(['depth', 'measured'], 0)))
    temp_col = st.sidebar.selectbox("Select Temperature Column (Horizontal Axis)", all_cols, index=all_cols.index(find_best_col(['temp', 'annular'], 1)))
    critical_temp = st.sidebar.slider("Wax/Scale Risk Threshold (°C)", 20, 80, 50)

    # التحقق من أن البيانات المختارة أرقام وليست نصوصاً (لحل أخطاء الرسم)
    df[depth_col] = pd.to_numeric(df[depth_col], errors='coerce')
    df[temp_col] = pd.to_numeric(df[temp_col], errors='coerce')
    df = df.dropna(subset=[depth_col, temp_col])

    # حسابات المناطق الخطرة
    danger_zone = df[df[temp_col] < critical_temp]
    
    # صف المؤشرات (KPIs)
    m1, m2, m3, m4 = st.columns(4)
    with m1: st.metric("Max Logged Depth", f"{round(df[depth_col].max(), 1)} m")
    with m2: st.metric("Lowest Temp Detected", f"{round(df[temp_col].min(), 2)} °C")
    
    if not danger_zone.empty:
        risk_interval = danger_zone[depth_col].max() - danger_zone[depth_col].min()
        m3.metric("Critical Zone Length", f"{round(risk_interval, 1)} m", delta="ACTION REQ", delta_color="inverse")
        m4.metric("Risk Status", "⚠️ CRITICAL")
    else:
        m3.metric("Critical Zone Length", "0 m", delta="NORMAL")
        m4.metric("Risk Status", "✅ STABLE")

    st.markdown("---")

    # التبويبات (Tabs)
    t1, t2, t3 = st.tabs(["📊 Interactive Analysis", "📜 Project Logic", "📂 Data Inspector"])

    with t1:
        col_chart, col_side = st.columns([2.5, 1])
        with col_chart:
            # رسم بياني تفاعلي متقدم
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df[temp_col], y=df[depth_col], mode='lines+markers', 
                                    name='Well Profile', line=dict(color='#00d4ff', width=2),
                                    marker=dict(size=2, opacity=0.5)))
            
            # منطقة الخطر بالتظليل
            fig.add_vrect(x0=df[temp_col].min(), x1=critical_temp, fillcolor="red", opacity=0.1, 
                         layer="below", line_width=0, annotation_text="SCALE DEPOSITION RISK ZONE")
            
            fig.update_yaxes(autorange="reversed", title="Depth (m)", gridcolor='#333')
            fig.update_xaxes(title="Temperature (°C)", gridcolor='#333')
            fig.update_layout(height=650, template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', 
                              plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=0, r=0, t=30, b=0))
            st.plotly_chart(fig, use_container_width=True)

        with col_side:
            st.markdown("### 🤖 Engineer's Decision Support")
            if not danger_zone.empty:
                st.error(f"Detection: Sub-critical cooling found at {round(danger_zone[depth_col].min(), 1)}m")
                st.markdown(f"""
                **Automated Recommendations:**
                1. **Chemical Injection:** Set point at **{round(danger_zone[depth_col].min() - 20, 1)}m**.
                2. **Flow Check:** Increase frequency of WHP monitoring.
                3. **Mitigation:** Evaluate heater-treater efficiency.
                """)
            else:
                st.success("Analysis complete: All parameters within safe operating envelope.")

    with t2:
        st.markdown(f"""
        ### Executive Summary
        This system, developed by **Eng. Sulaiman**, bridges the gap between raw sensor data and operational decision-making. 
        It specifically targets **Flow Assurance**, the science of ensuring oil and gas are produced economically throughout the life of the field.
        
        **Technical Specs:**
        - **Source:** Equinor Volve Field.
        - **Model:** Real-time Gradient Deviation Analysis.
        - **Impact:** Prevention of Non-Productive Time (NPT).
        """)

    with t3:
        st.dataframe(df.head(500), use_container_width=True)

else:
    st.error("❌ Fatal Error: Secure link to Google Drive failed. Check permissions.")
