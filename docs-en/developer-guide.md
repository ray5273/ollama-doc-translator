# Developer Guide

This document serves as a guide for developers aiming to understand and contribute to the internal structure of the Ollama Document Translator.

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

Defines metadata for an Action usable on GitHub Marketplace:

```yaml
name: 'Ollama Korean to English Translator'
description: 'Korean to English translation using local Ollama API'
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
    # 5. Process translation
    # 6. Create PR
```

### 3. Docker Container (Dockerfile)

Provides an isolated environment for executing the Action:

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
    Translate text using the Ollama API
    
    Args:
        text (str): Korean text to be translated
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
2. **Content Segmentation**: Split large files into chunks
3. **Translation Processing**: Sequentially translate each chunk
4. **Result Merging**: Combine translated chunks back together
5. **File Saving**: Save the translated content to the target directory

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

2. **Run Development Scripts**:
   ```bash
   # Local Testing
   python translate-local.py
   
   # Docker Testing
   docker build -t ollama-translator .
   docker run --network host ollama-translator
   ```

### Testing Environment

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
        
        # Translation function test
        result = translate_with_ollama("안녕하세요")
        self.assertEqual(result, "Hello World")

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

Currently supports only Markdown, but other formats can be added:

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
       
       Original: {text}
       Translation:
       """
   ```

## Post-Processing Enhancements

```python
def post_process_translation(translated_text):
    # Restore Markdown formatting
    translated_text = fix_markdown_formatting(translated_text)
    
    # Ensure consistency in specialized terminology
    translated_text = apply_terminology_rules(translated_text)
    
    return translated_text
```

## Performance Optimization

### Asynchronous Processing

```python
import asyncio
import aiohttp

async def translate_async(session, text):
    async with session.post(f"{OLLAMA_URL}/api/generate", json=payload) as response:
        result = await response.json()
        return result['response']

async def process_files_async(file_list):
    async with aiohttp.ClientSession() as session:
        tasks = [translate_async(session, content) for content in file_list]
        return await asyncio.gather(*tasks)
```

### Caching System

```python
import hashlib
import pickle
from pathlib import Path
```

```markdown
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
        TranslationError: Raised on translation failure
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
test: Addition of test cases
chore: Other housekeeping tasks

Example:
feat: Add Japanese translation support
fix: Resolve markdown table formatting issue
docs: Add API usage examples
```

### Pull Request Process
```

```markdown
## Issue Creation

Create an issue before developing new features or bug fixes.

## Branch Creation

Create branches in the format `feature/feature-name` or `fix/bug-name`.

## Code Development

Include test code.

## PR Creation

Create a pull request with detailed descriptions.

## Code Review and Merge

Complete code review followed by merging.

### Test Writing

```python
# tests/test_translation.py
def test_korean_to_english_translation():
    """Korean to English Translation Test"""
    korean_text = "안녕하세요. 반갑습니다."
    expected_english = "Hello. Nice to meet you."
    
    result = translate_with_ollama(korean_text)
    
    # Verify reasonable output even if not exact translation
    assert "hello" in result.lower()
    assert len(result) > 0

def test_markdown_preservation():
    """Markdown Format Preservation Test"""
    markdown_text = "# Title\n\n**Bold Text** is here."
    
    result = translate_with_ollama(markdown_text)
    
    assert result.startswith("#")
    assert "**" in result
```

### Documentation Updates

Update the following documents when adding new features:

- `README.md`: Basic usage guide
- `action.yml`: New input/output parameters
- `docs/`: Detailed guide documentation
- `examples/`: Usage examples

## Deployment Process

### Version Control

Use Semantic Versioning:

- `MAJOR`: API changes incompatible with previous versions
- `MINOR`: Addition of backward-compatible features
- `PATCH`: Backward-compatible bug fixes

### Release Procedure

1. **Create Version Tag**:
   ```bash
   git tag -a v1.2.0 -m "Release v1.2.0"
   git push origin v1.2.0
   ```

2. **Create GitHub Release**:
   - Automatically triggers Docker image build
   - Automatically updates Marketplace listings

3. **Update Documentation**:
   - Update version information in `README.md`
   - Update `CHANGELOG.md`

Thank you for your contributions! Feel free to ask questions via issues or discussions if needed.
```