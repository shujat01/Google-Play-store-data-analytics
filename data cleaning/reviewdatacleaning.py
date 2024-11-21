import pandas as pd

# Load dataset (replace 'dataset.csv' with the actual file path)
data = pd.read_csv('datasets/User Reviews.csv')

print("Original Dataset:")
print(data.head())

data_cleaned = data.dropna(subset=['Translated_Review', 'Sentiment', 'Sentiment_Polarity', 'Sentiment_Subjectivity'])

data_cleaned = data_cleaned.drop_duplicates()

data_cleaned['Translated_Review'] = data_cleaned['Translated_Review'].str.strip()

data_cleaned['Sentiment_Polarity'] = pd.to_numeric(data_cleaned['Sentiment_Polarity'], errors='coerce')
data_cleaned['Sentiment_Subjectivity'] = pd.to_numeric(data_cleaned['Sentiment_Subjectivity'], errors='coerce')

data_cleaned = data_cleaned.dropna(subset=['Sentiment_Polarity', 'Sentiment_Subjectivity'])


data_cleaned = data_cleaned[data_cleaned['Sentiment'].isin(['Positive', 'Neutral'])]

print("\nCleaned Dataset:")
print(data_cleaned.head())

# Save cleaned dataset to a new CSV file
data_cleaned.to_csv('cleaned User review dataset.csv', index=False)
