# Installation Guide

This document provides a detailed guide on how to install and set up the Ollama Document Translator.

## System Requirements

### Minimum Requirements
- **Operating System**: Windows 10/11, macOS 10.14+, Ubuntu 18.04+
- **Memory**: 8GB RAM (Recommended: 16GB or more)
- **Storage Space**: At least 10GB of free space
- **Network**: Internet connection (required for initial model download)

### Recommended Specifications
- **CPU**: Multi-core processor (Intel i5 or higher, or AMD Ryzen 5 or higher)
- **Memory**: 16GB RAM or more
- **GPU**: NVIDIA GPU (with CUDA support) - Optional but recommended for performance enhancement

## Installing Ollama

### Installation on Windows

1. **Using Windows Package Manager**:
   ```powershell
   winget install Ollama.Ollama
   ```

2. **Manual Installation**:
   - Download the Windows installer file from the [Ollama official website](https://ollama.com/download)
   - Run the downloaded file to proceed with installation
   - Restart your system after installation is complete

### Installation on macOS

```markdown
1. **Using Homebrew** (Recommended):
   ```bash
   brew install ollama
   ```
```

2. **Manual Installation**:
   - Download the macOS installer file from the [Ollama official website](https://ollama.com/download)
   - Drag the DMG file into the Applications folder after opening it

### Installation on Linux

```markdown
1. **Automatic Installation Script** (Recommended):
   ```bash
   curl -fsSL https://ollama.com/install.sh | sh
   ```

```markdown
2. **Manual Installation**:
   ```bash
   # Installation using Docker
   docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
   ```

## Model Installation

### Download Exaone 3.5 Model

After installing Ollama, you need to download the model for translation:

```bash
# Download Basic Model
ollama pull exaone3.5:7.8b
```

# When a Larger Model is Required
```
Pull ExaONE 3.5:32B via Ollama
```

### Other Translation Models

If you want to compare translation quality, you can also try other models:

```bash
# Other Recommended Models
ollama pull llama3.1:8b
ollama pull mistral:7b
ollama pull codellama:7b
```

## Verify Settings

### Starting the Ollama Server

```bash
# Run Ollama Server in the Background
ollama serve &
```

### Installation Verification

```markdown
1. **Check Server Status**:
   ```bash
   curl http://localhost:11434/api/tags
   ```

2. **Check Model List**:
   ```bash
   ollama list
   ```

```bash
ollama run exaone3.5:7.8b "Translate 'Hello' to English"
```

## Environment Setup

### Setting Environment Variables

```
Environment variables can be set as follows depending on the system:
```

**Windows (PowerShell)**:
```powershell
$env:OLLAMA_HOST = "0.0.0.0:11434"
$env:OLLAMA_MODELS = "C:\Users\[username]\.ollama\models"
``` 

(Note: The placeholder `[username]` should be replaced with the actual username when applying this script.)

**macOS/Linux (Bash)**:
```bash
export OLLAMA_HOST=0.0.0.0:11434
export OLLAMA_MODELS=~/.ollama/models
```

### Firewall Configuration

Ollama primarily uses port 11434. If you need to access it over the network, add firewall rules accordingly:

```bash
# Linux (ufw)
sudo ufw allow 11434
```

# Windows (PowerShell - Administrator Privileges)
```powershell
New-NetFirewallRule -DisplayName "Ollama" -Direction Inbound -Port 11434 -Protocol TCP -Action Allow
```

## GitHub Actions Configuration

### Self-hosted Runner Setup

To use a local Ollama server, setting up a Self-hosted Runner is recommended:

```markdown
1. **GitHub Repository** → **Settings** → **Actions** → **Runners**
2. Click on **New self-hosted runner**
3. Follow the guide appropriate for your operating system
4. Ensure Ollama is running before starting the Runner
```

### Setting Repository Secrets

Set up secrets to use with GitHub Actions:

```markdown
1. **GitHub Repository** → **Settings** → **Secrets and variables** → **Actions**
2. Add necessary secrets:
   - `OLLAMA_URL`: Ollama server URL (default: http://localhost:11434)
   - `GITHUB_TOKEN`: Provided automatically
```

## Performance Optimization

### GPU Usage Configuration

If you have an NVIDIA GPU, you can enable CUDA:

```bash
# Verify CUDA Support
nvidia-smi
```

# Enable GPU Usage
```bash
export OLLAMA_GPU=1
```

### Memory Optimization

Optimize memory usage when using large models:

```bash
# Configure Model Loading Options
export OLLAMA_NUM_PARALLEL=2
export OLLAMA_MAX_LOADED_MODELS=1
```

## Problem Solving

## Troubleshooting Common Installation Issues:

### Port Conflict
```bash
# Use a different port
export OLLAMA_HOST=0.0.0.0:11436
ollama serve
```

### Permission Issues (Linux/macOS)
```bash
# Grant execution permissions to the Ollama binary
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

```markdown
Refer to the following documents once installation is complete:
```

- [Configuration Guide](configuration.md) - Detailed Configuration Options
- [API Guide](api-guide.md) - How to Use the API
- [Troubleshooting Guide](troubleshooting.md) - Resolving Common Issues

If you encounter any issues during installation, please reach out via [GitHub Issues](https://github.com/your-username/ollama-doc-translator/issues).