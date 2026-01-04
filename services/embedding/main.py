import os

from fastapi import FastAPI
from sentence_transformers import SentenceTransformer
from services.shared.schemas import EmbeddingRequest, EmbeddingResponse, HealthResponse

app = FastAPI(title="embedding")
MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME", "sentence-transformers/all-MiniLM-L6-v2")
_model: SentenceTransformer | None = None


def get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer(MODEL_NAME)
    return _model


@app.get("/healthz", response_model=HealthResponse)
def healthz() -> HealthResponse:
    return HealthResponse(status="ok")


@app.get("/metrics")
def metrics() -> str:
    return "# placeholder metrics\n"


@app.post("/embedding", response_model=EmbeddingResponse)
def embedding(payload: EmbeddingRequest) -> EmbeddingResponse:
    model = get_model()
    vector = model.encode(payload.text).tolist()
    return EmbeddingResponse(vector=vector)
