# PersianLLM (Under Development )

> **Note:** This project is still under development. It is **not production-ready** and may contain errors. Download and use at your own risk.

A prototype project for **analyzing messages and predicting user reactions** using LLMs and Ollama.  
Currently tested with the `Gemma3:4B` model and a sample `Gizmiz Instruction Dataset`.

---


---

## Prerequisites

- Python 3.12+
- GPU (optional, useful for LoRA and PyTorch)
- Ollama CLI installed and configured

---

## Installation

1. **Clone the repository:**

```bash
git clone https://github.com/USERNAME/PersianLLM.git
cd PersianLLM
```

## Create and activate a virtual environment
```
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate
```
## Install dependencies
```
pip install --upgrade pip
pip install -r requirements.txt
```
## Install and configure Ollama:
### Download and install Ollama: https://ollama.com
#### List installed models:
```
ollama list
```
#### Ensure ```gemma3:4b``` is installed
### Running the CLI Demo
```python src/demo_prompt_cli.py```
#### This script reads messages from the dataset and generates predictions using the Gemma3:4B model.
#### Currently, LoRA fine-tuning or model training is not implemented

## Dataset Format
### Datasets should be in JSONL format and include the following fields:
```
{
  "instruction": "Analyze this message and predict user reactions.",
  "input": "Message text",
  "output": {
    "top_reactions": ["🤣", "👎", "👍"],
    "reasoning": "Explanation of the prediction"
  }
}
```
## Next Steps
- Test Hugging Face version of Gemma3-4B and implement lightweight LoRA fine-tuning
- Build a web or API interface for prompt-based responses
- Improve CLI to handle Ollama errors and unknown flags gracefully
