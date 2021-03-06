# -*- coding: utf-8 -*-
"""Untitled1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1K6wmREL1jbkzV15IDJMuQNduxkpI5wjE
"""

from google.colab import drive
drive.mount("/content/gdrive")

import pandas as pd
import numpy as np
import seaborn as sns

rawData=pd.read_csv("/content/gdrive/MyDrive/cancerdata.csv")
rawData.head()

# Check NULL Values
rawData.isna().sum()

rawData.columns

# remove id column
rawData.drop(["id"],axis=1,inplace=True)

# Change disgnosis column into 0 & 1
rawData["diagnosis"]=np.where(rawData["diagnosis"]=="M",1,0)
rawData.head()

#####
#### Standardization
####

from sklearn.preprocessing import StandardScaler
rawData_Scaling=StandardScaler().fit(rawData)
rawData_Std=rawData_Scaling.transform(rawData)
raw_Data_Std=pd.DataFrame(rawData_Std,columns=rawData.columns)
raw_Data_Std.head()

#### Number of clusters-elbow method

####

from sklearn.cluster import KMeans
wss=[]
for k in range(1,15):
  kmeans=KMeans(n_clusters=k,random_state=2410).fit(raw_Data_Std)
  wss.append(kmeans.inertia_) # inertia has the overall WSS

print(wss)

sns.lineplot(x=range(1,15),y=wss)

### Modeling

### Clustering with 3 clusters
KMeans_Model=KMeans(n_clusters=3,random_state=2410).fit(raw_Data_Std)

##### Clustering Output Binding
####
KMeans_Model.labels_

# Combine cluster info with original data
fullDf=pd.concat([rawData,pd.Series(KMeans_Model.labels_)],axis=1).rename(columns={0:"cluster"})
fullDf.head()

## Cluster Size
fullDf["cluster"].value_counts()

# cluster profiling
cluster_profile_df=fullDf.groupby(["cluster"]).mean()
cluster_profile_df

### Bivariate Analysis
## plot diagnosis vs perimeter_mean 
sns.scatterplot(y="perimeter_mean",x="diagnosis",data=fullDf)

## concavity_mean vs perimieter_mean
sns.scatterplot(x="concavity_mean",y="perimeter_mean",hue="cluster",palette=["red","green","blue"],data=fullDf)

### 3 variable plot concavity_worst vs diagnosis

sns.scatterplot(x="concavity_worst",y="perimeter_mean",hue="cluster",size="diagnosis",palette=["red","green","blue"],data=fullDf)

# cluster validation using silhouette value
from sklearn.metrics import silhouette_samples,silhouette_score

# Since we passed std data into model.so we require to use same data sets into silhouette 
fullDf2=pd.concat([raw_Data_Std,pd.Series(KMeans_Model.labels_)],axis=1).rename(columns={0:"cluster"}).copy()
fullDf2.head()

fullDf2["silhouette_value"]=silhouette_samples(fullDf2,KMeans_Model.labels_)
fullDf2.head()

fullDf2.groupby(["cluster"])["silhouette_value"].mean()

### Overall silouette score
silhouette_score(fullDf2,KMeans_Model.labels_)

### Overall visualization of KMeans using PCA
from sklearn.decomposition import PCA

KMeans_PCA=PCA(n_components=2).fit(raw_Data_Std)

KMeans_PCA.explained_variance_ratio_

## transform the data
KMeans_PCAtranform=pd.DataFrame(KMeans_PCA.transform(raw_Data_Std))

KMeans_PCAtranform.columns=["PCA1","PCA2"]
KMeans_PCAtranform.head()

### cpmbine cluster information
KMeans_PCAData=pd.concat([KMeans_PCAtranform,fullDf2["cluster"]],axis=1)

## plot the PCA data
sns.scatterplot(x="PCA1",y="PCA2",hue="cluster",data=KMeans_PCAData,palette=["red","green","blue"])

