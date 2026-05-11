import pandas as pd
import json

# خواندن دیتا
df_gizmiz = pd.read_csv("data/raw/clean_gizmiz.csv")
df_twitter = pd.read_csv("data/raw/clean_officialpersiantwitter.csv")

# helper function برای گرفتن top reactions
def get_top_reactions(row):
    reactions = []
    for i in range(1, 6):
        react = row[f"react{i}"]
        count = row[f"count{i}"]
        if count > 0:
            reactions.append(react)
    return reactions

# ساخت instruction dataset برای Gizmiz
instruction_list = []

for _, row in df_gizmiz.iterrows():
    instruction_list.append({
        "instruction": "این پیام را تحلیل کن و پیش‌بینی کن که کاربران چه واکنشی نشان می‌دهند.",
        "input": row["text"],
        "output": {
            "top_reactions": get_top_reactions(row),
            "reasoning": "این پیام محتوای احساسی دارد و احتمالاً واکنش کاربران به ترتیب نمایش داده شده رخ می‌دهد."
        }
    })

with open("data/instruction/gizmiz_instruction.jsonl", "w", encoding="utf-8") as f:
    for item in instruction_list:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")