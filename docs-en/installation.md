# Installation Guide

This document provides a detailed guide on how to install and set up the Ollama document translator.

## System Requirements

### Minimum Requirements
- **Operating System**: Windows 10/11, macOS 10.14+, Ubuntu 18.04+
- **Memory**: 8GB RAM (Recommended: 16GB or more)
- **Storage**: At least 10GB of free space
- **Network**: Internet connection (required for downloading earlier models)

### Recommended Specifications
- **CPU**: Multi-core processor (Intel i5 or above, or AMD Ryzen 5 or above)
- **Memory**: 16GB RAM or more
- **GPU**: NVIDIA GPU with CUDA support (optional, but it can help improve performance)

## Ollama Installation

### Installation on Windows

1. **Using the Windows Package Manager:**
   ```powershell
   winget install Ollama.Ollama
   ```

2. **Manual Installation:**
   - Download the Windows installation file from [Ollama’s official website](https://ollama.com/download).
   - Run the downloaded file to proceed with the installation.
   - Reboot the system after installation is complete.

### Installation on macOS

1. **Using Homebrew (recommended):**
   ```bash
   brew install ollama
   ```

2. **Manual Installation:**
   - Download the macOS installation file from [Ollama’s official website](https://ollama.com/download).
   - Open the DMG file and drag it into the Applications folder.

### Installation on Linux

1. **Automatic Installation Script (recommended):**
   ```bash
   curl -fsSL https://ollama.com/install.sh | sh
   ```

2. **Manual Installation:**
   ```bash
   # Installation using Docker:
   docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
   ```

## Model Installation

### Downloading the Exaone3.5 Model

Once Ollama is installed, you need to download the model to be used for translation:

```bash
# Download the default model
ollama pull exaone3.5:7.8b

# If a larger model is required:
ollama pull exaone3.5:32b
```

### Other Translation Models

If you want to compare the quality of translation, you can also try other models:

```bash
# Other recommended models:
ollama pull llama3.1:8b
ollama pull mistral:7b
ollama pull codellama:7b
```

## Verification of Settings

### Starting the Ollama Server

```bash
# Running the Ollama server in the background
ollama serve
```

### Verification of Installation

1. **Checking the server status**:
   ```bash
   curl http://localhost:11434/api/tags
   ```

2. **Checking the list of models**:
   ```bash
   ollama list
   ```

3. **A simple translation test**:
   ```bash
   ollama run exaone3.5:7.8b "Please translate '안녕하세요' into English"
   ```

## Environment Settings

### Setting Environment Variables

Depending on your system, you can set the following environment variables:

**Windows (PowerShell):**
```powershell
$env:OLLAMA_HOST = "0.0.0.0:11434"
$env:OLLAMA_MODELS = "C:\Users\[username]\.ollama\models"
```

**macOS/Linux (Bash):**
```bash
export OLLAMA_HOST=0.0.0.0:11434
export OLLAMA_MODELS=~/.ollama/models
```

### Firewall Settings

Ollama uses port 11434 by default. If you need to access it from the network, add the following firewall rules:

**Linux (ufw):**
```bash
sudo ufw allow 11434
```

**Windows (PowerShell - with administrator privileges):**
```powershell
New-NetFirewallRule -DisplayName "Ollama" -Direction Inbound -Port 11434 -Protocol TCP -Action Allow
```

## GitHub Actions Setup

### Setting Up a Self-hosted Runner

If you wish to use a local Ollama server, it is recommended to set up a self-hosted runner:

1. Go to **GitHub Repository** → **Settings** → **Actions** → **Runners**.
2. Click on **New self-hosted runner**.
3. Follow the guidelines appropriate for your operating system to complete the setup.
4. Ensure that Ollama is running before starting the runner.

### Setting Up Repository Secrets

Set up the secrets that will be used in GitHub Actions:

1. Go to **GitHub Repository** → **Settings** → **Secrets and variables** → **Actions**.
2. Add the necessary secrets:
   - `OLLAMA_URL`: The URL of your Ollama server (default value: http://localhost:11434).
   - `GITHUB_TOKEN`: This will be provided automatically.

## Performance Optimization

### GPU Usage Settings

If you have a NVIDIA GPU, you can enable CUDA:

```bash
# Check for CUDA support
nvidia-smi

# Enable GPU usage
export OLLAMA_GPU=1
```

### Memory Optimization

When using large models, you can optimize memory usage:

```bash
# Set model loading options
export OLLAMA_NUM_PARALLEL=2
export OLLAMA_MAX_LOADED_MODELS=1
```

## Problem Solving

Solutions to common installation problems:

### Port Conflict
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
# Set proxy (if necessary)
export HTTP_PROXY=http://proxy.company.com:8080
export HTTPS_PROXY=http://proxy.company.com:8080
ollama pull exaone3.5:7.8b
```

## Next Steps

Once the installation is complete, please refer to the following documents:

- [Configuration Guide](configuration.md) – Detailed configuration options
- [API Guide](api-guide.md) – How to use the API
- [Troubleshooting Guide](troubleshooting.md) – Solutions to common problems

If you encounter any issues during installation, please contact us via [GitHub Issues](https://github.com/your-username/ollama-doc-translator/issues).

---

> **⚠️ 이 문서는 AI로 번역된 문서입니다.**
>
> **⚠️ This document has been translated by AI.**