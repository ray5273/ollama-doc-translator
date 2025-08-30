# Installation Guide

This document provides detailed instructions on installing and setting up Ollama Document Translator.

## System Requirements

### Minimum Requirements
- **Operating System**: Windows 10/11, macOS 10.14+, Ubuntu 18.04+
- **Memory**: 8GB RAM (Recommended: 16GB or more)
- **Storage Space**: At least 10GB of free space
- **Network**: Internet connection (for initial model download)

### Recommended Specifications
- **CPU**: Multi-core processor (Intel i5 or better, or AMD Ryzen 5 or better)
- **Memory**: 16GB RAM or more
- **GPU**: NVIDIA GPU with CUDA support - Optional but enhances performance

## Ollama Installation

### Installation on Windows

1. **Using Windows Package Manager**:
   ```powershell
   winget install Ollama.Ollama
   ```

2. **Manual Installation**:
   - Download the Windows installation file from the [Ollama official website](https://ollama.com/download)
   - Run the downloaded file to proceed with installation
   - Restart the system after installation completion

### Installation on macOS

1. **Using Homebrew (Recommended)**:
   ```bash
   brew install ollama
   ```

2. **Manual Installation**:
   - Download the macOS installation file from the [Ollama official website](https://ollama.com/download)
   - Open the DMG file and drag the Applications folder into your Applications directory

### Installation on Linux

1. **Using Automatic Installation Script (Recommended)**:
   ```bash
   curl -fsSL https://ollama.com/install.sh | sh
   ```

2. **Manual Installation**:
   ```bash
   # Installation using Docker
   docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
   ```

## Model Installation

### Downloading the Exaone3.5 Model

After installing Ollama, download the model for translation:

```bash
# Downloading the base model
ollama pull exaone3.5:7.8b

# For larger models if needed
ollama pull exaone3.5:32b
```

### Other Translation Models

To compare translation quality, you can also try other models:

```bash
# Other recommended models
ollama pull llama3.1:8b
ollama pull mistral:7b
ollama pull codellama:7b
```

## Setup Verification

### Starting the Ollama Server

```bash
# Run Ollama server in the background
ollama serve
```

### Installation Verification

```markdown
1. **Server Status Check**:
   ```bash
   curl http://localhost:11434/api/tags
   ```

2. **Model List Check**:
   ```bash
   ollama list
   ```

3. **Simple Translation Test**:
   ```bash
   ollama run exaone3.5:7.8b "Hello, translate '안녕하세요' into English"
   ```

## Environment Setup

### Environment Variable Configuration

Depending on your system, you may need to set the following environment variables:

**Windows (PowerShell)**:
```powershell
$env:OLLAMA_HOST = "0.0.0.0:11434"
$env:OLLAMA_MODELS = "C:\Users\[username]\.ollama\models"
```

**macOS/Linux (Bash)**:
```bash
export OLLAMA_HOST=0.0.0.0:11434
export OLLAMA_MODELS=~/.ollama/models
```

### Firewall Configuration

Ollama uses port 11434 by default. If you need network access, add firewall rules:

```bash
# Linux (ufw)
sudo ufw allow 11434

# Windows (PowerShell - Administrator privileges)
New-NetFirewallRule -DisplayName "Ollama" -Direction Inbound -Port 11434 -Protocol TCP -Action Allow
```

## GitHub Actions Configuration

### Self-hosted Runner Setup

To use a local Ollama server, set up a Self-hosted Runner:

1. Navigate to **GitHub Repository** → **Settings** → **Actions** → **Runners**
2. Click **New self-hosted runner**
3. Follow the OS-specific setup guide
4. Ensure Ollama is running before starting the Runner

### Repository Secrets Configuration

Set up secrets for GitHub Actions usage:

1. Go to **GitHub Repository** → **Settings** → **Secrets and variables** → **Actions**
2. Add the following secrets:
   - `OLLAMA_URL`: Ollama server URL (default: http://localhost:11434)
   - `GITHUB_TOKEN`: Provided automatically

## Performance Optimization

### GPU Usage Configuration

If you have an NVIDIA GPU, enable CUDA:

```bash
# Check CUDA support
nvidia-smi

# Enable GPU usage
export OLLAMA_GPU=1
```

### Memory Optimization

Optimize memory usage when working with large models:
```markdown
```

```bash
# Configuration of Model Loading Options
export OLLAMA_NUM_PARALLEL=2
export OLLAMA_MAX_LOADED_MODELS=1
```

## Troubleshooting

### Port Conflicts
```bash
# Use a different port
export OLLAMA_HOST=0.0.0.0:11435
ollama serve
```

### Permission Issues (Linux/macOS)
```bash
# Grant execution permissions to the Ollama binary
chmod +x /usr/local/bin/ollama
```

### Model Download Failure
```bash
# Proxy configuration (if needed)
export HTTP_PROXY=http://proxy.company.com:8080
export HTTPS_PROXY=http://proxy.company.com:8080
ollama pull exaone3.5:7.8b
```

## Next Steps

Refer to the following documents once installation is complete:

- [Configuration Guide](configuration.md) - Detailed Configuration Options
- [API Guide](api-guide.md) - API Usage
- [Troubleshooting Guide](troubleshooting.md) - Common Issues Resolution

For installation issues, please reach out to [GitHub Issues](https://github.com/your-username/ollama-doc-translator/issues).