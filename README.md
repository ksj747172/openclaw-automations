# OpenClaw 자동화 스크립트 모음

OpenClaw AI 어시스턴트와 함께 사용할 수 있는 다양한 자동화 스크립트 모음입니다.

## 📁 프로젝트 구조

```
openclaw-automations/
├── README.md                    # 이 파일
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
└── setup-guides/               # 설정 가이드
    ├── gog-setup-guide.md      # Google Workspace CLI 설정
    ├── memory-hygiene-guide.md # 메모리 관리 설정
    ├── office-xyz-guide.md     # 가상 오피스 설정
    └── vllm-setup-guide.md     # vLLM 서버 설정
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

### 3. 설정 가이드
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

### OpenClaw 통합
- **OpenClaw Skills**: ClawHub 스킬 설치 및 설정
- **OpenClaw Studio**: 웹 대시보드
- **Ollama**: 로컬 LLM 추론

## 📦 설치 방법

### 1. 저장소 클론
```bash
git clone https://github.com/yourusername/openclaw-automations.git
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

### 3. 스크린샷 정리 자동화 설정
```bash
# LaunchAgent 파일 복사
cp screenshot-cleanup/launch-agent/com.user.cleanup_screenshots.plist ~/Library/LaunchAgents/

# LaunchAgent 로드
launchctl load ~/Library/LaunchAgents/com.user.cleanup_screenshots.plist
```

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

### 예시 3: OpenClaw 스킬 설정
```bash
# Google Workspace CLI 설정
open setup-guides/gog-setup-guide.md
```

## 🔧 설정 파일

### LaunchAgent 설정 (`com.user.cleanup_screenshots.plist`)
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.user.cleanup_screenshots</string>
    <key>ProgramArguments</key>
    <array>
        <string>/path/to/cleanup_screenshots_biweekly.sh</string>
        <string>14</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Weekday</key>
        <integer>1</integer>
        <key>Hour</key>
        <integer>9</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
</dict>
</plist>
```

## 📝 로깅

### 스크린샷 정리 로그
```
~/Library/Logs/cleanup_screenshots.log
~/Library/Logs/cleanup_screenshots.out.log
~/Library/Logs/cleanup_screenshots.err.log
```

### PDF 변환 로그
```
콘솔 출력으로 실시간 진행 상황 확인
```

## 🐛 문제 해결

### 일반적인 문제
1. **한글 파일명 문제**: `convert_images_to_pdf_fixed.py` 사용 (NFC 정규화)
2. **LaunchAgent 실행 안됨**: `launchctl list | grep cleanup`으로 상태 확인
3. **의존성 오류**: 가상 환경 재생성 및 패키지 재설치

### 디버깅 명령어
```bash
# LaunchAgent 상태 확인
launchctl list | grep cleanup

# LaunchAgent 재시작
launchctl unload ~/Library/LaunchAgents/com.user.cleanup_screenshots.plist
launchctl load ~/Library/LaunchAgents/com.user.cleanup_screenshots.plist

# 로그 확인
tail -f ~/Library/Logs/cleanup_screenshots.log
```

## 🤝 기여하기

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 라이선스

이 프로젝트는 MIT 라이선스를 따릅니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

## 👥 저자

- **Hongmin Kim** - [@yourusername](https://github.com/yourusername)

## 🙏 감사의 말

- OpenClaw 개발팀
- 모든 오픈소스 기여자들
- 이 프로젝트를 사용해주시는 모든 분들

---

**참고**: 이 프로젝트는 OpenClaw AI 어시스턴트와 함께 사용하기 위해 개발되었습니다. OpenClaw에 대한 자세한 정보는 [OpenClaw 공식 문서](https://docs.openclaw.ai)를 참조하세요.