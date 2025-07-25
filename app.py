### app.py
"""Earthquake Data Analysis and Visualization App
This Streamlit app fetches earthquake data from the USGS API, allows users to filter by date and magnitude,
and visualizes the data on an interactive map. It also provides analytics and logs query history
using SQLite.
"""

"""Earthquake Data Analysis and Visualization App"""
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import logging
import folium
from streamlit_folium import st_folium
from usgs_api import fetch_earthquake_data
from db_logger import init_db, log_query, get_query_history
from database import fetch_and_store_sample_data
from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib.pyplot as plt

# ------------------ Setup Logging ------------------
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ------------------ Page Config ------------------
st.set_page_config(page_title="🌍 Earthquake Analyzer", layout="wide")
logger.info("Streamlit app started.")

# ------------------ Initialize DB ------------------
init_db()

# ------------------ Custom CSS ------------------
st.markdown("""
    <style>
        .title {
            color: #004466;
            font-size: 36px;
            font-weight: bold;
        }
        .subtitle {
            color: #003344;
            font-size: 20px;
            font-weight: 600;
        }
        .footer {
            text-align: center;
            font-size: 12px;
            color: #888888;
            margin-top: 2rem;
        }
        .stButton>button {
            background-color: #0072B5;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

# ------------------ Header ------------------
st.markdown('<div class="title">🌍 Earthquake Data Analysis & Visualization</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Explore real-time earthquake activity across the globe using USGS data</div>', unsafe_allow_html=True)
st.markdown("---")

# ------------------ Sidebar Filters ------------------
st.sidebar.header("🔍 Query Filters")
end_date = datetime.utcnow().date()
start_date = st.sidebar.date_input("Start Date", end_date - timedelta(days=7), max_value=end_date)
end_date = st.sidebar.date_input("End Date", end_date, min_value=start_date)
min_mag = st.sidebar.slider("Minimum Magnitude", 1.0, 10.0, 4.0, 0.1)
logger.info(f"User selected filters - Start: {start_date}, End: {end_date}, Min Mag: {min_mag}")

# ------------------ Data Retrieval ------------------
df = fetch_earthquake_data(start_date, end_date, min_mag)
if df.empty:
    st.warning("No earthquake data found for the selected filters.")
    logger.warning("No data retrieved for selected filters.")
    st.stop()

log_query(start_date, end_date, min_mag, len(df))
logger.info(f"Fetched {len(df)} earthquake records.")

# ✅ Show preview of fetched data
st.subheader("📋 Earthquake Data Preview")
st.dataframe(df)

# ------------------ Store in Earthquakes Table ------------------
fetch_and_store_sample_data()
logger.info("Stored sample data into 'earthquakes.db'.")

# ------------------ Tab Layout ------------------
tab1, tab2, tab3 = st.tabs(["🌍 Map", "📊 Analytics", "📁 History"])

# ------------------ Tab 1: Earthquake Map ------------------
with tab1:
    st.subheader("📜 Interactive Earthquake Map")
    center = [df["latitude"].mean(), df["longitude"].mean()]
    quake_map = folium.Map(location=center, zoom_start=2)

    for _, row in df.iterrows():
        popup = f"""
        <b>Location:</b> {row['place']}<br>
        <b>Magnitude:</b> {row['magnitude']}<br>
        <b>Depth:</b> {row['depth']} km<br>
        <b>Time:</b> {row['time']}
        """
        color = "red" if row["magnitude"] >= 6 else "orange" if row["magnitude"] >= 5 else "blue"
        folium.CircleMarker(
            location=[row["latitude"], row["longitude"]],
            radius=5,
            color=color,
            fill=True,
            fill_opacity=0.7,
            popup=popup
        ).add_to(quake_map)

    st_folium(quake_map, width=1000, height=600)
    logger.info("Map rendered with earthquake markers.")

# ------------------ Tab 2: Charts ------------------
with tab2:
    with st.expander("📈 Earthquake Timeline"):
        st.subheader("Number of Earthquakes per Day")
        df["date"] = pd.to_datetime(df["time"]).dt.date
        timeline = df.groupby("date").size()
        st.line_chart(timeline)

    with st.expander("📊 Magnitude Distribution"):
        st.subheader("Magnitude Frequency Histogram")
        st.bar_chart(df["magnitude"].value_counts().sort_index())

    with st.expander("📉 Linear Regression - Date vs Avg Magnitude"):
        st.subheader("Trend of Average Earthquake Magnitude Over Time")
        df["date"] = pd.to_datetime(df["time"]).dt.date
        daily_avg_mag = df.groupby("date")["magnitude"].mean().reset_index()
        daily_avg_mag["ordinal_date"] = pd.to_datetime(daily_avg_mag["date"]).map(datetime.toordinal)

        X = daily_avg_mag["ordinal_date"].values.reshape(-1, 1)
        y = daily_avg_mag["magnitude"].values
        model = LinearRegression()
        model.fit(X, y)
        y_pred = model.predict(X)

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.scatter(daily_avg_mag["date"], y, label="Actual", color="blue")
        ax.plot(daily_avg_mag["date"], y_pred, label="Linear Fit", color="red")
        ax.set_xlabel("Date")
        ax.set_ylabel("Average Magnitude")
        ax.set_title("Linear Regression - Date vs Avg Magnitude")
        ax.legend()
        st.pyplot(fig)

    with st.expander(" Top 10 Strongest Earthquakes"):
        st.subheader("Top Earthquakes by Magnitude")
        st.dataframe(df.sort_values("magnitude", ascending=False).head(10)[["place", "magnitude", "time", "depth"]])

    st.download_button("📅 Download Results as CSV", data=df.to_csv(index=False), file_name="earthquake_data.csv", mime="text/csv")
    logger.info("Charts and CSV download rendered.")

# ------------------ Tab 3: Query History ------------------
with tab3:
    st.subheader("📁 Previous Queries Log")
    try:
        history_df = get_query_history()
        st.dataframe(history_df)
        logger.info("Displayed query history table.")
    except Exception as e:
        st.warning("No queries have been logged yet.")
        logger.warning(f"Failed to load query history: {e}")

# ------------------ Footer ------------------
st.markdown('<div class="footer">  USGS Data API · Folium</div>', unsafe_allow_html=True)
logger.info("App execution completed.")
