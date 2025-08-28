# API Guide

## Overview

This document serves as a guide on how to perform text translation using the Ollama API.

## Basic Settings

### 1. Installing Ollama

First, install Ollama on the system:

```bash
# Windows
winget install Ollama.Ollama
```

# macOS
```bash
brew install ollama
```

# Linux
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### 2. Model Download

Download the exaone3.5:7.8b model for translation:

```bash
git pull origin exaone3.5:7.8b
```

## How to Use the API

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

## Tips for Improving Translation Quality

Please provide the Korean text you would like translated while adhering to the guidelines regarding context, specialized terminology handling, and consistency. Here is a template based on your request:

**Korean Text:**
[Insert Korean Text Here]

**English Translation:**
[Insert Translated Text Here]

If you provide the specific text, I can apply this structure directly to your content.

## Important Notes

```
- Operates only in local environments
- Does not require internet connection
- Requires sufficient memory depending on model size
```