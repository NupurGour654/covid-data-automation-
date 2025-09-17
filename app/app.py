import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(
    page_title="🦠 COVID-19 Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------
# Title
# -------------------------------
st.title("🦠 COVID-19 Interactive Dashboard")
st.markdown("Explore COVID-19 trends using cleaned datasets. Interactive & fancy charts included!")

# -------------------------------
# Load Data
# -------------------------------
@st.cache_data
def load_data():
    cleaned_path = "../data/cleaned"  # 🔹 Update path if app.py location changes
    clean_complete = pd.read_csv(os.path.join(cleaned_path, "covid_19_clean_complete_cleaned.csv"))
    worldometer = pd.read_csv(os.path.join(cleaned_path, "worldometer_data_cleaned.csv"))
    return clean_complete, worldometer

clean_complete, worldometer = load_data()

# -------------------------------
# Sidebar Filters
# -------------------------------
st.sidebar.header("Filters")
country_list = sorted(clean_complete["Country/Region"].unique())
selected_country = st.sidebar.selectbox("Select Country", ["Global"] + country_list)

# -------------------------------
# Tabs
# -------------------------------
tab1, tab2, tab3 = st.tabs(["📊 Trend Charts", "🌍 Latest Snapshot", "⚖️ Deaths vs Cases"])

# -------------------------------
# Tab 1: Trend Charts
# -------------------------------
with tab1:
    st.subheader("COVID-19 Cases Trend")
    if selected_country == "Global":
        df_plot = clean_complete.groupby("Date")[["Confirmed","Deaths","Recovered","Active"]].sum().reset_index()
    else:
        df_plot = clean_complete[clean_complete["Country/Region"] == selected_country]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_plot["Date"], y=df_plot["Confirmed"], mode='lines+markers', name='Confirmed'))
    fig.add_trace(go.Scatter(x=df_plot["Date"], y=df_plot["Deaths"], mode='lines+markers', name='Deaths'))
    fig.add_trace(go.Scatter(x=df_plot["Date"], y=df_plot["Recovered"], mode='lines+markers', name='Recovered'))
    fig.add_trace(go.Scatter(x=df_plot["Date"], y=df_plot["Active"], mode='lines+markers', name='Active'))

    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Number of Cases",
        legend_title="Cases Type",
        hovermode="x unified"
    )
    st.plotly_chart(fig, use_container_width=True)

# -------------------------------
# Tab 2: Latest Snapshot
# -------------------------------
with tab2:
    st.subheader("🌍 Worldometer Latest Data")
    display_cols = ["Country/Region", "TotalCases", "TotalDeaths", "TotalRecovered", "ActiveCases", "Population"]
    st.dataframe(worldometer[display_cols].sort_values("TotalCases", ascending=False).head(20))

    # Summary metrics in sidebar
    st.sidebar.header("Summary Stats")
    if selected_country == "Global":
        latest = worldometer.sum(numeric_only=True)
        st.sidebar.metric("Total Cases", f"{int(latest['TotalCases']):,}")
        st.sidebar.metric("Total Deaths", f"{int(latest['TotalDeaths']):,}")
        st.sidebar.metric("Total Recovered", f"{int(latest['TotalRecovered']):,}")
    else:
        latest = worldometer[worldometer["Country/Region"]==selected_country].iloc[0]
        st.sidebar.metric("Total Cases", f"{int(latest['TotalCases']):,}")
        st.sidebar.metric("Total Deaths", f"{int(latest['TotalDeaths']):,}")
        st.sidebar.metric("Total Recovered", f"{int(latest['TotalRecovered']):,}")

# -------------------------------
# Tab 3: Deaths vs Cases Barplot
# -------------------------------
with tab3:
    st.subheader("Top 15 Countries: Deaths vs Cases")
    top_deaths = worldometer.sort_values(by="TotalDeaths", ascending=False).head(15)
    fig2 = px.bar(
        top_deaths,
        x="TotalDeaths",
        y="Country/Region",
        orientation='h',
        color="TotalDeaths",
        color_continuous_scale="Reds",
        labels={"TotalDeaths": "Total Deaths", "Country/Region": "Country"},
        text="TotalDeaths"
    )
    fig2.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig2, use_container_width=True)

