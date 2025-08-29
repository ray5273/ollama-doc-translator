# Setup Guide

Ollama translator's detailed configuration options and customization methods are explained.

## GitHub Action Setup

### Basic Settings

Simplest Workflow Setup:

```yaml
name: Document Translation
```

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

### Advanced Settings

All settings options utilized example:

```yaml
- uses: your-username/ollama-doc-translator@v1
  with:
    # Server configuration
    ollama-url: 'http://localhost:11434'
    model: 'exaone3.5:7.8b'
    
    # Directory configuration
    source-dir: 'docs'
    target-dir: 'docs-en'
    file-pattern: '**/*.md'
    
    # Translation configuration
    temperature: 0.3
    max-retries: 3
    skip-existing: true
    
    # PR configuration
    create-pr: true
    pr-title: 'Document translation update'
    pr-branch: 'translate-docs'
    commit-message: 'docs: Add English translation for Korean documents'
    
    # Authentication
    github-token: ${{ secrets.GITHUB_TOKEN }}
```

## Model Configuration

### Supported Models

You can use various Ollama models:

| Model Name | Size | Memory Requirement | Translation Quality | Speed |
|--------|------|---------------|-----------|------|
| `exaone3.5:7.8b` | 7.8B | 8GB | Excellent | Fast |
| `exaone3.5:32b` | 32B | 32GB | Superior | Slow |
| `llama3.1:8b` | 8B | 8GB | Good | Fast |
| `mistral:7b` | 7B | 7GB | Good | Very Fast |

### Model Performance Tuning

#### Temperature Setting
```yaml
temperature: 0.1  # More consistent translation (conservative)
temperature: 0.3  # Balanced translation (recommended)
temperature: 0.7  # More creative translation
```

#### Context Length
```yaml
# Configuration for long documents
context-length: 4096  # Default: 2048
```

## Setting Up the Directory Structure

### Basic Structure
```
project/
├── docs/           # Korean original
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
# Maintain subdirectory structure
source-dir: 'docs'
target-dir: 'docs-en'
file-pattern: '**/*.md'  # Include all subdirectories
```

```
docs/
├── getting-started/
│   ├── installation.md
│   └── quick-start.md
├── advanced/
│   └── configuration.md
└── README.md
```

→ Translation after

docs-en/
├── getting-started/
│   ├── installation.md
│   └── quick-start.md
├── advanced/
│   └── configuration.md
└── README.md

## 워크플로우 트리거 설정

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

### Schedule Execution
```yaml
on:
  schedule:
    - cron: '0 2 * * 1'  # Every Monday at 2:00 AM
  workflow_dispatch:     # Allow manual triggering
```

### Conditional Execution
```yaml
jobs:
  translate:
    if: contains(github.event.head_commit.message, '[translate]')
    # Run only if the commit message contains '[translate]'
```

## Pull Request Settings

### PR Template Customization

You can customize the default PR body:

```yaml
pr-title: '📚 Document Translation: ${{ github.event.head_commit.message }}'
pr-branch: 'auto-translate-${{ github.run_number }}'
```

### Automatic Reviewer Assignment

Create a `.github/CODEOWNERS` file to automatically assign reviewers to translation PRs:

```
docs-en/ @translation-team
*.md @docs-team
```

### Automatic Label Addition

GitHub CLI를 사용하여 라벨 추가:

Using the GitHub CLI to add labels:

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
# Process multiple files concurrently
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
# Execute translation only under specific conditions
skip-existing: true        # Skip files that are already translated
min-file-size: 100        # Skip files smaller than 100 bytes
max-file-size: 50000      # Skip files larger than 50KB
```

## Security Settings

### Token Management
```yaml
# Use least privilege token
permissions:
  contents: read
  pull-requests: write
  
github-token: ${{ secrets.GITHUB_TOKEN }}
```

### Private Repository
```yaml
# For use in a private repository
- uses: actions/checkout@v4
  with:
    token: ${{ secrets.PAT_TOKEN }}  # Personal Access Token
```

## Multilingual Support

### Multiple Language Translation

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
    text: 'Document translation completed: ${{ steps.translate.outputs.pr-url }}'
```

### Email Notification
```yaml
- name: Send Email
  uses: dawidd6/action-send-mail@v3
  with:
    subject: 'Document Translation Complete'
    body: 'A new translation PR has been created.'
```

## Debug Configuration for Problem Solving

### Detailed Logging
```yaml
- uses: your-username/ollama-doc-translator@v1
  with:
    debug: true
    verbose: true
```

### Artifact Storage
```yaml
- name: Upload translation logs
  if: failure()
  uses: actions/upload-artifact@v4
  with:
    name: translation-logs
    path: translation-*.log
```

You can combine these settings to create the optimal translation workflow for your project.