#!/bin/bash

# 작동하는 스크린샷 삭제 스크립트
DAYS_OLD=${1:-14}

echo "=== Screenshot Cleanup (older than $DAYS_OLD days) ==="
echo "Started at: $(date)"
echo ""

# 현재 시간 (초 단위)
NOW=$(date +%s)
# DAYS_OLD일 전의 시간 (초 단위)
CUTOFF=$((NOW - DAYS_OLD * 86400))

TOTAL_DELETED=0

# 데스크탑에서 삭제
echo "=== Checking Desktop ==="
find ~/Desktop -name "*.png" -type f 2>/dev/null | while read file; do
    # 파일 수정 시간 (초 단위)
    FILE_TIME=$(stat -f "%m" "$file" 2>/dev/null)
    
    if [ -n "$FILE_TIME" ] && [ $FILE_TIME -lt $CUTOFF ]; then
        DAYS_AGO=$(( (NOW - FILE_TIME) / 86400 ))
        echo "Found old file ($DAYS_AGO days): $(basename "$file")"
        rm "$file" && {
            echo "  -> Deleted"
            TOTAL_DELETED=$((TOTAL_DELETED + 1))
        }
    fi
done

# 다운로드 폴더에서 삭제
echo ""
echo "=== Checking Downloads ==="
find ~/Downloads -name "*.png" -type f 2>/dev/null | while read file; do
    # 파일 수정 시간 (초 단위)
    FILE_TIME=$(stat -f "%m" "$file" 2>/dev/null)
    
    if [ -n "$FILE_TIME" ] && [ $FILE_TIME -lt $CUTOFF ]; then
        DAYS_AGO=$(( (NOW - FILE_TIME) / 86400 ))
        echo "Found old file ($DAYS_AGO days): $(basename "$file")"
        rm "$file" && {
            echo "  -> Deleted"
            TOTAL_DELETED=$((TOTAL_DELETED + 1))
        }
    fi
done

echo ""
echo "=== Summary ==="
echo "Total deleted: $TOTAL_DELETED files"
echo "Cleanup completed at: $(date)"