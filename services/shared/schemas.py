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
