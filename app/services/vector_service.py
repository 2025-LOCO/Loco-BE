# app/services/vector_service.py
import os
import numpy as np
from typing import Optional
from sentence_transformers import SentenceTransformer

# 캐시 경로 (huggingface-cli download 위치와 동일)
HF_HOME = os.environ.get("HF_HOME", "/opt/hf-cache")
LOCAL_REPO = os.path.join(HF_HOME, "jhgan/ko-sroberta-multitask")

_model: Optional[SentenceTransformer] = None

def _get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        # 토크나이저 병렬 경고 억제
        os.environ["TOKENIZERS_PARALLELISM"] = "false"
        # 로컬 디렉터리만 사용 (온라인 접근 금지)
        _model = SentenceTransformer(
            LOCAL_REPO,
            device="cpu",        # t3.micro에서는 CPU 고정 권장
            cache_folder=HF_HOME # 내부 캐시도 동일 경로 사용
        )
    return _model

def text_to_vector(text: str) -> np.ndarray:
    """입력 텍스트를 임베딩 벡터로 변환"""
    model = _get_model()
    emb = model.encode(text, normalize_embeddings=True)  # L2 정규화
    return np.array(emb, dtype=np.float32)