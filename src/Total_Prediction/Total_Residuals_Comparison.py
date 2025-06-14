import pandas as pd
import matplotlib.pyplot as plt

# 1. 路径
xgb_path = r'C:\Users\cyz13\PycharmProjects\AI_ClassProject\src\Total_Prediction\Total_XGBoost_Prediction_Data_with_Pred.xlsx'
rf_path  = r'C:\Users\cyz13\PycharmProjects\AI_ClassProject\src\Total_Prediction\Total_RF_Prediction_Data_with_Pred.xlsx'
bp_path  = r'C:\Users\cyz13\PycharmProjects\AI_ClassProject\src\Total_Prediction\Total_BP_Prediction_Data_with_Pred.xlsx'

# 2. 读取数据
xgb_df = pd.read_excel(xgb_path)
rf_df = pd.read_excel(rf_path)
bp_df = pd.read_excel(bp_path)

# 3. 计算残差
xgb_pred = xgb_df['Pred_Total'].values
xgb_true = xgb_df['Total'].values
xgb_resid = xgb_true - xgb_pred

rf_pred = rf_df['Pred_Total'].values
rf_true = rf_df['Total'].values
rf_resid = rf_true - rf_pred

bp_pred = bp_df['Pred_Total'].values
bp_true = bp_df['Total'].values
bp_resid = bp_true - bp_pred

# 4. 画图
plt.figure(figsize=(8, 5))
plt.scatter(rf_pred, rf_resid, s=0.2, c='b', alpha=0.8, label='RF')
plt.scatter(bp_pred, bp_resid, s=0.2, c='g', alpha=0.8, label='BP')
plt.scatter(xgb_pred, xgb_resid, s=0.2, c='r', alpha=0.8, label='XGBoost')
plt.axhline(0, color='k', linestyle='--', linewidth=1)
plt.xlabel('Predicted Values')
plt.ylabel('Residuals')
plt.title('Residuals Comparison: XGBoost vs RF vs BP')
plt.ylim(-200, 200)
plt.grid(True, linestyle=':')
plt.legend()
plt.tight_layout()
plt.savefig(r'C:\Users\cyz13\PycharmProjects\AI_ClassProject\src\Total_Prediction\Residuals_Comparison.png', dpi=300)
plt.show()