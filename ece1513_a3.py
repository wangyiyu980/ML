# -*- coding: utf-8 -*-
"""ECE1513_A3.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1dVhdeya-IowzIyz12CyyewkxTUrLgLLz

Name: Yiyu Wang   
ID：1004574301   
URL: https://colab.research.google.com/drive/1dVhdeya-IowzIyz12CyyewkxTUrLgLLz?usp=sharing
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

#data
data = pd.read_csv("indian_liver_patient.csv")
data.fillna(0,inplace=True)
X = data.drop('Dataset', axis=1)
Y = data['Dataset']-1
X['Gender'] = X['Gender'].map({'Male': 1, 'Female': 0})

"""**Question 3. Find the correlation between the feature and
use the most two uncorrelated features in your scatter plot. How many clusters you
observed? Does this align with the number of labels in the dataset?**
"""

# the two most uncorrelated features
correlation_matrix = X.corr(numeric_only=True)
corr = correlation_matrix.unstack().sort_values().drop_duplicates()
f1,f2=corr.abs().idxmin()
f1,f2

plt.scatter(data[f1], data[f2])
plt.title(f'Scatter Plot of {f1} vs {f2}')
plt.xlabel(f1)
plt.ylabel(f2)
plt.show()

"""The scatter plot does not show two distinct clusters, which might suggest that 'Direct_Bilirubin' and 'Total_Proteins' alone do not provide a clear separation between liver patients and non-liver patients.

**Question 4. Clustering Methods:**  
**part a. Write a short paragraph about each clustering method mentioned above, and discuss the advantages, disadvantages, and use cases for each.**

**K-Means Clustering:**
K-means is a clustering algorithm that partitions a dataset into K distinct, non-overlapping clusters. It works well with large datasets and is best suited for situations where clusters are expected to be of similar size and density. The simplicity of K-means makes it easy to implement and interpret. However, it requires the number of clusters to be specified beforehand and is sensitive to initial seed placement.

**Hierarchical Clustering:**
Hierarchical clustering builds a multilevel hierarchy of clusters by either continually merging or splitting existing clusters. It does not require specifying the number of clusters, and the output dendrogram offers a detailed cluster structure. This method is less scalable to large datasets due to its higher computational cost. It is sensitive to noise and outliers, but it excels in revealing the fine-grained structure of data and is useful in exploratory data analysis, especially when the relationships within data are unknown.

**part b. Using Sklearn modules, implement the two clustering techniques. You would
ideally feed all the data to the clustering function and compare the predicted
clusters to the ground truth labels. Show the accuracy for each model.**
"""

# Standardize the data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# kmeans
kmeans = KMeans(n_clusters=2,n_init=10,random_state=42)
kmeans_Y = kmeans.fit_predict(X_scaled)
mapping_kmeans = {kmeans_label: true_label for kmeans_label, true_label in zip(kmeans_Y, Y)}
kmeans_mapped_Y = np.array([mapping_kmeans[label] for label in kmeans_Y])
accuracy_score(Y, kmeans_mapped_Y)

# Agglomerative
agglo = AgglomerativeClustering(n_clusters=2)
agglo_Y = agglo.fit_predict(X_scaled)
mapping_agglo = {agglo_label: true_label for agglo_label, true_label in zip(agglo_Y, Y)}
agglo_mapped_Y = np.array([mapping_agglo[label] for label in agglo_Y])
accuracy_score(Y, agglo_mapped_Y)

"""**part c. Repeat the same experiment with different hyperparameters, specifically the
number of clusters.**
"""

# number of clusters form 2 to 9
for n in range(2, 10):
    print(f"\nNumber of Clusters: {n}")

    # K-Means Clustering
    kmeans = KMeans(n_clusters=n,n_init=10,random_state=42)
    kmeans_Y = kmeans.fit_predict(X_scaled)
    mapping_kmeans = {kmeans_label: true_label for kmeans_label, true_label in zip(kmeans_Y, Y)}
    kmeans_mapped_Y = np.array([mapping_kmeans[label] for label in kmeans_Y])
    kmeans_accuracy=accuracy_score(Y, kmeans_mapped_Y)
    print(f"K-Means Clustering accuracy: {kmeans_accuracy}")

    # Hierarchical Clustering
    agglo = AgglomerativeClustering(n_clusters=n)
    agglo_Y = agglo.fit_predict(X_scaled)
    mapping_agglo = {agglo_label: true_label for agglo_label, true_label in zip(agglo_Y, Y)}
    agglo_mapped_Y = np.array([mapping_agglo[label] for label in agglo_Y])
    agglo_accuracy=accuracy_score(Y, agglo_mapped_Y)
    print(f"Hierarchical Clustering accuracy: {agglo_accuracy}")

"""**part d. Report which number of clusters is the best to cluster these data? Does this number match the number of labels you have? Do you observe any subgroups within a single label?**  
based on part c, the best number of clusters to cluster these data is 3, because it provide the highest accuracy for both K-Means Clustering and Hierarchical Clustering. This is not match the labels(2) we have, and this could indicates the presence of subgroups within the labels. For example, there might be different subtypes of liver disease within the liver patient records that are being picked up by the clustering algorithm.

**5. Dimensionality Reduction:**  
**part a. Write a short paragraph about the two methods mentioned above, and discuss the
advantages, disadvantages, and use cases for each.**


**PCA:** Principal Component Analysis (PCA) is a linear dimensionality reduction technique that identifies the axes with maximum variance to project high-dimensional data into a lower-dimensional space. It's efficient and widely used for noise reduction, feature extraction, and data visualization. However, PCA is limited by its linearity and assumption that high-variance directions are the most informative.

**t-SNE:** t-Distributed Stochastic Neighbor Embedding (t-SNE) is a non-linear technique excellent for visualizing complex high-dimensional data by grouping similar items closer in a low-dimensional space. While effective in revealing local structures and clusters, t-SNE is computationally intensive and sensitive to parameter settings.

**part b. Using Sklearn modules, reduce the dimensionality of the data from 10 features
into two features using both methods.**
"""

#pca
pca = PCA(n_components=2)
X_pca =pca.fit_transform(X_scaled)
X_pca

#t-SNE
tsne = TSNE(n_components=2, random_state=42)
X_tsne = tsne.fit_transform(X_scaled)
X_tsne







"""**part c. Repeat the scatter plot using the reduced features from each method. Unlike the previous
scatter plot, you need to use the labels to have separate colors for each label.**

"""

plt.scatter(X_pca[:, 0], X_pca[:, 1], c=Y, cmap='Paired', alpha=0.5,edgecolors='k')
plt.title('PCA: Reduced Features Scatter Plot')
plt.xlabel('PCA Feature 1')
plt.ylabel('PCA Feature 2')
plt.colorbar(label='Label')
plt.show()

plt.scatter(X_tsne[:, 0], X_tsne[:, 1],c=Y,cmap='Paired', alpha=0.5,edgecolors='k')
plt.title('t-SNE: Reduced Features Scatter Plot')
plt.xlabel('t-SNE Feature 1')
plt.ylabel('t-SNE Feature 2')
plt.colorbar(label='Label')
plt.show()

"""**part d. Compare the output of both method? Which is visually more effective in reducing the
data while preserving the categorization? why?**  

Based on the scatter plots, t-SNE has visually outperformed PCA in reducing the dimensionality of the data while preserving categorization. t-SNE's plot shows distinct, well-separated clusters, indicating that it has effectively captured local relationships and nuances within the data. PCA, while revealing variance-based structure, does not demarcate categories as clearly, resulting in more overlap between different labels.
"""