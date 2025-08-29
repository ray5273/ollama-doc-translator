# Ollama Document Translator

This project provides a GitHub Actions workflow for automatically translating Korean documents to English using the local Ollama API.

## Main Features

English translation:
- **Automated Translation:** Automatically translate Korean Markdown files in the `docs/` folder to the `docs-en/` folder
- **AI Model:** Use Exaone3.5:7.8b model for high-quality translations
- **Workflow Automation:** Fully automated translation process using GitHub Actions
- **Automatic PR Creation:** Automatically create Pull Requests upon completion of the translation

## How to Use

1. Add a Korean Markdown file to the `docs/` folder
2. When you commit to GitHub, the automatic translation workflow will be triggered
3. Once the translation is completed, an English version will be generated in the `docs-en/` folder
4. Review and merge the automatically created PR.

## Setup Requirements

English translation:
- The local Ollama server must have the exaone3.5:7.8b model installed
- Access to the Ollama API from GitHub Actions should be possible

## Supported File Types

English translation:
- Markdown file (`.md`)
- Korean-written descriptive document
- API documentation and user guide