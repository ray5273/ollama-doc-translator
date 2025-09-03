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
import re
from pathlib import Path
import subprocess

try:
    import tiktoken
    _ENCODING = tiktoken.get_encoding("cl100k_base")
except Exception:
    _ENCODING = None


def count_tokens(text: str) -> int:
    """Return token count using tiktoken if available."""
    if _ENCODING is not None:
        return len(_ENCODING.encode(text))
    # Fallback rough estimate
    return len(text) // 3

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

def translate_with_ollama(text, retries=0, context_history=None):
    """Translate text using Ollama API with retry logic and context awareness"""
    if retries >= MAX_RETRIES:
        print(f"⚠️  Max retries ({MAX_RETRIES}) reached, returning original text", flush=True)
        return text

    # Build context-aware prompt with previous translations
    context_section = ""
    if context_history:
        # Calculate available tokens for context (reserve space for current text and prompt)
        prompt_base_tokens = 800  # Base prompt template size
        current_text_tokens = count_tokens(text)
        output_reserve_tokens = int(current_text_tokens * 1.5)  # Reserve space for translation output

        available_context_tokens = CONTEXT_LENGTH - prompt_base_tokens - current_text_tokens - output_reserve_tokens
        
        if available_context_tokens > 200:  # Minimum viable context
            context_text = build_context_from_history(context_history, available_context_tokens)
            if context_text:
                context_section = f"""\n### Previous Translation Context\nTo maintain consistency, here are recent translations from this document:\n{context_text}\n"""

    prompt = f"""Please translate the following Korean markdown document into English. Strictly follow these instructions:

- Do not change the markdown format and structure.
- **Never translate or modify code blocks (including language tags like ```python), inline code (`...`), links, URLs, image paths, mathematical formulas, Mermaid diagrams, and HTML comments.**
- Maintain the structure and indentation of lists, tables, and YAML frontmatter.
- If the input is already in English or contains no Korean, return the input as is.
- Translate the same terms consistently throughout the document.
- Do not output unnecessary additional explanations, comments, or phrases like "Here is the translation:".
- If a sentence is cut off, translate it faithfully up to the cut-off point without unnecessary speculation.{context_section}

Korean markdown document to translate:
{text}

English markdown document:"""

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

        if translated.startswith('English markdown document:'):
            translated = translated.replace('English markdown document:', '').strip()

        return translated
    except Exception as e:
        print(f"⚠️  Translation error (attempt {retries + 1}): {e}", flush=True)
        time.sleep(2 ** retries)  # Exponential backoff
        return translate_with_ollama(text, retries + 1, context_history)

def build_context_from_history(context_history, max_tokens):
    """Build context string from previous translations within token limit"""
    if not context_history:
        return None
    
    context_pairs = []
    current_tokens = 0
    max_char_estimate = max_tokens * 3  # Rough estimation: 1 token ≈ 3-4 chars for Korean/English
    
    # Start from most recent translations and work backwards
    for korean, english in reversed(context_history[-10:]):  # Use last 10 pairs max
        # Create context pair with limited length
        korean_snippet = korean[:200] + "..." if len(korean) > 200 else korean
        english_snippet = english[:200] + "..." if len(english) > 200 else english
        
        pair_text = f"Korean: {korean_snippet}\nEnglish: {english_snippet}"
        pair_length = len(pair_text)
        
        if current_tokens + pair_length > max_char_estimate:
            break
            
        context_pairs.insert(0, pair_text)
        current_tokens += pair_length
    
    if not context_pairs:
        return None

    return "\n\n".join(context_pairs)


def split_markdown_into_chunks(text, max_tokens):
    """Split markdown text into chunks by paragraph respecting token limits."""
    paragraphs = text.split("\n\n")
    chunks = []
    current = []
    current_tokens = 0

    for para in paragraphs:
        tokens = count_tokens(para) + 1  # account for joining newline
        if current and current_tokens + tokens > max_tokens:
            chunks.append("\n\n".join(current).strip())
            current = [para]
            current_tokens = tokens
        else:
            current.append(para)
            current_tokens += tokens

    if current:
        chunks.append("\n\n".join(current).strip())

    return chunks

def process_markdown_file(input_path, output_path):
    """Process a single markdown file with token-aware chunks"""
    print(f"\n📝 Starting translation: {input_path} -> {output_path}", flush=True)

    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Initialize context history for this file
        context_history = []
        
        if CONTEXT_LENGTH <= 0:
            print("📄 Processing entire file as one chunk (no context limit)...", flush=True)
            translated_content = translate_with_ollama(content, context_history=context_history)
        else:
            # Calculate safe input tokens considering prompt and output
            prompt_overhead = 1024
            output_reserve_ratio = 3.0
            safe_input_tokens = int((CONTEXT_LENGTH - prompt_overhead) / output_reserve_ratio)

            if CONTEXT_LENGTH <= 4096:
                safe_input_tokens = 800
            elif CONTEXT_LENGTH <= 8192:
                safe_input_tokens = 1800
            elif CONTEXT_LENGTH <= 16384:
                safe_input_tokens = 4000
            elif CONTEXT_LENGTH <= 32768:
                safe_input_tokens = 8000
            elif CONTEXT_LENGTH <= 65536:
                safe_input_tokens = 20000
            else:
                safe_input_tokens = min(safe_input_tokens, 25000)

            content_tokens = count_tokens(content)

            if content_tokens <= safe_input_tokens:
                print(
                    f"📄 Processing entire file as one chunk (tokens: {content_tokens}, safe limit: {safe_input_tokens})...",
                    flush=True,
                )
                translated_content = translate_with_ollama(content, context_history=context_history)
            else:
                chunks = split_markdown_into_chunks(content, safe_input_tokens)
                translated_chunks = []
                total_chunks = len(chunks)

                print(
                    f"📊 Processing {total_chunks} chunks (safe input: {safe_input_tokens}, context: {CONTEXT_LENGTH})...",
                    flush=True,
                )

                for i, chunk in enumerate(chunks):
                    print(
                        f"🔄 [{i+1}/{total_chunks}] Processing chunk (tokens: {count_tokens(chunk)})...",
                        end="",
                        flush=True,
                    )

                    translated_chunk = translate_with_ollama(chunk, context_history=context_history)
                    translated_chunks.append(translated_chunk)

                    chunk_lines = chunk.strip().split("\n")
                    translated_lines = translated_chunk.strip().split("\n")

                    for orig_line, trans_line in zip(chunk_lines[:10], translated_lines[:10]):
                        if orig_line.strip() and trans_line.strip() and re.search(r"[가-힣]", orig_line):
                            context_history.append((orig_line.strip(), trans_line.strip()))

                    if len(context_history) > 20:
                        context_history = context_history[-20:]

                    print(
                        f" ✅ Done (result tokens: {count_tokens(translated_chunk)}, context pairs: {len(context_history)})",
                        flush=True,
                    )
                    time.sleep(0.5)

                print(f"📝 Joining {len(translated_chunks)} translated chunks...", flush=True)
                translated_content = "\n\n".join(translated_chunks)


        output_path.parent.mkdir(parents=True, exist_ok=True)
        ai_notice = "\n\n---\n\n> **⚠️ 이 문서는 AI로 번역된 문서입니다.**\n>\n> **⚠️ This document has been translated by AI.**"

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
    
    md_files = list(source_path.glob(FILE_PATTERN))
    
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