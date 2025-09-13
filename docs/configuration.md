# 설정 가이드

Ollama 문서 번역기의 상세한 설정 옵션과 커스터마이징 방법을 설명합니다.

## GitHub Action 설정

### 기본 설정

가장 간단한 형태의 워크플로우 설정:

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

### 고급 설정

모든 설정 옵션을 활용한 예제:

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

## 모델 설정

### 지원하는 모델

다양한 Ollama 모델을 사용할 수 있습니다:

| 모델명 | 크기 | 메모리 요구량 | 번역 품질 | 속도 |
|--------|------|---------------|-----------|------|
| `exaone3.5:7.8b` | 7.8B | 8GB | 매우 좋음 | 빠름 |
| `exaone3.5:32b` | 32B | 32GB | 최고 | 느림 |
| `llama3.1:8b` | 8B | 8GB | 좋음 | 빠름 |
| `mistral:7b` | 7B | 7GB | 좋음 | 매우 빠름 |

### 모델 성능 조정

#### Temperature 설정
```yaml
temperature: 0.1  # 더 일관된 번역 (보수적)
temperature: 0.3  # 균형잡힌 번역 (권장)
temperature: 0.7  # 더 창의적인 번역
```

#### 컨텍스트 길이
```yaml
# 긴 문서를 위한 설정
context-length: 4096  # 기본값: 2048
```

## 디렉토리 구조 설정

### 기본 구조
```
project/
├── docs/           # 한국어 원본
│   ├── README.md
│   └── guide.md
└── docs-en/        # 영어 번역본
    ├── README.md
    └── guide.md
```

### 커스텀 구조
```yaml
source-dir: 'korean-docs'
target-dir: 'english-docs'
file-pattern: '**/*.{md,mdx}'
```

### 하위 디렉토리 처리
```yaml
# 하위 디렉토리 구조 유지
source-dir: 'docs'
target-dir: 'docs-en'
file-pattern: '**/*.md'  # 모든 하위 디렉토리 포함
```

예시:
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

## 워크플로우 트리거 설정

### 파일 변경 감지
```yaml
on:
  push:
    paths: 
      - 'docs/**/*.md'
      - '!docs/README.md'  # README.md 제외
    branches: [ main, develop ]
```

### 스케줄 실행
```yaml
on:
  schedule:
    - cron: '0 2 * * 1'  # 매주 월요일 오전 2시
  workflow_dispatch:     # 수동 실행 허용
```

### 조건부 실행
```yaml
jobs:
  translate:
    if: contains(github.event.head_commit.message, '[translate]')
    # 커밋 메시지에 [translate]가 포함된 경우만 실행
```

## Pull Request 설정

### PR 템플릿 커스터마이징

기본 PR 본문을 커스터마이징할 수 있습니다:

```yaml
pr-title: '📚 문서 번역: ${{ github.event.head_commit.message }}'
pr-branch: 'auto-translate-${{ github.run_number }}'
```

### 리뷰어 자동 할당

`.github/CODEOWNERS` 파일을 생성하여 번역 PR에 자동으로 리뷰어를 할당:

```
docs-en/ @translation-team
*.md @docs-team
```

### 라벨 자동 추가

GitHub CLI를 사용하여 라벨 추가:

```yaml
- name: Add labels to PR
  run: |
    gh pr edit ${{ steps.translate.outputs.pr-number }} \
      --add-label "documentation" \
      --add-label "translation" \
      --add-label "automated"
```

## 성능 최적화

### 병렬 처리
```yaml
# 여러 파일을 동시에 처리
max-parallel-files: 3
```

### 캐시 설정
```yaml
- name: Cache Ollama models
  uses: actions/cache@v4
  with:
    path: ~/.ollama
    key: ollama-models-${{ runner.os }}
```

### 조건부 번역
```yaml
# 특정 조건에서만 번역 실행
skip-existing: true        # 이미 번역된 파일 스킵
min-file-size: 100        # 100바이트 미만 파일 스킵
max-file-size: 50000      # 50KB 초과 파일 스킵
```

## 보안 설정

### 토큰 관리
```yaml
# 최소 권한 토큰 사용
permissions:
  contents: read
  pull-requests: write
  
github-token: ${{ secrets.GITHUB_TOKEN }}
```

### 프라이빗 저장소
```yaml
# 프라이빗 저장소에서 사용
- uses: actions/checkout@v4
  with:
    token: ${{ secrets.PAT_TOKEN }}  # Personal Access Token
```

## 다중 언어 지원

### 여러 언어로 번역

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

## 알림 설정

### Slack 알림
```yaml
- name: Notify Slack
  if: steps.translate.outputs.pr-url
  uses: 8398a7/action-slack@v3
  with:
    status: success
    text: '문서 번역이 완료되었습니다: ${{ steps.translate.outputs.pr-url }}'
```

### 이메일 알림
```yaml
- name: Send Email
  uses: dawidd6/action-send-mail@v3
  with:
    subject: '문서 번역 완료'
    body: '새로운 번역 PR이 생성되었습니다.'
```

## 디버그 및 분석 설정

### 디버그 모드 활성화

디버그 모드를 통해 번역 과정의 상세한 정보를 확인할 수 있습니다:

```yaml
- uses: your-username/ollama-doc-translator@v1
  with:
    debug-mode: true           # 디버그 파일 생성 활성화
    github-token: ${{ secrets.GITHUB_TOKEN }}
```

### 생성되는 디버그 파일들

디버그 모드 활성화시 다음 파일들이 자동 생성됩니다:

#### 1. 청킹 디버그 파일 (`debug_chunks/`)
```
debug_chunks/
├── document-name_chunk_001.md     # 각 청크별 분석 파일
├── document-name_chunk_002.md
├── ...
└── document-name_summary.md       # 청킹 요약 보고서
```

각 청크 파일 헤더 예시:
```markdown
<!-- DEBUG CHUNK 1/15 -->
<!-- Tokens: 245 -->
<!-- Characters: 856 -->
<!-- Source: docs/api-guide.md -->

---

실제 청크 내용...
```

#### 2. 번역 비교 파일 (`debug_originals/`, `debug_translations/`)
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

### 디버그 정보 해석

#### 콘솔 출력 예시
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

#### 토큰 계산 정보
```yaml
# 대용량 문서 처리를 위한 컨텍스트 길이 설정
context-length: 32768          # 모델 컨텍스트 길이
```

시스템이 자동 계산하는 안전 토큰 수:
- **프롬프트 오버헤드**: ~200 토큰
- **출력 예약 공간**: 컨텍스트 길이의 40%
- **안전 마진**: 100 토큰
- **실제 사용 가능**: 약 19,268 토큰 (32,768 기준)

### 고급 디버깅 설정

#### 스마트 청킹 분석
```yaml
# 청킹 전략 상세 분석
- uses: your-username/ollama-doc-translator@v1
  with:
    debug-mode: true
    context-length: 4096        # 작은 청크로 더 세밀한 분석
    temperature: 0.1            # 일관된 번역 결과
```

#### 코드 블록 보존 검증
디버그 파일을 통해 코드 블록이 올바르게 보존되는지 확인:

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


### 아티팩트 및 로그 저장

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

### 성능 분석

디버그 모드에서 제공하는 성능 지표:

```bash
📊 Translation Performance Summary:
   ⏱️  Total time: 2m 34s
   📄 Files processed: 12
   🔄 Total chunks: 67
   📈 Average chunk size: 1,089 tokens
   ⚡ Translation speed: ~425 tokens/sec
   🎯 Success rate: 100% (0 retries needed)
```

### 문제 해결 가이드

#### 자주 발생하는 문제들

1. **청크가 너무 크게 생성됨**
   ```yaml
   context-length: 4096  # 기본값(32768)보다 작게 설정
   ```

2. **번역 품질이 일관되지 않음**
   ```yaml
   temperature: 0.1      # 더 보수적인 번역
   max-retries: 5        # 재시도 횟수 증가
   ```

3. **코드 블록이 깨짐**
   - `debug_comparisons/` 파일에서 원본과 번역 비교
   - 코드 블록 보존 로직이 제대로 작동하는지 확인

이 설정들을 조합하여 프로젝트에 맞는 최적의 번역 워크플로우를 구성할 수 있습니다.