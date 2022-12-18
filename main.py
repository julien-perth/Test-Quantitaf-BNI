from utilities import config
from load_data import f_load_data
from datetime import datetime
from daily_return import f_calculated_aggrageted_returns
from index_series import f_construct_index_series
from data_formating import create_final_df

start = datetime.now()

weigths = {}
returns = {}
port_daily_returns ={}
port_index_series ={}

lower_date = "1999-01-04"
upper_date = "2024-06-30"

for i in range(0,config.number_of_portfolios):
    weigths[f"weigths_port{i}"] = f_load_data(config.path,config.used_sheets[i])
    returns[f"returns_port{i}"] = f_load_data(config.path,config.used_sheets[4],config.columns_match,weigths[f"weigths_port{i}"].columns)

    port_daily_returns[i] = f_calculated_aggrageted_returns(weigths[f"weigths_port{i}"],returns[f"returns_port{i}"],config.fees_ratio,config.rebanlancing_method[i])
    port_index_series[i] = f_construct_index_series(lower_date, upper_date, weigths[f"weigths_port{i}"], returns[f"returns_port{i}"],config.rebanlancing_method[i])


performance_series = {}
for i in range(1,len(port_index_series)):
    performance_series[i-1] = port_index_series[i-1]-port_index_series[i]


to_export = [port_daily_returns,port_index_series,performance_series]
final_dfs ={}
for i in range(len(to_export)):
    if i != len(to_export)-1:
        final_dfs[i]=create_final_df(to_export[i], config.used_sheets)
    else:
        final_dfs[i]=create_final_df(to_export[i], config.name)
    if i ==0:
        final_dfs[i].set_axis(["Date","gross_returns", 'fees', 'total_returns','Portfolio'], axis='columns', inplace=True)

    final_dfs[i].to_csv("./"+config.file_name[i])

end = datetime.now()-start


