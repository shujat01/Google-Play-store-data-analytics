# TASK : "1. Generate a word cloud for the most frequent keywords found in 5-star reviews, but exclude common
#         stopwords and app names. Additionally, filter the reviews to include only 
#         those from apps in the "Health & Fitness" category."

import pandas as pd
import re
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
import nltk

nltk.download('stopwords')
nltk.download('punkt')

apps_df = pd.read_csv('datasets/cleaned playstore dataset.csv')
reviews_df = pd.read_csv('datasets/cleaned User review dataset.csv')
reviews_df.dropna(subset=['Translated_Review'], inplace=True)

data = pd.merge(apps_df, reviews_df, on='App', how='inner')

health_data = data[data['Category'] == 'HEALTH_AND_FITNESS'].copy()
def clean_text(text):
    if pd.isna(text):
        return ""
    text = re.sub(r'[^\w\s]', '', text)  
    text = re.sub(r'\d+', '', text)     
    text = text.lower()                 
    return text

health_data['Cleaned Reviews'] = health_data['Translated_Review'].apply(clean_text)

five_star_reviews = health_data[health_data['Rating'] == 4.0]['Cleaned Reviews']
print(five_star_reviews.shape)
all_reviews = " ".join(five_star_reviews)

print(all_reviews)

stop_words = set(stopwords.words('english'))
tokens = word_tokenize(all_reviews)
filtered_tokens = [word for word in tokens if word not in stop_words]

app_names = health_data['App'].apply(clean_text).unique()
filtered_tokens = [word for word in filtered_tokens if word not in app_names]

word_freq = Counter(filtered_tokens)

plt.figure(figsize=(10, 5))

if word_freq:
    wordcloud = WordCloud(width=800, height=400, background_color='white', max_words=100).generate_from_frequencies(word_freq)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.title('Word Cloud for Most Frequent Keywords in 5-Star Reviews (Health & Fitness)', fontsize=16)
else:
    # Display a blank word cloud if no words are available
    plt.imshow([[255]], cmap='gray', vmin=0, vmax=255, interpolation='nearest')  # Blank white image
    #plt.title('No Words Available For Most Frequent Keywords in 5-Star Reviews (Health & Fitness)', fontsize=16)

plt.axis('off')
plt.show()
