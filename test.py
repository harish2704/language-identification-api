#!/usr/bin/env python

import requests

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
