import pandas as pd

def create_final_df(dict_arrs,used_sheets):
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