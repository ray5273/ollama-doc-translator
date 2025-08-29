# API Guide

## Overview

This document is a guide on how to perform text translation using the Ollama API.

## Basic Settings

### 1. Ollama Installation

First, you need to install Ollama on your system:

```bash
# Windows
winget install Ollama.Ollama
```

# macOS
brew install ollama

# Linux
curl -fsSL https://ollama.com/install.sh | sh

### 2. Model Download

Download the exaone3.5:7.8b model to be used for translation:

```bash
ollama pull exaone3.5:7.8b
```

## API Usage

### Basic Request

```bash
curl -X POST http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "model": "exaone3.5:7.8b",
    "prompt": "Translate the following Korean text into English: 안녕하세요",
    "stream": false
  }'
```

### Response Format

```json
{
  "model": "exaone3.5:7.8b",
  "created_at": "2023-08-04T08:52:19.385406455-07:00",
  "response": "Hello",
  "done": true
}
```

## Improving Translation Quality

1. **Providing Context**: Provide the context of the text to be translated along with it.
2. **Handling Technical Terms**: Provide separate definitions for technical terms.
3. **Maintaining Consistency**: Always use the same translation for the same terms.

## 주의사항

## Precautions

- Operates only in a local environment
- Does not require an internet connection
- Requires sufficient memory depending on the model size