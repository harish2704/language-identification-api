#!/usr/bin/env python

import logging

logging.basicConfig(level=logging.DEBUG)

import falcon
import falcon.asgi
from pydantic import BaseModel, Field
from spectree import Response, SpecTree, Tag

from language_detector import predict

log = logging.getLogger("server")

api = SpecTree(
    "falcon-asgi",
    title="Language detection service",
    version="0.0.1",
    description="Detect language of given text",
    contact={
        "name": "Harish",
        "email": "harish2704@gmail.com",
        "url": "https://github.com/harish2704",
    },
)


class LanguageDetectionRequest(BaseModel):
    text: str

    class Config:
        schema_extra = {
            "example": {
                "text": "How are you?",
            }
        }


class LanguageDetectionResponse(BaseModel):
    lang: str
    score: float = Field(gt=0, le=1, description="Probability score of the detection")

    class Config:
        schema_extra = {
            "example": {
                "lang": "English",
                "score": 0.993,
            }
        }


class LanguageDetection:
    """
    Language detection demo
    """

    @api.validate(
        json=LanguageDetectionRequest, resp=Response(HTTP_200=LanguageDetectionResponse)
    )
    async def on_post(self, req, resp):
        """
        Detect language of given text
        """
        pred = predict(req.context.json.text)
        resp.media = {"lang": pred[1][0], "score": pred[0][0]}


app = falcon.asgi.App()
app.add_route("/api/language-detect", LanguageDetection())
api.register(app)
