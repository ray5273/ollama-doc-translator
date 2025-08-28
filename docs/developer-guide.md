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
2. **내용 분할**: 큰 파일을 청크로 분할
3. **번역 처리**: 각 청크를 순차적으로 번역
4. **결과 병합**: 번역된 청크들을 다시 합치기
5. **파일 저장**: 번역된 내용을 대상 디렉토리에 저장

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