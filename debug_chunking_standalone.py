#!/usr/bin/env python3
"""
Standalone Chunking Debugger
스마트 분할 과정을 독립적으로 테스트하고 시각화하는 도구
"""

import os
import sys
import re
from pathlib import Path

try:
    import tiktoken
    TIKTOKEN_AVAILABLE = True
except ImportError:
    TIKTOKEN_AVAILABLE = False

def count_tokens(text: str) -> int:
    """Count tokens accurately using tiktoken or improved approximation"""
    if TIKTOKEN_AVAILABLE:
        try:
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

def split_lines_preserving_structure(text: str, max_tokens: int) -> list:
    """Split text by lines while preserving markdown headers with their content"""
    lines = text.split('\n')
    groups = []
    current_group = []
    current_tokens = 0
    
    i = 0
    while i < len(lines):
        line = lines[i]
        line_tokens = count_tokens(line + '\n')
        
        # Check if this is a markdown header
        if line.strip().startswith('#'):
            # If we have a current group and adding this header would exceed limit
            if current_group and current_tokens + line_tokens > max_tokens:
                groups.append('\n'.join(current_group))
                current_group = []
                current_tokens = 0
            
            # Start new group with header
            header_group = [line]
            header_tokens = line_tokens
            
            # Try to include following content up to 80% of max_tokens
            j = i + 1
            while j < len(lines) and header_tokens < max_tokens * 0.8:
                next_line = lines[j]
                # Stop if we hit another header
                if next_line.strip().startswith('#'):
                    break
                next_tokens = count_tokens(next_line + '\n')
                if header_tokens + next_tokens > max_tokens * 0.8:
                    break
                header_group.append(next_line)
                header_tokens += next_tokens
                j += 1
            
            # Add the header group
            if current_group:
                groups.append('\n'.join(current_group))
                current_group = []
                current_tokens = 0
            
            groups.append('\n'.join(header_group))
            i = j  # Skip processed lines
            continue
        
        # Regular line processing
        if current_tokens + line_tokens <= max_tokens:
            current_group.append(line)
            current_tokens += line_tokens
        else:
            if current_group:
                groups.append('\n'.join(current_group))
            current_group = [line]
            current_tokens = line_tokens
        
        i += 1
    
    # Add remaining group
    if current_group:
        groups.append('\n'.join(current_group))
    
    return groups

def split_large_paragraph_recursively(paragraph: str, max_tokens: int) -> list:
    """Recursively split large paragraph into smaller chunks"""
    para_tokens = count_tokens(paragraph)
    
    if para_tokens <= max_tokens:
        return [paragraph]
    
    # First try structure-preserving split for markdown
    if '#' in paragraph:
        structure_chunks = split_lines_preserving_structure(paragraph, max_tokens)
        if len(structure_chunks) > 1:
            return structure_chunks
    
    # Try splitting by sentences first (Korean and English)
    sentence_patterns = [r'[.!?]\s+', r'[。！？]\s*']
    for pattern in sentence_patterns:
        sentences = re.split(pattern, paragraph)
        if len(sentences) > 1:
            reconstructed = []
            for i, sentence in enumerate(sentences[:-1]):
                match = re.search(pattern, paragraph[len(''.join(sentences[:i+1])):])
                if match:
                    reconstructed.append(sentence + match.group().strip())
                else:
                    reconstructed.append(sentence)
            if sentences[-1]:
                reconstructed.append(sentences[-1])
            
            return group_text_chunks_by_tokens(reconstructed, max_tokens)
    
    # Fall back to line splitting with structure preservation
    lines = paragraph.split('\n')
    if len(lines) > 1:
        return split_lines_preserving_structure(paragraph, max_tokens)
    
    # Last resort: split by half
    mid = len(paragraph) // 2
    return split_large_paragraph_recursively(paragraph[:mid], max_tokens) + \
           split_large_paragraph_recursively(paragraph[mid:], max_tokens)

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

def analyze_chunking_process(file_path: str, target_tokens: int = 9400):
    """Analyze and visualize the chunking process step by step"""
    print(f"🔍 Analyzing chunking process for: {file_path}")
    print(f"🎯 Target tokens per chunk: {target_tokens}")
    print("=" * 80)
    
    # Read file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"📖 Original file: {len(content)} chars, ~{count_tokens(content)} tokens")
    
    # Split by paragraphs
    paragraphs = split_markdown_by_paragraphs(content)
    print(f"📄 Split into {len(paragraphs)} paragraphs")
    
    # Analyze each paragraph
    large_paragraphs = []
    small_paragraphs = []
    
    for i, para in enumerate(paragraphs):
        tokens = count_tokens(para)
        if tokens > target_tokens:
            large_paragraphs.append((i, para, tokens))
            print(f"   📄 Paragraph {i+1}: {tokens} tokens (LARGE - needs splitting)")
        else:
            small_paragraphs.append((i, para, tokens))
    
    print(f"\n🔨 Analysis: {len(large_paragraphs)} large paragraphs need splitting")
    print(f"✅ {len(small_paragraphs)} paragraphs are already suitable")
    
    # Process all paragraphs in original order
    all_chunks = []
    split_details = []
    
    for i, paragraph in enumerate(paragraphs):
        para_tokens = count_tokens(paragraph)
        
        if para_tokens > target_tokens:
            print(f"\n🔧 Splitting paragraph {i+1} ({para_tokens} tokens):")
            sub_chunks = split_large_paragraph_recursively(paragraph, target_tokens)
            split_details.append({
                'original_para': i+1,
                'original_tokens': para_tokens,
                'sub_chunks': len(sub_chunks),
                'chunks': sub_chunks
            })
            
            for j, sub in enumerate(sub_chunks):
                sub_tokens = count_tokens(sub)
                print(f"   └─ Sub-chunk {j+1}: {sub_tokens} tokens ({len(sub)} chars)")
            all_chunks.extend(sub_chunks)
        else:
            all_chunks.append(paragraph)
    
    print(f"\n🔗 Regrouping {len(all_chunks)} chunks...")
    final_chunks = group_consecutive_chunks_by_tokens(all_chunks, target_tokens)
    
    print(f"✅ Final result: {len(final_chunks)} optimized chunks")
    
    # Save debug files
    base_name = Path(file_path).stem
    debug_dir = Path("debug_chunks_analysis")
    debug_dir.mkdir(exist_ok=True)
    
    # Save detailed analysis
    analysis_file = debug_dir / f"{base_name}_analysis.md"
    with open(analysis_file, 'w', encoding='utf-8') as f:
        f.write(f"# Chunking Analysis Report\n\n")
        f.write(f"**File:** {file_path}\n")
        f.write(f"**Target Tokens:** {target_tokens}\n")
        f.write(f"**Original Size:** {len(content)} chars, ~{count_tokens(content)} tokens\n\n")
        
        f.write(f"## Summary\n\n")
        f.write(f"- **Original Paragraphs:** {len(paragraphs)}\n")
        f.write(f"- **Large Paragraphs:** {len(large_paragraphs)} (needed splitting)\n")
        f.write(f"- **Small Paragraphs:** {len(small_paragraphs)} (already suitable)\n")
        f.write(f"- **Total Chunks After Splitting:** {len(all_chunks)}\n")
        f.write(f"- **Final Optimized Chunks:** {len(final_chunks)}\n\n")
        
        f.write(f"## Large Paragraph Split Details\n\n")
        for detail in split_details:
            f.write(f"### Paragraph {detail['original_para']}\n")
            f.write(f"- **Original:** {detail['original_tokens']} tokens\n")
            f.write(f"- **Split into:** {detail['sub_chunks']} sub-chunks\n\n")
            for j, chunk in enumerate(detail['chunks']):
                f.write(f"**Sub-chunk {j+1}:** {count_tokens(chunk)} tokens\n")
                f.write(f"```\n{chunk[:200]}{'...' if len(chunk) > 200 else ''}\n```\n\n")
        
        f.write(f"## Final Chunk Distribution\n\n")
        f.write("| Chunk | Tokens | Characters | Preview |\n")
        f.write("|-------|--------|------------|----------|\n")
        for i, chunk in enumerate(final_chunks):
            preview = chunk[:50].replace('\n', ' ').replace('|', '\\|')
            if len(chunk) > 50:
                preview += "..."
            f.write(f"| {i+1} | {count_tokens(chunk)} | {len(chunk)} | {preview} |\n")
    
    # Save each final chunk
    for i, chunk in enumerate(final_chunks):
        chunk_file = debug_dir / f"{base_name}_final_chunk_{i+1:03d}.md"
        metadata = f"""<!-- FINAL CHUNK {i+1}/{len(final_chunks)} -->
<!-- Tokens: {count_tokens(chunk)} -->
<!-- Characters: {len(chunk)} -->
<!-- Source: {file_path} -->

---

"""
        with open(chunk_file, 'w', encoding='utf-8') as f:
            f.write(metadata + chunk)
    
    print(f"\n🐛 Debug files saved to: {debug_dir}/")
    print(f"   📊 1 analysis report")
    print(f"   📁 {len(final_chunks)} final chunk files")
    
    return final_chunks

def main():
    """Main function"""
    if len(sys.argv) != 2:
        print("Usage: python debug_chunking_standalone.py <markdown_file>")
        print("Example: python debug_chunking_standalone.py docs/mega-token-example.md")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        sys.exit(1)
    
    print(f"🚀 Smart Chunking Analysis Tool")
    print(f"🧮 Tiktoken available: {TIKTOKEN_AVAILABLE}")
    print()
    
    chunks = analyze_chunking_process(file_path)
    
    print(f"\n📈 Token distribution:")
    token_counts = [count_tokens(chunk) for chunk in chunks]
    print(f"   Min: {min(token_counts)} tokens")
    print(f"   Max: {max(token_counts)} tokens") 
    print(f"   Avg: {sum(token_counts) / len(token_counts):.1f} tokens")

if __name__ == "__main__":
    main()