# API Guide

## Overview

This document serves as a guide on how to perform text translation using the Ollama API.

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

Download the exaone3.5:7.8b model for translation:

```bash
ollama pull exaone3.5:7.8b
```

## Using the API

### Basic Request

```bash
curl -X POST http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "model": "exaone3.5:7.8b",
    "prompt": "Next The text provided is already in English, so there is no need for translation. If you have any other text to translate, please let me know! The text provided is in Korean. Here is the translation into English:

"The text provided is in Korean. Here is the translation into English:" 

Since the actual text was not provided in your request, this is a placeholder response indicating that the text is in Korean and awaiting translation. Please provide the text you would like translated. The text provided is already in English. Therefore, no translation is needed. Please provide the Korean text you would like translated.: Hello",
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

1. **Provide Context**: Include the context of the text to be translated
2. **Handle Technical Terms**: Provide separate definitions for technical terms
3. **Maintain Consistency**: Use the same translation for the same term consistently

## Notes

- Only works in a local environment
- No internet connection required
- Sufficient memory required based on model size

---

> **⚠️ 이 문서는 AI로 번역된 문서입니다.**
>
> **⚠️ This document has been translated by AI.**