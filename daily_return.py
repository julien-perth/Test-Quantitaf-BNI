import numpy as np

def f_calculated_aggrageted_returns(df_weigths,df_returns,fees_ratio,adjustment_method):

    dfs_returns = f_filter_df_date(df_returns,df_weigths["Date"],"Date")
    total_weigth = np.asarray([df_weigths.iloc[i, 1:].sum() for i in range(len(df_weigths))]) # on calcule le poids total du portefeuille pour valider s'il utilise du levier

    arr_date = np.array([],dtype="datetime64[ns]")
    arrs_r=[]
    arrs_w = []

    weigth_adj_return = []
    new_sum_of_weigth = []
    eod_new_weigth = []

    daily_fees = np.array([])
    daily_return = np.array([])

    for i in range (len(dfs_returns)):
        arr_date = np.hstack((arr_date,dfs_returns[f"df{i}"].iloc[:,0]))
        arrs_r.append(np.array(dfs_returns[f"df{i}"].iloc[:,1:]))
        arrs_w.append(np.zeros((arrs_r[i].shape[0],arrs_r[i].shape[1])))

        if adjustment_method == "daily": ## hypothèse que les poids sont constants entre chaque target dates
            for j in range(len(arrs_w[i])):
                arrs_w[i][j,:] = np.array(df_weigths.iloc[i,1:])
        else: ## on laisse les poids "drift" entre les target dates
            arrs_w[i][:, :] = calc_difted_weigths(arrs_r[i],np.array(df_weigths.iloc[i,1:]))

        weigth_adj_return.append(f_calc_adjusted_weigth(arrs_w[i], arrs_r[i]))
        new_sum_of_weigth.append(f_calc_new_sum_of_weigth(weigth_adj_return[i]))

        # Calcule les nouveaux poids en fin de journée sachant les rendements de la journée et le poids constant
        eod_new_weigth.append(f_eod_new_weigths(weigth_adj_return[i], new_sum_of_weigth[i])*total_weigth[i])

        # Calcule du frais en % du rebalancement journalier sachant le nouveau poids calculé à la ligne ci-haut
        daily_fees = np.hstack((daily_fees, f_calc_daily_fees(arrs_w[i], eod_new_weigth[i], fees_ratio)))

        daily_return = np.hstack((daily_return,f_calc_daily_returns(arrs_w[i],arrs_r[i])))

    if adjustment_method != "daily": ### on recalcule les frais de transactions sachant qu'on rebalance seulement au traget dates
        daily_fees = f_recalc_fees(df_weigths, arr_date,daily_fees,eod_new_weigth,fees_ratio)

    total_return = daily_return-daily_fees

    return arr_date,daily_return,daily_fees,total_return


def f_recalc_fees(df_weigths,arr_date,daily_fees,eod_new_weigth,fees_ratio):

    target_dates = df_weigths["Date"]
    index_for_fees = []

    for i in range(len(target_dates)):
        index_for_fees.append(np.where(arr_date >= target_dates[i])[0][-1]) # trouve les indices de dates où le portfeuille doit être rebalancé

    index_for_fees = index_for_fees[:-1] # on ne rebalance pas la première date puisque ce sont les poids du premier


    for i in range(len(index_for_fees)):
        if i > 0 : #puisque les rendements sont séparés en section de target dates, il faut trouver l'index à utiliser pour le eod_new_weigth
            index_tu_use = index_for_fees[i]-index_for_fees[i-1]-1
        else :
            index_tu_use =index_for_fees[i]

        daily_fees[index_for_fees[i]] = f_calc_daily_fees (np.array(df_weigths.iloc[i,1:]),eod_new_weigth[i][index_tu_use,:],fees_ratio)

    final_daily_fees = np.zeros(len(daily_fees))

    for i in range(len(final_daily_fees)):
        for j in range (len(index_for_fees)):
            if i == index_for_fees[j]:
                final_daily_fees[i] = daily_fees[index_for_fees[j]]
                break
            else:
                final_daily_fees[i] = 0
    return final_daily_fees



def calc_difted_weigths(arr_r,arr_w):
    arr_r = np.flipud(arr_r)

    compounded_returns = np.zeros((arr_r.shape[0],arr_r.shape[1]))
    for i in range(arr_r.shape[1]):
        compounded_returns[:,i] = (1+arr_r[:,i]).cumprod()

    return arr_w*compounded_returns


def f_filter_df_date(df,criteria,col_to_filer):
    dfs = {}
    dfs[f"df{0}"] = df[(df[col_to_filer] >= criteria[0])]
    for i in range(1,len(criteria)):
        dfs[f"df{i}"] = df[(df[col_to_filer] >= criteria[i]) & (df[col_to_filer] < criteria[i-1])]
    return dfs


def f_calc_adjusted_weigth (arr_w,arr_r):
    return arr_w * (1 + arr_r)

def f_calc_new_sum_of_weigth (weigth_adj_return):
    return weigth_adj_return.sum(axis=1)

def f_eod_new_weigths (weigth_adj_return,new_sum_of_weigth):
    return (weigth_adj_return / np.asarray([new_sum_of_weigth for _ in range(len(weigth_adj_return))]).transpose()[:, :weigth_adj_return.shape[1]])

def f_calc_daily_fees (arr_w,eod_new_weigth,fees_ratio):
    deviation_to_target = eod_new_weigth - arr_w

    if deviation_to_target.ndim>1:
        return (abs(deviation_to_target)*fees_ratio).sum(axis=1)
    else:
        return (abs(deviation_to_target) * fees_ratio).sum()

def f_calc_daily_returns (arr_w,arr_r):
    return (arr_w*arr_r).sum(axis=1)





