# TASK : Plot  a bubble chart to  analyze the relationship between app size (in MB) and average rating,with
#        the bubble size representing the number of installs. Include a filter to show only apps with a rating
#        higher than 3.5 and that belong to the "Games" category and installs shouldbe more than 50k as well
#        well as this graph should work only between 5 PM IST to 7 PM IST apart from that time we should not
#        show this graph  in dashboard itself.


import pandas as pd
import plotly.express as px
import streamlit as st
from datetime import datetime
import pytz

# Load your dataset
apps_df = pd.read_csv('datasets/cleaned playstore dataset.csv')

# Convert the 'Installs' column to numeric (strip out commas)
apps_df['Installs'] = apps_df['Installs'].apply(lambda x: int(x.replace(',', '')) if isinstance(x, str) else x)

# Filter the dataset based on the given conditions
filtered_apps = apps_df[
    (apps_df['Rating'] > 3.5) &  # Rating greater than 3.5
    (apps_df['Category'] == 'GAME') &  # Category is 'Games'
    (apps_df['Installs'] > 50000)  # Installs greater than 50k
]

# Time restriction (5 PM IST to 7 PM IST)
ist_timezone = pytz.timezone("Asia/Kolkata")
current_time = datetime.now(ist_timezone)

if 17 <= current_time.hour < 19:  # 5 PM to 7 PM IST
    st.title("Bubble Chart: App Size vs Average Rating")

    # Create a bubble chart using Plotly Express
    fig = px.scatter(filtered_apps, 
                     x='Size', 
                     y='Rating', 
                     size='Installs', 
                     color='Category',
                     title="Relationship between App Size, Rating, and Installs",
                     labels={'Size': 'App Size (MB)', 'Rating': 'Average Rating'},
                     hover_name='App',
                     size_max=60)

    # Display the bubble chart
    st.plotly_chart(fig)
else:
    st.title("The graph is not available outside 5 PM to 7 PM IST.")
