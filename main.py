# --------------------------------------------------
# 그래프 2. 일관객 합계 TOP 5 영화의 날짜별 변화
# --------------------------------------------------

st.divider()

st.header("그래프 2. 일관객 합계 TOP 5 영화의 날짜별 변화")

# 영화별 기간 내 일관객 합계 계산
top5_movies = (
    df.groupby("영화명", as_index=False)["일관객"]
    .sum()
    .sort_values("일관객", ascending=False)
    .head(5)["영화명"]
    .tolist()
)

# TOP 5 영화만 추출
top5_df = (
    df[df["영화명"].isin(top5_movies)]
    .sort_values(["영화명", "날짜"])
)

# 여러 영화를 한 그래프에 표시
fig_top5 = px.line(
    top5_df,
    x="날짜",
    y="일관객",
    color="영화명",
    markers=True,
    labels={
        "날짜": "날짜",
        "일관객": "일관객 수",
        "영화명": "영화",
    },
    title="일관객 합계가 가장 큰 5편의 날짜별 일관객 변화",
)

# 마우스를 올렸을 때 날짜·영화명·관객수 표시
fig_top5.update_traces(
    hovertemplate=(
        "영화: %{fullData.name}"
        "<br>날짜: %{x|%Y-%m-%d}"
        "<br>일관객: %{y:,}명"
        "<extra></extra>"
    )
)

fig_top5.update_layout(
    hovermode="closest",
    xaxis_title="날짜",
    yaxis_title="일관객 수",
    legend_title="영화",
)

# 범례 클릭으로 개별 영화 표시/숨기기 가능
st.plotly_chart(
    fig_top5,
    use_container_width=True,
)

st.markdown(
    "**이 그래프로 알 수 있는 것:** "
    "기간 동안 일관객 합계가 가장 큰 5편의 관객 규모와 날짜별 변화를 서로 비교할 수 있습니다."
)
