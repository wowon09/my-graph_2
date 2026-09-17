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
    st.info("💡 **이 그래프로 알 수 있는 것:** 트리맵 유형을 통해 장르별 전체 관객 규모와 개별 영화가 장르 내에서 차지하는 비중을 면적으로 비교할 수 있다.")

    st.markdown("---")

    # -------------------------------------------------------------------
    # Section 3. 총 관객 수 히스토그램 (Histogram)
    # -------------------------------------------------------------------
    st.header("📌 Section 3. 영화별 총 관객 수 분포")
    
    # Plotly 히스토그램 생성
    fig3 = px.histogram(
        df,
        x='total_audi',
        nbins=30,
        title="<b>영화별 총 관객 수 분포 (히스토그램)</b>",
        labels={'total_audi': '총 관객 수 (명)'},
        color_discrete_sequence=['#E50914']
    )
    
    fig3.update_traces(
        hovertemplate="<b>관객 수 구간:</b> %{x}<br><b>영화 수:</b> %{y}편<extra></extra>"
    )
    
    fig3.update_layout(
        xaxis_title="총 관객 수 (명)",
        yaxis_title="영화 수 (편)",
        template="plotly_white",
        height=500
    )
    
    # 그래프 출력
    st.plotly_chart(fig3, use_container_width=True)
    
    # 최다 관객 보유 영화 데이터 추출
    max_movie_row = df.loc[df['total_audi'].idxmax()]
    max_movie_name = max_movie_row['movieNm']
    max_audi_val = max_movie_row['total_audi']
    
    # 동적 분석 결과 안내 문구
    st.info(
        f"💡 **이 그래프로 알 수 있는 것:** 대부분의 영화는 총 관객 수 **100만 명 이하 구간**에 밀집해 있는 반면, "
        f"가장 관객 수가 많은 영화는 **{max_movie_name}**({max_audi_val:,.0f}명)이다."
    )

    st.markdown("---")

    # -------------------------------------------------------------------
    # Section 4. 개봉일 스크린수 vs 총 관객수 (산점도 그래프)
    # -------------------------------------------------------------------
    st.header("📌 Section 4. 개봉일 스크린 수와 총 관객 수의 관계")
    
    # Plotly 산점도(Scatter Plot) 생성
    fig4 = px.scatter(
        df,
        x='first_scrn',
        y='total_audi',
        color='장르',
        hover_name='movieNm',
        title="<b>개봉일 스크린 수 vs 총 관객 수 (산점도)</b>",
        labels={'first_scrn': '개봉일 스크린 수 (개)', 'total_audi': '총 관객 수 (명)', '장르': '장르'},
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    
    # 마우스 호버 설정
    fig4.update_traces(
        hovertemplate="<b>영화명: %{hovertext}</b><br>장르: %{fullData.name}<br>개봉일 스크린 수: %{x:,}개<br>총 관객 수: %{y:,}명<extra></extra>",
        marker=dict(size=9, opacity=0.8)
    )
    
    fig4.update_layout(
        xaxis_title="개봉일 스크린 수 (개)",
        yaxis_title="총 관객 수 (명)",
        template="plotly_white",
        height=600,
        legend=dict(title="장르 목록")
    )
    
    # 그래프 출력
    st.plotly_chart(fig4, use_container_width=True)
    
    # '이 그래프로 알 수 있는 것' 안내 상자
    st.info("💡 **이 그래프로 알 수 있는 것:** 초기 스크린 확보량이 최종 관객 수에 미치는 전반적인 비례 관계를 확인하고, 적은 스크린 수로도 대흥행을 기록한 이변작(아웃라이어)을 한눈에 식별할 수 있다.")

    st.markdown("---")

    # -------------------------------------------------------------------
    # Section 5. 10편 이상 장르별 총 관객 수 박스플롯 (Box Plot)
    # -------------------------------------------------------------------
    st.header("📌 Section 5. 주요 장르별 총 관객 수 분포")
    
    # 영화가 10편 이상인 장르 필터링
    genre_counts = df['장르'].value_counts()
    target_genres = genre_counts[genre_counts >= 10].index
    df_box = df[df['장르'].isin(target_genres)]
    
    # Plotly 박스플롯 생성
    fig5 = px.box(
        df_box,
        x='장르',
        y='total_audi',
        color='장르',
        hover_name='movieNm',
        points='outliers',
        title="<b>영화 10편 이상 장르별 총 관객 수 분포 (박스플롯)</b>",
        labels={'total_audi': '총 관객 수 (명)', '장르': '장르'},
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    
    # 이상치 점 호버 설정
    fig5.update_traces(
        hovertemplate="<b>영화명: %{hovertext}</b><br>총 관객 수: %{y:,}명<extra></extra>"
    )
    
    fig5.update_layout(
        xaxis_title="장르 (10편 이상 보유)",
        yaxis_title="총 관객 수 (명)",
        template="plotly_white",
        height=600,
        showlegend=False
    )
    
    # 그래프 출력
    st.plotly_chart(fig5, use_container_width=True)
    
    # '이 그래프로 알 수 있는 것' 안내 상자
    st.info("💡 **이 그래프로 알 수 있는 것:** 주요 장르별 관객 수의 중간값과 범위를 비교하고, 각 장르 내에서 일반적 수치를 크게 상회하는 초대형 흥행작(이상치 점)을 한눈에 식별할 수 있다.")

    st.markdown("---")

    # -------------------------------------------------------------------
    # Section 6. 개봉일 스크린수, 첫 주 관객수, 총 관객수 (버블 차트)
    # -------------------------------------------------------------------
    st.header("📌 Section 6. 개봉일 스크린 수, 첫 주 관객 수, 총 관객 수의 관계")
    
    # Plotly 버블 차트 생성 (크기: first_week_audi)
    fig6 = px.scatter(
        df,
        x='first_scrn',
        y='total_audi',
        size='first_week_audi',
        color='장르',
        hover_name='movieNm',
        size_max=40,
        title="<b>개봉일 스크린 수 vs 총 관객 수 및 첫 주 관객 수 (버블 차트)</b>",
        labels={
            'first_scrn': '개봉일 스크린 수 (개)',
            'total_audi': '총 관객 수 (명)',
            'first_week_audi': '첫 주 관객 수 (명)',
            '장르': '장르'
        },
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    
    # 마우스 호버 설정
    fig6.update_traces(
        hovertemplate="<b>영화명: %{hovertext}</b><br>장르: %{fullData.name}<br>개봉일 스크린 수: %{x:,}개<br>총 관객 수: %{y:,}명<br>첫 주 관객 수: %{marker.size:,}명<extra></extra>"
    )
    
    fig6.update_layout(
        xaxis_title="개봉일 스크린 수 (개)",
        yaxis_title="총 관객 수 (명)",
        template="plotly_white",
        height=600,
        legend=dict(title="장르 목록")
    )
    
    # 그래프 출력
    st.plotly_chart(fig6, use_container_width=True)
    
    # '이 그래프로 알 수 있는 것' 안내 상자
    st.info("💡 **이 그래프로 알 수 있는 것:** 개봉일 스크린 수와 최종 관객 수 관계뿐만 아니라, 버블의 크기를 통해 초기 첫 주 흥행 파급력이 최종 관객 수로 이어지는지 여부를 다차원적으로 비교분석할 수 있다.")

    st.markdown("---")

    # -------------------------------------------------------------------
    # Section 7. 제작 국가 및 장르별 영화 편수 (선버스트 차트)
    # -------------------------------------------------------------------
    st.header("📌 Section 7. 제작 국가 및 장르별 영화 편수 분포")
    
    # Plotly 선버스트(Sunburst) 차트 생성
    fig7 = px.sunburst(
        df,
        path=[px.Constant("전체 국가"), 'nation', '장르'],
        title="<b>제작 국가 및 장르별 영화 편수 분포 (선버스트 차트)</b>",
        color='nation',
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    
    # 툴팁 설정
    fig7.update_traces(
        hovertemplate="<b>%{label}</b><br>영화 편수: %{value}편<extra></extra>"
    )
    
    fig7.update_layout(
        template="plotly_white",
        height=650
    )
    
    # 그래프 출력
    st.plotly_chart(fig7, use_container_width=True)
    
    # '이 그래프로 알 수 있는 것' 안내 상자
    st.info("💡 **이 그래프로 알 수 있는 것:** 선버스트 차트 유형을 통해 제작 국가별 영화 편수 비율과 각 국가 내에서 점유하는 주요 장르의 비중을 계층적 동심원 구조로 파악할 수 있다.")

    st.markdown("---")

    # -------------------------------------------------------------------
    # Section 8. 10위권 체류 날수 vs 총 관객 수 (산점도 그래프)
    # -------------------------------------------------------------------
    st.header("📌 Section 8. 10위권에 머문 날수는 대개 며칠쯤인가")
    
    # Plotly 산점도 생성
    fig8 = px.scatter(
        df,
        x='days_in_top10',
        y='total_audi',
        color='장르',
        hover_name='movieNm',
        title="<b>10위권에 머문 날수는 대개 며칠쯤인가</b>",
        labels={
            'days_in_top10': '10위권에 머문 날수 (일)',
            'total_audi': '총 관객 수 (명)',
            '장르': '장르'
        },
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    
    # 마우스 호버 설정
    fig8.update_traces(
        hovertemplate="<b>영화명: %{hovertext}</b><br>장르: %{fullData.name}<br>10위권 머문 날수: %{x}일<br>총 관객 수: %{y:,}명<extra></extra>",
        marker=dict(size=9, opacity=0.8)
    )
    
    fig8.update_layout(
        xaxis_title="10위권에 머문 날수 (일)",
        yaxis_title="총 관객 수 (명)",
        template="plotly_white",
        height=600,
        legend=dict(title="장르 목록")
    )
    
    # 그래프 출력
    st.plotly_chart(fig8, use_container_width=True)
    
    # '이 그래프로 알 수 있는 것' 안내 상자
    st.info("💡 **이 그래프로 알 수 있는 것:** 영화가 박스오피스 10위권 내에 머문 기간(일수)과 최종 총 관객 수 간의 밀접한 비례 관계를 확인하고, 장기 흥행(롱런) 작들의 데이터 분포를 직관적으로 파악할 수 있다.")

    st.markdown("---")

    # -------------------------------------------------------------------
    # Section 9. (추가 예정) 다음 분석 그래프 구역
    # -------------------------------------------------------------------
    st.header("📌 Section 9. (추가 예정) 추가 시각화")
    st.text("다음 분석 그래프가 들어올 구역입니다.")
    st.info("💡 **이 그래프로 알 수 있는 것:** ")

except Exception as e:
    st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
    
