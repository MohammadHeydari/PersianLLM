# src/demo_prompt.py

import json
from ollama import Ollama
import os

#  مسیر dataset
dataset_path = "data/instruction/gizmiz_instruction.jsonl"

# ⚡ init Ollama client
client = Ollama()

# ⚡ مدل blob Gemma3:4B که در Ollama نصب شده
model_name = "gemma3:4b"  # یا نامی که ollama list می‌دهد

# ⚡ خواندن dataset
with open(dataset_path, "r", encoding="utf-8") as f:
    dataset = [json.loads(line) for line in f]

# ⚡ تست 5 پیام اول
for item in dataset[:5]:
    instruction = item["instruction"]
    input_text = item["input"]

    # ساخت prompt
    prompt = f"{instruction}\n{input_text}\nAnswer:"

    # ⚡ ارسال به مدل
    response = client.chat(model=model_name, prompt=prompt, max_tokens=200)

    # نمایش نتیجه
    print("="*50)
    print("Input:")
    print(input_text)
    print("\nModel Prediction:")
    print(response['text'])  # پاسخ مدل