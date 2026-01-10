# Troubleshooting Guide

This guide provides common issues that may arise while using the Ollama document translator and their solutions.

[TRANSLATION_START]
# Troubleshooting Guide

This guide provides common issues that may arise while using the Ollama document translator and their solutions.
[TRANSLATION_END]

## Common Issues

### 1. Ollama Server Connection Error

#### Symptoms
```
❌ Error: Ollama Server Executed Here It does not..
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

3. **Check Port**:
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
❌ Model 'exaone3.5:7.8b' Find 수 There is no text to translate..
❌ Failed to pull model: network timeout
```

#### Solutions

1. **Check Internet Connection**:
   ```bash
   curl -I https://ollama.com
   ```

2. **Manually downloading the model**:
   ```bash
   # Model forced re-download
   ollama rm exaone3.5:7.8b
   ollama pull exaone3.5:7.8b
   ```

3. **Proxy Configuration** (Company Network):
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

#### Solutions

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
   
   # Log out and log in again required
   newgrp docker
   ```

3. **Check Token Permissions**:
   - Repository Settings → Actions → General
   - Select "Read and write permissions" under "Workflow permissions"

### 4. Translation Quality Issues

#### Symptoms
- Translations are inaccurate or inconsistent
- Markdown formatting is broken
- Technical terms are mistranslated

#### Solutions

1. **Adjust Temperature**:
   ```yaml
   temperature: 0.1  # for more consistent translations
   ```

2. **Use a Larger Model**:
   ```yaml
   model: 'exaone3.5:32b'  # for more accurate translations
   ```

3. **Adjust Chunk Size**:
   ```python
   # Modify in entrypoint.py
   chunks = content.split('\n\n')  # by paragraphs
   # or
   chunks = content.split('\n')    # by lines
   ```

4. **Improve Prompts**:
   ```python
   prompt = f"""Please translate the following Korean technical document into English. 
   Maintain the Markdown format precisely and keep technical terms as in the original text.
   
   Korean Text:
   {text}
   
   English Translation:"""
   ```

### 5. Memory Out of Error

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

2. **Using a smaller model**:
   ```yaml
   model: 'mistral:7b'  # Less memory usage
   ```

3. **Add swap memory** (Linux):
   ```bash
   # Creating a 4GB swap file
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

### 6. Failed to Create Pull Request

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

2. **Set Up Authentication**:
   ```bash
   gh auth login
   ```

3. **Check Token Permissions**:
   - Verify repo permissions under Personal access tokens

4. **Disable Manual PR Creation**:
   ```yaml
   create-pr: false
   ```

### 7. File Encoding Issues

#### Symptoms
```
❌ UnicodeDecodeError
❌ English Broken Marked
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

### 1. Improve Translation Speed

```yaml
# Enable Parallel Processing
max-parallel: 3

# Skipping existing files
skip-existing: true

# Using a faster model
model: 'mistral:7b'
```

### 2. Resource Monitoring

```bash
# System Resource Monitoring
htop
iostat -x 1
nvidia-smi  # Using GPU
```

### 3. Adjust Log Levels

```yaml
# Deactivate Debug Mode (Production)
debug: false
verbose: false
```

## Debugging Tools

### 1. Log Collection

```bash
# Ollama log check
journalctl -u ollama -f

# Docker Logs
docker logs ollama-container

# Download GitHub Actions Logs
gh run download <run-id>
```

### 2. Direct API Testing

```bash
# Ollama API Direct Call
curl -X POST http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "model": "exaone3.5:7.8b",
    "prompt": "Hello The text provided is already in English, so there is no need for translation. If you have any other text to translate, please provide it. Translate this Korean text to English. Respond with only the English translation, without commentary, notes, or explanations:

The study aimed to investigate the impact of social media on mental health among adolescents. The sample consisted of 300 participants aged between 13 and 18 years. Data were collected through online surveys and analyzed using statistical software. The results indicated a significant correlation between social media usage and mental health issues among adolescents. Recommendations were made for parents and educators to monitor and guide adolescents' social media use.",
    "stream": false
  }'
```

### 3. Network Diagnostics

```bash
# Network Connection Test
telnet localhost 11434

# DNS Resolution Check
nslookup ollama.com
```

## Requesting Support

If the issue is not resolved:

1. **Create an Issue Template**:
   - Operating system and version
   - Ollama version
   - Used model
   - Error message
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

## Smart Chunking & Debugging Issues

### 8. Large Document Processing Issues

#### Symptoms
```
❌ Context length exceeded
❌ Chunk Too Great Generated
❌ Translation:

I am EXAONE 3.5 from LG AI Research, a helpful Korean-English translator. In the middle Break
```

#### Solutions

1. **Adjust Context Length**:
   ```yaml
   context-length: 4096    # Set lower than default 32768
   ```

2. **Debug Mode for Chunking Analysis**:
   ```yaml
   debug-mode: true
   ```
   
   Created files:
   - `debug_chunks/`: Analysis of each chunk
   - `debug_originals/`: Original chunks
   - `debug_translations/`: Translated chunks

3. **Check Console Output**:
   ```bash
   📦 Created 15 token-aware chunks:
      Chunk 1: 1,156 tokens (2,845 chars)  # Check token count
   ```

### 9. Code Block Corruption Issue

#### Symptoms
```markdown
# Original text not provided. Please provide the Korean text you would like translated.
```python
def hello():
    print("world")
```

# Translation Result (Incorrect)
```python
def hello():
```
print("world")
```

#### Solution

1. **Check debug comparison files**:
   ```bash
   debug_comparisons/filename_comparison_001.md
   ```

2. **Section-based checking**:
   - Code Block Chunk In the middle Unsplit It seems like there might be a typo or incomplete input. Here is the translation of the provided text:

"Isn't it?"

If you have more text to translate, please provide it. Confirmation
   - H1-H3 Heading Based on Chunk Correctly Separate Confirmation

3. **Enhancing Translation Prompts**:
   Currently The system is Already Code Block Preservation Logic Included It is present.:
   ```
   - IMPORTANT: Do NOT add **bold**, *italic*, or any formatting that wasn't in the original text
   - Only translate text content, never modify or add markdown formatting
   ```

### 10. Translation Quality Discrepancy Issue

#### Symptoms
```
❌ Same terms translated differently
❌ Style varies across chunks
❌ Numbers disappear in numbered lists
```

#### Solutions

1. **Adjust Temperature**:
   ```yaml
   temperature: 0.1        # For more consistent translation (default: 0.3)
   ```

2. **Increase Retry Count**:
   ```yaml
   max-retries: 5         # Default: 3
   ```

3. **Analyze Translation Comparisons**:
   ```bash
   # Compare original and translated
   debug_comparisons/filename_comparison_001.md
   ```

4. **Check Numbered List Preservation**:
   The system is designed to preserve the following pattern:
   ```markdown
   # Original
   - 288. Cache Invalidation Scenario
   
   # Translation Result
   - 288. Cache Invalidation Scenario
   ```

### 11. How to Use Debug Files

#### Understanding the Debug File Structure

1. **Chunking Analysis** (`debug_chunks/`):
   ```markdown
   <!-- DEBUG CHUNK 1/15 -->
   <!-- Tokens: 1,156 -->
   <!-- Characters: 2,845 -->
   <!-- Source: docs/api-guide.md -->
   ```

2. **Translation Performance Summary**:
   ```bash
   📊 Translation Performance Summary:
      ⏱️  Total time: 2m 34s
      📄 Files processed: 12
      🔄 Total chunks: 67
      📈 Average chunk size: 1,089 tokens
   ```

3. **Identifying Problem Patterns**:
   - Repeated errors in specific chunks
   - Decreased quality in certain token ranges
   - Formatting issues in specific markdown patterns

#### Optimization Tips

1. **Optimal Chunk Size**:
   - 1,000-1,500 tokens: Balanced quality and speed
   - 500-800 tokens: High quality, slower speed
   - 2,000+ tokens: Fast speed, potential quality drop

2. **Utilizing Section-Based Splitting**:
   - H1-H2: Always split boundaries
   - H3: Split if over 200 tokens
   - Code blocks: Never split

## Frequently Asked Questions (FAQ)

### Q: How can I speed up the translation?
A: Use a GPU, opt for a smaller model, or run it on a Self-hosted runner.

### Q: How do I keep certain terms untranslated?
A: Add instructions in the prompt, such as "Keep technical terms in the original text."

### Q: Can I translate into multiple languages simultaneously?
A: Currently, only Korean-English is supported, but you can process multiple languages sequentially using a matrix strategy.

### Q: Does it work with private repositories?
A: Yes, you can use a Personal Access Token to access private repositories.

---

> **⚠️ 이 문서는 AI로 번역된 문서입니다.**
>
> **⚠️ This document has been translated by AI.**