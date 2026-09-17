import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 기본 설정
st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계",
    page_icon="🎬",
    layout="wide"
)

# 타이틀 및 개요
st.title("🎬 영화 데이터 그래프 도감 2 - 분포와 관계")
st.markdown("1년간 박스오피스 10위권에 진입한 216편의 개봉 영화 데이터를 바탕으로 장르, 국가, 스크린 수 등의 분포와 상관관계를 시각화합니다.")
st.markdown("---")

# 데이터 로드 함수 (캐싱 적용)
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"
    df = pd.read_csv(url)
    
    # 장르 정제: 세로막대 기호(|)로 분리된 장르 중 첫 번째 장르만 추출
    df['장르'] = df['genre'].astype(str).apply(lambda x: x.split('|')[0].strip())
    
    # 수치형 데이터 타입 변환
    numeric_cols = ['first_scrn', 'first_show', 'first_week_audi', 'total_audi', 'days_in_top10']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            
    return df

try:
    df = load_data()

    # -------------------------------------------------------------------
    # Section 1. 장르별 영화 편수 분포 (도넛 그래프)
    # -------------------------------------------------------------------
    st.header("📌 Section 1. 장르별 영화 편수 분포")
    
    # 장르별 영화 편수 집계
    genre_counts = df['장르'].value_counts().reset_index()
    genre_counts.columns = ['장르', '영화편수']
    
    # Plotly 도넛 그래프 생성
    fig1 = px.pie(
        genre_counts,
        names='장르',
        values='영화편수',
        title="<b>장르별 영화 편수 비율 (도넛 차트)</b>",
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    
    # 툴팁 설정: 마우스 호버 시 편수와 비율 표기
    fig1.update_traces(
        textposition='inside',
        textinfo='percent+label',
        hovertemplate="<b>장르:</b> %{label}<br><b>영화 편수:</b> %{value}편<br><b>비율:</b> %{percent}<extra></extra>"
    )
    
    fig1.update_layout(
        template="plotly_white",
        height=550,
        legend=dict(title="장르 목록", orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.05)
    )
    
    # 그래프 출력
    st.plotly_chart(fig1, use_container_width=True)
    
    # '이 그래프로 알 수 있는 것' 안내 상자
    st.info("💡 **이 그래프로 알 수 있는 것:** 도넛 그래프 유형을 통해 장르별 영화 편수 비중과 시장 점유 비율을 한눈에 파악할 수 있다.")

    st.markdown("---")

    # -------------------------------------------------------------------
    # Section 2. 장르 및 영화별 총 관객 수 트리맵 (Treemap)
    # -------------------------------------------------------------------
    st.header("📌 Section 2. 장르 및 영화별 총 관객 수 트리맵")
    
    # 계층구조 설정: 장르 > 영화명 (칸 크기: 총 관객 수)
    fig2 = px.treemap(
        df,
        path=[px.Constant("전체 장르"), '장르', 'movieNm'],
        values='total_audi',
        title="<b>장르 및 영화별 총 관객 수 분포 (트리맵)</b>",
        color='장르',
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    
    # 툴팁 설정: 영화명 및 총 관객 수 표기
    fig2.update_traces(
        hovertemplate="<b>%{label}</b><br>총 관객 수: %{value:,}명<extra></extra>"
    )
    
    fig2.update_layout(
        template="plotly_white",
        height=650
    )
    
    # 그래프 출력
    st.plotly_chart(fig2, use_container_width=True)
    
    # '이 그래프로 알 수 있는 것' 안내 상자
    st.info("💡 **이 그래프로 알 수 있는 것:** ")

    st.markdown("---")

    # -------------------------------------------------------------------
    # Section 3. (추가 예정) 다음 분석 그래프 구역
    # -------------------------------------------------------------------
    st.header("📌 Section 3. (추가 예정) 추가 시각화")
    st.text("다음 분석 그래프가 들어올 구역입니다.")
    st.info("💡 **이 그래프로 알 수 있는 것:** ")

except Exception as e:
    st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
