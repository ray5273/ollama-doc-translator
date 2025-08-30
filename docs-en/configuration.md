# Setup Guide

This guide provides detailed configuration options and customization methods for the Ollama document translation workflow.

## GitHub Action Setup

### Basic Setup

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

### Advanced Setup

Example utilizing all configuration options:

```yaml
- uses: your-username/ollama-doc-translator@v1
  with:
    # Server Configuration
    ollama-url: 'http://localhost:11434'
    model: 'exaone3.5:7.8b'
    
    # Directory Configuration
    source-dir: 'docs'
    target-dir: 'docs-en'
    file-pattern: '**/*.md'
    
    # Translation Configuration
    temperature: 0.3  # Default: 0.3
    max-retries: 3
    skip-existing: true
    
    # PR Configuration
    create-pr: true
    pr-title: 'Document Translation Update'
    pr-branch: 'translate-docs'
    commit-message: 'docs: Add Korean to English Translation'
    
    # Authentication
    github-token: ${{ secrets.GITHUB_TOKEN }}
```

## Model Configuration

### Supported Models

| Model Name       | Size | Memory Requirement | Translation Quality | Speed |
|------------------|------|--------------------|---------------------|-------|
| `exaone3.5:7.8b` | 7.8B | 8GB                | Excellent           | Fast  |
| `exaone3.5:32b`  | 32B  | 32GB               | Best                | Slow  |
| `llama3.1:8b`    | 8B   | 8GB                | Good                | Fast  |
| `mistral:7b`     | 7B   | 7GB                | Good                | Very Fast |

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

## Directory Structure Configuration

### Default Structure
```
project/
├── docs/           # Original Korean documents
│   ├── README.md
│   └── guide.md
└── docs-en/        # Translated English documents
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
# Preserves subdirectory structure
source-dir: 'docs'
target-dir: 'docs-en'
file-pattern: '**/*.md'  # Includes all subdirectories
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

→ Translated Result

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
    # Execute only if '[translate]' is in the commit message
```

## Pull Request Configuration

### Customizing PR Template

Customize the default PR body:

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
- name: Add Labels to PR
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
- name: Cache Ollama Models
  uses: actions/cache@v4
  with:
    path: ~/.ollama
    key: ollama-models-${{ runner.os }}
```

### Conditional Translation
```yaml
# Translate only under specific conditions
skip-existing: true        # Skip files already translated
min-file-size: 100         # Skip files smaller than 100 bytes
max-file-size: 50000       # Skip files larger than 50KB
```

## Security Configuration

### Token Management
```yaml
# Use minimal permissions token
permissions:
  contents: read
  pull-requests: write
  
github-token: ${{ secrets.GITHUB_TOKEN }}
```

### Private Repository Usage
```yaml
# For private repositories
- uses: actions/checkout@v4
  with:
    token: ${{ secrets.PAT_TOKEN }}  # Personal Access Token
```

## Multi-Language Support

### Translating into Multiple Languages

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
    text: 'Document translation completed: ${{ steps.translate.outputs.pr-url }}'
```

### Email Notifications
```yaml
- name: Send Email
  uses: dawidd6/action-send-mail@v3
  with:
    subject: 'Document Translation Complete'
    body: 'A new translation PR has been created.'
```

## Troubleshooting Debug Settings

### Detailed Logging
```yaml
- uses: your-username/ollama-doc-translator@v1
  with:
    debug: true
    verbose: true
```

### Artifact Storage
```yaml
- name: Upload Translation Logs
  if: failure()
  uses: actions/upload-artifact@v4
  with:
    name: translation-logs
    path: translation-*.log
```

By combining these settings, you can tailor your translation workflow to best suit your project needs.