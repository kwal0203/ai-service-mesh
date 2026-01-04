import os

import torch
from fastapi import FastAPI
from transformers import AutoModelForCausalLM, AutoTokenizer
from services.shared.schemas import GenerationRequest, GenerationResponse, HealthResponse

app = FastAPI(title="llm")

MODEL_NAME = os.getenv("LLM_MODEL_NAME", "EleutherAI/pythia-70m-deduped")
MAX_NEW_TOKENS_DEFAULT = int(os.getenv("LLM_MAX_NEW_TOKENS", "64"))
TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.7"))
TOP_P = float(os.getenv("LLM_TOP_P", "0.9"))

_tokenizer: AutoTokenizer | None = None
_model: AutoModelForCausalLM | None = None


def get_model() -> tuple[AutoTokenizer, AutoModelForCausalLM]:
    global _tokenizer, _model
    if _tokenizer is None or _model is None:
        _tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        _model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
        _model.eval()
        if _tokenizer.pad_token_id is None:
            _tokenizer.pad_token_id = _tokenizer.eos_token_id
    return _tokenizer, _model


@app.get("/healthz", response_model=HealthResponse)
def healthz() -> HealthResponse:
    return HealthResponse(status="ok")


@app.get("/metrics")
def metrics() -> str:
    return "# placeholder metrics\n"


@app.post("/generate", response_model=GenerationResponse)
def generate(payload: GenerationRequest) -> GenerationResponse:
    tokenizer, model = get_model()
    max_new_tokens = payload.max_new_tokens or MAX_NEW_TOKENS_DEFAULT
    inputs = tokenizer(payload.prompt, return_tensors="pt")
    with torch.inference_mode():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=True,
            temperature=TEMPERATURE,
            top_p=TOP_P,
            pad_token_id=tokenizer.pad_token_id,
        )
    decoded = tokenizer.decode(outputs[0], skip_special_tokens=True)
    completion = decoded[len(payload.prompt) :].strip()
    return GenerationResponse(text=completion or decoded)
