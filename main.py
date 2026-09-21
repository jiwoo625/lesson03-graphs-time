import streamlit as st
import pandas as pd
import plotly.express as px


# --------------------------------------------------
# 기본 설정
# --------------------------------------------------

st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간",
    page_icon="🎬",
    layout="wide",
)

st.title("🎬 영화 데이터 그래프 도감 1 - 시간")


# --------------------------------------------------
# 데이터 불러오기
# --------------------------------------------------

DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)

    # 날짜 열: YYYYMMDD → 실제 날짜형
    df["날짜"] = pd.to_datetime(
        df["날짜"].astype(str),
        format="%Y%m%d"
    )

    return df


df = load_data()


# --------------------------------------------------
# 그래프 1. 영화별 날짜별 일관객 변화
# --------------------------------------------------

st.header("그래프 1. 영화별 일관객 변화")

movie_list = sorted(df["영화명"].dropna().unique())

selected_movie = st.selectbox(
    "영화를 선택하세요.",
    movie_list,
)

movie_df = (
    df[df["영화명"] == selected_movie]
    .sort_values("날짜")
)


fig = px.line(
    movie_df,
    x="날짜",
    y="일관객",
    markers=True,
    labels={
        "날짜": "날짜",
        "일관객": "일관객 수",
    },
    title=f"「{selected_movie}」 날짜별 일관객 변화",
)

fig.update_traces(
    hovertemplate=(
        "날짜: %{x|%Y-%m-%d}"
        "<br>일관객: %{y:,}명"
        "<extra></extra>"
    )
)

fig.update_layout(
    hovermode="x unified",
    xaxis_title="날짜",
    yaxis_title="일관객 수",
)

st.plotly_chart(
    fig,
    use_container_width=True,
)

st.markdown(
    "**이 그래프로 알 수 있는 것:** "
    "선택한 영화의 날짜에 따른 일관객 수 변화를 살펴볼 수 있습니다."
)


# --------------------------------------------------
# 그래프 2. 앞으로 추가할 그래프 영역
# --------------------------------------------------

st.divider()

st.header("그래프 2. 추가 예정")

st.markdown(
    "**이 그래프로 알 수 있는 것:** "
    "앞으로 새로운 시간 관련 영화 데이터 그래프를 추가할 수 있는 영역입니다."
)


# --------------------------------------------------
# 그래프 3. 앞으로 추가할 그래프 영역
# --------------------------------------------------

st.divider()

st.header("그래프 3. 추가 예정")

st.markdown(
    "**이 그래프로 알 수 있는 것:** "
    "앞으로 새로운 분석 그래프를 추가할 수 있는 영역입니다."
)
