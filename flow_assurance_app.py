import os
import streamlit as st
import pandas as pd
import numpy as np

# 1. إعدادات الصفحة
st.set_page_config(page_title="Flow Assurance AI", layout="wide")

# 2. دالة تحميل البيانات الذكية
@st.cache_data
def load_data():
    # سنستخدم رابطاً مباشراً لملف Volve لضمان عدم توقف السحابة
    # إذا كنت رفعت الملف على GitHub، استبدل الرابط برابط الـ Raw الخاص بملفك
    url = "https://raw.githubusercontent.com/yrahul3910/Volve-Dataset/master/Well_F12_Production_Data.csv" 
    # ملاحظة: هذا رابط تجريبي، يفضل رفع ملفك الصغير F-9A على GitHub بجانب الكود
    df = pd.read_csv("Norway-NA-15_47_9-F-9 A depth.csv", low_memory=False)
    return df

# 3. محاولة تشغيل التطبيق
try:
    if os.path.exists("Norway-NA-15_47_9-F-9 A depth.csv"):
        df = pd.read_csv("Norway-NA-15_47_9-F-9 A depth.csv", low_memory=False)
    else:
        st.error("Please upload the CSV file to your GitHub repository!")
        st.stop()
except Exception as e:
    st.error(f"Error loading data: {e}")
