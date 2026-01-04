import math

import numpy as np
from fastapi import FastAPI
from services.shared.schemas import ClassifierRequest, ClassifierResponse, HealthResponse

app = FastAPI(title="classifier")
_weights: dict[int, np.ndarray] = {}
_bias = 0.1


@app.get("/healthz", response_model=HealthResponse)
def healthz() -> HealthResponse:
    return HealthResponse(status="ok")


@app.get("/metrics")
def metrics() -> str:
    return "# placeholder metrics\n"


@app.post("/classifier", response_model=ClassifierResponse)
def classifier(payload: ClassifierRequest) -> ClassifierResponse:
    vector = np.array(payload.vector, dtype=np.float32)
    if vector.size == 0:
        return ClassifierResponse(label="unknown", score=0.0)

    if vector.size not in _weights:
        rng = np.random.default_rng(seed=42 + vector.size)
        _weights[vector.size] = rng.standard_normal(vector.size).astype(np.float32)

    weights = _weights[vector.size]
    raw_score = float(vector.dot(weights) / math.sqrt(vector.size)) + _bias
    score = 1 / (1 + math.exp(-raw_score))
    label = "high_confidence" if score >= 0.6 else "low_confidence"
    return ClassifierResponse(label=label, score=score)
