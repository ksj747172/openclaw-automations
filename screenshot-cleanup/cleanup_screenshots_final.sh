#!/bin/bash

# 최종 스크린샷 삭제 스크립트
DAYS_OLD=${1:-14}

echo "=== Screenshot Cleanup (older than $DAYS_OLD days) ==="
echo "Started at: $(date)"
echo ""

# 현재 시간 (초 단위)
NOW=$(date +%s)
# DAYS_OLD일 전의 시간 (초 단위)
CUTOFF=$((NOW - DAYS_OLD * 86400))

echo "Current time: $(date)"
echo "Cutoff time: $(date -r $CUTOFF)"
echo ""

# 데스크탑에서 삭제
echo "=== Checking Desktop ==="
find ~/Desktop -name "*.png" -type f 2>/dev/null | while read file; do
    filename=$(basename "$file")
    
    # 파일명에 "스크린샷" 또는 "screenshot"이 포함되어 있는지 확인
    if [[ "$filename" =~ 스크린샷 ]] || [[ "$filename" =~ [Ss]creenshot ]]; then
        # 파일 수정 시간 (초 단위)
        FILE_TIME=$(stat -f "%m" "$file" 2>/dev/null)
        
        if [ -n "$FILE_TIME" ] && [ $FILE_TIME -lt $CUTOFF ]; then
            DAYS_AGO=$(( (NOW - FILE_TIME) / 86400 ))
            echo "Deleting: $filename (modified $(date -r $FILE_TIME), $DAYS_AGO days ago)"
            rm "$file"
        fi
    fi
done

echo ""
echo "=== Checking Downloads ==="
find ~/Downloads -name "*.png" -type f 2>/dev/null | while read file; do
    filename=$(basename "$file")
    
    # 파일명에 "스크린샷" 또는 "screenshot"이 포함되어 있는지 확인
    if [[ "$filename" =~ 스크린샷 ]] || [[ "$filename" =~ [Ss]creenshot ]]; then
        # 파일 수정 시간 (초 단위)
        FILE_TIME=$(stat -f "%m" "$file" 2>/dev/null)
        
        if [ -n "$FILE_TIME" ] && [ $FILE_TIME -lt $CUTOFF ]; then
            DAYS_AGO=$(( (NOW - FILE_TIME) / 86400 ))
            echo "Deleting: $filename (modified $(date -r $FILE_TIME), $DAYS_AGO days ago)"
            rm "$file"
        fi
    fi
done

echo ""
echo "Cleanup completed at: $(date)"