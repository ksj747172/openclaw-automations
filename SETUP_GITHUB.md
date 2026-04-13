# GitHub 저장소 설정 가이드

이 파일은 생성된 OpenClaw 자동화 코드를 GitHub에 업로드하는 방법을 설명합니다.

## 1. GitHub 저장소 생성

1. https://github.com 로그인
2. 우측 상단 "+" 버튼 → "New repository"
3. 저장소 정보 입력:
   - Repository name: `openclaw-automations`
   - Description: `OpenClaw AI 어시스턴트를 위한 자동화 스크립트 모음`
   - Public/Private 선택
   - "Initialize this repository with a README" 체크 해제
4. "Create repository" 클릭

## 2. 로컬 Git 저장소 설정

```bash
# 프로젝트 디렉토리로 이동
cd /Users/hongmin/.openclaw/workspace/openclaw-automations

# Git 초기화
git init

# 모든 파일 추가
git add .

# 첫 커밋
git commit -m "feat: Initial commit - OpenClaw automation scripts"

# GitHub 원격 저장소 추가
git remote add origin https://github.com/YOUR_USERNAME/openclaw-automations.git

# 메인 브랜치 설정
git branch -M main

# GitHub에 푸시
git push -u origin main
```

## 3. GitHub 토큰 생성 (필요시)

만약 인증 오류가 발생하면:

1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. "Generate new token" → "Generate new token (classic)"
3. 권한 설정:
   - repo (전체 체크)
   - workflow (선택사항)
4. 토큰 생성 후 복사
5. 원격 저장소 URL에 토큰 포함:
   ```bash
   git remote set-url origin https://YOUR_TOKEN@github.com/YOUR_USERNAME/openclaw-automations.git
   git push -u origin main
   ```

## 4. 추가 설정 (선택사항)

### GitHub Actions 자동화
`.github/workflows/` 디렉토리에 CI/CD 워크플로우 추가 가능

### GitHub Pages
설정 → Pages → Source: `main` 브랜치, `/docs` 폴더

### GitHub Wiki
프로젝트 위키 활성화하여 추가 문서화

## 5. 파일 구조 확인

푸시 후 GitHub에서 다음 구조 확인:
```
openclaw-automations/
├── README.md
├── LICENSE
├── .gitignore
├── requirements.txt
├── screenshot-cleanup/
├── image-to-pdf-converter/
└── setup-guides/
```

## 6. 문제 해결

### 푸시 실패시
```bash
# 원격 저장소 확인
git remote -v

# 강제 푸시 (주의)
git push -f origin main

# 또는 새로 시작
rm -rf .git
git init
# ... 위 과정 반복
```

### 큰 파일 업로드
```bash
# Git LFS 설치 (이미지/PDF 파일용)
brew install git-lfs
git lfs install
git lfs track "*.pdf" "*.png"
git add .gitattributes
git commit -m "feat: Add Git LFS for large files"
```

## 7. 업데이트 방법

코드 수정 후:
```bash
# 변경사항 추가
git add .

# 커밋
git commit -m "feat: Update description"

# 푸시
git push origin main
```

## 8. 협업 설정

1. Settings → Collaborators → "Add people"
2. 협업자 GitHub username 입력
3. 권한 설정 (Write 권한 권장)

## 참고사항

- **보안**: `.gitignore`에 민감한 정보 포함되지 않도록 확인
- **라이선스**: MIT 라이선스로 자유로운 사용/수정/배포 가능
- **기여**: Issues, Pull Requests 통해 기여 유도

이제 프로젝트가 GitHub에 성공적으로 업로드되었습니다! 🎉