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

## 문제 해결을 위한 디버그 설정

### 상세 로깅
```yaml
- uses: your-username/ollama-doc-translator@v1
  with:
    debug: true
    verbose: true
```

### 아티팩트 저장
```yaml
- name: Upload translation logs
  if: failure()
  uses: actions/upload-artifact@v4
  with:
    name: translation-logs
    path: translation-*.log
```

이 설정들을 조합하여 프로젝트에 맞는 최적의 번역 워크플로우를 구성할 수 있습니다.