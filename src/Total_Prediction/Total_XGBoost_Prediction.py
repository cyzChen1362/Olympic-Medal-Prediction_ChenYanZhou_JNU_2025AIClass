import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.metrics import mean_absolute_error
from sklearn.preprocessing import LabelEncoder
import shap

# %%

# =============== XGBoost部分 ==================

# 1. 读取数据（筛选后）
file_path = r'C:\Users\cyz13\PycharmProjects\AI_ClassProject\src\Total_Prediction\Total_Prediction_Data.xlsx'
df = pd.read_excel(file_path)

features = [
    'NOC', 'Host', 'ATP', 'Cnt', 'BOX', 'CSP', 'EDR',
    'EVL', 'GAR', 'MPN', 'POL', 'RUG', 'SHO', 'TEN',
    'TOW', 'VVO', 'WRG', 'FSK', 'IHO'
]
target = 'Total'

# 1. 读取数据（筛选前）
# file_path = r'C:\Users\cyz13\PycharmProjects\AI_ClassProject\src\ATP_processing\summerOly_medal_counts_ATP.xlsx'
# df = pd.read_excel(file_path)
#
# features = [
#     "NOC", "ATP", "Cnt", "Host",
#     "SWA", "DIV", "OWS", "SWM", "WPO", "ARC", "ATH",
#     "BDM", "BSB", "SBL", "BK3", "BKB", "PEL", "BOX", "BKG", "CSP", "CSL", "CKT", "CQT", "BMF", "BMX",
#     "MTB", "CRD", "CTR", "EDR", "EVE", "EJP", "EVL", "EDV", "FEN", "HOC", "AFB", "FBL", "GLF", "GAR",
#     "GRY", "GTR", "HBL", "JUD", "KTE", "LAX", "MPN", "POL", "RQT", "ROC", "ROW", "RU7", "RUG", "SAL",
#     "SHO", "SKB", "CLB", "SQU", "SRF", "TTE", "TKW", "TEN", "TRI", "TOW", "VBV", "VVO", "PBT", "WLF",
#     "WRF", "WRG", "FSK", "IHO"
# ]
# target = 'Total'

# 2. 检查缺失值
df = df[features + [target]].dropna()

# 3. NOC列 Label Encoding
df['NOC'] = df['NOC'].astype(str).str.strip()
le = LabelEncoder()
df['NOC'] = le.fit_transform(df['NOC'])

# 4. 特征、标签
X = df.drop(columns=[target])
y = df[target]

# 5. 划分数据集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2,random_state=7)

# 6. XGBoost模型
model = XGBRegressor(
    n_estimators=1000,      # 树的数量
    max_depth=5,            # 树的最大深度
    learning_rate=0.02,     # 学习率
    random_state=7          # 保证结果可复现
)
model.fit(X_train, y_train)

# 7. 预测与评估
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mse)
mape = np.mean(np.abs((y_test - y_pred) / (y_test + 1e-8))) * 100  # + 1e-8防止分母为0出错
print("测试集均方误差 MSE:", mse)
print("测试集R2分数:", r2)
print("测试集平均绝对误差 MAE:", mae)
print("测试集均方根误差 RMSE:", rmse)
print("测试集平均绝对百分比误差 MAPE: {:.2f}%".format(mape))

# 8. 全部预测，并写入新表格
df['Pred_Total'] = model.predict(X)   # 用全量特征生成对应预测
df['NOC'] = le.inverse_transform(df['NOC'])

save_path = r'C:\Users\cyz13\PycharmProjects\AI_ClassProject\src\Total_Prediction\Total_XGBoost_Prediction_Data_with_Pred.xlsx'
df.to_excel(save_path, index=False)
print(f"预测结果已写入：{save_path}")

# 9. 特征重要性查看
importances = model.feature_importances_
indices = np.argsort(importances)[::-1]
feature_names = X.columns

plt.figure(figsize=(10, 6))
plt.title("Feature Importances")
plt.bar(range(len(importances)), importances[indices], align="center")
plt.xticks(range(len(importances)), feature_names[indices], rotation=90)
plt.tight_layout()
plt.show()

# %%

# ============== SHAP分析部分 ==================

# 1. 创建Explainer对象
explainer = shap.Explainer(model, X_train, feature_perturbation="interventional")

# 2. 计算测试集的SHAP值
shap_values = explainer(X_test)

# 3. SHAP summary plot（全局特征贡献）
plt.figure()
shap.summary_plot(shap_values, X_test, show=True)

# 4. 保存summary plot为图片
shap.summary_plot(shap_values, X_test, show=False)
plt.savefig(r'C:\Users\cyz13\PycharmProjects\AI_ClassProject\src\Total_Prediction\shap_summary_plot.png', bbox_inches='tight')
plt.close()

# 5. SHAP条形图（平均绝对值）
plt.figure()
shap.plots.bar(shap_values, show=True)
shap.plots.bar(shap_values, show=False)
plt.savefig(r'C:\Users\cyz13\PycharmProjects\AI_ClassProject\src\Total_Prediction\shap_bar_plot.png', bbox_inches='tight')
plt.close()

# %%

# ========= 生成2028年预测表格并预测 =============
#
# # 1. 取2024年每个国家的最新一行
# df_raw = pd.read_excel(file_path)
# df_raw['Year'] = df_raw['Year'].astype(int)
# df_2024 = df_raw[df_raw['Year'] == 2024].copy()
#
# # 2. 按要求生成2028年预测表格
# df_2028 = df_2024.copy()
# df_2028['Year'] = 2028
# df_2028['Cnt'] = 34
# df_2028['Host'] = 0
# df_2028['NOC'] = df_2028['NOC'].astype(str).str.strip()
# df_2028.loc[df_2028['NOC'] == 'United States', 'Host'] = 1
#
# # 3. 只保留训练集中见过的国家
# valid_noc = set(le.classes_)
# df_2028 = df_2028[df_2028['NOC'].isin(valid_noc)].copy()
#
# # 4. NOC列重新LabelEncoder（用已有le即可）
# df_2028['NOC'] = le.transform(df_2028['NOC'])
#
# # 5. 仅保留预测需要的特征
# X_2028 = df_2028[features]
#
# # 6. 预测
# df_2028['Pred_Total'] = model.predict(X_2028)
#
# # 7. 删除Gold/Silver/Bronze列
# for col in ['Total','Gold', 'Silver', 'Bronze']:
#     if col in df_2028.columns:
#         df_2028.drop(columns=col, inplace=True)
#
# # 8. 按预测结果排序并加Rank
# df_2028 = df_2028.sort_values(by='Pred_Total', ascending=False).reset_index(drop=True)
# df_2028['Rank'] = df_2028.index + 1
#
# # 9. NOC列还原为国家名
# df_2028['NOC'] = le.inverse_transform(df_2028['NOC'])
#
# # 10. Pred_Total四舍五入取整
# df_2028['Pred_Total'] = df_2028['Pred_Total'].round().astype(int)
#
# # 11. 保存
# save_2028 = r'C:\Users\cyz13\PycharmProjects\AI_ClassProject\src\Total_Prediction\Total_2028_XGBoost_Prediction.xlsx'
# df_2028.to_excel(save_2028, index=False)
# print(f"2028年预测结果已写入：{save_2028}")

# 1. 取2024年每个国家的最新一行
df_raw = pd.read_excel(file_path)
df_raw['Year'] = df_raw['Year'].astype(int)
df_2024 = df_raw[df_raw['Year'] == 2024].copy()

# 2. 用2024年金银铜重新计算ATP（注意：Cnt为2028年设定的34）
if all(col in df_2024.columns for col in ['Gold', 'Silver', 'Bronze']):
    atp_2028 = (df_2024['Gold'] * 5 + df_2024['Silver'] * 3 + df_2024['Bronze'] * 1) / 9
    df_2024['ATP'] = atp_2028

# 3. 按要求生成2028年预测表格
df_2028 = df_2024.copy()
df_2028['Year'] = 2028
df_2028['Cnt'] = 34
df_2028['Host'] = 0
df_2028['NOC'] = df_2028['NOC'].astype(str).str.strip()
df_2028.loc[df_2028['NOC'] == 'United States', 'Host'] = 1

# 4. 只保留训练集中见过的国家
valid_noc = set(le.classes_)
df_2028 = df_2028[df_2028['NOC'].isin(valid_noc)].copy()

# 5. NOC列重新LabelEncoder（用已有le即可）
df_2028['NOC'] = le.transform(df_2028['NOC'])

# 6. 仅保留预测需要的特征
X_2028 = df_2028[features]

# 7. 预测
df_2028['Pred_Total'] = model.predict(X_2028)

# 8. 删除Total/Gold/Silver/Bronze列
for col in ['Total', 'Gold', 'Silver', 'Bronze']:
    if col in df_2028.columns:
        df_2028.drop(columns=col, inplace=True)

# 9. 按预测结果排序并加Rank
df_2028 = df_2028.sort_values(by='Pred_Total', ascending=False).reset_index(drop=True)
df_2028['Rank'] = df_2028.index + 1

# 10. NOC列还原为国家名
df_2028['NOC'] = le.inverse_transform(df_2028['NOC'])

# 11. Pred_Total四舍五入取整
df_2028['Pred_Total'] = df_2028['Pred_Total'].round().astype(int)

# 12. 保存
save_2028 = r'C:\Users\cyz13\PycharmProjects\AI_ClassProject\src\Total_Prediction\Total_2028_XGBoost_Prediction.xlsx'
df_2028.to_excel(save_2028, index=False)
print(f"2028年预测结果已写入：{save_2028}")

