from fastapi import FastAPI
from services.shared.schemas import ClassifierRequest, ClassifierResponse, HealthResponse

app = FastAPI(title="classifier")


@app.get("/healthz", response_model=HealthResponse)
def healthz() -> HealthResponse:
    return HealthResponse(status="ok")


@app.get("/metrics")
def metrics() -> str:
    return "# placeholder metrics\n"


@app.post("/classifier", response_model=ClassifierResponse)
def classifier(payload: ClassifierRequest) -> ClassifierResponse:
    return ClassifierResponse(label="demo", score=0.5)
