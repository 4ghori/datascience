import pandas as pd
from sklearn.externals import joblib
import os

dir = "C:\\Users\\Algorithmica\\Downloads"
objects = joblib.load(os.path.join(dir, 'deployment.pkl') )

#read test data
titanic_test = pd.read_csv(os.path.join(dir, "titanic_test.csv"))
print(titanic_test.info())

imputable_cont_features = objects.get('imputable_cont_features')
cont_imputer = objects.get('cont_imputer')
titanic_test[imputable_cont_features] = cont_imputer.transform(titanic_test[imputable_cont_features])

cat_imputer = objects.get('cat_imputer')
titanic_test['Embarked'] = cat_imputer.transform(titanic_test['Embarked'])

le_emb = objects.get('le_emb')
titanic_test['Embarked'] = le_emb.transform(titanic_test['Embarked'])

le_sex = objects.get('le_sex')
titanic_test['Sex'] = le_sex.transform(titanic_test['Sex'])

le_pclass = objects.get('le_pclass')
titanic_test['Pclass'] = le_pclass.transform(titanic_test['Pclass'])

ohe = objects.get('ohe')
cat_features = objects.get('cat_features')
cont_features = objects.get('cont_features')
tmp1 = ohe.transform(titanic_test[cat_features]).toarray()
tmp1 = pd.DataFrame(tmp1)
tmp2 = titanic_test[cont_features]
tmp = pd.concat([tmp1, tmp2], axis=1)

scaler = objects.get('scaler')
X_test = scaler.transform(tmp)

knn_estimator = objects.get('knn_estimator')
titanic_test['Survived'] = knn_estimator.predict(X_test)
titanic_test.to_csv("C:\\Users\\Algorithmica\\Downloads\\submission.csv", columns=["PassengerId", "Survived"], index=False)
