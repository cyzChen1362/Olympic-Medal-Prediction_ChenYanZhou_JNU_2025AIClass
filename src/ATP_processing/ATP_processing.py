import pandas as pd

# 读取原始Excel文件
file_path = r'..\raw_data_processing\summerOly_medal_counts_Try_ATP.xlsx'
df = pd.read_excel(file_path)

# 去除NOC列前后空格
df['NOC'] = df['NOC'].astype(str).str.strip()

# 排序
df = df.sort_values(['NOC', 'Year'])

# 计算上一届奖牌数
df['Gold_last'] = df.groupby('NOC')['Gold'].shift(1)
df['Silver_last'] = df.groupby('NOC')['Silver'].shift(1)
df['Bronze_last'] = df.groupby('NOC')['Bronze'].shift(1)

# 按公式计算ATP
df['ATP'] = (df['Gold_last'] * 5 + df['Silver_last'] * 3 + df['Bronze_last'] * 1) / 9

# 删除临时列
df = df.drop(columns=['Gold_last', 'Silver_last', 'Bronze_last'])

# 取出ATP列
atp = df.pop('ATP')

# 获取Year的列索引
year_idx = df.columns.get_loc('Year')

# Year后面插入ATP（即year_idx+1的位置）
df.insert(year_idx + 1, 'ATP', atp)

# 先Year升序，再Rank升序
df = df.sort_values(['Year', 'Rank']).reset_index(drop=True)

# 保存到新文件：
df.to_excel(r'..\ATP_processing\summerOly_medal_counts_ATP.xlsx', index=False)