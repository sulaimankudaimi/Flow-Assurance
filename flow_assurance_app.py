import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import os

# 1. إعدادات الصفحة
st.set_page_config(page_title="Eng. Sulaiman | Flow Assurance Pro", page_icon="🏗️", layout="wide")

# 2. الهوية الشخصية
st.markdown("""
    <div style="background-color:#001f3f; padding:30px; border-radius:15px; border-left: 10px solid #ffcc00; margin-bottom:20px">
        <h1 style="color:white; margin:0;">🛡️ Flow Assurance Expert System</h1>
        <h3 style="color:#ffcc00; margin:10px 0 0 0;">Lead Engineer: Eng. Sulaiman</h3>
    </div>
    """, unsafe_allow_html=True)

# 3. نظام جلب البيانات المرن
# سنحاول أولاً قراءة الملف إذا كان مرفوعاً على GitHub بجانب الكود
FILENAME = "Norway-NA-15_47_9-F-9 A depth.csv"

def load_data():
    if os.path.exists(FILENAME):
        return pd.read_csv(FILENAME, low_memory=False)
    return None

df = load_data()

# إذا لم يجد الملف، يطلب من المستخدم رفعه يدوياً (كخطة بديلة)
if df is None:
    st.warning(f"⚠️ الملف '{FILENAME}' غير موجود في المستودع.")
    uploaded_file = st.file_uploader("يرجى رفع ملف البيانات (CSV) لتشغيل المنحنيات:", type="csv")
    if uploaded_file:
        df = pd.read_csv(uploaded_file)

if df is not None:
    df.columns = df.columns.str.strip()
    all_cols = df.columns.tolist()

    # القائمة الجانبية
    st.sidebar.header("⚙️ التحليل الهندسي")
    y_axis = st.sidebar.selectbox("محور العمق (Y-Axis):", all_cols, index=0)
    x_axis = st.sidebar.selectbox("محور الحرارة (X-Axis):", all_cols, index=min(1, len(all_cols)-1))
    threshold = st.sidebar.slider("درجة الحرارة الحرجة (°C):", 0.0, 100.0, 50.0)

    # تنظيف البيانات المختارة
    df[x_axis] = pd.to_numeric(df[x_axis], errors='coerce')
    df[y_axis] = pd.to_numeric(df[y_axis], errors='coerce')
    df = df.dropna(subset=[x_axis, y_axis])

    # العرض
    m1, m2, m3 = st.columns(3)
    m1.metric("أقصى عمق", f"{round(df[y_axis].max(), 1)} m")
    m2.metric("أقل حرارة", f"{round(df[x_axis].min(), 2)} °C")
    m3.metric("حالة البئر", "خطر" if df[x_axis].min() < threshold else "آمن")

    # الرسم البياني
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df[x_axis], y=df[y_axis], mode='lines', line=dict(color='#00d4ff')))
    fig.add_vrect(x0=df[x_axis].min(), x1=threshold, fillcolor="red", opacity=0.1, annotation_text="منطقة الترسيب")
    fig.update_yaxes(autorange="reversed", title="Depth (m)")
    fig.update_xaxes(title="Temperature (°C)")
    fig.update_layout(height=600, template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("### 📑 عينة من البيانات")
    st.dataframe(df.head(10))
else:
    st.info("💡 بانتظار توفر البيانات لتوليد المنحنيات والتحليلات.")
