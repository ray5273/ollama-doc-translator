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
    "prompt": "Translate the following Korean text to English: 안녕하세요",
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

1. **Provide Context**: Offer context for the text being translated.
2. **Handle Specialized Terms**: Provide separate definitions for technical terms.
3. **Maintain Consistency**: Use consistent translations for identical terms.

## Important Notes

- Operates only in local environments.
- No internet connection required.
- Sufficient memory required based on model size.