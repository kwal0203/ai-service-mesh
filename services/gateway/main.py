import asyncio
import json
import logging
import os
from pathlib import Path

import httpx
from fastapi import FastAPI, HTTPException
from services.shared.schemas import (
    ClassifierRequest,
    ClassifierResponse,
    EmbeddingRequest,
    EmbeddingResponse,
    GenerationRequest,
    GenerationResponse,
    RagRequest,
    RagResponse,
    RagSource,
    EvalRequest,
    EvalResponse,
    HealthResponse,
    CompareRequest,
    CompareResponse,
    CaptionRequest,
    CaptionResponse,
    VisionRequest,
    VisionResponse,
)

app = FastAPI(title="gateway")

EMBEDDING_URL = os.getenv("EMBEDDING_URL", "http://embedding:8001/embedding")
CLASSIFIER_URL = os.getenv("CLASSIFIER_URL", "http://classifier:8002/classifier")
EVAL_URL = os.getenv("EVAL_URL", "http://eval:8003/eval")
LLM_URL = os.getenv("LLM_URL", "http://llm:8004/generate")
VISION_URL = os.getenv("VISION_URL", "http://vision:8005/classify-image")
REQUEST_TIMEOUT_SECONDS = float(os.getenv("REQUEST_TIMEOUT_SECONDS", "300"))
RAG_CORPUS_PATH = os.getenv("RAG_CORPUS_PATH")

_corpus: list[dict[str, str]] = []
_corpus_vectors: list[list[float]] | None = None
logger = logging.getLogger("gateway")


def load_corpus() -> list[dict[str, str]]:
    global _corpus
    if _corpus:
        return _corpus
    if RAG_CORPUS_PATH:
        path = Path(RAG_CORPUS_PATH)
    else:
        path = Path(__file__).resolve().parents[1] / "shared" / "rag_corpus.json"
    with path.open("r", encoding="utf-8") as handle:
        _corpus = json.load(handle)
    return _corpus


def cosine_similarity(a: list[float], b: list[float]) -> float:
    if not a or not b or len(a) != len(b):
        return 0.0
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = sum(x * x for x in a) ** 0.5
    norm_b = sum(y * y for y in b) ** 0.5
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


async def embed_text(client: httpx.AsyncClient, text: str) -> list[float]:
    embedding_response = await client.post(EMBEDDING_URL, json=EmbeddingRequest(text=text).model_dump())
    embedding_response.raise_for_status()
    embedding = EmbeddingResponse.model_validate(embedding_response.json())
    return embedding.vector


async def ensure_corpus_vectors(client: httpx.AsyncClient) -> list[list[float]]:
    global _corpus_vectors
    if _corpus_vectors is not None:
        return _corpus_vectors
    corpus = load_corpus()
    tasks = [embed_text(client, item["text"]) for item in corpus]
    _corpus_vectors = await asyncio.gather(*tasks)
    return _corpus_vectors


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
            embedding_vector = await embed_text(client, payload.text)
            embedding = EmbeddingResponse(vector=embedding_vector)

            classifier_response = await client.post(
                CLASSIFIER_URL,
                json=ClassifierRequest(vector=embedding_vector).model_dump(),
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


@app.post("/rag-lite", response_model=RagResponse)
async def rag_lite(payload: RagRequest) -> RagResponse:
    timeout = httpx.Timeout(REQUEST_TIMEOUT_SECONDS)
    async with httpx.AsyncClient(timeout=timeout) as client:
        try:
            corpus = load_corpus()
            corpus_vectors = await ensure_corpus_vectors(client)
            query_vector = await embed_text(client, payload.question)
            scores = [
                cosine_similarity(query_vector, vector) for vector in corpus_vectors
            ]
            top_k = payload.top_k or 3
            ranked = sorted(
                zip(scores, corpus),
                key=lambda pair: pair[0],
                reverse=True,
            )[:top_k]
            sources = [
                RagSource(
                    id=item["id"],
                    source=item["source"],
                    text=item["text"],
                    score=score,
                )
                for score, item in ranked
            ]
            context = "\n".join(f"- {src.text}" for src in sources)
            prompt = (
                "Answer the question using only the context snippets.\n"
                f"Question: {payload.question}\n"
                f"Context:\n{context}\n"
                "Answer:"
            )
            llm_response = await client.post(
                LLM_URL,
                json=GenerationRequest(prompt=prompt, max_new_tokens=96).model_dump(),
            )
            llm_response.raise_for_status()
            answer = GenerationResponse.model_validate(llm_response.json()).text
        except Exception as exc:  # noqa: BLE001 - surface helpful detail in logs
            logger.exception("rag-lite failed")
            raise HTTPException(status_code=502, detail=str(exc)) from exc
    return RagResponse(answer=answer, sources=sources)


@app.post("/compare", response_model=CompareResponse)
async def compare(payload: CompareRequest) -> CompareResponse:
    timeout = httpx.Timeout(REQUEST_TIMEOUT_SECONDS)
    async with httpx.AsyncClient(timeout=timeout) as client:
        try:
            vector_a = await embed_text(client, payload.text_a)
            vector_b = await embed_text(client, payload.text_b)
            similarity = cosine_similarity(vector_a, vector_b)
            prompt = (
                "Compare the two texts in one sentence.\n"
                f"Text A: {payload.text_a}\n"
                f"Text B: {payload.text_b}\n"
                "Summary:"
            )
            llm_response = await client.post(
                LLM_URL,
                json=GenerationRequest(prompt=prompt, max_new_tokens=64).model_dump(),
            )
            llm_response.raise_for_status()
            summary = GenerationResponse.model_validate(llm_response.json()).text
        except httpx.HTTPError as exc:
            raise HTTPException(status_code=502, detail=str(exc)) from exc
    return CompareResponse(similarity=similarity, summary=summary)


@app.post("/caption", response_model=CaptionResponse)
async def caption(payload: CaptionRequest) -> CaptionResponse:
    timeout = httpx.Timeout(REQUEST_TIMEOUT_SECONDS)
    async with httpx.AsyncClient(timeout=timeout) as client:
        try:
            vision_response = await client.post(
                VISION_URL,
                json=VisionRequest(
                    image_base64=payload.image_base64, top_k=payload.top_k
                ).model_dump(),
            )
            vision_response.raise_for_status()
            predictions = VisionResponse.model_validate(vision_response.json()).predictions
            labels = [pred.label for pred in predictions]
            scores = [pred.score for pred in predictions]
            style = payload.style or "neutral"
            length = payload.length or "short"
            prompt = (
                "Write an image caption using these labels. "
                f"Style: {style}. Length: {length}.\n"
                "Labels: " + ", ".join(labels) + "."
            )
            llm_response = await client.post(
                LLM_URL,
                json=GenerationRequest(prompt=prompt, max_new_tokens=32).model_dump(),
            )
            llm_response.raise_for_status()
            caption_text = GenerationResponse.model_validate(llm_response.json()).text
        except httpx.HTTPError as exc:
            raise HTTPException(status_code=502, detail=str(exc)) from exc
    return CaptionResponse(labels=labels, scores=scores, caption=caption_text)
