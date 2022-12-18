from daily_return import f_filter_df_date
from daily_return import f_calc_adjusted_weigth
from daily_return import f_calc_new_sum_of_weigth
from daily_return import calc_difted_weigths
import numpy as np

def f_construct_index_series(lower_date,upper_date,df_weigths,df_returns,adjustment_method,base=100):

    df_returns = df_returns[(df_returns["Date"] >= lower_date) & (df_returns["Date"] <= upper_date)]
    dfs_returns = f_filter_df_date(df_returns, df_weigths["Date"], "Date")

    total_weigth = np.asarray([df_weigths.iloc[i,1:].sum() for i in range (len(df_weigths))])

    arrs_date = np.array([],dtype="datetime64[ns]")
    arrs_r = []
    arrs_w = []

    weigth_adj_return = []
    index = np.array([])

    for i in range (len(dfs_returns)):
        arrs_date = np.hstack((arrs_date,dfs_returns[f"df{i}"].iloc[:, 0]))
        arrs_r.append(np.array(dfs_returns[f"df{i}"].iloc[:,1:]))

        arrs_w.append(np.zeros((arrs_r[i].shape[0], arrs_r[i].shape[1])))
        if adjustment_method == "daily":
            for j in range(len(arrs_w[i])):
                arrs_w[i][j, :] = np.array(df_weigths.iloc[i, 1:])
        else:
            arrs_w[i][:, :] = calc_difted_weigths(arrs_r[i], np.array(df_weigths.iloc[i, 1:]))

        if adjustment_method == "daily":
            weigth_adj_return.append(f_calc_adjusted_weigth(arrs_w[i],arrs_r[i]))
        else :
            weigth_adj_return.append(arrs_w[i])

        index = np.hstack((index,f_calc_new_sum_of_weigth(weigth_adj_return[i])*base/total_weigth[i]))

    return arrs_date,index
