import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_data():
    data = pd.read_excel("Cleaned_KPIs_Data.xlsx")
    data["Most_Used_Region"] = data["Most_Used_Region"].astype(str).str.strip()
    return data

data = load_data()


st.set_page_config(page_title="Customer Dashboard", layout="wide")

st.markdown("""
    <style>
        body {
            background-color: #001F3F;
            color: #FFA500;
        }
        .stMetricLabel, .stMetricValue, h1, h2, h3, p {
            color: #FFA500 !important;
        }
        div[data-baseweb="select"] > div {
            background-color: #003366 !important;
            color: #FFA500 !important;
        }
        div[data-baseweb="select"] svg {
            fill: #FFA500 !important;
        }
        label, span {
            color: #FFA500 !important;
        }
    </style>
""", unsafe_allow_html=True)

page = st.sidebar.radio("Navigation", ["Overview", "Segmentation", "Insights"])

# ==============================
#  PAGE 1 — Overview
# ==============================
if page == "Overview":
    st.title("📊 Customer Revenue & Usage Overview")

    regions = ["All Regions"] + sorted(data["Most_Used_Region"].dropna().unique().tolist())
    selected_region = st.selectbox("🌍 Select Region", regions, key="region_overview")

    plans = ["All Plans"] + sorted(data["Rate_Plan_Desc"].dropna().unique().tolist())
    selected_plan = st.selectbox("📦 Select Rate Plan", plans, key="plan_overview")

    filtered_data = data.copy()

    if selected_region != "All Regions":
        filtered_data = filtered_data[filtered_data["Most_Used_Region"] == selected_region]
    if selected_plan != "All Plans":
        filtered_data = filtered_data[filtered_data["Rate_Plan_Desc"] == selected_plan]

    total_revenue = filtered_data["rev"].sum()
    avg_data = filtered_data["total_data_usage"].mean()
    avg_og = filtered_data["total_og_usage"].mean()
    avg_aon = filtered_data["aon"].mean()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Revenue", f"{total_revenue:,.0f}")
    col2.metric("Avg Data Usage", f"{avg_data:,.2f}")
    col3.metric("Avg Call Usage", f"{avg_og:,.2f}")
    col4.metric("Avg AON", f"{avg_aon:,.2f}")

    st.subheader("Average Revenue by Region")
    rev_region = filtered_data.groupby("Most_Used_Region")["rev"].mean().reset_index()
    fig1 = px.bar(rev_region, x="Most_Used_Region", y="rev", color="Most_Used_Region",
                  color_discrete_sequence=["#FFA500"])
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("Rate Plan Distribution")
    plan_dist = filtered_data["Rate_Plan_Desc"].value_counts().reset_index()
    plan_dist.columns = ["Rate_Plan_Desc", "Count"]
    fig2 = px.pie(plan_dist, values="Count", names="Rate_Plan_Desc",
                  color_discrete_sequence=["#FFA500"])
    st.plotly_chart(fig2, use_container_width=True)

# ==============================
#  PAGE 2 — Segmentation
# ==============================
elif page == "Segmentation":
    st.title("📈 Customer Segmentation Insights")

    regions = ["All Regions"] + sorted(data["Most_Used_Region"].dropna().unique().tolist())
    selected_region = st.selectbox("🌍 Select Region", regions, key="region_seg")

    plans = ["All Plans"] + sorted(data["Rate_Plan_Desc"].dropna().unique().tolist())
    selected_plan = st.selectbox("📦 Select Rate Plan", plans, key="plan_seg")

    filtered_data = data.copy()

    if selected_region != "All Regions":
        filtered_data = filtered_data[filtered_data["Most_Used_Region"] == selected_region]
    if selected_plan != "All Plans":
        filtered_data = filtered_data[filtered_data["Rate_Plan_Desc"] == selected_plan]

    col1, col2, col3 = st.columns(3)

    rev_seg = filtered_data.groupby("Revenue_Segment")["rev"].mean().reset_index()
    fig3 = px.bar(rev_seg, x="Revenue_Segment", y="rev", color="Revenue_Segment",
                  color_discrete_sequence=["#FFA500"])
    col1.plotly_chart(fig3, use_container_width=True)

    data_seg = filtered_data.groupby("Data_Segment")["total_data_usage"].mean().reset_index()
    fig4 = px.bar(data_seg, x="Data_Segment", y="total_data_usage", color="Data_Segment",
                  color_discrete_sequence=["#FFA500"])
    col2.plotly_chart(fig4, use_container_width=True)

    call_seg = filtered_data.groupby("Call_Segment")["total_og_usage"].mean().reset_index()
    fig5 = px.bar(call_seg, x="Call_Segment", y="total_og_usage", color="Call_Segment",
                  color_discrete_sequence=["#FFA500"])
    col3.plotly_chart(fig5, use_container_width=True)

    st.subheader("AON vs Revenue")
    fig6 = px.scatter(filtered_data, x="aon", y="rev", color="Revenue_Segment",
                      color_discrete_sequence=["#FFA500"])
    st.plotly_chart(fig6, use_container_width=True)

# ==============================
#  PAGE 3 — Insights
# ==============================
elif page == "Insights":
    st.title("💡 Business Insights & Recommendations")

    insights = [
        "Bundle 2000 increased data usage but slightly reduced revenue.",
        "Medium Revenue customers show strong potential for upselling.",
        "High Revenue customers are loyal — reward them with retention incentives.",
        "Low usage customers should receive promotional offers to increase engagement.",
        "Monitor new customers (low AON) for early churn detection."
    ]

    for insight in insights:
        st.markdown(f"✅ **{insight}**")
