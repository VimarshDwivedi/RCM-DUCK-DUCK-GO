from transformers import T5Tokenizer, T5ForConditionalGeneration

model_name = "google/flan-t5-base"  # Or flan-t5-large, flan-t5-xl

tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)

def get_llm_response(context, question):
    prompt = f"""Answer the question based on the context.\n\nContext: {context}\n\nQuestion: {question}\n\nAnswer:"""
    inputs = tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True)
    outputs = model.generate(**inputs, max_new_tokens=200)
    return tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
