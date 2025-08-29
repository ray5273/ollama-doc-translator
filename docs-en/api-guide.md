# API Guide

## Overview

This document is a guide on how to perform text translation using the Ollama API.

## Basic Settings

1. Install Ollama

First, you need to install Ollama on the system:

```bash
 # Windows
 winget install Ollama.Ollama
 ```

# macOS
brew install ollama

```
# Linux
curl -fsSL https://ollama.com/install.sh | sh
```

2. Model download

Downloading the ExaOne 3.5:7.8b model for use in translation:

`docker pull exaone3.5:7.8b`

## API Usage

English Translation:

### Basic Request

```bash
 curl -X POST http://localhost:11434/api/generate \
   -H "Content-Type: application/json" \
   -d '{
       "model": "exaone3.5:7.8b",
       "prompt": "Please translate the following Korean text to English:안녕하세요",
       "stream": false
     }'

Answer format:

```json
 {
  "model": "exaone3.5:7.8b",
  "created_at": "2023-08-04T08:52:19.385406455-07:00",
  "response": "Hello",
  "done": true
}
```

## Tips for Improving Translation Quality

1. **Provide context**: Supply the context for the text to be translated
2. **Handle technical terms**: Define specialized terminologies separately
3. **Maintain consistency**: Always use the same translation for identical terms

## Cautions

English translation:
- Operates only in a local environment
- Does not require an internet connection
- Requires sufficient memory depending on model size