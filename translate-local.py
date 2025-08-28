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

def check_ollama_server():
    """Ollama 서버가 실행 중인지 확인"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        return response.status_code == 200
    except:
        return False

def check_model_available(model="exaone3.5:7.8b"):
    """지정된 모델이 사용 가능한지 확인"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json()
            model_names = [m['name'] for m in models.get('models', [])]
            return model in model_names
        return False
    except:
        return False

def translate_with_ollama(text, model="exaone3.5:7.8b"):
    """Ollama API를 사용하여 텍스트를 번역"""
    url = "http://localhost:11434/api/generate"
    
    prompt = f"""다음 한국어 텍스트를 영어로 번역해주세요. 마크다운 형식과 구조를 유지하세요. 번역된 텍스트만 반환하고 추가적인 설명은 하지 마세요.

한국어 텍스트:
{text}

영어 번역:"""
    
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.3,
            "top_p": 0.9
        }
    }
    
    try:
        print(f"번역 중... (모델: {model})")
        response = requests.post(url, json=payload, timeout=300)
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

def process_markdown_file(input_path, output_path):
    """마크다운 파일을 번역하여 저장"""
    print(f"\n번역 중: {input_path} -> {output_path}")
    
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 큰 파일을 처리하기 위해 청크로 분할
    chunks = content.split('\n\n')
    translated_chunks = []
    
    for i, chunk in enumerate(chunks):
        if chunk.strip():
            print(f"청크 번역 중 {i+1}/{len(chunks)}")
            translated_chunk = translate_with_ollama(chunk)
            translated_chunks.append(translated_chunk)
            time.sleep(1)  # API 속도 제한
        else:
            translated_chunks.append(chunk)
    
    translated_content = '\n\n'.join(translated_chunks)
    
    # 출력 디렉토리 생성
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # 번역된 내용 저장
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(translated_content)
    
    print(f"번역 완료: {output_path}")

def main():
    print("=== Ollama 문서 번역기 ===")
    
    # Ollama 서버 확인
    if not check_ollama_server():
        print("❌ Ollama 서버가 실행되고 있지 않습니다.")
        print("다음 명령으로 Ollama를 시작하세요: ollama serve")
        return
    
    print("✅ Ollama 서버 연결됨")
    
    # 모델 확인
    model = "exaone3.5:7.8b"
    if not check_model_available(model):
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
        
        process_markdown_file(md_file, output_file)
    
    print(f"\n🎉 모든 번역이 완료되었습니다!")
    print(f"번역된 파일들은 '{docs_en_dir}' 디렉토리에서 확인할 수 있습니다.")

if __name__ == "__main__":
    main()