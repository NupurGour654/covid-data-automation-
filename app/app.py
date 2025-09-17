import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(page_title="🦠 COVID-19 Dashboard", layout="wide")
st.title("🦠 COVID-19 Interactive Dashboard")
st.markdown("Explore COVID-19 trends using cleaned datasets from Google Sheets.")

# -------------------------------
# Load Data from Google Sheets
# -------------------------------
@st.cache_data
def load_data():
    # 🔹 File IDs from Google Drive
    CLEAN_COMPLETE_ID = "1xS796WDWsalAFcMClLNVtr8DUsuVZqjGuQ3HsAJ8OHA"
    WORLDOMETER_ID = "1XBu5i_5EioZX-pHRhAX90DQEZy2e2-XgtulEZIGLEao"

    # Convert to CSV export link
    clean_complete_url = f"https://docs.google.com/spreadsheets/d/{CLEAN_COMPLETE_ID}/export?format=csv&gid=1327158710"
    worldometer_url = f"https://docs.google.com/spreadsheets/d/{WORLDOMETER_ID}/export?format=csv&gid=0"

    # Load CSVs
    clean_complete = pd.read_csv(clean_complete_url)
    worldometer = pd.read_csv(worldometer_url)

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
# Tab 3: Deaths vs Cases
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
        labels={"TotalDeaths":"Total Deaths","Country/Region":"Country"},
        text="TotalDeaths"
    )
    fig2.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig2, use_container_width=True)
