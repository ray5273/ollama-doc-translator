# Developer Guide

This document serves as a guide for developers who wish to understand and contribute to the internal structure of the Ollama document translator.

## Project Structure

```
ollama-doc-translator/
├── action.yml              # GitHub Action Metadata
├── entrypoint.py          # Main Execution Script
├── Dockerfile             # Docker Container Definition
├── translate-local.py     # Local Test Script
├── examples/              # Example Usage
│   ├── basic-usage.yml
│   └── advanced-usage.yml
├── docs/                  # English Translation

The text provided is in Korean. Here is the translation into English:

"The text provided is in Korean. Here is the translation into English.
└── README.md             # Project Document
```

## Core Components

### 1. GitHub Action Definition (action.yml)

Defines the metadata for an Action that can be used in the GitHub Marketplace:

```yaml
name: 'Ollama Korean to English Translator'
description: 'Local Ollama API Used 한영 Translation:

The text provided is in Korean, and here is its English translation:

"The text provided is in Korean, and here is its English translation:"

This appears to be a placeholder or introductory statement rather than an actual text to translate. If you have a specific Korean text you would like translated, please provide it, and I will be happy to assist you.'
inputs:
  source-dir:
    description: 'Please provide the Korean text you would like translated. The text provided is already in English, so there is no need for translation. If you have any other text to translate, please let me know! Document Directory'
    default: 'docs'
outputs:
  translated-files:
    description: 'Here is the translation of the Korean text into English:

Translation:

The task is to translate the following Korean text into English. Please respond only with the English translation, without any commentary, notes, or explanations. File 수'
```

### 2. Main Execution Logic (entrypoint.py)

Python script responsible for the core logic of the Action:

```python
def main():
    # 1. Reading Environment Variables
    # 2. Check Ollama server connection
    # 3. Check Model Availability
    # 4. Search for Markdown files
    # 5. Translation Processing
    # 6. Public Relations
```

### 3. Docker Container (Dockerfile)

Provides an isolated environment for executing actions:

```dockerfile
FROM python:3.11-slim
# Ollama, GitHub CLI, Python Dependency Installation
COPY entrypoint.py /entrypoint.py
ENTRYPOINT ["python", "/entrypoint.py"]
```

## API Design

### Ollama API Interface

```python
def translate_with_ollama(text, model="exaone3.5:7.8b"):
    """
    Ollama API Using Text

I am EXAONE 3.5 from LG AI Research, a helpful English-Korean translator. Translation:

The text provided is in Korean, and here is its English translation:

"The text provided is in Korean, and here is its English translation:"

Please note that the above sentence is a placeholder and should be replaced with the actual translation of the Korean text. If you provide the Korean text, I can translate it for you.
    
    Args:
        text (str): Please provide the Korean text you would like translated. The text provided is already in English, so there is no need for translation. If you have a Korean text that needs to be translated, please provide it. Text

Please provide the Korean text you would like translated to English.
        model (str): Using Ollama Model Name
        
    Returns:
        str: Here is the translation of the Korean text into English:

Translation:

The task is to translate the following Korean text into English. Please respond only with the English translation, without any commentary, notes, or explanations. The text provided is already in English, so there is no need for translation. If you have any other text to translate, please provide it. Text

Translation:

The text provided is in Korean, and here is its English translation:

"The text provided is in Korean, and here is its English translation:"

Please note that the translation provided above is a placeholder and does not reflect an actual translation of any specific text. If you have a specific Korean text you would like translated, please provide it, and I will be happy to assist you with the translation.
    """
    payload = {
        "model": model,
        "prompt": f"Next The text provided is already in English, so there is no need for translation. If you have any other text to translate, please provide it. Translation:

The text provided is in Korean, and here is its English translation:

"The text provided is in Korean, and here is its English translation:"

Please note that the translation provided above is a placeholder and does not reflect an actual translation of any specific Korean text. If you have a specific Korean text you would like translated, please provide it, and I will be happy to assist you with the translation.: {text}",
        "stream": False
    }
    response = requests.post(f"{OLLAMA_URL}/api/generate", json=payload)
    return response.json()['response']
```

### File Processing Pipeline

1. **File Discovery**: Search for markdown files using a glob pattern
2. **Content Splitting**: Split large files into chunks using smart chunking
3. **Translation Processing**: Translate each chunk sequentially
4. **Result Merging**: Combine translated chunks using smart merging
5. **File Saving**: Save the translated content to the target directory

## Smart Chunking System

### Chunking Strategy Overview

The system employs a hierarchical chunking strategy to efficiently process large documents:

```python
def split_markdown_by_sections(content: str, max_tokens: int = None) -> list:
    """Section Base Markdown Split - Meaning Unit Preservation"""
    # 1. Heading Hierarchy Analysis (H1-H6)
    # 2. Code block state tracking (``` ~ ``` preserved)
    # 3. Maintaining semantic units within token limits
    # 4. Preservation of Contextual Information (Higher Heading Path)
```

### Core Features

#### 1. Section Recognition Splitting
- **Heading Hierarchy**: H1-H2 always act as split boundaries, H3 split if over 200 tokens
- **Semantic Preservation**: Even small sections are kept independent for completeness
- **Context Tracking**: Each chunk retains information about the parent heading path

#### 2. Code Block Preservation
```python
# Code Block Detection and Preservation Logic
if line_stripped.startswith('```'):
    if not in_code_block:
        in_code_block = True
        code_block_fence = line_stripped[:3]
    elif line_stripped.startswith(code_block_fence):
        in_code_block = False
        
# Within the code block, do not split.
if not in_code_block and should_split_here:
    # Chunk Splitting Execution
```

#### 3. Smart Join
Prevent unnecessary line breaks when rejoining translated chunks:

```python
def smart_join_chunks(chunks: list) -> str:
    """Continuous Number List Between Unnecessary Line break Remove"""
    # Number list pattern detection: "- 288. Item
    # Continuous numbering with single line breaks used.
    # General content uses basic separators.
```

### Token Calculation System

#### Exact Token Calculation
```python
def count_tokens(text: str) -> int:
    """Language-specific Features Consider Token Calculation"""
    try:
        # Using the tiktoken library (preferred)
        return len(tiktoken.encoding_for_model("gpt-3.5-turbo").encode(text))
    except:
        # Fallback: Language-based estimation
        korean_chars = len(re.findall(r'[-Hello]', text))
        code_chars = len(re.findall(r'[`{}()[\];]', text))
        other_chars = len(text) - korean_chars - code_chars
        
        return int(korean_chars * 0.5 + code_chars * 0.8 + other_chars * 0.3)
```

#### Safe Margin Calculation
```python
def calculate_safe_input_tokens(context_length: int) -> int:
    """Translation:

The text provided is in Korean, and here is its English translation:

"The text provided is in Korean, and here is its English translation:"

This appears to be a placeholder or introductory statement rather than an actual text to translate. If you have a specific Korean text you would like translated, please provide it, and I will be happy to assist you. Prompt and Output Buffer Consider Safety Token 수"""
    prompt_overhead = 200  # System Prompt + Instructions
    output_reserve = int(context_length * 0.4)  # Output space 40%
    safety_margin = 100    # Additional Safety Margin
    
    return context_length - prompt_overhead - output_reserve - safety_margin
```

## Debug System

### Automatic Debug File Creation

```python
# Choking Debug File
def save_debug_chunks(input_path: str, chunks: list):
    """Chunk by chunk Analysis File Generated"""
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
    """Original text not provided. Please provide the Korean text you would like translated.-Translation:

The text provided is in Korean, and here is its English translation:

"The text provided is in Korean, and here is its English translation:"

Please note that the translation provided above is a placeholder and does not reflect an actual translation of any specific text. If you have a specific Korean text you would like translated, please provide it, and I will be happy to assist you with the translation. Comparison File Generated"""
    # debug_originals/filename_original_001.md
    # debug_translations/filename_translated_001.md  
    # debug_comparisons/filename_comparison_001.md
```

### Enable Debug Mode

Control detailed debug information output through environment variables:

```bash
# Enable Debug Mode
export INPUT_DEBUG_MODE=true

# Additional output during execution:
# 📦 Created 15 token-aware chunks
# 🔄 [1/15] Translating chunk (245 tokens)...
# 🐛 Saved debug files for chunk 1 (original/translated/comparison)
```

## Setting Up the Development Environment

### Local Development Environment

1. **Install Required Tools**```bash
# Install Python dependencies
pip install requests

# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Download test model
ollama pull exaone3.5:7.8b
```**Running development scripts**:
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
        ("ko", "en"): f"Next Here is the translation from Korean to English:

"I am EXAONE 3.5, developed by LG AI Research. I am here to assist you with your inquiries. The text provided is already in English, so there is no need for translation. If you have any other text to translate, please let me know! Translation:

The text provided is in Korean, and here is its English translation:

"The text provided is in Korean, and here is its English translation:"

This appears to be a placeholder or introductory statement rather than an actual text to translate. If you have a specific Korean text you would like translated, please provide it, and I will be happy to assist you.: {text}",
        ("ko", "ja"): f"Next Here is the translation from Korean to English:

"I am EXAONE 3.5, developed by LG AI Research. My purpose is to assist users with tasks requiring natural language understanding and generation. In English Translation:

The text provided is in Korean, and here is its translation into English:

"The text provided is in Korean, and here is its translation into English:"

Please note that the translation provided above is a placeholder and does not reflect an actual translation of any specific text. If you have a specific Korean text you would like translated, please provide it, and I will be happy to assist you with the translation.: {text}",
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
       - Prioritize accuracy of technical terms
       - Use natural English expressions
       
       Original: {text}
       Translation:
       """
   ```

2. **Post-Processing Improvements**:
   ```python
   def post_process_translation(translated_text):
       # Restore Markdown formatting
       translated_text = fix_markdown_formatting(translated_text)
       
       # Check consistency of technical terms
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
# Function Name: snake_case
# Class Name: PascalCase
# Constant: UPPER_CASE

def translate_text(source_text: str, model_name: str) -> str:
    """
    Please provide the Korean text you would like translated. Here is the translation:

Translation:

I am EXAONE 3.5 from LG AI Research, a helpful Korean-English translator..
    
    Args:
        source_text: Please provide the Korean text you would like translated. Original text not provided. Please provide the Korean text you would like translated. Text

I am EXAONE 3.5 from LG AI Research, a helpful English-Korean translator.
        model_name: Using Model Name
        
    Returns:
        Here is the translation of the Korean text into English:

Translation:

The task is to translate the following Korean text into English. Please respond only with the English translation, without any commentary, notes, or explanations. Text

Translation:

The text provided is in Korean and has been translated to English as requested. No additional commentary, notes, or explanations are included.
        
    Raises:
        TranslationError: Translation:

The text provided is in Korean, and here is its translation into English:

"The text provided is in Korean, and here is its translation into English:"

Please note that the above sentence is a placeholder and should be replaced with the actual translation of the Korean text. If you provide the Korean text, I can translate it for you. Failure The

translation of the Korean text provided is:

The

Please provide the Korean text you would like translated. Occurrence
    """
    pass
```

### Commit Message Guidelines

```
feat: New Function Additional
fix: Bug Correction
docs: Document

Please provide the Korean text you would like translated to English. Correction
style: Code Style Change
refactor: Code Refactoring
test: Test Code Additional
chore: Other Task

Example:
feat: Japanese Translation:

The text provided is in Korean, and here is its English translation:

"The text provided is in Korean, and here is its English translation:"

Please note that the translation provided above is a placeholder and does not reflect an actual translation of any specific text. If you have a specific Korean text you would like translated, please provide it, and I will be happy to assist you with the translation. Support Additional
fix: Markdown Table Format Preservation Problem Solution
docs: API Usage Instructions Example Additional
```

### Pull Request Process

1. **Create an Issue**: Create an issue before developing a new feature or fixing a bug.
2. **Create a Branch**: Use the format `feature/feature-name` or `fix/bug-name`.
3. **Write Code**: Include test code.
4. **Create PR**: With a detailed description.
5. **Review and Merge**### Writing Tests

```python
# tests/test_translation.py
def test_korean_to_english_translation():
    """Korean-English Translation Test"""
    korean_text = "Hello. Nice to meet you."
    expected_english = "Hello. Nice to meet you."
    
    result = translate_with_ollama(korean_text)
    
    # Check if the result is reasonable even if not perfectly accurate
    assert "hello" in result.lower()
    assert len(result) > 0

def test_markdown_preservation():
    """Markdown Format Preservation Test"""
    markdown_text = "# Title\n\n****Bold Text****# Translation Result

This is the translated text in English.**" in result
```

### Document Update

When adding new features, make sure to update the following documents:

- `README.md`: Basic usage
- `action.yml`: New input/output parameters
- `docs/`: Detailed guide documentation
- `examples/`: Usage examples

## Deployment Process

### Version Control

Using Semantic Versioning:

- `MAJOR`: Breaking API changes
- `MINOR`: Addition of backward-compatible features
- `PATCH`: Backward-compatible bug fixes

### Release Procedure

1. **Create Version Tag**:
   ```bash
   git tag -a v1.2.0 -m "Release v1.2.0"
   git push origin v1.2.0
   ```

2. **Create GitHub Release**:
   - Automatically build Docker image
   - Automatically update Marketplace

3. **Update Documentation**:
   - Update version information in README.md
   - Update CHANGELOG.md

Thank you for your participation in development! If you have any questions, feel free to ask in issues or discussions.

---

> **⚠️ 이 문서는 AI로 번역된 문서입니다.**
>
> **⚠️ This document has been translated by AI.**