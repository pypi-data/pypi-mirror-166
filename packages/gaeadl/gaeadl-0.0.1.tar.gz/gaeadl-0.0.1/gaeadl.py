# by he pengfei 2022/9/10
import pandas as pd


# One-hot encoding
def one_hot(df, cols):
    """
    @param df pandas DataFrame
    @param cols a list of columns to encode
    @return a DataFrame with one-hot encoding
    """
    for each in cols:
        dummies = pd.get_dummies(df[each], prefix=each, drop_first=False)
        df = pd.concat([df, dummies], axis=1)
        df = df.drop(each, 1)
    return df


# 对df中非数值类型进行映射特征编码
def map_encoding(df, cols):
    new_df = df.copy()
    col_dicts = {}
    for each_col in cols:
        data = new_df.drop_duplicates(subset=[each_col], keep='first', inplace=False)
        col_value = data[each_col].values
        tmp = {}
        count = 1
        for k in col_value:
            tmp[k] = count
            count += 1
        col_dicts[each_col] = tmp
        new_df[each_col] = new_df[each_col].map(col_dicts[each_col])
    return new_df


## 归一化
# Function to min-max normalize 改进：对train test分别进行归一化 保证均值方差等参数一致 https://zhuanlan.zhihu.com/p/76682561?ivk_sa=1024320u
# https://blog.csdn.net/m0_47478595/article/details/106402843?spm=1001.2101.3001.6661.1&utm_medium=distribute.pc_relevant_t0.none-task-blog-2%7Edefault%7ECTRLIST%7ERate-1-106402843-blog-112556315.pc_relevant_multi_platform_whitelistv4&depth_1-utm_source=distribute.pc_relevant_t0.none-task-blog-2%7Edefault%7ECTRLIST%7ERate-1-106402843-blog-112556315.pc_relevant_multi_platform_whitelistv4&utm_relevant_index=1
def normalize(df, cols):
    """
    @param df pandas DataFrame
    @param cols a list of columns to encode
    @return a DataFrame with normalized specified features
    """
    result = df.copy()  # do not touch the original df
    for feature_name in cols:
        max_value = df[feature_name].max()
        min_value = df[feature_name].min()
        if max_value > min_value:
            result[feature_name] = (df[feature_name] - min_value) / (max_value - min_value)
    return result


## 过抽烟 数据平衡