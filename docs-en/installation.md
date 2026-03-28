# Installation Guide

This document provides a detailed guide on how to install and configure the Ollama document translator.

## System Requirements

### Minimum Requirements
- **Operating System**: Windows 10/11, macOS 10.14+, Ubuntu 18.04+
- **Memory**: 8GB RAM (Recommended: 16GB or more)
- **Storage**: 10GB of free space
- **Network**: Internet connection (for initial model download)

### Recommended Specifications
- **CPU**: Multi-core processor (Intel i5 or AMD Ryzen 5 or higher)
- **Memory**: 16GB RAM or more
- **GPU**: NVIDIA GPU (CUDA support) - Optional, but improves performance

## Installing Ollama

### Installing on Windows

1. **Using the Windows Package Manager**:
   ```powershell
   winget install Ollama.Ollama
   ```

2. **Manual Installation**:
   - Download the Windows installation file from [Ollama official website](https://ollama.com/download)
   - Run the downloaded file to proceed with the installation
   - Restart the system after installation

### Installing on macOS

1. **Using Homebrew** (Recommended):
   ```bash
   brew install ollama
   ```

2. **Manual Installation**:
   - Download the macOS installation file from [Ollama official website](https://ollama.com/download)
   - Open the DMG file and drag it to the Applications folder

### Installing on Linux

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

### Downloading the Exaone3.5 Model

Once Ollama is installed, you need to download the model to use for translation:

```bash
# Download the basic model
ollama pull exaone3.5:7.8b

# If a larger model is needed
ollama pull exaone3.5:32b
```

### Other Translation Models

If you want to compare translation quality, you can try other models as well:

```bash
# Other recommended models
ollama pull llama3.1:8b
ollama pull mistral:7b
ollama pull codellama:7b
```

## Verify Settings

### Start Ollama Server

```bash
# Run the Ollama server in the background.
ollama serve
```

### Verify Installation

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
   ollama run exaone3.5:7.8b "Translate Hello to English"
   ```

## Configuration

### Setting Environment Variables

You can set the following environment variables depending on your system:

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

### Firewall Settings

Ollama uses port 11434 by default. If you need to access it from the network, add a firewall rule:

```bash
# Linux (ufw)
sudo ufw allow 11434

# Windows (PowerShell - Administrator privileges)
New-NetFirewallRule -DisplayName "Ollama" -Direction Inbound -Port 11434 -Protocol TCP -Action Allow
```

## GitHub Actions Configuration

### Configuring Self-Hosted Runner

It is recommended to configure the Self-Hosted Runner to use a local Ollama server:

1. Go to **GitHub Repository** → **Settings** → **Actions** → **Runners**
2. Click **New self-hosted runner**
3. Follow the guide for your operating system to configure
4. Make sure Ollama is running before starting the Runner

### Configuring Repository Secrets

Configure the secrets to be used in GitHub Actions:

1. Go to **GitHub Repository** → **Settings** → **Secrets and variables** → **Actions**
2. Add the necessary secrets:
   - `OLLAMA_URL`: Ollama server URL (default: http://localhost:11434)
   - `GITHUB_TOKEN`: Automatically provided

## Performance Optimization

### GPU Usage Configuration

If you have an NVIDIA GPU, you can enable CUDA:

```bash
# CUDA support verification
nvidia-smi

# Enable GPU usage
export OLLAMA_GPU=1
```

### Memory Optimization

You can optimize memory usage when using large models:

```bash
# Setting model loading options
export OLLAMA_NUM_PARALLEL=2
export OLLAMA_MAX_LOADED_MODELS=1
```

## Troubleshooting

Solutions for common installation issues:

### Port Conflicts
```bash
# Use a different port.
export OLLAMA_HOST=0.0.0.0:11435
ollama serve
```

### Permission Issues (Linux/macOS)
```bash
# Grant execute permission to the Ollama binary.
chmod +x /usr/local/bin/ollama
```

### Model Download Failure
```bash
# Proxy settings (if necessary)
export HTTP_PROXY=http://proxy.company.com:8080
export HTTPS_PROXY=http://proxy.company.com:8080
ollama pull exaone3.5:7.8b
```

## Next Steps

After installation is complete, please refer to the following documents:

- [Configuration Guide](configuration.md) - Detailed configuration options
- [API Guide](api-guide.md) - API usage
- [Troubleshooting Guide](troubleshooting.md) - Common troubleshooting

If you encounter any issues during installation, please contact [GitHub Issues](https://github.com/your-username/ollama-doc-translator/issues).

---

> **⚠️ 이 문서는 AI로 번역된 문서입니다.**
>
> **⚠️ This document has been translated by AI.**