# Installation Guide

This document provides a detailed guide on how to install and set up the Ollama Document Translator.

## System Requirements

### Minimum Requirements
- **Operating System**: Windows 10/11, macOS 10.14+, Ubuntu 18.04+
- **Memory**: 8GB RAM (Recommended: 16GB or more)
- **Storage Space**: At least 10GB of free space
- **Network**: Internet connection (required for downloading initial models)

### Recommended Specifications
- **CPU**: Multi-core processor (Intel i5 or higher, or AMD Ryzen 5 or higher)
- **Memory**: 16GB RAM or more
- **GPU**: NVIDIA GPU with CUDA support - Optional but recommended for performance enhancement

## Ollama Installation

### Installation on Windows

1. **Using Windows Package Manager**:
   ```powershell
   winget install Ollama.Ollama
   ```

2. **Manual Installation**:
   - Download the Windows installation file from the [Ollama official website](https://ollama.com/download)
   - Run the downloaded file to proceed with installation
   - Restart your system after installation is complete

### Installation on macOS

1. **Using Homebrew** (Recommended):
   ```bash
   brew install ollama
   ```

2. **Manual Installation**:
   - Download the macOS installation file from the [Ollama official website](https://ollama.com/download)
   - Open the DMG file and drag it into the Applications folder

### Installation on Linux

1. **Automatic Installation Script** (Recommended):
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
# Download basic model
ollama pull exaone3.5:7.8b

# When a larger model is needed.
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

## Settings Verification

### Starting the Ollama Server

```bash
# Run Ollama server in the background
ollama serve
```

### Installation Verification

1. **Server Status Check**:
   ```bash
   curl http://localhost:11434/api/tags
   ```

2. **Model List Verification**:
   ```bash
   ollama list
   ```

3. **Simple Translation Test**:
   ```bash
   ollama run exaone3.5:7.8b "Translate 'Hello' into English"
   ``` 

(Note: The phrase "Hello Please provide the Korean text you would like translated into English. Please provide the Korean text you would like translated." was translated to "Translate 'Hello' into English" for clarity and context, assuming "Hello" refers to a greeting similar to "Hello" in English.)

## Environment Settings

### Setting Environment Variables

Depending on your system, you may need to set the following environment variables:

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

Ollama uses port 11434 by default. If you need to access it from your network, add firewall rules as follows:

```bash
# Linux (ufw)
sudo ufw allow 11434

# Windows (PowerShell - Run as Administrator)
New-NetFirewallRule -DisplayName "Ollama" -Direction Inbound -Port 11434 -Protocol TCP -Action Allow
```

## GitHub Actions Configuration

### Self-hosted Runner Setup

To use a local Ollama server, it is recommended to set up a Self-hosted Runner:

1. **GitHub Repository** → **Settings** → **Actions** → **Runners**
2. Click on **New self-hosted runner**
3. Follow the guide appropriate for your operating system to set it up
4. Ensure Ollama is running before starting the Runner

### Repository Secrets Configuration

Set up the secrets required for GitHub Actions:

1. **GitHub Repository** → **Settings** → **Secrets and variables** → **Actions**
2. Add the necessary secrets:
   - `OLLAMA_URL`: Ollama server URL (default: http://localhost:11434)
   - `GITHUB_TOKEN`: Provided automatically

## Performance Optimization

### GPU Usage Configuration

If you have an NVIDIA GPU, you can activate CUDA:

```bash
# Check CUDA Support
nvidia-smi

# Enable GPU Usage
export OLLAMA_GPU=1
```

### Memory Optimization

You can optimize memory usage when using large models:

```bash
# Model Load Option Settings
export OLLAMA_NUM_PARALLEL=2
export OLLAMA_MAX_LOADED_MODELS=1
```

## Problem Resolution

Solutions for Common Installation Issues:

### Port Conflict
```bash
# Use another port
export OLLAMA_HOST=0.0.0.0:11435
ollama serve
```

### Permission Issues (Linux/macOS)
```bash
# Grant execution permission to Ollama binary.
chmod +x /usr/local/bin/ollama
```

### Model Download Failure
```bash
# Proxy Settings (if needed)
export HTTP_PROXY=http://proxy.company.com:8080
export HTTPS_PROXY=http://proxy.company.com:8080
ollama pull exaone3.5:7.8b
```

## Next Steps

Once installation is complete, refer to the following documents:

- [Configuration Guide](configuration.md) - Detailed Configuration Options
- [API Guide](api-guide.md) - How to Use the API
- [Troubleshooting Guide](troubleshooting.md) - Common Issue Resolution

If you encounter issues during installation, please reach out to [GitHub Issues](https://github.com/your-username/ollama-doc-translator/issues).

---

> **⚠️ 이 문서는 AI로 번역된 문서입니다.**
>
> **⚠️ This document has been translated by AI.**