import numpy as np
import pandas as pd
from algorithms import rdf_parser
from sklearn.cluster import KMeans, DBSCAN, Birch
import numpy as np

# load data
hamster_lines = rdf_parser.load_doc()
hamster_ids, hamster_friendship = rdf_parser.collect_data(hamster_lines)
hamster_friendship_dict = rdf_parser.create_friendship(hamster_ids, hamster_friendship)

#print(hamster_ids)

def check_if_mutual_friends():
    for hamster in hamster_friendship_dict.keys():
        for friend in hamster_friendship_dict.keys():
            if hamster in hamster_friendship_dict[friend] and friend in hamster_friendship_dict[hamster]:
                print("Friends:")
                print(hamster, friend)

#check_if_mutual_friends()

def similarity(row1, row2):
    return np.sum(row1 == row2)

def form_a_friendship_matrix():
    df = pd.DataFrame(index=hamster_ids, columns=hamster_ids)
    df = df.fillna(0)
    for hamster in hamster_friendship_dict.keys():
        for friend in hamster_friendship_dict.keys():
            if hamster in hamster_friendship_dict[friend] and friend in hamster_friendship_dict[hamster]:
                df[hamster][friend] = 1
                df[friend][hamster] = 1
                df[hamster][hamster] = 1

    print(df)
    print(df.sum(axis=0))
    print(df.sum(axis=1))
    return df # vrati matricu

def is_friend(df, hamster, friend):
    if df[hamster][friend] == 1:
        return True
    else:
        return False


df = form_a_friendship_matrix()
#df['no_of_friends'] = df.sum(axis=1)-1
#print (df)

X = df.values

def kmeans_clustering(X):
    kmeans = KMeans(n_clusters=2, random_state=42).fit_predict(X)
    df['label'] = kmeans
    print(df)
    df.to_csv('kmeans_results.csv')

def dbscan_clustering(X):
    dbscan = DBSCAN(eps=6, min_samples=10, metric='euclidean', algorithm='auto', leaf_size=30, p=None, n_jobs=1).fit_predict(X)
    df['label'] = dbscan
    print(df)
    df.to_csv('dbscan_results.csv')


def birch_clustering(X):
    birch = Birch(threshold=0.5, branching_factor=50, n_clusters=3, compute_labels=True, copy=True).fit_predict(X)
    df['label'] = birch
    print(df)
    df.to_csv('birch_clustering.csv')
