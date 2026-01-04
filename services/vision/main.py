import base64
import io
import os

import torch
from fastapi import FastAPI
from PIL import Image
from torchvision.models import MobileNet_V3_Small_Weights, mobilenet_v3_small
from services.shared.schemas import HealthResponse, VisionPrediction, VisionRequest, VisionResponse

app = FastAPI(title="vision")

TOP_K_DEFAULT = int(os.getenv("VISION_TOP_K", "3"))

_model = None
_preprocess = None
_labels: list[str] = []


def get_model() -> tuple[torch.nn.Module, callable, list[str]]:
    global _model, _preprocess, _labels
    if _model is None or _preprocess is None or not _labels:
        weights = MobileNet_V3_Small_Weights.DEFAULT
        _model = mobilenet_v3_small(weights=weights)
        _model.eval()
        _preprocess = weights.transforms()
        _labels = list(weights.meta["categories"])
    return _model, _preprocess, _labels


def decode_image(data: str) -> Image.Image:
    if "base64," in data:
        data = data.split("base64,", 1)[1]
    raw = base64.b64decode(data)
    return Image.open(io.BytesIO(raw)).convert("RGB")


@app.get("/healthz", response_model=HealthResponse)
def healthz() -> HealthResponse:
    return HealthResponse(status="ok")


@app.get("/metrics")
def metrics() -> str:
    return "# placeholder metrics\n"


@app.post("/classify-image", response_model=VisionResponse)
def classify_image(payload: VisionRequest) -> VisionResponse:
    model, preprocess, labels = get_model()
    image = decode_image(payload.image_base64)
    input_tensor = preprocess(image).unsqueeze(0)
    with torch.inference_mode():
        logits = model(input_tensor)
        probs = torch.softmax(logits, dim=1).squeeze(0)
    top_k = payload.top_k or TOP_K_DEFAULT
    top_scores, top_indices = torch.topk(probs, k=top_k)
    predictions = [
        VisionPrediction(label=labels[int(idx)], score=float(score))
        for idx, score in zip(top_indices, top_scores)
    ]
    return VisionResponse(predictions=predictions)
