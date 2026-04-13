# vLLM 설정 가이드

## vLLM 소개
vLLM은 고성능 LLM 추론 엔진으로 PagedAttention 기술을 사용하여 대규모 언어 모델을 효율적으로 서빙합니다.

## 설치 방법

### 옵션 1: pip로 설치
```bash
# 기본 설치
pip install vllm

# GPU 지원 설치 (CUDA 12.1+)
pip install vllm --extra-index-url https://pypi.nvidia.com

# 모든 기능 포함 설치
pip install "vllm[all]"
```

### 옵션 2: Docker로 설치
```bash
# 공식 Docker 이미지
docker run --runtime nvidia --gpus all \
  -v ~/.cache/huggingface:/root/.cache/huggingface \
  -p 8000:8000 \
  --ipc=host \
  vllm/vllm-openai:latest \
  --model meta-llama/Llama-3.2-3B-Instruct
```

### 옵션 3: 소스에서 빌드
```bash
git clone https://github.com/vllm-project/vllm.git
cd vllm
pip install -e .  # 개발 모드 설치
```

## 기본 서버 실행

### 로컬 모델로 실행
```bash
# 기본 실행 (포트 8000)
python -m vllm.entrypoints.openai.api_server \
  --model meta-llama/Llama-3.2-3B-Instruct \
  --port 8000

# GPU 메모리 제한 설정
python -m vllm.entrypoints.openai.api_server \
  --model meta-llama/Llama-3.2-3B-Instruct \
  --gpu-memory-utilization 0.9 \
  --max-model-len 4096

# 양자화 모델 실행
python -m vllm.entrypoints.openai.api_server \
  --model TheBloke/Llama-3.2-3B-Instruct-AWQ \
  --quantization awq \
  --port 8000
```

### 여러 GPU 사용
```bash
# Tensor 병렬 처리
python -m vllm.entrypoints.openai.api_server \
  --model meta-llama/Llama-3.2-3B-Instruct \
  --tensor-parallel-size 2

# 파이프라인 병렬 처리
python -m vllm.entrypoints.openai.api_server \
  --model meta-llama/Llama-3.2-3B-Instruct \
  --pipeline-parallel-size 2
```

## OpenClaw와 연동

### 환경 변수 설정
```bash
# vLLM 서버 URL 설정
export VLLM_API_URL="http://localhost:8000/v1"

# 또는 OpenClaw 설정에 추가
openclaw config set models.providers.vllm.url "http://localhost:8000/v1"
openclaw config set models.providers.vllm.apiKey "optional-api-key"
```

### 모델 구성
```json
{
  "models": {
    "providers": {
      "vllm": {
        "url": "http://localhost:8000/v1",
        "models": {
          "llama-3.2-3b": {
            "id": "meta-llama/Llama-3.2-3B-Instruct",
            "contextWindow": 8192,
            "maxTokens": 4096
          }
        }
      }
    }
  }
}
```

## 테스트

### 서버 상태 확인
```bash
# 건강 상태 확인
curl http://localhost:8000/health

# 사용 가능한 모델 확인
curl http://localhost:8000/v1/models

# OpenAI 호환 API 테스트
curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "meta-llama/Llama-3.2-3B-Instruct",
    "messages": [
      {"role": "user", "content": "Hello, how are you?"}
    ],
    "max_tokens": 100
  }'
```

### OpenClaw에서 테스트
```bash
# vLLM 모델로 에이전트 실행
openclaw agent --model vllm:llama-3.2-3b --message "테스트 메시지"

# 또는 세션에서 모델 변경
openclaw config set session.model vllm:llama-3.2-3b
```

## 고급 설정

### 배치 처리 최적화
```bash
python -m vllm.entrypoints.openai.api_server \
  --model meta-llama/Llama-3.2-3B-Instruct \
  --max-num-batched-tokens 4096 \
  --max-num-seqs 256 \
  --batch-max-tokens 4096
```

### 로깅 및 모니터링
```bash
python -m vllm.entrypoints.openai.api_server \
  --model meta-llama/Llama-3.2-3B-Instruct \
  --log-level debug \
  --disable-log-requests \
  --disable-log-stats
```

### 추론 파라미터 튜닝
```bash
python -m vllm.entrypoints.openai.api_server \
  --model meta-llama/Llama-3.2-3B-Instruct \
  --temperature 0.7 \
  --top-p 0.9 \
  --top-k 50 \
  --repetition-penalty 1.1 \
  --length-penalty 1.0
```

## 문제 해결

### 일반적인 문제
1. **GPU 메모리 부족**: `--gpu-memory-utilization` 값 줄이기
2. **모델 로딩 실패**: Hugging Face 토큰 설정 확인
3. **느린 응답**: `--max-num-batched-tokens` 값 조정
4. **연결 오류**: 포트 충돌 확인 (기본: 8000)

### 로그 확인
```bash
# 상세 로깅 활성화
python -m vllm.entrypoints.openai.api_server \
  --model meta-llama/Llama-3.2-3B-Instruct \
  --log-level debug

# 로그 파일로 출력
python -m vllm.entrypoints.openai.api_server \
  --model meta-llama/Llama-3.2-3B-Instruct \
  --log-file vllm.log
```

## 성능 벤치마크
```bash
# 벤치마크 모드 실행
python -m vllm.entrypoints.openai.api_server \
  --model meta-llama/Llama-3.2-3B-Instruct \
  --benchmark

# 또는 별도 벤치마크 도구 사용
python -m vllm.benchmarks.serving \
  --model meta-llama/Llama-3.2-3B-Instruct \
  --num-prompts 100 \
  --request-rate 10
```

## 참고 자료
- vLLM 공식 문서: https://docs.vllm.ai
- GitHub 저장소: https://github.com/vllm-project/vllm
- OpenAI 호환 API: https://docs.vllm.ai/en/latest/serving/openai_compatible_server.html
- 성능 튜닝 가이드: https://docs.vllm.ai/en/latest/performance/tuning.html