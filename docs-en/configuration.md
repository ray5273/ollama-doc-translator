# Configuration Guide

This document outlines the detailed settings options and customization methods for the Ollama document translator.

## GitHub Action Configuration

### Basic Configuration

The simplest form of workflow configuration:

```yaml
name: Document

Translation:

Document Translation:

The text provided is in Korean, and here is its English translation:

"The text provided is in Korean, and here is its English translation:"

Please note that the above sentence is a placeholder and should be replaced with the actual translation of the Korean text. If you provide the Korean text, I can translate it for you.

on:
  push:
    paths: ['docs/**/*.md']

jobs:
  translate:
    runs-on: self-hosted
    steps:
    - uses: actions/checkout@v4
    - uses: your-username/ollama-doc-translator@v1
      with:
        github-token: ${{ secrets.GITHUB_TOKEN }}
```

### Advanced Configuration

An example utilizing all configuration options:

```yaml
- uses: your-username/ollama-doc-translator@v1
  with:
    # Server Configuration
    ollama-url: 'http://localhost:11434'
    model: 'exaone3.5:7.8b'
    
    # Directory Setup
    source-dir: 'docs'
    target-dir: 'docs-en'
    file-pattern: '**/*.md'
    
    # Translation settings
    temperature: 0.3
    max-retries: 3
    skip-existing: true
    
    # PR Setup
    create-pr: true
    pr-title: 'Document Translation:

The text provided is in Korean, and here is its English translation:

"The text provided is in Korean, and here is its English translation:"

This appears to be a placeholder or introductory statement rather than an actual text to translate. If you have a specific Korean text you would like translated, please provide it, and I will be happy to assist you. Update'
    pr-branch: 'translate-docs'
    commit-message: 'docs: The text provided is already in English, so there is no need for translation. If you have any specific text in Korean that needs translation, please provide it. Document

Translation:

Document The text provided is already in English, so there is no need for translation. If you have any other text to translate, please provide it. Translation:

The text provided is in Korean, and here is its English translation:

"The text provided is in Korean, and here is its English translation:"

This appears to be a placeholder or introductory statement rather than an actual text to translate. If you have a specific Korean text you would like translated, please provide it, and I will be happy to assist you. Additional'
    
    # Authentication
    github-token: ${{ secrets.GITHUB_TOKEN }}
```

## Model Configuration

### Supported Models

You can use various Ollama models:

| Model Name | Size | Memory Requirement | Translation Quality | Speed |
|------------|------|--------------------|--------------------|-------|
| `exaone3.5:7.8b` | 7.8B | 8GB | Excellent | Fast |
| `exaone3.5:32b` | 32B | 32GB | Best | Slow |
| `llama3.1:8b` | 8B | 8GB | Good | Fast |
| `mistral:7b` | 7B | 7GB | Good | Very Fast |

### Model Performance Tuning

#### Temperature Setting
```yaml
temperature: 0.1  # More consistent translation (conservative)
temperature: 0.3  # Balanced Translation (Recommended)
temperature: 0.7  # A more creative translation
```

#### Context Length
```yaml
# Settings for a long document
context-length: 4096  # Default: 2048
```

## Directory Structure Setup

### Basic Structure
```
project/
├── docs/           # Original text not provided. Please provide the Korean text to be translated.
│   ├── README.md
│   └── guide.md
└── docs-en/        # The text provided is already in English, so there is no need for translation. If you have any other text to translate from Korean to English, please provide it.
    ├── README.md
    └── guide.md
```

### Custom Structure
```yaml
source-dir: 'korean-docs'
target-dir: 'english-docs'
file-pattern: '**/*.{md,mdx}'
```

### Handling Subdirectories
```yaml
# Maintaining a subdirectory structure
source-dir: 'docs'
target-dir: 'docs-en'
file-pattern: '**/*.md'  # Include all subdirectories
```

Example:
```
docs/
├── getting-started/
│   ├── installation.md
│   └── quick-start.md
├── advanced/
│   └── configuration.md
└── README.md

→ Translation:

The text provided is in Korean, and here is its translation into English:

"The text provided is in Korean, and here is its translation into English:"

Please note that the above sentence is a placeholder and should be replaced with the actual translation of the Korean text. If you provide the Korean text, I can translate it for you. After

docs-en/
├── getting-started/
│   ├── installation.md
│   └── quick-start.md
├── advanced/
│   └── configuration.md
└── README.md
```

## Workflow Trigger Setup

### File Change Detection
```yaml
on:
  push:
    paths: 
      - 'docs/**/*.md'
      - '!docs/README.md'  # README.md excluded
    branches: [ main, develop ]
```

### Schedule Execution
```yaml
on:
  schedule:
    - cron: '0 2 * * 1'  # Every Monday at 2 AM
  workflow_dispatch:     # Allow manual execution
```

### Conditional Execution
```yaml
jobs:
  translate:
    if: contains(github.event.head_commit.message, '[translate]')
    # If the commit message contains [translate], execute.
```

## Setting Up Pull Requests

### Customizing PR Templates

You can customize the default PR body:

```yaml
pr-title: '📚 Document Translation:

The text provided is in Korean, and here is its English translation:

"The text provided is in Korean, and here is its English translation:"

Please note that the above sentence is a placeholder and should be replaced with the actual translation of the Korean text. If you provide the Korean text, I can translate it for you.: ${{ github.event.head_commit.message }}'
pr-branch: 'auto-translate-${{ github.run_number }}'
```

### Automatic Reviewer Assignment

Create a `.github/CODEOWNERS` file to automatically assign reviewers for translation PRs:

```
docs-en/ @translation-team
*.md @docs-team
```

### Automatic Label Addition

Use GitHub CLI to add labels:

```yaml
- name: Add labels to PR
  run: |
    gh pr edit ${{ steps.translate.outputs.pr-number }} \
      --add-label "documentation" \
      --add-label "translation" \
      --add-label "automated"
```

## Performance Optimization

### Parallel Processing
```yaml
# Under specific conditions only
skip-existing: true        # Skipping translated files
min-file-size: 100        # Skip files under 100 bytes
max-file-size: 50000      # Skip files over 50KB
```

### Cache Configuration
```yaml
- name: Cache Ollama models
  uses: actions/cache@v4
  with:
    path: ~/.ollama
    key: ollama-models-${{ runner.os }}
```

### Conditional Translation
```yaml
# Execute translation only under certain conditions
skip-existing: true        # Skip translated files
min-file-size: 100        # Skip files smaller than 100 bytes
max-file-size: 50000      # Skip files larger than 50KB

## Security Settings

### Token Management
```yaml
# Using minimal privilege tokens
permissions:
  contents: read
  pull-requests: write
  
github-token: ${{ secrets.GITHUB_TOKEN }}
```

### Private Repository
```yaml
# Using in private storage
- uses: actions/checkout@v4
  with:
    token: ${{ secrets.PAT_TOKEN }}  # Personal Access Token
```

## Multi-Language Support

### Translation into Multiple Languages

```yaml
strategy:
  matrix:
    target-lang: [en, ja, zh]
    
steps:
- uses: your-username/ollama-doc-translator@v1
  with:
    target-dir: 'docs-${{ matrix.target-lang }}'
    model: 'exaone3.5:7.8b'
    target-language: ${{ matrix.target-lang }}
```

## Notification Settings

### Slack Notification
```yaml
- name: Notify Slack
  if: steps.translate.outputs.pr-url
  uses: 8398a7/action-slack@v3
  with:
    status: success
    text: 'Document

Translation:

Document Translation:

I am EXAONE 3.5 from LG AI Research, a helpful Korean-English translator. Completed: ${{ steps.translate.outputs.pr-url }}'
```

### Email Notification
```yaml
- name: Send Email
  uses: dawidd6/action-send-mail@v3
  with:
    subject: 'Document Translation:

The text provided is in Korean, and here is its translation into English:

"The text provided is in Korean, and here is its translation into English:"

Please note that the above sentence is a placeholder and should be replaced with the actual translation of the Korean text. If you provide the Korean text, I can translate it for you. Completed'
    body: 'New Translation:

The text provided is in Korean, and here is its English translation:

"The text provided is in Korean, and here is its English translation:"

This appears to be a placeholder or introductory statement rather than an actual text to translate. If you have a specific Korean text you would like translated, please provide it, and I will be happy to assist you. PR It has been created..'
```

## Debug and Analysis Setup

### Enable Debug Mode

By enabling debug mode, you can inspect detailed information about the translation process:

```yaml
- uses: your-username/ollama-doc-translator@v1
  with:
    debug-mode: true           # Enable Debug File Creation
    github-token: ${{ secrets.GITHUB_TOKEN }}
```

### Generated Debug Files

When debug mode is enabled, the following files are automatically created:

#### 1. Chunking Debug Files (`debug_chunks/`)
```
debug_chunks/
├── document-name_chunk_001.md     # Analysis file per chunk
├── document-name_chunk_002.md
├── ...
└── document-name_summary.md       # Choking Summary Report
```

Example header for each chunk file:
```markdown
<!-- DEBUG CHUNK 1/15 -->
<!-- Tokens: 245 -->
<!-- Characters: 856 -->
<!-- Source: docs/api-guide.md -->

---

The actual Chunk Content...
```

#### 2. Translation Comparison Files (`debug_originals/`, `debug_translations/`)
```
debug_originals/
├── document-name_original_001.md   # Original chunks
├── document-name_original_002.md
└── ...

debug_translations/
├── document-name_translated_001.md # Translated chunks
├── document-name_translated_002.md
└── ...

debug_comparisons/
├── document-name_comparison_001.md # Original Text:

In the heart of the city, amidst the bustling streets and towering skyscrapers, stood a small, unassuming bookstore. Its shelves were lined with books of every genre, from classic literature to contemporary bestsellers. The aroma of old paper and ink filled the air, creating a cozy atmosphere that invited readers to lose themselves in the pages.

Translation:

In the heart of the city, amidst the bustling streets and towering skyscrapers, stood a small, unassuming bookstore. Its shelves were lined with books of every genre, from classic literature to contemporary bestsellers. The scent of old paper and ink filled the air, creating a cozy atmosphere that invited readers to lose themselves in the pages.
├── document-name_comparison_002.md
└── ...
```

### Debug Information Interpretation

#### Console Output Example
```bash
📄 Processing large file (5,234 tokens > 1,500 limit)...
🔧 Starting chunking process:
   📊 Input: 23 paragraphs
   🎯 Target: 1,200 tokens per chunk
📦 Created 5 token-aware chunks:
   Chunk 1: 1,156 tokens (2,845 chars)
   Chunk 2: 1,087 tokens (2,634 chars)
   Chunk 3: 978 tokens (2,123 chars)
   Chunk 4: 1,134 tokens (2,689 chars)
   Chunk 5: 879 tokens (1,956 chars)
🔄 [1/5] Translating chunk (1,156 tokens)... ✅ Done (2,934 chars)
🐛 Saved debug files for chunk 1 (original/translated/comparison)
```

#### Token Calculation Information
```yaml
# Setting Context Length for Large Document Processing
context-length: 32768          # Model Context Length
```

System-calculated safe token count:
- **Prompt Overhead**: ~200 tokens
- **Output Reservation Space**: 40% of context length
- **Safety Margin**: 100 tokens
- **Available for Use**: Approximately 19,268 tokens (based on 32,768)

### Advanced Debugging Configuration

#### Smart Chunking Analysis
```yaml
# Detailed Analysis of Coking Strategies
- uses: your-username/ollama-doc-translator@v1
  with:
    debug-mode: true
    context-length: 4096        # Smaller chunks for finer analysis
    temperature: 0.1            # Consistent Translation Output
```

#### Code Block Preservation Verification
Check if code blocks are preserved correctly through the debug file:

```markdown
<!-- Original text not provided. Please provide the Korean text you would like translated. Chunk from -->
```python
def translate_text(text):
    return translated_text
```

<!-- Translation:

The text provided is in Korean, and here is its translation into English:

"The text provided is in Korean, and here is its translation into English:"

Please note that the above sentence is a placeholder and should be replaced with the actual translation of the Korean text. If you provide the Korean text, I can translate it for you. In chunks Similarly Preservation -->
```python
def translate_text(text):
    return translated_text
```


### Artifact and Log Storage

```yaml
- name: Upload debug files
  if: always()  # Upload regardless of success/failure
  uses: actions/upload-artifact@v4
  with:
    name: translation-debug-files
    path: |
      debug_chunks/
      debug_originals/
      debug_translations/
      debug_comparisons/
    retention-days: 7

- name: Upload translation logs
  if: failure()
  uses: actions/upload-artifact@v4
  with:
    name: translation-logs
    path: |
      translation-*.log
      error-*.log
```

### Performance Analysis

Performance metrics provided in debug mode:

```bash
📊 Translation Performance Summary:
   ⏱️  Total time: 2m 34s
   📄 Files processed: 12
   🔄 Total chunks: 67
   📈 Average chunk size: 1,089 tokens
   ⚡ Translation speed: ~425 tokens/sec
   🎯 Success rate: 100% (0 retries needed)
```

### Troubleshooting Guide

#### Common Issues

1. **Chunks are too large**
   ```yaml
   context-length: 4096  # Set lower than default(32768)
   ```

2. **Inconsistent translation quality**
   ```yaml
   temperature: 0.1      # More conservative translation
   max-retries: 5        # Increase retry count
   ```

3. **Code blocks are breaking**
   - Compare original and translated in `debug_comparisons/` file
   - Ensure code block preservation logic is functioning correctly

By combining these settings, you can construct an optimal translation workflow tailored to your project.

---

> **⚠️ 이 문서는 AI로 번역된 문서입니다.**
>
> **⚠️ This document has been translated by AI.**