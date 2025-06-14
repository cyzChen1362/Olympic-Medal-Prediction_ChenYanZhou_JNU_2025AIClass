import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import LabelEncoder, StandardScaler

# 1. 读取数据
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

# 5. 标准化特征（神经网络推荐）
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 6. 划分数据集
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=7)

# 7. BP神经网络模型（MLPRegressor）
model = MLPRegressor(
    hidden_layer_sizes=(64, 32),   # 两层隐藏层
    activation='relu',
    solver='adam',
    learning_rate='adaptive',
    max_iter=1000,
    random_state=7
)
model.fit(X_train, y_train)

# 8. 预测与评估
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print("测试集均方误差 MSE:", mse)
print("测试集R2分数:", r2)

# 9. 全部预测，并写入新表格
df['Pred_Gold'] = model.predict(scaler.transform(X))
save_path = r'C:\Users\cyz13\PycharmProjects\AI_ClassProject\src\Gold_Prediction\Gold_BP_Prediction_Data_with_Pred.xlsx'
df.to_excel(save_path, index=False)
print(f"预测结果已写入：{save_path}")
