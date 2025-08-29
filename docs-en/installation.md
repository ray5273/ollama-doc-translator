# Installation Guide

This document provides a detailed guide on installing and setting up the Ollama documentation translator.

## System Requirements

### Minimum Requirements
- **Operating System**: Windows 10/11, macOS 10.14+, Ubuntu 18.04+
- **Memory**: 8GB RAM (Recommended: 16GB or more)
- **Storage**: 10GB or more of free space
- **Network**: Internet connection (for initial model download)

### Recommended Specifications
- **CPU**: Multi-core processor (Intel i5 or higher, or AMD Ryzen 5 or higher)
- **Memory**: 16GB RAM or more
- **GPU**: NVIDIA GPU (CUDA support) - Optional, but helps improve performance

## Ollama Installation

### Installation on Windows

1. **Using the Windows Package Manager**:
   ```powershell
   winget install Ollama.Ollama
   ```

2. **Manual Installation**:
   - Download the Windows installer from the [Ollama official website](https://ollama.com/download)
   - Run the downloaded file to proceed with the installation
   - Restart your system after installation is complete

### Installation on macOS

1. **Homebrew 사용** (권장):
   ```bash
   brew install ollama
   ```

2. **Manual Installation**:
   - Download the macOS installer from the [Ollama official website](https://ollama.com/download)
   - Open the DMG file and drag it to the Applications folder

### Installation on Linux

1. **Automated Installation Script** (Recommended):
   ```bash
   curl -fsSL https://ollama.com/install.sh | sh
   ```

2. **Manual Installation**:
   ```bash
   # Installation using Docker
   docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
   ```

## Model Installation

### Exaone3.5 Model Download

Ollama가 설치되면 번역에 사용할 모델을 다운로드해야 합니다:

Once Ollama is installed, you need to download a model to use for translation:

```bash
# Download base model
ollama pull exaone3.5:7.8b
```

# When You Need a Larger Model
ollama pull exaone3.5:32b

### Other Translation Models

If you'd like to compare translation quality, you can try other models:

```bash
# Other Recommended Models
ollama pull llama3.1:8b
ollama pull mistral:7b
ollama pull codellama:7b
```

## Configuration Check

### Starting the Ollama Server

```bash
# Run Ollama server in the background
ollama serve
```

### Installation Verification

1. **Check Server Status**:
   ```bash
   curl http://localhost:11434/api/tags
   ```

2. **Check Model List**:
   ```bash
   ollama list
   ```

3. **Simple Translation Test**:
   ```bash
   ollama run exaone3.5:7.8b "Translate '안녕하세요' into English"
   ```

## Environment Setup

### Environment Variable Setup

Depending on the system, you may be able to set the following environment variables:

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

Ollama uses port 11434 by default. If you need to access it over the network, add a firewall rule:

```bash
# Linux (ufw)
sudo ufw allow 11434
```

# Windows (PowerShell - Administrator)
New-NetFirewallRule -DisplayName "Ollama" -Direction Inbound -Port 11434 -Protocol TCP -Action Allow

## GitHub Actions Setup

### Self-hosted Runner Setup

To use a local Ollama server, it's recommended to set up a Self-hosted Runner:

1. **GitHub Repository** → **Settings** → **Actions** → **Runners**
2. Click **New self-hosted runner**
3. Follow the guide for your operating system to set up
4. Ensure Ollama is running before starting the Runner

### Repository Secrets Configuration

Set up secrets for use with GitHub Actions:

1. **GitHub Repository** → **Settings** → **Secrets and variables** → **Actions**
2. Add required secrets:
   - `OLLAMA_URL`: Ollama server URL (default: http://localhost:11434)
   - `GITHUB_TOKEN`: Automatically provided

## Performance Optimization

### Enabling GPU

NVIDIA GPU가 있는 경우 CUDA를 활성화할 수 있습니다:

If you have an NVIDIA GPU, you can enable CUDA:

```bash
# Check CUDA Support
nvidia-smi
```

# Enable GPU Usage
export OLLAMA_GPU=1

### Memory Optimization

Large models can be optimized for memory usage:

```bash
# Set model loading options
export OLLAMA_NUM_PARALLEL=2
export OLLAMA_MAX_LOADED_MODELS=1
```

## Problem Solving

Common Installation Issue Solutions:

### Port Conflict
```bash
# Use a different port
export OLLAMA_HOST=0.0.0.0:11435
ollama serve
```

### Permissions Issues (Linux/macOS)
```bash
# Grant execute permissions to the Ollama binary
chmod +x /usr/local/bin/ollama
```

### Model Download Failed
```bash
# Proxy settings (if needed)
export HTTP_PROXY=http://proxy.company.com:8080
export HTTPS_PROXY=http://proxy.company.com:8080
ollama pull exaone3.5:7.8b
```

## Next Steps

Once installation is complete, refer to the following documents:

- [Configuration Guide](configuration.md) - Detailed configuration options
- [API Guide](api-guide.md) - API usage
- [Troubleshooting Guide](troubleshooting.md) - Common issue resolution

If you encounter any issues during installation, please refer to [GitHub Issues](https://github.com/your-username/ollama-doc-translator/issues).