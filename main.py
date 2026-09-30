
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
    df = pd.read_csv(DATA_URL)

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

daily_total = (
    df.groupby("날짜", as_index=False)["일관객"]
    .sum()
    .sort_values("날짜")
)

top3_days = (
    daily_total
    .nlargest(3, "일관객")
    .sort_values("날짜")
)

fig3 = px.area(
    daily_total,
    x="날짜",
    y="일관객",
    labels={
        "날짜": "날짜",
        "일관객": "10위권 일관객 합계",
    },
)

fig3.update_traces(
    hovertemplate=(
        "날짜 %{x|%Y-%m-%d}"
        "<br>10위권 합계 %{y:,}명"
        "<extra></extra>"
    )
)

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
# 그래프 4. 영화별 일관객 합계 TOP 10
# ─────────────────────────────────────────────
st.header("4. 영화별 일관객 합계 TOP 10")

movie_summary = (
    df.groupby("영화명")
    .agg(
        일관객합계=("일관객", "sum"),
        일수=("날짜", "nunique"),
    )
    .sort_values(
        "일관객합계",
        ascending=False,
    )
    .head(10)
    .reset_index()
)

movie_summary = movie_summary.sort_values(
    "일관객합계",
    ascending=True,
)

fig4 = px.bar(
    movie_summary,
    x="일관객합계",
    y="영화명",
    orientation="h",
    labels={
        "일관객합계": "일관객 합계",
        "영화명": "영화명",
    },
)

fig4.update_traces(
    customdata=movie_summary["일수"],
    hovertemplate=(
        "영화 %{y}"
        "<br>일관객 합계 %{x:,}명"
        "<br>10위권에 든 날수 %{customdata}일"
        "<extra></extra>"
    )
)

st.plotly_chart(
    fig4,
    width="stretch",
)

st.caption(
    "이 그래프로 알 수 있는 것: __________________________________"
)


# ─────────────────────────────────────────────
# 그래프 5. 월 × 요일별 일관객 합계 히트맵
# ─────────────────────────────────────────────
st.header("5. 월 × 요일별 일관객 합계")

# 날짜에서 월과 요일 추출
heatmap_df = df.copy()

heatmap_df["월"] = heatmap_df["날짜"].dt.month

weekday_order = [
    "월요일",
    "화요일",
    "수요일",
    "목요일",
    "금요일",
    "토요일",
    "일요일",
]

heatmap_df["요일"] = (
    heatmap_df["날짜"]
    .dt.dayofweek
    .map(dict(enumerate(weekday_order)))
)

# 월 × 요일별 일관객 합계
monthly_weekday = (
    heatmap_df
    .groupby(["월", "요일"], as_index=False)["일관객"]
    .sum()
)

# 히트맵용 표 형태로 변환
heatmap_pivot = (
    monthly_weekday
    .pivot(
        index="월",
        columns="요일",
        values="일관객",
    )
    .reindex(columns=weekday_order)
)

fig5 = px.imshow(
    heatmap_pivot,
    labels={
        "x": "요일",
        "y": "월",
        "color": "일관객 합계",
    },
    x=weekday_order,
    y=heatmap_pivot.index,
    text_auto=True,
    aspect="auto",
    color_continuous_scale="Blues",
)

fig5.update_traces(
    hovertemplate=(
        "%{y}월 %{x}"
        "<br>일관객 합계 %{z:,}명"
        "<extra></extra>"
    )
)

st.plotly_chart(
    fig5,
    width="stretch",
)

st.caption(
    "이 그래프로 알 수 있는 것: __________________________________"
)

