# Ollama Korean to English Translator

A GitHub Action that automatically translates Korean markdown documents to English using local Ollama API with Exaone3.5 model.

![GitHub release](https://img.shields.io/github/v/release/your-username/ollama-doc-translator)
![GitHub marketplace](https://img.shields.io/badge/marketplace-ollama--translator-blue)
![License](https://img.shields.io/github/license/your-username/ollama-doc-translator)

## 🚀 Features

- **Automatic Translation**: Translate Korean markdown files to English automatically
- **AI-Powered**: Uses Exaone3.5:7.8b model for high-quality translations  
- **Smart Chunking**: Token-aware paragraph splitting with recursive optimization for large documents
- **Debug & Analysis**: Built-in chunking analysis and debug file generation
- **Customizable**: Configure source/target directories, models, and translation parameters
- **Auto PR Creation**: Automatically creates pull requests with translations
- **Smart Skipping**: Skip files that are already translated and up-to-date
- **Retry Logic**: Built-in retry mechanism for robust API calls

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
      uses: your-username/ollama-doc-translator@v1
      with:
        source-dir: 'docs'
        target-dir: 'docs-en'
        model: 'exaone3.5:7.8b'
        create-pr: true
        github-token: ${{ secrets.GITHUB_TOKEN }}
```

### Advanced Configuration

```yaml
- name: Translate with custom settings
  uses: your-username/ollama-doc-translator@v1
  with:
    ollama-url: 'http://localhost:11434'
    model: 'exaone3.5:7.8b'
    source-dir: 'korean-docs'
    target-dir: 'english-docs'
    file-pattern: '**/*.md'
    temperature: 0.2
    max-retries: 5
    skip-existing: true
    create-pr: true
    pr-title: 'Auto-translated documentation update'
    pr-branch: 'auto-translation'
    commit-message: 'docs: Auto-translate Korean to English'
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
| `create-pr` | Create pull request | No | `true` |
| `pr-title` | Pull request title | No | `Update English documentation translations` |
| `pr-branch` | PR branch name | No | `translation-update` |
| `commit-message` | Commit message | No | `docs: Update English translations` |
| `github-token` | GitHub token for PR creation | No | `${{ github.token }}` |
| `context-length` | Model context length for chunking | No | `32768` |

## 📤 Outputs

| Output | Description |
|--------|-------------|
| `translated-files` | Number of files translated |
| `skipped-files` | Number of files skipped |
| `pr-url` | Pull request URL (if created) |
| `pr-number` | Pull request number (if created) |

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

Debug files are saved to `debug_chunks/` directory:
```
debug_chunks/
├── filename_chunk_001.md          # Individual chunks with metadata
├── filename_chunk_002.md
├── ...
└── filename_summary.md            # Chunking summary report
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

### Token-Aware Chunking Strategy

The system uses sophisticated chunking logic:

1. **Paragraph Detection**: Split content by empty lines (`\n\n`) 
2. **Token Calculation**: Accurate counting using tiktoken (fallback: char-based estimation)
3. **Recursive Splitting**: Large paragraphs split by:
   - Sentences (Korean/English punctuation)
   - Lines (if sentences too long)
   - Character splitting (last resort)
4. **Optimization**: Small chunks regrouped within token limits
5. **Context Awareness**: Uses 40% of context length for safety margin

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