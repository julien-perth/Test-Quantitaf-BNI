import pandas as pd
import datetime


def f_load_data(path,sheet_name,columns_match="None",col_to_keep="None"):

    df = pd.read_excel(path, sheet_name=sheet_name)
    df.columns = f_define_header(df)
    id_to_start = f_find_line_to_index(df)+1
    df = df[id_to_start:]

    if type(col_to_keep) != str or col_to_keep != "None":
        final_cols_to_keep = []
        final_cols_to_keep.append("Date")
        for i in range(len(col_to_keep)):
            for j in range(len(columns_match[0])):
                if col_to_keep[i] == columns_match[0][j]:
                    final_cols_to_keep.append(columns_match[1][j])
                    j = len(columns_match[0])
        df = df[df.columns[df.columns.isin(final_cols_to_keep)]]

    df.reset_index(drop=True, inplace=True)

    nan_data = f_chek_nan(df)
    if len(nan_data[1]) > 0:
        df = f_fill_nan(df, nan_data[1], nan_data[0])

    return df


def f_find_line_to_index(df):
    for i in range(df.shape[0]):
        if type(df.iloc[i,0])== pd._libs.tslibs.timestamps.Timestamp or type(df.iloc[i,0]) == datetime.datetime:
            return i-1


def f_define_header(df):
    cols = []
    cols_2 = list(df.iloc[f_find_line_to_index(df)])
    if cols_2[0] != "Date":
        cols.append("Date")
        start = 1
    else :
        start = 0

    for i in range(start,len(cols_2)):
        cols.append(cols_2[i])

    return cols

def f_chek_nan(df):
    indxs = {}
    col_with_nan = []
    for i in range(0, df.shape[1]):
        indxs[f"col{i}"] = df.loc[pd.isna(df.iloc[:, i]), :].index
        if len(indxs[f"col{i}"]) > 0:
            col_with_nan.append(i)
    return indxs, col_with_nan


def f_fill_nan (df, col_to_validate, dict_indxs):
    for i in range(len(col_to_validate)):
        df.iloc[dict_indxs[f"col{col_to_validate[i]}"], col_to_validate[i]] = df.iloc[:, col_to_validate[i]].mean()
    return df