import numpy as np
import pandas as pd
import glob
import scipy.stats as stats

def get_feature_pairs(df_with_grouped_intersections, name, bad):
    '''
    Search for combinations of parameters with low or high intersections

    Args:
        df_with_grouped_intersections: a pandas dataframe, a table obtained from get_intersections function,
                                       grouped by hospital case and parameters' combination
        name: a string, a hospital case (e.g. 'full df_1 in full df_2')
        bad: boolean, determines what parameters are needed - with low or high intersections
    Return:
        A pandas series with combinations of parameters
    '''
    data = df_with_grouped_intersections[df_with_grouped_intersections['Name']==name]

    #find the lowest limit for normal values - below are outliers
    q1,q3 = df_with_grouped_intersections[df_with_grouped_intersections["Name"]==name].Intersection.quantile([0.25, 0.75])
    low = q1 - 1.5*(q3-q1)
    if bad: #bad==true -> return bad pairs
        df = df_with_grouped_intersections[(df_with_grouped_intersections["Name"]==name) & (df_with_grouped_intersections['Intersection']<low)]
    else: #bad==false -> return good pairs
        df = df_with_grouped_intersections[(df_with_grouped_intersections["Name"]==name) & (df_with_grouped_intersections['Intersection']>=low)]

    return df.Parameters

def get_features_count_df(df_with_grouped_intersections, name, bad):
    '''
    Counts occurences of a parameter

    Args:
        df_with_grouped_intersections: a pandas dataframe, a table obtained from get_intersections function,
                                       grouped by hospital case and parameters' combination
        name: a string, a hospital case (e.g. 'full df_1 in full df_2')
        bad: boolean, determines what parameters are needed - with low or high intersections
    Return:
        df: a pandas dataframe, parameters and their count
    '''
    params = get_feature_pairs(df_with_grouped_intersections, name, bad)

    #clean string values, get only parameter names
    param_list=[]
    for x in params:
        a,b=x.split(", ",1)
        param_list.append(a)
        param_list.append(b)
    #count parameter appearance
    dct=dict(zip(param_list,[param_list.count(i) for i in param_list]))
    sorted_dct = dict(sorted(dct.items(), key=lambda item: item[1], reverse=True))
    if bad:
        df = pd.DataFrame(sorted_dct.items(), columns=['Parameter', f'Count_in_bad_pairs'])
    else:
        df = pd.DataFrame(sorted_dct.items(), columns=['Parameter', f'Count_in_good_pairs'])

    return df

def fishers_exact_test(df, name, param_count):
    '''
    Perform enrichment analysis

    Args:
        df: a pandas dataframe, a table obtained from get_intersections function,
            grouped by hospital case and parameters' combination
        name: a string, a hospital case (e.g. 'full df_1 in full df_2')
        param_count: int, total count of parameters common for both hospitals
    Return:
        df: a dataframe, with information about each parameter: count, p value, etc.
    '''
    param_count = param_count - 1
    #get bad pairs and their count
    bad_pairs = get_feature_pairs(df_with_grouped_intersections=df, name=name, bad=True)
    df_bad=get_features_count_df(df_with_grouped_intersections=df, name=name, bad=True)
    #get good pairs and their count
    good_pairs = get_feature_pairs(df_with_grouped_intersections=df, name=name, bad=False)
    df_good=get_features_count_df(df_with_grouped_intersections=df, name=name, bad=False)

    if len(bad_pairs)!=0:
        enrich_df= pd.merge(df_bad, df_good, how='outer', on='Parameter').fillna(0)

        #perform Fisher's exact test
        odds_list=[]
        pval_list=[]
        for i in enrich_df.index:
            v00=enrich_df.iloc[i,[1,2]][0] # count of a parameter presence in a bad list
            v10=enrich_df.iloc[i,[1,2]][1] # count of a parameter presence in a good list

            odds,pval=stats.fisher_exact([[v00,(len(bad_pairs)-v00)],[v10,(len(good_pairs)-v10)]])
            odds_list.append(odds)
            pval_list.append(pval)

        enrich_df['Name']=name
        enrich_df["Parameter_count"] = param_count #parameter count
        enrich_df["Ratio_in_bad_pairs"] = np.round(enrich_df["Count_in_bad_pairs"]/enrich_df["Parameter_count"], 2)
        enrich_df["odds_ratio"] = odds_list
        enrich_df['p_value'] = pval_list

        return enrich_df
    else: #there are no low intersections
        enrich_df = pd.DataFrame()
        return enrich_df



def produce_summary_tables_ch(path_to_ch_outputs, dataset_labels):
    '''
    Computes parameters with the lowest intersections, their count and the mean intersections for each datasets

    Args:
        path_to_ch_outputs: a string, a path to a folder containing the intersections of convex hull analysis
        dataset_labels: a list of strings, names of the datasets used in convex hull analysis computations
    Returns:
        mean_coverage_df: dataframe, mean intersection for a dataset
        bad_params_df: dataframe, names of parameters that cause the lowest intersections for a case
        bad_params_df_count: dataframe, count of parameters with the lowest intersections
    '''
    all_df = pd.DataFrame()
    files = glob.glob(path_to_ch_outputs)
    for file in files:
        ch_int = pd.read_csv(file, index_col=0)
        all_df = pd.concat([all_df,ch_int])

    all_df.Parameters = all_df.Parameters.str.replace(' ', '')
    all_df = all_df.reset_index()
    all_df = pd.merge(all_df, all_df.Parameters.str.split(',', 1, expand = True), left_index=True, right_index=True)

    ### get labels from datasets
    mean_coverage_df = pd.DataFrame(columns = dataset_labels, index = dataset_labels)
    bad_params_df_count = pd.DataFrame(columns = dataset_labels, index = dataset_labels)
    bad_params_df = pd.DataFrame(columns = dataset_labels, index = dataset_labels)


    ### for each case of dataset intersection (dataset 1 in 2 or vice versa, etc..)
    for case in all_df.Name.unique():

        ch_int = all_df[(all_df.Name == case)]
        params = set(ch_int[1].unique()).union(set(ch_int[0].unique()))

        cover_list = []
        for param in params:
            ### take median intersection for each of parameters for a particular case of dataset intersection
            cover_list.append(ch_int[ch_int.Parameters.str.contains(param)].Intersection.median())

        int_df = pd.DataFrame(cover_list, index = params, columns=["Intersection"])
        ### here choose bad parameters based on criterium - outliers on the boxplot
        chosen = int_df[int_df.Intersection<(int_df.quantile(0.25) - 1.5*(int_df.quantile(0.75) - int_df.quantile(0.25)))[0]]

        ### extract dataset names
        indexes = case.replace('full ','',2)
        indexes = indexes.replace('sampled ','').replace(' in ', ',')
        indexes = indexes.split(',')
        mean_coverage_df.loc[indexes[1], indexes[0]] = int_df.Intersection.mean()
        bad_params_df_count.loc[indexes[1], indexes[0]] = chosen.shape[0]
        bad_params_df.loc[indexes[1], indexes[0]] = ', '.join(list(chosen.index.to_series()))

    bad_params_df_count = bad_params_df_count.astype(float)
    mean_coverage_df = mean_coverage_df.astype(float)

    return mean_coverage_df, bad_params_df, bad_params_df_count
