# TASK : Create a dual-axis chart comparing the average installs and revenue for free vs. paid apps within the top 3 app categories.
#        Apply filters to exclude apps with fewer than 10,000 installs and revenue below $10,000 and android version should be more than 4.0 
#        as well as size should be more than 15M and content rating should be Everyone and app name should not have more than 30 characters 
#        including space and special character .this graph should work only between 1 PM IST to 2 PM IST apart from that time we should not 
#        show this graph in dashboard itself.


import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from datetime import datetime
import pytz

apps_df = pd.read_csv('datasets/cleaned playstore dataset.csv') 

# Add Revenue column
apps_df['Revenue'] = apps_df.apply(
    lambda x: x['Price'] * x['Installs'] if x['Type'] == 'Paid' else 0,
    axis=1
)

def clean_android_version(version):
    if isinstance(version, str):  # If the value is a string
        version = version.replace('and up', '').strip()  # Remove 'and up' and trailing spaces
        return float(version.split('.')[0])  # Extract the major version
    elif isinstance(version, float):  # If the value is already a float (e.g., NaN or clean data)
        return version
    return None  # Handle unexpected cases

apps_df['Android Ver'] = apps_df['Android Ver'].apply(clean_android_version)

# Filtering criteria
filtered_apps = apps_df[
    (apps_df['Installs'] >= 10000) &
    ((apps_df['Type'] == 'Paid') & (apps_df['Revenue'] >= 10000) | (apps_df['Type'] == 'Free')) &
    (apps_df['Android Ver'] > 4.0) &
    (apps_df['Size'] > 15) &
    (apps_df['Content Rating'] == 'Everyone') &
    (apps_df['App'].str.len() <= 30)
]


# Calculate average installs and revenue for free vs paid apps within top 3 categories
top_categories = filtered_apps['Category'].value_counts().nlargest(3).index
filtered_apps = filtered_apps[filtered_apps['Category'].isin(top_categories)]

grouped_data = filtered_apps.groupby(['Category', 'Type']).agg({
    'Installs': 'mean',
    'Revenue': 'mean'
}).reset_index()

# Time restriction (1 PM IST to 2 PM IST)
ist_timezone = pytz.timezone("Asia/Kolkata")
current_time = datetime.now(ist_timezone)

if 13 <= current_time.hour < 14:  # 1 PM to 2 PM IST
    st.title("Dual-Axis Chart: Average Installs and Revenue")

    # Create a dual-axis chart
    fig = go.Figure()

    for category in top_categories:
        category_data = grouped_data[grouped_data['Category'] == category]

        # Add bar chart for average installs
        fig.add_trace(go.Bar(
            x=category_data['Type'],
            y=category_data['Installs'],
            name=f'{category} - Avg Installs',
            marker_color='lightblue'
        ))

        # Add line chart for average revenue
        fig.add_trace(go.Scatter(
            x=category_data['Type'],
            y=category_data['Revenue'],
            mode='lines+markers',
            name=f'{category} - Avg Revenue',
            yaxis='y2'
        ))

    # Update layout for dual-axis
    fig.update_layout(
        title="Comparison of Avg Installs and Revenue for Free vs Paid Apps",
        xaxis_title="App Type",
        yaxis=dict(title="Average Installs"),
        yaxis2=dict(
            title="Average Revenue",
            overlaying='y',
            side='right'
        ),
        barmode='group',
        legend_title="Categories"
    )

    # Display the chart
    st.plotly_chart(fig)
else:
    st.title("The graph is not available outside 1 PM to 2 PM IST.")
