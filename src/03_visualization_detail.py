"""
图表3：门店详情 - 散点图（写字楼 vs 公园）+ 气泡大小（抗性得分）+ 表格（Top 10）
用途：展示为什么不同城区的抗性差异，以及展示顶级高分门店
"""

import pandas as pd
import matplotlib.pyplot as plt
import os

# ====== 配置中文字体 ======
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# ====== 读取数据 ======
data_path = r"C:\Users\Administrator\Desktop\data_learn\Hot-Drink-Retail-Analysis\data\processed\04_residential_score.csv"
df = pd.read_csv(data_path, header=None)

# 手动设置列名（根据原始数据结构）
column_names = ['index', 'name', 'type', 'address', 'lon', 'lat', 'pname', 'cityname', 'adname', 'office_count', 'park_count', 'location_type', 'residential_score']
df.columns = column_names

print("CSV列名:", df.columns.tolist())
print(f"数据行数: {len(df)}")

# ====== 创建图表（包含子图）======
fig = plt.figure(figsize=(14, 10))

# ====== 子图1：散点图 ======
ax1 = plt.subplot(2, 1, 1)

# 定义城区颜色映射
color_map = {'东城区': '#3498db', '西城区': '#e74c3c', '朝阳区': '#2ecc71', '石景山区': '#f39c12'}
# 动态设置未定义城区的颜色
for adname in df['adname'].unique():
    if adname not in color_map:
        color_map[adname] = '#95a5a6'  # 灰色作为其他区域的默认颜色

colors = [color_map[adname] for adname in df['adname']]

# 绘制散点图（气泡大小代表抗性得分）
score_col = df.columns[-1]  # 最后一列是抗性得分
scatter = ax1.scatter(df['office_count'], df['park_count'], 
                      s=df[score_col]*5,  # 气泡大小
                      c=colors, 
                      alpha=0.6, 
                      edgecolors='black', 
                      linewidth=0.5)

ax1.set_xlabel('写字楼数量', fontsize=11, fontweight='bold')
ax1.set_ylabel('公园数量', fontsize=11, fontweight='bold')
ax1.set_title('北京饮品店选址特征分析\n（气泡大小代表抗性得分，颜色代表城区）', 
              fontsize=12, fontweight='bold', pad=15)

# 添加图例（只显示前3个主要城区）
from matplotlib.patches import Patch
legend_elements = [Patch(facecolor=color_map['东城区'], label='东城区'),
                   Patch(facecolor=color_map['西城区'], label='西城区'),
                   Patch(facecolor=color_map['朝阳区'], label='朝阳区')]
ax1.legend(handles=legend_elements, loc='upper right', fontsize=10)

# 添加网格
ax1.grid(alpha=0.3, linestyle='--')

# ====== 子图2：Top 10 高分店表格 ======
ax2 = plt.subplot(2, 1, 2)
ax2.axis('off')

# 提取Top 10高分店
df_top10 = df.nlargest(10, df.columns[-1])[['name', 'adname', 'location_type', 'office_count', df.columns[-1]]]
df_top10_display = df_top10.copy()
df_top10_display.columns = ['门店名称', '城区', '地段类型', '周边写字楼数', '抗性得分']
df_top10_display = df_top10_display.reset_index(drop=True)
df_top10_display.index = df_top10_display.index + 1  # 从1开始编号

# 创建表格
table_data = []
for idx, row in df_top10_display.iterrows():
    table_data.append([
        idx,
        row['门店名称'][:20],  # 截断长名称
        row['城区'],
        row['地段类型'][:8],   # 截断长标签
        row['周边写字楼数'],
        f"{row['抗性得分']:.1f}"
    ])

table = ax2.table(cellText=table_data,
                  colLabels=['排名', '门店名称', '城区', '地段类型', '写字楼数', '抗性得分'],
                  cellLoc='center',
                  loc='center',
                  bbox=[0, 0, 1, 1])

table.auto_set_font_size(False)
table.set_fontsize(9)
table.scale(1, 2)

# 美化表头
for i in range(6):
    table[(0, i)].set_facecolor('#34495e')
    table[(0, i)].set_text_props(weight='bold', color='white')

# 给每一行着色（奇偶行不同颜色）
for i in range(1, len(table_data) + 1):
    for j in range(6):
        if i % 2 == 0:
            table[(i, j)].set_facecolor('#ecf0f1')
        else:
            table[(i, j)].set_facecolor('#ffffff')

ax2.text(0.5, 1.05, 'Top 10 高分门店排行', 
         ha='center', fontsize=11, fontweight='bold', transform=ax2.transAxes)

plt.tight_layout()

# ====== 保存图表 ======
output_dir = r"C:\Users\Administrator\Desktop\data_learn\Hot-Drink-Retail-Analysis\reports"
os.makedirs(output_dir, exist_ok=True)
plt.savefig(os.path.join(output_dir, '03_门店详情_散点图与排行.png'), dpi=300, bbox_inches='tight')
print(f"✅ 图表已保存到: {os.path.join(output_dir, '03_门店详情_散点图与排行.png')}")

plt.show()
