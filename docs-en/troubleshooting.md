# Problem Solution Guide

This guide provides information on common issues that may arise when using the Ollama document translator, as well as solutions to those problems.

## Common Issues

### 1. Ollama Server Connection Errors

#### Symptoms
```
❌ Error: The Ollama server is not running.
❌ Connection refused: http://localhost:11434
```

#### Solutions

1. **Check the Ollama server status**:
   ```bash
   # Check for processes
   ps aux | grep ollama
   
   # Check service status (Linux)
   systemctl status ollama
   ```

2. **Start the Ollama server**:
   ```bash
   # Run in the background
   ollama serve &
   
   # Or run it in the foreground
   ollama serve
   ```

3. **Check the port**:
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
❌ The model 'exaone3.5:7.8b' cannot be found.
❌ Failed to pull the model: network timeout
```

#### Solutions

1. **Check Internet connection**:
   ```bash
   curl -I https://ollama.com
   ```

2. **Download the model manually**:
   ```bash
   # Force a re-download of the model
   ollama rm exaone3.5:7.8b
   ollama pull exaone3.5:7.8b
   ```

3. **Set proxy settings** (for company networks):
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
❌ Action failed: Container failed to start.
❌ Permission denied.
```

#### Solutions

1. **Check the self-hosted Runner status**:
   ```bash
   # Check the runner status
   ./run.sh --check
   
   # Restart the runner
   ./run.sh
   ```

2. **Docker permission issues (Linux)**:
   ```bash
   # Add the user to the docker group
   sudo usermod -aG docker $USER
   
   # You need to log out and then log in again.
   newgrp docker
   ```

3. **Check token permissions**:
   - Go to Repository Settings → Actions → General
   - Select "Read and write permissions" for "Workflow permissions".

### 4. Translation Quality Issues

#### Symptoms
- Inaccurate or inconsistent translations
- Corruption of markdown format
- Incorrect translation of technical terms

#### Solutions

1. **Adjusting the Temperature**:  
   ```yaml
   temperature: 0.1  # For more consistent translations
   ```

2. **Using a Larger Model**:  
   ```yaml
   model: 'exaone3.5:32b'  # For more accurate translations
   ```

3. **Adjusting the Chunk Size**:  
   ```python
   # Modify in entrypoint.py
   chunks = content.split('\n\n')  # By paragraph
   # Or
   chunks = content.split('\n')    # By line
   ```

4. **Improving the Prompt**:  
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
   # Create a 4GB swap file
   sudo fallocate -l 4G /swapfile
   sudo chmod 600 /swapfile
   sudo mkswap /swapfile
   sudo swapon /swapfile
   ```

4. **Set Docker memory limits**: 
   ```yaml
   # docker-compose.yml
   services:
     ollama:
       deploy:
         resources:
           limits:
             memory: 8G
   ```

### 6. Failed to create a pull request

#### Symptoms
```
❌ Failed to create a pull request
❌ GitHub CLI not found
```

#### Solutions

1. **Install the GitHub CLI**:
   ```bash
   # Ubuntu/Debian
   sudo apt install gh
   
   # macOS
   brew install gh
   
   # Windows
   winget install GitHub.cli
   ```

2. **Set up authentication**:
   ```bash
   gh auth login
   ```

3. **Check token permissions**: 
   Verify your personal access tokens for repo permissions.

4. **Disable automatic PR creation**: 
   ```yaml
   create-pr: false
   ```

### 7. File Encoding Issues

#### Symptoms
```
❌ UnicodeDecodeError
❌ Korean text is displayed incorrectly
```

#### Solutions

1. **Check file encoding**:
   ```bash
   file -i docs/*.md
   ```

2. **Convert to UTF-8**:
   ```bash
   # Convert the files to UTF-8
   iconv -f EUC-KR -t UTF-8 input.md > output.md
   ```

3. **Remove the BOM (if necessary)**:
   ```bash
   sed -i '1s/^\xEF\xBB\xBF/' *.md
   ```

## Performance Optimization Tips

### 1. Improving Translation Speed

```yaml
# Enable parallel processing
max-parallel: 3

# Skip existing files
skip-existing: true

# Use a faster model
model: 'mistral:7b'
```

### 2. Resource Monitoring

```bash
# Monitor system resources
htop
iostat -x 1
nvidia-smi  # When using a GPU
```

### 3. Adjusting Log Levels

```yaml
# Disable debug mode (for production)
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
# Directly call the Ollama API
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
# Test network connection
telnet localhost 11434

# Check DNS resolution
nslookup ollama.com
```

## Requesting Support

If the issue is not resolved, please follow these steps:

1. **Create an Issue Template**:
   - Operating System and Version
   - Ollama Version
   - Model Used
   - Error Message
   - Steps to Replicate the Issue

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

## Smart Choking & Debugging Issues

### 8. Problems with Handling Large Documents

#### Symptoms
```
❌ Context length exceeded
❌ Chunks generated are too large
❌ Translation stops midway
```

#### Solutions

1. **Adjust the context length**:
   ```yaml
   context-length: 4096    # Set to a value lower than the default of 32768
   ```

2. **Analyze chunking in debug mode**:
   ```yaml
   debug-mode: true
   ```
   
   Files generated:
   - `debug_chunks/`: Analysis for each individual chunk
   - `debug_originals/`: Original chunks
   - `debug_translations/`: Translated chunks

3. **Check console output**:
   ```bash
   📦 15 token-aware chunks created:
      Chunk 1: 1,156 tokens (2,845 chars)  # Check the number of tokens
   ```

### 9. Issue with damaged code blocks

#### Symptoms
```markdown
# Original
```python
def hello():
    print("world")
```

# Translation result (in incorrect cases)
```python
def hello():
```
print("world")
```

#### Solutions

1. **Check debug comparison files**:
   ```bash
   debug_comparisons/filename_comparison_001.md
   ```

2. **Verify section-based chunking**:
   - Ensure that code blocks are not split in the middle of chunking.
   - Check that chunks are correctly separated based on H1-H3 headings.

3. **Enhance translation prompts**:
   The current system already includes logic to preserve code blocks:
   ```
   - IMPORTANT: Do NOT add **bold**, *italic*, or any formatting that was not in the original text.
   - Only translate text content; never modify or add markdown formatting.
   ```

### 10. Translation Quality Inconsistency Issues

#### Symptoms
```
❌ The same terms are translated differently.
❌ The style of translation varies from check to check.
❌ Numbers in numbered lists disappear.
```

#### Solutions

1. **Adjusting the “Temperature” Setting**:
   ```yaml
   temperature: 0.1        # For more consistent translations (default value: 0.3).
   ```

2. **Increasing the Number of Retries**:
   ```yaml
   max-retries: 5         # Default value: 3.
   ```

3. **Comparing and Analyzing Translations**:
   ```bash
   # Compare the original text with the translated text.
   debug_comparisons/filename_comparison_001.md
   ```

4. **Ensuring Numbered Lists Are Preserved**:
   The system is designed to preserve the following pattern:
   ```markdown
   # Original Text
   - 288. Cache Invalidation Scenario

   # Translated Text
   - 288. Cache Invalidation Scenario
   ```

### 11. How to Use Debug Files

#### Understanding the Structure of Debug Files

1. **Translation Analysis** (`debug_chunks/`):
   ```markdown
   <!-- DEBUG CHUNK 1/15 -->
   <!-- Tokens: 1,156 -->
   <!-- Characters: 2,845 -->
   --> <!-- Source: docs/api-guide.md -->
   ```

2. **Translation Performance Analysis**:
   📊 Translation Performance Summary:
      ⏱️ Total time: 2m 34s
      📄 Files processed: 12
      🔄 Total chunks: 67
      📈 Average chunk size: 1,089 tokens
   ```

3. **Identifying Problem Patterns**:
   - Repeated errors occurring in specific chunks
   - Decline in quality within certain token ranges
   - Format corruption in specific Markdown patterns

#### Optimization Tips

1. **Optimal Chunk Size**:
   - 1,000-1,500 tokens: Balance between optimal quality and speed
   - 500-800 tokens: High quality, but slower speed
   - 2,000+ tokens: Fast speed, but risk of reduced quality

2. **Utilizing Section-Based Division**:
   - H1-H2: Always serve as division boundaries
   - H3: Divide when the content exceeds 200 tokens
   - Code blocks: Never divide
```

## Frequently Asked Questions (FAQ)

### Q: The translation is too slow; how can I make it faster?
A: Use a GPU, switch to a smaller model, or run it on a self-hosted runner.

### Q: How do I keep certain terms untranslated and retain their original form?
A: Add instructions such as “Technical terms should be retained in their original language” to your prompt.

### Q: Is it possible to translate multiple languages simultaneously?
A: Currently, only Korean-English translation is supported, but with a matrix strategy, it’s possible to process multiple languages sequentially.

### Q: Does it also work on private repositories?
A: Yes, it can be used on private repositories as well with the use of a Personal Access Token.

---

> **⚠️ 이 문서는 AI로 번역된 문서입니다.**
>
> **⚠️ This document has been translated by AI.**