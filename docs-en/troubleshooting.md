# Problem Solving Guide

This guide provides solutions to common issues that may arise while using the Ollama document translator.

## Common Issues

### 1. Ollama Server Connection Error

#### Symptoms
```
❌ Error: Ollama Server Executed It is Does not.
❌ Connection refused: http://localhost:11434
```

#### Troubleshooting Steps

1. **Check Ollama Server Status**:
   ```bash
   # Check processes
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
❌ Model 'exaone3.5:7.8b'The provided text "을" translates to "as" or depends on context, often functioning as a particle indicating the object of a verb in Korean sentences. Without additional context, a direct translation isn't fully illustrative, but generally:

**"as"** (in comparative contexts) or **"object marker"** (grammatically). 

Please provide more context if a specific translation is needed. Find Water None.
❌ Failed to pull model: network timeout
```

#### Troubleshooting Steps

1. **Check Internet Connection**:
   ```bash
   curl -I https://ollama.com
   ```

2. **Manually download the model**:
   ```bash
   # Model forced redownload
   ollama rm exaone3.5:7.8b
   ollama pull exaone3.5:7.8b
   ```

3. **Proxy Settings** (Company Network):
   ```bash
   export HTTP_PROXY=http://proxy.company.com:8080
   export HTTPS_PROXY=http://proxy.company.com:8080
   ollama pull exaone3.5:7.8b
   ```

4. **Check disk space**:
   ```bash
   df -h ~/.ollama/models
   ```

### 3. GitHub Actions Workflow Failure

#### Symptoms
```
❌ Action failed: Container failed to start
❌ Permission denied
```

#### Troubleshooting Steps

1. **Check Self-hosted Runner**:
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
   
   # Re-login required after this step
   newgrp docker
   ```

3. **Token Permissions Verification**:
   - Navigate to Repository Settings → Actions → General
   - Under "Workflow permissions," select "Read and write permissions"

### 4. Translation Quality Issues

#### Symptoms
- **Inaccurate or inconsistent translations**
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
   Ensure accurate preservation of Markdown formatting and keep technical terms in the original Korean.
   
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

#### Troubleshooting Steps

1. **Check System Memory**:
   ```bash
   free -h
   htop
   ```

2. **Use a smaller model.**:
   ```yaml
   model: 'mistral:7b'  # Less memory usage
   ```

3. **Add swap memory** (Linux):
   ```bash
   # Create a 4GB swap file
   sudo fallocate -l 4G /swapfile
   sudo chmod 600 /swapfile
   sudo mkswap /swapfile
   sudo swapon /swapfile
   ```

4. **Docker Memory Limit**:
   ```yaml
   # docker-compose.yml
   services:
     ollama:
       deploy:
         resources:
           limits:
             memory: 8G
   ```

### 6. Failed to Create Pull Request

#### Symptoms
```
❌ Failed to create pull request
❌ GitHub CLI not found
```

#### Troubleshooting Steps

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
❌ Korean characters Broken Displayed
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
# Enable parallel processing
max-parallel: 3

# Skip existing file
skip-existing: true

# Use a faster model.
model: 'mistral:7b'
```

### 2. Resource Monitoring

```bash
# System Resource Monitoring
htop
iostat -x 1
nvidia-smi  # When using GPU
```

### 3. Adjust Log Levels

```yaml
# Disable Debug Mode (Production)
debug: false
verbose: false
```

## Debugging Tools

### 1. Log Collection

```bash
# Check Ollama logs
journalctl -u ollama -f

# Docker Logs
docker logs ollama-container

# Download GitHub Actions Logs
gh run download <run-id>
```

### 2. Direct API Testing

```bash
# Direct call to Ollama API
curl -X POST http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "model": "exaone3.5:7.8b",
    "prompt": "Hello Please provide the Korean text you would like translated into English. Translate this Korean text to English.",
    "stream": false
  }'
```

### 3. Network Diagnostics

```bash
# Network connection test
telnet localhost 11434

# DNS Resolution Check
nslookup ollama.com
```

## Submitting a Support Request

If the issue is not resolved:

1. **Create an Issue Template**:
   - Operating system and version
   - Ollama version
   - Used model
   - Error message
   - Reproduction steps

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
❌ Chunk Too much Greatly Created
❌ Translation In the middle Breakage
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
# Original text not provided. Please provide the Korean text you would like translated.
```python
def hello():
    print("world")
```

# Please provide the Korean text you would like translated.
```python
def hello():
```
print("world")
```

#### Resolution Steps

1. **Check Debug Comparison Files**:
   ```bash
   debug_comparisons/filename_comparison_001.md
   ```

2. **Check Section Chunking**:
   - Ensure code blocks are not split in the middle of chunks
   - Verify chunks are correctly separated based on H1-H3 headings

3. **Enhance Translation Prompts**:
   The current system already includes logic for preserving code blocks:
   ```
   - IMPORTANT: Do NOT add **bold**, *italic*, or any formatting not present in the original text
   - Only translate text content; never modify or add markdown formatting
   ```

### 10. Translation Quality Discrepancy Issues

#### Symptoms
```
❌ Same Terminology Differently Translated
❌ Style Chunk by chunk Change
❌ Number From the list Numbered Disappearance
```

#### Solutions

1. **Temperature Adjustment**:
   ```yaml
   temperature: 0.1        # For more consistent translation (default: 0.3)
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

4. **Verification of Numbered List Preservation**:
   The system is designed to preserve the following pattern:
   ```markdown
   # Original
   - 288. Cache Invalidation Scenario
   
   # Translated Result
   - 288. Cache Invalidation Scenario
   ```

### 11. Debug File Usage Guide

#### Understanding Debug File Structure

1. **Chunking Analysis** (`debug_chunks/`):
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
   - Quality degradation within specific token ranges
   - Formatting issues in specific Markdown patterns

#### Optimization Tips

1. **Optimal Chunk Size**:
   - **1,000-1,500 tokens**: Balanced quality and speed
   - **500-800 tokens**: High quality but slower speed
   - **2,000+ tokens**: Faster speed but potential quality drop

2. **Utilizing Section-Based Segmentation**:
   - **H1-H2**: Always segment boundaries
   - **H3**: Segment if over 200 tokens
   - **Code Blocks**: Never segment

## Frequently Asked Questions (FAQ)

### Q: Why is translation so slow? How can I speed it up?
A: Use a GPU, opt for a smaller model, or run it on a Self-hosted runner.

### Q: How do I keep specific terms untranslated?
A: Add instructions in the prompt, such as "Keep technical terms in their original language."

### Q: Is multi-language translation supported simultaneously?
A: Currently, only Korean-English translation is supported, but you can sequentially process multiple languages using a matrix strategy.

### Q: Does it work with private repositories as well?
A: Yes, it is compatible with private repositories when using a Personal Access Token.

---

> **⚠️ 이 문서는 AI로 번역된 문서입니다.**
>
> **⚠️ This document has been translated by AI.**