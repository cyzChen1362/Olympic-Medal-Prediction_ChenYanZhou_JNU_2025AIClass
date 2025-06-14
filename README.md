# 🏅 奥运奖牌预测项目 | Olympic Medal Prediction

本项目基于 Python 实现，通过多种机器学习方法（XGBoost、BP神经网络、随机森林）对历届奥运会奖牌数据进行分析与预测，并使用 SHAP 方法提升模型可解释性。最终预测 2028 年奥运会的奖牌分布。

📌 本项目为暨南大学《人工智能》课程结课项目。

## 📁 项目结构

src/

├── raw_data_processing/         # 原始数据预处理

├── OlyEvent_Missing_Value/      # 缺失值处理与可视化

├── Spearman_processing/         # 特征相关性筛选

├── ATP_processing/              # 计算ATP特征

├── Total_Prediction/            # 奖牌总数 Total 的预测分析
 
└──  Gold_Prediction/            # 金牌数 Gold 的预测分析

## 📦 **环境配置与依赖**

### ✅ Python 环境

Python ≥ 3.9

### ✅ 核心依赖包版本

库名	版本

numpy	1.26.4

pandas	2.3.0

matplotlib	3.9.4

seaborn	0.13.2

scipy	1.13.1

xgboost	2.1.4

shap	0.48.0

scikit-learn	1.6.1

openpyxl	≥3.1

🔧 注：os, sys, ast, importlib 是 Python 内置模块，不需单独安装。

## 📊 数据准备

### ✅ 项目使用以下两份 Excel 数据源：

🔧 注：已包含于 raw_data_processing/ 文件夹

summerOly_medal_counts.xlsx：奖牌分布数据

summerOly_programs.xlsx：参赛项目分布数据

### ✅ 通过 raw_data_processing.py 统一处理并生成以下中间数据：


summerOly_medal_counts_Try_ATP.xlsx：用于添加 ATP 特征

summerOly_medal_counts_SpearmanData.xlsx：用于 Spearman 分析

summerOly_medal_counts_ATP.xlsx：最终用于建模

## 🚀 **快速开始**

以下为推荐运行顺序，可复现实验结果：

🔧 注：以下所有程序中的路径名都需要手动替换。

### ✅ 原始数据处理： 

raw_data_processing/raw_data_processing.py

### ✅ 缺失值热力图生成： 

OlyEvent_Missing_Value/Missing_Value_Event.py

### ✅ Spearman相关性分析与特征筛选： 

Spearman_processing/Spearman.py

Total_Prediction/Total_Features_Select.py

Gold_Prediction/Gold_Features_Select.py

### ✅ ATP特征添加：

ATP_processing/ATP_processing.py

### ✅ 建模与预测（以Total为例）：

Total_Prediction/Total_XGBoost_Prediction.py

Total_Prediction/Total_BP_Prediction.py

Total_Prediction/Total_RF_Prediction.py

### ✅ 对比残差与置信区间图：

Total_Prediction/CI_Width_Comparison.py

Total_Prediction/Total_Residuals_Comparison.py

### ✅ SHAP可解释性分析（在XGBoost预测脚本中已集成）

Total_Prediction/Total_XGBoost_Prediction.py

### ✅ Gold预测（与Total流程一致，用作验证）

Gold_Prediction/Gold_XGBoost_Prediction.py

Gold_Prediction/Gold_BP_Prediction.py

Gold_Prediction/Gold_RF_Prediction.py

### ✅ 对2028年奥运会进行预测（在XGBoost预测脚本中已集成）

Total_Prediction/Total_XGBoost_Prediction.py

