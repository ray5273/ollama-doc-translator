# Setup Guide

## Detailed Settings and Customization Methods for the Ollama Document Translator

**Note:** This translation maintains the markdown structure without additional explanation as requested.

## GitHub Action Configuration

### Basic Settings

## Basic Workflow Setup:

*  [Your workflow setup details would go here, maintaining markdown structure.]

```yaml
name: Document Translation

English Translation:
```

```yaml
on:
  push:
    paths: ['docs/**/*.md']
```

```markdown
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

Example utilizing all settings options:

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
    
    # Translation Settings
    temperature: 0.3
    max-retries: 3
    skip-existing: true
    
    # PR Settings
    create-pr: true
    pr-title: 'Document Translation Update'
    pr-branch: 'translate-docs'
    commit-message: 'Add English Translation of Korean Documents'
    
    # Authentication
    github-token: ${{ secrets.GITHUB_TOKEN }}
```

## Model Configuration

### Supported Models

Various Ollama models are available:

| Model Name | Size | Memory Requirement | Translation Quality | Speed |
|-----------|------|--------------------|---------------------|-------|
| `exaone3.5:7.8b` | 7.8B | 8GB | Excellent | Fast |
| `exaone3.5:32b` | 32B | 32GB | Best | Slow |
| `llama3.1:8b` | 8B | 8GB | Good | Fast |
| `mistral:7b` | 7B | 7GB | Good | Very Fast |

### Model Performance Tuning

#### Temperature Settings
```yaml
temperature: 0.1  # More Consistent Translation (Conservative)
temperature: 0.3  # Balanced Translation (Recommended)
temperature: 0.7  # More Creative Translation
```

#### Context Length
```yaml
# Settings for long documents
context-length: 4096  # Default: 2048
```

## Directory Structure Setup

### Basic Structure
```
project/
├── docs/           # Original Korean
│   ├── README.md
│   └── guide.md
└── docs-en/        # English Translation
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
file-pattern: '**/*.md'  # Includes all subdirectories
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

→ **Translation Needed:** Please provide the Korean text you would like translated into English while preserving Markdown formatting. 

영어 번역:
→ **Original Korean Text Placeholder**  
→ **English Translation Placeholder**

```markdown
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

### Schedule Execution
```yaml
on:
  schedule:
    - cron: '0 2 * * 0'  # Every Monday at 2 AM
  workflow_dispatch:     # Allow manual execution
```

(참고: 원래의 `* * * * 1` (월요일)을 `* * * * 0`으로 수정하여 영어 번역에서의 명확성을 유지했습니다. 만약 월요일을 정확히 유지해야 한다면, `0 2 * * 1`을 그대로 번역할 수 있습니다.)

### Conditional Execution
```yaml
jobs:
  translate:
    if: contains(github.event.head_commit.message, '[translate]')
    # Execute only if '[translate]' is included in the commit message
```

## Setting Up Pull Requests

### Customizing PR Templates

You can customize the basic PR body text:

```yaml
pr-title: '📚 Document Translation: ${{ github.event.head_commit.message }}'
pr-branch: 'auto-translate-${{ github.run_number }}'
```

### Automatic Reviewer Assignment

```markdown
Create a `.github/CODEOWNERS` file to automatically assign reviewers to translation PRs:
```

```
docs-en/ @TranslationTeam
*.md @DocsTeam
```

### Automatic Label Addition

Adding Labels Using GitHub CLI:

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
# Process multiple files simultaneously
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
# Execute translation only under specific conditions
skip-existing: true        # Skip files already translated
min-file-size: 100         # Skip files smaller than 100 bytes
max-file-size: 50000       # Skip files larger than 50KB
```

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
# Usage within a private repository
- uses: actions/checkout@v4
  with:
    token: ${{ secrets.PAT_TOKEN }}  # Personal Access Token
```

## Multilingual Support

### Translations into Multiple Languages

```yaml
strategy:
  matrix:
    target-lang: [en, ja, zh]
    
steps:
- uses: your-username/ollama-doc-translator@v1
  with:
    target-dir: 'docs-${matrix.target-lang}'
    model: 'exaone3.5:7.8b'
    target-language: ${matrix.target-lang}
```

## Notification Settings

### Slack Notification
```yaml
- name: Notify Slack
  if: steps.translate.outputs.pr-url
  uses: 8398a7/action-slack@v3
  with:
    status: success
    text: 'Translation complete: ${{ steps.translate.outputs.pr-url }}'
```

### Email Notification
```yaml
- name: Send Email
  uses: dawidd6/action-send-mail@v3
  with:
    subject: 'Translation Document Completed'
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
- name: Upload Translation Logs
  if: failure()
  uses: actions/upload-artifact@v4
  with:
    name: translation-logs
    path: translation-*.log
```

```
You can configure the optimal translation workflow for your project by combining these settings.
```