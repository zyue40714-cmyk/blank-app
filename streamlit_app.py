import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# -----------------------------------------------------------
# 1. 페이지 설정
# -----------------------------------------------------------
st.set_page_config(
    page_title="전자상거래 판매 데이터 분석 대시보드",
    page_icon="🛒",
    layout="wide"
)

# -----------------------------------------------------------
# 2. 제목
# -----------------------------------------------------------
st.title("🛒 전자상거래 판매 데이터 분석 대시보드")
st.markdown("""
이 대시보드는 **전자상거래 플랫폼의 판매 성과, 지역별 매출, 카테고리 트렌드 및 주요 KPI**를  
한눈에 파악할 수 있도록 제작되었습니다.
""")

st.divider()

# -----------------------------------------------------------
# 3. 전자상거래 더미 데이터 생성
# -----------------------------------------------------------
np.random.seed(42)
n = 6000

data = pd.DataFrame({
    "연도": np.random.choice([2022, 2023, 2024], n),
    "월": np.random.randint(1, 13, n),
    "카테고리": np.random.choice(["패션", "뷰티", "디지털", "가전", "식품", "스포츠"], n),
    "지역": np.random.choice(["베이징","상하이","광저우","선전","청두","항저우","우한"], n),
    "주문금액": np.random.gamma(4, 120, n).round(0),
    "수량": np.random.randint(1, 5, n)
})

data["GMV"] = data["주문금액"] * data["수량"]

# -----------------------------------------------------------
# 4. 사이드바 필터
# -----------------------------------------------------------
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/891/891462.png", width=80)
    st.title("⚙️ 필터 설정")

    year = st.multiselect("연도 선택", sorted(data["연도"].unique()), default=data["연도"].unique())
    cate = st.multiselect("카테고리 선택", sorted(data["카테고리"].unique()), default=data["카테고리"].unique())
    region = st.multiselect("지역 선택", sorted(data["지역"].unique()), default=data["지역"].unique())

    show_raw = st.checkbox("📄 원본 데이터 보기", value=False)

# -----------------------------------------------------------
# 5. 데이터 필터링
# -----------------------------------------------------------
filtered = data[
    data["연도"].isin(year) &
    data["카테고리"].isin(cate) &
    data["지역"].isin(region)
]

# -----------------------------------------------------------
# 6. KPI 카드
# -----------------------------------------------------------
total_gmv = int(filtered["GMV"].sum())
total_orders = len(filtered)
avg_order = int(filtered["GMV"].mean())

col1, col2, col3 = st.columns(3)
col1.metric("💰 총 GMV", f"{total_gmv:,.0f} 원")
col2.metric("🧾 총 주문수", f"{total_orders:,} 건")
col3.metric("💳 평균 객단가", f"{avg_order:,.0f} 원")

st.divider()

# -----------------------------------------------------------
# 7. 시각화 영역
# -----------------------------------------------------------

# (1) 월별 GMV 추세
st.subheader("📈 월별 GMV 추세")
monthly_gmv = filtered.groupby(["연도", "월"])["GMV"].sum().reset_index()

fig1 = px.line(
    monthly_gmv,
    x="월", y="GMV", color="연도",
    markers=True,
    color_discrete_sequence=px.colors.qualitative.Bold
)
fig1.update_layout(height=350)
st.plotly_chart(fig1, use_container_width=True)

# (2) 카테고리별 GMV 비교
st.subheader("🏷️ 카테고리별 GMV")
cate_gmv = filtered.groupby("카테고리")["GMV"].sum().reset_index()

fig2 = px.bar(
    cate_gmv, x="카테고리", y="GMV",
    text_auto=".2s",
    color="카테고리",
    color_discrete_sequence=px.colors.qualitative.Vivid
)
fig2.update_layout(showlegend=False, height=380)
st.plotly_chart(fig2, use_container_width=True)

# (3) 지역별 판매 비중 (Treemap)
st.subheader("🗺️ 지역 판매 비중")
region_gmv = filtered.groupby("지역")["GMV"].sum().reset_index()

fig3 = px.treemap(
    region_gmv,
    path=["지역"],
    values="GMV",
    color="GMV",
    color_continuous_scale="Mint"
)
st.plotly_chart(fig3, use_container_width=True)

# -----------------------------------------------------------
# 8. 원본 데이터 표시
# -----------------------------------------------------------
if show_raw:
    st.divider()
    st.subheader("📄 필터링된 원본 데이터")
    st.dataframe(filtered, use_container_width=True)
