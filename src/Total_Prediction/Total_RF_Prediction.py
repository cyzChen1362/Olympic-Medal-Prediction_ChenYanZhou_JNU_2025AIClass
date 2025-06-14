import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.metrics import mean_absolute_error
from sklearn.preprocessing import LabelEncoder

# %%

# ================== RF部分 ====================

# 1. 读取数据
file_path = r'C:\Users\cyz13\PycharmProjects\AI_ClassProject\src\Total_Prediction\Total_Prediction_Data.xlsx'
df = pd.read_excel(file_path)

features = [
    'NOC', 'Host', 'ATP', 'Cnt', 'BOX', 'CSP', 'EDR',
    'EVL', 'GAR', 'MPN', 'POL', 'RUG', 'SHO', 'TEN',
    'TOW', 'VVO', 'WRG', 'FSK', 'IHO'
]
target = 'Total'

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

# 6. 随机森林模型
model = RandomForestRegressor(
    n_estimators=1000,  # 树的数量
    max_depth=5,        # 树的最大深度
    random_state=7      # 保证结果可复现
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
df['Pred_Total'] = model.predict(X)
save_path = r'C:\Users\cyz13\PycharmProjects\AI_ClassProject\src\Total_Prediction\Total_RF_Prediction_Data_with_Pred.xlsx'
df.to_excel(save_path, index=False)
print(f"预测结果已写入：{save_path}")

# 9. 特征重要性查看
importances = model.feature_importances_
indices = np.argsort(importances)[::-1]
feature_names = X.columns

plt.figure(figsize=(10, 6))
plt.title("Feature Importances (Random Forest)")
plt.bar(range(len(importances)), importances[indices], align="center")
plt.xticks(range(len(importances)), feature_names[indices], rotation=90)
plt.tight_layout()
plt.show()
