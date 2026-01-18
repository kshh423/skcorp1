"""
수익률 확률 분포 시각화
"""
import matplotlib.pyplot as plt
import numpy as np

def draw_distribution_chart(ax, data):
    """
    최종 수익률 확률 분포를 시각화합니다.
    
    Args:
        ax: matplotlib axes 객체
        data: 분석 결과 딕셔너리
    """
    ax.clear()
    rets = data["returns_pct"]
    
    # 히스토그램
    n, bins, patches = ax.hist(rets, bins=50, color='teal', alpha=0.3, edgecolor='white')
    
    # 0% 기준 색상 구분
    for i in range(len(patches)):
        if bins[i] < 0:
            patches[i].set_facecolor('#e74c3c')  # 손실: 빨강
        else:
            patches[i].set_facecolor('#2ecc71')  # 수익: 초록
    
    # 통계 계산
    win_rate = np.mean(rets > 0) * 100
    mean_ret = np.mean(rets)
    var_95 = np.percentile(rets, 5)
    
    stats_text = (f"승률: {win_rate:.1f}%\n"
                  f"평균 수익: {mean_ret:+.1f}%\n"
                  f"리스크(하위5%): {var_95:.1f}%")
    
    # 텍스트 박스
    ax.text(0.95, 0.95, stats_text, transform=ax.transAxes, fontsize=9,
            verticalalignment='top', horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    ax.axvline(0, color='black', linewidth=1.5)
    ax.axvline(mean_ret, color='blue', linestyle='--', linewidth=1)
    
    ax.set_title("최종 수익률 확률 분포", fontsize=10)
    ax.set_xlabel("수익률 (%)")
    ax.set_ylabel("발생 빈도")
    ax.grid(True, alpha=0.2)
