from fastapi import FastAPI
from services.shared.schemas import EmbeddingRequest, EmbeddingResponse, HealthResponse

app = FastAPI(title="embedding")


@app.get("/healthz", response_model=HealthResponse)
def healthz() -> HealthResponse:
    return HealthResponse(status="ok")


@app.get("/metrics")
def metrics() -> str:
    return "# placeholder metrics\n"


@app.post("/embedding", response_model=EmbeddingResponse)
def embedding(payload: EmbeddingRequest) -> EmbeddingResponse:
    return EmbeddingResponse(vector=[0.1, 0.2, 0.3])
