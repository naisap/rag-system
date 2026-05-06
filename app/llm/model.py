# app/llm/model.py

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from langchain_core.runnables import RunnableLambda

def load_llm():
    model_name = "google/flan-t5-base"

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    def generate_text(inputs):
        prompt = inputs["text"] if "text" in inputs else str(inputs)

        tokenized = tokenizer(prompt, return_tensors="pt", truncation=True)
        outputs = model.generate(**tokenized, max_new_tokens=128)

        return tokenizer.decode(outputs[0], skip_special_tokens=True)

    return RunnableLambda(generate_text)