import streamlit as st
import pandas as pd

df = pd.read_csv("./data/university_rankings.csv")

st.title("Top 500 Universities")
st.subheader("Explore the rankings of the world's top universities")

st.sidebar.header("Filter Options")

selected_region = st.sidebar.multiselect(
    "Select Region(s):", options=df["region"].unique(), default=df["region"].unique()
)

available_countries = df[df["region"].isin(selected_region)]["country"].unique()

selected_country = st.sidebar.multiselect(
    "Select Country:", options=sorted(available_countries), default=available_countries
)

filtered_df = df[
    (df["region"].isin(selected_region)) & (df["country"].isin(selected_country))
]

st.write(f"Showing {len(filtered_df)} universities")
st.dataframe(filtered_df)
