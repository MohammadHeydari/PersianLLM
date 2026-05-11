import pandas as pd

gizmiz_path = "data/raw/clean_gizmiz.csv"
twitter_path = "data/raw/clean_officialpersiantwitter.csv"

df_gizmiz = pd.read_csv(gizmiz_path)
df_twitter = pd.read_csv(twitter_path)

print("=== GIZMIZ ===")
print(df_gizmiz.head())
print(df_gizmiz.columns)
print(df_gizmiz.info())

print("\n=== TWITTER CHANNEL ===")
print(df_twitter.head())
print(df_twitter.columns)
print(df_twitter.info())