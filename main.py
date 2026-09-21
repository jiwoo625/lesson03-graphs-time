```python
# 그래프 2

st.divider()

st.header("그래프 2. 일관객 합계 TOP 5 영화")

# 영화별 전체 기간 일관객 합계 계산
movie_total = (
    df.groupby("영화명")["일관객"]
    .sum()
    .sort_values(ascending=False)
)

# 일관객 합계가 가장 큰 5편 선택
top5_movies = movie_total.head(5).index.tolist()

# TOP 5 영화의 데이터만 가져오기
top5_df = df[
    df["영화명"].isin(top5_movies)
].copy()

# 날짜순 정렬
top5_df = top5_df.sort_values(
    ["날짜", "영화명"]
)

# 5편을 색으로 구분한 선 그래프
fig2 = px.line(
    top5_df,
    x="날짜",
    y="일관객",
    color="영화명",
    title="일관객 합계가 가장 큰 5편의 날짜별 일관객",
    labels={
        "날짜": "날짜",
        "일관객": "일관객 수",
        "영화명": "영화"
    }
)

# 마우스를 올렸을 때 표시
fig2.update_traces(
    hovertemplate=(
        "영화: %{fullData.name}"
        "<br>날짜: %{x|%Y-%m-%d}"
        "<br>일관객: %{y:,}명"
        "<extra></extra>"
    )
)

# 범례 설정
fig2.update_layout(
    hovermode="closest",
    xaxis_title="날짜",
    yaxis_title="일관객 수",
    legend_title="영화"
)

# 그래프 출력
st.plotly_chart(
    fig2,
    use_container_width=True
)

st.markdown(
    "**이 그래프로 알 수 있는 것:** "
    "전체 기간의 일관객 합계가 가장 큰 5편의 날짜별 관객 변화를 비교할 수 있습니다. "
    "범례에서 영화 이름을 클릭하면 해당 영화의 선을 켜거나 끌 수 있습니다."
)
```
