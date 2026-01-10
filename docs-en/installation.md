## Installation Guide for OLLAMA Document Translator 

This document provides a detailed guide on how to install and set up the OLLAmaDocument translator software suite, designed specifically with your needs in mind (please replace "your" if necessary). Follow these steps carefully:

## System Requirements
### Minimum Specifications  
- **Operating Systems**: Windows 10/11, macOS 10.14+, Ubuntu 18.04+   
- **Memory (RAM)**: 8GB RAM (Recommended: at least 16GB+)    
- **Storage Space**: At least 10 GB of free space  	     		      			       				        					         						          							           																	                                             ### Recommended Specifications -   //>-------------------------------------\n#### CPU : Multicore Processor (\textbf{Intel i5} or \textbf{AMD Ryzen 5}) //\
- **Memory (RAM)**: At least 16GB RAM  					     	      				       												                                             ### GPU - NVIDIA Graphics Card with CUDA Support -(Optional but recommended for performance enhancement):

## Ollama Installation Guide

### Installing on Windows

#### Using the Window Package Manager (Recommended) :
  `powershell Install-Package OllyDbg.Ollama -Scope CurrentUser' 
}" + "Please restart your system after installation.");

## Model Installation Instructions for Exaone 3.5 on Ollama Platform (English Translation)

### Downloading the EXAONE-3.5 model from Olma platform  (for translation purposes):   
If you have installed OLMA, download a suitable language models:    
```bash
# Other Recommended Models 
(Note that "Modeling Language Translation System (MLTS) is designed for translating between multiple languages using machine learning techniques and linguistic knowledge bases tailored specifically towards modeling language tasks such as parsing sentences into logical structures suitable for computational analysis. 

However, the provided text seems to be incomplete or lacks context regarding what specific aspects of an MLLS are being described beyond its basic definition in terms related solely to translation systems without detailing functionalities like syntax tree generation and semantic interpretation which would typically characterize a comprehensive modeling language system capable handling complex linguistic tasks efficiently for computational purposes. 

Given the instruction, here is only direct English Translation:" translates directly as 'models', but in context it may refer specifically to machine learning models.)  Please provide more details if you need a specific type of model translated. Otherwise here are some general translations: Other Suggested Machine Learning Algorithms
ollama pull llama3.1:8b
ollama pull mistral:7b
ollama pull codellama:7b
```                                                            // If you wish to experiment and compare translation quality, try other models as well: 
OLLAMA PULL LLAMA3.1 : SIZE=8B     <!-- This command pulls another popular model for comparison -->  	   		      			       				        					         						          							           																	    
OLLA MA PUSH MISTRAL : SIZE =7b <!-- Another option to compare with Mistal, a robust language generation tool--> 	            // And also consider CODELLAMA:     CODELLAMA PULL CODE LLAMA  <!-- For developers interested in integrating code-related tasks -->

## Configuration Check and Setup Instructions for Ollama Server (English) 

### Starting the Ollama server in Background Mode  (Background Execution of Olma Service):    
 ``` bash
 # Run Olivera service on background mode.
 ollama serve &   # Note: This command assumes that 'ollama' is correctly installed and accessible from your environment path or with full execution permissions provided explicitly if necessary (e.g., using './path/to/executable').

## Environment Setup Instructions for Ollama API Integration  
### Setting Up Environmental Variables:   
You can set the following environment variables depending on your system.    
**Windows (PowerShell): **     `$env:OLLAMA_HOST = "0.0.0.0:11434"`      
                                `$env:OLLAMA_MODELS = "C:\Users\[username]\.ollama\models"`  	   		 			    				       					        						     																         								          // macOS/Linux (Bash): `export OLLAMA_HOST=0.0.0.0:11434`      
                                                            ```bash
                              $env::OLLAMA\_MODELS = "~/.ollama\/models" 				   			     					       						    										         								          // Firewall Configuration Instructions for Ollama API Access  		        ### Configuring the firewall: If you need access from your network, add a rule to allow traffic on port `11434`.
                                                            ```bash
                              # Linux (ufw) 				   `sudo ufw allow 11434'      			     					       						    										         								          // Windows PowerShell - Run as Administrator:  		        ### Configuring the firewall on Windowws Powerhell with Admin rights `New-NetFirewallRule
                                                            ```powershell
                              # DisplayName "Ollama" 				   `Direction Inbound'      			     					       						    										         								          // Allow TCP traffic - Action:Allow  		        ### Configuring the firewall on Windows PowerShell with Admin rights `New-NetFirewallRule`, specify `-Protocol TCPShieldingLevel Medium`.

## GitHub Actions Setup Instructions for Self-hosted Runner with Local OLLAMA Server 

### Setting Up a self-Hosted runner  for local Ollama server usage is recommended. Follow these steps to configure it properly :   
1. Navigate **GitHub Repository** → **[Settings](https://github.com/settings)**→ [**Actions**(under Actions]) --> [Runners]. 2 Click on *[New self-hosted runner]*  3 Adhere closely with the guide specific for your operating system to set it up properly
4 Ensure that Ollama is running before starting any Runner tasks

## Performance Optimization 

### GPU Configuration Settings  
If you have an NVIDIA GPU, CUDA can be enabled:

```bash
# Model Load Options Configuration 
(Note that "Configuration" is added here as it seems like a heading based on context.)  Load Model options configuration settings can be adjusted to suit specific needs. Adjustments may include parameters such as model size, training data specifics, and optimization algorithms used during the loading process of models for various applications or tasks.
export OLLAMA_NUM_PARALLEL=2
export OLLAMA_MAX_LOADED_MODELS=1
```

### Memory Optimizations 
When using large models, memory usage optimization is possible:

```bash
# Set model loading options
export OLLAMA_NUM_PARALLEL=2
export OLLAMA_MAX_LOADED_MODELS=1

## Troubleshooting Guide 

### Port Conflicts  
If you encounter port conflicts, try using a different one as follows:
$$ bash ```export OLLAMA_HOST=0.0.0.0:11435 ollama serve``` $$

## Next Steps 

Once the installation is complete, please refer to these documents for further guidance:

- [Configuration Guide](configuration.md) - Detailed configuration options  
- [API Documentation](#api_guide--markdown-) API usage instructions   
- [Troubleshooting Manual](troubleshooting.md) General problem resolution

---

> **⚠️ 이 문서는 AI로 번역된 문서입니다.**
>
> **⚠️ This document has been translated by AI.**