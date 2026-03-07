from __future__ import annotations

from pathlib import Path
from urllib.parse import urlparse

import joblib
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from feature_extraction import extract_features_dataframe

app = FastAPI(title="PhishGuard AI API", version="1.0.0")

MODEL_PATH = Path(__file__).resolve().parent / "model.pkl"
model = joblib.load(MODEL_PATH)


class PredictRequest(BaseModel):
    url: str = Field(..., examples=["https://secure-login-example.com"])


class PredictResponse(BaseModel):
    url: str
    prediction: int
    result: str
    confidence: float


@app.get("/")
def health_check() -> dict[str, str]:
    return {"status": "ok", "service": "PhishGuard AI API"}


@app.post("/predict", response_model=PredictResponse)
def predict(payload: PredictRequest) -> PredictResponse:
    candidate = payload.url.strip()

    if not candidate:
        raise HTTPException(status_code=400, detail="URL cannot be empty")

    parsed = urlparse(candidate if "://" in candidate else f"http://{candidate}")
    if not parsed.netloc:
        raise HTTPException(status_code=400, detail="Invalid URL format")

    features = extract_features_dataframe([candidate])

    prediction = int(model.predict(features)[0])

    if hasattr(model, "predict_proba"):
        probability = float(model.predict_proba(features)[0][1])
        confidence = probability if prediction == 1 else 1.0 - probability
    else:
        confidence = 0.5

    label = "Phishing Website" if prediction == 1 else "Safe Website"

    return PredictResponse(
        url=candidate,
        prediction=prediction,
        result=label,
        confidence=round(confidence, 4),
    )