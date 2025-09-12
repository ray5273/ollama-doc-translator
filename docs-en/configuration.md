# Setup Guide

This guide explains detailed setup options and customization methods for the Ollama document translator.

## GitHub Action Configuration

### Basic Configuration

Simplest workflow setup example:

```yaml
name: Document Translation

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

Example utilizing all configuration options:

```yaml
- uses: your-username/ollama-doc-translator@v1
  with:
    # Server settings
    ollama-url: 'http://localhost:11434'
    model: 'exaone3.5:7.8b'
    
    # Directory settings
    source-dir: 'docs'
    target-dir: 'docs-en'
    file-pattern: '**/*.md'
    
    # Translation setting
    temperature: 0.3
    max-retries: 3
    skip-existing: true
    
    # PR Setup
    create-pr: true
    pr-title: 'Document Translation Update'
    pr-branch: 'translate-docs'
    commit-message: 'docs: Please provide the Korean text you would like translated. Document It seems there might be a misunderstanding; you've provided "영어" which means "English" in Korean, but no actual Korean text to translate was given. Could you please provide the Korean text you would like translated into English? Translation Additional'
    
    # Authentication
    github-token: ${{ secrets.GITHUB_TOKEN }}
```

## Model Configuration

### Supported Models

Various Ollama models are available:

| Model Name | Size | Memory Requirement | Translation Quality | Speed |
|------------|------|--------------------|---------------------|-------|
| `exaone3.5:7.8b` | 7.8B | 8GB | Very Good | Fast |
| `exaone3.5:32b` | 32B | 32GB | Best | Slow |
| `llama3.1:8b` | 8B | 8GB | Good | Fast |
| `mistral:7b` | 7B | 7GB | Good | Very Fast |

### Model Performance Tuning

#### Temperature Setting
```yaml
temperature: 0.1  # More consistent translation (conservative approach)
temperature: 0.3  # Balanced translation (recommended)
temperature: 0.7  # A more creative translation
```

#### Context Length
```yaml
# Settings for long documents
context-length: 4096  # Default value: 2048
```

## Directory Structure Setup

### Basic Structure
```
project/
├── docs/           # Please provide the Korean text you would like translated.
│   ├── README.md
│   └── guide.md
└── docs-en/        # Please provide the Korean text you would like translated into English.
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
# Maintain subdirectory structure
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

→ Translation After

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
      - '!docs/README.md'  # Exclude README.md
    branches: [ main, develop ]
```

### Scheduled Execution
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
    # Execute only if the commit message includes "[translate]".
```

## Pull Request Setup

### Customizing PR Template

You can customize the basic PR body:

```yaml
pr-title: '📚 Document Translation: ${{ github.event.head_commit.message }}'
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
# Execute translation only under specific conditions.
skip-existing: true        # Skip translated files already processed.
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
# Translate only under specific conditions
skip-existing: true        # Skip translated files
min-file-size: 100        # Skip files smaller than 100 bytes
max-file-size: 50000      # Skip files larger than 50KB

## Security Settings

### Token Management
```yaml
# Use of Minimal Privilege Tokens
permissions:
  contents: read
  pull-requests: write
  
github-token: ${{ secrets.GITHUB_TOKEN }}
```

### Private Repository
```yaml
# Used in private storage
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
    text: 'Document Translation It is completed.: ${{ steps.translate.outputs.pr-url }}'
```

### Email Notification
```yaml
- name: Send Email
  uses: dawidd6/action-send-mail@v3
  with:
    subject: 'Document Translation Completed'
    body: 'New Translation PRThis It was created..'
```

## Debug and Analysis Settings

### Enable Debug Mode

Through debug mode, you can inspect detailed information about the translation process:

```yaml
- uses: your-username/ollama-doc-translator@v1
  with:
    debug-mode: true           # Enable debug file creation
    github-token: ${{ secrets.GITHUB_TOKEN }}
```

### Generated Debug Files

When debug mode is activated, the following files are automatically generated:

#### 1. Chunking Debug Files (`debug_chunks/`)
```
debug_chunks/
├── document-name_chunk_001.md     # Analysis files per chunk
├── document-name_chunk_002.md
├── ...
└── document-name_summary.md       # Chunking Summary Report
```

Example header of each chunk file:
```markdown
<!-- DEBUG CHUNK 1/15 -->
<!-- Tokens: 245 -->
<!-- Characters: 856 -->
<!-- Source: docs/api-guide.md -->

---

Actual Chunk Content...
```

#### 2. Translation Comparison Files (`debug_originals/`, `debug_translations/`, `debug_comparisons/`)
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
├── document-name_comparison_001.md # Original-Translation Comparison File
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
# Setting context length for large document processing
context-length: 32768          # Model context length
```

System automatically calculated safe token count:
- **Prompt Overhead**: ~200 tokens
- **Output Reserved Space**: 40% of context length
- **Safety Margin**: 100 tokens
- **Available Usage**: Approximately 19,268 tokens (based on 32,768)

### Advanced Debugging Settings

#### Smart Chunking Analysis
```yaml
# Detailed Analysis of the Quaking Strategy
- uses: your-username/ollama-doc-translator@v1
  with:
    debug-mode: true
    context-length: 4096        # Fine-grained analysis in smaller chunks
    temperature: 0.1            # Consistent translation outcome
```

#### Code Block Preservation Verification
Verify that code blocks are correctly preserved through debug files:

```markdown
<!-- Original text not provided. Please provide the Korean text you would like translated. From the chunk -->
```python
def translate_text(text):
    return translated_text
```

<!-- Please provide the Korean text you would like translated. In chunks as well Similarly Preservation -->
```python
def translate_text(text):
    return translated_text
```
```

### Artifact and Log Storage

```yaml
- name: Upload debug files
  if: always()  # Upload regardless of success or failure
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

Performance Metrics Provided in Debug Mode:

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

1. **Large Chunks Generated**
   ```yaml
   context-length: 4096  # Set lower than default (32768)
   ```

2. **Inconsistent Translation Quality**
   ```yaml
   temperature: 0.1      # More conservative translation
   max-retries: 5        # Increase retry count
   ```

3. **Code Blocks Broken**
   - Compare original and translated files in `debug_comparisons/`
   - Verify code block preservation logic works correctly

These settings can be combined to configure the optimal translation workflow for your project.

---

> **⚠️ 이 문서는 AI로 번역된 문서입니다.**
>
> **⚠️ This document has been translated by AI.**