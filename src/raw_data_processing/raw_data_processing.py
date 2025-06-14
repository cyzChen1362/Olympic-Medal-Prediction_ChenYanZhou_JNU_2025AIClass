import pandas as pd

# 路径
medal_counts_path = r'C:\Users\cyz13\PycharmProjects\AI_ClassProject\src\raw_data_processing\summerOly_medal_counts.xlsx'
programs_path = r'C:\Users\cyz13\PycharmProjects\AI_ClassProject\src\raw_data_processing\summerOly_programs.xlsx'
df_medal = pd.read_excel(medal_counts_path)
df_prog = pd.read_excel(programs_path)

# 获取所有项目简称
code_cols = [col for col in df_prog['Code'].unique() if isinstance(col, str)]

# 1. 建立“年份字符串”与 programs 列名的映射
year_col_map = {}  # 例如 {'1896': '1896', '1900': '1900*', '1904': 1904}
for col in df_prog.columns:
    col_str = str(col).rstrip("*")
    if col_str.isdigit():
        year_col_map[col_str] = col

# 2. 生成 year_stat
year_stat = {}
for year_str, real_col in year_col_map.items():
    tmp = df_prog.copy()
    tmp[real_col] = pd.to_numeric(tmp[real_col], errors='coerce').fillna(0).astype(int)
    tmp_valid = tmp[tmp[real_col] > 0]
    total_sports = tmp_valid['Sport'].nunique()
    total_disciplines = tmp_valid['Discipline'].nunique()
    total_events = tmp_valid[real_col].sum()
    proj_dict = {code: 0 for code in code_cols}
    for _, row in tmp_valid.iterrows():
        proj_dict[row['Code']] = row[real_col]
    year_stat[year_str] = {
        'Total sports': total_sports,
        'Total disciplines': total_disciplines,
        'Total events': total_events,
        **proj_dict
    }

# 主办国字典
host_dict = {
    1896: "Greece",
    1900: "France",
    1904: "United States",
    1908: "United Kingdom",
    1912: "Sweden",
    1920: "Belgium",
    1924: "France",
    1928: "Netherlands",
    1932: "United States",
    1936: "Germany",
    1948: "United Kingdom",
    1952: "Finland",
    1956: "Australia",
    1960: "Italy",
    1964: "Japan",
    1968: "Mexico",
    1972: "Germany",
    1976: "Canada",
    1980: "Soviet Union",
    1984: "United States",
    1988: "Korea, South",
    1992: "Spain",
    1996: "United States",
    2000: "Australia",
    2004: "Greece",
    2008: "China",
    2012: "United Kingdom",
    2016: "Brazil",
    2020: "Japan",
    2024: "France",
}

records = []
for idx, row in df_medal.iterrows():
    year = int(row['Year'])
    year_str = str(year)
    noc = row['NOC']
    stat = year_stat.get(year_str, {})
    record = row.to_dict()
    record['Cnt'] = (year - 1896) // 4 + 1
    record['Host'] = 1 if str(noc).strip().lower() == str(host_dict.get(int(row['Year']), "")).strip().lower() else 0
    record['Total sports'] = stat.get('Total sports', 0)
    record['Total disciplines'] = stat.get('Total disciplines', 0)
    record['Total events'] = stat.get('Total events', 0)
    # 写入项目时，如果项目是缺失值，那么直接填0
    for code in code_cols:
        record[code] = stat.get(code, 0)
    records.append(record)

df_try_atp_new = pd.DataFrame(records)

# 补齐与目标表一致的列顺序
target_columns = [
    'Rank', 'NOC', 'Gold', 'Silver', 'Bronze', 'Total', 'Year', 'Cnt', 'Host',
    'Total sports', 'Total disciplines', 'Total events'
] + code_cols
df_try_atp_new = df_try_atp_new[target_columns]
df_try_atp_new.to_excel(r'C:\Users\cyz13\PycharmProjects\AI_ClassProject\src\raw_data_processing\summerOly_medal_counts_Try_ATP.xlsx', index=False)

# 生成 SpearmanData
spearman_columns = [
    'Gold', 'Silver', 'Bronze', 'Total', 'Host', 'Total sports', 'Total disciplines', 'Total events'
] + code_cols
df_spearman_new = df_try_atp_new[spearman_columns]

# 去除重复列
df_spearman_new = df_spearman_new.loc[:, ~df_spearman_new.columns.duplicated()]

df_spearman_new.to_excel(r'C:\Users\cyz13\PycharmProjects\AI_ClassProject\src\raw_data_processing\summerOly_medal_counts_SpearmanData.xlsx', index=False)
