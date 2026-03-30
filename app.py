import streamlit as st
import mysql.connector
import pandas as pd

# DB connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="vinisha@2005",
    database="asteroid_db"
)

# Title
st.title("🚀 Asteroid Analysis Dashboard")
st.write("Explore NASA Near-Earth Objects Data")

# KPI
count_df = pd.read_sql("SELECT COUNT(*) as total FROM asteroids", conn)
st.metric("Total Asteroids", count_df['total'][0])

# User Inputs
search = st.text_input("🔍 Search Asteroid Name")
limit = st.slider("Rows", 10, 10350, 5000)
option = st.selectbox("Choose Analysis", [
    "Fastest Asteroids",
    "Closest Asteroids",
    "Hazardous Asteroids",
    "Full Details"
])

# Queries
if option == "Fastest Asteroids":
    query = f"""
    SELECT a.name, c.velocity, c.close_approach_date
    FROM asteroids a
    JOIN close_approach c ON a.id = c.id
    WHERE a.name LIKE '%{search}%'
    ORDER BY c.velocity DESC
    LIMIT {limit}
    """

elif option == "Closest Asteroids":
    query = f"""
    SELECT a.name, c.miss_distance_km, c.close_approach_date
    FROM asteroids a
    JOIN close_approach c ON a.id = c.id
    WHERE a.name LIKE '%{search}%'
    ORDER BY c.miss_distance_km ASC
    LIMIT {limit}
    """

elif option == "Hazardous Asteroids":
    query = f"""
    SELECT a.name, a.hazardous
    FROM asteroids a
    WHERE a.hazardous = 1
    AND a.name LIKE '%{search}%'
    LIMIT {limit}
    """

elif option == "Full Details":
    query = f"""
    SELECT a.name, a.absolute_magnitude_h, a.diameter_min, a.diameter_max,
           c.close_approach_date, c.velocity
    FROM asteroids a
    JOIN close_approach c ON a.id = c.id
    WHERE a.name LIKE '%{search}%'
    LIMIT {limit}
    """

# Load data
df = pd.read_sql(query, conn)

# Show table
st.dataframe(df)

# Chart
st.subheader("📊 Velocity Chart")

chart_query = "SELECT velocity FROM close_approach LIMIT 100"
chart_df = pd.read_sql(chart_query, conn)

st.line_chart(chart_df)

# Close connection
conn.close()