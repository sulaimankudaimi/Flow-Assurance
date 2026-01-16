import os
import streamlit as st
import pandas as pd
import numpy as np

# 1. إعدادات الصفحة
st.set_page_config(page_title="Flow Assurance AI", layout="wide")

import streamlit as st
import pandas as pd

# رابط الملف المباشر من جوجل درايف الذي أنشأته أنت
file_url = "https://drive.google.com/uc?export=download&id=1WBWBshf28y7Pd2QPE7KFD0mbjI3HI4fl"

@st.cache_data # هذه الوظيفة تمنع إعادة تحميل الملف في كل مرة (تسريع التطبيق)
def load_data_from_drive(url):
    try:
        # قراءة الملف مباشرة من الرابط
        df = pd.read_csv(url, low_memory=False)
        return df
    except Exception as e:
        st.error(f"⚠️ Error: Could not connect to Google Drive. {e}")
        return None

# تنفيذ التحميل
df = load_data_from_drive(file_url)

if df is not None:
    st.success("✅ Connected to Google Drive - Data Loaded Successfully!")
    # هنا تضع بقية كود التحليل والرسم البياني الذي كتبناه سابقاً
    st.dataframe(df.head())
# 3. محاولة تشغيل التطبيق
try:
    if os.path.exists("Norway-NA-15_47_9-F-9 A depth.csv"):
        df = pd.read_csv("Norway-NA-15_47_9-F-9 A depth.csv", low_memory=False)
    else:
        st.error("Please upload the CSV file to your GitHub repository!")
        st.stop()
except Exception as e:
    st.error(f"Error loading data: {e}")
