# Developer Guide

This document is a guide for developers who want to understand and contribute to the internal structure of the Ollama documentation translator.

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
├── docs/                  # Korean documentation
└── README.md             # Project documentation
```

## Core Components

### 1. GitHub Action Definition (action.yml)

Defines metadata for Actions available on the GitHub Marketplace:

```yaml
name: 'Ollama Korean to English Translator'
description: 'Korean to English translation using a local Ollama API'
inputs:
  source-dir:
    description: 'Directory of Korean documents to be translated'
    default: 'docs'
outputs:
  translated-files:
    description: 'Number of translated files'
```

### 2. Main Execution Logic (entrypoint.py)

Action's core logic Python script:

```python
def main():
    # 1. Read environment variables
    # 2. Verify Ollama server connection
    # 3. Check model availability
    # 4. Search for markdown files
    # 5. Perform translation
    # 6. Create PR
```

### 3. Docker Container (Dockerfile)

Provide an isolated environment for executing actions:

```dockerfile
FROM python:3.11-slim
# Install Ollama, GitHub CLI, and Python dependencies
COPY entrypoint.py /entrypoint.py
ENTRYPOINT ["python", "/entrypoint.py"]
```

## API Design

### Ollama API Interface

```python
def translate_with_ollama(text, model="exaone3.5:7.8b"):
    """
    Translates text using the Ollama API.

    Args:
        text (str): Korean text to translate.
        model (str): The name of the Ollama model to use.

    Returns:
        str: The translated English text.
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

1. **File Discovery**: Search for Markdown files using a glob pattern.
2. **Content Chunking**: Split large files into chunks.
3. **Translation Processing**: Translate each chunk sequentially.
4. **Result Merging**: Merge the translated chunks back together.
5. **File Saving**: Save the translated content to the target directory.

## Development Environment Setup

### Local Development Environment

1. **Install Required Tools**:
   ```bash
   # Python Dependencies
   pip install requests
   
   # Ollama Installation
   curl -fsSL https://ollama.com/install.sh | sh
   
   # Download Test Model
   ollama pull exaone3.5:7.8b
   ```

2. **Run Development Script**:
   ```bash
   # Local Testing
   python translate-local.py
   
   # Docker Testing
   docker build -t ollama-translator .
   docker run --network host ollama-translator
   ```

### Test Environment

```python
# test_translation.py
import unittest
from unittest.mock import patch, Mock
```

```python
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

## Scalability

### New Language Added

To support other language pairs, modify the following:

```python
def get_translation_prompt(text, source_lang="ko", target_lang="en"):
    prompts = {
        ("ko", "en"): f"Translate the following Korean to English: {text}",
        ("ko", "ja"): f"Translate the following Korean to Japanese: {text}",
        ("en", "ko"): f"Translate the following English to Korean: {text}"
    }
    return prompts.get((source_lang, target_lang))
```

### New File Format Support

Currently, only Markdown is supported, but other formats could be added:

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
       - Prioritize accuracy of technical terms
       - Use natural English phrasing
       
       Original Text: {text}
       Translation:
       """
   ```

2. **Post-processing Improvements**:
   ```python
   def post_process_translation(translated_text):
       # Restore Markdown formatting
       translated_text = fix_markdown_formatting(translated_text)
       
       # Ensure terminology consistency
       translated_text = apply_terminology_rules(translated_text)
       
       return translated_text
   ```

## Performance Optimization

### Asynchronous Processing

```python
import asyncio
import aiohttp
```

async def translate_async(session, text):
    async with session.post(f"{OLLAMA_URL}/api/generate", 
                           json=payload) as response:
        result = await response.json()
        return result['response']

```python
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
```

```python
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

## Contributing Guide

### Code Style

Project Coding Standards:

```python
# PEP 8 compliance
# Function names: snake_case
# Class names: PascalCase
# Constants: UPPER_CASE
```

```python
def translate_text(source_text: str, model_name: str) -> str:
    """
    Translates text.

    Args:
        source_text: The original text to be translated.
        model_name: The name of the model to use.

    Returns:
        The translated text.

    Raises:
        TranslationError: Raised when translation fails.
    """
    pass
```

### Commit Message Guidelines

```
feat: Add new feature
fix: Fix bug
docs: Modify documentation
style: Change code style
refactor: Refactor code
test: Add test code
chore: Other tasks
```

feat: Add Japanese translation support
fix: Resolve issue with preserving Markdown table formatting
docs: Add API usage examples

### Pull Request Process

1. **Issue Creation**: Create an issue before implementing a new feature or fixing a bug.
2. **Branch Creation**: Use the format `feature/feature-name` or `fix/bug-name`.
3. **Code Implementation**: Include test code.
4. **PR Creation**: Create a Pull Request with detailed descriptions.
5. **Review & Merge**: Proceed with code review and then merge.

### Writing Tests

```python
# tests/test_translation.py
def test_korean_to_english_translation():
    """Korean-to-English translation test"""
    korean_text = "안녕하세요. 반갑습니다."
    expected_english = "Hello. Nice to meet you."
    
    result = translate_with_ollama(korean_text)
    
    # Check if the result is a reasonable outcome, even if not a perfect translation
    assert "hello" in result.lower()
    assert len(result) > 0
```

```python
def test_markdown_preservation():
    """Markdown format preservation test"""
    markdown_text = "# Heading\n\n**Bold text** is here."
    
    result = translate_with_ollama(markdown_text)
    
    assert result.startswith("#")
    assert "**" in result
```

### Document Update

When adding new features, be sure to update the following documents:

- `README.md`: Basic usage
- `action.yml`: New input/output parameters
- `docs/`: Detailed guides
- `examples/`: Usage examples

## Deployment Process

### Version Control

[Semantic Versioning](https://semver.org/) Usage:

- `MAJOR`: Incompatible API changes
- `MINOR`: Backwards-compatible feature additions
- `PATCH`: Backwards-compatible bug fixes

### Release Procedure

1. **Create Version Tag**:
   ```bash
   git tag -a v1.2.0 -m "Release v1.2.0"
   git push origin v1.2.0
   ```

2. **Create GitHub Release**:
   - Automatically build Docker image
   - Automatically update Marketplace

3. **Document Updates**:
   - README.md version information
   - CHANGELOG.md update

Thank you for contributing to the development! If you have any questions, please feel free to ask in the issues or discussions.