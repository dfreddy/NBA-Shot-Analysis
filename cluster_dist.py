import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.cluster import KMeans
from scipy.spatial.distance import cdist
import pickle
import csv
from urllib.request import urlopen, Request
import string
import requests

colour_black = '#050505'
colour_pink = '#FFB6C1'
colour_silver = '#C0C0C0'
colours = ['r', 'g', 'b', 'y', 'm', 'c', colour_pink, colour_silver]
k = 8

# IMPORT CSV FILE
data = pd.read_csv('teams.csv')

'''VISUALISE INITIAL GRAPH FOR wins x dist
data_wins = data['wins'].values
data_dist = data['avg distance'].values
winsXdist = np.array(list(zip(data_wins, data_dist)))

plt.scatter(data_wins, data_dist, c=colours[0], s=20)
plt.xlabel('Regular Season Wins')
plt.ylabel('Average Shot Distance')
plt.title('NBA seasons 2015 through 2018 - initial 2 clusters')
plt.show()
'''

# APPLY K-MEANS CLUSTERING TO DATA

''' INCONCLUSIVE WITH wins x dist
kmeans = KMeans(n_clusters=k)
kmeans = kmeans.fit(winsXdist)
labels = kmeans.predict(winsXdist)
centroids = kmeans.cluster_centers_
'''

# attempting with threes and paint clustering
data_names = data['team'].values
data_wins = data['wins'].values
data_threes = data['threes'].values
data_paint = data['paint'].values
data_array = []

# put all rows entries into a array of dicts
for i in range(len(data_wins)):
    data_array_entry = {'threes': data_threes[i],
                        'paint': data_paint[i],
                        'wins': data_wins[i],
                        'name': data_names[i]}
    data_array.append(data_array_entry)

threesXpaint = np.array(list(zip(data_threes, data_paint)))

''' VISUALISING INITIAL GRAPH WITHOUT CLUSTERING APPLIED
plt.scatter(data_threes, data_paint, c=colours[0], s=20)
plt.xlabel('Attempts from three')
plt.ylabel('Attempts from the paint')
plt.title('NBA seasons 2015 through 2018')
plt.show()
'''

kmeans = KMeans(n_clusters=k)
kmeans = kmeans.fit(threesXpaint)
labels = kmeans.predict(threesXpaint)
centroids = kmeans.cluster_centers_

# VISUALISING WITH CLUSTERS

fig = plt.figure()
kx = fig.add_subplot(111)
clusters = []

for i in range(k):
    points = np.array([threesXpaint[j] for j in range(len(threesXpaint)) if labels[j] == i])
    kx.scatter(points[:, 0], points[:, 1], s=20, c=colours[i])
    clusters_entry = {'over50': 0, 'avg_wins': 0, 'colour': colours[i], 'threes': points[:, 0], 'paint': points[:, 1]}
    clusters.append(clusters_entry)

kx.scatter(centroids[:, 0], centroids[:, 1], marker='*', s=40, c=colour_black)

plt.xlabel('Attempts from three')
plt.ylabel('Attempts in the paint')
plt.title('Number of clusters={}'.format(k))
plt.show()

# FINDING OPTIMAL CLUSTERS NUMBER
# found 8 to be the optimal number for 3s x paint
'''
k_range = range(1, 10)
distorts = []

# measure the average distance from cluster points to centers
for i in k_range:
    kmeansModel = KMeans(n_clusters=i)
    kmeansModel.fit(threesXpaint)
    distorts.append(sum(np.min(cdist(threesXpaint, kmeansModel.cluster_centers_, 'euclidean'), axis=1)) / threesXpaint.shape[0])

fig = plt.figure()
ox = fig.add_subplot(111)
ox.plot(k_range, distorts, 'b*-')

plt.xlabel('K clusters')
plt.ylabel('Average distortion')
plt.show()
'''

# FIND AVERAGE WINS FOR EACH CLUSTER
for i in range(len(clusters)):
    wins = 0
    for j in range(len(clusters[i].get('threes'))):  # for every item in the cluster
        for t in range(len(data_array)):
            if data_array[t].get('threes') == clusters[i].get('threes')[j]:  # find its equivalent in the data array
                wins = wins + data_array[t].get('wins')  # add its wins
                break
    w = {'avg_wins': round(wins / len(clusters[i].get('threes')))}
    clusters[i].update(w)

for i in range(len(clusters)):
    print('Cluster with colour ' + clusters[i].get('colour') + ' averages ' + str(clusters[i].get('avg_wins')) + ' wins')

# FOR EACH CLUSTER, FIND PERCENTAGE OF CLUSTER WITH OVER 50 WINS
for i in range(len(clusters)):
    over50 = 0
    print('\nNew cluster')
    for j in range(len(clusters[i].get('threes'))):  # for every item in the cluster
        for t in range(len(data_array)):
            if data_array[t].get('threes') == clusters[i].get('threes')[j]:  # find its equivalent in the data array
                print('Team has {} wins'.format(data_array[t].get('wins')))
                if data_array[t].get('wins') >= 50:
                    over50 = over50 + 1  # increment if over 50 wins
                break
    o = {'over50': over50 * 100 / len(clusters[i].get('threes'))}
    clusters[i].update(o)

for i in range(len(clusters)):
    print('Cluster with colour ' + clusters[i].get('colour') + ' has {0:.2f}'.format(clusters[i].get('over50')) + '% teams over 50 wins')
