# Developer Guide

This document serves as a guide for developers who wish to understand and contribute to the internal structure of Ollama Document Translator.

## Project Structure

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

## Core Components

### 1. GitHub Action Definition (action.yml)

Defines the metadata for an Action available on the GitHub Marketplace:

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

### 2. Main Execution Logic (entrypoint.py)

Python script responsible for the core logic of the Action:

```python
def main():
    # 1. 환경 변수 읽기
    # 2. Ollama 서버 연결 확인
    # 3. 모델 가용성 확인
    # 4. 마크다운 파일 검색
    # 5. 번역 처리
    # 6. PR 생성
```

### 3. Docker Container (Dockerfile)

Provides an isolated environment to execute actions:

```dockerfile
FROM python:3.11-slim
# Ollama, GitHub CLI, Python 의존성 설치
COPY entrypoint.py /entrypoint.py
ENTRYPOINT ["python", "/entrypoint.py"]
```

## API Design

### Ollama API Interface

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

### File Processing Pipeline

1. **File Discovery**: Search for markdown files using glob patterns
2. **Content Segmentation**: Divide large files into chunks using smart splitting
3. **Translation Processing**: Sequentially translate each chunk
4. **Result Merging**: Reassemble translated chunks using smart joining
5. **File Saving**: Save the translated content to the target directory

## Smart Chunking System

### Chunking Strategy Overview

The system employs a hierarchical chunking strategy to efficiently process large documents:

```python
def split_markdown_by_sections(content: str, max_tokens: int = None) -> list:
    """섹션 기반 마크다운 분할 - 의미 단위 보존"""
    # 1. 헤딩 계층 구조 분석 (H1-H6)
    # 2. 코드 블록 상태 추적 (``` ~ ``` 보존)
    # 3. 토큰 제한 내에서 의미 단위 유지
    # 4. 컨텍스트 정보 보존 (상위 헤딩 경로)
```

### Core Features

#### 1. Section Recognition Splitting
- **Heading Hierarchy**: H1-H2 always act as splitting boundaries, H3 split if over 200 tokens
- **Semantic Preservation**: Even small sections are maintained independently for completeness
- **Context Tracking**: Each chunk retains information about the parent heading path

#### 2. Code Block Preservation
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

#### 3. Smart Join (Smart Join)
Prevent unnecessary line breaks when reassembling translated chunks:

```python
def smart_join_chunks(chunks: list) -> str:
    """연속된 번호 목록 사이의 불필요한 줄바꿈 제거"""
    # 번호 목록 패턴 감지: "- 288. 항목"
    # 연속 번호시 단일 줄바꿈 사용
    # 일반 내용은 기본 분리자 사용
```
```

### Token Calculation System

#### Precise Token Calculation
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

#### Safety Margin Calculation
```python
def calculate_safe_input_tokens(context_length: int) -> int:
    """번역 프롬프트와 출력 버퍼 고려한 안전 토큰 수"""
    prompt_overhead = 200  # 시스템 프롬프트 + 지시사항
    output_reserve = int(context_length * 0.4)  # 출력 공간 40%
    safety_margin = 100    # 추가 안전 마진
    
    return context_length - prompt_overhead - output_reserve - safety_margin
```

## Debug System

### Automatic Debug File Generation

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

### Translation Comparison System

```python
def save_debug_translation(input_path: str, chunk_index: int, 
                         original_chunk: str, translated_chunk: str):
    """원본-번역 비교 파일 생성"""
    # debug_originals/filename_original_001.md
    # debug_translations/filename_translated_001.md  
    # debug_comparisons/filename_comparison_001.md
```

### Enable Debug Mode

Control detailed debug information output via environment variables:

```bash
# 디버그 모드 활성화
export INPUT_DEBUG_MODE=true

# 실행시 추가 출력:
# 📦 Created 15 token-aware chunks
# 🔄 [1/15] Translating chunk (245 tokens)...
# 🐛 Saved debug files for chunk 1 (original/translated/comparison)
```

## Setting Up the Development Environment

### Local Development Environment

1. **Install Required Tools**:
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
        # Mock API response
        mock_response = Mock()
        mock_response.json.return_value = {'response': 'Hello World'}
        mock_post.return_value = mock_response
        
        # Test translation function
        result = translate_with_ollama("안녕하세요")
        self.assertEqual(result, "Hello World")
```

## Extensibility

### Adding New Languages

To support additional language pairs, modify the following:

```python
def get_translation_prompt(text, source_lang="ko", target_lang="en"):
    prompts = {
        ("ko", "en"): f"다음 한국어를 영어로 번역: {text}",
        ("ko", "ja"): f"다음 한국어를 일본어로 번역: {text}",
        ("en", "ko"): f"Translate the following English to Korean: {text}"
    }
    return prompts.get((source_lang, target_lang))
```

### Supporting New File Formats

Currently, only Markdown is supported, but other formats can be added:

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

### Improving Translation Quality

1. **Prompt Engineering**:
   ```python
   def create_context_aware_prompt(text, context=""):
       return f"""
       Context: {context}
       
       Please translate the following technical document into English while maintaining:
       - Markdown format
       - Accuracy of specialized terminology first
       - Natural English expression
       
       Original: {text}
       Translation:
       """
   ```

2. **Post-Processing Improvements**:
   ```python
   def post_process_translation(translated_text):
       # Restore Markdown formatting
       translated_text = fix_markdown_formatting(translated_text)
       
       # Verify consistency of specialized terminology
       translated_text = apply_terminology_rules(translated_text)
       
       return translated_text
   ```

## Performance Optimization

### Asynchronous Processing

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

### Caching System

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

## Contribution Guide

### Coding Style

Coding standards used in the project:

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

### Commit Message Guidelines

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

### Pull Request Process

1. **Issue Creation**: Create an issue before developing a new feature or bug fix
2. **Branch Creation**: Use `feature/기능명` or `fix/버그명` format
3. **Code Writing**: Include test code
4. **PR Creation**: Create a pull request with detailed description
5. **Review Process**: Merge after code review

### Test Writing

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

### Document Updates

When adding new features, ensure the following documents are updated:

- `README.md`: Basic Usage
- `action.yml`: New Input/Output Parameters
- `docs/`: Detailed Guide Documentation
- `examples/`: Usage Examples

## Deployment Process

### Version Control

Use Semantic Versioning:

- `MAJOR`: API changes that are incompatible
- `MINOR`: Addition of features compatible with previous versions
- `PATCH`: Bug fixes compatible with previous versions

### Release Procedure

1. **Create Version Tag**:
   ```bash
   git tag -a v1.2.0 -m "Release v1.2.0"
   git push origin v1.2.0
   ```

2. **Create GitHub Release**:
   - Automatically builds Docker images
   - Automatically updates Marketplace listings

3. **Update Documentation**:
   - Update version information in README.md
   - Update CHANGELOG.md

Thank you for your contribution! Feel free to ask questions via issues or discussions if you have any inquiries.

---

> **⚠️ 이 문서는 AI로 번역된 문서입니다.**
>
> **⚠️ This document has been translated by AI.**