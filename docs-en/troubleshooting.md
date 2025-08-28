# Problem Solving Guide

## Common Issues and Solutions When Using Ollama Document Translator

This guide provides information on typical problems encountered and their resolutions while using the Ollama Document Translator.

## Common Issues

### 1. Ollama Server Connection Error

#### Symptoms
```
❌ Error: Ollama server is not running.
❌ Connection refused: http://localhost:11434
```

#### Solution Method

```markdown
1. **Check Ollama Server Status**:
   ```bash
   # Check Processes
   ps aux | grep ollama
   
   # Check Service Status (Linux)
   systemctl status ollama
   ```
```

```markdown
2. **Start Ollama Server**:
   ```bash
   # Run in background
   ollama serve &
   
   # Or run in foreground
   ollama serve
   ```
```

```markdown
3. **Port Check**:
   ```bash
   # Check if port 11434 is in use
   netstat -tulpn | grep 11434
   lsof -i :11434
   ```
```

```markdown
4. **Firewall Configuration**:
   ```bash
   # Ubuntu/Debian
   sudo ufw allow 11434
   
   # CentOS/RHEL
   sudo firewall-cmd --add-port=11434/tcp --permanent
   sudo firewall-cmd --reload
   ```
```

### 2. Model Download Failure

#### Symptoms
```
❌ Model 'exaone3.5:7.8b' not found.
❌ Failed to pull model: network timeout
```

#### Solution Method

```markdown
1. **Check Internet Connection**:
   ```bash
   curl -I https://ollama.com
   ```

2. **Manually Download the Model**:
   ```bash
   # Force Redownload the Model
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

#### Solution Method

```markdown
1. **Self-hosted Runner Verification**:
   ```bash
   # Check Runner Status
   ./run.sh --check
   
   # Restart Runner
   ./run.sh
   ```
```

2. **Docker Permission Issues** (Linux):
   ```bash
   # Add user to the docker group
   sudo usermod -aG docker $USER
   
   # Requires logging out and logging back in
   newgrp docker
   ```

3. **Token Authorization Verification**:
   - Repository Settings → Actions → General
   - Select "Read and write permissions" under "Workflow permissions"

### 4. Translation Quality Issues

#### Symptoms
- Inaccurate or inconsistent translations
- Broken Markdown formatting
- Incorrect translation of specialized terminology

#### Solution Method

```markdown
1. **Temperature Adjustment**:
   ```yaml
   temperature: 0.1  # More Consistent Translation
   ```

```yaml
model: 'exaone3.5:32b'  # For more accurate translation
```

```python
# Adjust chunk size in entrypoint.py
chunks = content.split('\n\n')  # By paragraph
# Alternatively,
chunks = content.split('\n')   # By line
```

```python
prompt = f"""Translate the following Korean technical document into English. 
Maintain Markdown format precisely and keep technical terms in the original language.

Korean Text:
{text}

English Translation:"""
```

### 5. Memory Insufficient Error

#### Symptoms
```
❌ Out of Memory Error
❌ Model Failed to Load
```

#### Solution Method

1. **System Memory Check**:
   ```bash
   free -h
   htop
   ```

```yaml
model: 'mistral:7b'  # Uses less memory
```

**3. Add Swap Memory** (Linux):
   ```bash
   # Create a 4GB swap file
   sudo fallocate -l 4G /swapfile
   sudo chmod 600 /swapfile
   sudo mkswap /swapfile
   sudo swapon /swapfile
   ```

```yaml
# docker-compose.yml
services:
  ollama:
    deploy:
      resources:
        limits:
          memory: 8G
```

### 6. Failure to Create a Pull Request

#### Symptoms
```
❌ Failed to create pull request
❌ GitHub CLI not found
```

#### Solution Method

```markdown
1. **Installation of GitHub CLI**:
   ```bash
   # Ubuntu/Debian
   sudo apt install gh
   
   # macOS
   brew install gh
   
   # Windows
   winget install GitHub.cli
   ```
```

2. **Authentication Setup**:
   ```bash
   gh auth login
   ```

3. **Token Authorization Check**:
   - Verify repo permissions under Personal access tokens

```yaml
create-pr: false
```

### 7. File Encoding Issues

#### Symptoms
```
❌ UnicodeDecodeError
❌ Hangul characters displayed incorrectly
```

#### Solution Method

```bash
file -i docs/*.md
```

```markdown
2. **Convert to UTF-8**:
   ```bash
   # Convert file to UTF-8
   iconv -f EUC-KR -t UTF-8 input.md > output.md
   ``` 
```

3. **Remove BOM** (if necessary):
   ```bash
   sed -i '1s/^\xEF\xBB\xBF//' *.md
   ```

## Performance Optimization Tips

### 1. Enhancing Translation Speed

```yaml
# Enable Parallel Processing
max-parallel: 3
```

# Skip Existing Files
```markdown
skip-existing: true
```

# Using Faster Models
model: 'mistral:7b'

### 2. Resource Monitoring

```bash
# System Resource Monitoring
htop
iostat -x 1
nvidia-smi  # When using GPU
```

### 3. Adjusting Log Levels

```yaml
# Disable Debug Mode (Production)
debug: false
verbose: false
```

## Debugging Tools

### 1. Log Collection

```bash
# Checking Ollama Logs
journalctl -u ollama -f
```

# Docker Logs
```bash
docker logs ollama-container
```

# Download GitHub Actions Logs
```
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
# Network Connection Test
telnet localhost 11434
```

# DNS Resolution Check
```
nslookup ollama.com
```

## Request Support

```
If the problem persists:
```

```markdown
1. **Issue Template Creation**:
   - Operating System and Version
   - Ollama Version
   - Used Model
   - Error Messages
   - Reproduction Steps
```

```markdown
2. **Attach Logs**:
   ```bash
   # Collect Relevant Logs
   ollama serve > ollama.log 2>&1
   ```

3. **GitHub Issues**:
   - [https://github.com/your-username/ollama-doc-translator/issues](https://github.com/your-username/ollama-doc-translator/issues)

4. **Community Forum**:
   - [Ollama Discord](https://discord.gg/ollama)
   - [GitHub Discussions](https://github.com/your-username/ollama-doc-translator/discussions)

## Frequently Asked Questions (FAQ)

### Q: Why is translation so slow? How can I speed it up?
A: Use a GPU, opt for a smaller model, or run on a Self-hosted runner.

### Q: How do you keep specific terms untranslated?
A: Add instructions in the prompt such as "Maintain technical terms in their original language."

### Q: Can translations be done simultaneously in multiple languages?
A: Currently, only Korean-English translation is supported, but multiple languages can be processed sequentially using a matrix strategy.

### Q: Does it work with private repositories as well?
A: Yes, it is usable with private repositories by using a Personal Access Token.