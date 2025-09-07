# Ollama Documentation Translator

This project provides a GitHub Actions workflow that automatically translates Korean documents into English using a local Ollama API.

## Main Features

- **Automatic Translation**: Automatically translates Korean Markdown documents in the `docs/` folder to the `docs-en/` folder.
- **AI Model**: High-quality translation using the exaone3.5:7.8b model.
- **Workflow Automation**: Fully automated translation process via GitHub Actions.
- **Automatic PR Generation**: A Pull Request is automatically generated after the translation is complete.

## How to Use

1. Add Korean Markdown documents to the `docs/` folder.
2. Commit to GitHub, and the automatic translation workflow will be executed.
3. Once the translation is complete, an English version of the documents will be created in the `docs-en/` folder.
4. Review and merge the automatically generated Pull Request.

## Setup Requirements

- The exaone3.5:7.8b model must be installed on your local Ollama server.
- Access to the Ollama API is required via GitHub Actions.

## Supported File Formats

- Markdown files (.md)
- Technical documents written in Korean
- API documentation and user guides

---

> **⚠️ 이 문서는 AI로 번역된 문서입니다.**
>
> **⚠️ This document has been translated by AI.**