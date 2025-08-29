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

### 1. GitHub Action Definition (`action.yml`)

Defines metadata for the Action available on GitHub Marketplace:

```yaml
name: 'Ollama Korean to English Translator'
description: 'Translation from Korean to English using local Ollama API'
inputs:
  source-dir:
    description: 'Directory containing Korean documents to translate'
    default: 'docs'
outputs:
  translated-files:
    description: 'Number of translated files'
```

### 2. Main Execution Logic (`entrypoint.py`)

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

### 3. Docker Container (`Dockerfile`)

Provides an isolated environment for running the Action:

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
        model (str): Ollama model name
        
    Returns:
        str: Translated English text
    """
    payload = {
        "model": model,
        "prompt": f"Translate the following Korean to English: {text}",
        "stream": False
    }
    response = requests.post(f"{OLLAMA_URL}/api/generate", json=payload)
    return response.json()['response']
```

### File Processing Pipeline

1. **File Discovery**: Search for markdown files using glob patterns
2. **Content Segmentation**: Split large files into chunks
3. **Translation Processing**: Sequentially translate each chunk
4. **Result Merging**: Combine translated chunks
5. **File Storage**: Save translated content to target directories

## Setup for Development Environment

### Local Development Environment

1. **Install Required Tools**:
   ```bash
   # Python dependencies
   pip install requests
   
   # Ollama installation
   curl -fsSL https://ollama.com/install.sh | sh
   
   # Download test model
   ollama pull exaone3.5:7.8b
   ```

2. **Run Development Scripts**:
   ```bash
   # Local testing
   python translate-local.py
   
   # Docker testing
   docker build -t ollama-translator .
   docker run --network host ollama-translator
   ```

### Testing Environment

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

To support additional language pairs, modify:

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

Currently supports markdown only, but other formats can be added:

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
   def translate_text(source_text: str, model_name: str) -> str:
       """Translate text using a specified model."""
       # Translation logic here
       pass
       
   """
   Args:
       source_text: Original text to translate
       model_name: Name of the model to use
       
   Returns:
       Translated text
       
   Raises:
       TranslationError: If translation fails
   """
   ```

### Commit Message Guidelines

```
feat: Add new feature
fix: Resolve bug
docs: Update documentation
style: Code style changes
refactor: Code refactoring
test: Add test cases
chore: Miscellaneous changes

Example:
feat: Support for Japanese translation
fix: Issue with markdown table preservation
docs: Add API usage examples
```

### Pull Request Process

1. **Create an Issue**: Before adding new features or bug fixes, create an issue.
2. **Create a Branch**: Use `feature/feature-name` or `fix/bug-name` format.
3. **Write Code**: Include tests.
4. **Create a PR**: With detailed descriptions.
5. **Review and Merge**: After code review.

### Writing Tests

```python
# tests/test_translation.py
def test_korean_to_english_translation():
    """Test Korean to English translation."""
    korean_text = "안녕하세요. 반갑습니다."
    expected_english = "Hello. Nice to meet you."
    
    result = translate_with_ollama(korean_text)
    
    # Assert reasonable output
    assert "hello" in result.lower()
    assert len(result) > 0


def test_markdown_preservation():
    """Test preservation of markdown format."""
    markdown_text = "# Title\n\n**Bold text** here."
    
    result = translate_with_ollama(markdown_text)
    
    assert result.startswith("#")
    assert "**" in result
```

### Updating Documentation

When adding new features, ensure the following documents are updated:

- `README.md`: Basic usage instructions
- `action.yml`: New input/output parameters
- `docs/`: Detailed guide documents
- `examples/`: Usage examples

Thank you for your contributions! Feel free to ask questions via issues or discussions if needed.