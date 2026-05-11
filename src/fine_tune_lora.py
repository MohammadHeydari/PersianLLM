import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import LoraConfig, get_peft_model, TaskType
import json

# مسیر مدل Ollama Gemma3:4B
model_name = "path_to_gemma3_4b_on_ollama"

# مسیر dataset
dataset_path = "data/instruction/gizmiz_instruction.jsonl"

# Load tokenizer و model
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto", torch_dtype=torch.float16)

# LoRA configuration
lora_config = LoraConfig(
    task_type=TaskType.CAUSAL_LM,
    r=8,
    lora_alpha=16,
    target_modules=["q_proj", "v_proj"],  # تغییرات اصلی در attention
    lora_dropout=0.05,
    bias="none"
)

# اضافه کردن LoRA به مدل
model = get_peft_model(model, lora_config)

# Load dataset
with open(dataset_path, "r", encoding="utf-8") as f:
    dataset = [json.loads(line) for line in f]

# ساده‌ترین preprocessing: توکنایز متن و output
inputs = []
labels = []

for item in dataset:
    prompt = f"{item['instruction']}\n{item['input']}\nOutput:"
    target = json.dumps(item['output'], ensure_ascii=False)
    inputs.append(prompt)
    labels.append(target)

# tokenization
encodings = tokenizer(inputs, padding=True, truncation=True, max_length=512, return_tensors="pt")
labels_enc = tokenizer(labels, padding=True, truncation=True, max_length=128, return_tensors="pt")["input_ids"]

# Move to GPU
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)
encodings = {k:v.to(device) for k,v in encodings.items()}
labels_enc = labels_enc.to(device)

# Training setup (خیلی ساده)
from torch.utils.data import TensorDataset, DataLoader
from torch.optim import AdamW

dataset = TensorDataset(encodings["input_ids"], encodings["attention_mask"], labels_enc)
dataloader = DataLoader(dataset, batch_size=4, shuffle=True)

optimizer = AdamW(model.parameters(), lr=2e-4)

# Simple training loop
epochs = 3
for epoch in range(epochs):
    for batch in dataloader:
        input_ids, attention_mask, labels = batch
        outputs = model(input_ids=input_ids, attention_mask=attention_mask, labels=labels)
        loss = outputs.loss
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()
    print(f"Epoch {epoch+1} completed, loss: {loss.item()}")