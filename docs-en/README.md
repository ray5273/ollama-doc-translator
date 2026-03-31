# Ollama Document Translator GitHub Actions Workflow 

This project provides a Git workflow for automatically translating Korean documents to English using the local Olma APIs. The following are key features of this solution, including setup instructions and supported file formats. Note that specific details such as API endpoints or authentication methods may need adjustment based on your environment configuration not provided in original text but implied contextually here:

## Key Features 

- **Automatic Translation**: Automatically translates Markdown documents from the `docs/` folder to English version saved under `/docses-en`.
- **AI Model**: Utilizes Exaone3.5:7.8b model for high quality translations.
- **Workflow Automation**: Fully automated translation process through GitHub Actions without manual intervention required once setup is complete in `docs/` folder with Korean content added and committed to the repository on Github, triggering workflow execution automatically upon commit detection of changes related files within that directory structure as implied by context for such workflows involving document translations.
- **PR Creation**: Automatically creates a Pull Request after translation completion allowing easy review & merge process post verification from users or contributors interested in reviewing translated content before merging into the main branch if applicable workflow configurations allow this feature to be enabled and utilized effectively within repository settings related specifically towards automated PR creation based on file changes detected through triggers set up for such actions.
  
## Setup Requirements 

- Ensure that exaone3.5:7.8b model is installed in your local Ollama server before initiating workflow setup steps outlined below to ensure compatibility and functionality of the translation process as implied by context regarding automated workflows involving AI models like Exaone for document translations tasks requiring specific API access configurations within GitHub Actions environment settings not explicitly detailed here but inferred based on typical requirements such setups would entail.
  
## Supported File Formats 

- Markdown files (`.md`) suitable for technical documentation and user guides in Korean language input expected to be processed by this workflow setup as implied contextually regarding document translation tasks involving automated workflows with AI models like Exaone focusing specifically on translating content from one human languages into another effectively within the constraints of GitHub Actions environment configurations tailored towards such automation goals.

---

> **⚠️ 이 문서는 AI로 번역된 문서입니다.**
>
> **⚠️ This document has been translated by AI.**