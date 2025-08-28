# Developer Guide

```markdown
This document serves as a guide for developers who wish to understand and contribute to the internal structure of the Ollama Document Translator.
```

## Project Structure

```
ollama-doc-translator/
├── action.yml              # GitHub Actions metadata
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

```markdown
Defines the metadata for Actions available on the GitHub Marketplace:
```

```yaml
name: 'Ollama Korean to English Translator'
description: 'Korean to English Translation using Local Ollama API'
inputs:
  source-dir:
    description: 'Directory containing Korean documents to be translated'
    default: 'docs'
outputs:
  translated-files:
    description: 'Number of translated files'
```

### 2. Main Execution Logic (entrypoint.py)

Python script responsible for the core logic of Action:

```python
def main():
    # 1. Read Environment Variables
    # 2. Verify Ollama Server Connection
    # 3. Check Model Availability
    # 4. Search for Markdown Files
    # 5. Translation Processing
    # 6. Create PR
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
    Translate text using the Ollama API
    
    Args:
        text (str): Korean text to be translated
        model (str): Name of the Ollama model to use
        
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

```markdown
1. **File Discovery**: Search for Markdown files using glob patterns
2. **Content Segmentation**: Divide large files into chunks
3. **Translation Processing**: Sequentially translate each chunk
4. **Result Merging**: Combine translated chunks back together
5. **File Saving**: Save the translated content to the target directory
```

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

```markdown
2. **Execution of Development Scripts**:
   ```bash
   # Local Test
   python translate-local.py
   
   # Docker Test
   docker build -t ollama-translator .
   docker run --network host ollama-translator
   ```
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

### Adding New Language Support

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

### Support for New File Formats

Currently, only Markdown is supported, but additional formats can be added:

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

### Enhancing Translation Quality

```python
def create_context_aware_prompt(text, context=""):
    return f"""
    Context: {context}
    
    Please translate the following technical document into English:
    - Maintain Markdown format
    - Prioritize accuracy of specialized terminology
    - Use natural English expressions
    
    Original Text: {text}
    Translation:
    """
```

```python
2. **Post-Processing Enhancement**:
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
```

```python
async def translate_async(session, text):
    async with session.post(f"{OLLAMA_URL}/api/generate", 
                           json=payload) as response:
        result = await response.json()
        return result['response']
```

```python
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

## Contribution Guide

### Coding Style

Coding Standards Used in the Project:

```python
# Adherence to PEP 8
# Function Name: snake_case
# Class Name: PascalCase
# Constant: UPPER_CASE
```

```python
def translate_text(source_text: str, model_name: str) -> str:
    """
    Translates text.
    
    Args:
        source_text: The original text to be translated.
        model_name: The name of the model to be used.
        
    Returns:
        The translated text.
        
    Raises:
        TranslationError: Raised upon translation failure.
    """
    pass
```

### Commit Message Guidelines

```
feat: Added new features
fix: Bug fixes
docs: Documentation updates
style: Changes in code style
refactor: Code refactoring
test: Added test cases
chore: Miscellaneous tasks
```

```
feat: Added Japanese Translation Support
fix: Resolved Issue with Markdown Table Format Preservation
docs: Added Examples of API Usage
```

### Pull Request Process

```markdown
1. **Issue Creation**: Create an issue before implementing new features or bug fixes
2. **Branch Creation**: Use formats like `feature/기능명` or `fix/버그명`
3. **Code Writing**: Include test code
4. **PR Creation**: Submit with detailed descriptions
5. **Review Process**: Merge after code review
```

### Writing Tests

```python
# tests/test_translation.py
def test_korean_to_english_translation():
    """Test for Korean to English Translation"""
    korean_text = "안녕하세요. 반갑습니다."
    expected_english = "Hello. Nice to meet you."
    
    result = translate_with_ollama(korean_text)
    
    # Verify if the result is reasonably accurate, even if not exact
    assert "hello" in result.lower()
    assert len(result) > 0
```

```python
def test_markdown_preservation():
    """Test for Markdown Format Preservation"""
    markdown_text = "# Heading\n\n**Bold Text** is here."
    
    result = translate_with_ollama(markdown_text)
    
    assert result.startswith("#")
    assert "**" in result
```

### Document Updates

When adding new features, ensure the following documents are updated:

```markdown
- `README.md`: Basic Usage Guide
- `action.yml`: New Input/Output Parameters
- `docs/`: Detailed Guide Documentation
- `examples/`: Usage Examples
```

## Deployment Process

### Version Control

Using Semantic Versioning](https://semver.org/)

```markdown
- `MAJOR`: Incompatible API Changes
- `MINOR`: Addition of Features with Backward Compatibility
- `PATCH`: Bug Fixes with Backward Compatibility
```

### Release Procedure

```markdown
1. **Create Version Tag**:
   ```bash
   git tag -a v1.2.0 -m "Release v1.2.0"
   git push origin v1.2.0
   ```
```

2. **Create GitHub Release**:
   - Automatically build Docker images
   - Automatically update Marketplace

```markdown
3. **Document Updates**:
   - Update version information in README.md
   - Update CHANGELOG.md
```

Thank you for your participation in development! Feel free to ask questions anytime through issues or discussions if you have any inquiries.