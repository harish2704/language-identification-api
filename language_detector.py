#!/usr/bin/env python

import os
import pickle
import iso639
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from logging import getLogger


log = getLogger("language-detector")

modelFilename = "lang-detect-MNB.pkl"
datasetFilename = "./dataset.csv"


def saveModel(model, cv):
    pickle.dump([model, cv], open(modelFilename, "wb"))
    log.info("saved model %s" % modelFilename)


def loadModel():
    loaded_model, loaded_cv = pickle.load(open(modelFilename, "rb"))
    log.info("loaded model %s" % modelFilename)
    return loaded_model, loaded_cv


def getModel():
    if os.path.exists(modelFilename):
        return loadModel()
    model, cv = trainModel()
    saveModel(model, cv)
    return model, cv


def getDataType1():
    if os.path.exists(datasetFilename):
        log.info("loading cached dataset %s" % datasetFilename)
        data = pd.read_csv(datasetFilename)
    else:
        log.info("Downloading dataset from url ...")
        data = pd.read_csv(
            "https://raw.githubusercontent.com/amankharwal/Website-data/master/dataset.csv"
        )
        data.to_csv(datasetFilename)
        log.info("Saved dataset to cache ...")
    data.isnull().sum()
    data["language"].value_counts()
    return data


def trainModel():
    log.info("Training model ...")
    cv = CountVectorizer()
    model = MultinomialNB()

    data = getDataType1()
    x = np.array(data["Text"])
    y = np.array(data["language"])

    X = cv.fit_transform(x)
    model.fit(X, y)
    log.info("Training complete. Feature count: %d" % model.feature_count_.size)
    return model, cv


model, cv = getModel()


def predict(text):
    data = cv.transform([text]).toarray()
    pred = model.predict_proba(data).reshape(-1)
    pred = pd.DataFrame(zip(pred, model.classes_))
    pred = pred.sort_values(0, ascending=False)[:3].to_dict("list")
    return pred
