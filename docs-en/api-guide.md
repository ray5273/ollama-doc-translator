# API Guide

## Overview

This document provides a guide on how to perform text translation using the Ollama API.

## Basic Setup

### 1. Ollama Installation

First, you need to install Ollama on your system:

```bash
# Windows
winget install Ollama.Ollama

# macOS
brew install ollama

# Linux
curl -fsSL https://ollama.com/install.sh | sh
```

### 2. Downloading the Model

Download the exaone3.5:7.8b model to use for translation:

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
    "prompt": "Next Korean the text Please provide the Korean text you would like me to translate. Please translate.: Hello",
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

## Tips to Improve Translation Quality

1.  **Provide Context**: Provide the context of the text to be translated.
2.  **Handle Technical Terms**: Provide definitions for technical terms.
3.  **Maintain Consistency**: Use the same translation for the same terms.

## Important Notes

-   Only works in a local environment.
-   No internet connection is required.
-   Sufficient memory may be required depending on the model size.

---

> **⚠️ 이 문서는 AI로 번역된 문서입니다.**
>
> **⚠️ This document has been translated by AI.**