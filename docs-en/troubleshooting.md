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
```

# Process Check
   ps aux | grep ollama

# Service Status Check (Linux)
   ```bash
   systemctl status ollama
   ```

2. **Start Ollama Server**:
   ```bash
```

# Background Execution
   ollama serve &

# or foreground execution
   ollama serve
   ```

3. **Port Check**:
   ```bash

# Check if Port 11434 is in Use
   ```bash
   netstat -tulpn | grep 11434
   lsof -i :11434
   ```

4. **Firewall Configuration**:
   ```bash
```

# Ubuntu/Debian
   sudo ufw allow 11434

# CentOS/RHEL
   ```bash
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
   ```bash```

# Model Force Redownload
   ollama rm exaone3.5:7.8b
   ollama pull exaone3.5:7.8b
   ```

3. **Proxy Configuration** (Company Network):
   ```bash
   export HTTP_PROXY=http://proxy.company.com:8080
   export HTTPS_PROXY=http://proxy.company.com:8080
   ollama pull exaone3.5:7.8b
   ```

4. **Disk Space Check**:
   ```bash
   df -h ~/.ollama/models
   ```

### 3. GitHub Actions Workflow Failure

#### Symptoms
```
❌ Action failed: Container failed to start
❌ Permission denied
```

#### Solutions

1. **Check Self-hosted Runner**:
   ```bash```
```

# Runner Status Check
   ./run.sh --check

# Runner Restart
   ./run.sh
   ```

2. **Docker Permission Issues** (Linux):
   ```bash

# Add user to docker group
   sudo usermod -aG docker $USER

# Log Out and Re-login Required
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

1. **Adjust Temperature**:
   ```yaml
   temperature: 0.1  # For more consistent translations
   ```

2. **Use a Larger Model**:
   ```yaml
   model: 'exaone3.5:32b'  # For more accurate translations
   ```

3. **Adjust Chunk Size**:
   ```python

# Modifications in entrypoint.py
   chunks = content.split('\n\n')  # by paragraph units

# Or
   ```python
   chunks = content.split('\n')    # line by line
   ```

4. **Prompt Improvement**:
   ```python
   prompt = f"""Translate the following Korean technical document into English. 
   Maintain markdown format precisely and keep technical terms as in the original text.
   
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

2. **Use a Smaller Model**:
   ```yaml
   model: 'mistral:7b'  # consumes less memory
   ```

3. **Add Swap Memory** (Linux):
   ```bash
   ```

# Create a 4GB Swap File
   ```sh
   sudo fallocate -l 4G /swapfile
   sudo chmod 600 /swapfile
   sudo mkswap /swapfile
   sudo swapon /swapfile
   ```

4. **Docker Memory Limit**:
   ```yaml
   ```

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

#### Solutions

1. **Install GitHub CLI**:
   ```bash```
```

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

3. **Token Permissions Verification**:
   - Verify repo permissions under Personal access tokens

4. **Disable Manual PR Creation**:
   ```yaml
   create-pr: false
   ```

### 7. Encoding Issues

#### Symptoms
```
❌ UnicodeDecodeError
❌ Korean characters displayed incorrectly
```

#### Solutions

1. **Check File Encoding**:
   ```bash
   file -i docs/*.md
   ```

2. **Convert to UTF-8**:
   ```bash```
```

# Convert Files to UTF-8
   ```bash
   iconv -f EUC-KR -t UTF-8 input.md > output.md
   ```

3. **Remove BOM** (if necessary):
   ```bash
   sed -i '1s/^\xEF\xBB\xBF//' *.md
   ```

## Performance Optimization Tips

### 1. Improve Translation Speed

```yaml
```

# Enable Parallel Processing
max-parallel: 3

# Skip Existing Files
skip-existing: true

# Using Faster Models
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

```yaml```
```

# Disable Debug Mode (Production)
debug: false
verbose: false

## Debugging Tools

### 1. Log Collection

```bash
```

# Ollama Logs Check
```bash
journalctl -u ollama -f
```

# Docker Logs
docker logs ollama-container

# Download GitHub Actions Logs
```bash
gh run download <run-id>
```

### 2. Direct API Testing

```bash
```

# Direct Ollama API Call

```bash
curl -X POST http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "model": "exaone3.5:7.8b",
    "prompt": "Translate '안녕하세요' to English",
    "stream": false
  }'
```

### 3. Network Diagnostics

# Network Connection Test
telnet localhost 11434

# DNS Resolution Check
```
nslookup ollama.com
```

## Requesting Support

If the issue is not resolved:

1. **Create an Issue Template**:
   - Operating System and Version
   - Ollama Version
   - Used Model
   - Error Message
   - Reproduction Steps

2. **Attach Logs**:
   ```bash
```

# Collecting Relevant Logs
   ollama serve > ollama.log 2>&1
   ```

3. **GitHub Issues**:
   - [https://github.com/your-username/ollama-doc-translator/issues](https://github.com/your-username/ollama-doc-translator/issues)

4. **Community Forum**:
   - [Ollama Discord](https://discord.gg/ollama)
   - [GitHub Discussions](https://github.com/your-username/ollama-doc-translator/discussions)
```

## Frequently Asked Questions (FAQ)

### Q: Why is translation so slow? How can I speed it up?
A: Use a GPU, opt for a smaller model, or run it on a Self-hosted runner.

### Q: How do I keep specific terms untranslated?
A: Add instructions like "Keep technical terms in the original text" to your prompt.

### Q: Is multi-language translation supported simultaneously?
A: Currently, only Korean-English translation is supported, but you can sequentially process multiple languages using a matrix strategy.

### Q: Does it work with private repositories?
A: Yes, it is usable with private repositories by using a Personal Access Token.

---

> **⚠️ 이 문서는 AI로 번역된 문서입니다.**
>
> **⚠️ This document has been translated by AI.**