# Setup Guide

Explaining the detailed settings options and customization methods of the Ollama document translator.

## Setting up GitHub Actions

English Translation:

### Basic settings

The simplest form of workflow setup:

name: Document Translation

on:
  push:
    paths: ["docs/**/*.md"]

jobs:
  translate:
    runs-on: self-hosted
    steps:
    - uses: actions/checkout@v4
    - uses: your-username/ollama-doc-translator@v1
      with:
        github-token: ${{ secrets.GITHUB_TOKEN }}

Advanced Settings

All settings options utilized example:

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
    pr-title: "Document translation update"
    pr-branch: 'translate-docs'
    commit-message: "docs: Add English translations for Korean documents"
    
    # Authentication
    github-token: ${{ secrets.GITHUB_TOKEN }}
```

## Model Setup

Supported models: (The original information to translate was not provided, so I can only provide the English translation of the given Korean text.)

You can use various Ollama models:

| Model Name | Size | Memory Required | Translation Quality | Speed |
 |------------|------|---------------|-----------|------|
 | `exaone3.5:7.8b` | 7.8B | 8GB | Excellent | Fast |
 | `exaone3.5:32b` | 32B | 32GB | Best | Slow |
 | `llama3.1:8b` | 8B | 8GB | Good | Fast |
 | `mistral:7b` | 7B | 7GB | Good | Very Fast |

Model performance adjustment

```yaml
 temperature: 0.1  # more consistent translation (conservative)
 temperature: 0.3  # balanced translation (recommended)
 temperature: 0.7  # more creative translation
```

```yaml
 # Settings for long documents
 context-length: 4096  # Default: 2048

## Directory structure setup

English translation:

```
project/
│
│  ┝ docs/           # Original Korean
│     │
│     │   ├── README.md
│     │   └── guide.md
│
│  ┝ docs-en/        # English translation
│     │
│     │   ├── README.md
│     │   └── guide.md
```

Custom structure
```yaml
sourceDir: "korean-docs"
targetDir: "english-docs"
filePattern: "**/*.{md,mdx}"
```

Handling of Subdirectories
```yaml
# Maintain subdirectory structure
source-dir: "docs"
target-dir: "docs-en"
file-pattern: "**/*.md" # Includes all subdirectories
```

Example:
```
docs/
│
└─ folder: getting-started/
    │
    ├─ file: installation.md
    └─ file: quick-start.md
    
└─ folder: advanced/
    │
    └─ file: configuration.md
    
└─ file: README.md
```

Original Korean Text: (No input provided)
Translated English Text: (No output to be provided as the original Korean text is missing)

docs-en/
|-- getting-started/
|   |-- installation.md
|   `-- quick-start.md
|
`-- advanced/
    `-- configuration.md
   
`-- README.md
```

## Workflow Trigger Setup

English translation (YAML format):
```yaml
on:
  push:
    paths: 
      - "docs/**/*.md"
      - "!docs/README.md"  # Exclude README.md
    branches: [ main, develop ]
```

schedule:
   on:
     schedule:
       - cron: "0 2 * * 1"  # Every Monday at 2:00 AM
     workflow_dispatch:    # Allow manual execution

```yaml
 jobs:
   translate:
     if: contains(github.event.head_commit.message, '[translate]')
     # Runs only when the commit message contains [translate]

## Setting up a Pull Request

English text translation:
### PR template customization

You can customize the basic PR body:

```yaml
 pr-title: "📚 Document Translation: ${{ github.event.head_commit.message }}"
 pr-branch: "auto-translate-${{ github.run_number }}"
```

Reviewer Automatic Assignment

Create a `.github/CODEOWNERS` file to automatically assign reviewers for translation PRs:

English translation:
```
docs-en/ @translation-team
*.md @docs-team
```

English Translation:
### Automatically Add Labels

Adding a label using the GitHub CLI:

```yaml
 - name: Add labels to PR
   run: |
     gh pr edit ${{ steps.translate.outputs.pr-number }}
      --add-label "documentation"
      --add-label "translation"
      --add-label "automated"
```

## Performance Optimization

Parallel processing
```yaml
# Process multiple files at once
max-parallel-files: 3
```

Cache settings
```yaml
- name: Cache Ollama models
  uses: actions/cache@v4
  with:
    path: ~/.ollama
    key: ollama-models-${{ runner.os }}
```

```yaml
# Translation will only be executed under certain conditions
skip-existing: true        # Skip files that are already translated
min-file-size: 100        # Skip files smaller than 100 bytes
max-file-size: 50000      # Skip files larger than 50KB
```

## Security Setup

```yaml
# Minimum permissions token usage
permissions:
  contents: read
  pull-requests: write
github-token: ${{ secrets.GITHUB_TOKEN }}
```

English translation (YAML format):
```yaml
# Used in the Privacy Storage
- uses: actions/checkout@v4
  with:
    token: ${{ secrets.PAT_TOKEN }}  # Personal Access Token
```

## Multi-language support

Multiple Languages Translation in English:

strategy:
  matrix:
    target_lang: [en, ja, zh]
    
steps:
- uses: your-username/ollama-doc-translator@v1
  with:
    target_dir: 'docs-${{ matrix.target_lang }}'
    model: 'exaone3.5:7.8b'
    target_language: ${{ matrix.target_lang }}

## Notification Settings

```yaml
- name: Notify Slack
  if: steps.translate.outputs.pr-url
  uses: 8398a7/action-slack@v3
  with:
    status: success
    text: "The document translation is completed: ${{ steps.translate.outputs.pr-url }}"

```yaml
- name: Send Email
  uses: dawidd6/action-send-mail@v3
  with:
    subject: 'Document Translation Completed'
    body: 'A new translation PR has been created.'
```

## Debug settings for problem solving

```yaml
- uses: your-username/ollama-doc-translator@v1
  with:
    debug: true
    verbose: true
```

```yaml
- name: Upload translation logs
  if: failure()
  uses: actions/upload-artifact@v4
  with:
    name: translation-logs
    path: translation-*.log
```

You can combine these settings to create an optimal translation workflow for your project.