# Installation Guide

This document provides a detailed guide on how to install and set up Ollama Document Translator.

## System Requirements

### Minimum Requirements
- **Operating System**: Windows 10/11, macOS 10.14+, Ubuntu 18.04+
- **Memory**: 8GB RAM (Recommended: 16GB or more)
- **Storage Space**: At least 10GB of free space
- **Network**: Internet connection (for initial model download)

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
   - Restart your system after installation completes

### Installation on macOS

1. **Using Homebrew** (Recommended):
   ```bash
   brew install ollama
   ```

2. **Manual Installation**:
   - Download the macOS installation file from the [Ollama official website](https://ollama.com/download)
   - Drag the DMG file into the Applications folder

### Installation on Linux

1. **Automatic Installation Script** (Recommended):
   ```bash
   curl -fsSL https://ollama.com/install.sh | sh
   ```

2. **Manual Installation**:
   ```bash
```

# Installation Using Docker
   ```bash
   docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
   ```

## Model Installation

### Downloading the Exaone 3.5 Model

After Ollama is installed, download the model for translation use:

```bash
```

# Download Basic Model
ollama pull exaone3.5:7.8b

# When a Larger Model is Needed
ollama pull exaone3.5:32b
```

### Other Translation Models

To compare translation quality, you can also try other models:

```bash

# Other Recommended Models
ollama pull llama3.1:8b
ollama pull mistral:7b
ollama pull codellama:7b

## Settings Confirmation

### Starting Ollama Server

```bash
```

# Running Ollama Server in Background
ollama serve

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
   ollama run exaone3.5:7.8b "Translate 'Hello' to English"
   ```

## Environment Settings

### Environment Variable Setup

Depending on your system, you may set the following environment variables:

**Windows (PowerShell)**:
```powershell
$env:OLLAMA_HOST = "0.0.0.0:11434"
$env:OLLAMA_MODELS = "C:\Users\[username]\.ollama\models"
```

**macOS/Linux (Bash)**:
```bash
export OLLAMA_HOST=0.0.04
export OLLAMA_MODELS=~/.ollama/models
``` 

### Firewall Settings

Ollama uses port 11434 by default. If you need network access, add firewall rules:

```bash```

# Linux (ufw)
sudo ufw allow 11434

# Windows (PowerShell - Administrator Privileges)
New-NetFirewallRule -DisplayName "Ollama" -Direction Inbound -Port 11434 -Protocol TCP -Action Allow

## GitHub Actions Configuration

### Self-hosted Runner Setup

To use a local Ollama server, it's recommended to set up a Self-hosted Runner:

1. Go to **GitHub Repository** → **Settings** → **Actions** → **Runners**
2. Click on **New self-hosted runner**
3. Follow the guide appropriate for your operating system
4. Ensure Ollama is running before starting the Runner

### Repository Secrets Setup

Set up the secrets required for GitHub Actions:

1. Go to **GitHub Repository** → **Settings** → **Secrets and variables** → **Actions**
2. Add the necessary secrets:
   - `OLLAMA_URL`: Ollama server URL (default: http://localhost:11434)
   - `GITHUB_TOKEN`: Provided automatically

## Performance Optimization

### GPU Usage Configuration

If you have an NVIDIA GPU, you can activate CUDA:

```bash
```

# CUDA Support Verification
nvidia-smi

# Enable GPU Usage
```

## Memory Optimization

Optimize memory usage when using large models:

```bash```
```

# Model Loading Options Configuration
```bash
export OLLAMA_NUM_PARALLEL=2
export OLLAMA_MAX_LOADED_MODELS=1
```

## Problem Solving

Solutions for Common Installation Issues:

### Port Conflict
```bash
```

# Using a Different Port
```bash
export OLLAMA_HOST=0.0.0.0:11435
ollama serve
```

### Permission Issues (Linux/macOS)
```bash
```

# Grant Execution Permission to Ollama Binary
```bash
chmod +x /usr/local/bin/ollama
```

### Model Download Failure

# Proxy Settings (If Necessary)
```bash
export HTTP_PROXY=http://proxy.company.com:8080
export HTTPS_PROXY=http://proxy.company.com:8080
ollama pull exaone3.5:7.8b
```

## Next Steps

Once installation is complete, refer to the following documents:

- [Configuration Guide](configuration.md) - Detailed Configuration Options
- [API Guide](api-guide.md) - API Usage
- [Troubleshooting Guide](troubleshooting.md) - Common Issue Resolution

If you encounter issues during installation, please reach out to [GitHub Issues](https://github.com/your-username/ollama-doc-translator/issues).

---

> **⚠️ 이 문서는 AI로 번역된 문서입니다.**
>
> **⚠️ This document has been translated by AI.**