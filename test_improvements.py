#!/usr/bin/env python3
"""
개선사항 테스트 스크립트
"""

from token_utils import (
    estimate_token_count,
    calculate_safe_chunk_size,
    protect_markdown_elements,
    restore_protected_elements,
    split_markdown_content,
    normalize_chunk_boundaries,
    join_translated_chunks
)

def test_token_estimation():
    """토큰 추정 테스트"""
    print("=== 토큰 추정 테스트 ===")
    
    test_cases = [
        "안녕하세요",
        "Hello world",
        "안녕하세요 Hello world",
        "```python\nprint('hello')\n```",
        "# 제목\n\n내용입니다.",
    ]
    
    for text in test_cases:
        tokens = estimate_token_count(text)
        print(f"'{text[:30]}...' -> {tokens} tokens")

def test_safe_chunk_size():
    """안전한 청크 크기 계산 테스트"""
    print("\n=== 안전한 청크 크기 계산 테스트 ===")
    
    contexts = [4096, 8192, 32768, 131072]
    
    for context in contexts:
        safe_size = calculate_safe_chunk_size(context)
        print(f"Context {context} -> Safe chunk size: {safe_size} tokens")

def test_protection():
    """마크다운 요소 보호 테스트"""
    print("\n=== 마크다운 요소 보호 테스트 ===")
    
    test_md = """# 제목

일반 텍스트입니다.

```python
print("Hello World")
```

인라인 코드: `variable_name`

수식: $E = mc^2$

블록 수식:
$$
\\sum_{i=1}^{n} x_i
$$

링크: [GitHub](https://github.com)
이미지: ![alt text](image.png)

| 열1 | 열2 |
|-----|-----|
| 데이터1 | 데이터2 |

이메일: test@example.com
"""
    
    protected, elements = protect_markdown_elements(test_md)
    print(f"원본 길이: {len(test_md)}")
    print(f"보호된 길이: {len(protected)}")
    print(f"보호된 요소 수: {len(elements)}")
    
    # 복원 테스트
    restored = restore_protected_elements(protected, elements)
    print(f"복원 성공: {restored == test_md}")

def test_smart_splitting():
    """스마트 분할 테스트"""
    print("\n=== 스마트 분할 테스트 ===")
    
    long_content = """---
title: 테스트 문서
---

# 첫 번째 섹션

이것은 첫 번째 섹션의 내용입니다. 
여러 문단으로 구성되어 있습니다.

```python
def hello():
    print("Hello World")
    return "success"
```

## 두 번째 하위 섹션

더 많은 내용들...

| 테이블 | 데이터 |
|--------|--------|
| 행1    | 값1    |
| 행2    | 값2    |

# 두 번째 섹션

또 다른 섹션입니다.

수식 예제: $\\int_0^\\infty e^{-x} dx = 1$

더 많은 내용들이 계속됩니다...
""" * 3  # 내용을 3배로 늘려서 분할이 필요하게 만듦
    
    max_tokens = 500
    chunks = split_markdown_content(long_content, max_tokens)
    chunks = normalize_chunk_boundaries(chunks)
    
    print(f"원본 토큰 수: {estimate_token_count(long_content)}")
    print(f"청크 수: {len(chunks)}")
    
    for i, chunk in enumerate(chunks):
        tokens = estimate_token_count(chunk)
        print(f"청크 {i+1}: {tokens} tokens (첫 30자: {chunk[:30].replace(chr(10), ' ')}...)")

def test_joining():
    """청크 결합 테스트"""
    print("\n=== 청크 결합 테스트 ===")
    
    chunks = [
        "# 제목\n\n첫 번째 내용",
        "## 하위 제목\n\n두 번째 내용",
        "일반 문단입니다.",
        "```python\ncode\n```",
        "마지막 내용"
    ]
    
    joined = join_translated_chunks(chunks)
    print(f"결합된 내용 길이: {len(joined)}")
    print("결합된 내용:")
    print(joined[:200] + "..." if len(joined) > 200 else joined)

if __name__ == "__main__":
    test_token_estimation()
    test_safe_chunk_size()
    test_protection()
    test_smart_splitting()
    test_joining()
    print("\n✅ 모든 테스트 완료!")