# Installation Guide

This document provides a detailed guide on how to install and set up Ollama Document Translator.

## System Requirements

### Minimum Requirements
- **Operating System**: Windows 10/11, macOS 10.14+, Ubuntu 18.04+
- **Memory**: 8GB RAM (Recommended: 16GB or more)
- **Storage Space**: At least 10GB of free space
- **Network**: Internet connection (for initial model download)

### Recommended Specifications
- **CPU**: Multi-core processor (Intel i5 or better, AMD Ryzen 5 or better)
- **Memory**: 16GB RAM or more
- **GPU**: NVIDIA GPU with CUDA support (Optional but recommended for performance)

## Ollama Installation

### Installation on Windows

1. **Using Windows Package Manager**:
   ```powershell
   winget install Ollama.Ollama
   ```

2. **Manual Installation**:
   - Download the Windows installation file from the [Ollama Official Website](https://ollama.com/download)
   - Run the downloaded file to proceed with installation
   - Restart your system after installation completes

### Installation on macOS

1. **Using Homebrew (Recommended)**:
   ```bash
   brew install ollama
   ```

2. **Manual Installation**:
   - Download the macOS installation file from the [Ollama Official Website](https://ollama.com/download)
   - Drag the DMG file into your Applications folder

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
# Download the base model
ollama pull exaone3.5:7.8b

# For larger models if needed
ollama pull exaone3.5:32b
```

### Other Translation Models

Try other models for comparative translation quality:

```bash
# Recommended alternative models
ollama pull llama3.1:8b
ollama pull mistral:7b
ollama pull codellama:7b
```

## Verification Setup

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

2. **List Models**:
   ```bash
   ollama list
   ```

3. **Simple Translation Test**:
   ```bash
   ollama run exaone3.5:7.8b "안녕하세요를 영어로 번역해주세요"
   ```

## Environment Configuration

### Setting Environment Variables

You may need to set the following environment variables depending on your system:

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

If Ollama needs network access, configure firewall rules:

```bash
# Linux (ufw)
sudo ufw allow 11434

# Windows (PowerShell - Administrator privileges)
New-NetFirewallRule -DisplayName "Ollama" -Direction Inbound -Port 11434 -Protocol TCP -Action Allow
```

## GitHub Actions Setup

### Self-hosted Runner Configuration

For local Ollama server use, configure a Self-hosted Runner:

1. Go to **GitHub Repository** → **Settings** → **Actions** → **Runners**
2. Click **New self-hosted runner**
3. Follow the setup guide for your OS
4. Ensure Ollama is running before starting the Runner

### Repository Secrets Configuration

Set secrets required for GitHub Actions:

1. Go to **GitHub Repository** → **Settings** → **Secrets and variables** → **Actions**
2. Add necessary secrets:
   - `OLLAMA_URL`: Ollama server URL (default: http://localhost:11434)
   - `GITHUB_TOKEN`: Provided automatically

## Performance Optimization

### Enabling GPU Usage

If you have an NVIDIA GPU with CUDA support:

```bash
# Check CUDA availability
nvidia-smi

# Enable GPU usage
export OLLAMA_GPU=1
```

### Memory Optimization

Optimize memory usage when using larger models:

```bash
# Configure model loading options
export OLLAMA_NUM_PARALLEL=2
export OLLAMA_MAX_LOADED_MODELS=1
```

## Troubleshooting

### Common Installation Issues

#### Port Conflicts
```bash
# Use a different port
export OLLAMA_HOST=0.0.0.0:11435
ollama serve
```

#### Permission Issues (Linux/macOS)
```bash
# Grant execution permissions to the Ollama binary
chmod +x /usr/local/bin/ollama
```

#### Model Download Failures
```bash
# Configure proxy settings if needed
export HTTP_PROXY=http://proxy.company.com:8080
export HTTPS_PROXY=http://proxy.company.com:8080
ollama pull exaone3.5:7.8b
```

## Next Steps

After installation, refer to the following documents:

- [Configuration Guide](configuration.md) - Detailed configuration options
- [API Guide](api-guide.md) - API usage instructions
- [Troubleshooting Guide](troubleshooting.md) - Common issue resolution

For installation issues, please reach out via [GitHub Issues](https://github.com/your-username/ollama-doc-translator/issues).