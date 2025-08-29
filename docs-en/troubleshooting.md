# Troubleshooting Guide

Here's a guide to common issues and solutions when using the Ollama documentation translator.

## Common Issues

### 1. Ollama Server Connection Error

#### Symptoms
```
❌ Error: Ollama server is not running.
❌ Connection refused: http://localhost:11434
```

#### Solutions

1. **Check Ollama Server Status**:
   ```bash
   # Check process
   ps aux | grep ollama
   
   # Check service status (Linux)
   systemctl status ollama
   ```

2. **Ollama Server Startup**:
   ```bash
   # Run in the background
   ollama serve &
   
   # Or run in the foreground
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
❌ Model 'exaone3.5:7.8b' not found.
❌ Failed to pull model: network timeout
```

#### Solutions

1. **Check Internet Connection**:
   ```bash
   curl -I https://ollama.com
   ```

2. **Manually Download the Model**:
   ```bash
   # Force re-download the model
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

#### Solutions

1. **Self-hosted Runner 확인**:
   ```bash
   # Check Runner status
   ./run.sh --check
   
   # Restart Runner
   ./run.sh
   ```

2. **Docker Permissions Issue** (Linux):
   ```bash
   # Add user to the docker group
   sudo usermod -aG docker $USER
   
   # Logout and relogin required
   newgrp docker
   ```

3. **Verify Token Permissions**:
   - Repository Settings → Actions → General
   - Select "Read and write permissions" in "Workflow permissions"

### 4. Translation Quality Issues

#### Symptoms
- Inaccurate or inconsistent translation
- Markdown formatting is broken
- Technical terms are mistranslated

#### Solutions

1. **Temperature Adjustment**:
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
   chunks = content.split('\n\n')  # Paragraph-based
   # Or
   chunks = content.split('\n')    # Line-based
   ```

4. **Prompt Improvement**:
   ```python
   prompt = f"""Please translate the following Korean technical document into English. 
   Please maintain the markdown format exactly, and keep technical terms as is from the original.
   
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

2. **Use a smaller model**:
   ```yaml
   model: 'mistral:7b'  # Use less memory
   ```

3. **Add Swap Memory** (Linux):
   ```bash
   # Create a 4GB swap file
   sudo fallocate -l 4G /swapfile
   sudo chmod 600 /swapfile
   sudo mkswap /swapfile
   sudo swapon /swapfile
   ```

4. **Docker Memory Limits**:
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

2. **Authentication Setup**:
   ```bash
   gh auth login
   ```

3. **Token Permission Verification**:
   - Verify repo permissions in Personal access tokens

4. **Disable Manual PR Creation**:
   ```yaml
   create-pr: false
   ```

### 7. File Encoding Issues

#### Symptoms
```
❌ UnicodeDecodeError
❌ Korean characters are displayed incorrectly
```

#### Solutions

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

### 1. Translation Speed Improvement

```yaml
# Enable Parallel Processing
max-parallel: 3
```

# Skip Existing File
skip-existing: true

# Using a Faster Model
model: 'mistral:7b'

### 2. Resource Monitoring

```bash
# System Resource Monitoring
htop
iostat -x 1
nvidia-smi  # When using GPU
```

### 3. Log Level Adjustment

```yaml
# Disable debug mode (production)
debug: false
verbose: false
```

## Debugging Tools

### 1. Log Collection

```bash
# Check Ollama Logs
journalctl -u ollama -f
```

# Docker Logs
docker logs ollama-container

# Download GitHub Actions Log
gh run download <run-id>

### 2. API Direct Testing

```bash
# Direct Ollama API Call
curl -X POST http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "model": "exaone3.5:7.8b",
    "prompt": "Translate 안녕하세요 to English",
    "stream": false
  }'
```

### 3. Network Diagnostics

```bash
# Network Connection Test
telnet localhost 11434
```

# DNS Resolution Check
nslookup ollama.com

## Requesting Support

문제가 해결되지 않는 경우:

If the problem persists:

1. **Issue Template Creation**:
   - Operating System and Version
   - Ollama Version
   - Model Used
   - Error Message
   - Reproduction Steps

2. **Log Attachment**:
   ```bash
   # Collect relevant logs
   ollama serve > ollama.log 2>&1
   ```

3. **GitHub Issues**:
   - [https://github.com/your-username/ollama-doc-translator/issues](https://github.com/your-username/ollama-doc-translator/issues)

4. **Community Forum**:
   - [Ollama Discord](https://discord.gg/ollama)
   - [GitHub Discussions](https://github.com/your-username/ollama-doc-translator/discussions)

## Frequently Asked Questions (FAQ)

### Q: 번역이 너무 느린데 어떻게 빠르게 할 수 있나요?
A: Use a GPU, use a smaller model, or run on a Self-hosted runner.

### Q: How to keep specific terms untranslated?
A: Add instructions like "Keep technical terms in the original language" to the prompt.

### Q: Can I translate simultaneously into multiple languages?
A: Currently, we only support Korean-English translation, but we can process multiple languages sequentially using a matrix strategy.

### Q: Does it work with private repositories?
A: Yes, it is available for private repositories when using a Personal Access Token.