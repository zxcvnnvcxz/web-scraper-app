import streamlit as st
import plotly.express as px
import sqlite3

connection = sqlite3.connect("./files/data.db")
cursor = connection.cursor()

cursor.execute("SELECT date FROM events")
date = cursor.fetchall()
date = [item[0] for item in date]

cursor.execute("SELECT temp FROM events")
temp = cursor.fetchall()
temp = [item[0] for item in temp]

figure = px.line(x=date, y=temp,
                 labels={"x": "Date", "y": "Temperature (C)"})

st.plotly_chart(figure)