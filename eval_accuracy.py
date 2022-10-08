#!/usr/bin/env python

import os
import asyncio as aio
import requests
import pandas as pd
from iso639 import languages
import aiohttp
from asyncio_pool import AioPool

API_URL = "http://localhost:8000"


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
    i = row[0]
    row = row[1]
    url = API_URL + "/api/language/predict"
    body = {"text": row["Text"]}

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=body) as r:
            json_body = await r.json()
            return [json_body, row]


async def evaluateAccuracy():
    data = getTestData()
    stats = {}
    failed = []
    pool = AioPool(20)

    results = await pool.map(task, data.iterrows())
    print("complted %d requests " % len(data))
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
