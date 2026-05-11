# src/demo_prompt_cli.py

import json
import subprocess

# مسیر dataset
dataset_path = "data/instruction/gizmiz_instruction.jsonl"

# مدل blob Gemma3:4B در Ollama
model_name = "gemma3:4b"

# خواندن dataset
with open(dataset_path, "r", encoding="utf-8") as f:
    dataset = [json.loads(line) for line in f]

# تست 5 پیام اول
for item in dataset[:5]:
    instruction = item["instruction"]
    input_text = item["input"]

    # ساخت prompt
    prompt = f"{instruction}\n{input_text}\nAnswer:"

    # ⚡ اجرای دستور ollama CLI و گرفتن خروجی با دستور run
    result = subprocess.run(
        ["ollama", "run", model_name, "--prompt", prompt],
        capture_output=True,
        text=True
    )

    # چاپ خروجی مدل
    print("="*50)
    print("Input:")
    print(input_text)
    print("\nModel Prediction:")
    print(result.stdout.strip())