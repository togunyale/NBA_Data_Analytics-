'''
Created on Oct 28, 2019

@author: togunyale
'''
import pandas as pd  
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns; sns.set()
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
rootSrc = '/Users/togunyale/eclipse-workspace/ReboundingProject/DataSets'
# GATHER THE INITAL FEATURE SPACE , INPUTS 
raw_data = pd.read_csv('/Users/togunyale/eclipse-workspace/ReboundingProject/DataSets/dataset_2019_10_26.csv')
dataset = raw_data.copy()

# GATHER THE SPECIFIC FEATURE SPACE 
data = np.asarray(dataset[['Age','Height' , 'Weight', 'UsageRate' , 'AssistRate' , 'ThreePtRate' , 'FreeThrowRate' , 'TotalFouls'
                           ,'TotalBlocks','OR2_per48','DR2_per48','OR3_per48','DR3_per48']].values)
newdata = np.array([data[:,0],data[:,1],data[:,2],data[:,3],data[:,4],data[:,5],data[:,6]
                    ,data[:,7],data[:,8],data[:,9],data[:,10],data[:,11],data[:,12]])

# GATHER THE MEAN VALUES FOR EACH X / INPUT/ DIMENSIONAL  -- THEN CREATE MEAN VECTOR THAT CONTAINS ALL THE MEANS 
x1_mean = np.mean(newdata[0])
x2_mean = np.mean(newdata[1])
x3_mean = np.mean(newdata[2])
x4_mean = np.mean(newdata[3])
x5_mean = np.mean(newdata[4])
x6_mean = np.mean(newdata[5])
x7_mean = np.mean(newdata[6])
x8_mean = np.mean(newdata[7])
x9_mean = np.mean(newdata[8])
x10_mean = np.mean(newdata[9])
x11_mean = np.mean(newdata[10])
x12_mean = np.mean(newdata[11])
x13_mean = np.mean(newdata[12])

mean_vector = np.array([[x1_mean],[x2_mean],[x3_mean],[x4_mean],[x5_mean],[x6_mean],[x7_mean],[x8_mean],[x9_mean]
                        ,[x10_mean],[x11_mean],[x12_mean],[x13_mean]])

# SCATTER MATRIX -- INIT
scatter_matrix = np.zeros((13,13)) #Size of the scatter mmatrix 
for i in range(newdata.shape[1]):
    scatter_matrix += (newdata[:13,i].reshape(13,1) - mean_vector).dot((newdata[:13,i].reshape(13,1) - mean_vector).T)
    
# COMPUTE EIGEN VECTORS AND VALUES:
eigValue, eigVectors = np.linalg.eig(scatter_matrix)

# PAIR THE EIGEN VALUES WITH THEIR CORRESPONDING EIGEN VECTORS AND THEN SORT BASED OFF THE EIGRN VALUES
eig_pairs = [(np.abs(eigValue[i]), eigVectors[i] ) for i in range(len(eigValue))]
eig_pairs.sort(key=lambda x:x[0] , reverse=True)

# CHOOSING THE K EIGEN VECTORS WITH THE LARGEST EIGENVALUES 
# matrix_w = np.hstack(INPUTS K NUMBER OF VECTORS WITH LARGEST VALUES ))
matrix_w = np.hstack((
    eig_pairs[0][1].reshape(13,1), 
    eig_pairs[1][1].reshape(13,1),
    eig_pairs[2][1].reshape(13,1), 
    eig_pairs[3][1].reshape(13,1),
    eig_pairs[4][1].reshape(13,1),
    eig_pairs[5][1].reshape(13,1), 
    eig_pairs[6][1].reshape(13,1),
    ))

# TRANSFORM DATASET INTO THE NEW SUBSPACE 
# TAKE THE K DIMENSIONAL SUBSPACE AND TRANSFORM THE D DIMENSIONAL DATASET INTO THAT NEW SUBASPACE 
# y = subspace.T x dataset(original feature space)
transformed = matrix_w.T.dot(newdata)

inputXY = pd.DataFrame( data = np.column_stack((transformed[0,0:302].reshape(-1,1),transformed[1,0:302].reshape(-1,1))), columns =['X','Y'])
sse = []
sil =[]

for cluster_cnt in range(1,11):
    kmeans = KMeans(n_clusters=cluster_cnt).fit(inputXY.values)
    # For Elbow Mehtod (1):
    centroid = kmeans.cluster_centers_
    predict = kmeans.predict(inputXY.values)
    curr_sse = 0
    
    # For Silhouette Method :
    if cluster_cnt > 1:
        labels = kmeans.labels_
        sil.append(silhouette_score(inputXY.values, labels, metric = 'euclidean'))
        
    # For Elbow Mehtod (2):            
    points = np.array(inputXY)
    evaluation = [[0,0] for x in range(cluster_cnt)]
    for it in range(len(np.array(inputXY))):
        curr_center = centroid[predict[it]]
        curr_sse+= (points[it, 0] - curr_center[0]) ** 2 + (points[it, 1] - curr_center[1]) ** 2 
        
    sse.append(curr_sse)
    
    
plt.plot(sse)  

plt.xlabel('Number of Clusters (k)')
plt.ylabel('Within-Cluster-Sum of Squared Errors (WSS)')
plt.title('Elbow Method : Cluster Determination')
plt.savefig(rootSrc +'/ElbowMethod_Graph.png', bbox_inches='tight')
plt.show()

plt.plot(sil)  

plt.xlabel('Number of Clusters (k)')
plt.ylabel('Silhouette Score')
plt.title('Silhouette Method : Cluster Determination')
plt.savefig(rootSrc +'/Silhouette Method.png', bbox_inches='tight')
plt.show()

kmeans = KMeans(n_clusters=3).fit(inputXY.values)
centroids = kmeans.cluster_centers_
predict = kmeans.predict(inputXY.values) 
plt.scatter(inputXY.values[:,0],inputXY.values[:,1], c=kmeans.labels_.astype(float), cmap='viridis',
            edgecolor='k')
plt.scatter(centroids[:, 0], centroids[:, 1], c='red', edgecolor='k', s=100)
plt.xlabel('X_Values')
plt.ylabel('Y_Values')
plt.show()

dataset['label'] = kmeans.labels_


player_eval = dataset.groupby(['label']).mean()

player_eval.to_csv(rootSrc + '/dataset_2019_11_01_MeanGroups.csv')
dataset.loc[dataset['label'] == 0].to_csv(rootSrc + '/dataset_2019_11_01_Group00.csv')
dataset.loc[dataset['label'] == 1].to_csv(rootSrc + '/dataset_2019_11_01_Group01.csv')
dataset.loc[dataset['label'] == 2].to_csv(rootSrc + '/dataset_2019_11_01_Groups02.csv')