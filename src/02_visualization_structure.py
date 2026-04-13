"""
图表2：商业结构 - 三城区位置类型占比堆叠柱状图
用途：展示三城区的商业结构差异（商务区 vs 混合社区 vs 景区）
"""

import pandas as pd
import matplotlib.pyplot as plt
import os

# ====== 配置中文字体 ======
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# ====== 读取数据 ======
data_path = r"C:\Users\Administrator\Desktop\data_learn\Hot-Drink-Retail-Analysis\data\processed\04_location_type_distribution.csv"
df = pd.read_csv(data_path)

# ====== 数据准备 ======
# 提取占比列
location_cols = ['抗寒：重度商务刚需_占比', '中庸：混合社区_占比', '脆弱：极度依赖天气_占比']
df_plot = df[['adname'] + location_cols].copy()

# 将百分比字符串转成数值
for col in location_cols:
    df_plot[col] = df_plot[col].str.rstrip('%').astype(float)

# ====== 创建图表 ======
fig, ax = plt.subplots(figsize=(10, 6))

# 定义颜色
colors_stack = ['#2ecc71', '#f39c12', '#e74c3c']  # 绿(商务)、橙(混合)、红(脆弱)

# 绘制堆叠柱状图
df_plot.set_index('adname')[location_cols].plot(
    kind='bar',
    stacked=True,
    ax=ax,
    color=colors_stack,
    width=0.6
)

# ====== 美化图表 ======
ax.set_ylabel('占比 (%)', fontsize=12, fontweight='bold')
ax.set_xlabel('城区', fontsize=12, fontweight='bold')
ax.set_title('北京三城区：商业结构对比\n（不同颜色代表不同的地段类型）', 
             fontsize=14, fontweight='bold', pad=20)

# 修改图例标签（去掉 _占比 后缀）
legend_labels = ['抗寒：重度商务刚需', '中庸：混合社区', '脆弱：极度依赖天气']
ax.legend(legend_labels, loc='upper right', fontsize=10)

# 旋转 X 轴标签，防止重叠
ax.set_xticklabels(ax.get_xticklabels(), rotation=0)

# 设置 Y 轴范围
ax.set_ylim(0, 100)

# 添加网格线
ax.grid(axis='y', alpha=0.3, linestyle='--')
ax.set_axisbelow(True)

plt.tight_layout()

# ====== 保存图表 ======
output_dir = r"C:\Users\Administrator\Desktop\data_learn\Hot-Drink-Retail-Analysis\reports"
os.makedirs(output_dir, exist_ok=True)
plt.savefig(os.path.join(output_dir, '02_商业结构_位置类型占比.png'), dpi=300, bbox_inches='tight')
print(f"✅ 图表已保存到: {os.path.join(output_dir, '02_商业结构_位置类型占比.png')}")

plt.show()
