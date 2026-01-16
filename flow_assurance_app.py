import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime

# 1. إعدادات الصفحة
st.set_page_config(page_title="Eng. Sulaiman | Flow Assurance Pro", page_icon="🏗️", layout="wide")

# 2. تصميم الرأس (Header) الاحترافي
st.markdown("""
    <div style="background-color:#001f3f; padding:30px; border-radius:15px; border-left: 10px solid #ffcc00; margin-bottom:20px">
        <h1 style="color:white; margin:0; font-family:Arial;">🛡️ Flow Assurance Expert System</h1>
        <h3 style="color:#ffcc00; margin:10px 0 0 0; font-family:Arial;">Lead Engineer: Eng. Sulaiman</h3>
        <p style="color:#bdc3c7; font-size:1.1em;">Advanced Real-Time Anomaly Detection | Volve Field Asset Management</p>
    </div>
    """, unsafe_allow_html=True)

# 3. جلب البيانات (رابط مباشر لضمان استقرار التطبيق)
URL = "https://raw.githubusercontent.com/yrahul3910/Volve-Dataset/master/Well_F12_Production_Data.csv"

@st.cache_data
def load_and_clean_data(url):
    try:
        df = pd.read_csv(url, low_memory=False)
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        st.error(f"Error connecting to data: {e}")
        return None

df = load_and_clean_data(URL)

if df is not None:
    all_cols = df.columns.tolist()
    
    # دالة ذكية لاختيار الأعمدة تلقائياً
    def find_best(keys, default_idx):
        for c in all_cols:
            if any(k.lower() in c.lower() for k in keys): return c
        return all_cols[default_idx]

    # --- القائمة الجانبية ---
    st.sidebar.markdown("### 🛠️ Unit & Data Control")
    depth_col = st.sidebar.selectbox("Select Y-Axis (Depth/Time)", all_cols, 
                                     index=all_cols.index(find_best(['depth', 'date', 'time'], 0)))
    temp_col = st.sidebar.selectbox("Select X-Axis (Temperature/Pressure)", all_cols, 
                                    index=all_cols.index(find_best(['temp', 'press', 'bhp'], 1)))
    critical_val = st.sidebar.slider("Risk Threshold Value", 0.0, 500.0, 100.0)

    # تنظيف البيانات (التصحيح هنا: التأكد من إغلاق كل الأقواس)
    df[temp_col] = pd.to_numeric(df[temp_col], errors='coerce')
    df[depth_col] = pd.to_numeric(df[depth_col], errors='coerce')
    df = df.dropna(subset=[temp_col, depth_col])

    # حسابات المناطق الخطرة
    danger_zone = df[df[temp_col] < critical_val]
    
    # صف المؤشرات (KPIs)
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Max Recorded Value", f"{round(df[depth_col].max(), 1)}")
    m2.metric("Min Variable Value", f"{round(df[temp_col].min(), 2)}")
    
    if not danger_zone.empty:
        m3.metric("Risk Zone Identified", "YES", delta="ACTION REQ", delta_color="inverse")
        m4.metric("Risk Status", "⚠️ CRITICAL")
    else:
        m3.metric("Risk Zone Identified", "NO", delta="NORMAL")
        m4.metric("Risk Status", "✅ STABLE")

    st.divider()

    # --- العرض البياني والتحليل ---
    t1, t2, t3 = st.tabs(["📊 Interactive Analysis", "📜 Project Logic", "📂 Data Inspector"])

    with t1:
        col_chart, col_side = st.columns([2.5, 1])
        with col_chart:
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df[temp_col], y=df[depth_col], mode='lines', 
                                    name='Well Profile', line=dict(color='#00d4ff', width=2)))
            
            # منطقة الخطر
            fig.add_vrect(x0=df[temp_col].min(), x1=critical_val, fillcolor="red", opacity=0.1, 
                         layer="below", line_width=0, annotation_text="RISK ZONE")
            
            fig.update_yaxes(autorange="reversed", title=depth_col)
            fig.update_xaxes(title=temp_col)
            fig.update_layout(height=600, template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', 
                              plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)

        with col_side:
            st.markdown("### 🤖 Decision Support")
            if not danger_zone.empty:
                st.error("⚠️ DEPOSITION ALERT")
                st.write(f"The analysis indicates that the well parameters have dropped below the safe threshold of **{critical_val}**.")
            else:
                st.success("✅ SYSTEM STABLE")
                st.write("Current flow parameters are within the safe operating envelope.")

    with t2:
        st.markdown(f"""
        ### Executive Project Summary
        **Developed by:** Eng. Sulaiman
        **Objective:** This AI-driven tool monitors real-time production data to prevent Non-Productive Time (NPT) 
        caused by scale, wax, or asphaltene deposition.
        
        **Methodology:** By cross-referencing bottom-hole temperatures and pressures against thermodynamic envelopes, 
        the system flags anomalies before they lead to complete wellbore blockage.
        """)
        [Image of a diagram showing wax and asphaltene deposition envelopes in oil production]

    with t3:
        st.markdown("### Preview of Processed Dataset")
        st.dataframe(df.head(100), use_container_width=True)
else:
    st.error("Fatal Error: Could not connect to Data Source. Please check the URL.")
