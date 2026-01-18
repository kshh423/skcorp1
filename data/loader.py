"""
하이브리드 데이터 로딩 모듈
- 2025년까지: CSV 파일 사용
- 2026년 이후: yfinance로 실시간 데이터 가져오기
"""
import pandas as pd
import yfinance as yf
from datetime import datetime

def load_sp500_data(file_path="sp500.csv", use_live_data=True):
    """
    S&P 500 데이터를 하이브리드 방식으로 로드합니다.
    
    Args:
        file_path: CSV 파일 경로
        use_live_data: 2026년 이후 실시간 데이터 사용 여부
    
    Returns:
        pd.Series: 날짜를 인덱스로 하는 종가 시계열
    """
    # 1. 기본 CSV 로드 (1928 ~ 2025)
    df = pd.read_csv(file_path, index_col=0, parse_dates=True)
    csv_series = df['Close'] if 'Close' in df.columns else df.iloc[:, 0]
    csv_series = csv_series.dropna()
    
    # 2. 2026년 이후 데이터가 필요한지 확인
    if not use_live_data:
        return csv_series
    
    csv_last_date = csv_series.index[-1]
    today = pd.Timestamp.now()
    
    # CSV 데이터가 최신이면 그대로 반환
    if csv_last_date >= today - pd.Timedelta(days=7):
        return csv_series
    
    try:
        # 3. yfinance로 2026년 이후 데이터 가져오기
        print(f"📡 2026년 이후 데이터를 yfinance에서 가져오는 중...")
        ticker = yf.Ticker("^GSPC")
        
        # CSV 마지막 날짜 다음날부터 오늘까지
        start_date = (csv_last_date + pd.Timedelta(days=1)).strftime('%Y-%m-%d')
        live_data = ticker.history(start=start_date)
        
        if live_data.empty:
            print("⚠️  yfinance 데이터 없음. CSV만 사용합니다.")
            return csv_series
        
        # 4. 데이터 병합
        live_series = live_data['Close']
        live_series.index = live_series.index.tz_localize(None)  # 시간대 제거
        
        # CSV와 실시간 데이터 합치기
        combined_series = pd.concat([csv_series, live_series])
        combined_series = combined_series[~combined_series.index.duplicated(keep='last')]
        combined_series = combined_series.sort_index()
        
        print(f"✅ 데이터 로드 완료: {combined_series.index[0]} ~ {combined_series.index[-1]}")
        print(f"   CSV: {len(csv_series)}개, 실시간: {len(live_series)}개, 총: {len(combined_series)}개")
        
        return combined_series
        
    except Exception as e:
        print(f"⚠️  yfinance 로드 실패: {e}")
        print("   CSV 데이터만 사용합니다.")
        return csv_series

def filter_by_date(series, start_date):
    """
    시작일 이후의 데이터만 필터링합니다.
    
    Args:
        series: 전체 시계열 데이터
        start_date: 시작일 (문자열)
    
    Returns:
        pd.Series: 필터링된 시계열
    """
    return series.loc[start_date:]
