#!/bin/bash

# 간단한 스크린샷 삭제 스크립트
DAYS_OLD=${1:-14}

echo "=== Screenshot Cleanup (older than $DAYS_OLD days) ==="
echo "Started at: $(date)"

# 데스크탑에서 삭제
echo "Checking Desktop..."
find ~/Desktop -name "*.png" -type f -mtime +$DAYS_OLD 2>/dev/null | while read file; do
    filename=$(basename "$file")
    if [[ "$filename" =~ 스크린샷 ]] || [[ "$filename" =~ [Ss]creenshot ]]; then
        echo "Deleting: $file"
        rm "$file"
    fi
done

# 다운로드 폴더에서 삭제
echo "Checking Downloads..."
find ~/Downloads -name "*.png" -type f -mtime +$DAYS_OLD 2>/dev/null | while read file; do
    filename=$(basename "$file")
    if [[ "$filename" =~ 스크린샷 ]] || [[ "$filename" =~ [Ss]creenshot ]]; then
        echo "Deleting: $file"
        rm "$file"
    fi
done

echo "Cleanup completed at: $(date)"