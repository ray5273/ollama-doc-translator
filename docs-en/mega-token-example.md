## CRITICAL INSTRUCTIONS - FOLLOW STRICTLY ##

1. **Preserve Structure:** All markdown syntax—including headings (`#`), lists (`-`, `1.`), code blocks (```), inline code (`...`), links (`[]()`), images, tables, blockquotes (`>`), and horizontal rules (`---`)—MUST be kept exactly as they are.
2. **Translate Content Only:** Only translate the human-readable Korean text.
3. **DO NOT Translate Non-Text Elements:**
    - Code within fenced code blocks (```...```) and inline code (`...`).
    - URLs, file paths, and technical identifiers.
    - YAML Frontmatter.
    - HTML/XML tags.
4. **No Extra Formatting:** Do not add or remove any markdown elements. Do not introduce new formatting.
5. **Output Only Translation:** Your response must contain ONLY the translated markdown content and nothing else. Do not add introductory phrases like "Here is the English translation:".
6. **Complete Code Blocks:** If the input contains code blocks (```), ensure ALL code blocks are properly closed with ```. Never leave a code block unclosed.


Korean Markdown Document:
# Translation Test Rich Markdown Document

This document is a collection of Korean content in various formats, designed to *definitely exceed 4096 tokens*.
It is intended for testing the **robustness** of translators/LLMs, including their ability to handle context, preserve format, and ignore code/table elements.

> **Guidelines:**
> 1) Make sure that code blocks and `mermaid` areas are preserved as they are.
> 2) Verify that numbers/unit formats (e.g., 1.2GB, 3ms), slash paths (`/var/log/app.log`), and options (`--flag`) are correctly translated.
> 3) The layout should not be disrupted even if tables, lists, quotes, checkboxes, formulas, and emojis 😀 are mixed together.


## 1. Mixing of Tables and Symbols/Units

| Item | Value | Unit | Note |
|---|---:|:---:|---|
| Processing Capacity | 12,345 | RPS | Up to 18,900 RPS at peak |
| Latency (P50) | 3.2 | ms | With `--enable-cache` enabled |
| Latency (P99) | 41.7 | ms | Including periods of GC (Garbage Collection) |
| Memory | 1.5 | GB | Based on RSS; cgroup limit is 2GB |
| Disk I/O | 220 | MB/s | Via NVMe-oF(TCP)


## 2. Task List

- [x] Accuracy of markdown header translations
- [x] Preservation of keywords within code blocks (`for`, `if`, `return`, etc.)
- [ ] Preservation of Mermaid diagrams and ignoring comments
- [ ] Preservation of units (GB/ms/%), paths (/etc/hosts)
- [ ] Preservation of inline formula $O(n \log n)$


## 3. Code Blocks: Bash/Python/JSON/YAML

```bash
#!/usr/bin/env bash
set -euo pipefail

APP_ENV="${APP_ENV:-prod}"
INPUT="${1:-/data/input.txt}"
OUT="/var/tmp/result.json"

echo "[INFO] Starting job on $(hostname) at $(date -Iseconds)"
if [[ ! -f "$INPUT" ]]; then
  echo "[ERROR] Input not found: $INPUT" >&2
  exit 1
fi

lines=$(wc -l < "$INPUT")
echo "[DEBUG] Line count: $lines"

curl -sS -X POST "http://127.0.0.1:8080/api" \  -H "Content-Type: application/json" \  -d "{"env":"$APP_ENV","count":$lines}" > "$OUT"

jq -r '.status' "$OUT" | grep -q success && echo "OK" || { echo "FAIL"; exit 2; }
```

```python
from __future__ import annotations

def rolling_avg(xs: list[float], k: int) -> list[float]:
    if k <= 0:
        raise ValueError("k must be > 0")
    out = []
    acc = 0.0
    for i, v in enumerate(xs):
        acc += v
        if i >= k:
            acc -= xs[i-k]
        if i >= k - 1:
            out.append(acc / k)
    return out

print(rolling_avg([1,2,3,4,5,6,7,8,9], 3))
```

```json
{
  "service": "analytics",
  "version": "1.4.2",
  "features": ["rollup", "compaction", "delta-index"],
  "limits": {
    "max_docs": 1000000,
    "max_payload_mb": 256
  }
}
```

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: test-config
data:
  APP_ENV: "staging"
  ENDPOINT: "https://api.example.com"
```

## 4. Mermaid Diagrams

### 4.1 Flowchart
```mermaid
flowchart TD
  A[Client] -->|HTTP/1.1| B(API Gateway)
  B --> C{Auth?}
  C -- yes --> D[Issue JWT]
  C -- no  --> E[401 Unauthorized]
  D --> F[Service A]
  D --> G[Service B]
  F --> H[(Cache)]
  G --> I[(DB)]
```
```

## CRITICAL INSTRUCTIONS - FOLLOW STRICTLY ##

1. **Preserve Structure:** All markdown syntax—including headings (`#`), lists (`-`, `1.`), code blocks (```), inline code (`...`), links (`[]()`), images, tables, blockquotes (`>`), and horizontal rules (`---`)—MUST be kept exactly as they are.
2. **Translate Content Only:** Only translate the human-readable Korean text.
3. **DO NOT Translate Non-Text Elements:**
    - Code within fenced code blocks (```...```) and inline code (`...`).
    - URLs, file paths, and technical identifiers.
    - YAML Frontmatter.
    - HTML/XML tags.
4. **No Extra Formatting:** Do not add or remove any markdown elements. Do not introduce new formatting.
5. **Output Only Translation:** Your response must contain ONLY the translated markdown content and nothing else. Do not add introductory phrases like "Here is the English translation:".
6. **Complete Code Blocks:** If the input contains code blocks (```), ensure ALL code blocks are properly closed with ```. Never leave a code block unclosed.


### 4.2 Sequence
```mermaid
sequenceDiagram
  participant U as User
  participant W as WebApp
  participant S as Service
  U->>W: POST /login (id,pw)
  W->>S: verify(id,pw)
  S-->>W: ok(token)
  W-->>U: 200 OK (set-cookie)
```

### 4.3 Gantt
```mermaid
gantt
  title Build & Deployment Schedule
  dateFormat YYYY-MM-DD
  section Build
  Unit Testing       :done,    des1, 2025-08-20,2025-08-21
  Integration Testing: active,  des2, 2025-08-22, 3d
  section Deploy
  Staging Deployment:         des3, after des2, 2d
  Production Deployment:         des4, 2025-08-28, 1d
```

## 5. Images/Links/Citations

![Sample Image](https://via.placeholder.com/640x360.png "placeholder")

- Document: <https://example.com/docs/guide>
- API Reference: [API Reference](https://example.com/api)
- Issue Tracker: https://example.com/issues

> “The quality of translation is determined by the simultaneous preservation of layout and meaning.” — Anonymous

## 6. Mixing Formulas and Text

- Average time complexity: $O(n \log n)$, worst case: $O(n^2)$
- Variance: $\sigma^2 = \frac{1}{n}\sum_{i=1}^{n}(x_i-\mu)^2$
- Sample average: $\bar{x} = \frac{1}{n}\sum x_i$

Paragraph example: This paragraph is a sample to ensure that bold, italic, and code are properly preserved during translation.
It includes emojis 😀, Chinese characters (漢字), English CamelCase, snake_case, and kebab-case.

### 7.1 Experimental Paragraph — Variation Pattern
The following paragraphs are similar, but to prevent duplicate translations, the vocabulary and order are slightly changed each time.
- Scenario: Summary of conversation records
- Condition: Includes 100k Korean characters
- Expected result: Summary rate of over 90%

#### Procedure
1. Input data: `/data/input_01.jsonl`
2. Options: `--batch 512 --timeout 3s --enable-cache`
3. Execution: `app run --job test-01 --qos high`
4. Verification: Check if `test-01 finished` is included in the logs

#### Observations
- As the GC cycle length increases, there is a tendency for P99 latency to increase.
- When the cache miss rate increases by 10%, throughput decreases by about 7%.
- When the connection pool size increases from 32 to 64, the retry rate per second decreases from 1.2% to 0.6%.

---

### 7.2 Experimental Paragraph — Variation Pattern
The following paragraphs are similar, but to prevent duplicate translations, the vocabulary and order are slightly changed each time.
- Scenario: Summary of conversation records
- Condition: Includes 100k Korean characters
- Expected result: Summary rate of over 90%

#### Procedure
1. Input data: `/data/input_02.jsonl`
2. Options: `--batch 512 --timeout 3s --enable-cache`
3. Execution: `app run --job test-02 --qos high`
4. Verification: Check if `test-02 finished` is included in the logs

#### Observations
- As the GC cycle length increases, there is a tendency for P99 latency to increase.
- When the cache miss rate increases by 10%, throughput decreases by about 7%.
- When the connection pool size increases from 32 to 64, the retry rate per second decreases from 1.2% to 0.6%.

---

### 7.3 Experimental Paragraph — Variation Pattern
The following paragraphs are similar, but to prevent duplicate translations, the vocabulary and order are slightly changed each time.
- Scenario: Kubernetes deployment
- Condition: HPA activated
- Expected result: Operation within a scale range of 2 to 10
```

## CRITICAL INSTRUCTIONS - FOLLOW STRICTLY ##

1. **Preserve Structure:** All markdown syntax—including headings (`#`), lists (`-`, `1.`), code blocks (```), inline code (`...`), links (`[]()`), images, tables, blockquotes (`>`), and horizontal rules (`---`)—MUST be kept exactly as they are.
2. **Translate Content Only:** Only translate the human-readable Korean text.
3. **DO NOT Translate Non-Text Elements:**
    - Code within fenced code blocks (```...```) and inline code (`...`).
    - URLs, file paths, and technical identifiers.
    - YAML Frontmatter.
    - HTML/XML tags.
4. **No Extra Formatting:** Do not add or remove any markdown elements. Do not introduce new formatting.
5. **Output Only Translation:** Your response must contain ONLY the translated markdown content and nothing else. Do not add introductory phrases like "Here is the English translation:".
6. **Complete Code Blocks:** If the input contains code blocks (```), ensure ALL code blocks are properly closed with ```. Never leave a code block unclosed.


#### Procedures
1. Input data: `/data/input_03.jsonl`
2. Options: `--batch 512 --timeout 3s --enable-cache`
3. Execution: `app run --job test-03 --qos high`
4. Verification: Check if "test-03 finished" is included in the logs


#### Observations
- A tendency to observe an increase in P99 latency as the GC cycle length increases.
- When the cache miss rate increases by 10%, throughput decreases by approximately 7%.
- When the connection pool size increases from 32 to 64, the retry rate per second decreases from 1.2% to 0.6%.


---

### 7.4 Experimental Section — Variation Patterns
The following sections are similar, but to prevent duplicate translations, the vocabulary and order are slightly altered with each iteration.
- Scenario: Kubernetes deployment
- Condition: HPA (High Performance Admission) enabled
- Expected result: Functioning within a scale range of 2 to 10


#### Procedures
1. Input data: `/data/input_04.jsonl`
2. Options: `--batch 512 --timeout 3s --enable-cache`
3. Execution: `app run --job test-04 --qos high`
4. Verification: Check if "test-04 finished" is included in the logs


#### Observations
- A tendency to observe an increase in P99 latency as the GC cycle length increases.
- When the cache miss rate increases by 10%, throughput decreases by approximately 7%.
- When the connection pool size increases from 32 to 64, the retry rate per second decreases from 1.2% to 0.6%.


---

### 7.5 Experimental Section — Variation Patterns
The following sections are similar, but to prevent duplicate translations, the vocabulary and order are slightly altered with each iteration.
- Scenario: Conversation record summary
- Condition: Including 100k Korean characters
- Expected result: A summary rate of over 90%


#### Procedures
1. Input data: `/data/input_05.jsonl`
2. Options: `--batch 512 --timeout 3s --enable-cache`
3. Execution: `app run --job test-05 --qos high`
4. Verification: Check if "test-05 finished" is included in the logs


#### Observations
- A tendency to observe an increase in P99 latency as the GC cycle length increases.
- When the cache miss rate increases by 10%, throughput decreases by approximately 7%.
- When the connection pool size increases from 32 to 64, the retry rate per second decreases from 1.2% to 0.6%.


---

### 7.6 Experimental Section — Variation Patterns
The following sections are similar, but to prevent duplicate translations, the vocabulary and order are slightly altered with each iteration.
- Scenario: Mermaid rendering
- Conditions: 50+ nodes, 100+ edges
- Expected result: No layout distortion


#### Procedures
1. Input data: `/data/input_06.jsonl`
2. Options: `--batch 512 --timeout 3s --enable-cache`
3. Execution: `app run --job test-06 --qos high`
4. Verification: Check if "test-06 finished" is included in the logs


#### Observations
- A tendency to observe an increase in P99 latency as the GC cycle length increases.
- When the cache miss rate increases by 10%, throughput decreases by approximately 7%.
- When the connection pool size increases from 32 to 64, the retry rate per second decreases from 1.2% to 0.6%.


---

### 7.7 Experimental Section — Variation Patterns
The following sections are similar, but to prevent duplicate translations, the vocabulary and order are slightly altered with each iteration.
- Scenario: Parsing large JSON volumes
- Conditions: 64MB payload, 4 workers
- Expected result: Completion without memory spikes


#### Procedures
1. Input data: `/data/input_07.jsonl`
2. Options: `--batch 512 --timeout 3s --enable-cache`
3. Execution: `app run --job test-07 --qos high`
4. Verification: Check if "test-07 finished" is included in the logs
```

## CRITICAL INSTRUCTIONS - FOLLOW STRICTLY ##
1. **Preserve Structure:** All markdown syntax—including headings (`#`), lists (`-`, `1.`), code blocks (```), inline code (`...`), links (`[]()`), images, tables, blockquotes (`>`), and horizontal rules (`---`)—MUST be kept exactly as they are.
2. **Translate Content Only:** Only translate the human-readable Korean text.
3. **DO NOT Translate Non-Text Elements:**
    - Code within fenced code blocks (```...```) and inline code (`...`).
    - URLs, file paths, and technical identifiers.
    - YAML Frontmatter.
    - HTML/XML tags.
4. **No Extra Formatting:** Do not add or remove any markdown elements. Do not introduce new formatting.
5. **Output Only Translation:** Your response must contain ONLY the translated markdown content and nothing else. Do not add introductory phrases like "Here is the English translation:".
6. **Complete Code Blocks:** If the input contains code blocks (```), ensure ALL code blocks are properly closed with ```. Never leave a code block unclosed.


#### Observations
- A trend of increasing P99 latency is observed as the GC cycle length increases.
- When the cache miss rate increases by 10%, throughput decreases by approximately 7%.
- When the connection pool size is increased from 32 to 64, the retry rate per second decreases from 1.2% to 0.6%.


---

### 7.8 Experiment Section — Variation Patterns
The following sections are similar, but to prevent duplicate translations, the wording and order are slightly changed with each iteration.
- Scenario: Parsing large volumes of JSON data.
- Conditions: 64MB payload, 4 workers.
- Expected result: Completion without any memory spikes.


#### Procedures
1. Input data: `/data/input_08.jsonl`
2. Options: `--batch 512 --timeout 3s --enable-cache`
3. Execution: `app run --job test-08 --qos high`
4. Verification: Check if `test-08 finished` is included in the logs.


#### Observations
- A trend of increasing P99 latency is observed as the GC cycle length increases.
- When the cache miss rate increases by 10%, throughput decreases by approximately 7%.
- When the connection pool size is increased from 32 to 64, the retry rate per second decreases from 1.2% to 0.6%.


---

### 7.9 Experiment Section — Variation Patterns
The following sections are similar, but to prevent duplicate translations, the wording and order are slightly changed with each iteration.
- Scenario: Parsing large volumes of JSON data.
- Conditions: 64MB payload, 4 workers.
- Expected result: Completion without any memory spikes.


#### Procedures
1. Input data: `/data/input_09.jsonl`
2. Options: `--batch 512 --timeout 3s --enable-cache`
3. Execution: `app run --job test-09 --qos high`
4. Verification: Check if `test-09 finished` is included in the logs.


#### Observations
- A trend of increasing P99 latency is observed as the GC cycle length increases.
- When the cache miss rate increases by 10%, throughput decreases by approximately 7%.
- When the connection pool size is increased from 32 to 64, the retry rate per second decreases from 1.2% to 0.6%.


---

### 7.10 Experiment Section — Variation Patterns
The following sections are similar, but to prevent duplicate translations, the wording and order are slightly changed with each iteration.
- Scenario: NVMe-oF I/O retries.
- Conditions: TCP RTT of 2ms, loss rate of 0.1%.
- Expected result: Retry rate below 1%.


#### Procedures
1. Input data: `/data/input_10.jsonl`
2. Options: `--batch 512 --timeout 3s --enable-cache`
3. Execution: `app run --job test-10 --qos high`
4. Verification: Check if `test-10 finished` is included in the logs.


#### Observations
- A trend of increasing P99 latency is observed as the GC cycle length increases.
- When the cache miss rate increases by 10%, throughput decreases by approximately 7%.
- When the connection pool size is increased from 32 to 64, the retry rate per second decreases from 1.2% to 0.6%.


---

### 7.11 Experiment Section — Variation Patterns
The following sections are similar, but to prevent duplicate translations, the wording and order are slightly changed with each iteration.
- Scenario: Parsing large volumes of JSON data.
- Conditions: 64MB payload, 4 workers.
- Expected result: Completion without any memory spikes.


#### Procedures
1. Input data: `/data/input_11.jsonl`
2. Options: `--batch 512 --timeout 3s --enable-cache`
3. Execution: `app run --job test-11 --qos high`
4. Verification: Check if `test-11 finished` is included in the logs.
```

## CRITICAL INSTRUCTIONS - FOLLOW STRICTLY ##

1. **Preserve Structure:** All markdown syntax—including headings (`#`), lists (`-`, `1.`), code blocks (```), inline code (`...`), links (`[]()`), images, tables, blockquotes (`>`), and horizontal rules (`---`)—MUST be kept exactly as they are.
2. **Translate Content Only:** Only translate the human-readable Korean text.
3. **DO NOT Translate Non-Text Elements:**
    - Code within fenced code blocks (```...```) and inline code (`...`).
    - URLs, file paths, and technical identifiers.
    - YAML Frontmatter.
    - HTML/XML tags.
4. **No Extra Formatting:** Do not add or remove any markdown elements. Do not introduce new formatting.
5. **Output Only Translation:** Your response must contain ONLY the translated markdown content and nothing else. Do not add introductory phrases like "Here is the English translation:".
6. **Complete Code Blocks:** If the input contains code blocks (```), ensure ALL code blocks are properly closed with ```. Never leave a code block unclosed.


#### Observations
- As the GC cycle length increases, there is a tendency for P99 latency to increase.
- When the cache miss rate increases by 10%, throughput decreases by approximately 7%.
- When the connection pool size increases from 32 to 64, the retry rate per second decreases from 1.2% to 0.6%.

---

### 7.12 Experiment Section — Variation Pattern
The following sections are similar, but to prevent duplicate translations, the vocabulary and order are slightly changed with each iteration.
- Scenario: Kubernetes deployment
- Condition: HPA enabled
- Expected result: Operation within a scale range of 2 to 10

#### Procedures
1. Input data: `/data/input_12.jsonl`
2. Options: `--batch 512 --timeout 3s --enable-cache`
3. Execution: `app run --job test-12 --qos high`
4. Verification: Check if `test-12 finished` is included in the logs

#### Observations
- As the GC cycle length increases, there is a tendency for P99 latency to increase.
- When the cache miss rate increases by 10%, throughput decreases by approximately 7%.
- When the connection pool size increases from 32 to 64, the retry rate per second decreases from 1.2% to 0.6%.

---

### 7.13 Experiment Section — Variation Pattern
The following sections are similar, but to prevent duplicate translations, the vocabulary and order are slightly changed with each iteration.
- Scenario: Large-scale JSON parsing
- Conditions: 64MB payload, 4 workers
- Expected result: Completion without memory spikes

#### Procedures
1. Input data: `/data/input_13.jsonl`
2. Options: `--batch 512 --timeout 3s --enable-cache`
3. Execution: `app run --job test-13 --qos high`
4. Verification: Check if `test-13 finished` is included in the logs

#### Observations
- As the GC cycle length increases, there is a tendency for P99 latency to increase.
- When the cache miss rate increases by 10%, throughput decreases by approximately 7%.
- When the connection pool size increases from 32 to 64, the retry rate per second decreases from 1.2% to 0.6%.

---

### 7.14 Experiment Section — Variation Pattern
The following sections are similar, but to prevent duplicate translations, the vocabulary and order are slightly changed with each iteration.
- Scenario: Large-scale JSON parsing
- Conditions: 64MB payload, 4 workers
- Expected result: Completion without memory spikes

#### Procedures
1. Input data: `/data/input_14.jsonl`
2. Options: `--batch 512 --timeout 3s --enable-cache`
3. Execution: `app run --job test-14 --qos high`
4. Verification: Check if `test-14 finished` is included in the logs

#### Observations
- As the GC cycle length increases, there is a tendency for P99 latency to increase.
- When the cache miss rate increases by 10%, throughput decreases by approximately 7%.
- When the connection pool size increases from 32 to 64, the retry rate per second decreases from 1.2% to 0.6%.

---

### 7.15 Experiment Section — Variation Pattern
The following sections are similar, but to prevent duplicate translations, the vocabulary and order are slightly changed with each iteration.
- Scenario: NVMe-oF I/O retries
- Conditions: TCP RTT of 2ms, loss of 0.1%
- Expected result: Retry rate of 1% or less

#### Procedures
1. Input data: `/data/input_15.jsonl`
2. Options: `--batch 512 --timeout 3s --enable-cache`
3. Execution: `app run --job test-15 --qos high`
4. Verification: Check if `test-15 finished` is included in the logs
```

## CRITICAL INSTRUCTIONS - FOLLOW STRICTLY ##
1. **Preserve Structure:** All markdown syntax—including headings (`#`), lists (`-`, `1.`), code blocks (```), inline code (`...`), links (`[]()`), images, tables, blockquotes (`>`), and horizontal rules (`---`)—MUST be kept exactly as they are.
2. **Translate Content Only:** Only translate the human-readable Korean text.
3. **DO NOT Translate Non-Text Elements:**
    - Code within fenced code blocks (```...```) and inline code (`...`).
    - URLs, file paths, and technical identifiers.
    - YAML Frontmatter.
    - HTML/XML tags.
4. **No Extra Formatting:** Do not add or remove any markdown elements. Do not introduce new formatting.
5. **Output Only Translation:** Your response must contain ONLY the translated markdown content and nothing else. Do not add introductory phrases like "Here is the English translation:".
6. **Complete Code Blocks:** If the input contains code blocks (```), ensure ALL code blocks are properly closed with ```. Never leave a code block unclosed.


#### Observations
- A trend of increasing P99 latency is observed as the GC cycle length increases.
- When the cache miss rate increases by 10%, throughput decreases by approximately 7%.
- When the connection pool size increases from 32 to 64, the retry rate per second decreases from 1.2% to 0.6%.

---

### 7.16 Experiment Section — Variation Patterns
The following sections are similar, but to prevent duplicate translations, the vocabulary and order are slightly changed with each iteration.
- Scenario: Mermaid rendering
- Conditions: 50+ nodes, 100+ edges
- Expected result: No layout distortion

#### Procedures
1. Input data: `/data/input_16.jsonl`
2. Options: `--batch 512 --timeout 3s --enable-cache`
3. Execution: `app run --job test-16 --qos high`
4. Verification: Check if `test-16 finished` is included in the logs

#### Observations
- A trend of increasing P99 latency is observed as the GC cycle length increases.
- When the cache miss rate increases by 10%, throughput decreases by approximately 7%.
- When the connection pool size increases from 32 to 64, the retry rate per second decreases from 1.2% to 0.6%.

---

### 7.17 Experiment Section — Variation Patterns
The following sections are similar, but to prevent duplicate translations, the vocabulary and order are slightly changed with each iteration.
- Scenario: Conversation record summarization
- Conditions: Including 100k Korean characters
- Expected result: A summary rate of over 90%

#### Procedures
1. Input data: `/data/input_17.jsonl`
2. Options: `--batch 512 --timeout 3s --enable-cache`
3. Execution: `app run --job test-17 --qos high`
4. Verification: Check if `test-17 finished` is included in the logs

#### Observations
- A trend of increasing P99 latency is observed as the GC cycle length increases.
- When the cache miss rate increases by 10%, throughput decreases by approximately 7%.
- When the connection pool size increases from 32 to 64, the retry rate per second decreases from 1.2% to 0.6%.

---

### 7.18 Experiment Section — Variation Patterns
The following sections are similar, but to prevent duplicate translations, the vocabulary and order are slightly changed with each iteration.
- Scenario: Parsing large JSON data
- Conditions: 64MB payload, 4 workers
- Expected result: Completion without memory spikes

#### Procedures
1. Input data: `/data/input_18.jsonl`
2. Options: `--batch 512 --timeout 3s --enable-cache`
3. Execution: `app run --job test-18 --qos high`
4. Verification: Check if `test-18 finished` is included in the logs

#### Observations
- A trend of increasing P99 latency is observed as the GC cycle length increases.
- When the cache miss rate increases by 10%, throughput decreases by approximately 7%.
- When the connection pool size increases from 32 to 64, the retry rate per second decreases from 1.2% to 0.6%.

---

### 7.19 Experiment Section — Variation Patterns
The following sections are similar, but to prevent duplicate translations, the vocabulary and order are slightly changed with each iteration.
- Scenario: Parsing large JSON data
- Conditions: 64MB payload, 4 workers
- Expected result: Completion without memory spikes

#### Procedures
1. Input data: `/data/input_19.jsonl`
2. Options: `--batch 512 --timeout 3s --enable-cache`
3. Execution: `app run --job test-19 --qos high`
4. Verification: Check if `test-19 finished` is included in the logs
```

## CRITICAL INSTRUCTIONS - FOLLOW STRICTLY ##

1. **Preserve Structure:** All markdown syntax—including headings (`#`), lists (`-`, `1.`), code blocks (```), inline code (`...`), links (`[]()`), images, tables, blockquotes (`>`), and horizontal rules (`---`)—MUST be kept exactly as they are.
2. **Translate Content Only:** Only translate the human-readable Korean text.
3. **DO NOT Translate Non-Text Elements:**
    - Code within fenced code blocks (```...```) and inline code (`...`).
    - URLs, file paths, and technical identifiers.
    - YAML Frontmatter.
    - HTML/XML tags.
4. **No Extra Formatting:** Do not add or remove any markdown elements. Do not introduce new formatting.
5. **Output Only Translation:** Your response must contain ONLY the translated markdown content and nothing else. Do not add introductory phrases like "Here is the English translation:".
6. **Complete Code Blocks:** If the input contains code blocks (```), ensure ALL code blocks are properly closed with ```. Never leave a code block unclosed.


#### Observations
- As the GC cycle length increases, there is a tendency for P99 latency to increase.
- When the cache miss rate increases by 10%, throughput decreases by approximately 7%.
- When the connection pool size increases from 32 to 64, the retry rate per second decreases from 1.2% to 0.6%.

---

### 7.20 Experiment Section — Variation Pattern
The following sections are similar, but to prevent duplicate translations, the vocabulary and order are slightly changed with each iteration.
- Scenario: NVMe-oF I/O retries
- Conditions: TCP RTT of 2ms, loss rate of 0.1%
- Expected result: Retry rate below 1%

#### Procedures
1. Input data: `/data/input_20.jsonl`
2. Options: `--batch 512 --timeout 3s --enable-cache`
3. Execution: `app run --job test-20 --qos high`
4. Verification: Check if `test-20 finished` is included in the logs

#### Observations
- As the GC cycle length increases, there is a tendency for P99 latency to increase.
- When the cache miss rate increases by 10%, throughput decreases by approximately 7%.
- When the connection pool size increases from 32 to 64, the retry rate per second decreases from 1.2% to 0.6%.

---

### 7.21 Experiment Section — Variation Pattern
The following sections are similar, but to prevent duplicate translations, the vocabulary and order are slightly changed with each iteration.
- Scenario: Kubernetes deployment
- Conditions: HPA enabled
- Expected result: Operation within a scale range of 2 to 10

#### Procedures
1. Input data: `/data/input_21.jsonl`
2. Options: `--batch 512 --timeout 3s --enable-cache`
3. Execution: `app run --job test-21 --qos high`
4. Verification: Check if `test-21 finished` is included in the logs

#### Observations
- As the GC cycle length increases, there is a tendency for P99 latency to increase.
- When the cache miss rate increases by 10%, throughput decreases by approximately 7%.
- When the connection pool size increases from 32 to 64, the retry rate per second decreases from 1.2% to 0.6%.

---

### 7.22 Experiment Section — Variation Pattern
The following sections are similar, but to prevent duplicate translations, the vocabulary and order are slightly changed with each iteration.
- Scenario: Mermaid rendering
- Conditions: 50+ nodes, 100+ edges
- Expected result: No layout distortion

#### Procedures
1. Input data: `/data/input_22.jsonl`
2. Options: `--batch 512 --timeout 3s --enable-cache`
3. Execution: `app run --job test-22 --qos high`
4. Verification: Check if `test-22 finished` is included in the logs

#### Observations
- As the GC cycle length increases, there is a tendency for P99 latency to increase.
- When the cache miss rate increases by 10%, throughput decreases by approximately 7%.
- When the connection pool size increases from 32 to 64, the retry rate per second decreases from 1.2% to 0.6%.

---

### 7.23 Experiment Section — Variation Pattern
The following sections are similar, but to prevent duplicate translations, the vocabulary and order are slightly changed with each iteration.
- Scenario: Large-scale JSON parsing
- Conditions: 64MB payload, 4 workers
- Expected result: Completion without memory spikes

#### Procedures
1. Input data: `/data/input_23.jsonl`
2. Options: `--batch 512 --timeout 3s --enable-cache`
3. Execution: `app run --job test-23 --qos high`
4. Verification: Check if `test-23 finished` is included in the logs
```

## CRITICAL INSTRUCTIONS - FOLLOW STRICTLY ##

1. **Preserve Structure:** All markdown syntax—including headings (`#`), lists (`-`, `1.`), code blocks (```), inline code (`...`), links (`[]()`), images, tables, blockquotes (`>`), and horizontal rules (`---`)—MUST be kept exactly as they are.
2. **Translate Content Only:** Only translate the human-readable Korean text.
3. **DO NOT Translate Non-Text Elements:**
    - Code within fenced code blocks (```...```) and inline code (`...`).
    - URLs, file paths, and technical identifiers.
    - YAML Frontmatter.
    - HTML/XML tags.
4. **No Extra Formatting:** Do not add or remove any markdown elements. Do not introduce new formatting.
5. **Output Only Translation:** Your response must contain ONLY the translated markdown content and nothing else. Do not add introductory phrases like "Here is the English translation:".
6. **Complete Code Blocks:** If the input contains code blocks (```), ensure ALL code blocks are properly closed with ```. Never leave a code block unclosed.


#### Observations
- As the GC cycle length increases, there is a tendency for P99 latency to increase.
- When the cache miss rate increases by 10%, throughput decreases by approximately 7%.
- When the connection pool size increases from 32 to 64, the retry rate per second decreases from 1.2% to 0.6%.

---

### 7.24 Experiment Section — Variation Patterns
The following sections are similar, but to prevent duplicate translations, the vocabulary and order are slightly changed with each iteration.
- Scenario: Mermaid rendering
- Conditions: 50+ nodes, 100+ edges
- Expected Result: No layout distortion

#### Procedures
1. Input data: `/data/input_24.jsonl`
2. Options: `--batch 512 --timeout 3s --enable-cache`
3. Execution: `app run --job test-24 --qos high`
4. Verification: Check if `test-24 finished` is included in the logs

#### Observations
- As the GC cycle length increases, there is a tendency for P99 latency to increase.
- When the cache miss rate increases by 10%, throughput decreases by approximately 7%.
- When the connection pool size increases from 32 to 64, the retry rate per second decreases from 1.2% to 0.6%.

---

### 7.25 Experiment Section — Variation Patterns
The following sections are similar, but to prevent duplicate translations, the vocabulary and order are slightly changed with each iteration.
- Scenario: Kubernetes deployment
- Conditions: HPA enabled
- Expected Result: Functioning within a scale range of 2 to 10

#### Procedures
1. Input data: `/data/input_25.jsonl`
2. Options: `--batch 512 --timeout 3s --enable-cache`
3. Execution: `app run --job test-25 --qos high`
4. Verification: Check if `test-25 finished` is included in the logs

#### Observations
- As the GC cycle length increases, there is a tendency for P99 latency to increase.
- When the cache miss rate increases by 10%, throughput decreases by approximately 7%.
- When the connection pool size increases from 32 to 64, the retry rate per second decreases from 1.2% to 0.6%.

---

### 7.26 Experiment Section — Variation Patterns
The following sections are similar, but to prevent duplicate translations, the vocabulary and order are slightly changed with each iteration.
- Scenario: NVMe-oF I/O retries
- Conditions: TCP RTT of 2ms, loss of 0.1%
- Expected Result: Retry rate below 1%

#### Procedures
1. Input data: `/data/input_26.jsonl`
2. Options: `--batch 512 --timeout 3s --enable-cache`
3. Execution: `app run --job test-26 --qos high`
4. Verification: Check if `test-26 finished` is included in the logs

#### Observations
- As the GC cycle length increases, there is a tendency for P99 latency to increase.
- When the cache miss rate increases by 10%, throughput decreases by approximately 7%.
- When the connection pool size increases from 32 to 64, the retry rate per second decreases from 1.2% to 0.6%.

---

### 7.27 Experiment Section — Variation Patterns
The following sections are similar, but to prevent duplicate translations, the vocabulary and order are slightly changed with each iteration.
- Scenario: Summary of conversation records
- Conditions: Including 100k Korean characters
- Expected Result: Summary rate of over 90%

#### Procedures
1. Input data: `/data/input_27.jsonl`
2. Options: `--batch 512 --timeout 3s --enable-cache`
3. Execution: `app run --job test-27 --qos high`
4. Verification: Check if `test-27 finished` is included in the logs
```

## CRITICAL INSTRUCTIONS - FOLLOW STRICTLY ##
1. **Preserve Structure:** All markdown syntax—including headings (`#`), lists (`-`, `1.`), code blocks (```), inline code (`...`), links (`[]()`), images, tables, blockquotes (`>`), and horizontal rules (`---`)—MUST be kept exactly as they are.
2. **Translate Content Only:** Only translate the human-readable Korean text.
3. **DO NOT Translate Non-Text Elements:**
    - Code within fenced code blocks (```...```) and inline code (`...`).
    - URLs, file paths, and technical identifiers.
    - YAML Frontmatter.
    - HTML/XML tags.
4. **No Extra Formatting:** Do not add or remove any markdown elements. Do not introduce new formatting.
5. **Output Only Translation:** Your response must contain ONLY the translated markdown content and nothing else. Do not add introductory phrases like "Here is the English translation:".
6. **Complete Code Blocks:** If the input contains code blocks (```), ensure ALL code blocks are properly closed with ```. Never leave a code block unclosed.


#### Observations
- As the GC cycle length increases, there is a tendency for P99 latency to increase.
- When the cache miss rate increases by 10%, throughput decreases by approximately 7%.
- When the connection pool size increases from 32 to 64, the retry rate per second decreases from 1.2% to 0.6%.

---

### Experiment Section 7.28 — Variation Patterns
The following paragraphs are similar, but to prevent duplicate translations, the vocabulary and order are slightly changed with each iteration.
- Scenario: Summary of conversation records
- Conditions: Including 100,000 Korean characters
- Expected result: A summary rate of over 90%.

#### Procedures
1. Input data: `/data/input_28.jsonl`
2. Options: `--batch 512 --timeout 3s --enable-cache`
3. Execution: `app run --job test-28 --qos high`
4. Verification: Check if `test-28 finished` is included in the logs

#### Observations
- As the GC cycle length increases, there is a tendency for P99 latency to increase.
- When the cache miss rate increases by 10%, throughput decreases by approximately 7%.
- When the connection pool size increases from 32 to 64, the retry rate per second decreases from 1.2% to 0.6%.

---

### Experiment Section 7.29 — Variation Patterns
The following paragraphs are similar, but to prevent duplicate translations, the vocabulary and order are slightly changed with each iteration.
- Scenario: Parsing large JSON data
- Conditions: 64MB payload, 4 workers
- Expected result: Completion without memory spikes

#### Procedures
1. Input data: `/data/input_29.jsonl`
2. Options: `--batch 512 --timeout 3s --enable-cache`
3. Execution: `app run --job test-29 --qos high`
4. Verification: Check if `test-29 finished` is included in the logs

#### Observations
- As the GC cycle length increases, there is a tendency for P99 latency to increase.
- When the cache miss rate increases by 10%, throughput decreases by approximately 7%.
- When the connection pool size increases from 32 to 64, the retry rate per second decreases from 1.2% to 0.6%.

---

### Experiment Section 7.30 — Variation Patterns
The following paragraphs are similar, but to prevent duplicate translations, the vocabulary and order are slightly changed with each iteration.
- Scenario: Summary of conversation records
- Conditions: Including 100,000 Korean characters
- Expected result: A summary rate of over 90%.

#### Procedures
1. Input data: `/data/input_30.jsonl`
2. Options: `--batch 512 --timeout 3s --enable-cache`
3. Execution: `app run --job test-30 --qos high`
4. Verification: Check if `test-30 finished` is included in the logs

#### Observations
- As the GC cycle length increases, there is a tendency for P99 latency to increase.
- When the cache miss rate increases by 10%, throughput decreases by approximately 7%.
- When the connection pool size increases from 32 to 64, the retry rate per second decreases from 1.2% to 0.6%.

---

### Experiment Section 7.31 — Variation Patterns
The following paragraphs are similar, but to prevent duplicate translations, the vocabulary and order are slightly changed with each iteration.
- Scenario: Kubernetes deployment
- Conditions: HPA (Horizontal Pod Autoscaling) activated
- Expected result: Operation within a scale range of 2 to 10

#### Procedures
1. Input data: `/data/input_31.jsonl`
2. Options: `--batch 512 --timeout 3s --enable-cache`
3. Execution: `app run --job test-31 --qos high`
4. Verification: Check if `test-31 finished` is included in the logs
```

## CRITICAL INSTRUCTIONS - FOLLOW STRICTLY ##

1. **Preserve Structure:** All markdown syntax—including headings (`#`), lists (`-`, `1.`), code blocks (```), inline code (`...`), links (`[]()`), images, tables, blockquotes (`>`), and horizontal rules (`---`)—MUST be kept exactly as they are.
2. **Translate Content Only:** Only translate the human-readable Korean text.
3. **DO NOT Translate Non-Text Elements:**
    - Code within fenced code blocks (```...```) and inline code (`...`).
    - URLs, file paths, and technical identifiers.
    - YAML Frontmatter.
    - HTML/XML tags.
4. **No Extra Formatting:** Do not add or remove any markdown elements. Do not introduce new formatting.
5. **Output Only Translation:** Your response must contain ONLY the translated markdown content and nothing else. Do not add introductory phrases like "Here is the English translation:".
6. **Complete Code Blocks:** If the input contains code blocks (```), ensure ALL code blocks are properly closed with ```. Never leave a code block unclosed.


#### Observations
- As the GC cycle length increases, there is a tendency for P99 latency to increase.
- When the cache miss rate increases by 10%, throughput decreases by approximately 7%.
- When the connection pool size increases from 32 to 64, the retry rate per second decreases from 1.2% to 0.6%.

---

### 7.32 Experiment Section — Variation Patterns
The following sections are similar, but to prevent duplicate translations, the vocabulary and order are slightly changed with each iteration.
- Scenario: Mermaid rendering
- Conditions: 50+ nodes, 100+ edges
- Expected result: No layout distortion

#### Procedures
1. Input data: `/data/input_32.jsonl`
2. Options: `--batch 512 --timeout 3s --enable-cache`
3. Execution: `app run --job test-32 --qos high`
4. Verification: Check if `test-32 finished` is included in the logs

#### Observations
- As the GC cycle length increases, there is a tendency for P99 latency to increase.
- When the cache miss rate increases by 10%, throughput decreases by approximately 7%.
- When the connection pool size increases from 32 to 64, the retry rate per second decreases from 1.2% to 0.6%.

---

### 7.33 Experiment Section — Variation Patterns
The following sections are similar, but to prevent duplicate translations, the vocabulary and order are slightly changed with each iteration.
- Scenario: Parsing large JSON files
- Conditions: 64MB payload, 4 workers
- Expected result: Completion without memory spikes

#### Procedures
1. Input data: `/data/input_33.jsonl`
2. Options: `--batch 512 --timeout 3s --enable-cache`
3. Execution: `app run --job test-33 --qos high`
4. Verification: Check if `test-33 finished` is included in the logs

#### Observations
- As the GC cycle length increases, there is a tendency for P99 latency to increase.
- When the cache miss rate increases by 10%, throughput decreases by approximately 7%.
- When the connection pool size increases from 32 to 64, the retry rate per second decreases from 1.2% to 0.6%.

---

### 7.34 Experiment Section — Variation Patterns
The following sections are similar, but to prevent duplicate translations, the vocabulary and order are slightly changed with each iteration.
- Scenario: Kubernetes deployment
- Conditions: HPA (Horizontal Pod Auto Scaling) activated
- Expected result: Functioning within a scale range of 2 to 10

#### Procedures
1. Input data: `/data/input_34.jsonl`
2. Options: `--batch 512 --timeout 3s --enable-cache`
3. Execution: `app run --job test-34 --qos high`
4. Verification: Check if `test-34 finished` is included in the logs

#### Observations
- As the GC cycle length increases, there is a tendency for P99 latency to increase.
- When the cache miss rate increases by 10%, throughput decreases by approximately 7%.
- When the connection pool size increases from 32 to 64, the retry rate per second decreases from 1.2% to 0.6%.

---

### 7.35 Experiment Section — Variation Patterns
The following sections are similar, but to prevent duplicate translations, the vocabulary and order are slightly changed with each iteration.
- Scenario: Mermaid rendering
- Conditions: 50+ nodes, 100+ edges
- Expected result: No layout distortion

#### Procedures
1. Input data: `/data/input_35.jsonl`
2. Options: `--batch 512 --timeout 3s --enable-cache`
3. Execution: `app run --job test-35 --qos high`
4. Verification: Check if `test-35 finished` is included in the logs
```

## CRITICAL INSTRUCTIONS - FOLLOW STRICTLY ##

1. **Preserve Structure:** All markdown syntax—including headings (`#`), lists (`-`, `1.`), code blocks (```), inline code (`...`), links (`[]()`), images, tables, blockquotes (`>`), and horizontal rules (`---`)—MUST be kept exactly as they are.
2. **Translate Content Only:** Only translate the human-readable Korean text.
3. **DO NOT Translate Non-Text Elements:**
    - Code within fenced code blocks (```...```) and inline code (`...`).
    - URLs, file paths, and technical identifiers.
    - YAML Frontmatter.
    - HTML/XML tags.
4. **No Extra Formatting:** Do not add or remove any markdown elements. Do not introduce new formatting.
5. **Output Only Translation:** Your response must contain ONLY the translated markdown content and nothing else. Do not add introductory phrases like "Here is the English translation:".
6. **Complete Code Blocks:** If the input contains code blocks (```), ensure ALL code blocks are properly closed with ```. Never leave a code block unclosed.


#### Observations
- As the GC cycle length increases, there is a tendency for P99 latency to increase.
- When the cache miss rate increases by 10%, throughput decreases by approximately 7%.
- When the connection pool size increases from 32 to 64, the retry rate per second decreases from 1.2% to 0.6%.

---

### 7.36 Experiment Section — Variation Pattern
The following sections are similar, but to prevent duplicate translations, the wording and order are slightly changed with each iteration.
- Scenario: NVMe-oF I/O retries
- Conditions: TCP RTT of 2ms, loss rate of 0.1%
- Expected result: Retry rate of less than 1%

#### Procedure
1. Input data: `/data/input_36.jsonl`
2. Options: `--batch 512 --timeout 3s --enable-cache`
3. Execution: `app run --job test-36 --qos high`
4. Verification: Check if `test-36 finished` is included in the logs

#### Observations
- As the GC cycle length increases, there is a tendency for P99 latency to increase.
- When the cache miss rate increases by 10%, throughput decreases by approximately 7%.
- When the connection pool size increases from 32 to 64, the retry rate per second decreases from 1.2% to 0.6%.

---

### 7.37 Experiment Section — Variation Pattern
The following sections are similar, but to prevent duplicate translations, the wording and order are slightly changed with each iteration.
- Scenario: Parsing large JSON files
- Conditions: 64MB payload, 4 workers
- Expected result: Completion without memory spikes

#### Procedure
1. Input data: `/data/input_37.jsonl`
2. Options: `--batch 512 --timeout 3s --enable-cache`
3. Execution: `app run --job test-37 --qos high`
4. Verification: Check if `test-37 finished` is included in the logs

#### Observations
- As the GC cycle length increases, there is a tendency for P99 latency to increase.
- When the cache miss rate increases by 10%, throughput decreases by approximately 7%.
- When the connection pool size increases from 32 to 64, the retry rate per second decreases from 1.2% to 0.6%.

---

### 7.38 Experiment Section — Variation Pattern
The following sections are similar, but to prevent duplicate translations, the wording and order are slightly changed with each iteration.
- Scenario: Mermaid rendering
- Conditions: 50+ nodes, 100+ edges
- Expected result: No layout distortion

#### Procedure
1. Input data: `/data/input_38.jsonl`
2. Options: `--batch 512 --timeout 3s --enable-cache`
3. Execution: `app run --job test-38 --qos high`
4. Verification: Check if `test-38 finished` is included in the logs

#### Observations
- As the GC cycle length increases, there is a tendency for P99 latency to increase.
- When the cache miss rate increases by 10%, throughput decreases by approximately 7%.
- When the connection pool size increases from 32 to 64, the retry rate per second decreases from 1.2% to 0.6%.

---

### 7.39 Experiment Section — Variation Pattern
The following sections are similar, but to prevent duplicate translations, the wording and order are slightly changed with each iteration.
- Scenario: Mermaid rendering
- Conditions: 50+ nodes, 100+ edges
- Expected result: No layout distortion

#### Procedure
1. Input data: `/data/input_39.jsonl`
2. Options: `--batch 512 --timeout 3s --enable-cache`
3. Execution: `app run --job test-39 --qos high`
4. Verification: Check if `test-39 finished` is included in the logs
```

## CRITICAL INSTRUCTIONS - FOLLOW STRICTLY ##

1. **Preserve Structure:** All markdown syntax—including headings (`#`), lists (`-`, `1.`), code blocks (```), inline code (`...`), links (`[]()`), images, tables, blockquotes (`>`), and horizontal rules (`---`)—MUST be kept exactly as they are.
2. **Translate Content Only:** Only translate the human-readable Korean text.
3. **DO NOT Translate Non-Text Elements:**
    - Code within fenced code blocks (```...```) and inline code (`...`).
    - URLs, file paths, and technical identifiers.
    - YAML Frontmatter.
    - HTML/XML tags.
4. **No Extra Formatting:** Do not add or remove any markdown elements. Do not introduce new formatting.
5. **Output Only Translation:** Your response must contain ONLY the translated markdown content and nothing else. Do not add introductory phrases like "Here is the English translation:".
6. **Complete Code Blocks:** If the input contains code blocks (```), ensure ALL code blocks are properly closed with ```. Never leave a code block unclosed.


Korean Markdown Document:
#### Observations
- As the GC cycle length increases, there is a tendency for P99 latency to increase.
- When the cache miss rate increases by 10%, throughput decreases by approximately 7%.
- When the connection pool size is increased from 32 to 64, the retry rate per second decreases from 1.2% to 0.6%.

---

### 7.40 Experiment Paragraph — Variation Patterns
The following paragraph is similar, but to prevent duplicate translations, the vocabulary and order are slightly changed with each iteration.
- Scenario: Summary of conversation records
- Condition: Including 100,000 Korean characters
- Expected result: A summary rate of over 90%

#### Procedure
1. Input data: `/data/input_40.jsonl`
2. Options: `--batch 512 --timeout 3s --enable-cache`
3. Execution: `app run --job test-40 --qos high`
4. Verification: Check if `test-40 finished` is included in the logs

#### Observations
- As the GC cycle length increases, there is a tendency for P99 latency to increase.
- When the cache miss rate increases by 10%, throughput decreases by approximately 7%.
- When the connection pool size is increased from 32 to 64, the retry rate per second decreases from 1.2% to 0.6%.

---
```

## CRITICAL INSTRUCTIONS - FOLLOW STRICTLY ##

1. **Preserve Structure:** All markdown syntax—including headings (`#`), lists (`-`, `1.`), code blocks (```), inline code (`...`), links (`[]()`), images, tables, blockquotes (`>`), and horizontal rules (`---`)—MUST be kept exactly as they are.
2. **Translate Content Only:** Only translate the human-readable Korean text.
3. **DO NOT Translate Non-Text Elements:**
    - Code within fenced code blocks (```...```) and inline code (`...`).
    - URLs, file paths, and technical identifiers.
    - YAML Frontmatter.
    - HTML/XML tags.
4. **No Extra Formatting:** Do not add or remove any markdown elements. Do not introduce new formatting.
5. **Output Only Translation:** Your response must contain ONLY the translated markdown content and nothing else. Do not add introductory phrases like "Here is the English translation:".
6. **Complete Code Blocks:** If the input contains code blocks (```), ensure ALL code blocks are properly closed with ```. Never leave a code block unclosed.


Korean Markdown Document:
## 8. Long Lists

- 2. Consistency in Error Handling — Case #001
- 3. Performance Profiling — Case #002
- 4. Accessibility (a11y) — Case #003
- 5. Log Schema Stability — Case #004
- 6. Cache Invalidation Scenarios — Case #005
- 7. Performance Profiling — Case #006
- 8. Performance Profiling — Case #007
- 9. API Backward Compatibility — Case #008
- 10. Log Schema Stability — Case #009
- 11. Accessibility (a11y) — Case #010
- 12. Cache Invalidation Scenarios — Case #011
- 13. Performance Profiling — Case #012
- 14. Application of Security Headers — Case #013
- 15. Internationalization (i18n) — Case #014
- 16. Resource Leak Detection — Case #015
- 17. Consistency in Error Handling — Case #016
- 18. Consistency in Error Handling — Case #017
- 19. Internationalization (i18n) — Case #018
- 20. CORS Policy Verification — Case #019
- 21. Performance Profiling — Case #020
- 22. Application of Security Headers — Case #021
- 23. Log Schema Stability — Case #022
- 24. Performance Profiling — Case #023
- 25. Cache Invalidation Scenarios — Case #024
- 26. CORS Policy Verification — Case #025
- 27. Performance Profiling — Case #026
- 28. Accessibility (a11y) — Case #027
- 29. Accessibility (a11y) — Case #028
- 30. API Backward Compatibility — Case #029
- 31. Cache Invalidation Scenarios — Case #030
- 32. Cache Invalidation Scenarios — Case #031
- 33. Performance Profiling — Case #032
- 34. Resource Leak Detection — Case #033
- 35. Log Schema Stability — Case #034
- 36. CORS Policy Verification — Case #035
- 37. Consistency in Error Handling — Case #036
- 38. Resource Leak Detection — Case #037
- 39. Consistency in Error Handling — Case #038
- 40. Internationalization (i18n) — Case #039
- 41. API Backward Compatibility — Case #040
- 42. CORS Policy Verification — Case #041
- 43. Cache Invalidation Scenarios — Case #042
- 44. Cache Invalidation Scenarios — Case #043
- 45. Performance Profiling — Case #044
- 46. Performance Profiling — Case #045
- 47. CORS Policy Verification — Case #046
- 48. Resource Leak Detection — Case #047
- 49. Cache Invalidation Scenarios — Case #048
- 50. Consistency in Error Handling — Case #049
- 51. Log Schema Stability — Case #050
- 52. Resource Leak Detection — Case #051
- 53. Internationalization (i18n) — Case #052
- 54. Log Schema Stability — Case #053
- 55. Resource Leak Detection — Case #054
- 56. Application of Security Headers — Case #055
- 57. Internationalization (i18n) — Case #056
- 58. API Backward Compatibility — Case #057
```

## CRITICAL INSTRUCTIONS - FOLLOW STRICTLY ##

1. **Preserve Structure:** All markdown syntax—including headings (`#`), lists (`-`, `1.`), code blocks (```), inline code (`...`), links (`[]()`), images, tables, blockquotes (`>`), and horizontal rules (`---`)—MUST be kept exactly as they are.
2. **Translate Content Only:** Only translate the human-readable Korean text.
3. **DO NOT Translate Non-Text Elements:**
    - Code within fenced code blocks (```...```) and inline code (`...`).
    - URLs, file paths, and technical identifiers.
    - YAML Frontmatter.
    - HTML/XML tags.
4. **No Extra Formatting:** Do not add or remove any markdown elements. Do not introduce new formatting.
5. **Output Only Translation:** Your response must contain ONLY the translated markdown content and nothing else. Do not add introductory phrases like "Here is the English translation:".
6. **Complete Code Blocks:** If the input contains code blocks (```), ensure ALL code blocks are properly closed with ```. Never leave a code block unclosed.


Korean Markdown Document:
- 59. Accessibility (a11y) — Case #058
- 60. API Backward Compatibility — Case #059
- 61. Performance Profiling — Case #060
- 62. Accessibility (a11y) — Case #061
- 63. API Backward Compatibility — Case #062
- 64. Internationalization (i18n) — Case #063
- 65. Application of Security Headers — Case #064
- 66. Consistency in Error Handling — Case #065
- 67. Performance Profiling — Case #066
- 68. Accessibility (a11y) — Case #067
- 69. Consistency in Error Handling — Case #068
- 70. Performance Profiling — Case #069
- 71. Resource Leak Detection — Case #070
- 72. Accessibility (a11y) — Case #071
- 73. Internationalization (i18n) — Case #072
- 74. Consistency in Error Handling — Case #073
- 75. Internationalization (i18n) — Case #074
- 76. Performance Profiling — Case #075
- 77. Application of Security Headers — Case #076
- 78. CORS Policy Verification — Case #077
- 79. Resource Leak Detection — Case #078
- 80. Resource Leak Detection — Case #079
- 81. Performance Profiling — Case #080
- 82. Accessibility (a11y) — Case #081
- 83. Accessibility (a11y) — Case #082
- 84. Performance Profiling — Case #083
- 85. Resource Leak Detection — Case #084
- 86. Accessibility (a11y) — Case #085
- 87. Cache Invalidation Scenarios — Case #086
- 88. CORS Policy Verification — Case #087
- 89. Log Schema Stability — Case #088
- 90. CORS Policy Verification — Case #089
- 91. Application of Security Headers — Case #090
- 92. API Backward Compatibility — Case #091
- 93. Accessibility (a11y) — Case #092
- 94. Performance Profiling — Case #093
- 95. Performance Profiling — Case #094
- 96. Log Schema Stability — Case #095
- 97. Internationalization (i18n) — Case #096
- 98. API Backward Compatibility — Case #097
- 99. Consistency in Error Handling — Case #098
- 100. Cache Invalidation Scenarios — Case #099
- 101. Accessibility (a11y) — Case #100
- 102. Accessibility (a11y) — Case #101
- 103. Internationalization (i18n) — Case #102
- 104. Accessibility (a11y) — Case #103
- 105. API Backward Compatibility — Case #104
- 106. Accessibility (a11y) — Case #105
- 107. Performance Profiling — Case #106
- 108. Application of Security Headers — Case #107
- 109. API Backward Compatibility — Case #108
- 110. Application of Security Headers — Case #109
- 111. Consistency in Error Handling — Case #110
- 112. Performance Profiling — Case #111
- 113. Resource Leak Detection — Case #112
- 114. CORS Policy Verification — Case #113
- 115. Accessibility (a11y) — Case #114
- 116. Consistency in Error Handling — Case #115
- 117. Consistency in Error Handling — Case #116
- 118. Performance Profiling — Case #117
- 119. CORS Policy Verification — Case #118
- 120. Resource Leak Detection — Case #119
- 121. Cache Invalidation Scenarios — Case #120
- 122. CORS Policy Verification — Case #121
- 123. Performance Profiling — Case #122
- 124. Consistency in Error Handling — Case #123
- 125. Performance Profiling — Case #124
- 126. Performance Profiling — Case #125
- 127. Accessibility (a11y) — Case #126
- 128. Accessibility (a11y) — Case #127
- 129. Consistency in Error Handling — Case #128
- 130. Consistency in Error Handling — Case #129
- 131. API Backward Compatibility — Case #130
- 132. Accessibility (a11y) — Case #131
- 133. API Backward Compatibility — Case #132
```

## CRITICAL INSTRUCTIONS - FOLLOW STRICTLY ##

1. **Preserve Structure:** All markdown syntax—including headings (`#`), lists (`-`, `1.`), code blocks (```), inline code (`...`), links (`[]()`), images, tables, blockquotes (`>`), and horizontal rules (`---`)—MUST be kept exactly as they are.
2. **Translate Content Only:** Only translate the human-readable Korean text.
3. **DO NOT Translate Non-Text Elements:**
    - Code within fenced code blocks (```...```) and inline code (`...`).
    - URLs, file paths, and technical identifiers.
    - YAML Frontmatter.
    - HTML/XML tags.
4. **No Extra Formatting:** Do not add or remove any markdown elements. Do not introduce new formatting.
5. **Output Only Translation:** Your response must contain ONLY the translated markdown content and nothing else. Do not add introductory phrases like "Here is the English translation:".
6. **Complete Code Blocks:** If the input contains code blocks (```), ensure ALL code blocks are properly closed with ```. Never leave a code block unclosed.


Korean Markdown Document:
- 134. Cache invalidation scenarios — Case #133
- 135. Application of security headers — Case #134
- 136. Internationalization (i18n) — Case #135
- 137. Application of security headers — Case #136
- 138. Performance profiling — Case #137
- 139. Performance profiling — Case #138
- 140. CORS policy verification — Case #139
- 141. Internationalization (i18n) — Case #140
- 142. Log schema stability — Case #141
- 143. CORS policy verification — Case #142
- 144. Accessibility (a11y) — Case #143
- 145. Application of security headers — Case #144
- 146. Log schema stability — Case #145
- 147. Performance profiling — Case #146
- 148. Performance profiling — Case #147
- 149. API backward compatibility — Case #148
- 150. Resource leak detection — Case #149
- 151. Performance profiling — Case #150
- 152. Resource leak detection — Case #151
- 153. Accessibility (a11y) — Case #152
- 154. API backward compatibility — Case #153
- 155. Accessibility (a11y) — Case #154
- 156. Application of security headers — Case #155
- 157. Accessibility (a11y) — Case #156
- 158. Performance profiling — Case #157
- 159. Cache invalidation scenarios — Case #158
- 160. Application of security headers — Case #159
- 161. Consistency in error handling — Case #160
- 162. Log schema stability — Case #161
- 163. Performance profiling — Case #162
- 164. Accessibility (a11y) — Case #163
- 165. Consistency in error handling — Case #164
- 166. Resource leak detection — Case #165
- 167. Log schema stability — Case #166
- 168. Internationalization (i18n) — Case #167
- 169. Cache invalidation scenarios — Case #168
- 170. Internationalization (i18n) — Case #169
- 171. Cache invalidation scenarios — Case #170
- 172. Resource leak detection — Case #171
- 173. Application of security headers — Case #172
- 174. Resource leak detection — Case #173
- 175. Consistency in error handling — Case #174
- 176. Resource leak detection — Case #175
- 177. Log schema stability — Case #176
- 178. CORS policy verification — Case #177
- 179. Application of security headers — Case #178
- 180. Log schema stability — Case #179
- 181. Performance profiling — Case #180
- 182. Resource leak detection — Case #181
- 183. Internationalization (i18n) — Case #182
- 184. Log schema stability — Case #183
- 185. Accessibility (a11y) — Case #184
- 186. Application of security headers — Case #185
- 187. Resource leak detection — Case #186
- 188. Resource leak detection — Case #187
- 189. Accessibility (a11y) — Case #188
- 190. Cache invalidation scenarios — Case #189
- 191. Accessibility (a11y) — Case #190
- 192. Cache invalidation scenarios — Case #191
- 193. Consistency in error handling — Case #192
- 194. Consistency in error handling — Case #193
- 195. Resource leak detection — Case #194
- 196. Consistency in error handling — Case #195
- 197. CORS policy verification — Case #196
- 198. Performance profiling — Case #197
- 199. Resource leak detection — Case #198
- 200. Accessibility (a11y) — Case #199
- 201. Resource leak detection — Case #200
- 202. Cache invalidation scenarios — Case #201
- 203. Internationalization (i18n) — Case #202
- 204. Log schema stability — Case #203
```

## CRITICAL INSTRUCTIONS - FOLLOW STRICTLY ##

1. **Preserve Structure:** All markdown syntax—including headings (`#`), lists (`-`, `1.`), code blocks (```), inline code (`...`), links (`[]()`), images, tables, blockquotes (`>`), and horizontal rules (`---`)—MUST be kept exactly as they are.
2. **Translate Content Only:** Only translate the human-readable Korean text.
3. **DO NOT Translate Non-Text Elements:**
    - Code within fenced code blocks (```...```) and inline code (`...`).
    - URLs, file paths, and technical identifiers.
    - YAML Frontmatter.
    - HTML/XML tags.
4. **No Extra Formatting:** Do not add or remove any markdown elements. Do not introduce new formatting.
5. **Output Only Translation:** Your response must contain ONLY the translated markdown content and nothing else. Do not add introductory phrases like "Here is the English translation:".
6. **Complete Code Blocks:** If the input contains code blocks (```), ensure ALL code blocks are properly closed with ```. Never leave a code block unclosed.


Korean Markdown Document:
- 205. 에러 처리 일관성 — Case #204
- 206. 리소스 누수 점검 — Case #205
- 207. 보안 헤더 적용 — Case #206
- 208. 리소스 누수 점검 — Case #207
- 209. 캐시 무효화 시나리오 — Case #208
- 210. 성능 프로파일링 — Case #209
- 211. 보안 헤더 적용 — Case #210
- 212. 국제화(i18n) — Case #211
- 213. 로그 스키마 안정성 — Case #212
- 214. 에러 처리 일관성 — Case #213
- 215. 캐시 무효화 시나리오 — Case #214
- 216. 보안 헤더 적용 — Case #215
- 217. 국제화(i18n) — Case #216
- 218. 보안 헤더 적용 — Case #217
- 219. 성능 프로파일링 — Case #218
- 220. 에러 처리 일관성 — Case #219
- 221. 보안 헤더 적용 — Case #220
- 222. 성능 프로파일링 — Case #221
- 223. API 역호환성 — Case #222
- 224. 리소스 누수 점검 — Case #223
- 225. 국제화(i18n) — Case #224
- 226. 보안 헤더 적용 — Case #225
- 227. 국제화(i18n) — Case #226
- 228. 성능 프로파일링 — Case #227
- 229. 로그 스키마 안정성 — Case #228
- 230. CORS 정책 검증 — Case #229
- 231. 성능 프로파일링 — Case #230
- 232. API 역호환성 — Case #231
- 233. CORS 정책 검증 — Case #232
- 234. 국제화(i18n) — Case #233
- 235. 에러 처리 일관성 — Case #234
- 236. 성능 프로파일링 — Case #235
- 237. 에러 처리 일관성 — Case #236
- 238. 성능 프로파일링 — Case #237
- 239. 보안 헤더 적용 — Case #238
- 240. 에러 처리 일관성 — Case #239
- 241. CORS 정책 검증 — Case #240
- 242. API 역호환성 — Case #241
- 243. 성능 프로파일링 — Case #242
- 244. 캐시 무효화 시나리오 — Case #243
- 245. 성능 프로파일링 — Case #244
- 246. 보안 헤더 적용 — Case #245
- 247. 에러 처리 일관성 — Case #246
- 248. 국제화(i18n) — Case #247
- 249. 로그 스키마 안정성 — Case #248
- 250. 보안 헤더 적용 — Case #249
- 251. 접근성(a11y) — Case #250
- 252. 접근성(a11y) — Case #251
- 253. 국제화(i18n) — Case #252
- 254. 국제화(i18n) — Case #253
- 255. CORS 정책 검증 — Case #254
- 256. 로그 스키마 안정성 — Case #255
- 257. CORS 정책 검증 — Case #256
- 258. 보안 헤더 적용 — Case #257
- 259. 캐시 무효화 시나리오 — Case #258
- 260. 에러 처리 일관성 — Case #259
- 261. 접근성(a11y) — Case #260
- 262. 리소스 누수 점검 — Case #261
- 263. 리소스 누수 점검 — Case #262
- 264. 성능 프로파일링 — Case #263
- 265. 접근성(a11y) — Case #264
- 266. 캐시 무효화 시나리오 — Case #265
- 267. 보안 헤더 적용 — Case #266
- 268. 리소스 누수 점검 — Case #267
- 269. 보안 헤더 적용 — Case #268
- 270. 성능 프로파일링 — Case #269
- 271. 에러 처리 일관성 — Case #270
- 272. 국제화(i18n) — Case #271
- 273. API 역호환성 — Case #272
- 274. 에러 처리 일관성 — Case #273
- 275. 접근성(a11y) — Case #274
- 276. API 역호환성 — Case #275
- 277. 국제화(i18n) — Case #276
```

## CRITICAL INSTRUCTIONS - FOLLOW STRICTLY ##

1. **Preserve Structure:** All markdown syntax—including headings (`#`), lists (`-`, `1.`), code blocks (```), inline code (`...`), links (`[]()`), images, tables, blockquotes (`>`), and horizontal rules (`---`)—MUST be kept exactly as they are.
2. **Translate Content Only:** Only translate the human-readable Korean text.
3. **DO NOT Translate Non-Text Elements:**
    - Code within fenced code blocks (```...```) and inline code (`...`).
    - URLs, file paths, and technical identifiers.
    - YAML Frontmatter.
    - HTML/XML tags.
4. **No Extra Formatting:** Do not add or remove any markdown elements. Do not introduce new formatting.
5. **Output Only Translation:** Your response must contain ONLY the translated markdown content and nothing else. Do not add introductory phrases like "Here is the English translation:".
6. **Complete Code Blocks:** If the input contains code blocks (```), ensure ALL code blocks are properly closed with ```. Never leave a code block unclosed.


Korean Markdown Document:
- 278. CORS Policy Verification — Case #277
- 279. Application of Security Headers — Case #278
- 280. Cache Invalidation Scenarios — Case #279
- 281. Log Schema Stability — Case #280
- 282. Resource Leak Inspection — Case #281
- 283. Resource Leak Inspection — Case #282
- 284. Accessibility (a11y) — Case #283
- 285. Accessibility (a11y) — Case #284
- 286. Consistency in Error Handling — Case #285
- 287. API Backward Compatibility — Case #286
- 288. Cache Invalidation Scenarios — Case #287
- 289. Accessibility (a11y) — Case #288
- 290. Accessibility (a11y) — Case #289
- 291. Application of Security Headers — Case #290
- 292. Internationalization (i18n) — Case #291
- 293. Application of Security Headers — Case #292
- 294. CORS Policy Verification — Case #293
- 295. Resource Leak Inspection — Case #294
- 296. Application of Security Headers — Case #295
- 297. CORS Policy Verification — Case #296
- 298. Log Schema Stability — Case #297
- 299. Cache Invalidation Scenarios — Case #298
- 300. API Backward Compatibility — Case #299
- 301. Cache Invalidation Scenarios — Case #300
- 302. Internationalization (i18n) — Case #301
- 303. Accessibility (a11y) — Case #302
- 304. Performance Profiling — Case #303
- 305. API Backward Compatibility — Case #304
- 306. Consistency in Error Handling — Case #305
- 307. Accessibility (a11y) — Case #306
- 308. Resource Leak Inspection — Case #307
- 309. API Backward Compatibility — Case #308
- 310. Application of Security Headers — Case #309
- 311. CORS Policy Verification — Case #310
- 312. API Backward Compatibility — Case #311
- 313. Accessibility (a11y) — Case #312
- 314. CORS Policy Verification — Case #313
- 315. Internationalization (i18n) — Case #314
- 316. Resource Leak Inspection — Case #315
- 317. Internationalization (i18n) — Case #316
- 318. Log Schema Stability — Case #317
- 319. Application of Security Headers — Case #318
- 320. Log Schema Stability — Case #319
- 321. Consistency in Error Handling — Case #320
- 322. Performance Profiling — Case #321
- 323. Accessibility (a11y) — Case #322
- 324. Application of Security Headers — Case #323
- 325. API Backward Compatibility — Case #324
- 326. CORS Policy Verification — Case #325
- 327. Resource Leak Inspection — Case #326
- 328. CORS Policy Verification — Case #327
- 329. CORS Policy Verification — Case #328
- 330. API Backward Compatibility — Case #329
- 331. Accessibility (a11y) — Case #330
- 332. Performance Profiling — Case #331
- 333. CORS Policy Verification — Case #332
- 334. Resource Leak Inspection — Case #333
- 335. Performance Profiling — Case #334
- 336. Resource Leak Inspection — Case #335
- 337. Consistency in Error Handling — Case #336
- 338. Internationalization (i18n) — Case #337
- 339. Cache Invalidation Scenarios — Case #338
- 340. API Backward Compatibility — Case #339
- 341. Cache Invalidation Scenarios — Case #340
- 342. CORS Policy Verification — Case #341
- 343. Internationalization (i18n) — Case #342
- 344. Performance Profiling — Case #343
- 345. Performance Profiling — Case #344
- 346. Log Schema Stability — Case #345
- 347. Consistency in Error Handling — Case #346
- 348. API Backward Compatibility — Case #347
- 349. Consistency in Error Handling — Case #348
- 350. Accessibility (a11y) — Case #349
```

## CRITICAL INSTRUCTIONS - FOLLOW STRICTLY ##

1. **Preserve Structure:** All markdown syntax—including headings (`#`), lists (`-`, `1.`), code blocks (```), inline code (`...`), links (`[]()`), images, tables, blockquotes (`>`), and horizontal rules (`---`)—MUST be kept exactly as they are.
2. **Translate Content Only:** Only translate the human-readable Korean text.
3. **DO NOT Translate Non-Text Elements:**
    - Code within fenced code blocks (```...```) and inline code (`...`).
    - URLs, file paths, and technical identifiers.
    - YAML Frontmatter.
    - HTML/XML tags.
4. **No Extra Formatting:** Do not add or remove any markdown elements. Do not introduce new formatting.
5. **Output Only Translation:** Your response must contain ONLY the translated markdown content and nothing else. Do not add introductory phrases like "Here is the English translation:".
6. **Complete Code Blocks:** If the input contains code blocks (```), ensure ALL code blocks are properly closed with ```. Never leave a code block unclosed.


Korean Markdown Document:
- 351. Performance Profiling — Case #350
- 352. Accessibility (a11y) — Case #351
- 353. Consistency in Error Handling — Case #352
- 354. Cache Invalidation Scenarios — Case #353
- 355. Internationalization (i18n) — Case #354
- 356. Resource Leak Detection — Case #355
- 357. Accessibility (a11y) — Case #356
- 358. Application of Security Headers — Case #357
- 359. Resource Leak Detection — Case #358
- 360. Performance Profiling — Case #359
- 361. Resource Leak Detection — Case #360
- 362. Log Schema Stability — Case #361
- 363. Internationalization (i18n) — Case #362
- 364. Consistency in Error Handling — Case #363
- 365. Resource Leak Detection — Case #364
- 366. Accessibility (a11y) — Case #365
- 367. Log Schema Stability — Case #366
- 368. Resource Leak Detection — Case #367
- 369. Performance Profiling — Case #368
- 370. API Backward Compatibility — Case #369
- 371. Accessibility (a11y) — Case #370
- 372. Performance Profiling — Case #371
- 373. CORS Policy Verification — Case #372
- 374. Cache Invalidation Scenarios — Case #373
- 375. Application of Security Headers — Case #374
- 376. Accessibility (a11y) — Case #375
- 377. API Backward Compatibility — Case #376
- 378. Accessibility (a11y) — Case #377
- 379. Application of Security Headers — Case #378
- 380. CORS Policy Verification — Case #379
- 381. CORS Policy Verification — Case #380
- 382. Log Schema Stability — Case #381
- 383. Log Schema Stability — Case #382
- 384. Performance Profiling — Case #383
- 385. Consistency in Error Handling — Case #384
- 386. Performance Profiling — Case #385
- 387. Log Schema Stability — Case #386
- 388. Resource Leak Detection — Case #387
- 389. Accessibility (a11y) — Case #388
- 390. API Backward Compatibility — Case #389
- 391. Performance Profiling — Case #390
- 392. CORS Policy Verification — Case #391
- 393. API Backward Compatibility — Case #392
- 394. Resource Leak Detection — Case #393
- 395. Application of Security Headers — Case #394
- 396. Cache Invalidation Scenarios — Case #395
- 397. Resource Leak Detection — Case #396
- 398. Performance Profiling — Case #397
- 399. Performance Profiling — Case #398
- 400. Consistency in Error Handling — Case #399
- 401. Cache Invalidation Scenarios — Case #400
- 402. API Backward Compatibility — Case #401
- 403. Log Schema Stability — Case #402
- 404. Resource Leak Detection — Case #403
- 405. Consistency in Error Handling — Case #404
- 406. Accessibility (a11y) — Case #405
- 407. API Backward Compatibility — Case #406
- 408. API Backward Compatibility — Case #407
- 409. CORS Policy Verification — Case #408
- 410. Resource Leak Detection — Case #409
- 411. Cache Invalidation Scenarios — Case #410
- 412. Application of Security Headers — Case #411
- 413. Application of Security Headers — Case #412
- 414. Application of Security Headers — Case #413
- 415. Accessibility (a11y) — Case #414
- 416. Internationalization (i18n) — Case #415
- 417. API Backward Compatibility — Case #416
- 418. Performance Profiling — Case #417
- 419. Cache Invalidation Scenarios — Case #418
- 420. Resource Leak Detection — Case #419
- 421. Resource Leak Detection — Case #420
- 422. Log Schema Stability — Case #421
- 423. API Backward Compatibility — Case #422
```

## CRITICAL INSTRUCTIONS - FOLLOW STRICTLY ##

1. **Preserve Structure:** All markdown syntax—including headings (`#`), lists (`-`, `1.`), code blocks (```), inline code (`...`), links (`[]()`), images, tables, blockquotes (`>`), and horizontal rules (`---`)—MUST be kept exactly as they are.
2. **Translate Content Only:** Only translate the human-readable Korean text.
3. **DO NOT Translate Non-Text Elements:**
    - Code within fenced code blocks (```...```) and inline code (`...`).
    - URLs, file paths, and technical identifiers.
    - YAML Frontmatter.
    - HTML/XML tags.
4. **No Extra Formatting:** Do not add or remove any markdown elements. Do not introduce new formatting.
5. **Output Only Translation:** Your response must contain ONLY the translated markdown content and nothing else. Do not add introductory phrases like "Here is the English translation:".
6. **Complete Code Blocks:** If the input contains code blocks (```), ensure ALL code blocks are properly closed with ```. Never leave a code block unclosed.


Korean Markdown Document:
- 424. Accessibility (a11y) — Case #423
- 425. Log Schema Stability — Case #424
- 426. Cache Invalidation Scenarios — Case #425
- 427. Log Schema Stability — Case #426
- 428. Internationalization (i18n) — Case #427
- 429. Performance Profiling — Case #428
- 430. Application of Security Headers — Case #429
- 431. Consistency in Error Handling — Case #430
- 432. Resource Leak Detection — Case #431
- 433. Consistency in Error Handling — Case #432
- 434. Cache Invalidation Scenarios — Case #433
- 435. Performance Profiling — Case #434
- 436. API Backward Compatibility — Case #435
- 437. Log Schema Stability — Case #436
- 438. Cache Invalidation Scenarios — Case #437
- 439. Application of Security Headers — Case #438
- 440. Accessibility (a11y) — Case #439
- 441. API Backward Compatibility — Case #440
- 442. API Backward Compatibility — Case #441
- 443. Application of Security Headers — Case #442
- 444. Accessibility (a11y) — Case #443
- 445. Log Schema Stability — Case #444
- 446. Cache Invalidation Scenarios — Case #445
- 447. Internationalization (i18n) — Case #446
- 448. API Backward Compatibility — Case #447
- 449. Internationalization (i18n) — Case #448
- 450. Performance Profiling — Case #449
- 451. Cache Invalidation Scenarios — Case #450
- 452. CORS Policy Verification — Case #451
- 453. Application of Security Headers — Case #452
- 454. CORS Policy Verification — Case #453
- 455. Internationalization (i18n) — Case #454
- 456. Log Schema Stability — Case #455
- 457. Performance Profiling — Case #456
- 458. Performance Profiling — Case #457
- 459. Application of Security Headers — Case #458
- 460. Resource Leak Detection — Case #459
- 461. Performance Profiling — Case #460
- 462. Accessibility (a11y) — Case #461
- 463. Consistency in Error Handling — Case #462
- 464. Consistency in Error Handling — Case #463
- 465. Consistency in Error Handling — Case #464
- 466. Cache Invalidation Scenarios — Case #465
- 467. Internationalization (i18n) — Case #466
- 468. Accessibility (a11y) — Case #467
- 469. Log Schema Stability — Case #468
- 470. Internationalization (i18n) — Case #469
- 471. API Backward Compatibility — Case #470
- 472. Application of Security Headers — Case #471
- 473. API Backward Compatibility — Case #472
- 474. Consistency in Error Handling — Case #473
- 475. Log Schema Stability — Case #474
- 476. Performance Profiling — Case #475
- 477. CORS Policy Verification — Case #476
- 478. CORS Policy Verification — Case #477
- 479. Internationalization (i18n) — Case #478
- 480. Internationalization (i18n) — Case #479
- 481. CORS Policy Verification — Case #480
- 482. API Backward Compatibility — Case #481
- 483. Performance Profiling — Case #482
- 484. Log Schema Stability — Case #483
- 485. API Backward Compatibility — Case #484
- 486. Cache Invalidation Scenarios — Case #485
- 487. Consistency in Error Handling — Case #486
- 488. Performance Profiling — Case #487
- 489. Consistency in Error Handling — Case #488
- 490. Cache Invalidation Scenarios — Case #489
- 491. Application of Security Headers — Case #490
- 492. Cache Invalidation Scenarios — Case #491
- 493. Consistency in Error Handling — Case #492
- 494. Resource Leak Detection — Case #493
- 495. Resource Leak Detection — Case #494
```

## CRITICAL INSTRUCTIONS - FOLLOW STRICTLY ##

1. **Preserve Structure:** All markdown syntax—including headings (`#`), lists (`-`, `1.`), code blocks (```), inline code (`...`), links (`[]()`), images, tables, blockquotes (`>`), and horizontal rules (`---`)—MUST be kept exactly as they are.
2. **Translate Content Only:** Only translate the human-readable Korean text.
3. **DO NOT Translate Non-Text Elements:**
    - Code within fenced code blocks (```...```) and inline code (`...`).
    - URLs, file paths, and technical identifiers.
    - YAML Frontmatter.
    - HTML/XML tags.
4. **No Extra Formatting:** Do not add or remove any markdown elements. Do not introduce new formatting.
5. **Output Only Translation:** Your response must contain ONLY the translated markdown content and nothing else. Do not add introductory phrases like "Here is the English translation:".
6. **Complete Code Blocks:** If the input contains code blocks (```), ensure ALL code blocks are properly closed with ```. Never leave a code block unclosed.


Korean Markdown Document:
- 496. 에러 처리 일관성 — Case #495
- 497. 국제화(i18n) — Case #496
- 498. 보안 헤더 적용 — Case #497
- 499. API 역호환성 — Case #498
- 500. 접근성(a11y) — Case #499
- 501. 캐시 무효화 시나리오 — Case #500
- 502. 캐시 무효화 시나리오 — Case #501
- 503. API 역호환성 — Case #502
- 504. 국제화(i18n) — Case #503
- 505. 국제화(i18n) — Case #504
- 506. 리소스 누수 점검 — Case #505
- 507. 리소스 누수 점검 — Case #506
- 508. 국제화(i18n) — Case #507
- 509. 캐시 무효화 시나리오 — Case #508
- 510. 접근성(a11y) — Case #509
- 511. 성능 프로파일링 — Case #510
- 512. 리소스 누수 점검 — Case #511
- 513. 접근성(a11y) — Case #512
- 514. CORS 정책 검증 — Case #513
- 515. 캐시 무효화 시나리오 — Case #514
- 516. API 역호환성 — Case #515
- 517. CORS 정책 검증 — Case #516
- 518. API 역호환성 — Case #517
- 519. API 역호환성 — Case #518
- 520. 성능 프로파일링 — Case #519
- 521. 접근성(a11y) — Case #520
- 522. CORS 정책 검증 — Case #521
- 523. 보안 헤더 적용 — Case #522
- 524. 캐시 무효화 시나리오 — Case #523
- 525. 로그 스키마 안정성 — Case #524
- 526. CORS 정책 검증 — Case #525
- 527. 국제화(i18n) — Case #526
- 528. 로그 스키마 안정성 — Case #527
- 529. 리소스 누수 점검 — Case #528
- 530. 국제화(i18n) — Case #529
- 531. 에러 처리 일관성 — Case #530
- 532. 에러 처리 일관성 — Case #531
- 533. 로그 스키마 안정성 — Case #532
- 534. 성능 프로파일링 — Case #533
- 535. 성능 프로파일링 — Case #534
- 536. API 역호환성 — Case #535
- 537. 국제화(i18n) — Case #536
- 538. CORS 정책 검증 — Case #537
- 539. API 역호환성 — Case #538
- 540. API 역호환성 — Case #539
- 541. 캐시 무효화 시나리오 — Case #540
- 542. 캐시 무효화 시나리오 — Case #541
- 543. 보안 헤더 적용 — Case #542
- 544. 캐시 무효화 시나리오 — Case #543
- 545. 보안 헤더 적용 — Case #544
- 546. 보안 헤더 적용 — Case #545
- 547. 성능 프로파일링 — Case #546
- 548. CORS 정책 검증 — Case #547
- 549. 국제화(i18n) — Case #548
- 550. 리소스 누수 점검 — Case #549
- 551. 성능 프로파일링 — Case #550
- 552. 성능 프로파일링 — Case #551
- 553. 국제화(i18n) — Case #552
- 554. 에러 처리 일관성 — Case #553
- 555. 국제화(i18n) — Case #554
- 556. 보안 헤더 적용 — Case #555
- 557. 보안 헤더 적용 — Case #556
- 558. 국제화(i18n) — Case #557
- 559. API 역호환성 — Case #558
- 560. API 역호환성 — Case #559
- 561. 로그 스키마 안정성 — Case #560
- 562. 보안 헤더 적용 — Case #561
- 563. 에러 처리 일관성 — Case #562
- 564. 보안 헤더 적용 — Case #563
- 565. 캐시 무효화 시나리오 — Case #564
- 566. 에러 처리 일관성 — Case #565
- 567. 로그 스키마 안정성 — Case #566
- 568. 국제화(i18n) — Case #567
```

## CRITICAL INSTRUCTIONS - FOLLOW STRICTLY ##

1. **Preserve Structure:** All markdown syntax—including headings (`#`), lists (`-`, `1.`), code blocks (```), inline code (`...`), links (`[]()`), images, tables, blockquotes (`>`), and horizontal rules (`---`)—MUST be kept exactly as they are.
2. **Translate Content Only:** Only translate the human-readable Korean text.
3. **DO NOT Translate Non-Text Elements:**
    - Code within fenced code blocks (```...```) and inline code (`...`).
    - URLs, file paths, and technical identifiers.
    - YAML Frontmatter.
    - HTML/XML tags.
4. **No Extra Formatting:** Do not add or remove any markdown elements. Do not introduce new formatting.
5. **Output Only Translation:** Your response must contain ONLY the translated markdown content and nothing else. Do not add introductory phrases like "Here is the English translation:".
6. **Complete Code Blocks:** If the input contains code blocks (```), ensure ALL code blocks are properly closed with ```. Never leave a code block unclosed.


Korean Markdown Document:
- 569. Internationalization (i18n) — Case #568
- 570. Performance Profiling — Case #569
- 571. API Backward Compatibility — Case #570
- 572. Performance Profiling — Case #571
- 573. API Backward Compatibility — Case #572
- 574. Application of Security Headers — Case #573
- 575. CORS Policy Verification — Case #574
- 576. Resource Leak Inspection — Case #575
- 577. CORS Policy Verification — Case #576
- 578. Resource Leak Inspection — Case #577
- 579. Consistency in Error Handling — Case #578
- 580. Log Schema Stability — Case #579
- 581. Consistency in Error Handling — Case #580
- 582. Performance Profiling — Case #581
- 583. Internationalization (i18n) — Case #582
- 584. Log Schema Stability — Case #583
- 585. Resource Leak Inspection — Case #584
- 586. API Backward Compatibility — Case #585
- 587. CORS Policy Verification — Case #586
- 588. CORS Policy Verification — Case #587
- 589. Cache Invalidation Scenarios — Case #588
- 590. Log Schema Stability — Case #589
- 591. API Backward Compatibility — Case #590
- 592. Application of Security Headers — Case #591
- 593. Application of Security Headers — Case #592
- 594. Consistency in Error Handling — Case #593
- 595. Internationalization (i18n) — Case #594
- 596. API Backward Compatibility — Case #595
- 597. Internationalization (i18n) — Case #596
- 598. CORS Policy Verification — Case #597
- 599. Cache Invalidation Scenarios — Case #598
- 600. Internationalization (i18n) — Case #599
- 601. Resource Leak Inspection — Case #600
- 602. Resource Leak Inspection — Case #601
- 603. Cache Invalidation Scenarios — Case #602
- 604. Resource Leak Inspection — Case #603
- 605. Cache Invalidation Scenarios — Case #604
- 606. Log Schema Stability — Case #605
- 607. API Backward Compatibility — Case #606
- 608. Application of Security Headers — Case #607
- 609. Performance Profiling — Case #608
- 610. API Backward Compatibility — Case #609
- 611. Consistency in Error Handling — Case #610
- 612. CORS Policy Verification — Case #611
- 613. CORS Policy Verification — Case #612
- 614. Performance Profiling — Case #613
- 615. Cache Invalidation Scenarios — Case #614
- 616. Performance Profiling — Case #615
- 617. Consistency in Error Handling — Case #616
- 618. Performance Profiling — Case #617
- 619. Performance Profiling — Case #618
- 620. Performance Profiling — Case #619
- 621. Internationalization (i18n) — Case #620
- 622. Performance Profiling — Case #621
- 623. Log Schema Stability — Case #622
- 624. API Backward Compatibility — Case #623
- 625. Application of Security Headers — Case #624
- 626. Consistency in Error Handling — Case #625
- 627. Log Schema Stability — Case #626
- 628. Performance Profiling — Case #627
- 629. Consistency in Error Handling — Case #628
- 630. Application of Security Headers — Case #629
- 631. Application of Security Headers — Case #630
- 632. Performance Profiling — Case #631
- 633. Log Schema Stability — Case #632
- 634. Resource Leak Inspection — Case #633
- 635. Resource Leak Inspection — Case #634
- 636. Accessibility (a11y) — Case #635
- 637. Accessibility (a11y) — Case #636
- 638. Resource Leak Inspection — Case #637
- 639. Cache Invalidation Scenarios — Case #638
- 640. Cache Invalidation Scenarios — Case #639
```

## CRITICAL INSTRUCTIONS - FOLLOW STRICTLY ##

1. **Preserve Structure:** All markdown syntax—including headings (`#`), lists (`-`, `1.`), code blocks (```), inline code (`...`), links (`[]()`), images, tables, blockquotes (`>`), and horizontal rules (`---`)—MUST be kept exactly as they are.
2. **Translate Content Only:** Only translate the human-readable Korean text.
3. **DO NOT Translate Non-Text Elements:**
    - Code within fenced code blocks (```...```) and inline code (`...`).
    - URLs, file paths, and technical identifiers.
    - YAML Frontmatter.
    - HTML/XML tags.
4. **No Extra Formatting:** Do not add or remove any markdown elements. Do not introduce new formatting.
5. **Output Only Translation:** Your response must contain ONLY the translated markdown content and nothing else. Do not add introductory phrases like "Here is the English translation:".
6. **Complete Code Blocks:** If the input contains code blocks (```), ensure ALL code blocks are properly closed with ```. Never leave a code block unclosed.


Korean Markdown Document:
- 641. Internationalization (i18n) — Case #640
- 642. Consistency in Error Handling — Case #641
- 643. API Backward Compatibility — Case #642
- 644. Performance Profiling — Case #643
- 645. Cache Invalidation Scenarios — Case #644
- 646. Cache Invalidation Scenarios — Case #645
- 647. Internationalization (i18n) — Case #646
- 648. Log Schema Stability — Case #647
- 649. CORS Policy Verification — Case #648
- 650. Log Schema Stability — Case #649
- 651. Resource Leak Detection — Case #650
- 652. Accessibility (a11y) — Case #651
- 653. Application of Security Headers — Case #652
- 654. Log Schema Stability — Case #653
- 655. Performance Profiling — Case #654
- 656. Application of Security Headers — Case #655
- 657. Log Schema Stability — Case #656
- 658. Application of Security Headers — Case #657
- 659. CORS Policy Verification — Case #658
- 660. API Backward Compatibility — Case #659
- 661. CORS Policy Verification — Case #660
- 662. API Backward Compatibility — Case #661
- 663. Performance Profiling — Case #662
- 664. Log Schema Stability — Case #663
- 665. Cache Invalidation Scenarios — Case #664
- 666. CORS Policy Verification — Case #665
- 667. Resource Leak Detection — Case #666
- 668. Application of Security Headers — Case #667
- 669. Cache Invalidation Scenarios — Case #668
- 670. Cache Invalidation Scenarios — Case #669
- 671. Performance Profiling — Case #670
- 672. API Backward Compatibility — Case #671
- 673. Accessibility (a11y) — Case #672
- 674. CORS Policy Verification — Case #673
- 675. Application of Security Headers — Case #674
- 676. Resource Leak Detection — Case #675
- 677. Accessibility (a11y) — Case #676
- 678. Internationalization (i18n) — Case #677
- 679. Resource Leak Detection — Case #678
- 680. Cache Invalidation Scenarios — Case #679
- 681. Cache Invalidation Scenarios — Case #680
- 682. Log Schema Stability — Case #681
- 683. Accessibility (a11y) — Case #682
- 684. CORS Policy Verification — Case #683
- 685. Resource Leak Detection — Case #684
- 686. Performance Profiling — Case #685
- 687. Log Schema Stability — Case #686
- 688. Performance Profiling — Case #687
- 689. CORS Policy Verification — Case #688
- 690. CORS Policy Verification — Case #689
- 691. Cache Invalidation Scenarios — Case #690
- 692. API Backward Compatibility — Case #691
- 693. API Backward Compatibility — Case #692
- 694. Internationalization (i18n) — Case #693
- 695. Internationalization (i18n) — Case #694
- 696. API Backward Compatibility — Case #695
- 697. Performance Profiling — Case #696
- 698. Cache Invalidation Scenarios — Case #697
- 699. Performance Profiling — Case #698
- 700. API Backward Compatibility — Case #699
- 701. Application of Security Headers — Case #700
- 702. Cache Invalidation Scenarios — Case #701
- 703. Consistency in Error Handling — Case #702
- 704. Performance Profiling — Case #703
- 705. Application of Security Headers — Case #704
- 706. Log Schema Stability — Case #705
- 707. Accessibility (a11y) — Case #706
- 708. API Backward Compatibility — Case #707
- 709. Cache Invalidation Scenarios — Case #708
- 710. Log Schema Stability — Case #709
- 711. Consistency in Error Handling — Case #710
- 712. Resource Leak Detection — Case #711
```

## CRITICAL INSTRUCTIONS - FOLLOW STRICTLY ##

1. **Preserve Structure:** All markdown syntax—including headings (`#`), lists (`-`, `1.`), code blocks (```), inline code (`...`), links (`[]()`), images, tables, blockquotes (`>`), and horizontal rules (`---`)—MUST be kept exactly as they are.
2. **Translate Content Only:** Only translate the human-readable Korean text.
3. **DO NOT Translate Non-Text Elements:**
    - Code within fenced code blocks (```...```) and inline code (`...`).
    - URLs, file paths, and technical identifiers.
    - YAML Frontmatter.
    - HTML/XML tags.
4. **No Extra Formatting:** Do not add or remove any markdown elements. Do not introduce new formatting.
5. **Output Only Translation:** Your response must contain ONLY the translated markdown content and nothing else. Do not add introductory phrases like "Here is the English translation:".
6. **Complete Code Blocks:** If the input contains code blocks (```), ensure ALL code blocks are properly closed with ```. Never leave a code block unclosed.


Korean Markdown Document:
- 713. Internationalization (i18n) — Case #712
- 714. Resource Leak Inspection — Case #713
- 715. CORS Policy Verification — Case #714
- 716. Log Schema Stability — Case #715
- 717. Accessibility (a11y) — Case #716
- 718. Consistency in Error Handling — Case #717
- 719. Performance Profiling — Case #718
- 720. Accessibility (a11y) — Case #719
- 721. CORS Policy Verification — Case #720
- 722. Log Schema Stability — Case #721
- 723. Accessibility (a11y) — Case #722
- 724. Resource Leak Inspection — Case #723
- 725. Cache Invalidation Scenarios — Case #724
- 726. Cache Invalidation Scenarios — Case #725
- 727. Performance Profiling — Case #726
- 728. Resource Leak Inspection — Case #727
- 729. CORS Policy Verification — Case #728
- 730. Performance Profiling — Case #729
- 731. Log Schema Stability — Case #730
- 732. Resource Leak Inspection — Case #731
- 733. Accessibility (a11y) — Case #732
- 734. Performance Profiling — Case #733
- 735. API Backward Compatibility — Case #734
- 736. CORS Policy Verification — Case #735
- 737. Resource Leak Inspection — Case #736
- 738. Application of Security Headers — Case #737
- 739. Log Schema Stability — Case #738
- 740. Accessibility (a11y) — Case #739
- 741. CORS Policy Verification — Case #740
- 742. Application of Security Headers — Case #741
- 743. CORS Policy Verification — Case #742
- 744. Application of Security Headers — Case #743
- 745. Internationalization (i18n) — Case #744
- 746. Internationalization (i18n) — Case #745
- 747. Log Schema Stability — Case #746
- 748. Cache Invalidation Scenarios — Case #747
- 749. Performance Profiling — Case #748
- 750. Cache Invalidation Scenarios — Case #749
- 751. Performance Profiling — Case #750
- 752. Log Schema Stability — Case #751
- 753. CORS Policy Verification — Case #752
- 754. Accessibility (a11y) — Case #753
- 755. CORS Policy Verification — Case #754
- 756. Cache Invalidation Scenarios — Case #755
- 757. Internationalization (i18n) — Case #756
- 758. Internationalization (i18n) — Case #757
- 759. Accessibility (a11y) — Case #758
- 760. Performance Profiling — Case #759
- 761. Resource Leak Inspection — Case #760
- 762. Internationalization (i18n) — Case #761
- 763. Cache Invalidation Scenarios — Case #762
- 764. Internationalization (i18n) — Case #763
- 765. Accessibility (a11y) — Case #764
- 766. Performance Profiling — Case #765
- 767. Resource Leak Inspection — Case #766
- 768. Accessibility (a11y) — Case #767
- 769. Consistency in Error Handling — Case #768
- 770. CORS Policy Verification — Case #769
- 771. Accessibility (a11y) — Case #770
- 772. Resource Leak Inspection — Case #771
- 773. Consistency in Error Handling — Case #772
- 774. Performance Profiling — Case #773
- 775. Log Schema Stability — Case #774
- 776. Consistency in Error Handling — Case #775
- 777. Resource Leak Inspection — Case #776
- 778. Accessibility (a11y) — Case #777
- 779. Performance Profiling — Case #778
- 770. Consistency in Error Handling — Case #779
- 780. Internationalization (i18n) — Case #780
- 781. API Backward Compatibility — Case #781
- 783. Log Schema Stability — Case #782
- 784. Accessibility (a11y) — Case #783
```

## CRITICAL INSTRUCTIONS - FOLLOW STRICTLY ##
1. **Preserve Structure:** All markdown syntax—including headings (`#`), lists (`-`, `1.`), code blocks (```), inline code (`...`), links (`[]()`), images, tables, blockquotes (`>`), and horizontal rules (`---`)—MUST be kept exactly as they are.
2. **Translate Content Only:** Only translate the human-readable Korean text.
3. **DO NOT Translate Non-Text Elements:**
    - Code within fenced code blocks (```...```) and inline code (`...`).
    - URLs, file paths, and technical identifiers.
    - YAML Frontmatter.
    - HTML/XML tags.
4. **No Extra Formatting:** Do not add or remove any markdown elements. Do not introduce new formatting.
5. **Output Only Translation:** Your response must contain ONLY the translated markdown content and nothing else. Do not add introductory phrases like "Here is the English translation:".
6. **Complete Code Blocks:** If the input contains code blocks (```), ensure ALL code blocks are properly closed with ```. Never leave a code block unclosed.


Korean Markdown Document:
- 785. Accessibility (a11y) — Case #784
- 786. Accessibility (a11y) — Case #785
- 787. Application of Security Headers — Case #786
- 788. Accessibility (a11y) — Case #787
- 789. CORS Policy Verification — Case #788
- 790. CORS Policy Verification — Case #789
- 791. Cache Invalidation Scenarios — Case #790
- 792. Application of Security Headers — Case #791
- 793. CORS Policy Verification — Case #792
- 794. Log Schema Stability — Case #793
- 795. Internationalization (i18n) — Case #794
- 796. Resource Leak Inspection — Case #795
- 797. Internationalization (i18n) — Case #796
- 798. Cache Invalidation Scenarios — Case #797
- 799. Application of Security Headers — Case #798
- 800. Application of Security Headers — Case #799
- 801. Internationalization (i18n) — Case #800

## 9. Conclusion
This document is a sample to evaluate whether the translation engine properly handles **format preservation**, **terminology consistency**, and **rules for ignoring code/formulas Paths**.
If necessary, more sections can be added following the same pattern to extend it to over 100,000 characters.

# Extended Section 1

## Repeat Block 1-1
- This paragraph has been added to create a very long document.

- It contains a mix of various grammatical structures and Korean text.

- It allows for checking translation quality, token limitations, and context loss, among other things.


```bash
echo 'section 1-1' >> /tmp/out.log
```

```mermaid
flowchart TD
  X-->Y
```

## Repeat Block 1-2
- This paragraph has been added to create a very long document.

- It contains a mix of various grammatical structures and Korean text.

- It allows for checking translation quality, token limitations, and context loss, among other things.


```bash
echo 'section 1-2' >> /tmp/out.log
```

```mermaid
flowchart TD
  X-->Y
```

## Repeat Block 1-3
- This paragraph has been added to create a very long document.

- It contains a mix of various grammatical structures and Korean text.

- It allows for checking translation quality, token limitations, and context loss, among other things.


```bash
echo 'section 1-3' >> /tmp/out.log
```

```mermaid
flowchart TD
  X-->Y
```

## Repeat Block 1-4
- This paragraph has been added to create a very long document.

- It contains a mix of various grammatical structures and Korean text.

- It allows for checking translation quality, token limitations, and context loss, among other things.


```bash
echo 'section 1-4' >> /tmp/out.log
```

```mermaid
flowchart TD
  X-->Y
```

## Repeat Block 1-5
- This paragraph has been added to create a very long document.

- It contains a mix of various grammatical structures and Korean text.

- It allows for checking translation quality, token limitations, and context loss, among other things.


```bash
echo 'section 1-5' >> /tmp/out.log
```

```mermaid
flowchart TD
  X-->Y
```

## Repeat Block 1-6
- This paragraph has been added to create a very long document.

- It contains a mix of various grammatical structures and Korean text.

- It allows for checking translation quality, token limitations, and context loss, among other things.


```bash
echo 'section 1-6' >> /tmp/out.log
```

```mermaid
flowchart TD
  X-->Y
```

## Repeat Block 1-7
- This paragraph has been added to create a very long document.

- It contains a mix of various grammatical structures and Korean text.

- It allows for checking translation quality, token limitations, and context loss, among other things.


```bash
echo 'section 1-7' >> /tmp/out.log
```
```

## CRITICAL INSTRUCTIONS - FOLLOW STRICTLY ##

1. **Preserve Structure:** All markdown syntax—including headings (`#`), lists (`-`, `1.`), code blocks (```), inline code (`...`), links (`[]()`), images, tables, blockquotes (`>`), and horizontal rules (`---`)—MUST be kept exactly as they are.
2. **Translate Content Only:** Only translate the human-readable Korean text.
3. **DO NOT Translate Non-Text Elements:**
    - Code within fenced code blocks (```...```) and inline code (`...`).
    - URLs, file paths, and technical identifiers.
    - YAML Frontmatter.
    - HTML/XML tags.
4. **No Extra Formatting:** Do not add or remove any markdown elements. Do not introduce new formatting.
5. **Output Only Translation:** Your response must contain ONLY the translated markdown content and nothing else. Do not add introductory phrases like "Here is the English translation:".
6. **Complete Code Blocks:** If the input contains code blocks (```), ensure ALL code blocks are properly closed with ```. Never leave a code block unclosed.


Korean Markdown Document:
echo 'section 1-7' >> /tmp/out.log

```

```mermaid
flowchart TD
  X-->Y
```

## Repeat Block 1-8

- This paragraph has been added to create a very long document.

- It contains a mix of various grammatical structures and Korean text.

- You can observe the translation quality, token limitations, and potential context loss here.


```bash

echo 'section 1-8' >> /tmp/out.log

```

```mermaid
flowchart TD
  X-->Y
```

## Repeat Block 1-9

- This paragraph has been added to create a very long document.

- It contains a mix of various grammatical structures and Korean text.

- You can observe the translation quality, token limitations, and potential context loss here.


```bash

echo 'section 1-9' >> /tmp/out.log

```

```mermaid
flowchart TD
  X-->Y
```

## Repeat Block 1-10

- This paragraph has been added to create a very long document.

- It contains a mix of various grammatical structures and Korean text.

- You can observe the translation quality, token limitations, and potential context loss here.


```bash

echo 'section 1-10' >> /tmp/out.log
```

---

> **⚠️ 이 문서는 AI로 번역된 문서입니다.**
>
> **⚠️ This document has been translated by AI.**