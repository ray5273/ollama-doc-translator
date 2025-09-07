# Problem Solving Guide

This guide provides solutions to common issues encountered while using the Ollama document translator.

## Common Issues

### 1. Ollama Server Connection Error

#### Symptoms
```
❌ Error: Ollama server is not running.
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

3. **Port Check**:
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
❌ Unable to find model 'exaone3.5:7.8b'.
❌ Failed to pull model: network timeout
```

#### Troubleshooting Steps

1. **Check Internet Connection**:
   ```bash
   curl -I https://ollama.com
   ```

2. **Manual Model Download**:
   ```bash
   # Force redownload the model
   ollama rm exaone3.5:7.8b
   ollama pull exaone3.5:7.8b
   ```

3. **Proxy Settings** (Company Network):
   ```bash
   export HTTP_PROXY=http://proxy.company.com:8080
   export HTTPS_PROXY=http://proxy.company.com:8080
   ollama pull exaone3.5:7.8b
   ```

4. **Check Disk Space**:
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
   
   # Re-login required
   newgrp docker
   ```

3. **Token Permissions Verification**:
   - Repository Settings → Actions → General
   - Select "Read and write permissions" under "Workflow permissions"

### 4. Translation Quality Issues

#### Symptoms
- Translation inaccuracies or inconsistencies
- Markdown formatting issues
- Incorrect translation of technical terms

#### Solutions

1. **Temperature Adjustment**:
   ```yaml
   temperature: 0.1  # For more consistent translation
   ```

2. **Use a Larger Model**:
   ```yaml
   model: 'exaone3.5:32b'  # For more accurate translation
   ```

3. **Adjust Chunk Size**:
   ```python
   # Modify in entrypoint.py
   chunks = content.split('\n\n')  # By paragraph
   # Or
   chunks = content.split('\n')    # By line
   ```

4. **Improve Prompt**:
   ```python
   prompt = f"""Translate the following Korean technical document into English. 
   Ensure Markdown formatting is preserved exactly, keeping technical terms in the original language.
   
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

2. **Use a Smaller Model**:
   ```yaml
   model: 'mistral:7b'  # Uses less memory
   ```

3. **Add Swap Memory** (Linux):
   ```bash
   # Create a 4GB swap file
   sudo fallocate -l 4G /swapfile
   sudo chmod 600 /swapfile
   sudo mkswap /swapfile
   sudo swapon /swapfile
   ```

4. **Set Docker Memory Limits**:
   ```yaml
   # docker-compose.yml
   services:
     ollama:
       deploy:
         resources:
           limits:
             memory: 8G
   ```

### 6. Pull Request Creation Failure

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

2. **Authentication Setup**:
   ```bash
   gh auth login
   ```

3. **Verify Token Permissions**:
   - Check repo permissions under Personal access tokens

4. **Disable Manual PR Creation**:
   ```yaml
   create-pr: false
   ```

### 7. File Encoding Issues

#### Symptoms
```
❌ UnicodeDecodeError
❌ Korean characters displayed incorrectly
```

#### Solution Methods

1. **Check File Encoding**:
   ```bash
   file -i docs/*.md
   ```

2. **Convert to UTF-8**:
   ```bash
   # Convert file to UTF-8
   iconv -f EUC-KR -t UTF-8 input.md > output.md
   ```

3. **Remove BOM** (if necessary):
   ```bash
   sed -i '1s/^\xEF\xBB\xBF//' *.md
   ```

## Performance Optimization Tips

### 1. Improve Translation Speed

```yaml
# Enable Parallel Processing
max-parallel: 3

# Skip Existing Files
skip-existing: true

# Use Faster Model
model: 'mistral:7b'
```

### 2. Resource Monitoring

```bash
# System Resource Monitoring
htop
iostat -x 1
nvidia-smi  # For GPU usage
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
# Check Ollama Logs
journalctl -u ollama -f

# Docker Logs
docker logs ollama-container

# Download GitHub Actions Logs
gh run download <run-id>
```

### 2. Direct API Testing

```bash
# Direct Call to Ollama API
curl -X POST http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "model": "exaone3.5:7.8b",
    "prompt": "Translate '안녕하세요' to English",
    "stream": false
  }'
```

### 3. Network Diagnostics

```bash
# Test Network Connection
telnet localhost 11434

# Verify DNS Resolution
nslookup ollama.com
```

## How to Request Support

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

## Frequently Asked Questions (FAQ)

### Q: Why is translation so slow? How can I speed it up?
A: Use a GPU, opt for a smaller model, or run it on a Self-hosted runner.

### Q: How do I keep specific terms untranslated?
A: Add instructions like "Keep technical terms in the original text" to your prompt.

### Q: Is multi-language translation supported simultaneously?
A: Currently, only Korean-English translation is supported, but you can sequentially process multiple languages using a matrix strategy.

### Q: Does it work with private repositories?
A: Yes, it is usable with private repositories by utilizing a Personal Access Token.

---

> **⚠️ 이 문서는 AI로 번역된 문서입니다.**
>
> **⚠️ This document has been translated by AI.**