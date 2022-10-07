#!/usr/bin/env python

import os
import requests
import pandas as pd
import numpy as np
from iso639 import languages
from asyncio_pool import AioPool
import asyncio as aio

API_URL = "http://localhost:8000"


def test_get_supported_languages():

    response = requests.get(API_URL + "/api/language/predict")
    assert response.status_code == 200
    resp_body = response.json()
    assert isinstance(resp_body["supported_languages"], list)
    assert isinstance(resp_body["supported_languages"][0], str)


def test_post_language_detection():
    response = requests.post(
        API_URL + "/api/language/predict", json={"text": "Testing this application"}
    )
    assert response.status_code == 200
    resp_body = response.json()
    assert resp_body["lang"] == "English"


def getSupportedLanguages():
    allLangs = requests.get(API_URL + "/api/language/predict").json()
    allLangs = allLangs["supported_languages"]
    return allLangs


def getTestData():
    cacheFile = "./test.csv"
    testDataUrl = "https://huggingface.co/datasets/papluca/language-identification/raw/main/test.csv"

    supportedLangs = getSupportedLanguages()
    if os.path.exists(cacheFile):
        data = pd.read_csv(cacheFile)
    else:
        data = pd.read_csv(testDataUrl)
        data.to_csv(cacheFile)
    data.rename(columns={"labels": "language", "text": "Text"}, inplace=True)
    data["language"] = data["language"].apply(lambda code: languages.part1[code].name)
    data = data[data["language"].isin(supportedLangs)]
    return data


async def task(row):
    row = row[1]
    response = requests.post(
        API_URL + "/api/language/predict", json={"text": row["Text"]}
    )
    resp_body = response.json()
    return [resp_body, row]


async def evaluateAccuracy():
    data = getTestData()
    stats = {}
    failed = []
    pool = AioPool(10)

    results = await pool.map(task, data.iterrows())
    print('complted %d requests ' % len(data))
    for [resp_body, row] in results:
        lang = row["language"]
        if lang not in stats:
            stats[lang] = {"total": 0, "failed": 0}
        if not resp_body["lang"] == lang:
            stats[lang]["failed"] += 1
            failed.append(row)

        stats[lang]["total"] += 1

    stats = pd.DataFrame(stats).T
    stats["success_percent"] = (1 - (stats["failed"] / stats["total"])) * 100.0
    stats.sort_values("success_percent", ascending=False, inplace=True)
    print(stats)
    return stats


if __name__ == "__main__":
    loop = aio.new_event_loop()
    loop.run_until_complete(evaluateAccuracy())
