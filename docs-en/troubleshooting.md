# Guide to Troubleshooting

This document provides guidance on common issues that may arise when using the Ollama documentation translator, along with their solutions.

## Common Issues

### 1. Ollama Server Connection Error

#### Symptoms
```
❌ Error: Ollama The server is Running There is/are No..
❌ Connection refused: http://localhost:11434
```

#### Solution

1. **Check Ollama server status**:
   ```bash
   # Check process
   ps aux | grep ollama
   
   # Check service status (Linux)
   systemctl status ollama
   ```

2. **Start Ollama server**:
   ```bash
   # Run in background
   ollama serve &
   
   # Or run in foreground
   ollama serve
   ```

3. **Check port**:
   ```bash
   # Check if port 11434 is in use
   netstat -tulpn | grep 11434
   lsof -i :11434
   ```

4. **Firewall settings**:
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
❌ Model 'exaone3.5:7.8b' to find Number There is none..
❌ Failed to pull model: network timeout
```

#### Solution

1. **Check Internet Connection**:
   ```bash
   curl -I https://ollama.com
   ```

2. **Manually download the model**:
   ```bash
   # Forcefully re-download the model
   ollama rm exaone3.5:7.8b
   ollama pull exaone3.5:7.8b
   ```

3. **Proxy settings** (Company Network):
   ```bash
   export HTTP_PROXY=http://proxy.company.com:8080
   export HTTPS_PROXY=http://proxy.company.com:8080
   ollama pull exaone3.5:7.8b
   ```

4. **Check disk space**:
   ```bash
   df -h ~/.ollama/models
   ```

### 3. GitHub Actions workflow failed

#### Symptoms
```
❌ Action failed: Container failed to start
❌ Permission denied
```

#### Solution

1. **Check Self-hosted Runner**:
   ```bash
   # Check runner status
   ./run.sh --check
   
   # Restart runner
   ./run.sh
   ```

2. **Docker Permission Issue (Linux)**:
   ```bash
   # Add user to docker group
   sudo usermod -aG docker $USER
   
   # Logout and log back in
   newgrp docker
   ```

3. **Token Permission Check**:
   - Repository Settings → Actions → General
   - Select "Read and write permissions"

### 4. Translation Quality Issues

#### Symptoms
- Inaccurate or inconsistent translation
- Markdown formatting is broken
- Technical terms are incorrectly translated

#### Solutions

1. **Adjust Temperature**:
   ```yaml
   temperature: 0.1  # More consistent translation
   ```

2. **Use a Larger Model**:
   ```yaml
   model: 'exaone3.5:32b'  # More accurate translation
   ```

3. **Adjust Chunk Size**:
   ```python
   # Modify in entrypoint.py
   chunks = content.split('\n\n')  # Paragraph-level
   # Or
   chunks = content.split('\n')    # Line-level
   ```

4. **Improve Prompt**:
   ```python
   prompt = f"""Please translate the following Korean technical document into English.
   Maintain the Markdown formatting accurately, and preserve the original technical terms.

   Korean text:
   {text}

   English translation:"""
   ```

### 5. Out of Memory Error

#### Symptoms
```
❌ Out of memory error
❌ Model failed to load
```

#### Solution

1. **Check System Memory**:
   ```bash
   free -h
   htop
   ```

2. **Use a smaller model.**:
   ```yaml
   model: 'mistral:7b'  # Use less memory
   ```

3. **Add swap memory** (Linux):
   ```bash
   # Create a 4GB swap file.
   sudo fallocate -l 4G /swapfile
   sudo chmod 600 /swapfile
   sudo mkswap /swapfile
   sudo swapon /swapfile
   ```

4. **Docker memory limit**:
   ```yaml
   # docker-compose.yml
   services:
     ollama:
       deploy:
         resources:
           limits:
             memory: 8G
   ```

### 6. Pull Request creation failed.

#### Symptoms
```
❌ Failed to create pull request
❌ GitHub CLI not found
```

#### Solution

1. **Install GitHub CLI**:
   ```bash
   # Ubuntu/Debian
   sudo apt install gh
   
   # macOS
   brew install gh
   
   # Windows
   winget install GitHub.cli
   ```

2. **Configure Authentication**:
   ```bash
   gh auth login
   ```

3. **Verify Token Permissions**:
   - Check repo permissions in Personal access tokens

4. **Disable Manual PR Creation**:
   ```yaml
   create-pr: false
   ```

### 7. File Encoding Issues

#### Symptoms
```
❌ UnicodeDecodeError
❌ Hangul broken Displayed
```

#### Solutions

1. **Verify File Encoding**:
   ```bash
   file -i docs/*.md
   ```

2. **Convert to UTF-8**:
   ```bash
   # Convert the file to UTF-8
   iconv -f EUC-KR -t UTF-8 input.md > output.md
   ```

3. **Remove BOM (if necessary)**:
   ```bash
   sed -i '1s/\xEF\xBB\xBF//' *.md
   ```

## Performance Optimization Tips

### 1. Improving Translation Speed

```yaml
# Enable parallel processing
max-parallel: 3

# Skip existing files
skip-existing: true

# Use a faster model.
model: 'mistral:7b'
```

### 2. Resource Monitoring

```bash
# System resource monitoring
htop
iostat -x 1
nvidia-smi  # When using a GPU
```

### 3. Adjusting Log Level

```yaml
# Disable debug mode (production)
debug: false
verbose: false
```

## Debugging Tools

### 1. Log Collection

```bash
# Check Ollama logs
journalctl -u ollama -f

# Docker logs
docker logs ollama-container

# Download GitHub Actions logs
gh run download <run-id>
```

### 2. Direct API Testing

```bash
# Directly calling the Ollama API
curl -X POST http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "model": "exaone3.5:7.8b",
    "prompt": "Hello Please provide the Korean text you would like me to translate. Translate it.",
    "stream": false
  }'
```

### 3. Network Diagnostics

```bash
# Network connection test
telnet localhost 11434

# DNS resolution check
nslookup ollama.com
```

## How to Request Support

If the issue is not resolved:

1.  **Create an Issue Template**:
    -   Operating System and Version
    -   Ollama Version
    -   Model Used
    -   Error Message
    -   Steps to Reproduce

2.  **Attach Logs**:
    ```bash
    # Collect relevant logs
    ollama serve > ollama.log 2>&1
    ```

3.  **GitHub Issues**:
    -   [https://github.com/your-username/ollama-doc-translator/issues](https://github.com/your-username/ollama-doc-translator/issues)

4.  **Community Forum**:
    -   [Ollama Discord](https://discord.gg/ollama)
    -   [GitHub Discussions](https://github.com/your-username/ollama-doc-translator/discussions)

## Smart Chunking & Debugging Issues

### 8. Large Document Processing Issues

#### Symptoms
```
❌ Context length exceeded
❌ chunks Too greatly Created
❌ Translation In the middle Disconnection
```

#### Solutions

1. **Adjust Context Length**:
   ```yaml
   context-length: 4096    # Set to a smaller value than the default of 32768
   ```

2. **Debug Mode Chunk Analysis**:
   ```yaml
   debug-mode: true
   ```
   
   Generated files:
   - `debug_chunks/`: Analysis for each chunk
   - `debug_originals/`: Original chunks
   - `debug_translations/`: Translated chunks

3. **Console Output Verification**:
   ```bash
   📦 Created 15 token-aware chunks:
      Chunk 1: 1,156 tokens (2,845 chars)  # Verify token count
   ```

### 9. Code Block Corruption Issue

#### Symptoms
```markdown
# Original
```python
def hello():
    print("world")
```

# Translation Results (In Case of Errors)
```python
def hello():
```
print("world")
```

#### Solution

1. **Check the debug comparison file.**:
   ```bash
   debug_comparisons/filename_comparison_001.md
   ```

2. **Section-based chunk verification**:
   - Code blocks chunk In the middle Not divided Is it not? Confirmation
   - H1-H3 Heading Based on chunks Correctly Is it separable? Confirmation

3. **Strengthen translation prompts**:
   Currently The system is Already Code Block Preservation the logic including There is.:
   ```
   - IMPORTANT: Do NOT add **bold**, *italic*, or any formatting that wasn't in the original text
   - Only translate text content, never modify or add markdown formatting
   ```

### 10. Problem of inconsistent translation quality

#### Symptoms
```
❌ Identical terms are translated differently
❌ The style varies across chunks
❌ Numbers disappear from numbered lists
```

#### Solution

1. **Adjust Temperature**:
   ```yaml
   temperature: 0.1        # More consistent translation (default: 0.3)
   ```

2. **Increase Retry Count**:
   ```yaml
   max-retries: 5         # Default: 3
   ```

3. **Translation Comparison Analysis**:
   ```bash
   # Compare original and translation
   debug_comparisons/filename_comparison_001.md
   ```

4. **Verify Numbered List Preservation**:
   The system is designed to preserve the following pattern:
   ```markdown
   # Original
   - 288. Cache Invalidation Scenario
   
   # Translation Result
   - 288. Cache Invalidation Scenario
   ```

### 11. How to Use Debug Files

#### Understanding the Structure of Debug Files

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
      ⏱️  Total time: 2m 34s
      📄 Files processed: 12
      🔄 Total chunks: 67
      📈 Average chunk size: 1,089 tokens
   ```

3. **Identifying Problem Patterns**:
   - Repeated errors occurring in specific chunks
   - Quality degradation in specific token ranges
   - Formatting issues in specific Markdown patterns

#### Optimization Tips

1. **Optimal Chunk Size**:
   - 1,000-1,500 tokens: Balanced quality and speed
   - 500-800 tokens: High quality, slow speed
   - 2,000+ tokens: Fast speed, risk of quality degradation

2. **Utilizing Section-Based Splitting**:
   - H1-H2: Always split at the boundary
   - H3: Split if 200 tokens or more
   - Code blocks: Never split

## Frequently Asked Questions (FAQ)

### Q: How can I speed up the translation process?
A: Use a GPU, use a smaller model, or run it on a self-hosted runner.

### Q: How can I keep specific terms untranslated?
A: Add instructions like "Keep technical terms in the original text" to the prompt.

### Q: Can I translate in multiple languages simultaneously?
A: Currently, we only support Korean-to-English translation, but you can process multiple languages sequentially using the matrix strategy.

### Q: Does it work with private repositories?
A: Yes, it works with private repositories using a Personal Access Token.

---

> **⚠️ 이 문서는 AI로 번역된 문서입니다.**
>
> **⚠️ This document has been translated by AI.**