"""
퀀트 리스크 지표 분석 엔진
"""
import numpy as np
from data import (
    load_sp500_data,
    filter_by_date,
    calculate_returns,
    calculate_percentile_rank,
    calculate_zscore
)

def run_quant_analysis(file_path, start_date, lookback=252, rank_mode='relative'):
    """
    퀀트 리스크 지표 분석을 실행합니다.
    
    Args:
        file_path: CSV 파일 경로
        start_date: 분석 시작일
        lookback: 수익률 계산 기간 (일)
        rank_mode: 'relative' (선택기간 상대순위) 또는 'absolute' (전체기간 절대순위)
    
    Returns:
        dict: 분석 결과 딕셔너리
    """
    try:
        # 데이터 로드 (하이브리드)
        print(f"\n📊 Tab 2 데이터 로딩 중...")
        print(f"   시작일: {start_date}")
        print(f"   분석 기간: {lookback}일")
        
        full_series = load_sp500_data(file_path)
        print(f"   전체 데이터: {len(full_series)}일")
        
        series = filter_by_date(full_series, start_date)
        print(f"   선택 데이터: {len(series)}일")
        
        # 데이터 충분성 검증
        if len(series) < lookback + 1:
            print(f"❌ 데이터 부족: {len(series)}일 < 필요: {lookback + 1}일")
            return None
        
        # 수익률 계산
        returns = calculate_returns(series, lookback)
        print(f"   수익률 계산: {len(returns)}개")
        
        if len(returns) == 0:
            print("❌ 수익률 계산 결과가 비어있습니다.")
            return None
        
        # 백분위 순위 계산 (모드에 따라)
        if rank_mode == 'absolute':
            full_returns = calculate_returns(full_series, lookback)
            percentile = calculate_percentile_rank(returns, mode='absolute', full_returns=full_returns)
        else:
            percentile = calculate_percentile_rank(returns, mode='relative')
        
        # Z-score 계산
        z_score = calculate_zscore(returns)
        
        # 복합 지수 계산 (백분위 + 정규화된 Z-score의 평균)
        z_scaled = (z_score.clip(-3, 3) + 3) / 6 * 100
        composite_idx = (percentile + z_scaled) / 2
        
        return {
            "percentile": percentile,
            "z_score": z_score,
            "composite_idx": composite_idx,
            "lookback": lookback,
            "current_val": composite_idx.iloc[-1],
            "rank_mode": rank_mode
        }
        
    except Exception as e:
        print(f"Error in quant_metrics.py: {e}")
        import traceback
        traceback.print_exc()
        return None
