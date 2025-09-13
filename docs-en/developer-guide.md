# Developer Guide

This document serves as a guide for developers who wish to understand and contribute to the internal structure of the Ollama document translator.

## Project Structure

```
ollama-doc-translator/
├── action.yml              # GitHub Action Metadata
├── entrypoint.py          # Main Execution Script
├── Dockerfile             # Docker Container Definition
├── translate-local.py     # Local test script
├── examples/              # Usage example
│   ├── basic-usage.yml
│   └── advanced-usage.yml
├── docs/                  # Please provide the Korean text you would like translated.
└── README.md             # Project document
```

## Core Components

### 1. GitHub Action Definition (action.yml)

Defines the metadata for an Action available on the GitHub Marketplace:

```python
def main():
    # Reading environment variables
    # 2. Verify Ollama Server Connection
    # 3. Verify Model Availability
    # 4. Search for Markdown files
    # 5. Translation processing
    # 6. PR Creation
```

### 2. Main Execution Logic (entrypoint.py)

Python script responsible for the core logic of the Action:

```python
def main():
    # 1. Read environment variables
    # 2. Verify Ollama server connection
    # 3. Check model availability
    # 4. Search for markdown files
    # 5. Translation processing
    # 6. Create PR

### 3. Docker Container (Dockerfile)

Provides an isolated environment to execute actions:

```dockerfile
FROM python:3.11-slim
# Ollama, GitHub CLI, Installation of Python Dependencies
COPY entrypoint.py /entrypoint.py
ENTRYPOINT ["python", "/entrypoint.py"]
```

## API Design

### Ollama API Interface

```python
def translate_with_ollama(text, model="exaone3.5:7.8b"):
    """
    Ollama APIIt seems there might be a typo or missing text in your request as "를" alone does not provide enough context for translation. Could you please provide the full Korean text you would like translated? Using Please provide the Korean text you would like translated. Translation
    
    Args:
        text (str): Translation needed Please provide the Korean text you would like translated. Please provide the Korean text you would like translated.
        model (str): To use Ollama Model Name
        
    Returns:
        str: Translated It seems there might be a misunderstanding as no Korean text was provided for translation in your request. Could you please provide the Korean text you would like translated into English? Please provide the Korean text you would like translated.
    """
    payload = {
        "model": model,
        "prompt": f"Please provide the Korean text you would like translated. It seems there might be a misunderstanding as no Korean text was provided for translation in your request. Could you please provide the Korean text you would like translated into English? Translation: {text}",
        "stream": False
    }
    response = requests.post(f"{OLLAMA_URL}/api/generate", json=payload)
    return response.json()['response']
```

### File Processing Pipeline

1. **File Discovery**: Search for markdown files using glob patterns
2. **Content Segmentation**: Segment large files using smart chunking
3. **Translation Processing**: Sequentially translate each chunk
4. **Result Merging**: Reassemble translated chunks using smart joining
5. **File Saving**: Save translated content to the target directory

## Smart Chunking System

### Chunking Strategy Overview

The system employs a hierarchical chunking strategy to efficiently process large documents:

```python
def split_markdown_by_sections(content: str, max_tokens: int = None) -> list:
    """Section Foundation Markdown Division - Meaning Unit Preservation"""
    # 1. Heading Hierarchical Structure Analysis (H1-H6)
    # 2. Tracking Code Block Status (``` ~ ``` preserved)
    # Maintaining semantic units within token limits.
    # 4. Preservation of Contextual Information (Upper Heading Path)
```

### Core Features

#### 1. Section Recognition Splitting
- **Heading Hierarchy**: H1-H2 always act as splitting boundaries, H3 split if over 200 tokens
- **Semantic Preservation**: Even small sections are maintained independently for completeness
- **Context Tracking**: Each chunk retains information about the parent heading path

#### 2. Code Block Preservation
```python
# Code block detection and preservation logic
if line_stripped.startswith('```'):
    if not in_code_block:
        in_code_block = True
        code_block_fence = line_stripped[:3]
    elif line_stripped.startswith(code_block_fence):
        in_code_block = False
        
# Do not split within the code block.
if not in_code_block and should_split_here:
    # Chunk splitting execution
```

#### 3. Smart Join (Smart Join)
Prevent unnecessary line breaks when reassembling translated chunks:

```python
def smart_join_chunks(chunks: list) -> str:
    """Continuous Number List Between Unnecessary Line break Removal"""
    # Number list pattern detection: "- Item 288
    # Use single line breaks for consecutive numbering.
    # General content uses basic separators.
```

### Token Calculation System

#### Accurate Token Calculation
```python
def count_tokens(text: str) -> int:
    """By language Characteristics Considered Token Calculation"""
    try:
        # Use of the tiktoken library (preferred)
        return len(tiktoken.encoding_for_model("gpt-3.5-turbo").encode(text))
    except:
        # Fallback: Language Estimation
        korean_chars = len(re.findall(r'[The provided text "가" is incomplete for translation as it appears to be just a Korean letter without context. Could you please provide more text for translation?-Hehe 😊]', text))
        code_chars = len(re.findall(r'[`{}()[\];]', text))
        other_chars = len(text) - korean_chars - code_chars
        
        return int(korean_chars * 0.5 + code_chars * 0.8 + other_chars * 0.3)
```

#### Safety Margin Calculation
```python
def calculate_safe_input_tokens(context_length: int) -> int:
    """Translation Prompt and Output Buffer Considered Safety Token Water"""
    prompt_overhead = 200  # System Prompt + Instructions
    output_reserve = int(context_length * 0.4)  # Output space 40%
    safety_margin = 100    # Additional Safety Margin
    
    return context_length - prompt_overhead - output_reserve - safety_margin
```

## Debug System

### Automatic Debug File Generation

```python
# Check Debug File
def save_debug_chunks(input_path: str, chunks: list):
    """Chunk by chunk Analysis File Creation"""
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
    """Original text not provided. Please provide the Korean text you would like translated.-Translation Comparison File Creation"""
    # debug_originals/filename_original_001.md
    # debug_translations/filename_translated_001.md  
    # debug_comparisons/filename_comparison_001.md
```

### Enable Debug Mode

Control detailed debug information output via environment variables:

```bash
# Activate debug mode
export INPUT_DEBUG_MODE=true

# Additional output upon execution:
# 📦 Created 15 token-aware chunks
# 🔄 [1/15] Translating chunk (245 tokens)...
# 🐛 Saved debug files for chunk 1 (original/translated/comparison)
```

## Setting Up the Development Environment

### Local Development Environment

1. **Install Essential Tools**```
# Python Dependencies
pip install requests

# Ollama Installation
curl -fsSL https://ollama.com/install.sh | sh

# Download Test Model
ollama pull exaone3.5:7.8b
```**Execution of development scripts**:
   ```bash
   # Local Test
   python translate-local.py
   
   # Docker Test
   docker build -t ollama-translator .
   docker run --network host ollama-translator
   ```

### Test environment

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
        result = translate_with_ollama("Hello")
        self.assertEqual(result, "Hello World")
```

## Extensibility

### Adding New Languages

To support additional language pairs, modify the following:

```python
def get_translation_prompt(text, source_lang="ko", target_lang="en"):
    prompts = {
        ("ko", "en"): f"Next Korean to English translation requested, but no text provided beyond "한국어를". Please provide the Korean text you would like translated. Please provide the Korean text you would like translated into English. Translation: {text}",
        ("ko", "ja"): f"Next Korean text not provided beyond "한국어를". Please provide the full Korean text you would like translated. It seems there might be a misunderstanding in your request as it ends abruptly with "일본어로" which means "in Japanese" in English, but no Korean text was provided for translation into Japanese. Could you please provide the Korean text you would like translated? If the intention was to request a translation into Japanese instead, please clarify or provide the Korean text. Translation: {text}",
        ("en", "ko"): f"Translate the following English to Korean: {text}"
    }
    return prompts.get((source_lang, target_lang))
```

### Supporting New File Formats

Currently, only Markdown is supported, but other formats can be added as well:

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
       - Accuracy of specialized terms
       - Natural English expression
       
       Original: {text}
       Translation:
       """
   ```

2. **Post-Processing Improvement**:
   ```python
   def post_process_translation(translated_text):
       # Restore Markdown formatting
       translated_text = fix_markdown_formatting(translated_text)
       
       # Verify consistency of specialized terms
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
# Adherence to PEP 8 guidelines
# Function Name: snake_case
# Class Name: PascalCase
# Constant: UPPER_CASE

def translate_text(source_text: str, model_name: str) -> str:
    """
    Please provide the Korean text you would like translated. I translate..
    
    Args:
        source_text: Translation needed Original text not provided. Please provide the Korean text you would like translated. Please provide the Korean text you would like translated.
        model_name: To use Model Name
        
    Returns:
        Translated Please provide the Korean text you would like translated.
        
    Raises:
        TranslationError: Translation Failure City Occurrence
    """
    pass
```

### Commit Message Conventions

```
feat: New Function Additional
fix: Bug Revision
docs: Document Modification
style: Code Style Change
refactor: Code Refactoring
test: Test Code Additional
chore: Other Work

Example:
feat: Japanese Translation Support Additional
fix: Markdown Table Format Preservation Problem Solution
docs: API How to use it Example Additional
```

### Pull Request Process

1. **Issue Creation**: Create an issue before developing a new feature or bug fix
2. **Branch Creation**Use `feature/Function Name` or `fix/Bug ID` format for entries.**Code Writing**: Include test code
4. **PR Creation**: Create a PR with detailed description
5. **Review Process**### Translation

```python
# tests/test_translation.py
def test_korean_to_english_translation():
    """Korean-English Translation Test"""
    korean_text = "Hello. Hello!."
    expected_english = "Hello. Nice to meet you."
    
    result = translate_with_ollama(korean_text)
    
    # Verify reasonable output even if not exact translation
    assert "hello" in result.lower()
    assert len(result) > 0

def test_markdown_preservation():
    """Markdown Format Preservation Test"""
    markdown_text = "# Title
```**Bold text**It seems there might be some confusion in your request as the provided text "It seems there might be a typo or incomplete input as "입니다" alone translates to "is" or "it is" in English without additional context. Could you please provide the full text you would like translated?." translates directly to "It is." in English, but the subsequent code snippet appears unrelated to the translation task and contains incomplete assertions. Here is the translation:

"It is.**" in result
```

### Document Update

When adding new features, ensure the following documents are updated:

- `README.md`: Basic Usage
- `action.yml`: New Input/Output Parameters
- `docs/`: Detailed Guide Documentation
- `examples/`: Usage Examples

## Deployment Process

### Version Control

Use Semantic Versioning:

- `MAJOR`: Changes to incompatible API
- `MINOR`: Addition of features compatible with previous versions
- `PATCH`: Fixes for bugs compatible with previous versions

### Release Procedure

1. **Create Version Tag**:
   ```bash
   git tag -a v1.2.0 -m "Release v1.2.0"
   git push origin v1.2.0
   ```

2. **Create GitHub Release**:
   - Automatically builds Docker images
   - Automatically updates Marketplace

3. **Update Documentation**:
   - Update version information in README.md
   - Update CHANGELOG.md

Thank you for your contribution! Feel free to ask questions via issues or discussions if you have any inquiries.

---

> **⚠️ 이 문서는 AI로 번역된 문서입니다.**
>
> **⚠️ This document has been translated by AI.**