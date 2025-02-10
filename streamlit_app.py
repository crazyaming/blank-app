import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

# 設定中文字型
font_path = "./font.otf"  # 根目錄下的字型路徑
font_prop = FontProperties(fname=font_path)

st.title("滴定曲線繪製工具")

# 使用者輸入參數
st.sidebar.header("設定參數")
acid_concentration = st.sidebar.number_input("酸的濃度 (M)", min_value=0.01, max_value=10.0, value=0.1, step=0.01)
acid_volume = st.sidebar.number_input("酸的體積 (mL)", min_value=1.0, max_value=1000.0, value=50.0, step=1.0)
base_concentration = st.sidebar.number_input("鹼的濃度 (M)", min_value=0.01, max_value=10.0, value=0.1, step=0.01)

# 滴定過程模擬
base_added = np.linspace(0, acid_volume * 2, 500)  # 模擬加入不同體積的鹼
h3o_concentration = []

for v_base in base_added:
    if v_base == 0:
        h3o_concentration.append(acid_concentration)
    else:
        total_acid_moles = acid_concentration * acid_volume / 1000
        total_base_moles = base_concentration * v_base / 1000

        if total_base_moles < total_acid_moles:
            # 酸過量，計算 [H3O+]
            remaining_acid_moles = total_acid_moles - total_base_moles
            h3o_concentration.append(remaining_acid_moles / (acid_volume + v_base) * 1000)
        elif total_base_moles > total_acid_moles:
            # 鹼過量，計算 [OH-]
            excess_base_moles = total_base_moles - total_acid_moles
            oh_concentration = excess_base_moles / (acid_volume + v_base) * 1000
            h3o_concentration.append(1e-14 / oh_concentration)
        else:
            # 當量點
            h3o_concentration.append(1e-7)

# pH 計算
ph_values = -np.log10(h3o_concentration)

# 繪製滴定曲線
plt.figure(figsize=(8, 5))
plt.plot(base_added, ph_values, label="滴定曲線", color="blue")
plt.axhline(7, color="gray", linestyle="--", linewidth=0.7, label="中性 pH 7")
plt.xlabel("加入的鹼體積 (mL)", fontproperties=font_prop)
plt.ylabel("pH 值", fontproperties=font_prop)
plt.title("滴定曲線", fontproperties=font_prop)
plt.legend(prop=font_prop)
plt.grid(True, linestyle='--', alpha=0.6)

st.pyplot(plt)
