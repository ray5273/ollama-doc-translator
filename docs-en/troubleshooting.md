# Problem Solution Guide

This guide provides information on common issues that may arise when using the Ollama document translator, as well as solutions to those problems.

## Common Issues

### 1. Ollama Server Connection Error

#### Symptoms
```
❌ Error: The Ollama server is not running.
❌ Connection refused: http://localhost:11434
```

#### Solutions

1. **Check the status of the Ollama server**:
```bash
```

# Process Verification
ps aux | grep ollama

# Checking Service Status (Linux)
   systemctl status ollama

2. **Starting the Ollama Server**:
   ```bash
```

# Background Execution
   ollama serve &

# Or run it in the background
   ollama serve
   ```

3. **Port checking**:
   ```bash

# Check if port 11434 is in use
   netstat -tulpn | grep 11434
   lsof -i :11434

4. **Firewall settings**:
   ```bash
```

# Ubuntu/Debian
sudo ufw allow 11434

# CentOS/RHEL
   sudo firewall-cmd --add-port=11434/tcp --permanent
   sudo firewall-cmd --reload
   ```

### 2. Model Download Failure

#### Symptoms
```
❌ The model 'exaone3.5:7.8b' cannot be found.
❌ Failed to pull model: network timeout
```

#### Solutions

1. **Check Internet connection**:
   ```bash
   curl -I https://ollama.com
   ```

2. **Download the model manually**:
   ```bash

# Forced Re-download of Models
   ollama rm exaone3.5:7.8b
   ollama pull exaone3.5:7.8b
   ```

3. **Proxy Settings** (for company network):
   ```bash
   export HTTP_PROXY=http://proxy.company.com:8080
   export HTTPS_PROXY=http://proxy.company.com:8080
   ollama pull exaone3.5:7.8b
   ```

4. **Checking Disk Space**:
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

1. **Check the Self-hosted Runner**:
   ```bash

# Checking Runner Status
   ./run.sh --check

# Restarting Runner
   ./run.sh
   ```

2. **Docker Permission Issues** (Linux):
   ```bash

# Add the user to the docker group
sudo usermod -aG docker $USER

# Re-login required after logging out
newgrp docker
```

3. **Checking token permissions:**
- Repository Settings → Actions → General
- Select “Read and write permissions” under “Workflow permissions”

### 4. Translation quality issues

#### Symptoms
- Inaccurate or inconsistent translations
- Corruption of markdown format
- Incorrect translation of technical terms

#### Solutions

1. **Adjusting the temperature setting:**
   ```yaml
   temperature: 0.1  # For more consistent translations
   ```

2. **Using a larger model:**
   ```yaml
   model: 'exaone3.5:32b'  # For more accurate translations
   ```

3. **Adjusting the chunk size:**
   ```python

# Modifications in entrypoint.py
chunks = content.split('\n\n')  # Paragraphs separated by newline lines

# Or
   chunks = content.split('\n')    # Line-by-line splitting

4. **Prompt Improvement**:
   ```python
   prompt = f"""Please translate the following Korean technical document into English.
   Maintain the markdown format accurately, and keep the technical terms as they are in the original text.

   Korean Text:
   {text}

   English Translation: """
   ```

### 5. Out of Memory Error

#### Symptoms
```
❌ Out of memory error
❌ Model failed to load
```

#### Solutions

1. **Check system memory**:
   ```bash
   free -h
   htop
   ```

2. **Use a smaller model**:
   ```yaml
   model: 'mistral:7b'  # Uses less memory
   ```

3. **Add swap memory** (Linux):
   ```bash
```

# Creating a 4GB swap file
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

4. **Docker memory limits**:
```yaml

# docker-compose.yml
services:
  ollama:
    deploy:
      resources:
        limits:
          memory: 8G

### 6. Failure to Create a Pull Request

#### Symptoms
```
❌ Failed to create pull request
❌ GitHub CLI not found
```

#### Solutions

1. **Install GitHub CLI**:
   ```bash
```

# Ubuntu/Debian
sudo apt install gh

# macOS
brew install gh

# Windows
   winget install GitHub.cli

2. **Authentication Settings:**
   ```bash
   gh auth login
   ```

3. **Checking Token Permissions:**
   - Verify repo permissions from the Personal access tokens section.

4. **Disabling Manual PR Creation:**
   ```yaml
   create-pr: false
   ```

### 7. File Encoding Issues

#### Symptoms:
```
❌ UnicodeDecodeError
❌ Korean text is displayed incorrectly.
```

#### Solutions:

1. **Check File Encoding:**
   ```bash
   file -i docs/*.md
   ```

2. **Convert to UTF-8:**
   ```bash
   ```
   convert files to UTF-8 encoding.
   ```
```

# Convert files to UTF-8 format
iconv -f EUC-KR -t UTF-8 input.md > output.md

3. **Remove the BOM (if necessary):**
```bash
sed -i '1s/^\xEF\xBB\xBF/' *.md
```

## Performance Optimization Tips

### 1. Improving Translation Speed

# Enable Parallel Processing
max-parallel: 3

# Skip Existing Files
skip-existing: true

# Using a Faster Model
model: 'mistral:7b'

### 2. Resource Monitoring

```bash
```

# System Resource Monitoring
htop
iostat -x 1
nvidia-smi  # When using a GPU

### 3. Adjusting Log Levels

```yaml
```

# Disable Debug Mode (Production)
debug: false
verbose: false

## Debugging Tools

### 1. Log Collection

```bash
```

# Checking Ollama logs
journalctl -u ollama -f

# Docker Logs
docker logs ollama-container

# Downloading GitHub Actions logs
gh run download <run-id>

### 2. Direct testing of the API

```bash
```

# Direct Call to the Ollama API
curl -X POST http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "model": "exaone3.5:7.8b",
    "prompt": "Translate 'Hello' into English",
    "stream": false
  }'
```

### 3. Network Diagnosis

```bash

# Network Connection Test
telnet localhost 11434

# Checking DNS Resolution
nslookup ollama.com

## Requesting Support

If the issue is not resolved:

1. **Create an Issue Template**:
   - Operating System and Version
   - Ollama Version
   - Model Used
   - Error Message
   - Steps to Replicate the Issue

2. **Attach Logs**:
   ```bash
```

# Related log collection
   ollama serve > ollama.log 2>&1
   ```

3. **GitHub Issues**:
   - [https://github.com/your-username/ollama-doc-translator/issues](https://github.com/your-username/ollama-doc-translator/issues)

4. **Community Forum**:
   - [Ollama Discord](https://discord.gg/ollama)
   - [GitHub Discussions](https://github.com/your-username/ollama-doc-translator/discussions)
```

## Frequently Asked Questions (FAQ)

### Q: The translation is too slow; how can I make it faster?
A: You can use a GPU, switch to a smaller model, or run it on a self-hosted runner.

### Q: How do I keep certain terms untranslated and retain their original form?
A: Add instructions to your prompt, such as “Maintain technical terms in their original language.”

### Q: Is it possible to translate multiple languages simultaneously?
A: Currently, only Korean-English translation is supported, but with a matrix strategy, it’s possible to process multiple languages sequentially.

### Q: Does it work on private repositories as well?
A: Yes, it can be used on private repositories as well with the use of a Personal Access Token.

---

> **⚠️ 이 문서는 AI로 번역된 문서입니다.**
>
> **⚠️ This document has been translated by AI.**