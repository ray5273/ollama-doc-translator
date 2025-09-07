# Setup Guide

This guide explains the detailed setup options and customization methods for the Ollama document translator.

## GitHub Action Settings

### Basic Settings

The simplest form of workflow setup:

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

### Advanced Settings

An example using all available settings options:

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

    # Translation settings
    temperature: 0.3
    max-retries: 3
    skip-existing: true

    # PR settings
    create-pr: true
    pr-title: 'Document Translation Update'
    pr-branch: 'translate-docs'
    commit-message: 'docs: Added English translation for Korean documents'

    # Authentication
    github-token: ${{ secrets.GITHUB_TOKEN }}
```

## Model Settings

### Supported Models
A variety of Ollama models are available for use:

| Model Name | Size | Memory Requirement | Translation Quality | Speed |
|--------|------|-----------------|------------------|-------|
| `exaone3.5:7.8b` | 7.8B | 8GB | Very Good | Fast |
| `exaone3.5:32b` | 32B | 32GB | Top Quality | Slow |
| `llama3.1:8b` | 8B | 8GB | Good | Fast |
| `mistral:7b` | 7B | 7GB | Good | Very Fast |

### Model Performance Tuning

#### Temperature Setting
```yaml
temperature: 0.1  # For more consistent translations (conservative)
temperature: 0.3  # For balanced translations (recommended)
temperature: 0.7  # For more creative translations |
```

#### Context Length
```yaml
# Settings for long documents
context-length: 4096  # Default value: 2048 |
```

## Directory Structure Setup

### Basic Structure
```
project/
├── docs/           # Korean original content
│   ├── README.md
│   └── guide.md
└── docs-en/        # English translation
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
# Maintain the subdirectory structure
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

→ After translation:

docs-en/
├── getting-started/
│   ├── installation.md
│   └── quick-start.md
├── advanced/
│   └── configuration.md
└── README.md
```

## Workflow Trigger Settings

### File Change Detection
```yaml
on:
  push:
    paths: 
      - 'docs/**/*.md'
      - '!docs/README.md'  # Excludes README.md
    branches: [main, develop]
```

### Scheduled Execution
```yaml
on:
  schedule:
    - cron: '0 2 * * 1'  # Every Monday at 2 a.m.
  workflow_dispatch:     # Allows for manual execution as well
```

### Conditional Execution
```yaml
jobs:
  translate:
    if: contains(github.event.head_commit.message, '[translate}')
    # Executes only if the commit message contains “[translate]”
```

## Pull Request Settings

### Customizing PR Templates

You can customize the default PR body:

```yaml
pr-title: '📚 Documentation Translation: ${{ github.event.head_commit.message }}'
pr-branch: 'auto-translate-${{ github.run_number }}
```

### Automatic Reviewer Assignment

Create a `.github/CODEOWNERS` file to automatically assign reviewers to translation PRs:

```
docs-en/ @translation-team
*.md @docs-team
```

### Automatic Label Addition

Use the GitHub CLI to add labels:

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
# Process multiple files simultaneously
max-parallel-files: 3
```

### Cache Settings
```yaml
- name: Cache Ollama models
  uses: actions/cache@v4
  with:
    path: ~/.ollama
    key: ollama-models-${{ runner.os }}
```

### Conditional Translation
```yaml
# Execute translation only under specific conditions
skip-existing: true        # Skip files that have already been translated
min-file-size: 100        # Skip files smaller than 100 bytes
max-file-size: 50000      # Skip files larger than 50KB
```

## Security Settings

### Token Management
```yaml
# Use of tokens with minimum permissions
permissions:
  contents: read
  pull-requests: write
  
github-token: ${{ secrets.GITHUB_TOKEN }}
```

### Private Repositories
```yaml
# For use in private repositories
- uses: actions/checkout@v4
  with:
    token: ${{ secrets.PAT_TOKEN }}  # Personal Access Token
```

## Multi-Language Support

### Translate into Multiple Languages

```yaml
strategy:
  matrix:
    target-lang: [en, ja, zh]
    
steps:
- uses: your-username/ollama-doc-translator@v1
  with:
    target-dir: 'docs-${{ matrix.target-lang }}
    model: 'exaone3.5:7.8b'
    target-language: ${{ matrix.target-lang }}
```

## Notification Settings

### Slack Notifications
```yaml
- name: Notify Slack
  if: steps.translate.outputs.pr-url
  uses: 8398a7/action-slack@v3
  with:
    status: success
    text: 'Document translation is complete: ${{ steps.translate.outputs.pr-url }}'
```

### Email Notifications
```yaml
- name: Send Email
  uses: dawidd6/action-send-mail@v3
  with:
    subject: 'Document Translation Completed'
    body: 'A new translation PR has been created.'
```

## Debug and Analysis Settings

### Enabling Debug Mode

Debug mode allows you to view detailed information about the translation process:

```yaml
- uses: your-username/ollama-doc-translator@v1
  with:
    debug-mode: true           # Enable the generation of debug files
    github-token: ${{ secrets.GITHUB_TOKEN }}
```

### Debug Files Generated

When debug mode is enabled, the following files are automatically generated:

#### 1. Chunk Debug Files (`debug_chunks/`)
```
debug_chunks/
├── document-name_chunk_001.md     # Analysis file for each chunk
├── document-name_chunk_002.md
├── ...
└── document-name_summary.md       # Summary report of the translation process
```

Example of a chunk file header:
```markdown
<!-- DEBUG CHUNK 1/15 -->
<!-- Tokens: 245 -->
<!-- Characters: 856 -->
<!-- Source: docs/api-guide.md -->

---
Actual content of the chunk...
```

#### 2. Original vs. Translated Files (`debug_originals/`, `debug_translations/`)
```
debug_originals/
├── document-name_original_001.md   # Original chunks
├── document-name_original_002.md
└── ...
```

debug_translations/
├── document-name_translated_001.md # Translated chunks
├── document-name_translated_002.md
└── ...
```

#### 3. Comparison Files (`debug_comparisons/`)
```
debug_comparisons/
├── document-name_comparison_001.md # File comparing original and translated content
├── document-namecomparison_002.md
└── ...
```
```

### Interpretation of Debug Information

#### Example of Console Output
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
# Context length setting for processing large documents
context-length: 32768          # Model context length
```

The system automatically calculates the following safe token counts:
- **Prompt overhead**: ~200 tokens
- **Reserved space for output**: 40% of the context length
- **Safety margin**: 100 tokens
- **Actual available tokens**: Approximately 19,268 tokens (based on 32,768)

### Advanced Debugging Settings

#### Smart Choking Analysis
```yaml
# Detailed analysis of choking strategy settings
- uses: your-username/ollama-doc-translator@v1
  with:
    debug-mode: true
    context-length: 4096        # More detailed analysis with smaller chunks
    temperature: 0.1            # For consistent translation results
```

#### Verification of Code Block Preservation
Verify that code blocks are properly preserved through the debugging process:

```markdown
<!-- In the original chunk -->
```python
def translate_text(text):
    return translated_text
```

<!-- The same should be preserved in the translated chunk -->
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

Performance metrics provided in debug mode:

```bash
📊 Translation Performance Summary:
   ⏱️ Total time: 2m 34s
   📄 Files processed: 12
   🔄 Total chunks: 67
   📈 Average chunk size: 1,089 tokens
   ⚡ Translation speed: ~425 tokens/sec
   🎯 Success rate: 100% (0 retries needed)
```

### Problem-Solving Guide

#### Common Issues

1. **Chunks are created too large**
   ```yaml
   context-length: 4096  # Set to a value lower than the default (32768)
   ```

2. **Inconsistent translation quality**
   ```yaml
   temperature: 0.1      # More conservative translation settings
   max-retries: 5        # Increase the number of retries
   ```

3. **Code blocks are broken**
   - Compare the original with the translated version in the `debug_comparisons/` files
   - Ensure that the logic for preserving code blocks is working correctly

By combining these settings, you can configure an optimal translation workflow tailored to your project.

---

> **⚠️ 이 문서는 AI로 번역된 문서입니다.**
>
> **⚠️ This document has been translated by AI.**