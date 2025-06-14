import pandas as pd

# 读取原始表格
input_path = r'C:\Users\cyz13\PycharmProjects\AI_ClassProject\src\ATP_processing\summerOly_medal_counts_ATP.xlsx'
df = pd.read_excel(input_path)

# 要保留的数据列
main_cols = ["Rank", "NOC", "Gold", "Silver", "Bronze", "Total", "Year", "ATP", "Cnt", "Host"]
feature_cols = ["BOX", "CSP", "EDR", "EVL", "GAR", "MPN", "POL", "RUG", "SHO", "TEN", "TOW", "VVO", "WRG", "FSK", "IHO"]
all_cols = main_cols + feature_cols

# 只保留需要的列
df_selected = df.loc[:, [col for col in all_cols if col in df.columns]]

# 保存到新文件
output_path = r'C:\Users\cyz13\PycharmProjects\AI_ClassProject\src\Total_Prediction\Total_Prediction_Data.xlsx'
df_selected.to_excel(output_path, index=False)

print("筛选并保存完成！")
