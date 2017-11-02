import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
import sys

def main():

    labelled = pd.read_csv(sys.argv[1])
    unlabelled = pd.read_csv(sys.argv[2])
    y = labelled['city']
    X = labelled.drop(['city'], axis=1)
    #X = X.drop(['year'], axis=1)
    X_train, X_test, y_train, y_test = train_test_split(X, y)
    unlabelled = unlabelled.drop(['city'], axis=1)

    # # Bayes
    # bayes_model = make_pipeline(StandardScaler(), GaussianNB())
    # bayes_model = bayes_model.fit(X_train, y_train)
    # print('Bayes accuracy: ', bayes_model.score(X_test, y_test))

    # # KNeighboursClassifier
    # knn_model = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=9))
    # knn_model = knn_model.fit(X_train, y_train)
    # print('KNN accuracy: ', knn_model.score(X_test, y_test))

    # SVC
    svc_model = make_pipeline(StandardScaler(), SVC(C=10, kernel='linear'))
    svc_model = svc_model.fit(X_train, y_train)
    print('SVC accuracy: ', svc_model.score(X_test, y_test))
    predictions = svc_model.predict(unlabelled)
   # models = [bayes_model, knn_model, svc_model]
   # for i, m in enumerate(models):  # yes, you can leave this loop in if you want.

    pd.Series(predictions).to_csv(sys.argv[3], index=False)
    #print()

    df = pd.DataFrame({'truth': y_test, 'prediction': svc_model.predict(X_test)})
    print(df[df['truth'] != df['prediction']])

if __name__ == '__main__':
    main()