import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import LabelEncoder
import shap

# =============== XGBoost部分 ==================

# 1. 读取数据（筛选后）
file_path = r'C:\Users\cyz13\PycharmProjects\AI_ClassProject\src\Gold_Prediction\Gold_Prediction_Data.xlsx'
df = pd.read_excel(file_path)

features = [
    "NOC", "ATP", "Cnt", "Host", "SWM", "ATH", "BKB", "BOX", "CSP", "EDR", "EVE", "EVL",
    "FEN", "HOC", "GAR", "HBL", "MPN", "POL", "ROW", "RUG", "TOW", "VVO", "WLF", "WRF",
    "WRG", "FSK", "IHO"
]
target = 'Gold'

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
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=7)

# 6. XGBoost模型
model = XGBRegressor(
    n_estimators=1000,
    max_depth=5,
    learning_rate=0.02,
    random_state=7
)
model.fit(X_train, y_train)

# 7. 预测与评估
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print("测试集均方误差 MSE:", mse)
print("测试集R2分数:", r2)

# 8. 全部预测，并写入新表格
df['Pred_Gold'] = model.predict(X)
df['NOC'] = le.inverse_transform(df['NOC'])

save_path = r'C:\Users\cyz13\PycharmProjects\AI_ClassProject\src\Gold_Prediction\Gold_XGBoost_Prediction_Data_with_Pred.xlsx'
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

# ============== SHAP分析部分 ==================

explainer = shap.Explainer(model, X_train, feature_perturbation="interventional")
shap_values = explainer(X_test)

plt.figure()
shap.summary_plot(shap_values, X_test, show=True)
shap.summary_plot(shap_values, X_test, show=False)
plt.savefig(r'C:\Users\cyz13\PycharmProjects\AI_ClassProject\src\Gold_Prediction\shap_summary_plot_gold.png', bbox_inches='tight')
plt.close()

plt.figure()
shap.plots.bar(shap_values, show=True)
shap.plots.bar(shap_values, show=False)
plt.savefig(r'C:\Users\cyz13\PycharmProjects\AI_ClassProject\src\Gold_Prediction\shap_bar_plot_gold.png', bbox_inches='tight')
plt.close()

# ========= 生成2028年预测表格并预测 =============

df_raw = pd.read_excel(file_path)
df_raw['Year'] = df_raw['Year'].astype(int)
df_2024 = df_raw[df_raw['Year'] == 2024].copy()

df_2028 = df_2024.copy()
df_2028['Year'] = 2028
df_2028['Cnt'] = 34
df_2028['Host'] = 0
df_2028['NOC'] = df_2028['NOC'].astype(str).str.strip()
df_2028.loc[df_2028['NOC'] == 'United States', 'Host'] = 1

valid_noc = set(le.classes_)
df_2028 = df_2028[df_2028['NOC'].isin(valid_noc)].copy()
df_2028['NOC'] = le.transform(df_2028['NOC'])

X_2028 = df_2028[features]
df_2028['Pred_Gold'] = model.predict(X_2028)

# 删除Total/Silver/Bronze列
for col in ['Total', 'Silver', 'Bronze']:
    if col in df_2028.columns:
        df_2028.drop(columns=col, inplace=True)

df_2028 = df_2028.sort_values(by='Pred_Gold', ascending=False).reset_index(drop=True)
df_2028['Rank'] = df_2028.index + 1
df_2028['NOC'] = le.inverse_transform(df_2028['NOC'])
df_2028['Pred_Gold'] = df_2028['Pred_Gold'].round().astype(int)

save_2028 = r'C:\Users\cyz13\PycharmProjects\AI_ClassProject\src\Gold_Prediction\Gold_2028_XGBoost_Prediction.xlsx'
df_2028.to_excel(save_2028, index=False)
print(f"2028年预测结果已写入：{save_2028}")
