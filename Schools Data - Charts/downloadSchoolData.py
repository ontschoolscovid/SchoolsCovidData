import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import urllib.request
import json
import os
from datetime import datetime

#creating a dataFrame
df = pd.read_csv('https://data.ontario.ca/dataset/b1fef838-8784-4338-8ef9-ae7cfd405b41/resource/7fbdbb48-d074-45d9-93cb-f7de58950418/download/schoolcovidsummary.csv')

today = datetime.today().strftime('%Y-%m-%d')

dt_all = pd.date_range(start=df['reported_date'].iloc[0],end=df['reported_date'].iloc[34]) #creating date range that only includes dates that have data (no weekends)
print(dt_all)

#sets the x axis to the date range and creates lines based on all the data retrieved and creates the figure
x = dt_all
totalCasesFig = go.Figure(go.Scatter(x = x, y = df['cumulative_school_related_student_cases'], mode='lines+markers', name = 'Student Cases'))
totalCasesFig.add_trace(go.Scatter(x = x, y = df['cumulative_school_related_staff_cases'], mode='lines+markers', name = 'Staff Cases', line=dict(color="purple")))
totalCasesFig.add_trace(go.Scatter(x = x, y = df['cumulative_school_related_cases'], mode='lines+markers', name = 'Total Cases', line=dict(color="red")))
totalCasesFig.add_trace(go.Scatter(x = x, y = df['cumulative_school_related_unspecified_cases'], mode='lines+markers', name = 'Unspecified Cases', line=dict(color="green")))
totalCasesFig.update_layout(title='Total Student and Staff Cases Over Time', plot_bgcolor='rgb(237, 237, 225)', showlegend=True)

#totalCasesFig.update_xaxes(rangebreaks=[dict(values=dt_breaks)])

#updates the figure with Axis titles
totalCasesFig.update_layout(
    xaxis_title="Date",
    yaxis_title="Number of Cases"
)

newCasesFig = go.Figure(go.Scatter(x = x, y = df['new_school_related_student_cases'], mode='lines+markers', name = 'Student Cases'))
newCasesFig.add_trace(go.Scatter(x = x, y = df['new_school_related_staff_cases'], mode='lines+markers', name = 'Staff Cases', line=dict(color="purple")))
newCasesFig.add_trace(go.Scatter(x = x, y = df['new_total_school_related_cases'], mode='lines+markers', name = 'Total New Cases', line=dict(color="red")))
newCasesFig.add_trace(go.Scatter(x = x, y = df['new_school_related_unspecified_cases'], mode='lines+markers', name = 'Unspecified Cases', line=dict(color="green")))
newCasesFig.update_layout(title='New Student and Staff Cases Over Time', plot_bgcolor='rgb(237, 237, 225)', showlegend=True)

#newCasesFig.update_xaxes(rangebreaks=[dict(values=dt_breaks)])

newCasesFig.update_layout(
    xaxis_title="Date",
    yaxis_title="Number of Cases"
)

#creating html files
totalCasesFig.write_html('html files/totalCasesFigure.html', auto_open=True)
newCasesFig.write_html('html files/newCasesFigure.html', auto_open=True)

#creating images for line plots
totalCasesFig.write_image("images/totalCasesFig.jpeg")
newCasesFig.write_image("images/newStaffFig.jpeg")