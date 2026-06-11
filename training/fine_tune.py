import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
from datasets import Dataset

# 1. Load Dataset
data = {
    "text": [
        "Either party may terminate this agreement with 30 days notice.",
        "The receiving party shall hold the information in strict confidence.",
        "Provider liability is capped at the total fees paid in the last 12 months."
    ],
    "label": [0, 1, 2] # 0: TERMINATION, 1: CONFIDENTIALITY, 2: LIABILITY
}
dataset = Dataset.from_dict(data)

# 2. Tokenization
model_name = "nlpaueb/legal-bert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)

def tokenize_function(examples):
    return tokenizer(examples["text"], padding="max_length", truncation=True, max_length=128)

tokenized_datasets = dataset.map(tokenize_function, batched=True)

# 3. Model Initialization
model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=3)

# 4. Training Arguments
training_args = TrainingArguments(
    output_dir="./results",
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=8,
    num_train_epochs=3,
    weight_decay=0.01,
)

# 5. Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets,
    eval_dataset=tokenized_datasets,
)

if __name__ == "__main__":
    print("Starting Fine-tuning process...")
    trainer.train()
    model.save_pretrained("./fine_tuned_legal_bert")
    tokenizer.save_pretrained("./fine_tuned_legal_bert")
    print("Model saved successfully.")
