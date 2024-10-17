from transformers import BertTokenizer, BertForSequenceClassification
import torch

# Load the model and tokenizer from the results folder
model = BertForSequenceClassification.from_pretrained("./results")
tokenizer = BertTokenizer.from_pretrained("./results")

# Test sentence for prediction
test_sentence = "Prodej bytu 2+kk v Praze 3 o velikosti 44m² za 10 milionů korun"

# Tokenize the input sentence
inputs = tokenizer(test_sentence, return_tensors="pt", truncation=True, padding=True)

# Get model predictions
with torch.no_grad():
    outputs = model(**inputs)

# Extract the predicted class
predictions = torch.argmax(outputs.logits, dim=-1).item()

print(f"Predicted class: {predictions}")
