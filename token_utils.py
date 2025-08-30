#!/usr/bin/env python3
"""
토큰 기반 유틸리티 함수들
"""

import re
import time


def estimate_token_count(text):
    """
    보수적인 토큰 개수 추정
    - 한글: 대략 1토큰 ≈ 1~1.3자
    - 영어: 1토큰 ≈ 3~4자
    - 안전하게 토큰 수를 높게 추정
    """
    if not text:
        return 0
    
    # 한글과 영어 문자 분리
    korean_chars = len(re.findall(r'[가-힣]', text))
    english_words = len(re.findall(r'\b[a-zA-Z]+\b', text))
    symbols_and_spaces = len(text) - korean_chars - sum(len(word) for word in re.findall(r'\b[a-zA-Z]+\b', text))
    
    # 토큰 추정 (보수적)
    korean_tokens = korean_chars * 1.3  # 한글은 1.3토큰으로 추정
    english_tokens = english_words * 0.7  # 영어 단어는 0.7토큰으로 추정  
    other_tokens = symbols_and_spaces * 0.5  # 기호와 공백은 0.5토큰으로 추정
    
    return int(korean_tokens + english_tokens + other_tokens)


def calculate_safe_chunk_size(context_length, temperature=0.3):
    """
    컨텍스트 길이에 따른 안전한 청크 크기 계산
    비율 기반으로 계산하여 더 정확한 토큰 관리
    """
    if context_length <= 0:
        return float('inf')  # 제한 없음
    
    # 프롬프트 오버헤드 (지시문, 시스템 메시지 등)
    base_prompt_tokens = 300
    variable_prompt_tokens = min(300, context_length * 0.1)  # 컨텍스트의 10%까지
    prompt_overhead = int(base_prompt_tokens + variable_prompt_tokens)
    
    # 출력 예약 토큰 (번역은 보통 입력보다 10-20% 길어짐)
    min_output_reserve = 800
    proportional_output_reserve = int(context_length * 0.35)
    output_reserve = max(min_output_reserve, proportional_output_reserve)
    
    # 안전 마진 (컨텍스트의 5%)
    safety_margin = int(context_length * 0.05)
    
    # 실제 입력에 사용할 수 있는 토큰 수
    safe_input_tokens = context_length - prompt_overhead - output_reserve - safety_margin
    
    # 최소값 보장
    safe_input_tokens = max(safe_input_tokens, 200)
    
    return safe_input_tokens


def protect_markdown_elements(text):
    """
    마크다운 특수 요소들을 임시 토큰으로 치환하여 보호
    """
    protected_elements = {}
    counter = 0
    
    def replace_with_token(match):
        nonlocal counter
        token = f"__PROTECTED_ELEMENT_{counter}__"
        protected_elements[token] = match.group(0)
        counter += 1
        return token
    
    # 코드 펜스 보호 (```...```) - Mermaid 포함
    text = re.sub(r'```[\s\S]*?```', replace_with_token, text)
    
    # 인라인 코드 보호 (`...`)
    text = re.sub(r'`[^`\n]+`', replace_with_token, text)
    
    # 수식 보호 ($...$, $$...$$)
    text = re.sub(r'\$\$[\s\S]*?\$\$', replace_with_token, text)
    text = re.sub(r'\$[^$\n]+\$', replace_with_token, text)
    
    # HTML 주석 보호
    text = re.sub(r'<!--[\s\S]*?-->', replace_with_token, text)
    
    # 테이블 보호 (연속된 | 라인들)
    table_pattern = r'(\|.*\|[\s]*\n)+(\|[\s]*[-:]+[\s]*\|[\s]*\n)?(\|.*\|[\s]*\n)+'
    text = re.sub(table_pattern, replace_with_token, text, flags=re.MULTILINE)
    
    # 링크와 이미지 보호 (더 정확한 패턴)
    text = re.sub(r'!\[[^\]]*\]\([^\)]+\)', replace_with_token, text)  # 이미지
    text = re.sub(r'\[[^\]]+\]\([^\)]+\)', replace_with_token, text)   # 링크
    
    # URL 보호 (더 포괄적)
    text = re.sub(r'https?://[^\s\)\]]+', replace_with_token, text)
    
    # 이메일 보호
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', replace_with_token, text)
    
    return text, protected_elements


def restore_protected_elements(text, protected_elements):
    """
    보호된 요소들을 원래대로 복원
    """
    for token, original in protected_elements.items():
        text = text.replace(token, original)
    return text


def split_markdown_content(content, max_tokens):
    """
    마크다운 구조를 인지한 스마트 분할
    헤딩 단위 -> 문단 단위 -> 문장 단위 순으로 분할
    """
    chunks = []
    current_chunk = ""
    current_tokens = 0
    
    # YAML front matter 처리
    front_matter = ""
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            front_matter = f"---{parts[1]}---"
            content = parts[2].lstrip('\n')
    
    # 헤딩으로 우선 분할
    sections = re.split(r'\n(#{1,3}\s+.*)', content)
    
    for i, section in enumerate(sections):
        if not section.strip():
            continue
            
        section_tokens = estimate_token_count(section)
        
        # 현재 청크에 추가할 수 있는지 확인
        if current_tokens + section_tokens <= max_tokens and current_chunk:
            current_chunk += '\n' + section
            current_tokens += section_tokens
        else:
            # 현재 청크 저장
            if current_chunk.strip():
                final_chunk = front_matter + '\n' + current_chunk if front_matter and chunks == [] else current_chunk
                chunks.append(final_chunk.strip())
                front_matter = ""  # front matter는 첫 번째 청크에만 추가
            
            # 섹션이 너무 크면 문단으로 재분할
            if section_tokens > max_tokens:
                sub_chunks = _split_section_by_paragraphs(section, max_tokens)
                chunks.extend(sub_chunks)
                current_chunk = ""
                current_tokens = 0
            else:
                current_chunk = section
                current_tokens = section_tokens
    
    # 마지막 청크 저장
    if current_chunk.strip():
        final_chunk = front_matter + '\n' + current_chunk if front_matter else current_chunk
        chunks.append(final_chunk.strip())
    
    return chunks


def _split_section_by_paragraphs(section, max_tokens):
    """
    섹션을 문단 단위로 분할
    """
    chunks = []
    current_chunk = ""
    current_tokens = 0
    
    paragraphs = section.split('\n\n')
    
    for paragraph in paragraphs:
        if not paragraph.strip():
            continue
            
        paragraph_tokens = estimate_token_count(paragraph)
        
        if current_tokens + paragraph_tokens <= max_tokens and current_chunk:
            current_chunk += '\n\n' + paragraph
            current_tokens += paragraph_tokens
        else:
            if current_chunk.strip():
                chunks.append(current_chunk.strip())
            
            # 문단이 너무 크면 문장으로 재분할
            if paragraph_tokens > max_tokens:
                sub_chunks = _split_paragraph_by_sentences(paragraph, max_tokens)
                chunks.extend(sub_chunks)
                current_chunk = ""
                current_tokens = 0
            else:
                current_chunk = paragraph
                current_tokens = paragraph_tokens
    
    if current_chunk.strip():
        chunks.append(current_chunk.strip())
    
    return chunks


def _split_paragraph_by_sentences(paragraph, max_tokens):
    """
    문단을 문장 단위로 분할 (최후의 수단)
    """
    chunks = []
    current_chunk = ""
    current_tokens = 0
    
    # 문장 분할 (마크다운 구조 고려)
    lines = paragraph.split('\n')
    
    for line in lines:
        if not line.strip():
            if current_chunk:
                current_chunk += '\n'
            continue
            
        line_tokens = estimate_token_count(line)
        
        if current_tokens + line_tokens <= max_tokens and current_chunk:
            current_chunk += '\n' + line
            current_tokens += line_tokens
        else:
            if current_chunk.strip():
                chunks.append(current_chunk.strip())
            
            current_chunk = line
            current_tokens = line_tokens
    
    if current_chunk.strip():
        chunks.append(current_chunk.strip())
    
    return chunks


def normalize_chunk_boundaries(chunks):
    """
    청크 경계에서 발생하는 아티팩트 정리
    """
    normalized_chunks = []
    
    for chunk in chunks:
        # 앞뒤 공백 정리
        chunk = chunk.strip()
        
        # 연속된 빈 줄 정리 (3개 이상의 연속 빈 줄을 2개로 제한)
        chunk = re.sub(r'\n{4,}', '\n\n\n', chunk)
        
        if chunk:
            normalized_chunks.append(chunk)
    
    return normalized_chunks


def join_translated_chunks(chunks):
    """
    번역된 청크들을 적절히 합치기
    경계 아티팩트 방지
    """
    if not chunks:
        return ""
    
    result = []
    
    for i, chunk in enumerate(chunks):
        if not chunk.strip():
            continue
            
        # 첫 번째 청크는 그대로 추가
        if i == 0:
            result.append(chunk.strip())
            continue
        
        prev_chunk = result[-1] if result else ""
        current_chunk = chunk.strip()
        
        # 이전 청크가 헤딩으로 끝나거나 현재 청크가 헤딩으로 시작하면 간격 조정
        if (prev_chunk.split('\n')[-1].startswith('#') or 
            current_chunk.split('\n')[0].startswith('#')):
            result.append('\n\n' + current_chunk)
        # 코드 블록이나 특수 블록의 경우
        elif (prev_chunk.endswith('```') or current_chunk.startswith('```') or
              prev_chunk.endswith('$$') or current_chunk.startswith('$$')):
            result.append('\n\n' + current_chunk)
        else:
            # 일반적인 경우
            result.append('\n\n' + current_chunk)
    
    return ''.join(result)