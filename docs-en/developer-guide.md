# Developer Guide

This document is a guide for developers who wish to understand and contribute to the internal structure of the Ollama document translator.

## Project Structure

```
ollama-doc-translator/
├── action.yml              # GitHub Action metadata
├── entrypoint.py          # Main execution script
├── Dockerfile             # Docker container definition
├── translate-local.py     # Local testing script
├── examples/              # Usage examples
│   ├── basic-usage.yml
│   └── advanced-usage.yml
├── docs/                  # Korean language documentation
└── README.md             | Project documentation
```

## Core Components

### 1. GitHub Action Definition (action.yml)

Defines the metadata for the Action that can be used on GitHub Marketplace:

```yaml
name: 'Ollama Korean to English Translator'
description: 'Korean-English translation using local Ollama API'
inputs:
  source-dir:
    description: 'Directory containing Korean language documents to be translated'
    default: 'docs'
outputs:
  translated-files:
    description: 'Number of files that have been translated'
```

### 2. Main Execution Logic (entrypoint.py)

The Python script that handles the core logic of the Action:

```python
def main():
```

# 1. Reading Environment Variables

# 2. Checking Ollama Server Connection

# 3. Checking Model Availability

# 4. Searching for Markdown Files

# 5. Translation Processing

# 6. Creating a Pull Request
```

### 3. Docker Container (Dockerfile)

Provides an isolated environment for executing actions:

```dockerfile
FROM python:3.11-slim

# Installing Dependencies for Ollama, GitHub CLI, and Python
COPY entrypoint.py /entrypoint.py
ENTRYPOINT ["python", "/entrypoint.py"]

## API Design

### Ollama API Interface

```python
def translate_with_ollama(text, model="exaone3.5:7.8b"):
    """
    Translate text using the Ollama API.

    Args:
        text (str): Korean text to be translated
        model (str): Name of the Ollama model to use

    Returns:
        str: Translated English text
    """
    payload = {
        "model": model,
        "prompt": f"Translate the following into English: {text}",
        "stream": False
    }
    response = requests.post(f"{OLLAMA_URL}/api/generate", json=payload)
    return response.json['response']
```

### File Processing Pipeline

1. **File Detection**: Search for Markdown files using glob patterns.
2. **Content Splitting**: Divide large files into chunks.
3. **Translation Processing**: Translate each chunk sequentially.
4. **Result Merging**: Combine the translated chunks back together.
5. **File Saving**: Save the translated content in the target directory.

## Development Environment Setup

### Local Development Environment

1. **Required Tools Installation**:
```bash
```

# Python Dependencies
pip install requests

# Ollama Installation
curl -fsSL https://ollama.com/install.sh | sh

# Downloading Test Models
   ollama pull exaone3.5:7.8b
   ```

2. **Running Development Scripts**:
   ```bash

# Local Testing
python translate-local.py

# Docker Testing
docker build -t ollama-translator .
docker run --network host ollama-translator

### Testing Environment

```python
```

# test_translation.py
import unittest
from unittest.mock import patch, Mock

class TestTranslation(unittest.TestCase):
    @patch('requests.post')
    def test_translate_with_ollama(self, mock_post):

# Mock API Response
mock_response = Mock()
mock_response.json 반환값 = {'response': 'Hello World'}
mock_post 返回值 = mock_response

# Translation Function Test
result = translate_with_ollama("Hello")
self.assertEqual(result, "Hello World")

## Scalability

### Adding New Languages

To support other language pairs, modify the following code:

```python
def get_translation_prompt(text, source_lang="ko", target_lang="en"):
    prompts = {
        ("ko", "en"): f"Translate the following Korean text into English: {text}",
        ("ko", "ja": f"Translate the following Korean text into Japanese: {text]",
        ("en", "ko"): f"Translate the following English text into Korean: {text}"
    }
    return prompts.get((source_lang, target_lang))
```

### Supporting New File Formats

Currently, only Markdown is supported, but it is possible to add support for other formats as well:

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
       - Maintain markdown format
       - Prioritize accuracy of professional terms
       - Use natural English expression
       
       Original text: {text}
       Translation:
       """
   ```

2. **Post-Processing Improvement**:
   ```python
   def post_process_translation(translated_text):
```

# Restore Markdown Format
translated_text = fix_markdown_formatting(translated_text)

# Checking for Consistency in Professional Terminology
       translated_text = apply_terminology_rules(translated_text)

       return translated_text

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

### Code Style

Coding standards used in the project:

```python
```

# Conformity to PEP 8

# Function Name: snake_case

# Class Name: PascalCase

# Constants: UPPER_CASE

def translate_text(source_text: str, model_name: str) -> str:
    """
    Translates text.

    Args:
        source_text: The original text to be translated.
        model_name: The name of the model to be used.

    Returns:
        The translated text.

    Raises:
        TranslationError: If the translation fails.
    """

    pass

### Commit Message Rules

```
feat: Addition of new feature
fix: Bug fix
docs: Documentation modification
style: Change in code style
refactor: Code refactoring
test: Addition of test code
chore: Other tasks

Example:
feat: Added support for Japanese translation
fix: Fixed an issue with preserving Markdown table format
docs: Added examples of API usage
```

### Pull Request Process

1. **Create an issue**: Create an issue before adding a new feature or fixing a bug.
2. **Create a branch**: In the format `feature/feature_name` or `fix/bug_name`.
3. **Write the code**: Include test code.
4. **Create a PR**: With a detailed description.
5. **Review and merge**: After code review, merge it.

### Test Writing

```python
```

# tests/test_translation.py
def test_korean_to_english_translation():
    """Korean-English translation test"""
    korean_text = "Hello. Nice to meet you."
    expected_english = "Hello. Nice to meet you."

    result = translate_with_ollama(korean_text)

# Even if it's not an exact translation, check if the result is reasonable.
assert "hello" in result.lower()
assert len(result) > 0

def test_markdown_preservation():
    """Test for preserving markdown format"""
    markdown_text = "# Title\n\n**Bold text**."

    result = translate_with_ollama(markdown_text)

    assert result.startswith("#")
    assert "**" in result
```

### Document Updates

When adding new features, be sure to update the following documents:

- `README.md`: Basic usage
- `action.yml`: New input/output parameters
- `docs/`: Detailed guide documents
- `examples/`: Usage examples
```

## Deployment Process

### Version Management

We use [Semantic Versioning](https://semver.org/):

- `MAJOR`: Incompatible API changes
- `MINOR`: Addition of features that are backward compatible
- `PATCH`: Bug fixes that are backward compatible

### Release Procedure

1. **Create a version tag**:
   ```bash
   git tag -a v1.2.0 -m "Release v1.2.0"
   git push origin v1.2.0
   ```

2. **Create a GitHub release**:
   - Automatically build a Docker image
   - Automatically update on the Marketplace

3. **Update documentation**:
   - Update the version information in README.md
   - Update CHANGELOG.md

Thank you for participating in the development! If you have any questions, feel free to ask in issues or discussions at any time.

---

> **⚠️ 이 문서는 AI로 번역된 문서입니다.**
>
> **⚠️ This document has been translated by AI.**