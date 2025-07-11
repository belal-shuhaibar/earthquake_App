# usgs_api.py

import requests
import pandas as pd
from datetime import datetime
import logging

# Setup logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def fetch_earthquake_data(start_date, end_date, min_magnitude):
    logger.info(f"Fetching earthquake data from USGS API...")
    url = (
        "https://earthquake.usgs.gov/fdsnws/event/1/query?"
        f"format=geojson&starttime={start_date}&endtime={end_date}&minmagnitude={min_magnitude}"
    )
    logger.info(f"API Request URL: {url}")

    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"Request to USGS API failed: {e}")
        return pd.DataFrame()

    data = response.json()
    features = data.get("features", [])
    logger.info(f"Received {len(features)} features from API.")

    records = []
    for quake in features:
        try:
            props = quake["properties"]
            coords = quake["geometry"]["coordinates"]
            records.append({
                "place": props.get("place", "Unknown"),
                "magnitude": props.get("mag", 0.0),
                "time": datetime.utcfromtimestamp(props.get("time", 0) / 1000.0),
                "longitude": coords[0],
                "latitude": coords[1],
                "depth": coords[2],
            })
        except Exception as e:
            logger.warning(f"Error processing record: {e}")
            continue

    logger.info(f"Processed {len(records)} earthquake records.")
    return pd.DataFrame(records)
