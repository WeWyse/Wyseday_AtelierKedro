import pandas as pd
import numpy as np

from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
from kedro.config import TemplatedConfigLoader
from kedro.io import DataCatalog

def run_main(
        catalog: DataCatalog
):

  # Load IRIS data set
  iris = datasets.load_iris()
  X = iris.data[:, 2:]
  y = iris.target

  # Create training/ test data split
  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1, stratify=y)

  # Create an instance of Random Forest Classifier
  forest = RandomForestClassifier(criterion='gini',
                                  n_estimators=5,
                                  random_state=1,
                                  n_jobs=2)

  # Fit the model
  forest.fit(X_train, y_train)

  catalog.save("exemple_model", forest)


  model = catalog.load("exemple_model")


  # Measure model performance
  y_pred = model.predict(X_test)
  print('Accuracy: %.3f' % accuracy_score(y_test, y_pred))


if __name__ == "__main__":

  conf_loader = TemplatedConfigLoader("./conf", globals_pattern="*globals.yml")
  conf_catalog = conf_loader.get("my_catalog.yml")

  catalog = DataCatalog.from_config(conf_catalog)

  run_main(
    catalog=catalog
  )