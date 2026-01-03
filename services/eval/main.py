from fastapi import FastAPI
from services.shared.schemas import EvalRequest, EvalResponse, HealthResponse

app = FastAPI(title="eval")


@app.get("/healthz", response_model=HealthResponse)
def healthz() -> HealthResponse:
    return HealthResponse(status="ok")


@app.get("/metrics")
def metrics() -> str:
    return "# placeholder metrics\n"


@app.post("/eval", response_model=EvalResponse)
def eval_api(payload: EvalRequest) -> EvalResponse:
    return EvalResponse(passed=True)
