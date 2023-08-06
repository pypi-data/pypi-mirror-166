import numpy as np
import pandas as pd
from matplotlib.collections import PolyCollection, LineCollection
from scipy.spatial import ConvexHull, Delaunay
from sklearn.utils import resample
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN
import random
import os
from sklearn.model_selection import GridSearchCV, StratifiedKFold
import logging
logging.basicConfig(filename='log.txt',level=logging.INFO)

### Convex Hull

def add_edge(i, j, edges, edge_points, tri):
    '''
    Add a line between the i-th and j-th points. Modifies a given list of edge_points

    Args:
        i,j: vertices of facets forming the convex hull of "tri"-argument
        edges: a set of edges
        edge_points: a list of edges
        tri: a scipy.spatial.Delaunay object
    '''
    if (i, j) in edges or (j, i) in edges:
        # already in the set
        return
    edges.add( (i, j) )
    edge_points.append(tri.points[ [i, j] ])

def in_hull(p, hull):
    '''
    Test if given points are in the convex hull of

    Args:
        p: number of n-points coordinates in k-dimension
        hull: a scipy.spatial.Delaunay object or an array of points with the same dimension for which Delaunay triangulation will be computed
    Return:
        A boolean list: True - a point lies within some simplex, False - there is no simplex found (a point lies outside the hull)
    '''
    if not isinstance(hull,Delaunay):
        hull = Delaunay(hull)

    return hull.find_simplex(p)>=0

def get_intersections(to_boot, fixed, size, df_names, pair):
    '''
    Calculates intersections of two lists of points of the same dimension

    Args:
        to_boot: numpy array of points of one dataframe which size will be altered. Contains only parameters of interest
        fixed: numpy array of points of another dataframe which size remains the same. Contains only parameters of interest
        size: a list of integers, sizes for resampling
        df_names: a list of strings, dataframes' names (e.g. ['df_1','df_2']), in the same order as to_boot and fixed arguments
        pair: a list, a combination of parameters
    Returns:
        df: a pandas dataframe, a table with intersection values for a combination of parameters and hospital cases
    '''

    dct = {'Size':{},'Name':{}, 'Parameters':{}, 'Intersection':{}}
    count = 0

    for s in size:
        for i in np.arange(100):
            # create a random sample set of a certain size
            boot_1 = resample(to_boot, replace=True, n_samples=s, random_state=i+s) #sampled dataframe
            boot_2 = resample(fixed, replace=True, n_samples=len(fixed), random_state=i+s) #fixed full dataframe

            #test if df_1 (boot_1) in df_2
            inside_1 = in_hull(boot_1,boot_2)
            ins_1 = boot_1[inside_1]
            dct['Size'][count] = s
            dct['Name'][count] = f"sampled {df_names[0]} in full {df_names[1]}"
            dct['Parameters'][count] = ", ".join(pair)
            dct['Intersection'][count] = len(ins_1)/len(boot_1)
            count+=1

            #test if df_2 in df_1 (boot_1)
            inside_2 = in_hull(boot_2,boot_1)
            ins_2 = boot_2[inside_2]
            dct['Size'][count] = s
            dct['Name'][count] = f"full {df_names[1]} in sampled {df_names[0]}"
            dct['Parameters'][count] = ", ".join(pair)
            dct['Intersection'][count] = len(ins_2)/len(boot_2)
            count+=1

    df = pd.DataFrame(dct)
    return df

def full_intersections(df_1, df_2, df_names, pair):
    '''
    Calculates intersections of two lists of points of the same dimension

    Args:
        df_1, df_2: numpy array of points of a clinic which contains only parameters of interest
        df_names: a list of strings, hospitals' names (e.g. ['df_1','df_2']), in the same order as df_1 and df_1 arguments
        pair: a list, a combination of parameters
    Returns:
        df: a pandas dataframe, a table with intersection values for a combination of parameters and hospital cases
    '''

    dct = {'Name':{}, 'Parameters':{}, 'Intersection':{}}
    count = 0

    for i in np.arange(100):
        # create a random sample set of a certain size for both clinics
        boot_1 = resample(df_1, replace=True, n_samples=len(df_1), random_state=i+i)
        boot_2 = resample(df_2, replace=True, n_samples=len(df_2), random_state=i+i)

        #test if df_1 in df_2
        inside_1 = in_hull(boot_1,boot_2)
        ins_1 = boot_1[inside_1]
        dct['Name'][count] = f"full {df_names[0]} in full {df_names[1]}"
        dct['Parameters'][count] = ", ".join(pair)
        dct['Intersection'][count] = len(ins_1)/len(boot_1)
        count+=1


        #test if df_2 in df_1
        inside_2 = in_hull(boot_2,boot_1)
        ins_2 = boot_2[inside_2]
        dct['Name'][count] = f"full {df_names[1]} in full {df_names[0]}"
        dct['Parameters'][count] = ", ".join(pair)
        dct['Intersection'][count] = len(ins_2)/len(boot_2)
        count+=1


    df = pd.DataFrame(dct)
    return df

def run_dbscan(points, xy, df_name, eps = 0.5, min_samples = 4, not_noise = 0.9):
    '''
    Detect outliers using DBSCAN

    Args:
        points: numpy array of all points of one dataframe
        xy: a list of strings, a combination of parameters
        df_name: a string, a dataframe name
        eps: float, start value for epsilon hyperparameter of dbscan algorithm
        min_samples: int, start value for min_samples hyperparameter of dbscan algorithm
        not_noise: float, minimal number of points that are considered to be with correct values
    Return:
        bools: a boolean list, True - a point belongs to a cluster, False - an outlier
        end_eps: float, end value for eps-parameter
        end_min_samples: int, end value for min_samples-parameter
    '''
    scaled = StandardScaler().fit_transform(points)

    bools=[] # container for points that form a cluster
    while bools.count(True) < len(points)*not_noise: #controls the amount of outliers
        db = DBSCAN(eps=eps, min_samples=min_samples).fit(scaled)
        while (len(set(db.labels_))!=2):

            if len(set(db.labels_))>2: #2 labels = 1 cluster label + 1 outlier label
                eps=round(eps+0.05, 2)
                db = DBSCAN(eps=eps, min_samples=min_samples).fit(scaled)

            if len(set(db.labels_))<2:
                if len(set(db.labels_))==1 and (-1 in set(db.labels_)):
                    eps=round(eps+0.05,2)
                else:
                    min_samples=min_samples+1
                db = DBSCAN(eps=eps, min_samples=min_samples).fit(scaled)

        #case: set(db.labels_)==2
        bools = [True if x>(-1) else False for x in db.labels_]
        if bools.count(True) >= len(points)*not_noise:
            end_eps = round(eps, 2)
            end_min_samples = min_samples
        eps=round(eps+0.05,2)

    return bools, end_eps, end_min_samples

### Machine Learning

def get_correlated(df, coef):
    ''' Finds correlated features
    Args:
        df: dataframe with parameter values
        coef: upper limit to consider features to be not correlated
    Return:
        to_drop: list of features to drop as correlated with another ones
    '''
    # Create correlation matrix
    corr_matrix = df.corr().abs()

    # Select upper triangle of correlation matrix
    upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(np.bool))
    to_drop = [column for column in upper.columns if any(upper[column] > coef)]

    return to_drop

def run_classifier(all_features, target, classifier, clf_params, scoring):
    ''' Tunes classifier
    Args:
        all_features: dataframe with all features to process
        classifier: options - LR, RF, SVM, Ada
        clf_params: parameters for classifiers
        scoring: metric to measure classifier performance
    Return:
        all_features_accuracy: best scores
        best_parameters: parameters of the best model
    '''
    if len(all_features.columns)>1: #for omission method should be more than 1 parameter
        features = all_features.drop(columns=[target]).copy()
        logging.info(features.shape)
        # Run classifier with cross-validation
        X = pd.DataFrame(features, columns=features.columns)
        y = all_features[target]
        cv = StratifiedKFold(n_splits=5, shuffle = True)
        clf = GridSearchCV(classifier, clf_params, scoring = scoring, cv = cv, n_jobs = -1)
        clf.fit(X, y)

        all_features_accuracy = clf.best_score_
        best_parameters = clf.best_params_
    else:
        logging.info("Not enough features for classifier to run")
        all_features_accuracy = 0
        best_parameters = None

    return all_features_accuracy, best_parameters


def find_features(all_features, target, classifier, clf_params, scoring):
    ''' Finds important features with omission method
    Args:
        all_features: dataframe with all features to process
        target: string, name of the target feature
        classifier: options - LR, RF, SVM, Ada
        clf_params: parameters for classifiers
        scoring: metric to measure classifier performance
    Return:
        all_features_accuracy: the best score of classifier performance for all features
        values: series of important features scores
        important_features: series of important features
        best_parameters: parameters of the best model
    '''
    # find accuracy with all features
    features = all_features.drop(columns=[target]).copy()
    logging.info(features.shape)

    all_features_accuracy , best_parameters = run_classifier(all_features, target, classifier, clf_params, scoring)

    ### feature omission importance
    output_final = []
    std_list = []
    if len(features.columns)>1:
        logging.info("starting for-loop")
        for feature in features.columns:
            # repeat multiple time (to apply the same approach as in permuataion_importance)
            repeated_omission=[] # at the end contains n elements (=loop repetition) for every feature at a time
            for i in range(0,10):
                features_omission = all_features.drop(columns = [feature]+[target]).copy()

                X = pd.DataFrame(features_omission, columns=features_omission.columns)
                y = all_features[target]

                cv = StratifiedKFold(n_splits=5, shuffle = True)
                clf = GridSearchCV(classifier, clf_params, scoring = scoring, cv = cv, n_jobs = -1)
                clf.fit(X, y)
                repeated_omission.append(all_features_accuracy - clf.best_score_) #stores differences

            output_final.append(np.mean(repeated_omission)) #stores mean of feature omission n-loop-repetitions
            std_list.append(np.std(repeated_omission)) #stores std of feature omission n-loop-repetitions
    else:
        logging.info("not enough features")

    #find important features accourding to feature omission
    norm_output = []

    for output, std in zip(output_final, std_list):
        if (output - 2*std)>0:
            norm_output.append(output)
        else:
            norm_output.append(-100)

    if len(norm_output)!=0:
        df_to_plot = pd.DataFrame({'parameters': features.columns, 'value': norm_output})
        df_to_plot=df_to_plot[df_to_plot['value']>0]
        df_to_plot=df_to_plot.sort_values(by=['value'], ascending=False)

        important_features = df_to_plot.parameters
        values = df_to_plot.value

        if (len(important_features)==0):
            logging.info(f"No features that > 0")
    else:
        important_features=pd.Series()
        values= pd.Series()

    return all_features_accuracy, values, important_features, best_parameters
