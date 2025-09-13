# Ollama Document Translator

This project provides a GitHub Actions workflow for automatically translating Korean documents into English using a local Ollama API.

## Key Features

- **Automatic Translation**: Automatically translates Korean markdown documents in the `docs/` folder to English in the `docs-en/` folder
- **AI Model**: High-quality translation using the Exaone3.5:7.8b model
- **Workflow Automation**: Fully automated translation process using GitHub Actions
- **PR Auto Creation**: Automatically creates a Pull Request upon completion of translation

## Usage Instructions

1. Add Korean markdown documents to the `docs/` folder
2. Commit to GitHub to trigger the automated translation workflow
3. Upon completion, English versions will be generated in the `docs-en/` folder
4. Review and merge the automatically generated PR

## Setup Requirements

- Exaone3.5:7.8b model must be installed on your local Ollama server
- GitHub Actions must have access to the Ollama API

## Supported File Formats

- Markdown files (`.md`)
- Technical documents written in Korean
- API documentation and user guides

---

> **⚠️ 이 문서는 AI로 번역된 문서입니다.**
>
> **⚠️ This document has been translated by AI.**