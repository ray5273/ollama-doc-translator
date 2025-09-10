# Setup Guide

This guide explains detailed setup options and customization methods for the Ollama document translator.

## GitHub Action Configuration

### Basic Setup

The simplest workflow setup:

```yaml
name: 문서 번역

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
    # 서버 설정
    ollama-url: 'http://localhost:11434'
    model: 'exaone3.5:7.8b'
    
    # 디렉토리 설정
    source-dir: 'docs'
    target-dir: 'docs-en'
    file-pattern: '**/*.md'
    
    # 번역 설정
    temperature: 0.3
    max-retries: 3
    skip-existing: true
    
    # PR 설정
    create-pr: true
    pr-title: '문서 번역 업데이트'
    pr-branch: 'translate-docs'
    commit-message: 'docs: 한국어 문서 영어 번역 추가'
    
    # 인증
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
temperature: 0.1  # 더 일관된 번역 (보수적)
temperature: 0.3  # 균형잡힌 번역 (권장)
temperature: 0.7  # 더 창의적인 번역
```

#### Context Length
```yaml
# 긴 문서를 위한 설정
context-length: 4096  # 기본값: 2048
```

## Directory Structure Setup

### Basic Structure
```
project/
├── docs/           # 한국어 원본
│   ├── README.md
│   └── guide.md
└── docs-en/        # 영어 번역본
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
# 하위 디렉토리 구조 유지
source-dir: 'docs'
target-dir: 'docs-en'
file-pattern: '**/*.md'  # 모든 하위 디렉토리 포함
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

→ 번역 후

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
      - '!docs/README.md'  # README.md 제외
    branches: [ main, develop ]
```

### Scheduled Execution
```yaml
on:
  schedule:
    - cron: '0 2 * * 1'  # 매주 월요일 오전 2시
  workflow_dispatch:     # 수동 실행 허용
```

### Conditional Execution
```yaml
jobs:
  translate:
    if: contains(github.event.head_commit.message, '[translate]')
    # 커밋 메시지에 [translate]가 포함된 경우만 실행
```

## Pull Request Setup

### PR Template Customization

You can customize the default PR body:

```yaml
pr-title: '📚 문서 번역: ${{ github.event.head_commit.message }}'
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
# 여러 파일을 동시에 처리
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
# 특정 조건에서만 번역 실행
skip-existing: true        # 이미 번역된 파일 스킵
min-file-size: 100        # 100바이트 미만 파일 스킵
max-file-size: 50000      # 50KB 초과 파일 스킵
```

## Security Settings

### Token Management
```yaml
# 최소 권한 토큰 사용
permissions:
  contents: read
  pull-requests: write
  
github-token: ${{ secrets.GITHUB_TOKEN }}
```

### Private Repository
```yaml
# 프라이빗 저장소에서 사용
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
    text: '문서 번역이 완료되었습니다: ${{ steps.translate.outputs.pr-url }}'
```

### Email Notification
```yaml
- name: Send Email
  uses: dawidd6/action-send-mail@v3
  with:
    subject: '문서 번역 완료'
    body: '새로운 번역 PR이 생성되었습니다.'
```

## Debug and Analysis Settings

### Enable Debug Mode

Through debug mode, you can inspect detailed information about the translation process:

```yaml
- uses: your-username/ollama-doc-translator@v1
  with:
    debug-mode: true           # 디버그 파일 생성 활성화
    github-token: ${{ secrets.GITHUB_TOKEN }}
```

### Generated Debug Files

When debug mode is activated, the following files are automatically generated:

#### 1. Chunking Debug Files (`debug_chunks/`)
```
debug_chunks/
├── document-name_chunk_001.md     # 각 청크별 분석 파일
├── document-name_chunk_002.md
├── ...
└── document-name_summary.md       # 청킹 요약 보고서
```

Example header of each chunk file:
```markdown
<!-- DEBUG CHUNK 1/15 -->
<!-- Tokens: 245 -->
<!-- Characters: 856 -->
<!-- Source: docs/api-guide.md -->

---

실제 청크 내용...
```

#### 2. Translation Comparison Files (`debug_originals/`, `debug_translations/`, `debug_comparisons/`)
```
debug_originals/
├── document-name_original_001.md   # 원본 청크들
├── document-name_original_002.md
└── ...

debug_translations/
├── document-name_translated_001.md # 번역된 청크들
├── document-name_translated_002.md
└── ...

debug_comparisons/
├── document-name_comparison_001.md # 원본-번역 비교 파일
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
# 대용량 문서 처리를 위한 컨텍스트 길이 설정
context-length: 32768          # 모델 컨텍스트 길이
```

System Automatically Calculated Safe Token Count:
- **Prompt Overhead**: ~200 tokens
- **Output Reserved Space**: 40% of context length
- **Safety Margin**: 100 tokens
- **Available Usage**: Approximately 19,268 tokens (based on 32,768)

### Advanced Debugging Settings

#### Smart Chunking Analysis
```yaml
# 청킹 전략 상세 분석
- uses: your-username/ollama-doc-translator@v1
  with:
    debug-mode: true
    context-length: 4096        # 작은 청크로 더 세밀한 분석
    temperature: 0.1            # 일관된 번역 결과
```

#### Code Block Preservation Verification
Verify that code blocks are correctly preserved through debug files:

```markdown
<!-- 원본 청크에서 -->
```python
def translate_text(text):
    return translated_text
```

<!-- 번역 청크에서도 동일하게 보존 -->
```python
def translate_text(text):
    return translated_text
```
```

### Artifact and Log Storage

```yaml
- name: Upload debug files
  if: always()  # 성공/실패 관계없이 업로드
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

3. **Code Blocks Breaking**
   - Compare original and translated in `debug_comparisons/` file
   - Verify code block preservation logic is functioning correctly

By combining these settings, you can configure an optimal translation workflow for your project.

---

> **⚠️ 이 문서는 AI로 번역된 문서입니다.**
>
> **⚠️ This document has been translated by AI.**