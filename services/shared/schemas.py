from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str


class EmbeddingRequest(BaseModel):
    text: str


class EmbeddingResponse(BaseModel):
    vector: list[float]


class ClassifierRequest(BaseModel):
    vector: list[float]


class ClassifierResponse(BaseModel):
    label: str
    score: float


class EvalRequest(BaseModel):
    label: str
    score: float


class EvalResponse(BaseModel):
    passed: bool


class GenerationRequest(BaseModel):
    prompt: str
    max_new_tokens: int | None = None


class GenerationResponse(BaseModel):
    text: str


class VisionRequest(BaseModel):
    image_base64: str
    top_k: int | None = None


class VisionPrediction(BaseModel):
    label: str
    score: float


class VisionResponse(BaseModel):
    predictions: list[VisionPrediction]
