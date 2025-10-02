# Ollama Korean to English Translator

A GitHub Action that automatically translates Korean markdown documents to English using local Ollama API with Exaone3.5 model.

![GitHub release](https://img.shields.io/github/v/release/ray5273/ollama-doc-translator)
![GitHub marketplace](https://img.shields.io/badge/marketplace-ollama--translator-blue)
![License](https://img.shields.io/github/license/ray5273/ollama-doc-translator)

## 🚀 Features

- **Automatic Translation**: Translate Korean markdown files to English automatically
- **AI-Powered**: Uses Exaone3.5:7.8b model for high-quality translations  
- **Smart Chunking**: Section-aware splitting with code block preservation and semantic boundary detection
- **Translation Quality**: Preserves numbered lists, prevents formatting corruption, maintains consistent terminology
- **Debug & Analysis**: Comprehensive chunking analysis and debug file generation with side-by-side comparisons
- **Code Block Protection**: Never splits code blocks across chunks, preserves all programming languages
- **Customizable**: Configure source/target directories, models, translation parameters, and chunking strategies
- **Smart Branch Management**: Automatic branch detection with options for direct commits or pull requests
- **Smart Skipping**: Skip files that are already translated and up-to-date
- **Retry Logic**: Built-in retry mechanism with exponential backoff for robust API calls

## 📋 Prerequisites

- A running Ollama server with access to the Exaone3.5:7.8b model
- GitHub repository with Korean markdown files

## 🛠️ Usage

### Basic Usage

```yaml
name: Translate Korean Docs

on:
  push:
    branches: [ main ]
    paths: [ 'docs/**/*.md' ]

jobs:
  translate:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Translate Korean to English
      uses: ray5273/ollama-doc-translator@v1
      with:
        source-dir: 'docs'
        target-dir: 'docs-en'
        model: 'exaone3.5:7.8b'
        # Commits directly to main branch by default
        github-token: ${{ secrets.GITHUB_TOKEN }}
```

### Advanced Configuration

```yaml
- name: Translate with custom settings
  uses: ray5273/ollama-doc-translator@v1
  with:
    # Server & Model Configuration
    ollama-url: 'http://localhost:11434'
    model: 'exaone3.5:7.8b'
    context-length: 32768
    
    # Directory & File Settings  
    source-dir: 'korean-docs'
    target-dir: 'english-docs'
    file-pattern: '**/*.md'
    
    # Translation Quality Settings
    temperature: 0.2              # More consistent translations
    max-retries: 5               # More robust error handling
    skip-existing: true
    
    # Debug & Analysis
    debug-mode: true             # Generate debug files for analysis
    
    # Commit Strategy (choose one)
    # Option 1: Commit directly to current branch (default)
    create-pr: false
    commit-message: 'docs: Auto-translate Korean to English'
    # base-branch: ''  # Uses current branch if empty

    # Option 2: Commit to specific branch
    # base-branch: 'main'  # Force commit to main branch

    # Option 3: Create pull request
    # create-pr: true
    # pr-title: 'Auto-translated documentation update'
    # pr-branch: 'auto-translation'
    # base-branch: 'main'  # Target branch for PR

    github-token: ${{ secrets.GITHUB_TOKEN }}
```

## 📝 Inputs

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `ollama-url` | Ollama API URL | No | `http://localhost:11434` |
| `model` | Ollama model for translation | No | `exaone3.5:7.8b` |
| `source-dir` | Source directory with Korean files | No | `docs` |
| `target-dir` | Target directory for English files | No | `docs-en` |
| `file-pattern` | File pattern to match (glob) | No | `**/*.md` |
| `temperature` | Model temperature (0.0-1.0) | No | `0.3` |
| `max-retries` | Maximum API call retries | No | `3` |
| `skip-existing` | Skip existing newer files | No | `true` |
| `create-pr` | Create pull request (if false, commits directly to base branch) | No | `false` |
| `base-branch` | Target branch for commits/PR (uses current branch if empty) | No | `main` |
| `pr-title` | Pull request title | No | `Update English documentation translations` |
| `pr-branch` | PR branch name | No | `translation-update` |
| `commit-message` | Commit message | No | `docs: Update English translations` |
| `github-token` | GitHub token for PR creation | No | `${{ github.token }}` |
| `context-length` | Model context length for chunking | No | `32768` |
| `debug-mode` | Enable debug analysis files (chunks/originals/translations/comparisons) | No | `false` |

## 📤 Outputs

| Output | Description |
|--------|-------------|
| `translated-files` | Number of files translated |
| `skipped-files` | Number of files skipped |
| `pr-url` | Pull request URL (if created) |
| `pr-number` | Pull request number (if created) |

## 🌿 Branch Management

The action supports flexible branch management with automatic branch detection:

### Direct Commit (Default)
```yaml
- uses: ray5273/ollama-doc-translator@v1
  with:
    create-pr: false  # Default behavior
    # Commits directly to current branch automatically
```

### Commit to Specific Branch
```yaml
- uses: ray5273/ollama-doc-translator@v1
  with:
    create-pr: false
    base-branch: 'main'  # Force commit to main branch
```

### Create Pull Request
```yaml
- uses: ray5273/ollama-doc-translator@v1
  with:
    create-pr: true
    base-branch: 'main'     # Target branch for PR
    pr-branch: 'translate-update'  # Source branch name
    pr-title: 'Update translations'
```

### Automatic Branch Detection
- **Empty `base-branch`**: Uses current working branch automatically
- **Specified `base-branch`**: Uses the specified branch
- **GitHub Workflows**: Can use `${{ github.ref_name }}` for current branch

This ensures the action works correctly regardless of which branch triggers the workflow (main, develop, feature branches, etc.).

## 🔧 Setup Instructions

### 1. Ollama Server Setup

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Start Ollama server  
ollama serve

# Pull the translation model
ollama pull exaone3.5:7.8b
```

### 2. Repository Setup

1. Create Korean markdown files in your `docs/` directory
2. Add the workflow file to `.github/workflows/translate.yml`
3. Push changes to trigger the translation

### 3. Self-Hosted Runner (Recommended)

For best performance with local Ollama, use a self-hosted runner:

```yaml
jobs:
  translate:
    runs-on: self-hosted  # Use your own runner with Ollama
```

## 📁 Example Project Structure

```
your-repo/
├── .github/workflows/
│   └── translate.yml           # Translation workflow
├── docs/                       # Korean documentation
│   ├── README.md
│   ├── api-guide.md
│   └── user-manual.md
├── docs-en/                    # English translations (auto-generated)
│   ├── README.md
│   ├── api-guide.md
│   └── user-manual.md
└── README.md
```

## 🔍 Smart Chunking & Debug Features

### Automatic Debug File Generation

During translation, the system automatically generates debug files to help you understand how large documents are being processed:

- **Real-time chunking logs**: Console output showing paragraph analysis and splitting decisions
- **Debug chunks**: Individual `.md` files for each chunk with metadata headers
- **Summary reports**: Overview of chunking process with token distribution

Debug files are saved to multiple directories for comprehensive analysis:
```
your-repo/
├── debug_chunks/                   # Chunking analysis
│   ├── filename_chunk_001.md      # Individual chunks with token count
│   ├── filename_chunk_002.md
│   └── filename_summary.md        # Chunking summary report
├── debug_originals/                # Original Korean chunks  
│   ├── filename_original_001.md   # Source chunks before translation
│   └── filename_original_002.md
├── debug_translations/             # English translated chunks
│   ├── filename_translated_001.md # Translated chunks after processing
│   └── filename_translated_002.md  
└── debug_comparisons/              # Side-by-side comparisons
    ├── filename_comparison_001.md # Original vs translated analysis
    └── filename_comparison_002.md
```

### Standalone Chunking Analysis

For advanced debugging and optimization, use the standalone analysis tool:

```bash
# Analyze chunking process without translation
python debug_chunking_standalone.py docs/large-document.md
```

**Features:**
- Step-by-step visualization of paragraph splitting
- Token distribution statistics (min/max/average)  
- Detailed analysis reports with chunk previews
- Individual chunk files for manual inspection

**Output files in `debug_chunks_analysis/`:**
- `*_analysis.md`: Comprehensive analysis report
- `*_final_chunk_*.md`: Final optimized chunks

### Advanced Chunking Strategy

The system uses sophisticated section-aware chunking logic:

1. **Section-Based Splitting**: 
   - H1-H2 headings: Always create split boundaries
   - H3 headings: Split when content > 200 tokens
   - Preserves semantic meaning and document structure

2. **Code Block Preservation**: 
   - Automatically detects ````python`, ````yaml`, ````bash` blocks
   - Never splits code blocks across chunks
   - Ignores `#` comments inside code blocks as headings

3. **Smart Content Joining**: 
   - Preserves numbered lists without extra line breaks
   - Detects patterns like "- 288. Item" → "- 289. Item"
   - Maintains proper markdown formatting

4. **Translation Quality Enhancements**:
   - Preserves ALL numbers in numbered lists exactly as they appear
   - Prevents unauthorized bold/italic formatting additions
   - Maintains consistent terminology across chunks

5. **Token Calculation**: 
   - Accurate counting using tiktoken (fallback: language-specific estimation)
   - Korean chars: ~0.5 tokens, Code chars: ~0.8 tokens
   - Context awareness: Uses 40% of context length for safety margin

## 🎛️ Manual Workflow Control

The GitHub Action supports manual triggering with customizable options:

### Workflow Dispatch Example
```yaml
name: Translate Korean Docs to English

on:
  workflow_dispatch:
    inputs:
      base_branch:
        description: 'Target branch (leave empty for current branch)'
        required: false
        default: ''
        type: string
      create_pr:
        description: 'Create pull request instead of direct commit'
        required: false
        default: false
        type: boolean
      force_translate:
        description: 'Force translate all files (ignore skip-existing)'
        required: false
        default: false
        type: boolean
      specific_files:
        description: 'Specific files to translate (comma-separated)'
        required: false
        default: ''
        type: string

jobs:
  translate:
    runs-on: self-hosted
    steps:
    - uses: actions/checkout@v4
    - uses: ray5273/ollama-doc-translator@v1
      with:
        base-branch: ${{ inputs.base_branch || github.ref_name }}
        create-pr: ${{ inputs.create_pr }}
        specific-files: ${{ inputs.specific_files }}
        skip-existing: ${{ !inputs.force_translate }}
        github-token: ${{ secrets.GITHUB_TOKEN }}
```

### Manual Trigger Benefits
- **Branch Control**: Choose target branch or use current branch
- **Selective Translation**: Translate specific files only
- **Force Mode**: Re-translate all files regardless of modification time
- **Commit Strategy**: Choose between direct commit or pull request

## 🚀 Getting Started

1. **Fork this repository** or create a new one
2. **Add Korean markdown files** to the `docs/` directory
3. **Create a workflow file** (see usage examples above)
4. **Set up Ollama** on your runner with the required model
5. **Push changes** to trigger automatic translation

### For Large Documents

When working with large documents (>30,000 tokens):

1. **Monitor debug output**: Check console logs for chunking details
2. **Review debug files**: Inspect generated chunk files in `debug_chunks/`
3. **Adjust context length**: Increase `context-length` input if needed
4. **Use analysis tool**: Run `debug_chunking_standalone.py` for optimization

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Ollama](https://ollama.com/) for providing the local LLM infrastructure
- [Exaone3.5](https://github.com/LG-AI-Research/exaone) for the translation model
- GitHub Actions community for inspiration and best practices
