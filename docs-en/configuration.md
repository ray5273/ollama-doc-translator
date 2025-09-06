# Setup Guide

This document explains the detailed setup options and customization methods for the Ollama document translator.

## GitHub Action Setup

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

An example that utilizes all setting options:

```yaml
- uses: your-username/ollama-doc-translator@v1
  with:
```

# Server Settings
    ollama-url: 'http://localhost:11434'
    model: 'exaone3.5:7.8b'

# Directory Settings
source-dir: 'docs'
target-dir: 'docs-en'
file-pattern: '**/*.md'

# Translation Settings
temperature: 0.3
max-retries: 3
skip-existing: true

# PR Settings
create-pr: true
pr-title: 'Document Translation Update'
pr-branch: 'translate-docs'
commit-message: 'docs: Adding English translation for Korean documents'

# Authentication
github-token: ${{ secrets.GITHUB_TOKEN }}

## Model Settings

### Supported Models

A variety of Ollama models are available for use:

| Model Name | Size | Memory Requirement | Translation Quality | Speed |
|--------|------|---------------|-----------|------|
| `exaone3.5:7.8b` | 7.8B | 8GB | Very Good | Fast |
| `exaone3.5:32b` | 32B | 32GB | Highest Quality | Slow |
| `llama3.1:8b` | 8B | 8GB | Good | Fast |
| `mistral:7b` | 7B | 7GB | Good | Very Fast |

### Model Performance Tuning

#### Temperature Setting
```yaml
temperature: 0.1  # More consistent translation (conservative)
temperature: 0.3  # Balanced translation (recommended)
temperature: 0.7  # More creative translation |
```

#### Context Length
```yaml
```

# Settings for long documents
context-length: 4096  # Default value: 2048

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

### Handling of Subdirectories
```yaml
```

# Maintain Subdirectory Structure
source-dir: 'docs'
target-dir: 'docs-en'
file-pattern: '**/*.md'  # Include all subdirectories

Example:
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
    if: contains(github.event.head_commit.message, '[translate]")
```

# Execute only if the commit message contains [translate].

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
```

# Processing multiple files simultaneously
max-parallel-files: 3

### Cache settings
```yaml
- name: Cache Ollama models
  uses: actions/cache@v4
  with:
    path: ~/.ollama
    key: ollama-models-${{ runner.os }}
```

### Conditional translation
```yaml
```

# Translate Only Under Specific Conditions
skip-existing: true        # Skip files that have already been translated
min-file-size: 100        # Skip files smaller than 100 bytes
max-file-size: 50000      # Skip files larger than 50KB

## Security Settings

### Token Management
```yaml
```

# Using minimum permission tokens
permissions:
  contents: read
  pull-requests: write

github-token: ${{ secrets.GITHUB_TOKEN }}

### Private repository
```yaml
```

# For use in private repositories
- uses: actions/checkout@v4
  with:
    token: ${{ secrets.PAT_TOKEN }}  # Personal Access Token

## Multi-Language Support

### Translation into Multiple Languages

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
    text: 'Document translation is complete: ${{ steps.translateoutputs.pr-url }}'
```

### Email Notifications
```yaml
- name: Send Email
  uses: dawidd6/action-send-mail@v3
  with:
    subject: 'Document Translation Completed'
    body: 'A new translation PR has been created.'
```

## Debug Settings for Problem Solving

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

By combining these settings, you can configure the most optimal translation workflow for your project.

---

> **⚠️ 이 문서는 AI로 번역된 문서입니다.**
>
> **⚠️ This document has been translated by AI.**