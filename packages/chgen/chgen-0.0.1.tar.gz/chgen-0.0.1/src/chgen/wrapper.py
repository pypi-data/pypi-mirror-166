import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn import svm
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.metrics import precision_recall_fscore_support, roc_auc_score
from sklearn.inspection import permutation_importance
import logging
logging.basicConfig(filename='log.txt',level=logging.INFO)

from chgen.functions import run_dbscan, get_intersections, full_intersections, get_correlated, run_classifier, find_features

def find_loss(combo, df, df_name, eps = 0.5, min_samples = 4, not_noise = 0.9):
    '''
    Wrapper function to detect outliers using DBSCAN

    Args:
        combo: a list, pair of parameters of interest
        df: dataframe with values
        df_name: string, name of a dataframe to process
        eps: float, a DBSCAN parameter to define a neighborhood of a point
        min_samples: int, minimal number of points in the neighborhood of a point
        not_noise: float, minimal (relative) amount of instances of a dataframe to be considered as a cluster
    Return:
        bools: a boolean list, True - a point belongs to a cluster, False - an outlier
        combo: string, pair of parameters of interest
        pat_loss: int, number of points considered as an outlier
        eps: float, end value for eps-parameter
        smpl: int, end value for min_samples-parameter
    '''
    points = df.loc[:,combo]
    points = np.array(points)

    bools, eps, smpl = run_dbscan(points = points, xy = combo, df_name = df_name, eps = eps, min_samples = min_samples, not_noise = not_noise)

    #count patient loss
    pats=points[bools]
    pat_loss = df.shape[0]-len(pats)

    combo = ', '.join(combo)

    return bools, combo, pat_loss, eps, smpl

def compute_intersections(combo, df_1, df_2, df_names, bools_1 = [], bools_2 = [], first_fixed = None, size = []):
    '''
    Wrapper function to calculate intersections of two lists of points (with/without outliers) of the same dimension

    Args:
        combo: a list, a combination of parameters
        df_1: numpy array of points of one dataframe which size will be altered. Contains only parameters of interest
        df_2: numpy array of points of another dataframe which size remains the same. Contains only parameters of interest
        df_names: a list of strings, hospitals' names (e.g. ['df_1','df_2']), in the same order as to_boot and fixed arguments
        bools_1, bools_2: lists of boolean values, True - a point is in the cluster, False - a point is an outlier
        first_fixed: boolean, determines what dataframe (True = the first one or False = the second one) keeps its length,
                     if None - both datasets are taken at the full length
        size: a list of integers for resampling
    Returns:
        df: a pandas dataframe, a table with intersection values for a combination of parameters and dataframe cases
    '''

    try:
        points_1 = df_1.loc[:,combo]
        points_2 = df_2.loc[:,combo]
        points_1 = np.array(points_1)
        points_2 = np.array(points_2)

        if (len(bools_1)!=0) and (len(bools_2)!=0):
            #keep only clustered point (w/o outliers) for current combo
            points_1=points_1[bools_1]
            points_2=points_2[bools_2]

        if first_fixed == True:
            df = get_intersections(to_boot = points_2, fixed = points_1, size = size, df_names = df_names[::-1], pair = combo)
        elif first_fixed == False:
            df = get_intersections(to_boot = points_1, fixed = points_2, size = size, df_names = df_names, pair = combo)
        else: # default case - compute intersections with all datapoints
            df = full_intersections(df_1 = points_1, df_2 = points_2, df_names = df_names, pair = combo)
        return df

    except:
        logging.info(f'Problem: {combo}')
        df = pd.DataFrame()
        return df

def classify(df_1, df_2, target, df_name, corr_coef):
    '''
    Computes a report with the result of classification using four classifiers and two methods. A model tries to
    distinguish between two dataframes and find features that are the most important in that task.

    Args:
        df_1, df_2: pandas dataframes, dataframes of interest
        target: string, dependent feature
        df_name: name of a dataframes (in target variable) to be set at 1 in classification problem
        corr_coef: float, coefficient of acceptable correlation, if more, then one of the correlated features will be dropped
    Returns:
        result: a dataframe with the results of classifiaction
    '''

    #find common parameters for both dfs
    common_params = sorted(list(set(df_1.columns).intersection(df_2.columns)))
    logging.info(f'Number of common parameters: {len(common_params)}')
    logging.info(f'Common parameters: {common_params}')

    #keep only checked common >70% pat parameters
    df_1 = df_1[common_params]
    df_2 = df_2[common_params]

    df = pd.concat([df_1,df_2])

    correlated = get_correlated(df.drop(columns = [target]), corr_coef)
    df.drop(columns=correlated, inplace=True)

    all_features = df.drop(columns=[target]).copy()
    label=df[target]
    # split df
    X_train, X_test, y_train, y_test = train_test_split(all_features, label, test_size = 0.2, stratify=label)
    logging.info(" Shapes: " + str(X_train.shape) +" "+ str(y_train.shape)+ " " + str(X_test.shape)+ " "+ str(y_test.shape))

    #scale features
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)


    df_train = pd.DataFrame(X_train, columns=all_features.columns)
    df_test = pd.DataFrame(X_test, columns=all_features.columns)

    logging.info(" Unique values: " + "df_train: " +" "+ str(y_train.value_counts())+ " " + " df_test: "+ " "+ str(y_test.value_counts()))


    #order: LR, RF, SVM, Ada
    clfs = [LogisticRegression(), RandomForestClassifier(), svm.SVC(), AdaBoostClassifier()]
    parameters = [{'penalty': ["l2"], "C": np.linspace(0.001,2,20), "class_weight": ['balanced'], "solver": ["liblinear"]}, #LR
                  {'criterion': np.array(['gini']), 'n_estimators': [100], 'min_samples_leaf': np.arange(2,5), 'max_depth': np.arange(2,5), 'min_samples_split': np.arange(2,5), "class_weight": ['balanced']}, #RF
                  {"C":np.linspace(0.1,3,100), "class_weight": ["balanced"],  "kernel": ["rbf"], "gamma": ["auto"], 'probability':[True]}, #SVC
                  {'n_estimators':[50]}] #Ada

    #column names of a dataframe to save
    dct={
         'Classifier':{},
         'Test_score':{},
         'Score_value':{},
         'Iteration_omission':{},
         'Model_roc_auc_omission':{},
         'Features_omission':{},
         'Importance_omission':{},
         'Rank_omission':{},
         'Iteration_permutation':{},
         'Model_roc_auc_permutation':{},
         'Features_permutation':{},
         'Importance_permutation':{},
         'Rank_permutation':{}
         }

    k,c,p,l,idx_o,idx_p = 0,0,0,0,0,0 #counter for indexes (k - df, clf and score, c - classes, p - permutation)
    it=1
    rank=1

    new_y_train = y_train.copy()
    new_y_train = y_train.apply(lambda x: 1 if x==df_name else 0) # setting the chosen dataframe to 1

    new_y_test = y_test.copy()
    new_y_test = y_test.apply(lambda x: 1 if x==df_name else 0)
    for classifier, param in zip(clfs, parameters):
        dct['Classifier'][k]=str(classifier).split("(")[0]
        cv = StratifiedKFold(n_splits=5, shuffle = True)
        clf = GridSearchCV(classifier, param, scoring = "roc_auc", cv = cv, n_jobs = -1)
        clf.fit(df_train, new_y_train)

        if "Logistic" in str(classifier):
            model = LogisticRegression(**clf.best_params_)
            logging.info("LR Best params: "+str(clf.best_params_))
        elif "Random" in str(classifier):
            model = RandomForestClassifier(**clf.best_params_, n_jobs = -1)
            logging.info("RF Best params: "+str(clf.best_params_))
        elif "SVC" in str(classifier):
            model = svm.SVC(**clf.best_params_)
            logging.info("SVC Best params: "+str(clf.best_params_))
        elif "Ada" in str(classifier):
            model = AdaBoostClassifier(**clf.best_params_)
            logging.info("Ada Best params: "+str(clf.best_params_))

        logging.info(f" MODEL: {model}")
        model.fit(df_train, new_y_train)

        ### PREDICTION ANALYSIS
        logging.info("\n-----------------------PREDICTION---------------------------")
        df_pred = model.predict(df_test)
        df_probs = model.predict_proba(df_test)[:, 1] #for roc_auc score

        #results measurement
        roc_auc = roc_auc_score(new_y_test, df_probs)
        precision, recall, f1_score, support = precision_recall_fscore_support(new_y_test, df_pred, average='binary')
        dct['Test_score'][c] = "ROC_AUC"
        dct['Score_value'][c] = round(roc_auc, 5)
        c=c+1
        dct['Test_score'][c] = "Precision"
        dct['Score_value'][c] = round(precision, 5)
        c=c+1
        dct['Test_score'][c] = "Recall"
        dct['Score_value'][c] = round(recall, 5)
        c=c+1
        dct['Test_score'][c] = "f1_score"
        dct['Score_value'][c] = round(f1_score, 5)
        c=c+1

        logging.info(" ROC_AUC: " + str(roc_auc))
        logging.info(" Precision: " + str(precision))
        logging.info(" Recall:    " + str(recall))
        logging.info(" f1_score:  " + str(f1_score))

        ### PERMUTATION ANALYSIS
        logging.info("\n-----------------------PERMUTATION--------------------------")
        perm_features_to_drop = []
        score_perm = cross_val_score(model, df_train, new_y_train, scoring="roc_auc", cv=StratifiedKFold(n_splits=5, shuffle = True))
        mean_score_perm = np.mean(score_perm)
        logging.info(f"Perm Score: {score_perm}, mean: {mean_score_perm}")
        if mean_score_perm>0.5:
            dct['Iteration_permutation'][idx_p]=it
            dct['Model_roc_auc_permutation'][idx_p] = round(mean_score_perm, 5)
            res = permutation_importance(model, df_train, new_y_train, n_repeats=10, scoring = "roc_auc")
            means, stds = res.importances_mean, res.importances_std
            logging.info(f"Permutation means: {means}")
            logging.info(f"Permutation stds: {stds}")
            rank_curr=rank
            for mean in means.argsort()[::-1]:
                if means[mean] - 2 * stds[mean] > 0:
                    curr_it_p=it
                    dct['Iteration_permutation'][idx_p]=curr_it_p
                    perm_features_to_drop.append(df_train.columns[mean])
                    dct['Features_permutation'][p]=df_train.columns[mean]
                    dct['Importance_permutation'][p]=f"{means[mean]:.5f}"
                    dct['Rank_permutation'][p]=rank_curr
                    rank_curr=rank_curr+1
                    logging.info((f"{df_train.columns[mean]}: " + f"{means[mean]:.5f}" + f" +/- {stds[mean]:.8f}"))
                    p=p+1
            curr_it_p += 1
            idx_p=p
            logging.info(f"Permutated features to drop: {perm_features_to_drop}")
            X_perm_new = df_train.drop(columns=perm_features_to_drop, axis=1)
            #loop permutation importance further w/o features found in the first iteration
            while((len(perm_features_to_drop)!=0) & (len(X_perm_new.columns)!=0) & (mean_score_perm>0.5)):
                perm_features_to_drop = []
                model.fit(X_perm_new, new_y_train)
                score_perm = cross_val_score(model, X_perm_new, new_y_train, scoring="roc_auc", cv=StratifiedKFold(n_splits=5, shuffle = True))
                mean_score_perm = np.mean(score_perm)
                logging.info(f"Perm Score: {score_perm}, mean: {mean_score_perm}")

                if mean_score_perm>0.5:
                    dct['Model_roc_auc_permutation'][idx_p] = round(mean_score_perm, 5)
                    res = permutation_importance(model, X_perm_new, new_y_train, n_repeats=10, scoring = "roc_auc")
                    means, stds = res.importances_mean, res.importances_std
                    logging.info(f"Permutation means: {means}")
                    logging.info(f"Permutation stds: {stds}")
                    for mean in means.argsort()[::-1]:
                        if means[mean] - 2 * stds[mean] > 0:
                            dct['Iteration_permutation'][idx_p]=curr_it_p
                            perm_features_to_drop.append(X_perm_new.columns[mean])
                            dct['Features_permutation'][p]=X_perm_new.columns[mean]
                            dct['Importance_permutation'][p]=f"{means[mean]:.5f}"
                            dct['Rank_permutation'][p]=rank_curr
                            rank_curr=rank_curr+1
                            logging.info((f"{X_perm_new.columns[mean]}: " + f"{means[mean]:.5f}" + f" +/- {stds[mean]:.8f}"))
                            p=p+1
                    curr_it_p += 1
                    idx_p=p
                    logging.info(f"Permutated features to drop: {perm_features_to_drop}")
                    X_perm_new = X_perm_new.drop(columns=perm_features_to_drop, axis=1)



        ### OMISSION ANALYSIS
        logging.info("\n-------------------------OMISSION----------------------------")
        df_omission = df_train.copy()
        df_omission[target] = new_y_train.values
        iter_1 = find_features(df_omission, target, classifier, param, scoring="roc_auc")
        best_parameters = iter_1[3]
        #df without features obtained in first iteration
        all_features_current = df_omission.drop(columns=iter_1[2])
        output = []
        curr_it=it
        rank_curr=rank
        # doubled for LR as it may happen that there are now features>0
        if iter_1[0]>0.5:
            dct['Iteration_omission'][idx_o]=curr_it
            dct['Model_roc_auc_omission'][k]=round(iter_1[0], 5)

        while ((not iter_1[2].empty) & (iter_1[0]>0.5)):

            if (all_features_current.shape[1] != 0):
                dct['Iteration_omission'][idx_o]=curr_it
                curr_it=curr_it+1
                dct['Model_roc_auc_omission'][k]=round(iter_1[0], 5)
                for el_2, el_1 in zip(iter_1[2], iter_1[1]):
                    dct['Features_omission'][l] = el_2
                    dct['Importance_omission'][l] = round(el_1, 5)
                    dct['Rank_omission'][l]=rank_curr
                    rank_curr=rank_curr+1
                    l=l+1
                idx_o,k=l,l
                output.append(iter_1[0:3])
                logging.info(iter_1[0:3])
                logging.info("______________________________________________")
                #iterate without important features from first iteration (second iteration)
                iter_1 = find_features(all_features_current, target, classifier, param, scoring="roc_auc")[0:3]
                if not iter_1[2].empty:
                    all_features_current = all_features_current.drop(columns=iter_1[2])
            else:
                logging.info("done")
                break
        logging.info("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        k,c,p,l,idx_o,idx_p = max(c,p,l), max(c,p,l), max(c,p,l), max(c,p,l), max(c,p,l), max(c,p,l)

    #table with scores (test set) and perm importance on train test
    result = pd.DataFrame(dct)
    result.sort_index(ascending=True, inplace=True)
    result = result.replace(np.nan, " ")

    return result
