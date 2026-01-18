"""
수익률 및 통계 지표 계산 모듈
"""
import numpy as np

def calculate_returns(series, lookback):
    """
    N일 수익률을 계산합니다.
    
    Args:
        series: 가격 시계열
        lookback: 수익률 계산 기간 (일)
    
    Returns:
        pd.Series: 수익률 시계열 (%)
    """
    return series.pct_change(lookback).dropna()

def calculate_percentile_rank(returns, mode='relative', full_returns=None):
    """
    수익률의 백분위 순위를 계산합니다 (0~100).
    
    Args:
        returns: 수익률 시계열 (선택 기간)
        mode: 'relative' (상대순위) 또는 'absolute' (절대순위)
        full_returns: 전체 기간 수익률 (절대순위 모드일 때 필요)
    
    Returns:
        pd.Series: 백분위 순위 시계열
    """
    if mode == 'absolute' and full_returns is not None:
        # 절대 순위: 전체 기간 분포 기준
        sorted_values = np.sort(full_returns.values)
        return returns.apply(
            lambda x: (np.searchsorted(sorted_values, x) / len(sorted_values)) * 100
        )
    else:
        # 상대 순위: 선택 기간 내 분포 기준
        sorted_values = np.sort(returns.values)
        return returns.apply(
            lambda x: (np.searchsorted(sorted_values, x) / len(sorted_values)) * 100
        )

def calculate_zscore(returns):
    """
    Z-score를 계산합니다.
    
    Args:
        returns: 수익률 시계열
    
    Returns:
        pd.Series: Z-score 시계열
    """
    return (returns - returns.mean()) / returns.std()

def calculate_log_returns(series):
    """
    로그 수익률을 계산합니다 (몬테카를로용).
    
    Args:
        series: 가격 시계열
    
    Returns:
        pd.Series: 로그 수익률
    """
    return np.log(1 + series.pct_change())
