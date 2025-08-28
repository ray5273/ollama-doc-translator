# 설치 가이드

이 문서는 Ollama 문서 번역기를 설치하고 설정하는 방법에 대한 상세한 가이드를 제공합니다.

## 시스템 요구사항

### 최소 요구사항
- **운영체제**: Windows 10/11, macOS 10.14+, Ubuntu 18.04+
- **메모리**: 8GB RAM (권장: 16GB 이상)
- **저장공간**: 10GB 이상의 여유 공간
- **네트워크**: 인터넷 연결 (초기 모델 다운로드용)

### 권장 사양
- **CPU**: 멀티코어 프로세서 (Intel i5 이상 또는 AMD Ryzen 5 이상)
- **메모리**: 16GB RAM 이상
- **GPU**: NVIDIA GPU (CUDA 지원) - 선택사항이지만 성능 향상에 도움

## Ollama 설치

### Windows에서 설치

1. **Windows 패키지 매니저 사용**:
   ```powershell
   winget install Ollama.Ollama
   ```

2. **수동 설치**:
   - [Ollama 공식 웹사이트](https://ollama.com/download)에서 Windows 설치 파일 다운로드
   - 다운로드한 파일을 실행하여 설치 진행
   - 설치 완료 후 시스템 재시작

### macOS에서 설치

1. **Homebrew 사용** (권장):
   ```bash
   brew install ollama
   ```

2. **수동 설치**:
   - [Ollama 공식 웹사이트](https://ollama.com/download)에서 macOS 설치 파일 다운로드
   - DMG 파일을 열어서 Applications 폴더로 드래그

### Linux에서 설치

1. **자동 설치 스크립트** (권장):
   ```bash
   curl -fsSL https://ollama.com/install.sh | sh
   ```

2. **수동 설치**:
   ```bash
   # Docker를 사용한 설치
   docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
   ```

## 모델 설치

### Exaone3.5 모델 다운로드

Ollama가 설치되면 번역에 사용할 모델을 다운로드해야 합니다:

```bash
# 기본 모델 다운로드
ollama pull exaone3.5:7.8b

# 더 큰 모델이 필요한 경우
ollama pull exaone3.5:32b
```

### 다른 번역 모델

번역 품질을 비교해보고 싶다면 다른 모델들도 시도해볼 수 있습니다:

```bash
# 기타 추천 모델들
ollama pull llama3.1:8b
ollama pull mistral:7b
ollama pull codellama:7b
```

## 설정 확인

### Ollama 서버 시작

```bash
# 백그라운드에서 Ollama 서버 실행
ollama serve
```

### 설치 확인

1. **서버 상태 확인**:
   ```bash
   curl http://localhost:11434/api/tags
   ```

2. **모델 목록 확인**:
   ```bash
   ollama list
   ```

3. **간단한 번역 테스트**:
   ```bash
   ollama run exaone3.5:7.8b "안녕하세요를 영어로 번역해주세요"
   ```

## 환경 설정

### 환경 변수 설정

시스템에 따라 다음 환경 변수를 설정할 수 있습니다:

**Windows (PowerShell)**:
```powershell
$env:OLLAMA_HOST = "0.0.0.0:11434"
$env:OLLAMA_MODELS = "C:\Users\[username]\.ollama\models"
```

**macOS/Linux (Bash)**:
```bash
export OLLAMA_HOST=0.0.0.0:11434
export OLLAMA_MODELS=~/.ollama/models
```

### 방화벽 설정

Ollama는 기본적으로 포트 11434를 사용합니다. 네트워크에서 접근해야 하는 경우 방화벽 규칙을 추가하세요:

```bash
# Linux (ufw)
sudo ufw allow 11434

# Windows (PowerShell - 관리자 권한)
New-NetFirewallRule -DisplayName "Ollama" -Direction Inbound -Port 11434 -Protocol TCP -Action Allow
```

## GitHub Actions 설정

### Self-hosted Runner 설정

로컬 Ollama 서버를 사용하려면 Self-hosted Runner를 설정하는 것이 좋습니다:

1. **GitHub Repository** → **Settings** → **Actions** → **Runners**로 이동
2. **New self-hosted runner** 클릭
3. 운영체제에 맞는 가이드를 따라 설정
4. Runner를 시작하기 전에 Ollama가 실행 중인지 확인

### Repository Secrets 설정

GitHub Actions에서 사용할 시크릿을 설정하세요:

1. **GitHub Repository** → **Settings** → **Secrets and variables** → **Actions**
2. 필요한 시크릿 추가:
   - `OLLAMA_URL`: Ollama 서버 URL (기본값: http://localhost:11434)
   - `GITHUB_TOKEN`: 자동으로 제공됨

## 성능 최적화

### GPU 사용 설정

NVIDIA GPU가 있는 경우 CUDA를 활성화할 수 있습니다:

```bash
# CUDA 지원 확인
nvidia-smi

# GPU 사용 활성화
export OLLAMA_GPU=1
```

### 메모리 최적화

큰 모델을 사용할 때 메모리 사용량을 최적화할 수 있습니다:

```bash
# 모델 로드 옵션 설정
export OLLAMA_NUM_PARALLEL=2
export OLLAMA_MAX_LOADED_MODELS=1
```

## 문제 해결

일반적인 설치 문제에 대한 해결책:

### 포트 충돌
```bash
# 다른 포트 사용
export OLLAMA_HOST=0.0.0.0:11435
ollama serve
```

### 권한 문제 (Linux/macOS)
```bash
# Ollama 바이너리에 실행 권한 부여
chmod +x /usr/local/bin/ollama
```

### 모델 다운로드 실패
```bash
# 프록시 설정 (필요한 경우)
export HTTP_PROXY=http://proxy.company.com:8080
export HTTPS_PROXY=http://proxy.company.com:8080
ollama pull exaone3.5:7.8b
```

## 다음 단계

설치가 완료되면 다음 문서들을 참조하세요:

- [설정 가이드](configuration.md) - 상세 설정 옵션
- [API 가이드](api-guide.md) - API 사용법
- [문제 해결 가이드](troubleshooting.md) - 일반적인 문제 해결

설치 중 문제가 발생하면 [GitHub Issues](https://github.com/your-username/ollama-doc-translator/issues)에 문의해주세요.