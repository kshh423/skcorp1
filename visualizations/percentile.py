"""
백분위 순위 시각화 (Tab 1, Tab 2 공용)
"""
import matplotlib.pyplot as plt
import pandas as pd

def draw_percentile_chart(ax, data, show_price_bg=False, start_date=None, 
                          show_label=True, title="백분위 순위"):
    """
    백분위 순위 차트를 시각화합니다.
    
    Args:
        ax: matplotlib axes 객체
        data: 분석 결과 딕셔너리
        show_price_bg: 가격 배경 표시 여부
        start_date: 시작일 (가격 배경용)
        show_label: 현재 값 라벨 표시 여부
        title: 차트 제목
    """
    ax.clear()
    
    # rank_ts 우선 확인 (Tab 1용), percentile은 Tab 2용
    if "rank_ts" in data:
        rank_ts = data["rank_ts"]
    elif "percentile" in data:
        rank_ts = data["percentile"]
    else:
        print("❌ percentile: data에 'rank_ts' 또는 'percentile' 키가 없습니다.")
        ax.text(0.5, 0.5, '데이터 오류: 순위 정보가 없습니다', 
                ha='center', va='center', transform=ax.transAxes, fontsize=12)
        return
    
    # rank_ts 타입 및 길이 확인
    print(f"🔍 percentile 차트: rank_ts 타입={type(rank_ts)}, 길이={len(rank_ts) if hasattr(rank_ts, '__len__') else 'N/A'}")
    
    # rank_ts가 유효한지 확인 (pandas Series 체크 완화)
    if not hasattr(rank_ts, 'index') or not hasattr(rank_ts, 'values'):
        print(f"❌ percentile: rank_ts가 유효한 Series가 아닙니다. 타입: {type(rank_ts)}")
        ax.text(0.5, 0.5, '데이터 오류: 순위 형식이 잘못되었습니다', 
                ha='center', va='center', transform=ax.transAxes, fontsize=12)
        return
    
    if len(rank_ts) == 0:
        print("❌ percentile: rank_ts가 비어있습니다.")
        ax.text(0.5, 0.5, '데이터 부족: 순위를 계산할 수 없습니다', 
                ha='center', va='center', transform=ax.transAxes, fontsize=12)
        return
    
    print(f"✅ percentile 차트: 데이터 유효 ({len(rank_ts)}개 포인트)")
    
    # 가격 배경 표시
    if show_price_bg and start_date:
        try:
            ax2 = ax.twinx()
            from data import load_sp500_data, filter_by_date
            full_series = load_sp500_data("sp500.csv")
            price_series = filter_by_date(full_series, start_date)
            
            ax2.plot(price_series.index, price_series.values, 
                    color='gray', linewidth=1, alpha=0.3, linestyle='-')
            ax2.set_ylabel("S&P 500 가격 (USD)", fontsize=9, color='gray')
            ax2.tick_params(axis='y', labelcolor='gray', labelsize=8)
            ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:,.0f}'))
            ax2.grid(False)
        except Exception as e:
            print(f"⚠️  가격 배경 표시 실패: {e}")
    
    # 메인 순위 선
    ax.plot(rank_ts.index, rank_ts.values, color='#2980b9', linewidth=1.2)
    
    # 기준선
    ax.axhline(75, color='red', linewidth=2, alpha=0.5, linestyle='--')
    ax.axhline(50, color='limegreen', linewidth=2, alpha=0.5, linestyle='--')
    ax.axhline(25, color='blue', linewidth=2, alpha=0.5, linestyle='--')
    
    # 현재 값 강조
    if show_label and len(rank_ts) > 0:
        current_val = rank_ts.iloc[-1]
        ax.scatter(rank_ts.index[-1], current_val, color='black', s=40, zorder=5)
        ax.annotate(f'{current_val:.1f}%', 
                    xy=(rank_ts.index[-1], current_val), 
                    xytext=(5, 5), textcoords='offset points',
                    ha='left', weight='bold',
                    bbox=dict(boxstyle='round,pad=0.3', fc='yellow', alpha=0.7))
    
    ax.set_ylim(-10, 110)
    ax.set_title(title, fontsize=11)
    ax.grid(axis='y', linestyle='--', alpha=0.3)
