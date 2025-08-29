# Installation Guide

This document provides a detailed guide on how to install and set up the Ollama document translator.

## System Requirements

Minimum Requirements:
- **Operating System:** Windows 10/11, macOS 10.14+, Ubuntu 18.04+
- **Memory:** 8GB RAM (Recommended: 16GB or higher)
- **Storage Space:** More than 10GB of free space
- **Network:** Internet connection (for initial model download)

Recommended Specifications
- **CPU:** Multi-core processor (Intel i5 or higher, or AMD Ryzen 5 or higher)
- **Memory:** 16GB RAM or higher
- **GPU:** NVIDIA GPU (with CUDA support) - optional but helps improve performance

## Installing Ollama

On Windows Installation

1. **Using the Windows package manager:**
   ```powershell
   winget install Ollama.Ollama
   ```

2. **Manual installation:**
   - Download the Windows installer file from the [Ollama official website](https://ollama.com/download)
   - Run the downloaded file to proceed with the installation
   - Restart your system after the installation is complete

On macOS, install: (Note: The English translation is not a complete sentence as it seems to be part of a list or guide)

1. **Use Homebrew** (Recommended):
   ```bash
   brew install ollama
   ```

2. **Manual installation:**
   - Download the macOS install file from the [Ollama official website](https://ollama.com/download)
   - Open the DMG file and drag it to the Applications folder

On Linux, to install:

1. **Automated Installation Script** (Recommended):
   ```bash
   curl -fsSL https://ollama.com/install.sh | sh
   ```

2. **Manual installation:**
  ```bash
  # Installation using Docker
  docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
  ```

## Model Installation

Download Exaone3.5 model

After installing Ollama, you need to download the model to be used for translation:

```bash
 # Download basic model
 ollama pull exaone3.5:7.8b
```

# In cases where a larger model is needed
ollama_pull_exaone3.5:32b
```

Other translation models.

If you want to compare translation quality, you can also try out other models:

```bash
 # Other recommended models
 olm-api-python-client pull llama3.1:8b
 olm-api-python-client pull mistral:7b
 olm-api-python-client pull codellemas:7b
```

Note: The original Korean text provided was actually in Markdown format, not Korean language. In this case, I have preserved the structure and formatting while translating the comments to English based on their context.

## Configuration Check

Launching Ollama server

```bash
 # Run the Ollama server in the background
 ollama serve
 ```

Checking installation

1. **Check server status:**
   ```bash
   curl http://localhost:11434/api/tags
   ```

2. **List models:**
   ```bash
   ollama list
   ```

3. **Simple Translation Test:**
```bash
ollama run exaone3.5:7.8b "Please translate '안녕하세요' to English."
```

## Environment Setup

Environment Variable Setup

The following environment variables can be set according to the system:

**Windows (PowerShell)**:
```powershell
$ENV:OLLAMA_HOST = "0.0.0.0:11434"
$ENV:OLLAMA_MODELS = "C:\Users\[username]\.ollama\models"
```

**macOS/Linux (Bash)**:
```bash
export OLLAMA_HOST=0.0.0.0:11434
export OLLAMA_MODELS=$HOME/.ollama/models
```

Firewall setup

Ollama by default uses port 11434. If access is required from the network, add firewall rules:

```bash
 # Linux (ufw)
 sudo ufw allow 11434
```

```powershell
# Windows (PowerShell - Administrator permissions)
New-NetFirewallRule -DisplayName "Ollama" -Direction Inbound -Port 11434 -Protocol TCP -Action Allow
```

## Setting up GitHub Actions

Self-hosted Runner setup

To use a local Ollama server, it is recommended to set up a Self-hosted Runner:

1. Navigate to your **GitHub Repository** → **Settings** → **Actions** → **Runners**
2. Click on **New self-hosted runner**
3. Follow the guide for your operating system to set it up
4. Before starting the Runner, ensure that Ollama is running.

Repository Secrets Setup

Set up the secret to be used in GitHub Actions:

1. **Go to GitHub Repository** → **Settings** → **Secrets and variables** → **Actions**
2. Add required secrets:
   - `OLLAMA_URL`: Ollama server URL (default: http://localhost:11434)
   - `GITHUB_TOKEN`: provided automatically

## Performance Optimization

English Translation:

### GPU usage settings

In cases where an NVIDIA GPU is present, you can enable CUDA.

```bash
# Checking for CUDA support
nvidia-smi
```

```python
# Enable GPU usage
export OLLAMA_GPU=1
```

Memo: Memory optimization

When using large models, you can optimize memory usage:

```bash
 # Set model load options
 export OLLAMA_NUM_PARALLEL=2
 export OLLAMA_MAX_LOADED_MODELS=1
 ```

## Resolving Issues

Solution for common installation issues:

Port conflict
```bash
# Another port in use
export OLLAMA_HOST=0.0.0.0:11435
ollama serve
```

Permission issue (LinUX/macOS)
```bash
# Grant execution permissions to Ollama binary
chmod +x /usr/local/bin/ollama
```

```bash
# Proxy setup (if necessary)
export HTTP_PROXY=http://proxy.company.com:8080
export HTTPS_PROXY=http://proxy.company.com:8080
ollama pull exaone3.5:7.8b
```

## Next Step

Once the installation is complete, refer to the following documents:

English translation:
- [Configuration guide](configuration.md) - Detailed configuration options
- [API guide](api-guide.md) - Guide on using the API
- [Troubleshooting guide](troubleshooting.md) - Resolving common issues

If you encounter issues during installation, please reach out on [GitHub Issues](https://github.com/your-username/ollama-doc-translator/issues).