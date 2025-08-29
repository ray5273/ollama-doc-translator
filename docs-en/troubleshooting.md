# Solution Guide

Guide to common issues that may occur while using the Ollama document translator and their solutions.

## Common Issues
 (No additional translation or explanation provided, only the translated text is given.)

1. Ollama server connection error

#### Symptoms
 ```
❌ Error: The Ollama server is not running.
❌ Connection refused: http://localhost:11434
```

#### Solution

(No additional explanation or context provided, just the translation of the given Korean text to English while maintaining the Markdown format and structure.)

1. **Check Ollama Server Status:**
   ```bash
   # Check processes
   ps aux | grep ollama
   
   # Check service status (Linux)
   systemctl status ollama
   ```

2. **Start an Ollama Server:**
   ```bash
   # Run in background
   ollama serve &
   
   # Or run in foreground
   ollama serve
   ```

3. **Port Check:**
   ```bash
   # Check if port 11434 is in use
   netstat -tulpn | grep 11434
   lsof -i :11434
   ```

4. **Firewall Setup:**
```bash
# Ubuntu/Debian
sudo ufw allow 11434

# CentOS/RHEL
sudo firewall-cmd --add-port=11434/tcp --permanent
sudo firewall-cmd --reload
```

2. Model download failure

#### Symptoms
 ```
❌ Model 'exaone3.5:7.8b' not found
❌ Failed to pull model: network timeout
```

#### Solution

(No additional explanation or context provided, just the translation of the given Korean text to English while maintaining the Markdown format and structure.)

1. **Verify internet connection:**
   ```bash
   curl -I https://ollama.com
   ```

2. **Manually download a model:**
```bash
# Forcefully re-download a model
ollama rm exaone3.5:7.8b
ollama pull exaone3.5:7.8b
```

3. **Proxy Setup** (Corporate Network):
```bash
export HTTP_PROXY=http://proxy.company.com:8080
export HTTPS_PROXY=http://proxy.company.com:8080
ollama pull exaone3.5:7.8b
```

4. **Disk space check:**
   ```bash
   df -h ~/.ollama/models
   ```

3. GitHub Actions workflow failure

#### Symptoms
 ```
❌ Action failed: Container failed to start
❌ Permission denied
```

#### Solution

(No additional explanation or context provided, just the translation of the given Korean text to English while maintaining the Markdown format and structure.)

1. **Verify Self-hosted Runner:**
   ```bash
   # Check Runner status
   ./run.sh --check
   
   # Restart the Runner
   ./run.sh
   ```

2. **Docker permission issue** (Linux):
```bash
# Add the user to the docker group
sudo usermod -aG docker $USER

# Logout required after this, then re-login
newgrp docker
```

3. **Token permission verification:**
   - Go to Repository Settings → Actions → General
   - In "Workflow permissions", select "Read and write permissions"

4. Translation quality issues

#### Symptoms
- Translation is inaccurate or inconsistent
- Markdown formatting is broken
- Professional terminology is mistranslated

#### Solution

(No additional explanation or context provided, just the translation of the given Korean text to English while maintaining the Markdown format and structure.)

1. **Temperature Adjustment:**
   ```yaml
   temperature: 0.1  # for more consistent translation
   ```

2. **Use a Larger Model:**
   ```yaml
   model: 'exaone3.5:32b'  # More accurate translation
   ```

3. **Adjust chunk size:**
   ```python
   # Modified in entrypoint.py
   chunks = content.split('\n\n')  # by paragraphs
   # Or
   chunks = content.split('\n')    # by lines
   ```

4. **Prompt Improvement:**
```python
prompt = f"""Please translate the following Korean described text to English, maintaining the Markdown format and keeping the terminology in the original language.

Korean Text:
{text}

English Translation:}"""
```

5. Memory card insufficient error

#### Symptoms
 ```
 ❌ Out of memory error
 ❌ Model failed to load
 ```

#### Solution

(No additional explanation or context provided, just the translation of the given Korean text to English while maintaining the Markdown format and structure.)

1. **Check system memory:**
   ```bash
   free -h
   htop
   ```

2. **Use a smaller model:**
   ```yaml
   model: 'mistral:7b'  # Uses less memory
   ```

3. **Add swap memory** (Linux):
```bash
# Create a 4GB swap file
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

4. **Limit Docker Memory:**
   ```yaml
   # docker-compose.yml
   services:
     ollama:
       deploy:
         resources:
           limits:
             memory: 8G
   ```

6. Failed to create Pull Request

#### Symptoms
 ```
 X Failed to create pull request
 X GitHub CLI not found
 ```

#### Solution

(No additional explanation or context provided, just the translation of the given Korean text to English while maintaining the Markdown format and structure.)

1. **Install GitHub CLI:**
   ```bash
   # Ubuntu/Debian
   sudo apt install gh
   
   # macOS
   brew install gh
   
   # Windows
   winget install GitHub.cli
   ```

2. **Authentication Setup:**
   ```bash
   gh auth login
   ```

3. **Verify token permissions:**
   - Verify repo permissions for personal access tokens

4. **Disable automatic PR generation:**
   ```yaml
   create-pr: false
   ```

7. File encoding issue

#### Symptoms
 ```
❌ UnicodeDecodeError
❌ Corrupted display of Hangul (Korean characters)
```

#### Solution

(No additional explanation or context provided, just the translation of the given Korean text to English while maintaining the Markdown format and structure.)

1. **Verify file encoding:**
   ```bash
   file -i docs/*.md
   ```

2. **Convert to UTF-8:**
   ```bash
   # Convert file to UTF-8
   iconv -f EUC-KR -t UTF-8 input.md > output.md
   ```

3. **Remove BOM** (if needed):
```bash
sed -i '1s/^\\xEF\\xBB\\xBF//' *.md
```

## Performance optimization tips

1. Improve translation speed

```yaml
 # Enable parallel processing
 max-parallel: 3

# Existing file skip
 skip-existing: true

# Using a Faster Model
model: "mistral:7b"
```

2. Resource Monitoring

```bash
 # System resource monitoring
 htop
 iostat -x 1
 nvidia-smi  # For GPU usage
```

3. Adjust log level

```yaml
 # Disable debug mode (production)
 debug: false
 verbose: false
```

## Debugging Tools

1. Log collection

```bash
 # Check Ollama log
 journalctl -u ollama -f
```

# Docker logs
 docker logs ollama-container

# Download GitHub Actions logs
 gh run download <run-id>
 ```

2. Direct API testing

Note: The English translation provided is accurate to the given input, maintaining the Markdown format and structure while only including the translated text without any additional explanation.

```bash
 # Direct call to Ollama API
 curl -X POST http://localhost:11434/api/generate \
   -H "Content-Type: application/json" \
   -d '{"model": "exaone3.5.7.8b", "prompt": "Translate Hello in Korean to English", "stream": false}'

3. Network Diagnostics

```bash
 # Network connection test
 telnet localhost 11434
```

# Check DNS resolution for ollama.com
nslookup ollama.com
```

## Request Support

In case the issue is not resolved:

1. **Issue Template Creation:**
   - Operating system and version
   - Ollama version
   - Model used
   - Error message
   - Steps to reproduce

2. **Log Attachment:**
   ```bash
   # Collect relevant logs
   ollama serve > ollama.log 2>&1
   ```

3. **GitHub Issues:**
   - [https://github.com/your-username/ollama-doc-translator/issues](https://github.com/your-username/ollama-doc-translator/issues)

4. **Community Forums:**
   - [Ollama Discord] (https://discord.gg/ollama)
   - [GitHub Discussions](https://github.com/your-username/ollama-doc-translator/discussions)

## Frequently Asked Questions (FAQ)

Q: How can I make the translation faster?
A: You can use a GPU, use a smaller model, or run it on a self-hosted runner.

To indicate that certain terms should not be translated but kept as they are, add a note like "Keep specified terms untranslated" in the prompt.

Q: Can you perform translations simultaneously in multiple languages?
A: Currently, we only support Korean to English, but with our matrix strategy, it is possible to process multiple languages sequentially.

Q: Does it work with a private repository as well?
A: Yes, using a Personal Access Token allows you to use it with a private repository.