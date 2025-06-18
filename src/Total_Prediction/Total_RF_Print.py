import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import t
from scipy.ndimage import uniform_filter1d

# %%

# ================= 数据处理 ===================

# 1. 读取数据
file_path = r'..\Total_Prediction\Total_RF_Prediction_Data_with_Pred.xlsx'
df = pd.read_excel(file_path)

true_values = df['Total'].values
predicted_values = df['Pred_Total'].values

# 2. 残差与误差统计
residuals = true_values - predicted_values
mse = np.mean(residuals ** 2)
rmse = np.sqrt(mse)
mae = np.mean(np.abs(residuals))
standard_error = np.std(residuals, ddof=1) / np.sqrt(len(residuals))
t_value = t.ppf(0.975, len(residuals) - 1)  # 95%
conf_interval = t_value * standard_error

print(f'全数据集均方误差 (MSE): {mse:.4f}')
print(f'全数据集均方根误差 (RMSE): {rmse:.4f}')
print(f'全数据集平均绝对误差 (MAE): {mae:.4f}')
print(f'全数据集标准误差 (SE): {standard_error:.4f}')
print(f'95% 置信区间: ±{conf_interval:.4f}')

# %%

# ================== 残差图 ===================

plt.figure(figsize=(6, 4))
plt.scatter(predicted_values, residuals, s=0.2, c='r', alpha=0.8, label='Residuals')
plt.axhline(0, color='b', linestyle='--', linewidth=1.5)
plt.xlabel('Predicted Values')
plt.ylabel('Residuals')
plt.title('RF Residual Plot')
plt.ylim(-200, 200)
plt.grid(True)
plt.tight_layout()
plt.savefig(r'..\Total_Prediction\Total_RF_Residual_Plot.png', dpi=300)
plt.show()

# %%

# =============== 置信区间折线图  ===============

# 1. 筛选 Total 最大的100个数据
top_idx = np.argsort(true_values)[-100:]         # 取 Total 最大的100个索引（升序，取最后100个）
top_idx = np.sort(top_idx)                       # 排序后画图更美观

true_values_top = true_values[top_idx]
predicted_values_top = predicted_values[top_idx]
residuals_top = true_values_top - predicted_values_top

# 2. 排序
sort_idx = np.argsort(true_values_top)  # 按true_values_top从小到大排序索引
true_values_top = true_values_top[sort_idx]
predicted_values_top = predicted_values_top[sort_idx]
n = len(residuals_top)
SE = np.std(residuals_top, ddof=1) / np.sqrt(n)

# 3. t分布置信区间
t_dict = {
    '95% CI': (t.ppf(0.975, n - 1), 15, (0.4, 0.7, 0.2)),
    '90% CI': (t.ppf(0.95, n - 1), 12, (0.4, 0.6, 0.2)),
    '80% CI': (t.ppf(0.9, n - 1), 10, (0.3, 0.5, 0.1)),
    '70% CI': (t.ppf(0.85, n - 1), 8, (0.2, 0.4, 0.1)),
    '60% CI': (t.ppf(0.8, n - 1), 7, (0.1, 0.3, 0.1)),
}
x = np.arange(n)
window_size = 10

# 4. 创建置信区间上界、下界
ci_bounds = {}
for label, (tval, mult, color) in t_dict.items():
    width = tval * SE * mult
    upper = true_values_top + width
    lower = true_values_top - width
    upper = uniform_filter1d(upper, size=window_size, mode='nearest')
    lower = uniform_filter1d(lower, size=window_size, mode='nearest')
    ci_bounds[label] = (upper, lower, color)

# 5. 画图
plt.figure(figsize=(10, 6))
for label, (upper, lower, color) in ci_bounds.items():
    plt.fill_between(x, upper, lower, color=color, alpha=0.4, label=label, edgecolor=None)

# 6. 预测&真实曲线
plt.plot(x, true_values_top, 'r--', linewidth=1, label='True Values')
plt.plot(x, predicted_values_top, color=(1, 0.7, 0), linestyle='--', linewidth=1.5, label='Predicted Values')

# 7. 用红色三角点标记超出95%置信区间的预测值
upper_95, lower_95, _ = ci_bounds['95% CI']
out_idx = np.where((predicted_values_top > upper_95) | (predicted_values_top < lower_95))[0]
plt.scatter(x[out_idx], predicted_values_top[out_idx], c='r', marker='^', s=60, label='Out of 95% CI')

plt.xlabel('Sample Index')
plt.ylabel('Values')
plt.title('RF Prediction Results with Confidence Intervals')
plt.grid(True)
plt.legend(loc='best', frameon=False)
plt.tight_layout()
plt.savefig(r'..\Total_Prediction\Total_RF_Confint_Plot.png', dpi=300)
plt.show()
