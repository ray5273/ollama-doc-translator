# Troubleshooting Guide

This guide provides solutions to common issues encountered while using the Ollama document translator.

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
❌ Model 'exaone3.5:7.8b' not found.
❌ Failed to pull model: network timeout
```

#### Solutions

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

4. **Disk Space Verification**:
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
   ```bash
   # Check runner status
   ./run.sh --check
   
   # Restart runner
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
- Inconsistent or inaccurate translations
- Markdown formatting issues
- Misinterpretation of technical terms

#### Solutions

1. **Adjust Temperature**:
   ```yaml
   temperature: 0.1  # For more consistent translations
   ```

2. **Use Larger Model**:
   ```yaml
   model: 'exaone3.5:32b'  # For more accurate translations
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
   prompt = f"""Translate the following Korean technical document to English.
   Ensure markdown formatting is preserved and technical terms remain in the original language.
   
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

2. **Use Smaller Model**:
   ```yaml
   model: 'mistral:7b'  # Lower memory usage
   ```

3. **Add Swap Memory** (Linux):
   ```bash
   # Create 4GB swap file
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
❌ Korean characters displayed incorrectly
```

#### Solutions

1. **Check File Encoding**:
   ```bash
   file -i docs/*.md
   ```

2. **Convert to UTF-8**:
   ```bash
   # Convert files to UTF-8
   iconv -f EUC-KR -t UTF-8 input.md > output.md
   ```

3. **Remove BOM** (If necessary):
   ```bash
   sed -i 's/^\xef\{BB\}//' input.md
   ```

## Getting Support

If issues persist:

1. **Create an Issue**:
   - Operating system and version
   - Ollama version
   - Model used
   - Error messages
   - Steps to reproduce

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

### Q: How can I speed up translations?
A: Utilize GPU acceleration, use smaller models, or run Self-hosted runners.

### Q: How do I ensure certain terms remain untranslated?
A: Include instructions in your prompt, such as "Keep technical terms in the original language."

### Q: Can I translate documents into multiple languages simultaneously?
A: Currently, only Korean to English is supported. You can sequentially process multiple languages using a matrix strategy.

### Q: Does it work with private repositories?
A: Yes, with a Personal Access Token, it supports private repositories as well.