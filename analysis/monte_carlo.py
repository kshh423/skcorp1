"""
몬테카를로 시뮬레이션 분석 엔진
"""
import numpy as np
from data import (
    load_sp500_data, 
    filter_by_date, 
    calculate_returns,
    calculate_percentile_rank,
    calculate_log_returns
)

def run_monte_carlo_analysis(file_path, start_date, forecast_days=252, 
                             iterations=10000, rank_mode='relative'):
    """
    몬테카를로 시뮬레이션 분석을 실행합니다.
    
    Args:
        file_path: CSV 파일 경로
        start_date: 분석 시작일
        forecast_days: 예측 기간 (일)
        iterations: 시뮬레이션 반복 횟수
        rank_mode: 'relative' (선택기간 상대순위) 또는 'absolute' (전체기간 절대순위)
    
    Returns:
        dict: 분석 결과 딕셔너리
    """
    try:
        # 데이터 로드 (하이브리드)
        print(f"\n📊 데이터 로딩 중...")
        print(f"   파일: {file_path}")
        print(f"   시작일: {start_date}")
        print(f"   예측 기간: {forecast_days}일")
        
        full_series = load_sp500_data(file_path)
        print(f"   전체 데이터: {len(full_series)}일 ({full_series.index[0]} ~ {full_series.index[-1]})")
        
        series = filter_by_date(full_series, start_date)
        print(f"   선택 데이터: {len(series)}일 ({series.index[0]} ~ {series.index[-1]})")
        
        # 데이터 충분성 검증
        if len(series) < forecast_days + 1:
            print(f"❌ 데이터 부족: {len(series)}일 < 필요: {forecast_days + 1}일")
            print(f"   해결: 시작일을 더 과거로 설정하거나, 분석 기간을 줄여주세요.")
            return None
        
        # 1. 순위 계산 (모드에 따라)
        returns = calculate_returns(series, forecast_days)
        print(f"   수익률 계산: {len(returns)}개")
        
        if len(returns) == 0:
            print("❌ 수익률 계산 결과가 비어있습니다.")
            return None
        
        if rank_mode == 'absolute':
            # 전체 기간 수익률로 절대 순위 계산
            full_returns = calculate_returns(full_series, forecast_days)
            print(f"   전체 수익률: {len(full_returns)}개")
            rank_ts = calculate_percentile_rank(returns, mode='absolute', full_returns=full_returns)
        else:
            # 선택 기간 내 상대 순위 계산
            rank_ts = calculate_percentile_rank(returns, mode='relative')
        
        print(f"   순위 계산: {len(rank_ts)}개")
        print(f"✅ 순위 데이터 준비 완료")
        
        # 2. 몬테카를로 시뮬레이션
        print(f"\n🎲 몬테카를로 시뮬레이션 시작...")
        S0 = series.iloc[-1]
        print(f"   현재 가격: ${S0:.2f}")
        
        log_returns = calculate_log_returns(series)
        log_returns = log_returns.dropna()
        
        if len(log_returns) == 0:
            print("❌ 로그 수익률 계산 실패")
            return None
        
        # 드리프트 및 변동성 계산
        drift = log_returns.mean() - (0.5 * log_returns.var())
        stdev = log_returns.std()
        
        print(f"   드리프트: {drift:.6f}, 변동성: {stdev:.6f}")
        
        # 시뮬레이션 실행
        daily_returns = np.exp(
            drift + stdev * np.random.normal(0, 1, (forecast_days, iterations))
        )
        
        price_list = np.zeros_like(daily_returns)
        price_list[0] = S0
        for t in range(1, forecast_days):
            price_list[t] = price_list[t - 1] * daily_returns[t]
        
        # 최종 수익률 계산
        final_prices = price_list[-1]
        sim_returns_pct = ((final_prices - S0) / S0) * 100
        
        print(f"✅ 시뮬레이션 완료 ({iterations}회)")
        
        # 반환 전 데이터 검증
        print(f"\n🔍 반환 데이터 검증:")
        print(f"   rank_ts 타입: {type(rank_ts)}")
        print(f"   rank_ts 길이: {len(rank_ts)}")
        
        result = {
            "current_price": S0,
            "price_list": price_list,
            "returns_pct": sim_returns_pct,
            "days": forecast_days,
            "percentile": float(rank_ts.iloc[-1]) if len(rank_ts) > 0 else 50.0,
            "rank_ts": rank_ts,
            "rank_mode": rank_mode
        }
        
        print(f"   result['rank_ts'] 타입: {type(result['rank_ts'])}")
        print(f"   result['rank_ts'] 샘플 (처음 3개): {result['rank_ts'].head(3).tolist()}")
        
        return result
        
    except Exception as e:
        print(f"\n❌ Error in monte_carlo.py: {e}")
        import traceback
        traceback.print_exc()
        return None
