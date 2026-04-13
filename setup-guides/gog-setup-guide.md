# Google Workspace CLI (gog) 설정 가이드

## 1. Google Cloud Console 설정
1. https://console.cloud.google.com/ 접속
2. 새 프로젝트 생성 또는 기존 프로젝트 선택
3. "API 및 서비스" → "사용자 인증 정보"
4. "사용자 인증 정보 만들기" → "OAuth 2.0 클라이언트 ID"
5. 애플리케이션 유형: "데스크톱 애플리케이션"
6. 클라이언트 ID 생성 후 JSON 다운로드

## 2. gog 인증 설정
```bash
# 다운로드한 client_secret.json 파일로 인증 설정
gog auth credentials /path/to/client_secret.json

# Google 계정 추가 (여러 서비스 활성화)
gog auth add you@gmail.com --services gmail,calendar,drive,contacts,sheets,docs

# 인증된 계정 확인
gog auth list
```

## 3. 환경 변수 설정 (선택사항)
```bash
# 기본 계정 설정
export GOG_ACCOUNT="you@gmail.com"

# 설정 파일에 추가하려면:
echo 'export GOG_ACCOUNT="you@gmail.com"' >> ~/.zshrc
source ~/.zshrc
```

## 4. 테스트 명령어
```bash
# Gmail 테스트
gog gmail search 'newer_than:7d' --max 5

# Calendar 테스트
gog calendar events primary --from $(date -I) --to $(date -I -d "+7 days")

# Drive 테스트
gog drive search "document" --max 5
```

## 참고사항
- 첫 실행 시 브라우저에서 Google 로그인 필요
- API 범위에 따라 추가 승인 필요할 수 있음
- 보안을 위해 client_secret.json 파일 안전하게 보관