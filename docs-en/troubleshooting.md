# Problem Solving Guide

This guide provides solutions to common issues encountered while translating Ollama documents.

## Common Issues

### 1. Ollama Server Connection Error

#### Symptoms
```
❌ Error: Ollama 서버가 실행되고 있지 않습니다.
❌ Connection refused: http://localhost:11434
```

#### Troubleshooting Steps

1. **Check Ollama Server Status**:
   ```bash
   # Check process
   ps aux | grep ollama
   
   # Check service status (Linux)
   systemctl status ollama
   ```

2. **Start Ollama Server**:
   ```bash
   # Run in background
   ollama serve &
   
   # Or run in foreground
   ollama serve
   ```

3. **Port Verification**:
   ```bash
   # Check if port 11434 is in use
   netstat -tulpn | grep 11434
   lsof -i :11434
   ```

4. **Firewall Configuration**:
   ```bash
   # Ubuntu/Debian
   sudo ufw allow 11434
   
   # CentOS/RHEL
   sudo firewall-cmd --add-port=11434/tcp --permanent
   sudo firewall-cmd --reload
   ```

### 2. Model Download Failure

#### Symptoms
```
❌ 모델 'exaone3.5:7.8b'을 찾을 수 없습니다.
❌ Failed to pull model: network timeout
```

#### Troubleshooting Steps

1. **Check Internet Connection**:
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

#### Troubleshooting Steps

1. **Self-hosted Runner Check**:
   ```bash
   # Check Runner status
   ./run.sh --check
   
   # Restart Runner
   ./run.sh
   ```

2. **Docker Permission Issues** (Linux):
   ```bash
   # Add user to docker group
   sudo usermod -aG docker $USER
   
   # Re-login required
   newgrp docker
   ```

3. **Token Permissions Verification**:
   - Repository Settings → Actions → General
   - Select "Read and write permissions" under "Workflow permissions"

### 4. Translation Quality Issues

#### Symptoms
- Inaccurate or inconsistent translations
- Markdown formatting issues
- Incorrect translation of technical terms

#### Solutions

1. **Temperature Adjustment**:
   ```yaml
   temperature: 0.1  # For more consistent translations
   ```

2. **Use a Larger Model**:
   ```yaml
   model: 'exaone3.5:32b'  # For more accurate translations
   ```

3. **Adjust Chunk Size**:
   ```python
   # Modify in entrypoint.py
   chunks = content.split('\n\n')  # Split by paragraphs
   # Alternatively
   chunks = content.split('\n')    # Split by lines
   ```

4. **Improve Prompt**:
   ```python
   prompt = f"""Translate the following Korean technical document into English. 
   Ensure accurate preservation of Markdown formatting and technical terms.
   
   Korean Text:
   {text}
   
   English Translation:"""
   ```

### 5. Memory Insufficient Error

#### Symptoms
```
❌ Out of memory error
❌ Model failed to load
```

#### Solutions

1. **Check System Memory**:
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

#### Solutions

1. **Install GitHub CLI**:
   ```bash
   # Ubuntu/Debian
   sudo apt install gh
   
   # macOS
   brew install gh
   
   # Windows
   winget install GitHub.cli
   ```

2. **Set Up Authentication**:
   ```bash
   gh auth login
   ```

3. **Verify Token Permissions**:
   - Check repository permissions under Personal access tokens

4. **Disable Manual PR Creation**:
   ```yaml
   create-pr: false
   ```

### 7. File Encoding Issues

#### Symptoms
```
❌ UnicodeDecodeError
❌ 한글이 깨져서 표시됨
```

#### Solution Steps

1. **Check File Encoding**:
   ```bash
   file -i docs/*.md
   ```

2. **Convert to UTF-8**:
   ```bash
   # Convert file to UTF-8 encoding
   iconv -f EUC-KR -t UTF-8 input.md > output.md
   ```

3. **Remove BOM (if necessary)**:
   ```bash
   sed -i '1s/^\xEF\xBB\xBF//' *.md
   ```

## Performance Optimization Tips

### 1. Improve Translation Speed

```yaml
# 병렬 처리 활성화
max-parallel: 3

# 기존 파일 스킵
skip-existing: true

# 더 빠른 모델 사용
model: 'mistral:7b'
```

### 2. Resource Monitoring

```bash
# 시스템 리소스 모니터링
htop
iostat -x 1
nvidia-smi  # GPU 사용 시
```

### 3. Adjust Log Levels

```yaml
# 디버그 모드 비활성화 (프로덕션)
debug: false
verbose: false
```

## Debugging Tools

### 1. Log Collection

```bash
# Ollama 로그 확인
journalctl -u ollama -f

# Docker 로그
docker logs ollama-container

# GitHub Actions 로그 다운로드
gh run download <run-id>
```

### 2. Direct API Testing

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

### 3. Network Diagnostics

```bash
# 네트워크 연결 테스트
telnet localhost 11434

# DNS 해상도 확인
nslookup ollama.com
```

## Submit a Support Request

If the issue is not resolved:

1. **Fill out the Issue Template**:
   - Operating System and Version
   - Ollama Version
   - Used Model
   - Error Message
   - Reproduction Steps

2. **Attach Logs**:
   ```bash
   # Collect relevant logs
   ollama serve > ollama.log 2>&1
   ```

3. **GitHub Issues**:
   - [https://github.com/your-username/ollama-doc-translator/issues](https://github.com/your-username/ollama-doc-translator/issues)

4. **Community Forums**:
   - [Ollama Discord](https://discord.gg/ollama)
   - [GitHub Discussions](https://github.com/your-username/ollama-doc-translator/discussions)

## Smart Chunking & Debugging Issues

### 8. Large Document Processing Issues

#### Symptoms
```
❌ Context length exceeded
❌ 청크가 너무 크게 생성됨
❌ 번역이 중간에 끊어짐
```

#### Solutions

1. **Adjust Context Length**:
   ```yaml
   context-length: 4096    # Set lower than default 32768
   ```

2. **Debug Chunking Analysis Mode**:
   ```yaml
   debug-mode: true
   ```
   
   Generated Files:
   - `debug_chunks/`: Analysis per chunk
   - `debug_originals/`: Original chunks
   - `debug_translations/`: Translated chunks

3. **Check Console Output**:
   ```bash
   📦 Created 15 token-aware chunks:
      Chunk 1: 1,156 tokens (2,845 chars)  # Verify token count
   ```

### 9. Code Block Corruption Issue

#### Symptoms
```markdown
# 원본
```python
def hello():
    print("world")
```

# 번역 결과 (잘못된 경우)
```

# Translated Result (Incorrect)
```
print("world")
```
print("world")
```

#### Solutions

1. **Check Debug Comparison Files**:
   ```bash
   debug_comparisons/filename_comparison_001.md
   ```

2. **Check Section Chunking**:
   - Ensure code blocks are not split in the middle of chunks
   - Verify chunks are correctly separated based on H1-H3 headings

3. **Enhance Translation Prompts**:
   The current system already includes logic to preserve code blocks:
   ```
   - IMPORTANT: Do NOT add **bold**, *italic*, or any formatting that wasn't in the original text
   - Only translate text content, never modify or add markdown formatting
   ```
```

### 10. Translation Quality Discrepancy Issues

#### Symptoms
```
❌ 동일한 용어가 다르게 번역됨
❌ 문체가 청크마다 달라짐
❌ 번호 목록에서 번호가 사라짐
```

#### Solutions

1. **Temperature Adjustment**:
   ```yaml
   temperature: 0.1        # More consistent translation (default: 0.3)
   ```

2. **Increase Retry Attempts**:
   ```yaml
   max-retries: 5         # Default: 3
   ```

3. **Translation Comparison Analysis**:
   ```bash
   # Compare original and translated text
   debug_comparisons/filename_comparison_001.md
   ```

4. **Preservation of Numbered List Verification**:
   The system is designed to preserve the following pattern:
   ```markdown
   # Original
   - 288. Cache Invalidation Scenario
   
   # Translated Result
   - 288. Cache Invalidation Scenario
   ```

### 11. Debug File Usage

#### Understanding Debug File Structure

1. **Chunk Analysis** (`debug_chunks/`):
   ```markdown
   <!-- DEBUG CHUNK 1/15 -->
   <!-- Tokens: 1,156 -->
   <!-- Characters: 2,845 -->
   <!-- Source: docs/api-guide.md -->
   ```

2. **Translation Performance Analysis**:
   ```bash
   📊 Translation Performance Summary:
      ⏱️ Total time: 2m 34s
      📄 Files processed: 12
      🔄 Total chunks: 67
      📈 Average chunk size: 1,089 tokens
   ```

3. **Identifying Problem Patterns**:
   - Repeated errors in specific chunks
   - Quality degradation in specific token ranges
   - Formatting issues in specific markdown patterns

#### Optimization Tips

1. **Optimal Chunk Size**:
   - 1,000-1,500 tokens: Balanced quality and speed
   - 500-800 tokens: High quality, slower speed
   - 2,000+ tokens: Faster speed, potential quality drop

2. **Utilizing Section-Based Segmentation**:
   - Always split at H1-H2 levels
   - Split at H3 if chunk size exceeds 200 tokens
   - Never split code blocks

## Frequently Asked Questions (FAQ)

### Q: Why is translation so slow? How can I speed it up?
A: Use GPU acceleration, opt for smaller models, or run on a Self-hosted runner.

### Q: How do I keep specific terms untranslated?
A: Add instructions in the prompt, such as "Keep technical terms in the original language."

### Q: Is multi-language translation supported simultaneously?
A: Currently, only Korean-English translation is supported, but you can sequentially process multiple languages using a matrix strategy.

### Q: Does it work with private repositories?
A: Yes, it supports private repositories using a Personal Access Token.

---

> **⚠️ 이 문서는 AI로 번역된 문서입니다.**
>
> **⚠️ This document has been translated by AI.**