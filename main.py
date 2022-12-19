import pandas as pd
from utilities import config
from load_data import f_load_data
from datetime import datetime
from daily_return import f_calculated_aggrageted_returns
from index_series import f_construct_index_series
from data_formating import create_final_df
from data_formating import create_final_df_tranpose

start = datetime.now()
weigths = {}
returns = {}
port_daily_returns ={}
port_index_series ={}

## Utilisez ces dates pour le filtre lors de la création des index en base 100
lower_date = "1999-01-04"
upper_date = "2024-06-30"

## Exécution des calculs demandés
for i in range(0,config.number_of_portfolios):
    weigths[f"weigths_port{i}"] = f_load_data(config.path,config.used_sheets[i])
    returns[f"returns_port{i}"] = f_load_data(config.path,config.used_sheets[4],config.columns_match,weigths[f"weigths_port{i}"].columns)

    port_daily_returns[i] = f_calculated_aggrageted_returns(weigths[f"weigths_port{i}"],returns[f"returns_port{i}"],config.fees_ratio,config.rebanlancing_method[i])
    port_index_series[i] = f_construct_index_series(lower_date, upper_date, weigths[f"weigths_port{i}"], returns[f"returns_port{i}"],config.rebanlancing_method[i])

### Préparation de la donnée en dataframe en export
final_dfs ={}
dfs=create_final_df(port_index_series,config.used_sheets,config.name)
for i in range(len(dfs)):
    final_dfs[i] = dfs[i][i]
    for j in range(1, len(dfs[i])):
        if i == 1 :
            j=j+1
        final_dfs[i] = pd.concat([final_dfs[i], dfs[i][j]])
    final_dfs[i].reset_index(drop=True, inplace=True)

final_dfs[len(dfs)] = create_final_df_tranpose(port_daily_returns, config.used_sheets)
final_dfs[len(dfs)].reset_index(drop=True, inplace=True)
dict_portfolio_index[i].set_axis(["Date", "Gross Returns", "Fees", "Total Returns", "Portfolio"], axis='columns', inplace=True)

### Export en CSV
order = [3, 1, 2]
for i in range(len(final_dfs)):
    final_dfs[order[i]].to_csv("./"+config.file_name[i])

end = datetime.now()-start



