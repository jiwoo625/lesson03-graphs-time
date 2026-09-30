
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

movie_list = sorted(
    df["영화명"].dropna().unique()
)

movie = st.selectbox(
    "영화를 고르세요",
    movie_list,
)

one_movie = (
    df[df["영화명"] == movie]
    .sort_values("날짜")
)

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

movie_total = (
    df.groupby("영화명")["일관객"]
    .sum()
    .sort_values(ascending=False)
)

top5_movies = movie_total.head(5).index.tolist()

top5 = (
    df[df["영화명"].isin(top5_movies)]
    .sort_values(["날짜", "영화명"])
)

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

fig2.update_traces(
    hovertemplate=(
        "영화 %{fullData.name}"
        "<br>날짜 %{x|%Y-%m-%d}"
        "<br>관객 %{y:,}명"
        "<extra></extra>"
    )
)

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
# 그래프 3. 날짜별 10위권 일관객 합계
# ─────────────────────────────────────────────
st.header("3. 날짜별 10위권 일관객 합계")

# 날짜별로 그날 10위권 영화의 일관객을 모두 더합니다.
daily_total = (
    df.groupby("날짜", as_index=False)["일관객"]
    .sum()
    .sort_values("날짜")
)

# 일관객 합계가 가장 큰 날 3일을 찾습니다.
top3_days = (
    daily_total
    .nlargest(3, "일관객")
    .sort_values("날짜")
)

# 영역 그래프를 만듭니다.
fig3 = px.area(
    daily_total,
    x="날짜",
    y="일관객",
    labels={
        "날짜": "날짜",
        "일관객": "10위권 일관객 합계",
    },
)

# 마우스를 올렸을 때 날짜와 합계 관객 수를 보여줍니다.
fig3.update_traces(
    hovertemplate=(
        "날짜 %{x|%Y-%m-%d}"
        "<br>10위권 합계 %{y:,}명"
        "<extra></extra>"
    )
)

# 합계가 가장 큰 3일을 그래프 위에 표시합니다.
for _, row in top3_days.iterrows():
    fig3.add_annotation(
        x=row["날짜"],
        y=row["일관객"],
        text=row["날짜"].strftime("%Y-%m-%d"),
        showarrow=True,
        arrowhead=2,
        yshift=10,
    )

st.plotly_chart(
    fig3,
    width="stretch",
)

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

