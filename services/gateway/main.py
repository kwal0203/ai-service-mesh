from fastapi import FastAPI
from services.shared.schemas import (
    ClassifierRequest,
    ClassifierResponse,
    EmbeddingRequest,
    EmbeddingResponse,
    EvalRequest,
    EvalResponse,
    HealthResponse,
)

app = FastAPI(title="gateway")


@app.get("/healthz", response_model=HealthResponse)
def healthz() -> HealthResponse:
    return HealthResponse(status="ok")


@app.get("/metrics")
def metrics() -> str:
    return "# placeholder metrics\n"


@app.post("/predict")
def predict(payload: EmbeddingRequest) -> dict[str, object]:
    embedding = EmbeddingResponse(vector=[0.1, 0.2, 0.3])
    classifier = ClassifierResponse(label="demo", score=0.5)
    evaluation = EvalResponse(passed=True)
    return {
        "embedding": embedding.model_dump(),
        "classifier": classifier.model_dump(),
        "evaluation": evaluation.model_dump(),
    }
