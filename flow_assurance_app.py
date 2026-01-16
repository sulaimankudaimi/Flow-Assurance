import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os

# 1. إعدادات الصفحة الاحترافية
st.set_page_config(
    page_title="PetroVision: Flow Assurance Predictor",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ Flow Assurance: Well F-9A Anomaly Detector")
st.markdown("---")

# 2. رابط Google Drive (تحويله لرابط تحميل مباشر)
FILE_ID = "1WBWBshf28y7Pd2QPE7KFD0mbjI3HI4fl"
DIRECT_URL = f"https://drive.google.com/uc?export=download&id={FILE_ID}"

# 3. دالة تحميل البيانات مع التخزين المؤقت (Cache) للسرعة
@st.cache_data
def load_data(url):
    try:
        # قراءة البيانات مباشرة من جوجل درايف
        df = pd.read_csv(url, low_memory=False)
        # تنظيف أسماء الأعمدة من الفراغات الزائدة
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        st.error(f"⚠️ فشل الاتصال بقاعدة البيانات: {e}")
        return None

# تنفيذ التحميل
with st.spinner("📥 جاري جلب البيانات من السحابة..."):
    df = load_data(DIRECT_URL)

if df is not None:
    st.success("✅ تم الاتصال بجوجل درايف وجلب البيانات بنجاح!")

    # 4. البحث التلقائي عن الأعمدة (Depth & Temperature)
    try:
        depth_col = [c for c in df.columns if 'Depth' in c and 'm' in c][0]
        temp_col = [c for c in df.columns if 'Temperature' in c][0]
    except IndexError:
        st.error("❌ لم يتم العثور على أعمدة العمق أو الحرارة المطلوبة في الملف.")
        st.stop()

    # 5. واجهة المستخدم الجانبية (Sidebar)
    st.sidebar.header("⚙️ إعدادات التحليل")
    critical_temp = st.sidebar.slider("درجة الحرارة الحرجة (Critical Temp °C)", 30, 70, 50)
    
    # 6. توزيع الصفحة (Layout)
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("📈 منحنى التدرج الحراري (Thermal Gradient)")
        fig = px.line(df, x=temp_col, y=depth_col, labels={temp_col: "الحرارة (°C)", depth_col: "العمق (م)"})
        fig.update_yaxes(autorange="reversed")  # قلب المحور ليظهر العمق للأسفل
        fig.add_vrect(x0=min(df[temp_col]), x1=critical_temp, fillcolor="red", opacity=0.1, layer="below", line_width=0)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("🚨 تقرير مخاطر التدفق")
        danger_zone = df[df[temp_col] < critical_temp]
        
        if not danger_zone.empty:
            top_d = danger_zone[depth_col].min()
            bottom_d = danger_zone[depth_col].max()
            
            st.warning(f"تم اكتشاف منطقة خطر (Scale/Wax Risk)!")
            st.metric("أدنى درجة حرارة", f"{round(danger_zone[temp_col].min(), 2)} °C")
            st.info(f"📍 يمتد الخطر من عمق {round(top_d, 2)} م إلى {round(bottom_d, 2)} م")
            
            # توصية هندسية
            st.markdown(f"""
            **💡 توصية الخبير:**
            * يجب البدء بحقن مانعات الترسيب (Chemical Inhibitors) عند عمق **{round(top_d + 50, 2)} م**.
            * مراقبة ضغط رأس البئر (WHP) لأي ارتفاع مفاجئ.
            """)
        else:
            st.success("✅ البئر في حالة حرارية مستقرة حالياً.")

    # 7. عرض عينة من البيانات الخام
    with st.expander("🔍 استعراض البيانات الخام (Raw Data)"):
        st.dataframe(df.head(100))

else:
    st.info("يرجى التأكد من أن رابط Google Drive متاح للجميع (Anyone with the link can view).")
