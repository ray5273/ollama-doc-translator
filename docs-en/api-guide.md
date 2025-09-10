# API Guide

## Overview

This document provides a guide on how to perform text translation using the Ollama API.

## Basic Setup

### 1. Ollama Installation

First, install Ollama on your system:

```bash
# Windows
winget install Ollama.Ollama

# macOS
brew install ollama

# Linux
curl -fsSL https://ollama.com/install.sh | sh
```

### 2. Model Download

Download the exaone3.5:7.8b model for translation:

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
    "prompt": "다음 한국어 텍스트를 영어로 번역해주세요: 안녕하세요",
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

1. **Provide Context**: Offer context along with the text to be translated
2. **Handle Technical Terms**: Provide separate definitions for technical jargon
3. **Maintain Consistency**: Use the same translation consistently for identical terms

## Important Notes

- Operates only in local environments
- No internet connection required
- Sufficient memory may be needed depending on model size

---

> **⚠️ 이 문서는 AI로 번역된 문서입니다.**
>
> **⚠️ This document has been translated by AI.**