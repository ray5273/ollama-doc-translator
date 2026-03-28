# Ollama Document Translator

This project provides a GitHub Actions workflow that automatically translates Korean documents to English using the local Ollama API.

## Key Features

- **Automatic Translation**: Automatically translates Korean Markdown documents in the `docs/` folder to the `docs-en/` folder.
- **AI Model**: Uses the Exaone3.5:7.8b model for high-quality translation.
- **Workflow Automation**: Fully automated translation process through GitHub Actions.
- **Automatic PR Generation**: Automatically creates a Pull Request after translation is complete.

## Usage Instructions

1. Add Korean Markdown documents to the `docs/` folder.
2. When you commit to GitHub, the automatic translation workflow will run.
3. After translation is complete, the English version will be created in the `docs-en/` folder.
4. Review and merge the automatically generated PR.

## Setup Requirements

- The exaone3.5:7.8b model must be installed on the local Ollama server.
- Access to the Ollama API must be available from GitHub Actions.

## Supported File Formats

- Markdown files (`.md`)
- Technical documents written in Korean
- API documentation and user guides

---

> **⚠️ 이 문서는 AI로 번역된 문서입니다.**
>
> **⚠️ This document has been translated by AI.**