# OpenClaw 자동화 스크립트 모음

OpenClaw AI 어시스턴트와 함께 사용할 수 있는 다양한 자동화 스크립트 모음입니다.

## 📁 프로젝트 구조

```
openclaw-automations/
├── README.md                    # 이 파일
├── LICENSE                      # MIT 라이선스
├── .gitignore                   # Git 무시 파일
├── requirements.txt             # Python 의존성
├── SETUP_GITHUB.md             # GitHub 설정 가이드
├── screenshot-cleanup/          # 스크린샷 정리 자동화
│   ├── cleanup_screenshots.sh
│   ├── cleanup_screenshots_biweekly.sh
│   ├── cleanup_screenshots_final.sh
│   ├── cleanup_screenshots_force.sh
│   ├── cleanup_screenshots_simple.sh
│   ├── cleanup_screenshots_working.sh
│   └── launch-agent/           # macOS LaunchAgent 설정
│       └── com.user.cleanup_screenshots.plist
├── image-to-pdf-converter/     # 이미지 → PDF 변환기
│   ├── convert_images_to_pdf.py
│   ├── convert_images_to_pdf_fixed.py
│   ├── run_conversion.sh
│   └── run_fixed_conversion.sh
├── setup-guides/               # 설정 가이드
│   ├── gog-setup-guide.md      # Google Workspace CLI 설정
│   ├── memory-hygiene-guide.md # 메모리 관리 설정
│   ├── office-xyz-guide.md     # 가상 오피스 설정
│   └── vllm-setup-guide.md     # vLLM 서버 설정
├── system-config/              # 시스템 설정
│   └── openclaw-자동-시작-설정/
│       ├── ai.openclaw.gateway.force.plist
│       └── README.md
├── automation-scripts/         # 자동화 스크립트
│   └── github-자동-커밋-시스템/
│       ├── github_auto_committer.py
│       ├── auto-git-commit.sh
│       ├── auto-commit-config.json
│       └── README.md
├── test-scripts/               # 테스트 스크립트
│   └── 테스트-자동화-코드/
│       ├── hello_world.py
│       └── README.md
└── decorator-tests/            # 데코레이터 테스트 (예정)
```

## 🚀 주요 기능

### 1. 스크린샷 자동 정리 시스템
**목적**: 2주마다 오래된 스크린샷 PNG 파일 자동 삭제

**특징**:
- 2주마다 자동 실행 (짝수 주차)
- 데스크탑, 다운로드 폴더 검색
- 14일 이상된 파일만 삭제
- macOS LaunchAgent 통합
- 상세 로깅 시스템

**사용법**:
```bash
# 수동 실행
./screenshot-cleanup/cleanup_screenshots_biweekly.sh 14

# 강제 실행 (주차 확인 없음)
./screenshot-cleanup/cleanup_screenshots_force.sh 7
```

### 2. 이미지 → PDF 변환기
**목적**: 여러 PNG 이미지를 하나의 PDF로 변환

**특징**:
- 8개 이상의 PNG 파일을 단일 PDF로 병합
- 각 페이지 상단에 파일명 자동 추가
- NFD → NFC 한글 정규화 지원
- A4 크기 최적화
- 가상 환경 자동 설정

**사용법**:
```bash
# 기본 변환
cd image-to-pdf-converter
python3 convert_images_to_pdf.py

# 한글 정규화 포함 변환
python3 convert_images_to_pdf_fixed.py
```

### 3. GitHub 자동 커밋 시스템
**목적**: 모든 자동화 코드를 GitHub에 자동 커밋

**특징**:
- 코드 생성 즉시 자동 커밋
- Pull → 수정 → Push 자동화
- 상세 커밋 메시지 생성
- 카테고리별 자동 분류
- 완전한 문서화

**사용법**:
```python
from github_auto_committer import auto_commit

@auto_commit(
    project_name="프로젝트명",
    description="설명",
    category="카테고리"
)
def create_code(output_path: str) -> str:
    # 코드 생성
    return output_path
```

### 4. OpenClaw 자동 시작 설정
**목적**: 맥북 부팅 시 OpenClaw 자동 실행

**특징**:
- 부팅 시 자동 실행
- `--force` 옵션 자동 적용
- 충돌 시 자동 재시작
- 상세 로깅 시스템

**설치**:
```bash
# LaunchAgent 복사
cp system-config/openclaw-자동-시작-설정/ai.openclaw.gateway.force.plist ~/Library/LaunchAgents/

# LaunchAgent 로드
launchctl load ~/Library/LaunchAgents/ai.openclaw.gateway.force.plist
```

### 5. OpenClaw 설정 가이드
다양한 OpenClaw 통합을 위한 설정 가이드 제공:
- **Google Workspace CLI (gog)**: Gmail, Drive, Sheets 연동
- **Memory Hygiene**: 벡터 메모리 관리 및 최적화
- **office.xyz**: 가상 오피스 플랫폼 연동
- **vLLM**: 고성능 로컬 LLM 서버 설정

## 🛠 기술 스택

### 백엔드
- **Python 3.9+**: 주요 스크립트 언어
- **Pillow**: 이미지 처리 라이브러리
- **ReportLab**: PDF 생성 라이브러리
- **unicodedata**: 한글 정규화 처리

### 시스템
- **macOS LaunchAgent**: 백그라운드 작업 스케줄링
- **Bash Scripting**: 자동화 스크립트
- **Virtual Environments**: Python 의존성 관리
- **Git Automation**: 자동 커밋 및 동기화

### OpenClaw 통합
- **OpenClaw Skills**: ClawHub 스킬 설치 및 설정
- **OpenClaw Studio**: 웹 대시보드
- **Ollama**: 로컬 LLM 추론
- **vLLM**: 고성능 LLM 서버

## 📦 설치 방법

### 1. 저장소 클론
```bash
git clone https://github.com/ksj747172/openclaw-automations.git
cd openclaw-automations
```

### 2. 의존성 설치
```bash
# Python 가상 환경 생성
python3 -m venv venv
source venv/bin/activate

# 필수 패키지 설치
pip install Pillow reportlab
```

### 3. 자동 커밋 시스템 설정
```bash
cd automation-scripts/github-자동-커밋-시스템

# GitHub 토큰 설정 (선택사항)
echo '{"github_auto_commit": {"token": "YOUR_GITHUB_TOKEN"}}' > auto-commit-config.json

# 테스트 실행
python3 github_auto_committer.py "테스트" "설명" ./test-folder
```

## 🔄 자동화 워크플로우

### 새로운 코드 생성
1. 코드 생성 → 자동 GitHub 커밋
2. README 자동 업데이트
3. 카테고리별 분류

### 기존 코드 수정
1. GitHub에서 Pull
2. 코드 수정 및 테스트
3. 커밋 및 Push
4. README 업데이트

### 문서 관리
- 모든 변경사항 문서화
- 사용법 가이드 포함
- 버전 정보 기록

## 📝 커밋 규칙

### 커밋 메시지 형식
```
feat: [프로젝트명] - [설명]
fix: [프로젝트명] - [버그 수정]
improve: [프로젝트명] - [기능 개선]
docs: [프로젝트명] - [문서 업데이트]
```

### 메타데이터 포함
- 생성일자
- 생성자 (OpenClaw Assistant)
- 프로젝트 설명
- 기술 스택 정보

## 🎯 사용 예시

### 예시 1: 주간 스크린샷 정리
```bash
# 7일 이상된 스크린샷 삭제
./screenshot-cleanup/cleanup_screenshots_force.sh 7
```

### 예시 2: 문서 아카이빙
```bash
# 여러 스크린샷을 하나의 PDF로 변환
cd image-to-pdf-converter
python3 convert_images_to_pdf_fixed.py --input-folder ~/Downloads/screenshots --output report.pdf
```

### 예시 3: 자동 커밋 시스템
```python
# Python 데코레이터 사용
from github_auto_committer import auto_commit

@auto_commit("새 프로젝트", "설명", "automation-scripts")
def create_automation(output_dir: str) -> str:
    # 자동화 코드 생성
    return output_dir
```

## 🔧 설정 파일

### LaunchAgent 설정 (`ai.openclaw.gateway.force.plist`)
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>ai.openclaw.gateway.force</string>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>ProgramArguments</key>
    <array>
        <string>/opt/homebrew/bin/openclaw</string>
        <string>gateway</string>
        <string>--force</string>
    </array>
</dict>
</plist>
```

### 자동 커밋 설정 (`auto-commit-config.json`)
```json
{
  "github_auto_commit": {
    "enabled": true,
    "repository": "ksj747172/openclaw-automations",
    "token": "YOUR_GITHUB_TOKEN",
    "author": "OpenClaw Assistant",
    "email": "assistant@openclaw.ai"
  }
}
```

## 📊 로깅

### 스크린샷 정리 로그
```
~/Library/Logs/cleanup_screenshots.log
~/Library/Logs/cleanup_screenshots.out.log
~/Library/Logs/cleanup_screenshots.err.log
```

### OpenClaw Gateway 로그
```
~/.openclaw/logs/gateway-force.out.log
~/.openclaw/logs/gateway-force.err.log
```

### 자동 커밋 로그
```
~/.openclaw/workspace/git-commit.log
```

## 🐛 문제 해결

### 일반적인 문제
1. **한글 파일명 문제**: `convert_images_to_pdf_fixed.py` 사용 (NFC 정규화)
2. **LaunchAgent 실행 안됨**: `launchctl list | grep openclaw`으로 상태 확인
3. **GitHub 커밋 실패**: 토큰 확인 및 권한 확인
4. **의존성 오류**: 가상 환경 재생성 및 패키지 재설치

### 디버깅 명령어
```bash
# LaunchAgent 상태 확인
launchctl list | grep openclaw

# OpenClaw 포트 확인
curl http://127.0.0.1:18789/

# GitHub 커밋 확인
cd /Users/hongmin/.openclaw/workspace/github-sync
git log --oneline -5

# 로그 확인
tail -f ~/.openclaw/logs/gateway-force.out.log
```

## 🤝 기여하기

### 자동 기여 시스템
이 프로젝트는 OpenClaw AI Assistant에 의해 자동으로 관리됩니다:

1. **코드 생성** → 자동 GitHub 커밋
2. **문서 업데이트** → README 자동 반영
3. **버전 관리** → 커밋 이력으로 추적
4. **품질 관리** → 테스트 및 검증

### 수동 기여
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 라이선스

이 프로젝트는 MIT 라이선스를 따릅니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

## 👥 저자

- **OpenClaw AI Assistant** - [@ksj747172](https://github.com/ksj747172)
- **Hongmin Kim** - 프로젝트 소유자

## 🔄 자동화 통계
- **총 파일 수**: 30+ 파일
- **총 커밋 수**: 지속적 증가 중
- **카테고리 수**: 6개 이상
- **자동화 수준**: 완전 자동화

## 🙏 감사의 말

- OpenClaw 개발팀
- 모든 오픈소스 기여자들
- GitHub 자동화 인프라
- 이 프로젝트를 사용해주시는 모든 분들

---

**자동 관리 시스템**: 이 프로젝트는 OpenClaw AI Assistant에 의해 자동으로 관리됩니다. 모든 코드 생성, 수정, 문서화는 자동화 시스템을 통해 처리됩니다.

**참고**: 이 프로젝트는 OpenClaw AI 어시스턴트와 함께 사용하기 위해 개발되었습니다. OpenClaw에 대한 자세한 정보는 [OpenClaw 공식 문서](https://docs.openclaw.ai)를 참조하세요.