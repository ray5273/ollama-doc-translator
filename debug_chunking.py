#!/usr/bin/env python3

import os
from pathlib import Path

# Model-specific tokenizer loading with fallbacks
_TOKENIZER = None
_TOKEN_ENCODING = None

def load_model_tokenizer(model_name):
    """Load appropriate tokenizer based on model name"""
    global _TOKENIZER, _TOKEN_ENCODING
    
    # Model-specific tokenizer mapping
    model_tokenizers = {
        'exaone3.5': 'LGAI-EXAONE/EXAONE-3.0-7.8B-Instruct',
        'exaone': 'LGAI-EXAONE/EXAONE-3.0-7.8B-Instruct',
        'llama': 'meta-llama/Llama-2-7b-hf',
        'mistral': 'mistralai/Mistral-7B-v0.1',
        'qwen': 'Qwen/Qwen2-7B',
        'gemma': 'google/gemma-7b'
    }
    
    # Try model-specific tokenizer first
    try:
        from transformers import AutoTokenizer
        
        # Find matching tokenizer for the model
        tokenizer_name = None
        for key, value in model_tokenizers.items():
            if key.lower() in model_name.lower():
                tokenizer_name = value
                break
        
        if tokenizer_name:
            print(f"🔄 Loading tokenizer for {model_name}: {tokenizer_name}")
            _TOKENIZER = AutoTokenizer.from_pretrained(tokenizer_name, trust_remote_code=True)
            print(f"✅ Successfully loaded {tokenizer_name} tokenizer")
            return True
    except Exception as e:
        print(f"⚠️  Failed to load model-specific tokenizer: {e}")
    
    # Fallback to tiktoken
    try:
        import tiktoken
        _TOKEN_ENCODING = tiktoken.get_encoding("cl100k_base")
        print("✅ Using tiktoken cl100k_base tokenizer as fallback")
        return True
    except Exception as e:
        print(f"⚠️  Failed to load tiktoken: {e}")
    
    print("⚠️  No tokenizer available, using character-based estimation")
    return False

def token_length(text):
    """Return token length using the best available tokenizer."""
    # Try model-specific tokenizer first (most accurate)
    if _TOKENIZER:
        try:
            tokens = _TOKENIZER.encode(text, add_special_tokens=False)
            return len(tokens)
        except Exception as e:
            print(f"⚠️  Model tokenizer error: {e}", flush=True)
    
    # Fallback to tiktoken
    if _TOKEN_ENCODING:
        try:
            return len(_TOKEN_ENCODING.encode(text))
        except Exception as e:
            print(f"⚠️  Tiktoken error: {e}", flush=True)
    
    # Final fallback to character-based estimation
    # Korean text typically has higher token density
    if any('\u3130' <= char <= '\u318F' or '\uAC00' <= char <= '\uD7AF' for char in text):
        # Korean: ~3.5 chars per token
        return max(1, len(text) // 3)
    else:
        # English/other: ~4 chars per token
        return max(1, len(text) // 4)

def get_tokenizer_info():
    """Return information about the currently active tokenizer."""
    if _TOKENIZER:
        try:
            model_name = getattr(_TOKENIZER, 'name_or_path', 'Unknown')
            return f"🤖 Model-specific tokenizer: {model_name}"
        except:
            return "🤖 Model-specific tokenizer: Active"
    elif _TOKEN_ENCODING:
        return "🔧 Tiktoken tokenizer: cl100k_base"
    else:
        return "📏 Character-based estimation (Korean-optimized)"

def analyze_file_chunking():
    """mega-token-example-01.md 파일의 청킹 분석"""
    # Initialize tokenizer for exaone3.5:7.8b
    load_model_tokenizer('exaone3.5:7.8b')
    
    input_file = Path('docs/mega-token-example-01.md')
    
    if not input_file.exists():
        print("❌ docs/mega-token-example-01.md 파일이 없습니다.")
        return
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"📄 파일 분석: {input_file}")
    print(f"📊 {get_tokenizer_info()}")
    print(f"📏 총 문자 수: {len(content):,}")
    print(f"🎯 총 토큰 수: {token_length(content):,}")
    print(f"📊 토큰/문자 비율: {token_length(content) / len(content):.3f}")
    
    # 컨텍스트 길이별 청크 수 분석
    contexts = [4096, 8192, 16384, 32768]
    
    for context_length in contexts:
        prompt_overhead_old = 500
        prompt_overhead_new = 400
        output_reserve_old = context_length // 2
        output_reserve_new = min(context_length // 4, 3072)  # Latest optimization
        
        safe_tokens_old = max(1, context_length - prompt_overhead_old - output_reserve_old)
        safe_tokens_new = max(1, context_length - prompt_overhead_new - output_reserve_new)
        
        chunks_old = token_length(content) // safe_tokens_old + 1
        chunks_new = token_length(content) // safe_tokens_new + 1
        
        print(f"\n📋 Context {context_length}:")
        print(f"   Old: {safe_tokens_old:,} tokens/chunk → ~{chunks_old} chunks")
        print(f"   New: {safe_tokens_new:,} tokens/chunk → ~{chunks_new} chunks")

if __name__ == "__main__":
    analyze_file_chunking()