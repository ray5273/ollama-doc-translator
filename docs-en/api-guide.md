# API Guide

## Overview

This document is a guide on how to use the Ollama API for text translation.

## Basic Setup

### 1. Install Ollama

First, you need to install Ollama on your system:

```bash
# Windows
winget install Ollama.Ollama

# macOS
brew install ollama

# Linux
curl -fsSL https://ollama.com/install.sh | sh
```

### 2. Download the Model

Download the `exaone3.5:7.8b` model for translation:

```bash
ollama pull exaone3.5:7.8b
```

## How to Use the API

### Basic Request

```bash
curl -X POST http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "model": "exaone3.5:7.8b",
    "prompt": "Please translate the following Korean text into English: Hello",
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

## Tips for Improving Translation Quality

1. **Provide Context**: Provide the context of the text you want to translate.
2. **Handle Technical Terms**: Define technical terms separately.
3. **Maintain Consistency**: Use the same translation for identical terms.

## Notes

- It only works in a local environment.
- No internet connection is required.
- Sufficient memory is needed depending on the size of the model.

---

> **⚠️ 이 문서는 AI로 번역된 문서입니다.**
>
> **⚠️ This document has been translated by AI.**