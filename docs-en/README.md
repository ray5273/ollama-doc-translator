# Ollama Document Translator

This project provides a GitHub Actions workflow for automatically translating Korean documents into English using a local Ollama API.

## Key Features

- **Automatic Translation**: Automatically translates Markdown documents in the `docs/` folder to English in the `docs-en/` folder
- **AI Model**: Utilizes the Exaone3.5:7.8b model for high-quality translation
- **Workflow Automation**: Fully automated translation process via GitHub Actions
- **PR Creation**: Automatically generates a Pull Request upon completion of translation

## Usage Instructions

1. Add Korean Markdown documents to the `docs/` folder
2. Commit to GitHub to trigger the automated translation workflow
3. Upon completion, English versions will be generated in the `docs-en/` folder
4. Review and merge the automatically generated PR

## Setup Requirements

- Exaone3.5:7.8b model installed on a local Ollama server
- Access to the Ollama API within GitHub Actions

## Supported File Formats

- Markdown files (`.md`)
- Technical documents written in Korean
- API documentation and user guides