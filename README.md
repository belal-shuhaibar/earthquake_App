#  Earthquake Data Analysis and Visualization App

This Streamlit web application allows users to explore real-time earthquake data from the USGS (United States Geological Survey) API. The app includes data filters, interactive maps, dynamic charts, and a query logging feature for analysis history. It is built using Python, Streamlit, SQLite, and visualization libraries like Folium and Pandas.

---

##  Features

- **Live Data Fetching** from the USGS Earthquake API based on user-defined filters (date range and minimum magnitude).
- **Interactive Streamlit Interface** with sliders, date pickers, and real-time visualization.
- **Map Visualization** with color-coded markers using Folium.
- **Charts** showing earthquake distribution by magnitude and time.
- **SQLite Integration** for logging user queries and storing earthquake data.
- **Downloadable CSV** of filtered earthquake data.

---

##  Technology Stack

- **Frontend**: [Streamlit](https://streamlit.io)
- **Backend**: Python (requests, pandas, logging)
- **Database**: SQLite (`sqlite3` module)
- **API**: [USGS Earthquake API](https://earthquake.usgs.gov/fdsnws/event/1/)
- **Mapping**: Folium

---

##  Project Structure

```
├── app.py               # Main Streamlit UI
├── database.py          # Fetch and store data from USGS
├── db_logger.py         # Log user queries
├── usgs_api.py          # API integration and data formatting
├── earthquakes.db       # SQLite DB for earthquake data
├── query_logs.db        # SQLite DB for query logging
├── README.md            # Project documentation
```

---

##  How It Works

1. **User selects** filters for date range and minimum magnitude via the Streamlit UI.
2. **Backend script** (`usgs_api.py`) constructs the API URL and fetches real-time data from the USGS endpoint.
3. **Data is processed** using Pandas and stored in `earthquakes.db`.
4. **Query is logged** with timestamp in `query_logs.db` using `db_logger.py`.
5. **Results are visualized** with charts and maps, and can be exported as CSV.

---

## 📷 Screenshots

> Add the following in the actual GitHub repository:
- Screenshot of Streamlit UI
- <img width="1355" height="625" alt="image" src="https://github.com/user-attachments/assets/c1f69535-4f55-45b6-b328-4164e76a0790" />

- Screenshot of the map with earthquake markers
- <img width="1365" height="634" alt="image" src="https://github.com/user-attachments/assets/aff43351-3692-40a0-ba47-ac80994f707a" />

- Screenshot of the query log table
- <img width="1362" height="628" alt="image" src="https://github.com/user-attachments/assets/32032db7-facd-493a-9598-c61f5a35d34d" />

- Number of Earthquakes per day
- <img width="1365" height="636" alt="image" src="https://github.com/user-attachments/assets/e62761bc-11ab-4fc1-a30c-0db3f18d964b" />


---

##  Team Members

- Vijay Javvaji– API integration (`usgs_api.py`)
- Belal Shuhaibar– Database management (`database.py`, `db_logger.py`)
- Mithil Sai Yachamaneni– Frontend & Streamlit integration (`app.py`)

---

## 🏁 Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/earthquake_App.git
   cd earthquake_App
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   streamlit run app.py
   ```

4. Visit `http://localhost:8501` in your browser.

---

##  Future Improvements

- Add predictive modeling using historical trends.
- Integrate with cloud databases like PostgreSQL.
- Include alert systems for high-magnitude earthquakes.

---

## 📚 References

- [USGS Earthquake API Docs](https://earthquake.usgs.gov/fdsnws/event/1/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [SQLite Official Docs](https://www.sqlite.org/docs.html)

