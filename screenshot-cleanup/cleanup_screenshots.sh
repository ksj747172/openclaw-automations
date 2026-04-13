#!/bin/bash

# 스크린샷 파일 삭제 스크립트
# 설정: 삭제할 파일의 최소 일수 (기본: 7일)
DAYS_OLD=${1:-7}

LOG_FILE="/Users/hongmin/Library/Logs/cleanup_screenshots.log"
echo "$(date): Starting screenshot cleanup (files older than $DAYS_OLD days)..." >> "$LOG_FILE"

# LC_ALL을 설정하여 한글 파일명 처리
LC_ALL="ko_KR.UTF-8"
export LC_ALL

# 주요 폴더 목록
FOLDERS=(
    "/Users/hongmin/Desktop"
    "/Users/hongmin/Downloads"
    "/Users/hongmin/Documents"
    "/Users/hongmin/Pictures"
)

# 1. 먼저 어떤 파일이 삭제될지 확인 (테스트 모드)
echo "$(date): Files that would be deleted (test mode):" >> "$LOG_FILE"
for folder in "${FOLDERS[@]}"; do
    if [ -d "$folder" ]; then
        # 한글 "스크린샷" 파일 찾기
        find "$folder" -name "*.png" -type f -mtime +$DAYS_OLD 2>/dev/null | grep -i "스크린샷" | while read line; do
            echo "$(date): Would delete: $line" >> "$LOG_FILE"
        done
        # 영어 "screenshot" 파일 찾기
        find "$folder" -name "*.png" -type f -mtime +$DAYS_OLD 2>/dev/null | grep -i "screenshot" | while read line; do
            echo "$(date): Would delete: $line" >> "$LOG_FILE"
        done
    fi
done

# 2. 실제 삭제 실행
echo "$(date): Actually deleting files..." >> "$LOG_FILE"
DELETED_COUNT=0
for folder in "${FOLDERS[@]}"; do
    if [ -d "$folder" ]; then
        # 한글 "스크린샷" 파일 삭제
        find "$folder" -name "*.png" -type f -mtime +$DAYS_OLD 2>/dev/null | grep -i "스크린샷" | while read line; do
            rm -v "$line" 2>/dev/null && {
                echo "$(date): Deleted: $line" >> "$LOG_FILE"
                DELETED_COUNT=$((DELETED_COUNT + 1))
            }
        done
        # 영어 "screenshot" 파일 삭제
        find "$folder" -name "*.png" -type f -mtime +$DAYS_OLD 2>/dev/null | grep -i "screenshot" | while read line; do
            rm -v "$line" 2>/dev/null && {
                echo "$(date): Deleted: $line" >> "$LOG_FILE"
                DELETED_COUNT=$((DELETED_COUNT + 1))
            }
        done
    fi
done

echo "$(date): Cleanup completed. Deleted $DELETED_COUNT files." >> "$LOG_FILE"