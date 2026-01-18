"""
퀀트 리스크 지표 시각화 (3-Panel)
"""
import matplotlib.pyplot as plt
import platform

if platform.system() == 'Windows':
    plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

def draw_composite_chart(ax, data):
    """
    복합 리스크 지수를 시각화합니다.
    
    Args:
        ax: matplotlib axes 객체
        data: 분석 결과 딕셔너리
    """
    ax.clear()
    idx = data["composite_idx"]
    curr_c = data["current_val"]
    
    # 과열/과매도 구간 표시
    ax.axhspan(80, 100, color='red', alpha=0.1)
    ax.axhspan(0, 20, color='blue', alpha=0.1)
    
    ax.plot(idx.index, idx.values, color='#2c3e50', linewidth=1.5)
    ax.axhline(50, color='gray', linestyle='--', alpha=0.5)
    
    # 현재 값 강조
    ax.scatter(idx.index[-1], curr_c, color='black', s=30, zorder=5)
    ax.annotate(f'{curr_c:.1f}', xy=(idx.index[-1], curr_c), xytext=(5, 5),
                textcoords='offset points', weight='bold', color='#c0392b',
                bbox=dict(boxstyle='round,pad=0.2', fc='yellow', alpha=0.5))
    
    ax.set_ylim(-5, 105)
    ax.set_title(f"복합 리스크 지수 (현재: {curr_c:.1f})", fontsize=10)
    ax.grid(True, alpha=0.2)

def draw_zscore_chart(ax, data):
    """
    Z-score를 시각화합니다.
    
    Args:
        ax: matplotlib axes 객체
        data: 분석 결과 딕셔너리
    """
    ax.clear()
    z = data["z_score"]
    curr_z = z.iloc[-1]
    
    # 기준선
    ax.axhline(2.0, color='red', linestyle='--', alpha=0.6)
    ax.axhline(-2.0, color='blue', linestyle='--', alpha=0.6)
    ax.axhline(0, color='black', linewidth=0.8)
    
    ax.plot(z.index, z.values, color='#8e44ad', linewidth=1.2)
    
    # 현재 값 강조
    ax.scatter(z.index[-1], curr_z, color='black', s=30, zorder=5)
    ax.annotate(f'{curr_z:+.2f}σ', xy=(z.index[-1], curr_z), xytext=(5, 0),
                textcoords='offset points', color='#8e44ad', weight='bold', va='center')
    
    ax.set_ylim(-4, 4)
    ax.set_title(f"통계적 괴리도 (현재 Z: {curr_z:+.2f}σ)", fontsize=10)
    ax.grid(True, alpha=0.2)
