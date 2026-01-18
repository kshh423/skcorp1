"""
S&P 500 종합 퀀트 분석 시스템 - Streamlit 버전
v2.0 - 하이브리드 데이터 로딩 + 순위 모드 선택
"""
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager
import platform

# 한글 폰트 설정
from utils import setup_korean_font, install_font_guide

# 분석 엔진
from analysis import run_monte_carlo_analysis, run_quant_analysis

# 시각화
from visualizations import (
    draw_simulation_chart,
    draw_distribution_chart,
    draw_percentile_chart,
    draw_composite_chart,
    draw_zscore_chart
)

# 한글 폰트 초기화
font_name = setup_korean_font()

# 페이지 설정
st.set_page_config(
    #page_title="S&P 500 퀀트 분석 시스템",
    #page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 제목
st.title("S&P 500 분석 시스템 v2.0")
#st.markdown("---")

# 사이드바 - 전역 설정
with st.sidebar:
    st.header("⚙️ 분석 설정")
    
    # 시작일
    start_date = st.date_input(
        "분석 시작일",
        value=pd.to_datetime("2010-01-01"),
        min_value=pd.to_datetime("1928-01-03"),
        max_value=pd.to_datetime("today"),
        help="분석을 시작할 날짜를 선택하세요"
    )
    
    # 분석 기간
    forecast_days = st.number_input(
        "분석 기간 (일)",
        min_value=20,
        max_value=1000,
        value=252,
        step=1,
        help="수익률 계산 기간 (252일 = 약 1년)"
    )
    
    # 순위 모드
    rank_mode = st.selectbox(
        "순위 모드",
        options=["relative", "absolute"],
        format_func=lambda x: "상대순위 (선택 기간 내)" if x == "relative" else "절대순위 (전체 기간)",
        help="• relative: 선택 기간 내에서의 상대적 순위\n• absolute: 1928년부터 전체 기간 대비 절대적 순위"
    )
    
    #st.markdown("---")
    
    # 정보
    st.info("""
    **💡 사용 팁**
    - 시작일을 최근으로 설정하면 최근 추세 분석
    - 기간을 252일(1년)로 설정하면 연간 수익률 분석
    - relative 모드: 최근 동향 파악
    - absolute 모드: 역사적 위치 파악
    """)
    
    #st.markdown("---")
    st.caption("v2.0 | 하이브리드 데이터 로딩")

# 탭 생성
tab1, tab2 = st.tabs(["📈 종합 분석 (Monte Carlo)", "📊 퀀트 리스크 분석"])

# ========================================
# TAB 1: 몬테카를로 시뮬레이션
# ========================================
with tab1:
    #st.header("📈 종합 분석 (Monte Carlo)")
    
    # 옵션
    col_opt1, col_opt2, col_opt3 = st.columns([2, 2, 2])
    with col_opt1:
        show_label = st.checkbox("수익률 수치 표시", value=True, key="tab1_label")
    with col_opt2:
        show_price_bg = st.checkbox("하단 그래프 가격 배경", value=False, key="tab1_price_bg")
    with col_opt3:
        run_analysis_btn = st.button("🚀 분석 실행", type="primary", key="tab1_run", use_container_width=True)
    

    
    # 분석 실행
    if run_analysis_btn or 'tab1_data' in st.session_state:
        if run_analysis_btn:
            with st.spinner("📊 몬테카를로 시뮬레이션 실행 중..."):
                try:
                    start_date_str = start_date.strftime("%Y-%m-%d")
                    data = run_monte_carlo_analysis(
                        "sp500.csv",
                        start_date_str,
                        forecast_days=int(forecast_days),
                        rank_mode=rank_mode
                    )
                    
                    if data:
                        st.session_state['tab1_data'] = data
                        st.success("✅ 분석 완료!")
                    else:
                        st.error("❌ 분석 실패: 데이터가 부족하거나 오류가 발생했습니다.")
                        st.stop()
                        
                except Exception as e:
                    st.error(f"❌ 분석 실패: {str(e)}")
                    st.stop()
        
        # 데이터 가져오기
        data = st.session_state.get('tab1_data')
        
        if data:
            # 결과 요약
            mode_text = "절대순위" if data.get("rank_mode") == "absolute" else "상대순위"
            current_percentile = data.get('percentile', 50)
            
            # 메트릭 표시
            col_m1, col_m2, col_m3, col_m4 = st.columns(4)
            with col_m1:
                st.metric("현재 가격", f"${data['current_price']:,.2f}")
            with col_m2:
                st.metric("순위 모드", mode_text)
            with col_m3:
                rank_value = 100 - current_percentile
                st.metric("현재 순위", f"상위 {rank_value:.1f}%")
            with col_m4:
                mean_return = np.mean(data['returns_pct'])
                st.metric("예상 평균 수익률", f"{mean_return:+.2f}%")
            
            st.markdown("---")
            
            # 차트 그리기
            fig = plt.figure(figsize=(14, 10))
            
            # 좌상: 시뮬레이션
            ax1 = fig.add_subplot(221)
            draw_simulation_chart(ax1, data, show_label=show_label)
            
            # 우상: 분포
            ax2 = fig.add_subplot(222)
            draw_distribution_chart(ax2, data)
            
            # 하단: 순위
            ax3 = fig.add_subplot(212)
            start_date_str = start_date.strftime("%Y-%m-%d")
            draw_percentile_chart(
                ax3, data,
                show_price_bg=show_price_bg,
                start_date=start_date_str,
                title=f"역사적 순위 지표 ({mode_text})"
            )
            
            fig.tight_layout()
            st.pyplot(fig)
            plt.close(fig)
            
    else:
        st.info("👈 좌측 설정을 확인하고 **🚀 분석 실행** 버튼을 눌러주세요.")

# ========================================
# TAB 2: 퀀트 리스크 분석
# ========================================
with tab2:
    #st.header("📊 퀀트 리스크 분석 (3-Panel)")
    
    # 옵션
    col_opt1, col_opt2 = st.columns([5, 2])
    with col_opt1:
        st.info("💡 전역 설정(좌측 사이드바)이 자동으로 연동됩니다.")
    with col_opt2:
        run_quant_btn = st.button("🚀 퀀트 지표 실행", type="primary", key="tab2_run", use_container_width=True)
    

    
    # 분석 실행
    if run_quant_btn or 'tab2_data' in st.session_state:
        if run_quant_btn:
            with st.spinner("📊 퀀트 지표 계산 중..."):
                try:
                    start_date_str = start_date.strftime("%Y-%m-%d")
                    data = run_quant_analysis(
                        "sp500.csv",
                        start_date_str,
                        lookback=int(forecast_days),
                        rank_mode=rank_mode
                    )
                    
                    if data:
                        st.session_state['tab2_data'] = data
                        st.success("✅ 분석 완료!")
                    else:
                        st.error("❌ 분석 실패: 데이터가 부족하거나 오류가 발생했습니다.")
                        st.stop()
                        
                except Exception as e:
                    st.error(f"❌ 분석 실패: {str(e)}")
                    st.stop()
        
        # 데이터 가져오기
        data = st.session_state.get('tab2_data')
        
        if data:
            # 결과 요약
            mode_text = "절대순위" if data.get("rank_mode") == "absolute" else "상대순위"
            current_composite = data.get('current_val', 50)
            current_z = data['z_score'].iloc[-1] if len(data['z_score']) > 0 else 0
            current_percentile = data['percentile'].iloc[-1] if len(data['percentile']) > 0 else 50
            
            # 메트릭 표시
            col_m1, col_m2, col_m3, col_m4 = st.columns(4)
            with col_m1:
                st.metric("순위 모드", mode_text)
            with col_m2:
                rank_value = 100 - current_percentile
                st.metric("현재 순위", f"상위 {rank_value:.1f}%")
            with col_m3:
                st.metric("복합 리스크 지수", f"{current_composite:.1f}")
            with col_m4:
                st.metric("Z-score", f"{current_z:+.2f}σ")
            
            st.markdown("---")
            
            # 차트 그리기
            fig = plt.figure(figsize=(14, 12))
            
            # 상단: 백분위
            ax1 = fig.add_subplot(311)
            draw_percentile_chart(ax1, data, title=f"1. 역사적 순위 ({mode_text})")
            
            # 중간: 복합 지수
            ax2 = fig.add_subplot(312)
            draw_composite_chart(ax2, data)
            
            # 하단: Z-score
            ax3 = fig.add_subplot(313)
            draw_zscore_chart(ax3, data)
            
            fig.tight_layout()
            st.pyplot(fig)
            plt.close(fig)
            
    else:
        st.info("👈 좌측 설정을 확인하고 **🚀 퀀트 지표 실행** 버튼을 눌러주세요.")

# Footer
st.markdown("---")

# 폰트 정보
if font_name:
    st.caption(f"🔤 사용 중인 폰트: {font_name}")
else:
    with st.expander("⚠️ 한글 폰트가 설정되지 않았습니다. 설치 가이드 보기"):
        st.markdown(install_font_guide())

st.caption("""
📊 S&P 500 종합 퀀트 분석 시스템 v2.0  
🔹 하이브리드 데이터: CSV (1928~2025) + yfinance (2026~)  
🔹 분석 엔진: Monte Carlo 시뮬레이션 (10,000회) + 퀀트 지표  
""")
