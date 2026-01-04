import os

import httpx
from fastapi import FastAPI, HTTPException
from services.shared.schemas import (
    ClassifierRequest,
    ClassifierResponse,
    EmbeddingRequest,
    EmbeddingResponse,
    GenerationRequest,
    GenerationResponse,
    EvalRequest,
    EvalResponse,
    HealthResponse,
    VisionRequest,
    VisionResponse,
)

app = FastAPI(title="gateway")

EMBEDDING_URL = os.getenv("EMBEDDING_URL", "http://embedding:8001/embedding")
CLASSIFIER_URL = os.getenv("CLASSIFIER_URL", "http://classifier:8002/classifier")
EVAL_URL = os.getenv("EVAL_URL", "http://eval:8003/eval")
LLM_URL = os.getenv("LLM_URL", "http://llm:8004/generate")
VISION_URL = os.getenv("VISION_URL", "http://vision:8005/classify-image")
REQUEST_TIMEOUT_SECONDS = float(os.getenv("REQUEST_TIMEOUT_SECONDS", "120"))


@app.get("/healthz", response_model=HealthResponse)
def healthz() -> HealthResponse:
    return HealthResponse(status="ok")


@app.get("/metrics")
def metrics() -> str:
    return "# placeholder metrics\n"


@app.post("/predict")
async def predict(payload: EmbeddingRequest) -> dict[str, object]:
    timeout = httpx.Timeout(REQUEST_TIMEOUT_SECONDS)
    async with httpx.AsyncClient(timeout=timeout) as client:
        try:
            embedding_response = await client.post(
                EMBEDDING_URL,
                json=payload.model_dump(),
            )
            embedding_response.raise_for_status()
            embedding = EmbeddingResponse.model_validate(embedding_response.json())

            classifier_response = await client.post(
                CLASSIFIER_URL,
                json=ClassifierRequest(vector=embedding.vector).model_dump(),
            )
            classifier_response.raise_for_status()
            classifier = ClassifierResponse.model_validate(classifier_response.json())

            eval_response = await client.post(
                EVAL_URL,
                json=EvalRequest(label=classifier.label, score=classifier.score).model_dump(),
            )
            eval_response.raise_for_status()
            evaluation = EvalResponse.model_validate(eval_response.json())
        except httpx.HTTPError as exc:
            raise HTTPException(status_code=502, detail=str(exc)) from exc

    return {
        "embedding": embedding.model_dump(),
        "classifier": classifier.model_dump(),
        "evaluation": evaluation.model_dump(),
    }


@app.post("/generate", response_model=GenerationResponse)
async def generate(payload: GenerationRequest) -> GenerationResponse:
    timeout = httpx.Timeout(REQUEST_TIMEOUT_SECONDS)
    async with httpx.AsyncClient(timeout=timeout) as client:
        try:
            llm_response = await client.post(LLM_URL, json=payload.model_dump())
            llm_response.raise_for_status()
        except httpx.HTTPError as exc:
            raise HTTPException(status_code=502, detail=str(exc)) from exc
    return GenerationResponse.model_validate(llm_response.json())


@app.post("/classify-image", response_model=VisionResponse)
async def classify_image(payload: VisionRequest) -> VisionResponse:
    timeout = httpx.Timeout(REQUEST_TIMEOUT_SECONDS)
    async with httpx.AsyncClient(timeout=timeout) as client:
        try:
            vision_response = await client.post(VISION_URL, json=payload.model_dump())
            vision_response.raise_for_status()
        except httpx.HTTPError as exc:
            raise HTTPException(status_code=502, detail=str(exc)) from exc
    return VisionResponse.model_validate(vision_response.json())
