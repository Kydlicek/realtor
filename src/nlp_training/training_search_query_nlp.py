import pandas as pd
from sklearn.preprocessing import LabelEncoder
import torch
from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments
from sklearn.model_selection import train_test_split

# Load the dataset
df = pd.read_csv('dataset_real_estate.csv')

# Handle numeric columns (replace NaN with 0 or another value)
df['velikost_m2'] = df['velikost_m2'].fillna(0)  # Fill missing size with 0
df['cena'] = df['cena'].fillna(0).astype(float)   # Convert to numeric and fill missing with 0

# Handle categorical columns (convert to string and fill with 'unknown')
df['transakce'] = df['transakce'].astype(str)
df['dispozice'] = df['dispozice'].astype(str)
df['mesto'] = df['mesto'].astype(str)

df.fillna('unknown', inplace=True)  # Fill any remaining NaNs in categorical columns

# Apply label encoding for categorical columns
label_encoders = {}
for column in ['transakce', 'dispozice', 'mesto']:
    le = LabelEncoder()
    df[column] = le.fit_transform(df[column].astype(str))  # Encode labels as integers
    label_encoders[column] = le  # Store the encoder for future use

# Preparing the text field by combining relevant columns into a natural language prompt
df['text'] = df.apply(lambda row: f"{row['transakce']} {row['dispozice']} {row['mesto']} velikost {row['velikost_m2']} cena {row['cena']}", axis=1)

# Train/test split
train_texts, val_texts, train_labels, val_labels = train_test_split(df['text'], df[['transakce', 'velikost_m2', 'dispozice', 'mesto', 'cena']], test_size=0.2)

# Load tokenizer from Hugging Face for BERT
tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased')

# Tokenize the text
train_encodings = tokenizer(train_texts.tolist(), truncation=True, padding=True)
val_encodings = tokenizer(val_texts.tolist(), truncation=True, padding=True)

# Ensure the labels are numeric and converted to tensors
train_labels = torch.tensor(train_labels.values.astype(float))
val_labels = torch.tensor(val_labels.values.astype(float))

# Define a PyTorch dataset class
class RealEstateDataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = self.labels[idx]
        return item

    def __len__(self):
        return len(self.labels)

# Create datasets for training and validation
train_dataset = RealEstateDataset(train_encodings, train_labels)
val_dataset = RealEstateDataset(val_encodings, val_labels)

# Load the BERT model
model = BertForSequenceClassification.from_pretrained('bert-base-multilingual-cased', num_labels=5)

# Define training arguments for Hugging Face Trainer
training_args = TrainingArguments(
    output_dir='./results',          # output directory
    num_train_epochs=3,              # number of training epochs
    per_device_train_batch_size=16,  # batch size for training
    per_device_eval_batch_size=64,   # batch size for evaluation
    warmup_steps=500,                # number of warmup steps for learning rate scheduler
    weight_decay=0.01,               # strength of weight decay
    logging_dir='./logs',            # directory for storing logs
    logging_steps=10,
)

# Define a Hugging Face Trainer object
trainer = Trainer(
    model=model,                         # the instantiated model to be trained
    args=training_args,                  # training arguments, defined above
    train_dataset=train_dataset,         # training dataset
    eval_dataset=val_dataset             # evaluation dataset
)

# Train the model
trainer.train()

# Evaluate the model
trainer.evaluate()

# Save the model and tokenizer
model.save_pretrained("./saved_model")
tokenizer.save_pretrained("./saved_model")
