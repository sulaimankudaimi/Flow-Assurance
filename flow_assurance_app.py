import kagglehub
import pandas as pd
import os
import numpy as np

# 1. تحميل البيانات من المصدر الذي اخترته
print("📥 Downloading Well F-9A data...")
path = kagglehub.dataset_download("imranulhaquenoor/volve-dataset-well-f-9-a")

# 2. تحديد وقراءة ملف العمق (Depth) لأنه يحتوي على الحرارة والعمق معاً
file_name = 'Norway-NA-15_47_9-F-9 A depth.csv'
full_path = os.path.join(path, file_name)

# قراءة البيانات مع تجاهل تنبيهات الأنواع
df = pd.read_csv(full_path, low_memory=False)

# 3. تنظيف أسماء الأعمدة وتحديد الأعمدة المطلوبة
df.columns = df.columns.str.strip()
try:
    depth_col = [c for c in df.columns if 'Depth' in c and 'm' in c][0]
    temp_col = [c for c in df.columns if 'Temperature' in c][0]
    print(f"✅ Analysis started using: {depth_col} and {temp_col}")
except IndexError:
    print("❌ Could not find exact columns. Check the column names!")
    depth_col, temp_col = None, None

if depth_col and temp_col:
    # 4. محرك تحليل الخطر (Risk Engine)
    CRITICAL_TEMP = 50.0 
    danger_zone = df[df[temp_col] < CRITICAL_TEMP].copy()

    if not danger_zone.empty:
        top_danger = danger_zone[depth_col].min()
        bottom_danger = danger_zone[depth_col].max()
        min_temp = danger_zone[temp_col].min()
        
        print("\n" + "="*55)
        print("🚨 WELL FLOW ASSURANCE RISK REPORT - WELL F-9A")
        print("="*55)
        print(f"📍 STATUS: CRITICAL SCALE/WAX RISK")
        print(f"🌡️ Minimum Temperature Recorded: {round(min_temp, 2)} °C")
        print("-" * 40)
        print(f"🚧 Danger Zone Depth: From {round(top_danger, 2)} m to {round(bottom_danger, 2)} m")
        print(f"📏 Total Affected Interval: {round(bottom_danger - top_danger, 2)} meters")
        print("-" * 40)
        print(f"💡 RECOMMENDATION:")
        print(f"   - Monitor Wellhead Pressure (WHP) for abnormal increases.")
        print(f"   - Inject Chemical Inhibitors at depth: {round(top_danger + 50, 2)} m.")
        print("="*55)
    else:
        print("✅ STATUS: WELL THERMALLY STABLE")