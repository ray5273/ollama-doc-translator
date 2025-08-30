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
from token_utils import (
    estimate_token_count,
    calculate_safe_chunk_size,
    protect_markdown_elements,
    restore_protected_elements,
    split_markdown_content,
    normalize_chunk_boundaries,
    join_translated_chunks
)

def check_ollama_server(ssl_verify=True):
    """Ollama 서버가 실행 중인지 확인"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5, verify=ssl_verify)
        return response.status_code == 200
    except:
        return False

def check_model_available(model="exaone3.5:7.8b", ssl_verify=True):
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

def translate_with_ollama(text, model="exaone3.5:7.8b", ssl_verify=True, retries=0, max_retries=3, context_length=32768):
    """Ollama API를 사용하여 텍스트를 번역 (향상된 버전)"""
    url = "http://localhost:11434/api/generate"
    
    if retries >= max_retries:
        print(f"⚠️ 최대 재시도 횟수({max_retries}) 도달, 원본 반환")
        return text, 0, 0
    
    # 보호된 요소들 처리
    protected_text, protected_elements = protect_markdown_elements(text)
    
    # 입력 토큰 수 계산
    input_tokens = estimate_token_count(protected_text)
    
    prompt = f"""다음 한국어 텍스트를 영어로 번역해주세요. 다음 지침을 엄격히 따르세요:

- 마크다운 형식과 구조를 정확히 유지하세요 
- 코드 블록, 인라인 코드, 링크, URL, 이미지 경로, 수식, Mermaid, HTML 주석은 번역하지 마세요
- 입력이 이미 영어이거나 한국어가 없다면 그대로 반환하세요 
- 목록/테이블 구조를 그대로 유지하세요. YAML 프론트 매터가 있다면 그대로 유지하세요 
- 번역된 텍스트만 반환하고 추가적인 설명은 하지 마세요

한국어 텍스트:
{protected_text}

영어 번역:"""
    
    # 향상된 옵션 설정
    options = {
        "temperature": 0.2,  # 더 일관된 번역을 위해 낮춤
        "top_p": 0.9,
        "repeat_penalty": 1.1,
        "num_predict": -1
    }
    
    # 컨텍스트 길이 설정
    if context_length > 0:
        options["num_ctx"] = context_length
    
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": options
    }
    
    try:
        print(f"번역 중... (모델: {model}, 토큰: {input_tokens})")
        response = requests.post(url, json=payload, timeout=300, verify=ssl_verify)
        response.raise_for_status()
        result = response.json()
        translated = result.get('response', '').strip()
        
        # 가끔 모델이 추가 설명을 포함할 수 있으므로 정리
        if translated.startswith('영어 번역:'):
            translated = translated.replace('영어 번역:', '').strip()
        
        # 보호된 요소들 복원
        translated = restore_protected_elements(translated, protected_elements)
        
        # 출력 토큰 수 계산
        output_tokens = estimate_token_count(translated)
        
        return translated, input_tokens, output_tokens
    except Exception as e:
        print(f"번역 오류 (시도 {retries + 1}): {e}")
        if retries < max_retries - 1:
            time.sleep(2 ** retries)  # 지수 백오프
            return translate_with_ollama(text, model, ssl_verify, retries + 1, max_retries, context_length)
        else:
            return text, input_tokens, 0

def process_markdown_file(input_path, output_path, context_length=4096, ssl_verify=True):
    """마크다운 파일을 향상된 토큰 기반 방식으로 번역하여 저장"""
    print(f"\n번역 중: {input_path} -> {output_path}")
    
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 전체 문서의 토큰 수 계산
    total_tokens = estimate_token_count(content)
    print(f"📊 문서 토큰 수: {total_tokens}")
    
    if context_length > 0:
        # 안전한 청크 크기 계산 (토큰 기반)
        max_chunk_tokens = calculate_safe_chunk_size(context_length, 0.2)
        
        if total_tokens > max_chunk_tokens:
            # 스마트 분할 실행
            print(f"📋 청크로 분할 (최대 청크당 토큰: {max_chunk_tokens})")
            chunks = split_markdown_content(content, max_chunk_tokens)
            chunks = normalize_chunk_boundaries(chunks)
            
            translated_chunks = []
            total_chunks = len(chunks)
            total_input_tokens = 0
            total_output_tokens = 0
            
            print(f"📊 {total_chunks}개 청크 처리 중 (컨텍스트: {context_length})...")
            
            for i, chunk in enumerate(chunks):
                chunk_tokens = estimate_token_count(chunk)
                print(f"🔄 [{i+1}/{total_chunks}] 청크 처리 중 ({chunk_tokens} 토큰)...", end='')
                
                translated_chunk, input_tokens, output_tokens = translate_with_ollama(
                    chunk, ssl_verify=ssl_verify, context_length=context_length
                )
                
                if translated_chunk:
                    translated_chunks.append(translated_chunk)
                    total_input_tokens += input_tokens
                    total_output_tokens += output_tokens
                    print(f" ✅ 완료 ({input_tokens}→{output_tokens} 토큰)")
                else:
                    print(f" ⚠️ 빈 결과")
                    translated_chunks.append(chunk)  # 원본 사용
                
                time.sleep(0.5)  # API 속도 제한 완화
            
            print(f"📝 {len(translated_chunks)}개 청크 결합 중...")
            print(f"📊 총 토큰 처리: {total_input_tokens} → {total_output_tokens}")
            translated_content = join_translated_chunks(translated_chunks)
        else:
            # 파일이 충분히 작아서 한 번에 처리 가능
            print(f"📄 전체 파일을 한 번에 번역 ({total_tokens} 토큰, 제한: {max_chunk_tokens})...")
            translated_content, input_tokens, output_tokens = translate_with_ollama(
                content, ssl_verify=ssl_verify, context_length=context_length
            )
            print(f"📊 토큰 처리: {input_tokens} → {output_tokens}")
    else:
        # Context length 제한 없음, 전체 파일을 한 번에 처리
        print(f"📄 전체 파일을 한 번에 번역 (컨텍스트 제한 없음, {total_tokens} 토큰)...")
        translated_content, input_tokens, output_tokens = translate_with_ollama(
            content, ssl_verify=ssl_verify, context_length=0
        )
        print(f"📊 토큰 처리: {input_tokens} → {output_tokens}")
    
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
    model = "exaone3.5:7.8b"
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