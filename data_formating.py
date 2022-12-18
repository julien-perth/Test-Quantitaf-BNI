import pandas as pd

def create_final_df_tranpose(dict_arrs,used_sheets):
    full_data = pd.DataFrame(dict_arrs[0]).transpose()

    full_data["portfolio"] = used_sheets[0]

    for i in range(1,len(dict_arrs)):
        x=pd.DataFrame(dict_arrs[i]).transpose()
        if i !=len(dict_arrs)-1:
            x["portfolio"] = used_sheets[i]
        else:
            x["portfolio"] = used_sheets[i]+" "+"target_dates"

        full_data = pd.concat([full_data,x])
    return full_data


def create_final_df(port_index_series,used_sheets,name):
    performance_series = {}
    dict_portfolio_index = {}

    dict_portfolio_index[0] = pd.DataFrame(port_index_series[0]).transpose()
    dict_portfolio_index[0].set_axis(["Date", "index_value"], axis='columns', inplace=True)
    dict_portfolio_index[0]["portfolio"] = used_sheets[0]

    for i in range(1, len(port_index_series)):
        dict_portfolio_index[i] = pd.DataFrame(port_index_series[i]).transpose()
        dict_portfolio_index[i].set_axis(["Date", "index_value"], axis='columns', inplace=True)

        if i == len(port_index_series) - 1:
            dict_portfolio_index[i]["portfolio"] = used_sheets[i] + " " + "target_dates"
        else:
            dict_portfolio_index[i]["portfolio"] = used_sheets[i]

        performance_series[i] = pd.DataFrame(dict_portfolio_index[i - 1].iloc[:, 1] - dict_portfolio_index[i].iloc[:, 1])
        performance_series[i].insert(loc=0, column="Date", value=dict_portfolio_index[i - 1].iloc[:, 0])
        performance_series[i]["portfolio"] = name[i - 1]

    return dict_portfolio_index, performance_series
