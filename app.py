import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt


# Set page configuration
st.set_page_config(page_title="E-commerce Customer Behavior Dashboard", layout="wide")

# Title of the app
st.title("📊 E-commerce Customer Behavior Dashboard")

# Load the dataset
def load_data():
    df = pd.read_csv("./data/E-commerce Customer Behavior.csv")  
    return df
df = load_data()

# Sidebar for filters
st.sidebar.header("Filters")
gender_filter = st.sidebar.multiselect("Select Gender", options=df["Gender"].unique(), default=df["Gender"].unique())
city_filter = st.sidebar.multiselect("Select City", options=df["City"].unique(), default=df["City"].unique())
membership_filter = st.sidebar.multiselect("Select Membership Type", options=df["Membership Type"].unique(), default=df["Membership Type"].unique())

# Apply filters
filtered_df = df[
    (df["Gender"].isin(gender_filter)) &
    (df["City"].isin(city_filter)) &
    (df["Membership Type"].isin(membership_filter))
]

# Display dataset overview
st.header("Dataset Overview")
st.write("Filtered Dataset")
st.dataframe(filtered_df.head())

# Visualization 1: Total Spend by Membership Type
st.header("Total Spend by Membership Type")
fig1 = px.box(
    filtered_df,
    x="Membership Type",
    y="Total Spend",
    color="Membership Type",
    title="Total Spend Distribution by Membership Type"
)
st.plotly_chart(fig1, use_container_width=True)

# Visualization 2: Satisfaction Level by City
st.header("Satisfaction Level by City")
fig2 = px.histogram(
    filtered_df,
    x="City",
    color="Satisfaction Level",
    barmode="group",
    title="Satisfaction Level Distribution by City"
)
st.plotly_chart(fig2, use_container_width=True)

# Visualization 3: Average Rating vs Days Since Last Purchase
st.header("Average Rating vs Days Since Last Purchase")
fig3 = px.scatter(
    filtered_df,
    x="Days Since Last Purchase",
    y="Average Rating",
    color="Satisfaction Level",
    size="Total Spend",
    hover_data=["Customer ID", "City"],
    title="Average Rating vs Days Since Last Purchase"
)
st.plotly_chart(fig3, use_container_width=True)

# Visualization 4: Correlation Heatmap
st.header("Correlation Heatmap")
numeric_cols = filtered_df.select_dtypes(include=["float64", "int64"]).columns
corr_matrix = filtered_df[numeric_cols].corr()
fig4, ax = plt.subplots()
sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", ax=ax)
st.pyplot(fig4)

# Visualization 5: Satisfaction Level Distribution
st.header("Satisfaction Distribution")
fig_pie = px.pie(filtered_df, names="Satisfaction Level", title="Customer Satisfaction Distribution")
st.plotly_chart(fig_pie, use_container_width=True)

# Identify potential churn risks
st.header("Potential Churn Risks")
churn_risk = filtered_df[filtered_df["Days Since Last Purchase"] > 40]
st.write(f"Customers at risk of churn: {len(churn_risk)}")
st.dataframe(churn_risk[["Customer ID", "City", "Days Since Last Purchase"]])

# Footer
st.markdown("---")
st.markdown("Portfolio dibimbing by Dhaffa Devara | Data Enthusiast | Python & Data Science Learner")