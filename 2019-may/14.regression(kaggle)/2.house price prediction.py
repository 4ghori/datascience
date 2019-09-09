#knn
import sys
path = 'E://utils'
sys.path.append(path)

import common_utils  as utils
import regression_utils as rutils
from sklearn import metrics, model_selection, neighbors, linear_model, decomposition, manifold
import math
import pandas as pd
import os
import seaborn as sns
import numpy as np

def log_rmse(y_orig, y_pred):
    return math.sqrt(metrics.mean_squared_log_error(y_orig,y_pred) )

def rmse(y_orig, y_pred):
    return math.sqrt(metrics.mean_squared_error(y_orig,y_pred) )


path = 'E://'
house_train = pd.read_csv(os.path.join(path,"house_train.csv"))
house_train.shape
house_train.info()

house_test = pd.read_csv(os.path.join(path,"house_test.csv"))
house_test.shape
house_test.info()

house = pd.concat((house_train, house_test), axis = 0)
house.shape
house.info()

print(utils.get_continuous_features(house))
print(utils.get_non_continuous_features(house))

sns.countplot(x='YearBuilt',data=house_train)
sns.jointplot(x="SalePrice", y="YearBuilt", data=house_train)
sns.FacetGrid(house_train, hue="YearBuilt",size=8).map(sns.kdeplot, "SalePrice").add_legend()

sns.countplot(x='YrSold',data=house_train)
sns.jointplot(x="SalePrice", y="YrSold", data=house_train)
sns.FacetGrid(house_train, hue="YrSold",size=8).map(sns.kdeplot, "SalePrice").add_legend()

features_to_cast = ['MSSubClass']
utils.cast_to_cat(house, features_to_cast)

features_to_drop = ['Id']
missing_features_above_th = utils.get_features_to_drop_on_missingdata(house, 0.25)
features_to_drop.extend(missing_features_above_th)
house1 = utils.drop_features(house, features_to_drop)
house1.info()

imputable_cat_features = utils.get_non_continuous_features(house1)
cat_imputer = utils.get_categorical_imputers(house1, imputable_cat_features)
house1[imputable_cat_features] = cat_imputer.transform(house1[imputable_cat_features])

imputable_cont_features = utils.get_continuous_features(house1)
cont_imputer = utils.get_continuous_imputers(house1, imputable_cont_features)
house1[imputable_cont_features] = cont_imputer.transform(house1[imputable_cont_features])
house1.info()

house2 = utils.ohe(house1, imputable_cat_features)

scaler = utils.get_scaler(house2)
house3 = scaler.transform(house2)
house3 = pd.DataFrame(house3, columns=house2.columns)

X_train = house3[:house_train.shape[0]]
y_train = house_train['SalePrice']

utils.corr_heatmap(X_train)
lpca = decomposition.PCA()
lpca.fit(X_train)
print(np.cumsum(lpca.explained_variance_ratio_))
pca_data = lpca.transform(X_train)
print(pca_data.shape)
pca_data = pd.DataFrame(pca_data)

lasso_selector = linear_model.Lasso()
lasso_selector.fit(pca_data, y_train)
print(lasso_selector.coef_)
utils.plot_feature_importances(lasso_selector, pca_data, 40)

X_train1 = utils.select_features(lasso_selector, pca_data)
print(X_train1.shape)

tsne = manifold.TSNE(n_components=2)
tsne_data = tsne.fit_transform(X_train1)
rutils.plot_data_3d_regression(tsne_data, y_train)

scoring = metrics.make_scorer(log_rmse, greater_is_better=False)

knn_estimator = neighbors.KNeighborsRegressor()
knn_grid = {'n_neighbors':list(range(5,15)) }
final_model = utils.grid_search_best_model(knn_estimator, knn_grid, X_train1, y_train, scoring=scoring)

X_test = house3[house_train.shape[0]:]
pca_test_data = lpca.transform(X_test)
X_test1 = utils.select_features(lasso_selector, pd.DataFrame(pca_test_data))
print(X_test1.shape)

house_test['SalePrice'] = final_model.predict(X_test1)
house_test.to_csv("C:\\Users\\Algorithmica\\Downloads\\submission.csv", columns=["Id", "SalePrice"], index=False)
