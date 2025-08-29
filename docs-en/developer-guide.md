# Developer Guide

This document is a guide for developers who want to understand the internal structure of the Ollama document translator and contribute to it.

## Project Structure

ollama-doc-translator/
│
│   action.yml              # GitHub Action metadata
│   entrypoint.py          # Main execution script
│   Dockerfile             # Docker container definition
│   translate-local.py     # Local test script
│   examples/              # Example usage
│      ├── basic-usage.yml
│      └── advanced-usage.yml
│   docs/                  # Korean documentation
│
└── README.md             # Project documentation

## Core Components

English translation:
```yaml
# GitHub Actions definition (action.yml)
```

Defines the metadata for actions that can be used in the GitHub Marketplace:

```yaml
name: 'Ollama Korean to English Translator'
description: "Local Ollama API-powered Korean-to-English translation"
inputs:
  source-dir:
    description: "Directory containing Korean text documents for translation"
    default: "docs"
outputs:
  translated-files:
    description: "Number of generated translations"

2. Main Execution Logic (entrypoint.py)

The Python script responsible for the core logic of Action:

```python
def main():
    # 1. Read environment variables
    # 2. Check Ollama server connection
    # 3. Check model availability
    # 4. Search for Markdown file
    # 5. Process translation
    # 6. Create PR
```

3. Docker Container (Dockerfile)

Provides an isolated environment for executing Action:

```dockerfile
 FROM python:3.11-slim
 # Install Ollama, GitHub CLI, and Python dependencies
 COPY entrypoint.py /entrypoint.py
 ENTRYPOINT ["python", "/entrypoint.py"]
```

## API Design

Ollama API interface

```python
def translate_with_ollama(text: str, model: str="exaone3.5:7.8b"):
    """
    Translate text using the Ollama API
    
    Arguments:
        text (str): Korean text to be translated
        model (str): Name of the Ollama model to use
        
    Returns:
        str: The resulting English translation
    """
    payload = {
        "model": model,
        "prompt": f"Translate the following into English: {text}",
        "stream": False
    }
    response = requests.post(f"{OLLAMA_URL}/api/generate", json=payload)
    return response.json()['response']
```

English Translation:
### File processing pipeline

1. **File Discovery:** Search for Markdown files using glob patterns
2. **Content Splitting:** Split large files into chunks
3. **Translation Processing:** Sequentially translate each chunk
4. **Result Merging:** Recombine the translated chunks
5. **Save File:** Save the translated content to the target directory

## Setting up Development Environment

English translation:
#### Local development environment

1. **Required Tools Installation:**
   ```bash
   # Python dependencies
   pip install requests
   
   # Install Ollama
   curl -fsSL https://ollama.com/install.sh | sh
   
   # Download test model
   ollama pull exaone3.5:7.8b
   ```

2. **Executing Development Scripts:**
```bash
# Local testing
python translate-local.py

# Docker testing
docker build -t ollama-translator .
docker run --network host ollama-translator
```

English translation:

#### Test environment

```python
 # test_translation.py
 import unittest
 from unittest.mock import patch, Mock
```

```python
class TestTranslation(unittest.TestCase):
    def test_translate_with_ollama(self):
        # Mock API response
        mock_response = Mock()
        mock_response.json.return_value = {'response': 'Hello World'}
        
        def mock_post(*args, **kwargs):
            return mock_response
        
        with patch('requests.post') as mock_post:
            # Test translation function
            result = translate_with_ollama("안녕하세요")
            self.assertEqual(result, "Hello World")
```

## Scalability

New language added (Korean text not provided)

To support another language pair, edit the following:

```python
def get_translation_prompt(text, source_lang="ko", target_lang="en"):
    prompts = {
        ("ko", "en"): f"Translate the following Korean to English: {text}",
        ("ko", "ja"): f"Translate the following Korean to Japanese: {text}",
        ("en", "ko"): f"Translate the following English to Korean: {text}"
    }
    return prompts.get((source_lang, target_lang))
```

New file type support

Currently, only Markdown is supported but other formats are also possible to add:

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

Improve Korean text translation quality

1. **Front-end Engineering**:
```python
def create_context_aware_prompt(text, context=""):
    return f"""
    Context: {context}
    
    Please translate the following described document into English:
    - Maintain Markdown format
    - Prioritize professional terminology accuracy
    - Use natural English expressions
    
    Original text: {text}
    Translation:
    """
```

2. **Post-processing Improvements:**
```python
def post_process_translation(translated_text):
    # Restore markdown formatting
    translated_text = fix_markdown_formatting(translated_text)
    
    # Ensure terminology consistency
    translated_text = apply_terminology_rules(translated_text)
    
    return translated_text
```

## Performance Optimization

Non-blocking processing

```python
import asyncio
import aiohttp
```

async def translate_async(session, text):
    async with session.post(f"{OLLAMA_URL}/api/generate", json=payload) as response:
        result = await response.json()
        return result['response']

async def process_files_async(file_list):
    async with aiohttp.ClientSession() as session:
        tasks = [translate_async(session, content) for content in file_list]
        return await asyncio.gather(*tasks)

Markdown format translation:
```
[Korean text]:
```

```python
import hashlib
import pickle
from pathlib import Path
```

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

Code Style

Coding standards used in the project:

```python
 # Adheres to PEP 8
 # Function name: snake_case
 # Class name: PascalCase
 # Constant: UPPER_CASE
```

```python
def translate_text(source_text: str, model_name: str) -> str:
    """
    Translates a text.
    
    Args:
        source_text: The original text to be translated
        model_name: Name of the model to use
        
    Returns:
        The translated text
        
    Raises:
        TranslationError: If translation fails
    """
    pass

Markdown Format

Translation:
```markdown
### Command Message Rules
```

feat: Added new feature
fix: Fixed bugs
docs: Updated documentation
style: Changed code style
refactor: Refactored code
test: Added test code
chore: Various chores

Feature: Added Japanese translation support
Fix: Resolved issue with preserving Markdown table formatting
Docs: Added API usage example
```

Pull Request process

1. **Issue creation**: Create a new issue for any new feature or bug fix beforehand
2. **Branch creation**: In the format `feature/feature_name` or `fix/bug_name`
3. **Code creation**: Write code including test code
4. **Pull Request (PR) creation**: With detailed explanation
5. **Review proceed**: Code review and merge afterwards

English Translation:

### Writing tests

```python
# tests/test_translation.py
def test_korean_to_english_translation():
    """Test for Korean to English translation"""
    korean_text = "안녕하세요. 반갑습니다."
    expected_english = "Hello. Nice to meet you."
    
    result = translate_with_ollama(korean_text)
    
    # Check if the translation, although not exact, is reasonable
    assert "hello" in result.lower()
    assert len(result) > 0
```

def test_markdown_preservation():
    """Markdown formatting preservation test"""
    markdown_text = "# Title\n\n**Bold text** here."
    
    result = translate_with_ollama(markdown_text)
    
    assert result.startswith("#")
    assert "**" in result

English Translation:

### Update document

When adding new features, make sure to update the following documents:

English translation:
- `README.md`: Basic usage guide
- `action.yml`: New input/output parameters
- `docs/`: Detailed guide documents
- `examples/`: Use case examples

## Distribution Process

Version Control

Usage of Semantic Versioning: (link to https://semver.org/)

```
MAJOR: Incompatible API changes
MINOR: Substantial feature additions with backward compatibility
PATCH: Bug fixes with backward compatibility
```

Release process

1. **Create version tag:**
   ```bash
   git tag -a v1.2.0 -m "Release v1.2.0"
   git push origin v1.2.0
   ```

2. **Create GitHub Release:**
   - Automatically build Docker image
   - Auto-update Marketplace

3. **Document Updates:**
   - Update version information in README.md
   - Update CHANGELOG.md

Thank you for contributing to the development! If you have any questions, feel free to ask them at any time in issues or discussions.