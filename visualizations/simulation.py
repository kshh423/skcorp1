"""
몬테카를로 시뮬레이션 시각화
"""
import matplotlib.pyplot as plt
import numpy as np

def draw_simulation_chart(ax, data, show_label=True):
    """
    몬테카를로 시뮬레이션 결과를 시각화합니다.
    
    Args:
        ax: matplotlib axes 객체
        data: 분석 결과 딕셔너리
        show_label: 라벨 표시 여부
    """
    ax.clear()
    
    S0 = data["current_price"]
    price_list = data["price_list"]
    days = data["days"]
    
    # 수익률로 변환
    returns_paths_all = (price_list / S0 - 1) * 100
    paths_subset = returns_paths_all[:, :100]
    x = np.arange(days)
    
    # 1. 배경 시나리오
    ax.plot(x, paths_subset, color='#5d6d7e', alpha=0.25, linewidth=0.7)
    
    # 2. 분위수 계산
    p95 = np.percentile(returns_paths_all, 95, axis=1)
    p75 = np.percentile(returns_paths_all, 75, axis=1)
    p50 = np.percentile(returns_paths_all, 50, axis=1)
    p25 = np.percentile(returns_paths_all, 25, axis=1)
    p5 = np.percentile(returns_paths_all, 5, axis=1)
    
    # 3. 신뢰구간
    ax.fill_between(x, p5, p95, color='#3498db', alpha=0.15, label='90% 범위')
    ax.fill_between(x, p25, p75, color='#2980b9', alpha=0.25, label='50% 범위')
    
    # 4. 중윗값
    ax.plot(x, p50, color='#1c4966', linewidth=2, label='중윗값')
    
    if show_label:
        median_val = p50[-1]
        ax.annotate(f' 중윗값: {median_val:+.1f}%', 
                    xy=(days-1, median_val), xytext=(5, 0),
                    textcoords='offset points', va='center', weight='bold',
                    bbox=dict(boxstyle='round,pad=0.2', fc='white', alpha=0.8, ec='#1c4966'))
    
    ax.axhline(0, color='black', linewidth=1, alpha=0.5)
    ax.set_title("S&P 500 향후 수익률 시나리오", fontsize=11, weight='bold')
    if show_label:
        ax.legend(loc='upper left', fontsize='x-small')
    ax.grid(True, alpha=0.15)
