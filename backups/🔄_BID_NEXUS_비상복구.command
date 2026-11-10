#!/bin/bash
export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:$PATH"
cd ~/bid-nexus || exit 1

echo "=========================================================="
echo " 🔄 BID-NEXUS 골든 마스터(GOLDEN_MASTER_LATEST) 1초 복원 중..."
echo "=========================================================="

killall -9 Python python python3 streamlit 2>/dev/null || true

if [ -f "backups/GOLDEN_MASTER_LATEST.zip" ]; then
    unzip -o backups/GOLDEN_MASTER_LATEST.zip -d ~/bid-nexus/
    echo "✅ 골든 마스터 원본 코드 및 로컬 ML 엔진 복원 완료!"
fi

nohup python3 -m streamlit run app_v3_boutique.py \
    --server.port=8505 \
    --server.headless=true > /tmp/bid_nexus_8505.log 2>&1 &

for i in {1..15}; do
    if lsof -i :8505 >/dev/null 2>&1; then
        open -a Safari "http://localhost:8505"
        exit 0
    fi
    sleep 1
done
