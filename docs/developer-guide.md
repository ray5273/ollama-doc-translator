# 개발자 가이드

이 문서는 Ollama 문서 번역기의 내부 구조를 이해하고 기여하고자 하는 개발자를 위한 가이드입니다.

## 프로젝트 구조

```
ollama-doc-translator/
├── action.yml              # GitHub Action 메타데이터
├── entrypoint.py          # 메인 실행 스크립트
├── Dockerfile             # Docker 컨테이너 정의
├── translate-local.py     # 로컬 테스트 스크립트
├── examples/              # 사용 예제
│   ├── basic-usage.yml
│   └── advanced-usage.yml
├── docs/                  # 한국어 문서
└── README.md             # 프로젝트 문서
```

## 핵심 컴포넌트

### 1. GitHub Action 정의 (action.yml)

GitHub Marketplace에서 사용할 수 있는 Action의 메타데이터를 정의합니다:

```yaml
name: 'Ollama Korean to English Translator'
description: '로컬 Ollama API를 사용한 한영 번역'
inputs:
  source-dir:
    description: '번역할 한국어 문서 디렉토리'
    default: 'docs'
outputs:
  translated-files:
    description: '번역된 파일 수'
```

### 2. 메인 실행 로직 (entrypoint.py)

Action의 핵심 로직을 담당하는 Python 스크립트:

```python
def main():
    # 1. 환경 변수 읽기
    # 2. Ollama 서버 연결 확인
    # 3. 모델 가용성 확인
    # 4. 마크다운 파일 검색
    # 5. 번역 처리
    # 6. PR 생성
```

### 3. Docker 컨테이너 (Dockerfile)

Action을 실행하기 위한 격리된 환경을 제공:

```dockerfile
FROM python:3.11-slim
# Ollama, GitHub CLI, Python 의존성 설치
COPY entrypoint.py /entrypoint.py
ENTRYPOINT ["python", "/entrypoint.py"]
```

## API 설계

### Ollama API 인터페이스

```python
def translate_with_ollama(text, model="exaone3.5:7.8b"):
    """
    Ollama API를 사용하여 텍스트 번역
    
    Args:
        text (str): 번역할 한국어 텍스트
        model (str): 사용할 Ollama 모델명
        
    Returns:
        str: 번역된 영어 텍스트
    """
    payload = {
        "model": model,
        "prompt": f"다음을 영어로 번역: {text}",
        "stream": False
    }
    response = requests.post(f"{OLLAMA_URL}/api/generate", json=payload)
    return response.json()['response']
```

### 파일 처리 파이프라인

1. **파일 발견**: glob 패턴으로 마크다운 파일 검색
2. **내용 분할**: 스마트 청킹으로 큰 파일을 청크로 분할
3. **번역 처리**: 각 청크를 순차적으로 번역
4. **결과 병합**: 번역된 청크들을 스마트 조인으로 다시 합치기
5. **파일 저장**: 번역된 내용을 대상 디렉토리에 저장

## 스마트 청킹 시스템

### 청킹 전략 개요

시스템은 대용량 문서를 효율적으로 처리하기 위해 계층적 청킹 전략을 사용합니다:

```python
def split_markdown_by_sections(content: str, max_tokens: int = None) -> list:
    """섹션 기반 마크다운 분할 - 의미 단위 보존"""
    # 1. 헤딩 계층 구조 분석 (H1-H6)
    # 2. 코드 블록 상태 추적 (``` ~ ``` 보존)
    # 3. 토큰 제한 내에서 의미 단위 유지
    # 4. 컨텍스트 정보 보존 (상위 헤딩 경로)
```

### 핵심 기능

#### 1. 섹션 인식 분할
- **헤딩 계층**: H1-H2는 항상 분할 경계, H3는 200토큰 이상시 분할
- **의미 보존**: 작은 섹션도 완전성을 위해 독립적으로 유지
- **컨텍스트 추적**: 각 청크는 상위 헤딩 경로 정보 보유

#### 2. 코드 블록 보존
```python
# 코드 블록 감지 및 보존 로직
if line_stripped.startswith('```'):
    if not in_code_block:
        in_code_block = True
        code_block_fence = line_stripped[:3]
    elif line_stripped.startswith(code_block_fence):
        in_code_block = False
        
# 코드 블록 내부에서는 분할하지 않음
if not in_code_block and should_split_here:
    # 청크 분할 실행
```

#### 3. 스마트 조인 (Smart Join)
번역된 청크들을 다시 합칠 때 불필요한 줄바꿈 방지:

```python
def smart_join_chunks(chunks: list) -> str:
    """연속된 번호 목록 사이의 불필요한 줄바꿈 제거"""
    # 번호 목록 패턴 감지: "- 288. 항목"
    # 연속 번호시 단일 줄바꿈 사용
    # 일반 내용은 기본 분리자 사용
```

### 토큰 계산 시스템

#### 정확한 토큰 계산
```python
def count_tokens(text: str) -> int:
    """언어별 특성 고려한 토큰 계산"""
    try:
        # tiktoken 라이브러리 사용 (선호)
        return len(tiktoken.encoding_for_model("gpt-3.5-turbo").encode(text))
    except:
        # 폴백: 언어별 추정
        korean_chars = len(re.findall(r'[가-힣]', text))
        code_chars = len(re.findall(r'[`{}()[\];]', text))
        other_chars = len(text) - korean_chars - code_chars
        
        return int(korean_chars * 0.5 + code_chars * 0.8 + other_chars * 0.3)
```

#### 안전 마진 계산
```python
def calculate_safe_input_tokens(context_length: int) -> int:
    """번역 프롬프트와 출력 버퍼 고려한 안전 토큰 수"""
    prompt_overhead = 200  # 시스템 프롬프트 + 지시사항
    output_reserve = int(context_length * 0.4)  # 출력 공간 40%
    safety_margin = 100    # 추가 안전 마진
    
    return context_length - prompt_overhead - output_reserve - safety_margin
```

## 디버그 시스템

### 자동 디버그 파일 생성

```python
# 청킹 디버그 파일
def save_debug_chunks(input_path: str, chunks: list):
    """청크별 분석 파일 생성"""
    for i, chunk in enumerate(chunks):
        # debug_chunks/filename_chunk_001.md
        metadata = f"""<!-- DEBUG CHUNK {i+1}/{len(chunks)} -->
<!-- Tokens: {count_tokens(chunk)} -->
<!-- Characters: {len(chunk)} -->
<!-- Source: {input_path} -->"""
```

### 번역 비교 시스템

```python
def save_debug_translation(input_path: str, chunk_index: int, 
                         original_chunk: str, translated_chunk: str):
    """원본-번역 비교 파일 생성"""
    # debug_originals/filename_original_001.md
    # debug_translations/filename_translated_001.md  
    # debug_comparisons/filename_comparison_001.md
```

### 디버그 모드 활성화

환경 변수로 상세 디버그 정보 출력 제어:

```bash
# 디버그 모드 활성화
export INPUT_DEBUG_MODE=true

# 실행시 추가 출력:
# 📦 Created 15 token-aware chunks
# 🔄 [1/15] Translating chunk (245 tokens)...
# 🐛 Saved debug files for chunk 1 (original/translated/comparison)
```

## 개발 환경 설정

### 로컬 개발 환경

1. **필수 도구 설치**:
   ```bash
   # Python 의존성
   pip install requests
   
   # Ollama 설치
   curl -fsSL https://ollama.com/install.sh | sh
   
   # 테스트 모델 다운로드
   ollama pull exaone3.5:7.8b
   ```

2. **개발용 스크립트 실행**:
   ```bash
   # 로컬 테스트
   python translate-local.py
   
   # Docker 테스트
   docker build -t ollama-translator .
   docker run --network host ollama-translator
   ```

### 테스트 환경

```python
# test_translation.py
import unittest
from unittest.mock import patch, Mock

class TestTranslation(unittest.TestCase):
    @patch('requests.post')
    def test_translate_with_ollama(self, mock_post):
        # Mock API 응답
        mock_response = Mock()
        mock_response.json.return_value = {'response': 'Hello World'}
        mock_post.return_value = mock_response
        
        # 번역 함수 테스트
        result = translate_with_ollama("안녕하세요")
        self.assertEqual(result, "Hello World")
```

## 확장 가능성

### 새로운 언어 추가

다른 언어 쌍을 지원하려면 다음을 수정:

```python
def get_translation_prompt(text, source_lang="ko", target_lang="en"):
    prompts = {
        ("ko", "en"): f"다음 한국어를 영어로 번역: {text}",
        ("ko", "ja"): f"다음 한국어를 일본어로 번역: {text}",
        ("en", "ko"): f"Translate the following English to Korean: {text}"
    }
    return prompts.get((source_lang, target_lang))
```

### 새로운 파일 형식 지원

현재는 마크다운만 지원하지만 다른 형식도 추가 가능:

```python
def process_file(file_path):
    extension = file_path.suffix.lower()
    
    if extension == '.md':
        return process_markdown_file(file_path)
    elif extension == '.rst':
        return process_rst_file(file_path)
    elif extension == '.tex':
        return process_latex_file(file_path)
```

### 번역 품질 개선

1. **프롬프트 엔지니어링**:
   ```python
   def create_context_aware_prompt(text, context=""):
       return f"""
       컨텍스트: {context}
       
       다음 기술 문서를 영어로 번역해주세요:
       - 마크다운 형식 유지
       - 전문 용어 정확성 우선
       - 자연스러운 영어 표현
       
       원문: {text}
       번역:
       """
   ```

2. **후처리 개선**:
   ```python
   def post_process_translation(translated_text):
       # 마크다운 형식 복구
       translated_text = fix_markdown_formatting(translated_text)
       
       # 전문 용어 일관성 확인
       translated_text = apply_terminology_rules(translated_text)
       
       return translated_text
   ```

## 성능 최적화

### 비동기 처리

```python
import asyncio
import aiohttp

async def translate_async(session, text):
    async with session.post(f"{OLLAMA_URL}/api/generate", 
                           json=payload) as response:
        result = await response.json()
        return result['response']

async def process_files_async(file_list):
    async with aiohttp.ClientSession() as session:
        tasks = [translate_async(session, content) 
                for content in file_list]
        return await asyncio.gather(*tasks)
```

### 캐싱 시스템

```python
import hashlib
import pickle
from pathlib import Path

class TranslationCache:
    def __init__(self, cache_dir=".translation_cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
    
    def get_cache_key(self, text, model):
        content = f"{text}:{model}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def get(self, text, model):
        cache_file = self.cache_dir / f"{self.get_cache_key(text, model)}.pkl"
        if cache_file.exists():
            with open(cache_file, 'rb') as f:
                return pickle.load(f)
        return None
    
    def set(self, text, model, translation):
        cache_file = self.cache_dir / f"{self.get_cache_key(text, model)}.pkl"
        with open(cache_file, 'wb') as f:
            pickle.dump(translation, f)
```

## 기여 가이드

### 코드 스타일

프로젝트에서 사용하는 코딩 표준:

```python
# PEP 8 준수
# 함수명: snake_case
# 클래스명: PascalCase
# 상수: UPPER_CASE

def translate_text(source_text: str, model_name: str) -> str:
    """
    텍스트를 번역합니다.
    
    Args:
        source_text: 번역할 원본 텍스트
        model_name: 사용할 모델명
        
    Returns:
        번역된 텍스트
        
    Raises:
        TranslationError: 번역 실패 시 발생
    """
    pass
```

### 커밋 메시지 규칙

```
feat: 새로운 기능 추가
fix: 버그 수정
docs: 문서 수정
style: 코드 스타일 변경
refactor: 코드 리팩토링
test: 테스트 코드 추가
chore: 기타 작업

예시:
feat: 일본어 번역 지원 추가
fix: 마크다운 테이블 형식 보존 문제 해결
docs: API 사용법 예제 추가
```

### Pull Request 프로세스

1. **이슈 생성**: 새로운 기능이나 버그 수정 전 이슈 생성
2. **브랜치 생성**: `feature/기능명` 또는 `fix/버그명` 형식
3. **코드 작성**: 테스트 코드 포함
4. **PR 생성**: 상세한 설명과 함께
5. **리뷰 진행**: 코드 리뷰 후 머지

### 테스트 작성

```python
# tests/test_translation.py
def test_korean_to_english_translation():
    """한국어-영어 번역 테스트"""
    korean_text = "안녕하세요. 반갑습니다."
    expected_english = "Hello. Nice to meet you."
    
    result = translate_with_ollama(korean_text)
    
    # 정확한 번역은 아니더라도 합리적인 결과인지 확인
    assert "hello" in result.lower()
    assert len(result) > 0

def test_markdown_preservation():
    """마크다운 형식 보존 테스트"""
    markdown_text = "# 제목\n\n**굵은 글씨** 입니다."
    
    result = translate_with_ollama(markdown_text)
    
    assert result.startswith("#")
    assert "**" in result
```

### 문서 업데이트

새로운 기능을 추가할 때는 반드시 다음 문서들을 업데이트:

- `README.md`: 기본 사용법
- `action.yml`: 새로운 입력/출력 파라미터
- `docs/`: 상세 가이드 문서
- `examples/`: 사용 예제

## 배포 프로세스

### 버전 관리

[Semantic Versioning](https://semver.org/) 사용:

- `MAJOR`: 호환되지 않는 API 변경
- `MINOR`: 하위 호환성 있는 기능 추가
- `PATCH`: 하위 호환성 있는 버그 수정

### 릴리스 절차

1. **버전 태그 생성**:
   ```bash
   git tag -a v1.2.0 -m "Release v1.2.0"
   git push origin v1.2.0
   ```

2. **GitHub Release 생성**:
   - 자동으로 Docker 이미지 빌드
   - Marketplace 자동 업데이트

3. **문서 업데이트**:
   - README.md의 버전 정보
   - CHANGELOG.md 업데이트

개발에 참여해주셔서 감사합니다! 궁금한 점이 있으시면 언제든지 이슈나 디스커션에 질문해주세요.