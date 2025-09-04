#!/usr/bin/env python3
"""
Ollama Korean to English Translator GitHub Action
Translates Korean markdown documents to English using Ollama API
"""

import os
import sys
import json
import requests
import time
import glob
from pathlib import Path
import subprocess
import re

try:
    import tiktoken
    TIKTOKEN_AVAILABLE = True
except ImportError:
    TIKTOKEN_AVAILABLE = False

# Action inputs from environment variables
OLLAMA_URL = os.getenv('INPUT_OLLAMA_URL', 'http://localhost:11434')
MODEL = os.getenv('INPUT_MODEL', 'exaone3.5:7.8b')
SOURCE_DIR = os.getenv('INPUT_SOURCE_DIR', 'docs')
TARGET_DIR = os.getenv('INPUT_TARGET_DIR', 'docs-en')
FILE_PATTERN = os.getenv('INPUT_FILE_PATTERN', '**/*.md')
COMMIT_MESSAGE = os.getenv('INPUT_COMMIT_MESSAGE', 'docs: Update English translations')
CREATE_PR = os.getenv('INPUT_CREATE_PR', 'true').lower() == 'true'
PR_TITLE = os.getenv('INPUT_PR_TITLE', 'Update English documentation translations')
PR_BRANCH = os.getenv('INPUT_PR_BRANCH', 'translation-update')
GITHUB_TOKEN = os.getenv('INPUT_GITHUB_TOKEN', '')
BASE_BRANCH = os.getenv('INPUT_BASE_BRANCH', 'main')
GITHUB_API_URL = os.getenv('INPUT_GITHUB_API_URL', 'https://api.github.com')
SKIP_EXISTING = os.getenv('INPUT_SKIP_EXISTING', 'true').lower() == 'true'
TEMPERATURE = float(os.getenv('INPUT_TEMPERATURE', '0.3'))
MAX_RETRIES = int(os.getenv('INPUT_MAX_RETRIES', '3'))
SSL_VERIFY = os.getenv('INPUT_SSL_VERIFY', 'true').lower() == 'true'
CONTEXT_LENGTH = int(os.getenv('INPUT_CONTEXT_LENGTH') or '32768')

def log(message):
    """Print log message with timestamp"""
    print(f"🔄 {message}", flush=True)

def error(message):
    """Print error message and exit"""
    print(f"❌ Error: {message}", flush=True)
    sys.exit(1)

def success(message):
    """Print success message"""
    print(f"✅ {message}", flush=True)

def set_output(name, value):
    """Set GitHub Actions output"""
    # Use the newer method for setting outputs
    github_output = os.getenv('GITHUB_OUTPUT')
    if github_output:
        with open(github_output, 'a', encoding='utf-8') as f:
            # Handle multiline values properly
            if '\n' in str(value):
                # Use heredoc format for multiline values
                delimiter = f"EOF_{name}_{int(time.time())}"
                f.write(f"{name}<<{delimiter}\n{value}\n{delimiter}\n")
            else:
                # Simple format for single line values
                f.write(f"{name}={value}\n")
    else:
        # Fallback to older method (escape newlines)
        escaped_value = str(value).replace('\n', '%0A')
        print(f"::set-output name={name}::{escaped_value}")

def check_ollama_server():
    """Check if Ollama server is running"""
    try:
        response = requests.get(f"{OLLAMA_URL}/api/tags", timeout=10, verify=SSL_VERIFY)
        return response.status_code == 200
    except Exception as e:
        return False

def check_model_available():
    """Check if the specified model is available"""
    try:
        response = requests.get(f"{OLLAMA_URL}/api/tags", timeout=10, verify=SSL_VERIFY)
        if response.status_code == 200:
            models = response.json()
            model_names = [m['name'] for m in models.get('models', [])]
            return MODEL in model_names
        return False
    except Exception as e:
        return False

def pull_model():
    """Pull the model if not available"""
    log(f"Pulling model: {MODEL}")
    try:
        # Use ollama CLI to pull model
        result = subprocess.run(['ollama', 'pull', MODEL], 
                              capture_output=True, text=True, timeout=600)
        if result.returncode == 0:
            success(f"Model {MODEL} pulled successfully")
            return True
        else:
            log(f"Failed to pull model: {result.stderr}")
            return False
    except Exception as e:
        log(f"Failed to pull model: {str(e)}")
        return False

def translate_with_ollama(text, retries=0):
    """Translate text using Ollama API with retry logic"""
    if retries >= MAX_RETRIES:
        print(f"⚠️  Max retries ({MAX_RETRIES}) reached, returning original text", flush=True)
        return text
    
    prompt = f"""다음 한국어 마크다운 문서를 영어로 번역해주세요. 다음 지침을 엄격히 따르세요:

- 마크다운 형식과 구조를 절대 변경하지 마세요
- 코드 블록, 인라인 코드(`...`), 링크, URL, 이미지 경로, 수식, Mermaid, HTML 주석은 절대 번역하거나 수정하지 마세요
- 코드 블록은 ```python, ```js 등 언어 태그 포함 그대로 유지하세요
- 목록, 테이블, YAML 프론트매터의 구조와 들여쓰기를 그대로 유지하세요
- 입력이 이미 영어이거나 한국어가 없다면 입력 그대로 반환하세요
- 같은 용어는 문서 전체에서 일관되게 번역하세요
- 번역 결과에 ```markdown, ````, "Here is translation:" 등의 추가 포맷팅이나 설명을 절대 추가하지 마세요
- 번역된 내용만 그대로 출력하세요. 어떤 설명이나 주석도 추가하지 마세요
- 문장이 잘린 경우, 불필요하게 추측하지 말고 잘린 부분까지만 충실히 번역하세요

한국어 마크다운 문서:
{text}

영어 마크다운 문서:"""
    
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": TEMPERATURE,
            "top_p": 0.9
        }
    }
    
    try:
        response = requests.post(f"{OLLAMA_URL}/api/generate", 
                               json=payload, timeout=900, verify=SSL_VERIFY)
        response.raise_for_status()
        result = response.json()
        translated = result.get('response', '').strip()
        
        # Store original for fallback
        original_translated = translated
        
        # Clean up response if needed - remove unwanted prefixes and formatting
        if translated.startswith('영어 번역:'):
            translated = translated.replace('영어 번역:', '').strip()
        
        # Remove markdown code block formatting that the AI might add
        if translated.startswith('```markdown\n') and translated.endswith('\n```'):
            translated = translated[12:-4].strip()  # Remove ```markdown\n and \n```
        elif translated.startswith('```\n') and translated.endswith('\n```'):
            translated = translated[4:-4].strip()  # Remove ```\n and \n```
        
        # Remove other common unwanted prefixes
        unwanted_prefixes = [
            'Here is the translation:',
            'Here is the English translation:',
            '영어로 번역하면:',
            '번역 결과:',
            'Translation:',
            'English translation:'
        ]
        
        for prefix in unwanted_prefixes:
            if translated.lower().startswith(prefix.lower()):
                translated = translated[len(prefix):].strip()
                break
        
        # If cleaned result is empty, fall back to original input
        if not translated or translated.isspace():
            print(f"⚠️  Cleaned result is empty, using original input", flush=True)
            return text
        
        return translated
    except Exception as e:
        print(f"⚠️  Translation error (attempt {retries + 1}): {e}", flush=True)
        time.sleep(2 ** retries)  # Exponential backoff
        return translate_with_ollama(text, retries + 1)

def count_tokens(text: str) -> int:
    """Count tokens accurately using tiktoken or improved approximation"""
    if TIKTOKEN_AVAILABLE:
        try:
            # Use GPT-4 tokenizer for accurate counting (handles Korean and English well)
            enc = tiktoken.get_encoding("cl100k_base")
            return len(enc.encode(text))
        except Exception:
            pass
    
    # Improved approximation based on actual measurements
    # Korean: ~1.2 chars/token (more conservative)
    # English: ~3.5 chars/token 
    # Code/markup: ~2 chars/token
    korean_chars = len(re.findall(r'[가-힣]', text))
    code_chars = len(re.findall(r'[`\[\](){}<>]', text))  # Code/markup characters
    other_chars = len(text) - korean_chars - code_chars
    
    # More conservative token estimation
    korean_tokens = korean_chars * 0.85  # ~1.2 chars per token
    code_tokens = code_chars * 0.5       # ~2 chars per token  
    other_tokens = other_chars * 0.3     # ~3.3 chars per token
    
    return int(korean_tokens + code_tokens + other_tokens)

def split_markdown_by_paragraphs(content: str) -> list:
    """Split markdown content by paragraphs while preserving headers with content"""
    # First split by double newlines
    raw_paragraphs = re.split(r'\n\s*\n', content.strip())
    raw_paragraphs = [p.strip() for p in raw_paragraphs if p.strip()]
    
    # Now merge headers with their following content
    merged_paragraphs = []
    i = 0
    while i < len(raw_paragraphs):
        current = raw_paragraphs[i]
        
        # If this is a header and there's a next paragraph
        if current.strip().startswith('#') and i + 1 < len(raw_paragraphs):
            next_para = raw_paragraphs[i + 1]
            # Merge header with next paragraph unless next is also a header
            if not next_para.strip().startswith('#'):
                merged = current + '\n\n' + next_para
                merged_paragraphs.append(merged)
                i += 2  # Skip both paragraphs
                continue
        
        merged_paragraphs.append(current)
        i += 1
    
    return merged_paragraphs

def calculate_safe_input_tokens(context_length: int) -> int:
    """Calculate safe input token count - adaptive based on context length"""
    prompt_overhead = 1000     # Reserve tokens for prompt
    
    # Adaptive output reserve based on context length
    if context_length <= 4096:
        max_output_tokens = context_length * 0.3  # 30% for output
        input_ratio = 0.5  # Use 50% of remaining for input
    elif context_length <= 8192:
        max_output_tokens = context_length * 0.4  # 40% for output
        input_ratio = 0.4  # Use 40% of remaining for input
    else:
        max_output_tokens = 8192   # Cap at 8192 for large contexts
        input_ratio = 0.4  # Use 40% of remaining for input
    
    remaining = context_length - max_output_tokens - prompt_overhead
    
    # Ensure we have at least some tokens for input
    if remaining <= 0:
        # Fallback for very small context lengths
        return max(512, int(context_length * 0.3))
    
    return int(remaining * input_ratio)

def split_lines_preserving_structure(lines: list, max_tokens: int) -> list:
    """Split lines while preserving markdown structure like headers"""
    chunks = []
    current_chunk = []
    current_tokens = 0
    
    i = 0
    while i < len(lines):
        line = lines[i]
        line_tokens = count_tokens(line + '\n')
        
        # Check if this is a markdown header
        is_header = line.strip().startswith('#') and line.strip() != ''
        
        if is_header:
            # For headers, try to include some content after it
            header_chunk = [line]
            header_tokens = line_tokens
            
            # Look ahead to include content after header
            j = i + 1
            while j < len(lines) and header_tokens < max_tokens * 0.8:  # Use 80% to be safe
                next_line = lines[j]
                next_tokens = count_tokens(next_line + '\n')
                
                # Stop if we hit another header or exceed token limit
                if next_line.strip().startswith('#') and next_line.strip() != '':
                    break
                if header_tokens + next_tokens > max_tokens * 0.8:
                    break
                
                header_chunk.append(next_line)
                header_tokens += next_tokens
                j += 1
            
            # Finalize current chunk if it exists
            if current_chunk:
                chunks.append('\n'.join(current_chunk))
                current_chunk = []
                current_tokens = 0
            
            # Add header chunk
            chunks.append('\n'.join(header_chunk))
            i = j  # Skip the lines we've already included
            continue
        
        # Regular line processing
        if current_tokens + line_tokens <= max_tokens:
            current_chunk.append(line)
            current_tokens += line_tokens
        else:
            # Finalize current chunk
            if current_chunk:
                chunks.append('\n'.join(current_chunk))
            current_chunk = [line]
            current_tokens = line_tokens
        
        i += 1
    
    # Add final chunk
    if current_chunk:
        chunks.append('\n'.join(current_chunk))
    
    return chunks

def split_large_paragraph_recursively(paragraph: str, max_tokens: int) -> list:
    """Recursively split large paragraph into smaller chunks - preserves headers"""
    para_tokens = count_tokens(paragraph)
    
    if para_tokens <= max_tokens:
        return [paragraph]
    
    # Special handling for markdown sections - preserve headers with their content
    lines = paragraph.split('\n')
    if len(lines) > 1:
        return split_lines_preserving_structure(lines, max_tokens)
    
    # Try splitting by sentences first (Korean and English)
    sentence_patterns = [r'[.!?]\s+', r'[。！？]\s*']
    for pattern in sentence_patterns:
        sentences = re.split(pattern, paragraph)
        if len(sentences) > 1:
            # Reconstruct sentences with proper endings
            reconstructed = []
            for i, sentence in enumerate(sentences[:-1]):
                match = re.search(pattern, paragraph[len(''.join(sentences[:i+1])):])
                if match:
                    reconstructed.append(sentence + match.group().strip())
                else:
                    reconstructed.append(sentence)
            if sentences[-1]:  # Add last sentence if not empty
                reconstructed.append(sentences[-1])
            
            # Group sentences within token limit
            return group_text_chunks_by_tokens(reconstructed, max_tokens)
    
    # Last resort: split by half
    mid = len(paragraph) // 2
    return split_large_paragraph_recursively(paragraph[:mid], max_tokens) + \
           split_large_paragraph_recursively(paragraph[mid:], max_tokens)

def group_text_chunks_by_tokens(chunks: list, max_tokens: int, separator: str = '\n\n') -> list:
    """Group text chunks within token limits with strict validation"""
    groups = []
    current_group = []
    current_tokens = 0
    separator_tokens = count_tokens(separator)
    
    for chunk in chunks:
        chunk_tokens = count_tokens(chunk)
        
        # If single chunk exceeds limit, split it further
        if chunk_tokens > max_tokens:
            # Finalize current group first
            if current_group:
                groups.append(separator.join(current_group))
                current_group = []
                current_tokens = 0
            
            # Split the large chunk by more aggressive means
            if separator == '\n':
                # Already splitting by lines, so split by chars
                lines = chunk.split('\n')
                temp_group = []
                temp_tokens = 0
                
                for line in lines:
                    line_tokens = count_tokens(line)
                    if temp_tokens + line_tokens + 1 <= max_tokens:
                        temp_group.append(line)
                        temp_tokens += line_tokens + 1
                    else:
                        if temp_group:
                            groups.append('\n'.join(temp_group))
                        # If single line is still too big, split by characters
                        if line_tokens > max_tokens:
                            char_chunks = split_text_by_chars(line, max_tokens)
                            groups.extend(char_chunks)
                        else:
                            temp_group = [line]
                            temp_tokens = line_tokens
                
                if temp_group:
                    groups.append('\n'.join(temp_group))
            else:
                # Split by characters
                char_chunks = split_text_by_chars(chunk, max_tokens)
                groups.extend(char_chunks)
            continue
        
        # Check if we can add to current group
        needed_tokens = current_tokens + chunk_tokens + (separator_tokens if current_group else 0)
        
        if needed_tokens <= max_tokens:
            current_group.append(chunk)
            current_tokens = needed_tokens
        else:
            # Finalize current group and start new one
            if current_group:
                final_group = separator.join(current_group)
                # Double check the final group doesn't exceed limits
                if count_tokens(final_group) <= max_tokens:
                    groups.append(final_group)
                else:
                    # This shouldn't happen, but safety check
                    groups.extend(split_text_by_chars(final_group, max_tokens))
            current_group = [chunk]
            current_tokens = chunk_tokens
    
    # Add final group
    if current_group:
        final_group = separator.join(current_group)
        if count_tokens(final_group) <= max_tokens:
            groups.append(final_group)
        else:
            groups.extend(split_text_by_chars(final_group, max_tokens))
    
    return groups

def split_text_by_chars(text: str, max_tokens: int) -> list:
    """Split text by character count estimation"""
    if count_tokens(text) <= max_tokens:
        return [text]
    
    # Estimate chars per token
    chars_per_token = len(text) / count_tokens(text)
    target_chars = int(max_tokens * chars_per_token * 0.8)  # Safety margin
    
    chunks = []
    start = 0
    
    while start < len(text):
        end = min(start + target_chars, len(text))
        
        # Try to break at word/line boundary within 50 chars
        if end < len(text):
            for i in range(end, max(start + 1, end - 50), -1):
                if text[i] in ' \n\t':
                    end = i
                    break
        
        chunk = text[start:end].strip()
        if chunk:
            # Verify chunk is within token limit
            if count_tokens(chunk) <= max_tokens:
                chunks.append(chunk)
            else:
                # Recursive split if still too large
                chunks.extend(split_text_by_chars(chunk, max_tokens))
        
        start = end
        # Skip whitespace
        while start < len(text) and text[start] in ' \t':
            start += 1
    
    return chunks

def save_debug_chunks(input_path: str, chunks: list, debug_dir: str = "debug_chunks"):
    """Save chunks to debug files for inspection"""
    import os
    from pathlib import Path
    
    # Create debug directory
    debug_path = Path(debug_dir)
    debug_path.mkdir(exist_ok=True)
    
    # Get base filename
    base_name = Path(input_path).stem
    
    # Save each chunk as a separate file
    for i, chunk in enumerate(chunks):
        chunk_file = debug_path / f"{base_name}_chunk_{i+1:03d}.md"
        
        # Add chunk metadata header
        metadata = f"""<!-- DEBUG CHUNK {i+1}/{len(chunks)} -->
<!-- Tokens: {count_tokens(chunk)} -->
<!-- Characters: {len(chunk)} -->
<!-- Source: {input_path} -->

---

"""
        
        with open(chunk_file, 'w', encoding='utf-8') as f:
            f.write(metadata + chunk)
    
    # Save summary file
    summary_file = debug_path / f"{base_name}_summary.md"
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write(f"# Chunking Debug Summary\n\n")
        f.write(f"**Source:** {input_path}\n")
        f.write(f"**Total Chunks:** {len(chunks)}\n")
        f.write(f"**Total Characters:** {sum(len(chunk) for chunk in chunks)}\n")
        f.write(f"**Total Tokens:** {sum(count_tokens(chunk) for chunk in chunks)}\n\n")
        
        f.write("## Chunk Details\n\n")
        f.write("| Chunk | Tokens | Characters | Preview |\n")
        f.write("|-------|--------|------------|----------|\n")
        
        for i, chunk in enumerate(chunks):
            preview = chunk[:50].replace('\n', ' ').replace('|', '\\|')
            if len(chunk) > 50:
                preview += "..."
            f.write(f"| {i+1:03d} | {count_tokens(chunk)} | {len(chunk)} | {preview} |\n")
    
    print(f"🐛 Debug files saved to: {debug_path}/", flush=True)
    print(f"   📁 {len(chunks)} chunk files + 1 summary file", flush=True)

def group_paragraphs_by_tokens(paragraphs: list, safe_tokens: int) -> list:
    """Group paragraphs by token limits with aggressive splitting - maintains order"""
    print(f"🔧 Starting chunking process:", flush=True)
    print(f"   📊 Input: {len(paragraphs)} paragraphs", flush=True)
    print(f"   🎯 Target: {safe_tokens} tokens per chunk", flush=True)
    
    # Process paragraphs in order, splitting large ones as needed
    all_chunks = []
    large_para_count = 0
    
    for i, paragraph in enumerate(paragraphs):
        para_tokens = count_tokens(paragraph)
        
        if para_tokens > safe_tokens:
            large_para_count += 1
            print(f"   📄 Paragraph {i+1}: {para_tokens} tokens → splitting recursively", flush=True)
            # Split large paragraph recursively
            sub_chunks = split_large_paragraph_recursively(paragraph, safe_tokens)
            print(f"      ↳ Split into {len(sub_chunks)} sub-chunks", flush=True)
            for j, sub in enumerate(sub_chunks):
                print(f"         └─ Sub-chunk {j+1}: {count_tokens(sub)} tokens ({len(sub)} chars)", flush=True)
            # Add sub-chunks in order
            all_chunks.extend(sub_chunks)
        else:
            # Add regular paragraph
            all_chunks.append(paragraph)
    
    print(f"   🔨 Split {large_para_count} large paragraphs → {len(all_chunks)} total chunks", flush=True)
    
    # Second pass: group consecutive chunks together within token limits
    print(f"   🔗 Regrouping {len(all_chunks)} chunks within token limits...", flush=True)
    final_chunks = group_consecutive_chunks_by_tokens(all_chunks, safe_tokens)
    
    print(f"   ✅ Final result: {len(final_chunks)} optimized chunks", flush=True)
    
    return final_chunks

def group_consecutive_chunks_by_tokens(chunks: list, max_tokens: int) -> list:
    """Group consecutive chunks within token limits - preserves order"""
    groups = []
    current_group = []
    current_tokens = 0
    separator_tokens = count_tokens('\n\n')
    
    for i, chunk in enumerate(chunks):
        chunk_tokens = count_tokens(chunk)
        
        # If single chunk exceeds limit, add it as-is (already split as much as possible)
        if chunk_tokens > max_tokens:
            # Finalize current group first
            if current_group:
                groups.append('\n\n'.join(current_group))
                current_group = []
                current_tokens = 0
            # Add the large chunk directly (it's been split as much as possible)
            groups.append(chunk)
            continue
        
        # Calculate tokens needed to add this chunk
        needed_tokens = current_tokens + chunk_tokens + (separator_tokens if current_group else 0)
        
        if needed_tokens <= max_tokens:
            # Add to current group
            current_group.append(chunk)
            current_tokens = needed_tokens
        else:
            # Finalize current group and start new one
            if current_group:
                groups.append('\n\n'.join(current_group))
            current_group = [chunk]
            current_tokens = chunk_tokens
    
    # Add final group
    if current_group:
        groups.append('\n\n'.join(current_group))
    
    return groups

def process_markdown_file(input_path, output_path):
    """Process a single markdown file"""
    print(f"\n📝 Starting translation: {input_path} -> {output_path}", flush=True)
    
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if CONTEXT_LENGTH > 0:
            # Use accurate token-based chunking
            safe_tokens = calculate_safe_input_tokens(CONTEXT_LENGTH)
            total_tokens = count_tokens(content)
            
            print(f"📊 File analysis: {len(content)} chars, ~{total_tokens} tokens (limit: {safe_tokens})", flush=True)
            
            if total_tokens > safe_tokens:
                # Split content by paragraphs and group by token limits
                paragraphs = split_markdown_by_paragraphs(content)
                print(f"📄 Found {len(paragraphs)} paragraphs", flush=True)
                
                # Group paragraphs by token limits
                chunks = group_paragraphs_by_tokens(paragraphs, safe_tokens)
                total_chunks = len(chunks)
                
                print(f"📦 Created {total_chunks} token-aware chunks:", flush=True)
                for i, chunk in enumerate(chunks):
                    tokens = count_tokens(chunk)
                    print(f"   Chunk {i+1}: {tokens} tokens ({len(chunk)} chars)", flush=True)
                
                # Save debug files for inspection
                save_debug_chunks(input_path, chunks)
                
                translated_chunks = []
                
                for i, chunk in enumerate(chunks):
                    chunk_tokens = count_tokens(chunk)
                    print(f"🔄 [{i+1}/{total_chunks}] Translating chunk ({chunk_tokens} tokens)...", end='', flush=True)
                    
                    # All chunks should now be within safe limits due to aggressive splitting
                    if chunk_tokens > safe_tokens * 1.2:  # 20% tolerance
                        print(f" ⚠️ Chunk still too large ({chunk_tokens} tokens), using original", flush=True)
                        translated_chunks.append(chunk)  # Keep original content
                        continue
                    
                    translated_chunk = translate_with_ollama(chunk)
                    if translated_chunk:
                        translated_chunks.append(translated_chunk)
                        print(f" ✅ Done ({len(translated_chunk)} chars)", flush=True)
                    else:
                        print(f" ⚠️ Empty result, using original", flush=True)
                        translated_chunks.append(chunk)  # Fallback to original
                    time.sleep(1.0)  # Longer delay between requests
                
                print(f"📝 Joining {len(translated_chunks)} translated chunks...", flush=True)
                translated_content = '\n\n'.join(translated_chunks)
            else:
                # File is small enough, process as single chunk
                print(f"📄 Processing entire file as one chunk ({total_tokens} tokens, limit: {safe_tokens})...", flush=True)
                translated_content = translate_with_ollama(content)
        else:
            # No context length limit, process entire file
            print(f"📄 Processing entire file as one chunk (no context limit)...", flush=True)
            translated_content = translate_with_ollama(content)
        
        # Create output directory
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Add AI translation notice at the bottom
        ai_notice = "\n\n---\n\n> **⚠️ 이 문서는 AI로 번역된 문서입니다.**\n>\n> **⚠️ This document has been translated by AI.**"
        
        # Write translated content with AI notice at the bottom
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(translated_content + ai_notice)
        
        print(f"🎉 Translation completed: {output_path}\n", flush=True)
        return True
    except Exception as e:
        print(f"❌ Failed to process {input_path}: {str(e)}", flush=True)
        return False

def create_pull_request(translated_files=None):
    """Create a pull request with the changes"""
    if not GITHUB_TOKEN:
        log("No GitHub token provided, skipping PR creation")
        return None, None
    
    try:
        # Configure git
        subprocess.run(['git', 'config', 'user.name', 'github-actions[bot]'], 
                      capture_output=True)
        subprocess.run(['git', 'config', 'user.email', 
                       'github-actions[bot]@users.noreply.github.com'], 
                      capture_output=True)
        
        # Add only the translated files if specified, otherwise add all changes in target dir
        if translated_files:
            log(f"Adding {len(translated_files)} translated files to git")
            for file_path in translated_files:
                log(f"Adding: {file_path}")
                subprocess.run(['git', 'add', file_path], capture_output=True)
        else:
            # Fallback to adding entire target directory
            log(f"Adding all changes in {TARGET_DIR}")
            subprocess.run(['git', 'add', TARGET_DIR], capture_output=True)
        
        # Check if there are staged changes
        result = subprocess.run(['git', 'diff', '--cached', '--name-only'], 
                              capture_output=True, text=True)
        
        if not result.stdout.strip():
            log("No staged changes to commit")
            return None, None
        
        staged_files = result.stdout.strip().split('\n')
        log(f"Staged files for commit: {staged_files}")
        
        # Create branch
        branch_name = f"{PR_BRANCH}-{int(time.time())}"
        subprocess.run(['git', 'checkout', '-b', branch_name], capture_output=True)
        
        # Commit changes
        subprocess.run(['git', 'commit', '-m', COMMIT_MESSAGE], capture_output=True)
        
        # Get remote URL and extract repo info
        remote_result = subprocess.run(['git', 'remote', 'get-url', 'origin'], 
                                     capture_output=True, text=True)
        if remote_result.returncode != 0:
            log("Failed to get remote URL")
            return None, None
        
        remote_url = remote_result.stdout.strip()
        
        # Extract owner/repo from URL and determine GitHub instance
        github_host = "github.com"
        
        if remote_url.startswith('git@'):
            # SSH format: git@github.com:owner/repo.git or git@enterprise.com:owner/repo.git
            host_and_path = remote_url.split('@')[1]
            github_host = host_and_path.split(':')[0]
            repo_part = host_and_path.split(':')[1].replace('.git', '')
        else:
            # HTTPS format: https://github.com/owner/repo.git or https://enterprise.com/owner/repo.git
            if '//' in remote_url:
                url_parts = remote_url.split('//')
                if len(url_parts) > 1:
                    host_and_path = url_parts[1]
                    path_parts = host_and_path.split('/', 1)
                    if len(path_parts) > 1:
                        github_host = path_parts[0]
                        repo_part = path_parts[1].replace('.git', '')
                    else:
                        log("Invalid repository URL format")
                        return None, None
                else:
                    log("Invalid repository URL format")
                    return None, None
            else:
                log("Invalid repository URL format")
                return None, None
        
        if '/' not in repo_part:
            log("Could not extract owner/repo from URL")
            return None, None
            
        owner, repo = repo_part.split('/', 1)
        
        # Push branch using token authentication
        push_url = f"https://x-access-token:{GITHUB_TOKEN}@{github_host}/{owner}/{repo}.git"
        push_result = subprocess.run(['git', 'push', push_url, branch_name], 
                                   capture_output=True, text=True)
        
        if push_result.returncode != 0:
            log(f"Failed to push branch: {push_result.stderr}")
            # Try to use existing remote
            subprocess.run(['git', 'push', 'origin', branch_name], 
                         capture_output=True, text=True)
        
        # Determine API URL based on GitHub instance
        if GITHUB_API_URL != 'https://api.github.com':
            # Use provided API URL (for GitHub Enterprise)
            api_base_url = GITHUB_API_URL.rstrip('/')
        elif github_host != 'github.com':
            # Automatically construct Enterprise API URL
            api_base_url = f"https://{github_host}/api/v3"
        else:
            # Default GitHub.com
            api_base_url = "https://api.github.com"
        
        log(f"Using API URL: {api_base_url}")
        
        # Create PR using GitHub API
        pr_body = f"""## 📝 Documentation Translation Update

This PR contains automatically generated English translations of Korean documentation files.

### Changes
- Translated Korean markdown files from `{SOURCE_DIR}/` to `{TARGET_DIR}/`
- Used {MODEL} model for translation

### Files Changed
{chr(10).join(f'- `{file}`' for file in staged_files)}

### Translation Settings
- Model: {MODEL}
- Temperature: {TEMPERATURE}
- Source: {SOURCE_DIR}
- Target: {TARGET_DIR}

Please review the translations for accuracy and merge if they look good.

---
🤖 This PR was automatically generated by the Ollama Korean to English Translator action."""
        
        # Create PR via GitHub API
        api_url = f"{api_base_url}/repos/{owner}/{repo}/pulls"
        pr_data = {
            "title": PR_TITLE,
            "body": pr_body,
            "head": branch_name,
            "base": BASE_BRANCH
        }
        
        headers = {
            "Authorization": f"token {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        try:
            log(f"Creating PR with base branch: {BASE_BRANCH}")
            response = requests.post(api_url, json=pr_data, headers=headers, verify=SSL_VERIFY)
            if response.status_code == 201:
                pr_info = response.json()
                pr_url = pr_info['html_url']
                pr_number = str(pr_info['number'])
                success(f"Pull request created: {pr_url}")
                return pr_url, pr_number
            else:
                log(f"Failed to create PR via API: {response.status_code}")
                log(f"Response: {response.text}")
                
                # If specified base branch failed, try common alternatives
                if BASE_BRANCH not in ['main', 'master']:
                    for fallback_branch in ['main', 'master']:
                        log(f"Retrying with base branch: {fallback_branch}")
                        pr_data["base"] = fallback_branch
                        response = requests.post(api_url, json=pr_data, headers=headers, verify=SSL_VERIFY)
                        if response.status_code == 201:
                            pr_info = response.json()
                            pr_url = pr_info['html_url']
                            pr_number = str(pr_info['number'])
                            success(f"Pull request created with fallback branch: {pr_url}")
                            return pr_url, pr_number
                
                return None, None
        except Exception as e:
            log(f"Failed to create PR via API: {str(e)}")
            return None, None
        
    except Exception as e:
        log(f"Failed to create pull request: {str(e)}")
        return None, None

def main():
    """Main execution function"""
    log("Starting Ollama Korean to English Translator")
    
    # Validate inputs
    if not os.path.exists(SOURCE_DIR):
        error(f"Source directory '{SOURCE_DIR}' does not exist")
    
    # Check Ollama server
    log(f"Checking Ollama server at {OLLAMA_URL}")
    if not check_ollama_server():
        error(f"Ollama server is not running at {OLLAMA_URL}")
    
    success("Ollama server is running")
    
    # Check model availability
    log(f"Checking model: {MODEL}")
    if not check_model_available():
        log(f"Model {MODEL} not found, attempting to pull...")
        if not pull_model():
            error(f"Failed to pull model {MODEL}")
    
    success(f"Model {MODEL} is available")
    
    # Find markdown files
    source_path = Path(SOURCE_DIR)
    target_path = Path(TARGET_DIR)
    
    pattern = source_path / FILE_PATTERN
    md_files = list(source_path.rglob('*.md'))
    
    if not md_files:
        log(f"No markdown files found in {SOURCE_DIR}")
        set_output('translated-files', '0')
        set_output('skipped-files', '0')
        return
    
    print(f"📋 Found {len(md_files)} markdown files to process\n", flush=True)
    
    translated_count = 0
    skipped_count = 0
    translated_files = []  # Keep track of translated files
    
    # Process each file
    for file_index, md_file in enumerate(md_files, 1):
        rel_path = md_file.relative_to(source_path)
        output_file = target_path / rel_path
        
        print(f"📄 [{file_index}/{len(md_files)}] Processing: {md_file}", flush=True)
        
        # Skip if file exists and is newer
        if (SKIP_EXISTING and output_file.exists() and 
            output_file.stat().st_mtime > md_file.stat().st_mtime):
            print(f"⏭️  Skipping {md_file} (translation is up to date)\n", flush=True)
            skipped_count += 1
            continue
        
        if process_markdown_file(md_file, output_file):
            translated_count += 1
            translated_files.append(str(output_file))  # Add to translated files list
            print(f"✅ [{file_index}/{len(md_files)}] Successfully translated: {output_file}", flush=True)
        else:
            skipped_count += 1
            print(f"❌ [{file_index}/{len(md_files)}] Failed to translate: {md_file}", flush=True)
        
        # Show overall progress
        print(f"📈 Progress: {file_index}/{len(md_files)} files processed, {translated_count} translated, {skipped_count} skipped\n", flush=True)
    
    print(f"🎯 Final Summary: {translated_count} files translated, {skipped_count} files skipped", flush=True)
    
    # Set outputs
    set_output('translated-files', str(translated_count))
    set_output('skipped-files', str(skipped_count))
    
    # Output translated files list for artifact upload (use space-separated for better compatibility)
    if translated_files:
        # Convert to relative paths and join with spaces
        relative_files = []
        for file_path in translated_files:
            try:
                rel_path = os.path.relpath(file_path)
                relative_files.append(rel_path)
            except:
                relative_files.append(file_path)
        set_output('translated-files-list', ' '.join(relative_files))
    else:
        set_output('translated-files-list', '')
    
    # Create PR if requested and there are changes
    if CREATE_PR and translated_count > 0:
        pr_url, pr_number = create_pull_request(translated_files)
        if pr_url:
            set_output('pr-url', pr_url)
            set_output('pr-number', pr_number)
    elif translated_count > 0:
        log(f"PR creation disabled. {translated_count} files translated and ready for artifact upload.")

if __name__ == "__main__":
    main()