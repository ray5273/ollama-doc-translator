# Developer Guide

This document serves as a guide for developers who wish to understand and contribute to the internal structure of Ollama Document Translator.

## Project Structure

```
ollama-doc-translator/
├── action.yml              # GitHub Action metadata
├── entrypoint.py          # Main execution script
├── Dockerfile             # Docker container definition
├── translate-local.py     # Local test script
├── examples/              # Usage examples
│   ├── basic-usage.yml
│   └── advanced-usage.yml
├── docs/                  # Korean documentation
└── README.md             # Project documentation
```

## Core Components

### 1. GitHub Action Definition (action.yml)

Defines the metadata for an Action available on the GitHub Marketplace:

```yaml
name: 'Ollama Korean to English Translator'
description: 'Korean to English Translation using Local Ollama API'
inputs:
  source-dir:
    description: 'Directory containing Korean documents to translate'
    default: 'docs'
outputs:
  translated-files:
    description: 'Number of translated files'
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
    # 6. Create PR`
```

### 3. Docker Container (Dockerfile)

Provides an isolated environment for executing actions:

```dockerfile
FROM python:3.11-slim
# Install Ollama, GitHub CLI, Python dependencies
COPY entrypoint.py /entrypoint.py
ENTRYPOINT ["python", "/entrypoint.py"]
```

## API Design

### Ollama API Interface

```python
def translate_with_ollama(text, model="exaone3.5:7.8b"):
    """
    Translate text using Ollama API
    
    Args:
        text (str): Korean text to translate
        model (str): Ollama model name to use
        
    Returns:
        str: Translated English text
    """
    payload = {
        "model": model,
        "prompt": f"Translate the following to English: {text}",
        "stream": False
    }
    response = requests.post(f"{OLLAMA_URL}/api/generate", json=payload)
    return response.json()['response']
```

### File Processing Pipeline

1. **File Discovery**: Search for markdown files using glob patterns
2. **Content Segmentation**: Divide large files into chunks
3. **Translation Processing**: Sequentially translate each chunk
4. **Result Merging**: Combine translated chunks
5. **File Saving**: Save translated content to the target directory

## Setting Up the Development Environment

### Local Development Environment

1. **Install Essential Tools**:
   ```bash
   # Python Dependencies
   pip install requests
   
   # Ollama Installation
   curl -fsSL https://ollama.com/install.sh | sh
   
   # Download Test Model
   ollama pull exaone3.5:7.8b
   ```

2. **Run Development Scripts**:
   ```bash
   # Local Test
   python translate-local.py
   
   # Docker Test
   docker build -t ollama-translator .
   docker run --network host ollama-translator
   ```

### Test Environment

```python
# test_translation.py
import unittest
from unittest.mock import patch, Mock

class TestTranslation(unittest.TestCase):
    @patch('requests.post')
    def test_translate_with_ollama(self, mock_post):
        # Mock API Response
        mock_response = Mock()
        mock_response.json.return_value = {'response': 'Hello World'}
        mock_post.return_value = mock_response
        
        # Test Translation Function
        result = translate_with_ollama("안녕하세요")
        self.assertEqual(result, "Hello World")
```

## Extensibility

### Adding New Languages

To support additional language pairs, modify the following:

```python
def get_translation_prompt(text, source_lang="ko", target_lang="en"):
    prompts = {
        ("ko", "en"): f"Translate the following Korean to English: {text}",
        ("ko", "ja"): f"Translate the following Korean to Japanese: {text}",
        ("en", "ko"): f"Translate the following English to Korean: {text}"
    }
    return prompts.get((source_lang, target_lang))
```

### Supporting New File Formats

Currently only Markdown is supported, but other formats can be added:

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
       
       Please translate the following technical document into English:
       - Maintain Markdown format
       - Prioritize accuracy of specialized terminology
       - Use natural English expressions
       
       Original: {text}
       Translation:
       """
   ```

2. **Post-Processing Improvement**:
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
# PEP 8 Compliance
# Function names: snake_case
# Class names: PascalCase
# Constants: UPPER_CASE

def translate_text(source_text: str, model_name: str) -> str:
    """
    Translates text.
    
    Args:
        source_text: The original text to be translated
        model_name: The name of the model to use
        
    Returns:
        Translated text
        
    Raises:
        TranslationError: Raised upon translation failure
    """
    pass
```

### Commit Message Guidelines

```
feat: Add new feature
fix: Bug fix
docs: Documentation changes
style: Changes in code style
refactor: Code refactoring
test: Addition of test code
chore: Other tasks

Example:
feat: Add Japanese translation support
fix: Resolve issue with Markdown table formatting
docs: Add API usage examples
```

### Pull Request Process

1. **Issue Creation**: Create an issue before developing a new feature or bug fix
2. **Branch Creation**: Use `feature/기능명` or `fix/버그명` format
3. **Code Writing**: Include test code
4. **PR Creation**: With detailed description
5. **Review Process**: Merge after code review

### Test Writing

```python
# tests/test_translation.py
def test_korean_to_english_translation():
    """Korean-to-English Translation Test"""
    korean_text = "안녕하세요. 반갑습니다."
    expected_english = "Hello. Nice to meet you."
    
    result = translate_with_ollama(korean_text)
    
    # Check for reasonable result even if not exact translation
    assert "hello" in result.lower()
    assert len(result) > 0

def test_markdown_preservation():
    """Markdown Format Preservation Test"""
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

Use [Semantic Versioning](https://semver.org/):

- `MAJOR`: Changes incompatible with previous API versions
- `MINOR`: Addition of new features backward compatible
- `PATCH`: Fixes bugs backward compatible

### Release Procedure

1. **Create Version Tag**:
   ```bash
   git tag -a v1.2.0 -m "Release v1.2.0"
   git push origin v1.2.0
   ```

2. **Create GitHub Release**:
   - Automatically builds Docker image
   - Automatically updates Marketplace

3. **Update Documentation**:
   - Update version information in README.md
   - Update CHANGELOG.md

Thank you for your contribution! Feel free to ask questions via issues or discussions if you have any inquiries.

---

> **⚠️ 이 문서는 AI로 번역된 문서입니다.**
>
> **⚠️ This document has been translated by AI.**