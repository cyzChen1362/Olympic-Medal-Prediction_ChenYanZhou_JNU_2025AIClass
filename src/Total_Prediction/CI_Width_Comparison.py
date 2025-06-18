import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import t

def compute_ci_width(true_values, predicted_values, window=10, alpha=0.05):
    n = len(true_values)
    ci_widths = np.zeros(n)
    half_win = window // 2
    for i in range(n):
        # 窗口内的残差
        left = max(0, i - half_win)
        right = min(n, i + half_win + 1)
        residuals_win = true_values[left:right] - predicted_values[left:right]
        se = np.std(residuals_win, ddof=1) / np.sqrt(len(residuals_win))
        tval = t.ppf(1 - alpha/2, len(residuals_win) - 1)
        ci_widths[i] = 2 * tval * se  # 上下界间距
    return ci_widths

def load_pred(file_path):
    df = pd.read_excel(file_path)
    return df['Total'].values, df['Pred_Total'].values

# --- 文件路径 ---
xgb_path = r'..\Total_Prediction\Total_XGBoost_Prediction_Data_with_Pred.xlsx'
rf_path  = r'..\Total_Prediction\Total_RF_Prediction_Data_with_Pred.xlsx'
bp_path  = r'..\Total_Prediction\Total_BP_Prediction_Data_with_Pred.xlsx'

# --- 读入全数据 ---
true_xgb, pred_xgb = load_pred(xgb_path)
true_rf, pred_rf   = load_pred(rf_path)
true_bp, pred_bp   = load_pred(bp_path)

# --- 排序（可选，按真实值从小到大） ---
sort_idx = np.argsort(true_xgb)  # 以XGBoost的真实值为基准排序
true_xgb = true_xgb[sort_idx]
pred_xgb = pred_xgb[sort_idx]
true_rf = true_rf[sort_idx]
pred_rf = pred_rf[sort_idx]
true_bp = true_bp[sort_idx]
pred_bp = pred_bp[sort_idx]

# --- 计算宽度 ---
window = 10  # 滑动窗口大小
ci_width_xgb = compute_ci_width(true_xgb, pred_xgb, window=window)
ci_width_rf  = compute_ci_width(true_rf, pred_rf, window=window)
ci_width_bp  = compute_ci_width(true_bp, pred_bp, window=window)

# --- 画图 ---
x = np.arange(len(true_xgb))
plt.figure(figsize=(12,6))
plt.plot(x, ci_width_xgb, label='XGBoost 95% CI Width', color='royalblue', linewidth=1)
plt.plot(x, ci_width_rf,  label='RF 95% CI Width', color='forestgreen', linewidth=1)
plt.plot(x, ci_width_bp,  label='BP 95% CI Width', color='orange', linewidth=1)
plt.xlabel('Sample Index (sorted by Total)')
plt.ylabel('95% Confidence Interval Width')
plt.title('Sample-wise 95% CI Width Comparison (XGBoost vs RF vs BP)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(r'..\Total_Prediction\CI_Width_Comparison_AllData.png', dpi=300)
plt.show()
