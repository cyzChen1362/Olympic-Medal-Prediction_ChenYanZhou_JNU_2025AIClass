import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import spearmanr


# 计算Spearman矩阵并画热力图

# 1. 读取数据
df = pd.read_excel(r'..\raw_data_processing\summerOly_medal_counts_SpearmanData.xlsx')

# 保证某一列的数据并不完全一样，这样算出来的Spearman系数才有意义
df = df.loc[:, df.nunique() > 1]

# 2. 计算Spearman相关系数
spearman_corr = df.corr(method='spearman')

# 3. 保存结果
spearman_corr.to_excel(r'..\Spearman_processing\Spearman_Result.xlsx')
print(spearman_corr)

# 读取 Spearman 计算结果
df = pd.read_excel(r'..\Spearman_processing\Spearman_Result.xlsx')

# 将所有 NaN 替换为 0
df = df.fillna(0)

# 保存为新的 Excel 文件
df.to_excel(r'..\Spearman_processing\Spearman_Result_filled.xlsx', index=False)

# 读取Spearman相关性结果
df = pd.read_excel(r'..\Spearman_processing\Spearman_Result_filled.xlsx', index_col=0)

# 画热力图
# 这里可能会警告，但没关系，图是可以出来的
plt.figure(figsize=(18, 18))
sns.heatmap(df, cmap='YlOrRd', square=True, linewidths=0.1, cbar=True)
plt.title('Spearman Correlation Heatmap', fontsize=20)
plt.xticks(rotation=90, fontsize=8)
plt.yticks(fontsize=8)

plt.tight_layout()
plt.savefig(r'..\Spearman_processing\Spearman_Correlation_Heatmap.png', dpi=300)
plt.show()

# %%

# 筛选特征

# 1. 读取 Spearman 相关性矩阵
spearman_corr = pd.read_excel(r'..\Spearman_processing\Spearman_Result.xlsx', index_col=0)

# 2. 读取同样已去除常数列的原始数据
df = pd.read_excel(r'..\raw_data_processing\summerOly_medal_counts_SpearmanData.xlsx')
df = df.loc[:, df.columns.isin(spearman_corr.columns)]  # 保证和相关性矩阵列一致

# 3. 目标变量
target_cols = ['Gold', 'Silver', 'Bronze', 'Total']

# 4. 存储结果
results = []

for target in target_cols:
    if target not in spearman_corr.columns:
        continue
    for feature in spearman_corr.columns:
        if feature == target:
            continue
        coef = spearman_corr.at[feature, target]
        # 计算p值
        valid = df[[feature, target]].dropna()
        if valid[feature].nunique() < 2 or valid[target].nunique() < 2:
            pval = None  # 避免意外
        else:
            _, pval = spearmanr(valid[feature], valid[target], nan_policy='omit')
        results.append({
            'feature': feature,
            'target': target,
            'spearmanr': coef,
            'p_value': pval
        })

# 5. 转为DataFrame
res_df = pd.DataFrame(results)

# 6. 只筛选相关性大于0.02且p值小于0.2的
filtered = res_df[(abs(res_df['spearmanr']) > 0.02) & (res_df['p_value'] < 0.2)]

# 7. 打印结果
print(filtered)

# 8. 保存结果到Excel
filtered.to_excel(r'..\Spearman_processing\Spearman_StrongCorr_Significant.xlsx', index=False)

