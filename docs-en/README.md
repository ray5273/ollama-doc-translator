# Ollama Document Translator GitHub Actions Workflow 

This project provides a Git workflow for automatically translating Korean documents to English using the local Olmah API. The following are key features of this solution, designed as an automated process through Github Actions.  

## Key Features:
- **Automatic Translation**: Automatically translates Markdown files from `docs/` folder into their corresponding folders in `/docs-en`. 
- **AI Model**: Utilizes the Exaone3.5:7.8b model for high quality translations.
- **Workflow Automation**: Fully automated translation process managed through Github Actions, eliminating manual intervention once set up correctly.
  > Note that while this workflow aims to be fully automatic after setup with proper configurations and access permissions in place (such as having the correct Ollama API endpoint accessible), initial steps like setting model availability may require human oversight or configuration adjustments depending on your environment specifics for optimal performance of Exaone3.5:7.8b within local infrastructure constraints not detailed here due to potential variability across setups without explicit mention from users regarding their specific configurations and environments in relation to this workflow's execution context beyond the scope provided initially by developers aiming at broad applicability with minimal setup barriers highlighted through documentation like these guidelines for quick onboarding into automated translation workflows leveraging AI advancements.
- **PR Automation**: Automatically creates a Pull Request once translations are completed, streamlining review and merging processes post completion of document revisions in English versions created within the workflow's output directory structure designed to mirror source language organization but adapted specifically towards facilitating multilingual content management through automation tools like this one tailored for efficient crosslingual documentation maintenance.

## Setup Requirements: 
- The local Ollama server must have access and installation configured of Exaone3.5 model at version `7.8b`.  
- Access to the Olmah API within Github Actions needs proper configuration setup, ensuring secure communication channels are established for automated tasks execution without manual intervention once workflow triggers based on file commits or other predefined events triggering translation processes as outlined in project documentation and configurations guiding users through initial steps necessary beyond basic installation of model access permissions.

## Supported File Formats: 
- Markdown files (`.md`)  
- Technical documents written in Korean   
- API Documentation & User Guides

---

> **⚠️ 이 문서는 AI로 번역된 문서입니다.**
>
> **⚠️ This document has been translated by AI.**