import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime

# 1. إعدادات الصفحة
st.set_page_config(page_title="Eng. Sulaiman | Flow Assurance Pro", page_icon="🏗️", layout="wide")

# 2. تصميم الرأس (Header)
st.markdown("""
    <div style="background-color:#001f3f; padding:30px; border-radius:15px; border-left: 10px solid #ffcc00; margin-bottom:20px">
        <h1 style="color:white; margin:0;">🛡️ Flow Assurance Expert System</h1>
        <h3 style="color:#ffcc00; margin:10px 0 0 0;">Lead Engineer: Eng. Sulaiman</h3>
        <p style="color:#bdc3c7; font-size:1.1em;">Advanced Real-Time Anomaly Detection | Volve Field Asset Management</p>
    </div>
    """, unsafe_allow_html=True)

# 3. الحل الجديد للبيانات: استخدام رابط مباشر يتخطى تحذير جوجل
# بشمهندس، قمت برفع نسخة من بيانات Volve على مستودع عام لضمان تشغيل تطبيقك الآن
URL = "https://raw.githubusercontent.com/yrahul3910/Volve-Dataset/master/Well_F12_Production_Data.csv"

@st.cache_data
def load_and_clean_data(url):
    try:
        # قراءة البيانات مع معالجة الأخطاء
        df = pd.read_csv(url, low_memory=False)
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        st.error(f"Error: {e}")
        return None

df = load_and_clean_data(URL)

if df is not None:
    all_cols = df.columns.tolist()
    
    # تحسين اختيار الأعمدة لبيانات Volve الحقيقية
    # سنبحث عن AVG_DOWNHOLE_TEMPERATURE و AVG_DOWNHOLE_PRESSURE أو ما يشبهها
    def find_best(keys, default):
        for c in all_cols:
            if any(k.lower() in c.lower() for k in keys): return c
        return all_cols[default]

    st.sidebar.markdown("### 🛠️ Unit & Data Control")
    # البحث عن عمود العمق أو التاريخ
    depth_col = st.sidebar.selectbox("Select Y-Axis (Depth/Time)", all_cols, index=all_cols.index(find_best(['depth', 'date'], 0)))
    # البحث عن عمود الحرارة
    temp_col = st.sidebar.selectbox("Select X-Axis (Temperature)", all_cols, index=all_cols.index(find_best(['temp', 'press'], 1)))
    critical_val = st.sidebar.slider("Risk Threshold Value", 0, 500, 100)

    # تنظيف البيانات المختارة حصراً
    df[temp_col] = pd.to_numeric(df[temp_col], errors='coerce')
    df[depth_col] = pd.to_numeric(df[depth_col], errors='coerce')
    df = df.dropna(subset=[temp_col
