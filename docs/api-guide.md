# API 가이드

## 개요

이 문서는 Ollama API를 사용하여 텍스트 번역을 수행하는 방법에 대한 가이드입니다.

## 기본 설정

### 1. Ollama 설치

먼저 시스템에 Ollama를 설치해야 합니다:

```bash
# Windows
winget install Ollama.Ollama

# macOS
brew install ollama

# Linux
curl -fsSL https://ollama.com/install.sh | sh
```

### 2. 모델 다운로드

번역에 사용할 exaone3.5:7.8b 모델을 다운로드합니다:

```bash
ollama pull exaone3.5:7.8b
```

## API 사용법

### 기본 요청

```bash
curl -X POST http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "model": "exaone3.5:7.8b",
    "prompt": "다음 한국어 텍스트를 영어로 번역해주세요: 안녕하세요",
    "stream": false
  }'
```

### 응답 형식

```json
{
  "model": "exaone3.5:7.8b",
  "created_at": "2023-08-04T08:52:19.385406455-07:00",
  "response": "Hello",
  "done": true
}
```

## 번역 품질 향상 팁

1. **컨텍스트 제공**: 번역할 텍스트의 맥락을 함께 제공
2. **전문 용어 처리**: 기술 용어는 별도로 정의 제공
3. **일관성 유지**: 동일한 용어는 항상 같은 번역 사용

## 주의사항

- 로컬 환경에서만 동작합니다
- 인터넷 연결이 필요하지 않습니다
- 모델 크기에 따라 충분한 메모리가 필요합니다