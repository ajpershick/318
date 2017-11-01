import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys

from sklearn.pipeline import make_pipeline

def main():

    labelled = pd.read_csv(sys.argv[1])
    unlabelled = pd.read_csv(sys.argv[2])
    y = labelled['city'].drop_duplicates()
    x = labelled.drop(['city'], axis=1)
    x = x.drop(['year'], axis=1)

    models = [bayes_rgb_model, bayes_lab_model, knn_rgb_model, knn_lab_model, svc_rgb_model, svc_lab_model]
    for i, m in enumerate(models):  # yes, you can leave this loop in if you want.
        m.fit(X_train, y_train)
        plot_predictions(m)
        plt.savefig('predictions-%i.png' % (i,))


    output = sys.argv[3]
    print()

if __name__ == '__main__':
    main()