# app/services/vector_service.py
from sentence_transformers import SentenceTransformer

# 한국어 특화 모델 (최초 실행 시 자동으로 다운로드 됩니다)
model = SentenceTransformer('jhgan/ko-sroberta-multitask')

def text_to_vector(text: str):
    """주어진 텍스트를 벡터 임베딩으로 변환합니다."""
    return model.encode(text)
