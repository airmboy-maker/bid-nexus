#!/bin/bash
export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:$PATH"
cd ~/bid-nexus || exit 1

echo "=========================================================="
echo " ⚡ BID-NEXUS v3.0 로컬 ML 자율 입찰 터미널 시동 중..."
echo "=========================================================="

# 1. 기존 중복 실행 중인 프로세스 정리
killall -9 Python python python3 streamlit 2>/dev/null || true

# 2. 백그라운드에서 Streamlit 서버 구동 (8505 포트)
nohup python3 -m streamlit run app_v3_boutique.py \
    --server.port=8505 \
    --server.headless=true > /tmp/bid_nexus_8505.log 2>&1 &

# 3. 8505 포트 리스닝 확인 후 즉시 Safari 브라우저 오픈
echo "⏳ 로컬 서버(8505 포트) 연결 대기 중..."
for i in {1..15}; do
    if lsof -i :8505 >/dev/null 2>&1; then
        echo "✅ 서버 가동 완료! 사파리(Safari) 브라우저를 엽니다."
        open -a Safari "http://localhost:8505"
        sleep 1
        exit 0
    fi
    sleep 1
done

echo "⚠️ 부팅이 지연되고 있습니다. 사파리를 직접 호출합니다."
open -a Safari "http://localhost:8505"
