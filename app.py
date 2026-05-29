import pandas as pd
import streamlit as st
import plotly.express as px

# Page Settings
st.set_page_config(page_title="Sales Dashboard", layout="wide")

# Dashboard Title
st.title("📊 Sales & Revenue Dashboard")

# Read CSV File
df = pd.read_csv("sales_data.csv")

# Convert Date Column
df["Order Date"] = pd.to_datetime(df["Order Date"])

# ---------------- SIDEBAR FILTERS ----------------

st.sidebar.header("Filters")

region = st.sidebar.multiselect(
    "Select Region",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

category = st.sidebar.multiselect(
    "Select Category",
    options=df["Category"].unique(),
    default=df["Category"].unique()
)

# Filter Data
filtered_df = df[
    (df["Region"].isin(region)) &
    (df["Category"].isin(category))
]

# ---------------- KPI SECTION ----------------

total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
total_orders = len(filtered_df)

col1, col2, col3 = st.columns(3)

col1.metric("Total Sales", f"₹{total_sales:,}")
col2.metric("Total Profit", f"₹{total_profit:,}")
col3.metric("Total Orders", total_orders)

st.markdown("---")

# ---------------- SALES TREND CHART ----------------

sales_trend = filtered_df.groupby(
    filtered_df["Order Date"].dt.strftime("%Y-%m")
)["Sales"].sum().reset_index()

fig_line = px.line(
    sales_trend,
    x="Order Date",
    y="Sales",
    title="Monthly Sales Trend",
    markers=True
)

st.plotly_chart(fig_line, use_container_width=True)

# ---------------- TOP PRODUCTS CHART ----------------

top_products = filtered_df.groupby("Product")["Sales"].sum().reset_index()

fig_bar = px.bar(
    top_products,
    x="Product",
    y="Sales",
    color="Product",
    title="Top Performing Products"
)

st.plotly_chart(fig_bar, use_container_width=True)

# ---------------- PIE CHART ----------------

category_sales = filtered_df.groupby("Category")["Sales"].sum().reset_index()

fig_pie = px.pie(
    category_sales,
    names="Category",
    values="Sales",
    title="Sales by Category"
)

st.plotly_chart(fig_pie, use_container_width=True)

# ---------------- DATA TABLE ----------------

st.subheader("Sales Data Table")

st.dataframe(filtered_df)