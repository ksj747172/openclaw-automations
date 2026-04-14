#!/bin/bash
# Traveloka 이메일을 PDF로 변환하는 전체 프로세스 실행

set -e

echo "=== Traveloka 이메일 PDF 변환 시작 ==="
echo ""

# 작업 디렉토리
WORKDIR="/Users/hongmin/Documents/traveloka_emails"
mkdir -p "$WORKDIR"
cd "$WORKDIR"

echo "작업 디렉토리: $WORKDIR"
echo ""

# 1. 환경 변수 확인
if [ -z "$NAVER_EMAIL" ] || [ -z "$NAVER_PASSWORD" ]; then
    echo "⚠️ 환경 변수가 설정되지 않았습니다."
    echo "테스트 모드로 실행합니다."
    echo ""
    echo "실제 이메일을 가져오려면:"
    echo "export NAVER_EMAIL='your_id@naver.com'"
    echo "export NAVER_PASSWORD='your_password'"
    echo ""
    
    TEST_MODE=true
else
    TEST_MODE=false
    echo "✅ 환경 변수 확인 완료"
    echo ""
fi

# 2. Python 스크립트 복사
echo "스크립트 준비 중..."
cp /Users/hongmin/.openclaw/workspace/fetch_traveloka_emails.py .
cp /Users/hongmin/.openclaw/workspace/emails_to_pdf.py .

# 3. 이메일 가져오기
echo "이메일 가져오는 중..."
if [ "$TEST_MODE" = true ]; then
    python3 fetch_traveloka_emails.py
else
    python3 fetch_traveloka_emails.py
fi

echo ""

# 4. PDF 생성
echo "PDF 생성 중..."
python3 emails_to_pdf.py

echo ""

# 5. 결과 확인
echo "=== 결과 확인 ==="
ls -la *.pdf *.json 2>/dev/null || echo "생성된 파일이 없습니다."

echo ""

# 6. 정리
echo "임시 파일 정리..."
rm -f fetch_traveloka_emails.py emails_to_pdf.py

echo ""
echo "=== 완료 ==="
echo "Traveloka 이메일 PDF 변환 프로세스가 완료되었습니다."