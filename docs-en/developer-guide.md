# Developer Guide

This document is a guide for developers who want to understand and contribute to the internal structure of the Ollama documentation translator.

## Project Structure

```
ollama-doc-translator/
├── action.yml              # GitHub Actions metadata
├── entrypoint.py          # Main execution script
├── Dockerfile             # Docker container definition
├── translate-local.py     # Local test script
├── examples/              # Example usage
│   ├── basic-usage.yml
│   └── advanced-usage.yml
├── docs/                  # Korean document
└── README.md             # Project document
```

## Core Components

### 1. GitHub Action Definition (action.yml)

Defines the metadata for Actions available on the GitHub Marketplace:

```yaml
name: 'Ollama Korean to English Translator'
description: 'Local Ollama API Used Korean-English Translation'
inputs:
  source-dir:
    description: 'To be translated Korean Document Directory'
    default: 'docs'
outputs:
  translated-files:
    description: 'Translated File Number'
```

### 2. Main Execution Logic (entrypoint.py)

Python script responsible for the core logic of the Action:

```python
def main():
    # 1. Read environment variables
    # 2. Verify Ollama server connection
    # 3. Verify model availability
    # 4. Search for Markdown files
    # 5. Translation processing
    # 6. Create a PR
```

### 3. Docker Container (Dockerfile)

Provides an isolated environment to run the action:

```dockerfile
FROM python:3.11-slim
# Ollama, GitHub CLI, Python dependencies installation
COPY entrypoint.py /entrypoint.py
ENTRYPOINT ["python", "/entrypoint.py"]
```

## API Design

### Ollama API Interface

```python
def translate_with_ollama(text, model="exaone3.5:7.8b"):
    """
    Ollama API Using Text Translation
    
    Args:
        text (str): To be translated Korean Text
        model (str): To use Ollama Model name
        
    Returns:
        str: Translated English Text
    """
    payload = {
        "model": model,
        "prompt": f"Following Please provide the Korean text you would like me to translate. Translation: {text}",
        "stream": False
    }
    response = requests.post(f"{OLLAMA_URL}/api/generate", json=payload)
    return response.json()['response']
```

### File Processing Pipeline

1. **File Discovery**: Search for Markdown files using a glob pattern
2. **Content Splitting**: Split large files into chunks using smart chunking
3. **Translation Processing**: Translate each chunk sequentially
4. **Result Merging**: Merge the translated chunks back together using smart joining
5. **File Saving**: Save the translated content to the target directory

## Smart Chunking System

### Chunking Strategy Overview

The system uses a hierarchical chunking strategy to efficiently process large documents:

```python
def split_markdown_by_sections(content: str, max_tokens: int = None) -> list:
    """Section Foundation Markdown Division - Meaning Unit Preservation"""
    # 1. Heading hierarchy analysis (H1-H6)
    # 2. Tracking the status of code blocks (``` ~ ``` preserved)
    # 3. Maintain meaning units within the token limit.
    # 4. Preserve context information (top-level heading path)
```

### Key Features

#### 1. Section-Based Splitting
- **Heading Hierarchy**: H1-H2 are always splitting boundaries, H3 is split if it exceeds 200 tokens
- **Meaning Preservation**: Even small sections are maintained independently for completeness
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
Prevent unnecessary line breaks when merging translated chunks:

```python
def smart_join_chunks(chunks: list) -> str:
    """continuous Number List between Unnecessary Line break Removal"""
    # Detecting list pattern: "- 288. Item
    # When using consecutive numbers, use a single line break.
    # General content: Use of basic separator.
```

### Token Calculation System

#### Accurate Token Calculation
```python
def count_tokens(text: str) -> int:
    """By language Characteristics Considered Token Calculation"""
    try:
        # Preferably using the tiktoken library.
        return len(tiktoken.encoding_for_model("gpt-3.5-turbo").encode(text))
    except:
        # Full-backs: Estimates by language
        korean_chars = len(re.findall(r'[-Hi]', text))
        code_chars = len(re.findall(r'[`{}()[\];]', text))
        other_chars = len(text) - korean_chars - code_chars
        
        return int(korean_chars * 0.5 + code_chars * 0.8 + other_chars * 0.3)
```

#### Safe Margin Calculation
```python
def calculate_safe_input_tokens(context_length: int) -> int:
    """Translation Prompt and Output Buffer Considered Safety Token Number"""
    prompt_overhead = 200  # System prompt + instructions
    output_reserve = int(context_length * 0.4)  # Output space: 40%
    safety_margin = 100    # Additional safety margin
    
    return context_length - prompt_overhead - output_reserve - safety_margin
```

## Debug System

### Automatic Debug File Generation

```python
# Debugging file for Cleaning
def save_debug_chunks(input_path: str, chunks: list):
    """By chunk Analysis File Creation"""
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
    """Original-Translation Comparison File Creation"""
    # debug_originals/filename_original_001.md
    # debug_translations/filename_translated_001.md  
    # debug_comparisons/filename_comparison_001.md
```

### Enable Debug Mode

Control detailed debug information output using environment variables:

```bash
# Enable debug mode
export INPUT_DEBUG_MODE=true

# Additional output when running:
# 📦 Created 15 token-aware chunks
# 🔄 [1/15] Translating chunk (245 tokens)...
# 🐛 Saved debug files for chunk 1 (original/translated/comparison)
```

## Setting up the Development Environment

### Local Development Environment

1. **Install Required Tools**:
   ```bash
   # Python dependencies
   pip install requests
   
   # Ollama installation
   curl -fsSL https://ollama.com/install.sh | sh
   
   # Download test model
   ollama pull exaone3.5:7.8b
   ```**Run the development script.**:
   ```bash
   # Local testing
   python translate-local.py
   
   # Docker testing
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
        
        # Test the translation function
        result = translate_with_ollama("Hello")
        self.assertEqual(result, "Hello World")
```

## Scalability

### Adding new languages

To support other language pairs, modify the following:

```python
def get_translation_prompt(text, source_lang="ko", target_lang="en"):
    prompts = {
        ("ko", "en"): f"Next Korean language Please provide the Korean text you would like me to translate. Translation: {text}",
        ("ko", "ja"): f"Next Korean In Japanese Translation: {text}",
        ("en", "ko"): f"Translate the following English to Korean: {text}"
    }
    return prompts.get((source_lang, target_lang))
```

### Supporting new file formats

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
       
       Please translate the following technical document into English:
       - Maintain Markdown format
       - Prioritize accuracy of technical terms
       - Natural English expression
       
       Original text: {text}
       Translation:
       """
   ```

2. **Post-processing Improvement**:
   ```python
   def post_process_translation(translated_text):
       # Restore Markdown format
       translated_text = fix_markdown_formatting(translated_text)
       
       # Verify consistency of technical terms
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

### Code Style

Coding standards used in the project:

```python
# Adhere to PEP 8
# Function name: snake_case
# Class Name: PascalCase
# Constant: UPPER_CASE

def translate_text(source_text: str, model_name: str) -> str:
    """
    the text I will translate..
    
    Args:
        source_text: To be translated Original Text
        model_name: To use Model name
        
    Returns:
        Translated Text
        
    Raises:
        TranslationError: Translation Failure poem occurrence
    """
    pass
```

### Commit Message Rules

```
feat: New Function Additional
fix: Bug Correction
docs: Document Revision
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

1. **Issue Creation**: Create an issue for new features or bug fixes.
2. **Branch Creation**: Create a branch with the format `feature/feature_name` or `fix/bug_name`.
3. **Code Implementation**: Include test code.
4. **PR Creation**: Create a Pull Request with detailed descriptions.
5. **Review and Merge**: Conduct code review and merge.

### Test Writing

```python
# tests/test_translation.py
def test_korean_to_english_translation():
    """Korean to English translation test"""
    korean_text = "Hello. Nice to meet you.."
    expected_english = "Hello. Nice to meet you."
    
    result = translate_with_ollama(korean_text)
    
    # The translation may not be perfect, but check if it's reasonable
    assert "hello" in result.lower()
    assert len(result) > 0

def test_markdown_preservation():
    """Markdown format preservation test"""
    markdown_text = "# Title\n\n**Bold text**
    
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

## Deployment Process

### Version Management

Using [Semantic Versioning](https://semver.org/):

- `MAJOR`: API changes that are not backward compatible
- `MINOR`: Adding features that are backward compatible
- `PATCH`: Fixing bugs that are backward compatible

### Release Procedure

1. **Create Version Tag**:
   ```bash
   git tag -a v1.2.0 -m "Release v1.2.0"
   git push origin v1.2.0
   ```

2. **Create GitHub Release**:
   - Automatically build Docker image
   - Automatic Marketplace update

3. **Update Documentation**:
   - Version information in README.md
   - Update CHANGELOG.md

Thank you for your participation! If you have any questions, please ask in an issue or discussion.

---

> **⚠️ 이 문서는 AI로 번역된 문서입니다.**
>
> **⚠️ This document has been translated by AI.**