# Ollama Document Translator

```markdown
This project provides a GitHub Actions workflow for automatically translating Korean documents into English using a local Ollama API.
```

## Key Features

```markdown
- **Automatic Translation**: Automatically translate Korean Markdown documents in the `docs/` folder to English in the `docs-en/` folder
- **AI Model**: Utilizes the Exaone3.5:7.8b model for high-quality translation
- **Workflow Automation**: Fully automated translation process using GitHub Actions
- **PR Auto Generation**: Automatically generates a Pull Request upon completion of translation
```

## Usage Instructions

```markdown
1. Add Korean Markdown documents to the `docs/` folder
2. Committing to GitHub triggers the automatic translation workflow
3. Upon completion of translation, an English version will be generated in the `docs-en/` folder
4. Review and merge the automatically generated PR
```

## Setup Requirements

```
- An exaone3.5 model (version 7.8b) must be installed on your local Ollama server.
- You must have access to the Ollama API from GitHub Actions.
```

## Supported File Formats

- Markdown file (`.md`)
- Technical document written in Korean
- API documentation and user guides