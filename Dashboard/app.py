import streamlit as st
import pandas as pd

st.title("Customer Retention Analysis Dashboard")

df = pd.read_csv("Data/European_Bank.csv")

st.sidebar.header("User Capabilities")

engagement_filter = st.sidebar.selectbox(
"Engagement Status",
["All", "Active", "Inactive"]
)

product_count = st.sidebar.selectbox(
"Product Count",
["All", 1, 2, 3, 4]
)

balance_threshold = st.sidebar.slider(
"Balance Threshold",
0,
int(df["Balance"].max()),
int(df["Balance"].median())
)

salary_threshold = st.sidebar.slider(
"Salary Threshold",
0,
int(df["EstimatedSalary"].max()),
int(df["EstimatedSalary"].median())
)

filtered_df = df.copy()

if engagement_filter == "Active":
filtered_df = filtered_df[filtered_df["IsActiveMember"] == 1]

elif engagement_filter == "Inactive":
filtered_df = filtered_df[filtered_df["IsActiveMember"] == 0]

if product_count != "All":
filtered_df = filtered_df[
filtered_df["NumOfProducts"] == product_count
]

filtered_df = filtered_df[
(filtered_df["Balance"] >= balance_threshold) &
(filtered_df["EstimatedSalary"] >= salary_threshold)
]

st.subheader("Dataset Preview")
st.dataframe(filtered_df.head())

st.subheader("Engagement vs Churn Overview")
st.bar_chart(filtered_df["Exited"].value_counts())

st.subheader("Geographical Churn Analysis")

geo = pd.crosstab(
filtered_df["Geography"],
filtered_df["Exited"],
normalize="index"
) * 100

if 1 in geo.columns:
st.bar_chart(geo[1])

st.subheader("Active vs Inactive Customer Retention")

active = pd.crosstab(
filtered_df["IsActiveMember"],
filtered_df["Exited"],
normalize="index"
) * 100

if 1 in active.columns:
st.bar_chart(active[1])

st.subheader("Gender-wise Churn Analysis")

gender = pd.crosstab(
filtered_df["Gender"],
filtered_df["Exited"],
normalize="index"
) * 100

if 1 in gender.columns:
st.bar_chart(gender[1])

st.subheader("Product Utilization Impact Analysis")

products = pd.crosstab(
filtered_df["NumOfProducts"],
filtered_df["Exited"],
normalize="index"
) * 100

if 1 in products.columns:
st.bar_chart(products[1])

st.write(
"Customers with 2 products show the strongest retention, while churn increases significantly for customers with higher product counts."
)

st.subheader("High-Value Disengaged Customer Detector")

high_value_customers = filtered_df[
(filtered_df["Balance"] > balance_threshold) &
(filtered_df["IsActiveMember"] == 0)
]

st.write(
f"Number of disengaged high-value customers: {len(high_value_customers)}"
)

st.dataframe(
high_value_customers[
[
"CustomerId",
"Balance",
"EstimatedSalary",
"IsActiveMember",
"Exited"
]
].head(10)
)

st.subheader("Retention Strength Scoring Panel")

filtered_df["RelationshipStrength"] = (
filtered_df["IsActiveMember"] +
(filtered_df["NumOfProducts"] >= 2).astype(int)
)

relationship = pd.crosstab(
filtered_df["RelationshipStrength"],
filtered_df["Exited"],
normalize="index"
) * 100

if 1 in relationship.columns:
st.bar_chart(relationship[1])
