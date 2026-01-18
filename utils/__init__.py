"""
한글 폰트 설정 유틸리티
Linux, Mac, Windows 환경에서 자동으로 한글 폰트 설정
"""
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import platform
import os
import warnings

def setup_korean_font():
    """
    운영체제에 맞는 한글 폰트를 자동으로 설정합니다.
    """
    system = platform.system()
    
    # 기본 폰트 리스트 가져오기
    font_list = [f.name for f in fm.fontManager.ttflist]
    
    # 운영체제별 폰트 우선순위
    if system == 'Windows':
        fonts = ['Malgun Gothic', 'NanumGothic', 'NanumBarunGothic']
    elif system == 'Darwin':  # Mac
        fonts = ['AppleGothic', 'NanumGothic', 'NanumBarunGothic', 'Arial Unicode MS']
    if system == 'Linux':
            nanum_path = '/usr/share/fonts/truetype/nanum/NanumGothic.ttf'
            if os.path.exists(nanum_path):
                fm.fontManager.addfont(nanum_path)
                plt.rcParams['font.family'] = 'NanumGothic'
                plt.rcParams['axes.unicode_minus'] = False
                return 'NanumGothic'
    # 사용 가능한 폰트 찾기
    selected_font = None
    for font in fonts:
        if font in font_list:
            selected_font = font
            break
    
    # 폰트 설정
    if selected_font:
        plt.rcParams['font.family'] = selected_font
        print(f"✅ 한글 폰트 설정: {selected_font}")
    else:
        # 폴백: sans-serif
        plt.rcParams['font.family'] = 'sans-serif'
        warnings.warn(f"⚠️  한글 폰트를 찾을 수 없습니다. 기본 폰트를 사용합니다.\n"
                     f"   사용 가능한 폰트: {', '.join(font_list[:5])}...")
        print(f"⚠️  한글 폰트 미설정 - 기본 폰트 사용")
    
    # 마이너스 기호 깨짐 방지
    plt.rcParams['axes.unicode_minus'] = False
    
    return selected_font

def install_font_guide():
    """
    폰트 설치 가이드를 반환합니다.
    """
    system = platform.system()
    
    if system == 'Linux':
        return """
        ### Linux 한글 폰트 설치 가이드
        
        **Ubuntu/Debian:**
        ```bash
        sudo apt-get update
        sudo apt-get install fonts-nanum fonts-nanum-coding
        ```
        
        **CentOS/RHEL:**
        ```bash
        sudo yum install naver-nanum-fonts
        ```
        
        **설치 후:**
        ```bash
        fc-cache -fv
        rm -rf ~/.cache/matplotlib
        ```
        """
    elif system == 'Darwin':
        return """
        ### Mac 한글 폰트 설치 가이드
        
        **Homebrew 사용:**
        ```bash
        brew tap homebrew/cask-fonts
        brew install --cask font-nanum-gothic
        ```
        
        **수동 설치:**
        1. https://hangeul.naver.com/font 접속
        2. 나눔고딕 다운로드
        3. 폰트 파일 더블클릭하여 설치
        
        **설치 후:**
        ```bash
        rm -rf ~/.matplotlib
        ```
        """
    else:  # Windows
        return """
        ### Windows 한글 폰트
        
        **Windows에는 기본적으로 '맑은 고딕'이 설치되어 있습니다.**
        
        만약 문제가 있다면:
        1. 제어판 → 글꼴 확인
        2. '맑은 고딕' 또는 '나눔고딕' 확인
        """

if __name__ == "__main__":
    # 테스트
    setup_korean_font()
    print(install_font_guide())
