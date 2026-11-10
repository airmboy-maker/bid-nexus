#!/bin/bash
cd ~/bid-nexus
pkill -f "streamlit run" 2>/dev/null || true
git checkout v3-boutique
git reset --hard v3.0-golden-master
git clean -fd
echo "✅ [복귀 완료] v3.0-golden-master (9829a22) 최종본 상태로 100% 원상복구되었습니다."
open http://127.0.0.1:8502
python3 -m streamlit run app_v3_boutique.py --server.address=0.0.0.0 --server.port=8502 --server.headless=true --browser.gatherUsageStats=false --logger.level=error
