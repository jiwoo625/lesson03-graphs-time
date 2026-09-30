
import streamlit as st
import pandas as pd
import plotly.express as px


# ─────────────────────────────────────────────
# 페이지 설정
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간",
    layout="wide",
)

st.title("영화 데이터 그래프 도감 1 - 시간")


# ─────────────────────────────────────────────
# 데이터 불러오기
# ─────────────────────────────────────────────
DATA_URL = "https://raw.githubusercontent.com/happykth/data/main/kobis_daily.csv"


@st.cache_data
def load_data():
    # 1년치(365일) 일별 박스오피스 10위권 기록
    df = pd.read_csv(DATA_URL)

    # 날짜 열을 진짜 날짜로 변환
    df["날짜"] = pd.to_datetime(
        df["날짜"],
        format="%Y%m%d"
    )

    return df


df = load_data()


# ─────────────────────────────────────────────
# 그래프 1. 한 영화의 흥행 곡선
# ─────────────────────────────────────────────
st.header("1. 한 영화의 흥행 곡선")

# 드롭다운으로 영화를 고릅니다.
movie_list = sorted(
    df["영화명"].dropna().unique()
)

movie = st.selectbox(
    "영화를 고르세요",
    movie_list,
)

# 선택한 영화의 날짜별 데이터를 가져옵니다.
one_movie = (
    df[df["영화명"] == movie]
    .sort_values("날짜")
)

# 날짜별 일관객 선 그래프
fig1 = px.line(
    one_movie,
    x="날짜",
    y="일관객",
    markers=True,
    labels={
        "날짜": "날짜",
        "일관객": "일관객",
    },
)

# 마우스를 올리면 날짜와 관객 수가 보이게 합니다.
fig1.update_traces(
    hovertemplate=(
        "날짜 %{x|%Y-%m-%d}"
        "<br>관객 %{y:,}명"
        "<extra></extra>"
    )
)

st.plotly_chart(
    fig1,
    width="stretch",
)

st.caption(
    "이 그래프로 알 수 있는 것: __________________________________"
)


# ─────────────────────────────────────────────
# 그래프 2. 일관객 합계 상위 5편
# ─────────────────────────────────────────────
st.header("2. 일관객 합계가 가장 큰 영화 5편")

# 영화별 전체 기간 일관객 합계를 계산합니다.
movie_total = (
    df.groupby("영화명")["일관객"]
    .sum()
    .sort_values(ascending=False)
)

# 일관객 합계가 가장 큰 5편을 선택합니다.
top5_movies = movie_total.head(5).index.tolist()

# 상위 5편의 날짜별 데이터를 가져옵니다.
top5 = (
    df[df["영화명"].isin(top5_movies)]
    .sort_values(["날짜", "영화명"])
)

# 다섯 영화를 색으로 구분한 선 그래프를 만듭니다.
fig2 = px.line(
    top5,
    x="날짜",
    y="일관객",
    color="영화명",
    markers=True,
    labels={
        "날짜": "날짜",
        "일관객": "일관객",
        "영화명": "영화명",
    },
)

# 마우스를 올리면 영화명, 날짜, 관객 수를 보여줍니다.
fig2.update_traces(
    hovertemplate=(
        "영화 %{fullData.name}"
        "<br>날짜 %{x|%Y-%m-%d}"
        "<br>관객 %{y:,}명"
        "<extra></extra>"
    )
)

# 범례를 클릭하면 영화별 선을 켜거나 끌 수 있습니다.
fig2.update_layout(
    legend_title_text="영화명",
)

st.plotly_chart(
    fig2,
    width="stretch",
)

st.caption(
    "이 그래프로 알 수 있는 것: __________________________________"
)


# ─────────────────────────────────────────────
# 그래프 3
# ─────────────────────────────────────────────
st.header("3. 그래프 3")

st.caption("여기에 세 번째 그래프를 추가하세요.")

st.caption(
    "이 그래프로 알 수 있는 것: __________________________________"
)


# ─────────────────────────────────────────────
# 그래프 4
# ─────────────────────────────────────────────
st.header("4. 그래프 4")

st.caption("여기에 네 번째 그래프를 추가하세요.")

st.caption(
    "이 그래프로 알 수 있는 것: __________________________________"
)


# ─────────────────────────────────────────────
# 그래프 5
# ─────────────────────────────────────────────
st.header("5. 그래프 5")

st.caption("여기에 다섯 번째 그래프를 추가하세요.")

st.caption(
    "이 그래프로 알 수 있는 것: __________________________________"
)

