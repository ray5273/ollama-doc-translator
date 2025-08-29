# Ollama Documentation Translator

This project provides a GitHub Actions workflow that automatically translates Korean documents into English using a local Ollama API.

## 주요 기능

## Key Features

- **Automatic Translation**: Automatically translate Korean Markdown documents in the `docs/` folder to the `docs-en/` folder.
- **AI Model**: High-quality translation using the Exaone3.5:7.8b model.
- **Workflow Automation**: Fully automated translation process via GitHub Actions.
- **Automatic PR Generation**: Automatically generate a Pull Request after translation is complete.

## How to Use

1. Add Korean Markdown documents to the `docs/` folder.
2. Committing to GitHub will automatically trigger the translation workflow.
3. Once the translation is complete, the English version will be generated in the `docs-en/` folder.
4. Review and merge the automatically generated PR.

## Setup Requirements

- The exaone3.5:7.8b model must be installed on a local Ollama server.
- The GitHub Actions environment must have access to the Ollama API.

## Supported File Formats

- Markdown file (`.md`)
- Technical documentation written in Korean
- API documentation and user guide