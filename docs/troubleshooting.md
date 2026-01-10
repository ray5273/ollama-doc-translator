# 문제 해결 가이드

Ollama 문서 번역기 사용 중 발생할 수 있는 일반적인 문제들과 해결 방법을 안내합니다.

## 일반적인 문제들

### 1. Ollama 서버 연결 오류

#### 증상
```
❌ Error: Ollama 서버가 실행되고 있지 않습니다.
❌ Connection refused: http://localhost:11434
```

#### 해결 방법

1. **Ollama 서버 상태 확인**:
   ```bash
   # 프로세스 확인
   ps aux | grep ollama
   
   # 서비스 상태 확인 (Linux)
   systemctl status ollama
   ```

2. **Ollama 서버 시작**:
   ```bash
   # 백그라운드 실행
   ollama serve &
   
   # 또는 포그라운드 실행
   ollama serve
   ```

3. **포트 확인**:
   ```bash
   # 11434 포트가 사용 중인지 확인
   netstat -tulpn | grep 11434
   lsof -i :11434
   ```

4. **방화벽 설정**:
   ```bash
   # Ubuntu/Debian
   sudo ufw allow 11434
   
   # CentOS/RHEL
   sudo firewall-cmd --add-port=11434/tcp --permanent
   sudo firewall-cmd --reload
   ```

### 2. 모델 다운로드 실패

#### 증상
```
❌ 모델 'exaone3.5:7.8b'을 찾을 수 없습니다.
❌ Failed to pull model: network timeout
```

#### 해결 방법

1. **인터넷 연결 확인**:
   ```bash
   curl -I https://ollama.com
   ```

2. **수동으로 모델 다운로드**:
   ```bash
   # 모델 강제 재다운로드
   ollama rm exaone3.5:7.8b
   ollama pull exaone3.5:7.8b
   ```

3. **프록시 설정** (회사 네트워크):
   ```bash
   export HTTP_PROXY=http://proxy.company.com:8080
   export HTTPS_PROXY=http://proxy.company.com:8080
   ollama pull exaone3.5:7.8b
   ```

4. **디스크 공간 확인**:
   ```bash
   df -h ~/.ollama/models
   ```

### 3. GitHub Actions 워크플로우 실패

#### 증상
```
❌ Action failed: Container failed to start
❌ Permission denied
```

#### 해결 방법

1. **Self-hosted Runner 확인**:
   ```bash
   # Runner 상태 확인
   ./run.sh --check
   
   # Runner 재시작
   ./run.sh
   ```

2. **Docker 권한 문제** (Linux):
   ```bash
   # 사용자를 docker 그룹에 추가
   sudo usermod -aG docker $USER
   
   # 로그아웃 후 재로그인 필요
   newgrp docker
   ```

3. **토큰 권한 확인**:
   - Repository Settings → Actions → General
   - "Workflow permissions"에서 "Read and write permissions" 선택

### 4. 번역 품질 문제

#### 증상
- 번역이 부정확하거나 일관성이 없음
- 마크다운 형식이 깨짐
- 전문 용어가 잘못 번역됨

#### 해결 방법

1. **Temperature 조정**:
   ```yaml
   temperature: 0.1  # 더 일관된 번역
   ```

2. **더 큰 모델 사용**:
   ```yaml
   model: 'exaone3.5:32b'  # 더 정확한 번역
   ```

3. **청크 크기 조정**:
   ```python
   # entrypoint.py에서 수정
   chunks = content.split('\n\n')  # 문단 단위
   # 또는
   chunks = content.split('\n')    # 줄 단위
   ```

4. **프롬프트 개선**:
   ```python
   prompt = f"""다음 한국어 기술 문서를 영어로 번역해주세요. 
   마크다운 형식을 정확히 유지하고, 기술 용어는 원문을 유지하세요.
   
   한국어 텍스트:
   {text}
   
   영어 번역:"""
   ```

### 5. 메모리 부족 오류

#### 증상
```
❌ Out of memory error
❌ Model failed to load
```

#### 해결 방법

1. **시스템 메모리 확인**:
   ```bash
   free -h
   htop
   ```

2. **더 작은 모델 사용**:
   ```yaml
   model: 'mistral:7b'  # 더 적은 메모리 사용
   ```

3. **스왑 메모리 추가** (Linux):
   ```bash
   # 4GB 스왑 파일 생성
   sudo fallocate -l 4G /swapfile
   sudo chmod 600 /swapfile
   sudo mkswap /swapfile
   sudo swapon /swapfile
   ```

4. **Docker 메모리 제한**:
   ```yaml
   # docker-compose.yml
   services:
     ollama:
       deploy:
         resources:
           limits:
             memory: 8G
   ```

### 6. Pull Request 생성 실패

#### 증상
```
❌ Failed to create pull request
❌ GitHub CLI not found
```

#### 해결 방법

1. **GitHub CLI 설치**:
   ```bash
   # Ubuntu/Debian
   sudo apt install gh
   
   # macOS
   brew install gh
   
   # Windows
   winget install GitHub.cli
   ```

2. **인증 설정**:
   ```bash
   gh auth login
   ```

3. **토큰 권한 확인**:
   - Personal access tokens에서 repo 권한 확인

4. **수동 PR 생성 비활성화**:
   ```yaml
   create-pr: false
   ```

### 7. 파일 인코딩 문제

#### 증상
```
❌ UnicodeDecodeError
❌ 한글이 깨져서 표시됨
```

#### 해결 방법

1. **파일 인코딩 확인**:
   ```bash
   file -i docs/*.md
   ```

2. **UTF-8로 변환**:
   ```bash
   # 파일을 UTF-8로 변환
   iconv -f EUC-KR -t UTF-8 input.md > output.md
   ```

3. **BOM 제거** (필요한 경우):
   ```bash
   sed -i '1s/^\xEF\xBB\xBF//' *.md
   ```

## 성능 최적화 팁

### 1. 번역 속도 향상

```yaml
# 병렬 처리 활성화
max-parallel: 3

# 기존 파일 스킵
skip-existing: true

# 더 빠른 모델 사용
model: 'mistral:7b'
```

### 2. 리소스 모니터링

```bash
# 시스템 리소스 모니터링
htop
iostat -x 1
nvidia-smi  # GPU 사용 시
```

### 3. 로그 레벨 조정

```yaml
# 디버그 모드 비활성화 (프로덕션)
debug: false
verbose: false
```

## 디버깅 도구

### 1. 로그 수집

```bash
# Ollama 로그 확인
journalctl -u ollama -f

# Docker 로그
docker logs ollama-container

# GitHub Actions 로그 다운로드
gh run download <run-id>
```

### 2. API 직접 테스트

```bash
# Ollama API 직접 호출
curl -X POST http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "model": "exaone3.5:7.8b",
    "prompt": "안녕하세요를 영어로 번역하세요",
    "stream": false
  }'
```

### 3. 네트워크 진단

```bash
# 네트워크 연결 테스트
telnet localhost 11434

# DNS 해상도 확인
nslookup ollama.com
```

## 지원 요청하기

문제가 해결되지 않는 경우:

1. **이슈 템플릿 작성**:
   - 운영체제 및 버전
   - Ollama 버전
   - 사용한 모델
   - 오류 메시지
   - 재현 단계

2. **로그 첨부**:
   ```bash
   # 관련 로그 수집
   ollama serve > ollama.log 2>&1
   ```

3. **GitHub Issues**:
   - [https://github.com/your-username/ollama-doc-translator/issues](https://github.com/your-username/ollama-doc-translator/issues)

4. **커뮤니티 포럼**:
   - [Ollama Discord](https://discord.gg/ollama)
   - [GitHub Discussions](https://github.com/your-username/ollama-doc-translator/discussions)

## 스마트 청킹 & 디버그 문제

### 8. 대용량 문서 처리 문제

#### 증상
```
❌ Context length exceeded
❌ 청크가 너무 크게 생성됨
❌ 번역이 중간에 끊어짐
```

#### 해결 방법

1. **컨텍스트 길이 조정**:
   ```yaml
   context-length: 4096    # 기본값 32768보다 작게 설정
   ```

2. **디버그 모드로 청킹 분석**:
   ```yaml
   debug-mode: true
   ```
   
   생성되는 파일들:
   - `debug_chunks/`: 각 청크별 분석
   - `debug_originals/`: 원본 청크들
   - `debug_translations/`: 번역된 청크들

3. **콘솔 출력 확인**:
   ```bash
   📦 Created 15 token-aware chunks:
      Chunk 1: 1,156 tokens (2,845 chars)  # 토큰 수 확인
   ```

### 9. 코드 블록 손상 문제

#### 증상
```markdown
# 원본
```python
def hello():
    print("world")
```

# 번역 결과 (잘못된 경우)
```python
def hello():
```
print("world")
```

#### 해결 방법

1. **디버그 비교 파일 확인**:
   ```bash
   debug_comparisons/filename_comparison_001.md
   ```

2. **섹션 기반 청킹 확인**:
   - 코드 블록이 청크 중간에서 분할되지 않는지 확인
   - H1-H3 헤딩 기반으로 청크가 올바르게 분리되는지 확인

3. **번역 프롬프트 강화**:
   현재 시스템은 이미 코드 블록 보존 로직을 포함하고 있습니다:
   ```
   - IMPORTANT: Do NOT add **bold**, *italic*, or any formatting that wasn't in the original text
   - Only translate text content, never modify or add markdown formatting
   ```

### 10. 번역 품질 불일치 문제

#### 증상
```
❌ 동일한 용어가 다르게 번역됨
❌ 문체가 청크마다 달라짐
❌ 번호 목록에서 번호가 사라짐
```

#### 해결 방법

1. **Temperature 조정**:
   ```yaml
   temperature: 0.1        # 더 일관된 번역 (기본값: 0.3)
   ```

2. **재시도 횟수 증가**:
   ```yaml
   max-retries: 5         # 기본값: 3
   ```

3. **번역 비교 분석**:
   ```bash
   # 원본과 번역 비교
   debug_comparisons/filename_comparison_001.md
   ```

4. **번호 목록 보존 확인**:
   시스템은 다음 패턴을 보존하도록 설계됨:
   ```markdown
   # 원본
   - 288. 캐시 무효화 시나리오
   
   # 번역 결과
   - 288. Cache Invalidation Scenario
   ```

### 11. 디버그 파일 활용법

#### 디버그 파일 구조 이해

1. **청킹 분석** (`debug_chunks/`):
   ```markdown
   <!-- DEBUG CHUNK 1/15 -->
   <!-- Tokens: 1,156 -->
   <!-- Characters: 2,845 -->
   <!-- Source: docs/api-guide.md -->
   ```

2. **번역 성능 분석**:
   ```bash
   📊 Translation Performance Summary:
      ⏱️  Total time: 2m 34s
      📄 Files processed: 12
      🔄 Total chunks: 67
      📈 Average chunk size: 1,089 tokens
   ```

3. **문제 패턴 식별**:
   - 특정 청크에서 반복적으로 오류 발생
   - 특정 토큰 범위에서 품질 저하
   - 특정 마크다운 패턴에서 형식 손상

#### 최적화 팁

1. **적정 청크 크기**:
   - 1,000-1,500 토큰: 최적 품질과 속도 균형
   - 500-800 토큰: 높은 품질, 느린 속도  
   - 2,000+ 토큰: 빠른 속도, 품질 저하 위험

2. **섹션 기반 분할 활용**:
   - H1-H2: 항상 분할 경계
   - H3: 200 토큰 이상시 분할
   - 코드 블록: 절대 분할하지 않음

## 자주 묻는 질문 (FAQ)

### Q: 번역이 너무 느린데 어떻게 빠르게 할 수 있나요?
A: GPU를 사용하거나, 더 작은 모델을 사용하거나, Self-hosted runner에서 실행하세요.

### Q: 특정 용어를 번역하지 않고 그대로 유지하려면?
A: 프롬프트에 "기술 용어는 원문 유지" 등의 지시사항을 추가하세요.

### Q: 여러 언어로 동시에 번역할 수 있나요?
A: 현재는 한국어-영어만 지원하지만, 매트릭스 전략으로 여러 언어를 순차적으로 처리할 수 있습니다.

### Q: 프라이빗 저장소에서도 작동하나요?
A: 네, Personal Access Token을 사용하면 프라이빗 저장소에서도 사용 가능합니다.