#!/usr/bin/env python3
"""
로컬 테스트용 번역 스크립트
Ollama API를 사용하여 docs/ 폴더의 한국어 마크다운 파일을 docs-en/ 폴더로 번역합니다.
"""

import os
import json
import requests
import time
from pathlib import Path

def check_ollama_server(ssl_verify=True):
    """Ollama 서버가 실행 중인지 확인"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5, verify=ssl_verify)
        return response.status_code == 200
    except:
        return False

def check_model_available(model="ray5273/exaone-3.5-7.8b-KorEng-Translation:q8", ssl_verify=True):
    """지정된 모델이 사용 가능한지 확인"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5, verify=ssl_verify)
        if response.status_code == 200:
            models = response.json()
            model_names = [m['name'] for m in models.get('models', [])]
            return model in model_names
        return False
    except:
        return False

def translate_with_ollama(text, model="ray5273/exaone-3.5-7.8b-KorEng-Translation:q8", ssl_verify=True):
    """Ollama API를 사용하여 텍스트를 번역 (fine-tuned 모델 형식에 맞춤)"""
    url = "http://localhost:11434/api/generate"

    # System prompt matching the fine-tuned model's training data
    system_prompt = """You are an expert Korean to English translator specializing in technical documentation and markdown content.

Your translation guidelines:
1. Produce natural, fluent English while preserving the original meaning
2. Keep ALL markdown formatting exactly as-is:
   - Headers (#, ##, ###)
   - Bold (**text**) and italic (*text*)
   - Code blocks (```language ... ```)
   - Inline code (`code`)
   - Links [text](url) - translate text, keep url unchanged
   - Tables (| ... |)
   - Lists (-, *, 1.)
3. Do NOT translate:
   - Code inside code blocks
   - URLs and file paths
   - Variable names and function names
   - Technical terms that are commonly kept in English
4. Maintain paragraph structure and line breaks"""

    # User prompt matching the fine-tuned model's training data format
    prompt = f"""Translate to English (preserve markdown formatting):

{text}"""

    payload = {
        "model": model,
        "system": system_prompt,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.3,
            "top_k": 50,
            "top_p": 0.9,
            "repetition_penalty": 1.0
        }
    }
    
    try:
        print(f"번역 중... (모델: {model})")
        response = requests.post(url, json=payload, timeout=300, verify=ssl_verify)
        response.raise_for_status()
        result = response.json()
        translated = result.get('response', '').strip()
        
        # 가끔 모델이 추가 설명을 포함할 수 있으므로 정리
        if translated.startswith('영어 번역:'):
            translated = translated.replace('영어 번역:', '').strip()
        
        return translated
    except Exception as e:
        print(f"번역 오류: {e}")
        return text

def process_markdown_file(input_path, output_path, context_length=4096, ssl_verify=True):
    """마크다운 파일을 번역하여 저장"""
    print(f"\n번역 중: {input_path} -> {output_path}")
    
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if context_length > 0:
        # Calculate safe input length based on context size
        if context_length <= 4096:
            safe_input_length = 800   # Tiny chunks for very small context
        elif context_length <= 8192:
            safe_input_length = 1500  # Small chunks
        elif context_length <= 32768:
            safe_input_length = 4000  # Medium chunks
        else:
            # For large context, use proportional calculation
            prompt_overhead = 500
            output_reserve = context_length // 2
            safe_input_tokens = context_length - prompt_overhead - output_reserve
            safe_input_length = safe_input_tokens * 2
        
        if len(content) > safe_input_length:
            # Split content into chunks based on safe input length
            chunks = []
            current_chunk = ""
            paragraphs = content.split('\n\n')
            
            for paragraph in paragraphs:
                # If paragraph itself is too long, split it further
                if len(paragraph) > safe_input_length:
                    # Save current chunk if it exists
                    if current_chunk:
                        chunks.append(current_chunk)
                        current_chunk = ""
                    
                    # Split long paragraph by sentences or lines
                    lines = paragraph.split('\n')
                    temp_chunk = ""
                    for line in lines:
                        if len(temp_chunk) + len(line) + 1 <= safe_input_length:
                            if temp_chunk:
                                temp_chunk += '\n' + line
                            else:
                                temp_chunk = line
                        else:
                            if temp_chunk:
                                chunks.append(temp_chunk)
                            temp_chunk = line
                    if temp_chunk:
                        current_chunk = temp_chunk
                elif len(current_chunk) + len(paragraph) + 2 <= safe_input_length:
                    if current_chunk:
                        current_chunk += '\n\n' + paragraph
                    else:
                        current_chunk = paragraph
                else:
                    if current_chunk:
                        chunks.append(current_chunk)
                    current_chunk = paragraph
            
            if current_chunk:
                chunks.append(current_chunk)
            
            translated_chunks = []
            
            print(f"청크로 분할하여 번역 ({len(chunks)}개 청크, 안전한 입력 길이: {safe_input_length})")
            
            for i, chunk in enumerate(chunks):
                print(f"청크 번역 중 {i+1}/{len(chunks)}")
                translated_chunk = translate_with_ollama(chunk, ssl_verify=ssl_verify)
                translated_chunks.append(translated_chunk)
                time.sleep(1)  # API 속도 제한
            
            translated_content = '\n\n'.join(translated_chunks)
        else:
            # 파일이 충분히 작아서 한 번에 처리 가능
            print(f"전체 파일을 한 번에 번역합니다 (크기: {len(content)}, 안전 제한: {safe_input_length})...")
            translated_content = translate_with_ollama(content, ssl_verify=ssl_verify)
    else:
        # Context length 제한 없음, 전체 파일을 한 번에 처리
        print("전체 파일을 한 번에 번역합니다 (context 제한 없음)...")
        translated_content = translate_with_ollama(content, ssl_verify=ssl_verify)
    
    # 출력 디렉토리 생성
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # 번역된 내용 저장
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(translated_content)
    
    print(f"번역 완료: {output_path}")

def main():
    print("=== Ollama 문서 번역기 ===")
    
    # 설정 옵션
    ssl_verify = input("SSL 인증서 검증을 사용하시겠습니까? (y/n, 기본값: y): ").lower() not in ['n', 'no']
    context_input = input("모델 context 길이를 입력하세요 (0 = chunking 안함, 기본값: 4096): ").strip()
    context_length = int(context_input) if context_input else 4096
    
    print(f"설정: SSL 검증 = {ssl_verify}, Context 길이 = {context_length}")
    
    # Ollama 서버 확인
    if not check_ollama_server(ssl_verify):
        print("❌ Ollama 서버가 실행되고 있지 않습니다.")
        print("다음 명령으로 Ollama를 시작하세요: ollama serve")
        return
    
    print("✅ Ollama 서버 연결됨")
    
    # 모델 확인
    model = "ray5273/exaone-3.5-7.8b-KorEng-Translation:q8"
    if not check_model_available(model, ssl_verify):
        print(f"❌ 모델 '{model}'을 찾을 수 없습니다.")
        print(f"다음 명령으로 모델을 다운로드하세요: ollama pull {model}")
        return
    
    print(f"✅ 모델 '{model}' 사용 가능")
    
    docs_dir = Path('docs')
    docs_en_dir = Path('docs-en')
    
    if not docs_dir.exists():
        print("❌ docs/ 디렉토리를 찾을 수 없습니다.")
        return
    
    # docs/ 디렉토리에서 모든 마크다운 파일 찾기
    md_files = list(docs_dir.rglob('*.md'))
    
    if not md_files:
        print("❌ docs/ 디렉토리에 마크다운 파일이 없습니다.")
        return
    
    print(f"\n📄 {len(md_files)}개의 마크다운 파일을 찾았습니다:")
    for md_file in md_files:
        print(f"  - {md_file}")
    
    print(f"\n🚀 번역을 시작합니다...")
    
    for md_file in md_files:
        # 상대 경로 계산
        rel_path = md_file.relative_to(docs_dir)
        output_file = docs_en_dir / rel_path
        
        # 이미 존재하고 더 새로운 경우 건너뛰기
        if output_file.exists() and output_file.stat().st_mtime > md_file.stat().st_mtime:
            print(f"⏭️  {md_file} 건너뛰기 (번역본이 최신)")
            continue
        
        process_markdown_file(md_file, output_file, context_length, ssl_verify)
    
    print(f"\n🎉 모든 번역이 완료되었습니다!")
    print(f"번역된 파일들은 '{docs_en_dir}' 디렉토리에서 확인할 수 있습니다.")

if __name__ == "__main__":
    main()