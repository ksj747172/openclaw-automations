# Memory Hygiene 설정 가이드

## 현재 메모리 상태 확인
```bash
# 메모리 검색 테스트
openclaw memory search "test" 2>/dev/null || echo "Memory search not available"

# 메모리 상태 확인
openclaw memory status 2>/dev/null || echo "Memory status not available"
```

## 메모리 플러그인 설정 (필요시)
```bash
# 메모리 플러그인 활성화
openclaw config set plugins.entries.memory-lancedb.config.autoCapture false
openclaw config set plugins.entries.memory-lancedb.config.autoRecall true

# 설정 적용
openclaw gateway restart
```

## 정기적인 메모리 관리 설정
```bash
# 월별 메모리 정리 크론 작업 추가
openclaw cron add --name "memory-maintenance" --schedule "0 4 1 * *" --command "echo 'Monthly memory maintenance scheduled'"
```

## 메모리 사용 모범 사례

### 저장해야 할 정보:
- 사용자 선호도 (도구, 워크플로우, 커뮤니케이션 스타일)
- 중요한 결정 (프로젝트 선택, 아키텍처)
- 주요 사실 (계정, 자격 증명 위치, 연락처)
- 배운 교훈

### 저장하지 말아야 할 정보:
- Heartbeat 상태 ("HEARTBEAT_OK", "새 메시지 없음")
- 일시적 정보 (현재 시간, 임시 상태)
- 원시 메시지 로그 (이미 파일에 저장됨)
- OAuth URL 또는 토큰

## 메모리 초기화 (필요시)
```bash
# 벡터 메모리 삭제
rm -rf ~/.clawdbot/memory/lancedb/ 2>/dev/null || echo "Memory directory not found"

# 게이트웨이 재시작
openclaw gateway restart
```

## MEMORY.md에서 주요 사실 재저장
```bash
# MEMORY.md에서 중요한 정보 추출 및 저장
# (수동으로 진행 필요)
echo "Memory hygiene setup complete. Manual review of MEMORY.md recommended."