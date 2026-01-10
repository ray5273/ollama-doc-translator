# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a GitHub Action that translates Korean markdown documents to English using Ollama with the EXAONE 3.5 model. It consists of two main components:

1. **GitHub Action** (root) - Automatic Korean→English markdown translation via Ollama API
2. **Fine-tuning Module** (`markdown-translator-finetuning/`) - Tools for fine-tuning open-weight LLMs for markdown translation

## Commands

### Root Project (GitHub Action)

```bash
# Local testing - translates docs/ to docs-en/
python translate-local.py

# Docker testing
docker build -t ollama-translator .
docker run --network host ollama-translator

# Requires: Ollama running with exaone3.5:7.8b model
ollama serve
ollama pull exaone3.5:7.8b
```

### Fine-tuning Module (`markdown-translator-finetuning/`)

```bash
cd markdown-translator-finetuning

# Install dependencies
python -m pip install -r requirements.txt

# Generate training data
python scripts/generate_synthetic.py --method template --num-samples 1000
python scripts/generate_synthetic.py --method openai --num-samples 1000 --parallel --max-concurrent 50
python scripts/generate_synthetic.py --method ollama --model llama3.1:8b --num-samples 100

# Preprocess data
python scripts/prepare_data.py --input data/raw --output data/processed --include-synthetic

# Training (QLoRA for 12-16GB VRAM)
python scripts/train.py --config configs/training_config.yaml --qlora

# Evaluation
python scripts/evaluate.py --adapter-path outputs/checkpoints/final/adapter

# Inference
python scripts/inference.py --input docs/README.ko.md --output docs/README.en.md
python scripts/inference.py --interactive

# Upload to Hub
python scripts/upload_to_hub.py --adapter-path outputs/checkpoints/final/adapter --repo-id username/model
```

## Architecture

### GitHub Action Flow
1. `action.yml` - Action metadata and input/output definitions
2. `entrypoint.py` - Main logic: Ollama server check → model availability → file discovery → chunk-based translation → PR creation
3. Translation uses paragraph-level chunking (split by `\n\n`) with retry logic and exponential backoff

### Fine-tuning Module Structure
```
markdown-translator-finetuning/
├── configs/           # YAML configs for QLoRA, LoRA, training, inference, Hub upload
├── src/
│   ├── data/          # Synthetic generation, preprocessing, async batch generation
│   ├── model/         # Model loading (QLoRA/LoRA), Hub upload
│   ├── training/      # Trainer, collator, callbacks
│   ├── evaluation/    # BLEU, chrF, COMET, markdown preservation metrics
│   └── inference/     # Translation pipeline
└── scripts/           # CLI entrypoints for all operations
```

### Key Design Decisions
- Translations preserve markdown structure (code blocks, links, tables)
- Files split into chunks at paragraph boundaries to handle large documents
- Skip-existing logic based on file modification timestamps
- GitHub Enterprise support via configurable API URLs
- Multiple LLM providers for data generation: OpenAI, Anthropic, Ollama, vLLM

## Code Style

- Python 3.11+ required
- PEP 8 with line length 100 (configured in pyproject.toml)
- Type hints encouraged
- Commit messages: `feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`

## Testing

The project relies on integration testing with a running Ollama instance. Mock the Ollama API for unit tests:

```python
from unittest.mock import patch, Mock

@patch('requests.post')
def test_translate_with_ollama(mock_post):
    mock_response = Mock()
    mock_response.json.return_value = {'response': 'Translated text'}
    mock_post.return_value = mock_response
    # ... test translation function
```

## Environment Variables

GitHub Action inputs are exposed as `INPUT_*` environment variables (e.g., `INPUT_OLLAMA_URL`, `INPUT_MODEL`, `INPUT_SOURCE_DIR`).

For fine-tuning, API keys are set via:
- `OPENAI_API_KEY` - OpenAI API
- `ANTHROPIC_API_KEY` - Anthropic API
- `HF_TOKEN` - Hugging Face Hub authentication
