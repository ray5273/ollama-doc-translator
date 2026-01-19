# Setup Guide

This document explains the detailed configuration options and customization methods for the Ollama documentation translator.

## GitHub Action Configuration

### Basic Configuration

The simplest workflow configuration:

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

Example using all configuration options:

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
    commit-message: 'docs: Korean Document English Translation Additional'
    
    # Certification
    github-token: ${{ secrets.GITHUB_TOKEN }}
```

## Model Settings

### Supported Models

You can use various Ollama models:

| Model Name | Size | Memory Requirement | Translation Quality | Speed |
|---|---|---|---|---|
| `exaone3.5:7.8b` | 7.8B | 8GB | Very Good | Fast |
| `exaone3.5:32b` | 32B | 32GB | Best | Slow |
| `llama3.1:8b` | 8B | 8GB | Good | Fast |
| `mistral:7b` | 7B | 7GB | Good | Very Fast |

### Model Performance Adjustment

#### Temperature Setting
```yaml
temperature: 0.1  # More consistent translation (conservative)
temperature: 0.3  # Balanced translation (recommended)
temperature: 0.7  # More creative translation
```

#### Context Length
```yaml
# Settings for long documents
context-length: 4096  # Default: 2048
```

## Directory Structure Configuration

### Basic Structure
```
project/
├── docs/           # Original Korean text
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
# Maintain the existing subdirectory structure.
source-dir: 'docs'
target-dir: 'docs-en'
file-pattern: '**/*.md'  # Including all subdirectories.
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

## Workflow Trigger Configuration

### File Change Detection
```yaml
on:
  push:
    paths: 
      - 'docs/**/*.md'
      - '!docs/README.md'  # Excluding README.md
    branches: [ main, develop ]
```

### Scheduled Execution
```yaml
on:
  schedule:
    - cron: '0 2 * * 1'  # Every Monday at 2:00 AM
  workflow_dispatch:     # Allow manual execution
```

### Conditional Execution
```yaml
jobs:
  translate:
    if: contains(github.event.head_commit.message, '[translate]')
    # Execute only if the commit message contains "[translate]
```

## Pull Request Configuration

### Customizing PR Template

You can customize the basic PR content:

```yaml
pr-title: '📚 Document Translation: ${{ github.event.head_commit.message }}'
pr-branch: 'auto-translate-${{ github.run_number }}'
```

### Automatic Reviewer Assignment

Create a `.github/CODEOWNERS` file to automatically assign reviewers to the translation PR:

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
# Process multiple files simultaneously.
max-parallel-files: 3
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
# Run translation only under specific conditions.
skip-existing: true        # Skip already translated files
min-file-size: 100        # Skip files smaller than 100 bytes.
max-file-size: 50000      # Skip files exceeding 50KB
```

## Security Settings

### Token Management
```yaml
# Use of least privilege tokens
permissions:
  contents: read
  pull-requests: write
  
github-token: ${{ secrets.GITHUB_TOKEN }}
```

### Private Repository
```yaml
# For use in a private repository.
- uses: actions/checkout@v4
  with:
    token: ${{ secrets.PAT_TOKEN }}  # Personal Access Token
```

## Multi-language Support

### Translation in Multiple Languages

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

### Slack Notifications
```yaml
- name: Notify Slack
  if: steps.translate.outputs.pr-url
  uses: 8398a7/action-slack@v3
  with:
    status: success
    text: 'Document Translation Completed.: ${{ steps.translate.outputs.pr-url }}'
```

### Email Notifications
```yaml
- name: Send Email
  uses: dawidd6/action-send-mail@v3
  with:
    subject: 'Document Translation Completed'
    body: 'New Translation PR Created.'
```

## Debug and Analysis Settings

### Enable Debug Mode

You can check detailed information about the translation process through debug mode:

```yaml
- uses: your-username/ollama-doc-translator@v1
  with:
    debug-mode: true           # Enable the creation of debug files.
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
└── document-name_summary.md       # Summary Report on Cleaning
```

Example of chunk file header:
```markdown
<!-- DEBUG CHUNK 1/15 -->
<!-- Tokens: 245 -->
<!-- Characters: 856 -->
<!-- Source: docs/api-guide.md -->

---

Real chunk Content...
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
# Setting the context length for processing large documents.
context-length: 32768          # Model context length
```

Number of safe tokens automatically calculated by the system:
- **Prompt overhead**: ~200 tokens
- **Output reservation**: 40% of context length
- **Safety margin**: 100 tokens
- **Actually usable**: Approximately 19,268 tokens (based on 32,768)

<!-- Translation Also in chunks. Similarly Preservation -->
<!-- Original From chunks -->
### Advanced Debugging Settings

#### Smart Chunk Analysis
```


### Save artifacts and logs

```

#### Code Block Preservation Verification
Verify that code blocks are correctly preserved through the debug file:

```markdown
<!-- From original chunk -->
```python
def translate_text(text):
    return translated_text
```

#### Artifacts and Logs Storage

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

#### Frequently Encountered Issues

1. **Chunks are generated too large**
   ```yaml
   context-length: 4096  # Set to a smaller value than the default (32768)
   ```

2. **Inconsistent translation quality**
   ```yaml
   temperature: 0.1      # Use a more conservative translation
   max-retries: 5        # Increase the number of retries
   ```

3. **Code blocks are broken**
   - Compare the original and translated code in the `debug_comparisons/` file
   - Verify that the logic for preserving code blocks is functioning correctly

You can combine these settings to create the optimal translation workflow for your project.

---

> **⚠️ 이 문서는 AI로 번역된 문서입니다.**
>
> **⚠️ This document has been translated by AI.**