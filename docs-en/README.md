# OllaMa Document Translator Documentation Generator for GitHub Actions Workflows using Local Ollama APIs and Exaone 3.5:7.8b Model Translation AI  

This project provides a GitLab Action workflow that automatically translates Korean documents into English utilizing the local Olma API, powered by an advanced translation model based on EXAONE-3.5 (version with enhanced capabilities). Below are detailed instructions and specifications for using this tool effectively in your repository workflows: 

## Key Features
  
- **Automatic Translation**: Automatically translates Markdown documents from the `docs/` folder into English within a new directory named `/docses`.   
- **AI Model Integration**: Utilizes EXAONE3.5 (version with enhanced capabilities):7.8b model for high quality translations 
- **Workflow Automation**: Fully automated translation process triggered by GitHub Actions  
- **PR Generation Automatically Created Post Translation Completion** : Creates a Pull Request automatically after the completion of translating documents into English versions in `/docses`.   
    
## How to Use It? Steps Below!     	 
1. Add Korean Markdown files (`*.md`) or technical documentation written entirely in your preferred language within `docs/`, ensuring they are structured appropriately for translation needs, including API specifications and user guides if applicable;  
2. Commit changes back into GitHub – this triggers the automated workflow to start processing translations through Ollama APIs seamlessly integrated with EXAONE3:78b model capabilities enhanced version ; 
3. Once completed successfully in `docs-en/`, you will find your translated English versions ready for review and merging;  
4. Review automatically generated PRs, merge them into the main branch as needed to incorporate updated translations seamlessly within project documentation structure!   	     		    			       				      					 
## Requirements Setup:                                       						         							          								           									            - Ensure that an instance of EXAONE35 (enhanced capabilities version):7.8b model is installed on your local Ollama server;  
- Access to the Olma API must be configured within GitHub Actions settings for seamless integration and operation! 
## Supported File Formats:                                             					   	     			       				      						    		 - Markdown files (`.md`) formatted appropriately with necessary metadata or structure markers if needed by translation algorithms;  
- Technical documentation written entirely in Korean language, ensuring clarity of content is maintained during the transformation process for accurate translations! 
*Note: Specific configurations and additional setup steps may be required depending on your environment settings.*

---

> **⚠️ 이 문서는 AI로 번역된 문서입니다.**
>
> **⚠️ This document has been translated by AI.**