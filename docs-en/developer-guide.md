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
├── docs/                  # Korean documentation
└── README.md             | Project documentation
```

## Core Components

### 1. GitHub Action Definition (action.yml)

This defines the metadata for the Action that can be used on GitHub Marketplace:

```yaml
name: 'Ollama Korean to English Translator'
description: 'Korean-English translation using local Ollama API'
inputs:
  source-dir:
    description: 'Directory containing the Korean language documents to be translated'
    default: 'docs'
outputs:
  translated-files:
    description: 'Number of translated files'
```

### 2. Main Execution Logic (entrypoint.py)

This Python script is responsible for the core logic of the Action:

```python
def main():
    # 1. Read environment variables
    # 2. Check connection to the Ollama server
    # 3. Verify model availability
    # 4. Search for Markdown files
    # 5. Perform translation processing
    # 6. Generate a PR (Pull Request)
```

### 3. Docker Container (Dockerfile)

Provides an isolated environment for executing actions:

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

1. **File Detection**: Searches for Markdown files using glob patterns.
2. **Content Splitting**: Divides large files into chunks using smart chunking.
3. **Translation Processing**: Translates each chunk sequentially.
4. **Result Merging**: Recombines the translated chunks using smart joining techniques.
5. **File Saving**: Saves the translated content to the designated directory.

## Smart Chunking System

### Overview of Chunking Strategy

To process large documents efficiently, the system employs a hierarchical chunking strategy:

```python
def split_markdown_by_sections(content: str, max_tokens: int = None) -> list:
    """Split markdown by sections while preserving meaning units."""
    # 1. Analyze the heading hierarchy (H1-H6)
    # 2. Track the status of code blocks (preserve ``` ~ ``` )
    # 3. Maintain meaning units within token limits
    # 4. Preserve context information (parent heading paths)
```

### Core Functions

#### 1. Section Recognition and Splitting
- **Heading Hierarchy**: H1-H2 are always used as splitting boundaries; H3 sections are split if they contain more than 200 tokens.
- **Meaning Preservation**: Even small sections are maintained independently to preserve their integrity.
- **Context Tracking**: Each chunk retains information about its parent heading.

#### 2. Code Block Preservation
```python
# Logic for detecting and preserving code blocks
if line_stripped.startswith('```'):
    if not in_code_block:
        in_code_block = True
        code_block_fence = line_stripped[:3]
    elif line_stripped.startswith(code_block_fence):
        in_code_block = False
        
# No splitting is performed within code blocks
if not in_code_block and should_split_here:
    # Execute chunk splitting
```

#### 3. Smart Joining
When rejoining the translated chunks, unnecessary line breaks are avoided:

```python
def smart_join_chunks(chunks: list) -> str:
    """Remove unnecessary line breaks between consecutive numbered lists."""
    # Detect the pattern for numbered lists: "- 288. item"
    # Use a single line break for consecutive numbers
    # For regular content, use the default separator
```
```

### Token Calculation System

#### Accurate Token Calculation
```python
def count_tokens(text: str) -> int:
    """Token calculation considering language-specific characteristics"""
    try:
        # Using the tiktoken library (preferred)
        return len(tiktoken.encoding_for_model("gpt-3.5-turbo").encode(text))
    except:
        # Fallback: Estimation based on language characteristics
        korean_chars = len(re.findall(r'[가-힣]', text))
        code_chars = len(re.findall(r'[`{}()[\];]', text))
        other_chars = len(text) - korean_chars - code_chars
        
        return int(korean_chars * 0.5 + code_chars * 0.8 + other_chars * 0.3)
```

#### Safe Margin Calculation
```python
def calculate_safe_input_tokens(context_length: int) -> int:
    """Number of safe tokens considering translation prompts and output buffers"""
    prompt_overhead = 200  # System prompt plus instructions
    output_reserve = int(context_length * 0.4)  # 40% of the output space reserved
    safety_margin = 100    # Additional safety margin
    
    return context_length - prompt_overhead - output_reserve - safety_margin
```

## Debug System

### Automatic Debug File Generation

```python
# Chunk-based debug file generation
def save_debug_chunks(input_path: str, chunks: list):
    """Generate analysis files for each chunk."""
    for i, chunk in enumerate(chunks):
        # Example file name: debug_chunks/filename_chunk_001.md
        metadata = f"""<!-- DEBUG CHUNK {i+1}/{len(chunks)} -->
        <!-- Tokens: {count_tokens(chunk)} -->
        <!-- Characters: {len(chunk)} -->
        -->"""
```

### Translation Comparison System

```python
def save_debug_translation(input_path: str, chunk_index: int, 
                         original_chunk: str, translated_chunk: str):
    """Generate files for comparing the original and translated text."""
    # Example file names: debug_originals/filename_original_001.md, debug_translations/filename_translated_001.md, debug_comparisons/filename_comparison_001.md
```

### Enabling Debug Mode

Controlling the display of detailed debug information through environment variables:

```bash
# Enable debug mode
export INPUT_DEBUG_MODE=true

# Additional output during execution:
# 📦 Created 15 token-aware chunks
# 🔄 [1/15] Translating chunk (245 tokens)...
# 🐛 Saved debug files for chunk 1 (original/translated/comparison)
```

## Development Environment Setup

### Local Development Environment

1. **Required Tool Installation:**
   ```bash
   # Python dependencies
   pip install requests
   
   # Install Ollama
   curl -fsSL https://ollama.com/install.sh | sh
   
   # Download the test model
   ollama pull exaone3.5:7.8b
   ```

2. **Run Development Scripts:**
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
        # Mock the API response
        mock_response = Mock()
        mock_response.json.return_value = {'response': 'Hello World'}
        mock_post.return_value = mock_response
        
        # Test the translation function
        result = translate_with_ollama("Hello")
        self.assertEqual(result, "Hello World")
    ```

## Possibilities for Expansion

### Adding New Languages

To support other language pairs, modify the following code:

```python
def get_translation_prompt(text, source_lang="ko", target_lang="en"):
    prompts = {
        ("ko", "en"): f"Translate the following Korean text into English: {text}",
        ("ko", "ja": f"Translate the following Korean text into Japanese: {text]",
        ("en", "ko": f"Translate the following English text into Korean: {text}"
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
       - Maintain markdown format.
       - Prioritize accuracy of professional terms.
       - Use natural English expression.
       
       Original text: {text}
       Translation:
       """
   ```

2. **Post-Processing Improvement**:
   ```python
   def post_process_translation(translated_text):
       # Restore markdown format
       translated_text = fix_markdown_formatting(translated_text)
       
       # Ensure consistency of professional terms
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
# Complies with PEP 8
# Function names: snake_case
# Class names: PascalCase
# Constants: UPPER_CASE

def translate_text(source_text: str, model_name: str) -> str:
    """
    Translates text.

    Args:
        source_text: The original text to be translated
        model_name: The name of the model to be used

    Returns:
        The translated text

    Raises:
        TranslationError: Occurs in case of translation failure
    """
    pass
```

### Commit Message Rules

```
feat: Addition of new functionality
fix: Bug fixing
docs: Documentation modification
style: Change in code style
refactor: Code refactoring
test: Addition of test code
chore: Other tasks

Examples:
feat: Added support for Japanese translation
fix: Fixed an issue with maintaining Markdown table format
docs: Added examples of API usage
```

### Pull Request Process

1. **Issue Creation**: Create an issue before implementing new features or fixing bugs.
2. **Branch Creation**: Use the format `feature/feature_name` or `fix/bug_name`.
3. **Code Writing**: Include test code.
4. **PR Creation**: Create a pull request with detailed descriptions.
5. **Review Process**: Merge after code review is completed.

### Testing

```python
# tests/test_translation.py
def test_korean_to_english_translation():
    """Korean-to-English translation test"""
    korean_text = "Hello. Nice to meet you."
    expected_english = "Hello. Nice to meet you."

    result = translate_with_ollama(korean_text)

    # Even if it’s not an exact translation, check if the result is reasonable.
    assert "hello" in result.lower()
    assert len(result) > 0

def test_markdown_preservation():
    """Markdown format preservation test"""
    markdown_text = "# Title\n\n**Bold text**"

    result = translate_with_ollama(markdown_text)

    assert result.startswith("#")
    assert "**" in result
```

### Document Updates

Whenever new features are added, be sure to update the following documents:

- `README.md`: Basic usage instructions
- `action.yml`: New input/output parameters
- `docs/`: Detailed guide documents
- `examples/`: Usage examples

## Deployment Process

### Version Management

We use [Semantic Versioning](https://semver.org/):

- `MAJOR`: Changes to APIs that are not backwards compatible.
- `MINOR`: Addition of features that are backward compatible.
- `PATCH`: Fixing of bugs that are backward compatible.

### Release Procedure

1. **Create a version tag:**
   ```bash
   git tag -a v1.2.0 -m "Release v1.2.0"
   git push origin v1.2.0
   ```

2. **Create a GitHub release:**
   - Automatically builds a Docker image.
   - Automatically updates in the Marketplace.

3. **Update documentation:**
   - Update the version information in `README.md`.
   - Update `CHANGELOG.md`.

Thank you for participating in the development! If you have any questions, feel free to ask in issues or discussions at any time.

---

> **⚠️ 이 문서는 AI로 번역된 문서입니다.**
>
> **⚠️ This document has been translated by AI.**