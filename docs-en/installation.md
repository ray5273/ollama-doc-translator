# Installation Guide

This document provides a detailed guide on how to install and set up the Ollama document translator.

## System Requirements

### Minimum Requirements
- **Operating System**: Windows 10/11, macOS 10.14+, Ubuntu 18.04+
- **Memory**: 8GB RAM (recommended: 16GB or more)
- **Storage**: 10GB of free space
- **Network**: Internet connection (for initial model download)

### Recommended Specifications
- **CPU**: Multi-core processor (Intel i5 or higher or AMD Ryzen 5 or higher)
- **Memory**: 16GB RAM or more
- **GPU**: NVIDIA GPU with CUDA support - optional but helps improve performance

## Ollama Installation

### Installation on Windows

1. **Using Windows Package Manager**:
   ```powershell
   winget install Ollama.Ollama
   ```

2. **Manual Installation**:
   - Download the Windows installer from the [Ollama official website](https://ollama.com/download)
   - Run the downloaded file to start the installation
   - Restart your system after installation is complete

### Installation on macOS

1. **Using Homebrew** (recommended):
   ```bash
   brew install ollama
   ```

2. **Manual Installation**:
   - Download the macOS installer from the [Ollama official website](https://ollama.com/download)
   - Drag the DMG file to the Applications folder

### Installation on Linux

1. **Automatic Installation Script** (recommended):
   ```bash
   curl -fsSL https://ollama.com/install.sh | sh
   ```

2. **Manual Installation**:
   ```bash
   # Installation using Docker
   docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
   ```

## Model Installation

### Downloading the Exaone 3.5 Model

Once Ollama is installed, you need to download the model for translation:

```bash
# Downloading the base model
ollama pull exaone3.5:7.8b

# When a larger model is needed.
ollama pull exaone3.5:32b
```

### Other Translation Models

If you want to compare translation quality, you can try other models as well:

```bash
# Other Recommended Models
ollama pull llama3.1:8b
ollama pull mistral:7b
ollama pull codellama:7b
```

## Configuration Check

### Start Ollama Server

```bash
# Running Ollama Server in the Background
ollama serve
```

### Installation Verification

1. **Check Server Status**:
   ```bash
   curl http://localhost:11434/api/tags
   ```

2. **List Models**:
   ```bash
   ollama list
   ```

3. **Simple Translation Test**:
   ```bash
   ollama run exaone3.5:7.8b "Translate 'Hello' to English"
   ```

## Environment Setup

### Setting Environment Variables

Depending on your system, you can set the following environment variables:

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

Ollama uses port 11434 by default. If you need to access it from your network, add firewall rules:

```bash
# Linux (ufw)
sudo ufw allow 11434

# Windows (PowerShell - Administrator Privileges)
New-NetFirewallRule -DisplayName "Ollama" -Direction Inbound -Port 11434 -Protocol TCP -Action Allow
```

## GitHub Actions Configuration

### Setting Up Self-hosted Runner

To use a local Ollama server, it is recommended to set up a Self-hosted Runner:

1. Go to **GitHub Repository** → **Settings** → **Actions** → **Runners**
2. Click on **New self-hosted runner**
3. Follow the guide for your operating system to set it up
4. Ensure Ollama is running before starting the Runner

### Setting Repository Secrets

Set up the secrets to be used in GitHub Actions:

1. Go to **GitHub Repository** → **Settings** → **Secrets and variables** → **Actions**
2. Add the following secrets:
   - `OLLAMA_URL`: Ollama server URL (default: http://localhost:11434)
   - `GITHUB_TOKEN`: Automatically provided
[TRANSLATION_END]

## Performance Optimization

### GPU Configuration

If you have an NVIDIA GPU, you can enable CUDA:

```bash
# Checking CUDA Support
nvidia-smi

# GPU Usage Activation
export OLLAMA_GPU=1
```

### Memory Optimization

You can optimize memory usage when using large models:

```bash
# Model Load Options Configuration
export OLLAMA_NUM_PARALLEL=2
export OLLAMA_MAX_LOADED_MODELS=1
```

## Troubleshooting

Solutions for common installation issues:

### Port Conflict
```bash
# Using another port
export OLLAMA_HOST=0.0.0.0:11435
ollama serve
```

### Permission Issues (Linux/macOS)
```bash
# Grant execution permission to Ollama binary
chmod +x /usr/local/bin/ollama
```

### Model Download Failure
```bash
# Proxy Configuration (if needed)
export HTTP_PROXY=http://proxy.company.com:8080
export HTTPS_PROXY=http://proxy.company.com:8080
ollama pull exaone3.5:7.8b
```

## Next Steps

Once installation is complete, refer to the following documents:

- [Configuration Guide](configuration.md) - Detailed configuration options
- [API Guide](api-guide.md) - How to use the API
- [Troubleshooting Guide](troubleshooting.md) - Common issues and solutions

If you encounter any issues during installation, please reach out to [GitHub Issues](https://github.com/your-username/ollama-doc-translator/issues).

---

> **⚠️ 이 문서는 AI로 번역된 문서입니다.**
>
> **⚠️ This document has been translated by AI.**