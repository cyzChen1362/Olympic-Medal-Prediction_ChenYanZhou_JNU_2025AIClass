import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# 读取Excel文件
file_path = r'C:\Users\cyz13\PycharmProjects\AI_ClassProject\src\raw_data_processing\summerOly_programs.xlsx'
df = pd.read_excel(file_path)

# 只保留Code和年份数据
df_years = df.loc[:, [df.columns[2]] + list(df.columns[4:])]

# 统一将不是数字的值（无法转为float的）视为缺失值
def is_number_or_nan(x):
    try:
        float(x)
        return x
    except:
        return np.nan

# 对除第一列外的所有值进行清洗
df_years.iloc[:, 1:] = df_years.iloc[:, 1:].applymap(is_number_or_nan)

# 设置图像尺寸
plt.figure(figsize=(20, 20))

# 绘制缺失值热力图
sns.heatmap(
    df_years.iloc[:, 1:].isnull(),
    cbar=True,
    cmap='YlGnBu',
    yticklabels=df_years[df.columns[2]],
    xticklabels=df_years.columns[1:],   # 年份
    linewidths=1,
    linecolor='gray'
)

plt.title('Missing Value Heatmap', fontsize=18)
plt.xlabel('Year', fontsize=14)
plt.ylabel('Event', fontsize=14)
plt.tight_layout()

# 保存图片
save_path = r'C:\Users\cyz13\PycharmProjects\AI_ClassProject\src\OlyEvent_Missing_Value\missing_heatmap_square.png'
plt.savefig(save_path, dpi=300)
plt.close()

print(f"缺失值热力图已保存到：{save_path}")
