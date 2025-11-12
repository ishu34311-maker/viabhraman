# config.py
import pymongo
import streamlit as st

# You can set this in Streamlit Secrets for security
MONGO_URI = st.secrets.get("MONGO_URI", "your_mongo_connection_string")

client = pymongo.MongoClient(MONGO_URI)
db = client["viabrhaman_db"]

customers_collection = db["customers"]
queries_collection = db["queries"]
packages_collection = db["packages"]
