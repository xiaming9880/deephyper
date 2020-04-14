from sklearn.neighbors import KNeighborsClassifier
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from deephyper.search.nas.model.preprocessing import minmaxstdscaler
import numpy as np


class BaseClassifierPipeline:
    """Baseline classifier to evaluate the problem at stake.

    >>> from sklearn.neighbors import KNeighborsClassifier
    >>> from deephyper.baseline import BaseClassifierPipeline
    >>> from sklearn.datasets import load_digits
    >>> load_data = lambda : load_digits(return_X_y=True)
    >>> baseline_classifier = BaseClassifierPipeline(KNeighborsClassifier(), load_data)
    >>> baseline_classifier.run() # doctest:+ELLIPSIS
    Not Weighted Accuracy (Test set):...
    """

    def __init__(
        self,
        clf=KNeighborsClassifier(),
        load_data_func=lambda: load_breast_cancer(return_X_y=True),
        seed=42,
    ):
        self.clf = clf
        self.seed = seed
        self.load_data_func = load_data_func
        self.preproc = minmaxstdscaler()

    def load_data(self):
        try:
            (X_train, y_train), (X_test, y_test) = self.load_data_func()
        except:
            X, y = self.load_data_func()
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.33, random_state=self.seed
            )

        return X_train, X_test, y_train, y_test

    def run(self):

        # loading the data
        X_train, X_test, y_train, y_test = self.load_data()

        # preprocessing the data
        X_train = self.preproc.fit_transform(X_train)
        X_test = self.preproc.transform(X_test)

        self.clf.fit(X_train, y_train)

        y_pred = self.clf.predict(X_test)
        acc_not_weighted = accuracy_score(y_test, y_pred)

        print("Not Weighted Accuracy (Test set): ", acc_not_weighted)

    def evaluate(self, metric):

        X_train, X_test, y_train, y_test = self.load_data()

        X_train = self.preproc.transform(X_train)
        X_test = self.preproc.transform(X_test)

        y_pred = self.clf.predict(X_train)
        score_train = metric(y_train, y_pred)

        y_pred = self.clf.predict(X_test)
        score_test = metric(y_test, y_pred)

        metric_name = metric.__name__

        print(f"{metric_name} on Train: ", score_train)
        print(f"{metric_name} on Test: ", score_test)


if __name__ == "__main__":
    baseline = BaseClassifierPipeline()
    baseline.run()