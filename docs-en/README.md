# Ollama Document Translator

This project provides a GitHub Actions workflow to automatically translate Korean documents into English using a local Ollama API.

## Key Features

- **Automatic Translation**: Automatically translates Markdown documents in the `docs/` folder to the `docs-en/` folder
- **AI Model**: Uses the Exaone3.5:7.8b model for high-quality translations
- **Workflow Automation**: Fully automated translation process through GitHub Actions
- **PR Auto-Creation**: Automatically creates a Pull Request after translation is complete

## Usage

1. Add Korean Markdown documents to the `docs/` folder
2. Commit to GitHub and the automated translation workflow will run
3. Once translation is complete, an English version will be created in the `docs-en/` folder
4. Review and merge the automatically created PR

## Requirements

- The exaone3.5:7.8b model must be installed on the local Ollama server
- Access to the Ollama API must be configured in GitHub Actions

## Supported File Formats

- Markdown files (`.md`)
- Technical documents written in Korean
- API documentation and user guides

---

> **⚠️ 이 문서는 AI로 번역된 문서입니다.**
>
> **⚠️ This document has been translated by AI.**