import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('golf_data.csv')
columns_to_keep = ['player', 'sg_putt', 'sg_arg', 'sg_app', 'sg_ott', 'sg_t2g', 'sg_total']
df = df[columns_to_keep]
df = df.dropna()
ssd = []
player_names = df['player']

df_numeric = df.select_dtypes(include=[np.number])

for k in range(1, 11):
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(df_numeric)
    ssd.append(kmeans.inertia_)


plt.plot(range(1, 11), ssd, 'bo-')
plt.title('The Elbow Method')
plt.xlabel('Number of clusters')
plt.ylabel('Sum of squared distances')
plt.show()

kmeans = KMeans(n_clusters=4)
clusters = kmeans.fit_predict(df_numeric)
centroids = kmeans.cluster_centers_
player_cluster = pd.DataFrame(clusters, index=df_numeric.index, columns=['cluster'])
player_cluster['player'] = df['player']
print(player_cluster)

for cluster, group in player_cluster.groupby("cluster"):
    print("Cluster:", cluster, "Size:", group.shape[0])
    for player in group.sample(5)['player']:
        print("\t", player)

for idx, centroid in enumerate(centroids):
    print("Centroid %d: %s" % (idx, centroid))
