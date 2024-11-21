import pandas as pd

df = pd.read_csv('datasets/Play Store Data.csv')

print("Initial Dataset Info:")
print(df.info())
df.columns = df.columns.str.strip()

df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')

# Function to clean and convert the 'Size' column
def clean_size_column(size):
    if isinstance(size, str):
        size = size.strip().lower()
        if 'k' in size:
            return float(size.replace('k', '')) / 1024  # Convert KB to MB
        elif 'm' in size:
            return float(size.replace('m', ''))  
    return None 

df['Size'] = df['Size'].apply(clean_size_column)
df['Size'] = pd.to_numeric(df['Size'], errors='coerce')  


df['Reviews'] = pd.to_numeric(df['Reviews'], errors='coerce')

# df.loc[df['Type'] == '0', 'Type'] = 'Free'
# df.loc[df['Installs']=='Free', 'Installs'] =['0']
df.drop(10472, axis=0, inplace=True)

df['Installs'] = df['Installs'].str.replace(',', '').str.replace('+', '').astype(float)

df['Price'] = df['Price'].str.replace('$', '', regex=False).astype(float)

df['Last Updated'] = pd.to_datetime(df['Last Updated'], errors='coerce')

df['Android Ver'] = df['Android Ver'].replace("Varies with device", None)  # Replace with NaN

df = df.drop_duplicates()

df = df.dropna(thresh=len(df.columns) - 2)

print("\nCleaned Dataset Info:")
print(df.info())

# Save cleaned dataset to a new file
cleaned_file_path = "cleaned playstore dataset.csv"
df.to_csv(cleaned_file_path, index=False)
