"""
图表1：对标排序 - 三城区高分店占比排序
用途：一眼看出哪个区的门店抗寒能力最强
"""

import pandas as pd
import matplotlib.pyplot as plt
import os

# ====== 配置中文字体 ======
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# ====== 读取数据 ======
data_path = r"C:\Users\Administrator\Desktop\data_learn\Hot-Drink-Retail-Analysis\data\processed\04_high_score_report.csv"
df = pd.read_csv(data_path)

# ====== 数据准备 ======
# 按高分店占比降序排列
df_sorted = df.sort_values('高分店占比(%)', ascending=False)

# ====== 创建图表 ======
fig, ax = plt.subplots(figsize=(10, 6))

# 绘制柱状图
colors = ['#2ecc71', '#f39c12', '#e74c3c']  # 绿、橙、红
bars = ax.bar(df_sorted['adname'], df_sorted['高分店占比(%)'], color=colors)

# ====== 美化图表 ======
ax.set_ylabel('高分店占比 (%)', fontsize=12, fontweight='bold')
ax.set_xlabel('城区', fontsize=12, fontweight='bold')
ax.set_title('北京三城区：门店抗寒能力对标排序\n（高分店占比越高，抗寒能力越强）', 
             fontsize=14, fontweight='bold', pad=20)

# 在每个柱子上显示数值
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{height:.2f}%',
            ha='center', va='bottom', fontsize=11, fontweight='bold')

# 添加网格线（使图表更易读）
ax.grid(axis='y', alpha=0.3, linestyle='--')
ax.set_axisbelow(True)

# 设置 Y 轴范围
ax.set_ylim(0, max(df_sorted['高分店占比(%)']) * 1.15)

plt.tight_layout()

# ====== 保存图表 ======
output_dir = r"C:\Users\Administrator\Desktop\data_learn\Hot-Drink-Retail-Analysis\reports"
os.makedirs(output_dir, exist_ok=True)
plt.savefig(os.path.join(output_dir, '01_对标排序_高分店占比.png'), dpi=300, bbox_inches='tight')
print(f"✅ 图表已保存到: {os.path.join(output_dir, '01_对标排序_高分店占比.png')}")

plt.show()
