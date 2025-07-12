<!-- NOTEBOOK: -->

# Practical Introduction

In this practical session, we will explore transformer architectures and work with Large Language Models (LLMs). We'll implement attention mechanisms, use pre-trained models, and learn about fine-tuning and prompting techniques.

---

## Exercise 1: Understanding Self-Attention

In this exercise, we'll implement the self-attention mechanism from scratch to understand how transformers process sequential data. Self-attention allows the model to weigh the importance of different words in a sequence when encoding a particular word.

Let's start by importing the necessary libraries:

```python
import numpy as np
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Tuple
```

We'll create a simple implementation of self-attention:

```python
def scaled_dot_product_attention(Q: torch.Tensor, K: torch.Tensor, V: torch.Tensor, mask: torch.Tensor = None) -> Tuple[torch.Tensor, torch.Tensor]:
    """
    Compute scaled dot-product attention.
    
    Args:
        Q: Query tensor of shape (batch_size, seq_len, d_k)
        K: Key tensor of shape (batch_size, seq_len, d_k)
        V: Value tensor of shape (batch_size, seq_len, d_v)
        mask: Optional mask tensor of shape (batch_size, seq_len, seq_len)
    
    Returns:
        output: Attention output tensor
        attention_weights: Attention weights tensor
    """
    d_k = Q.size(-1)
    
    # Compute attention scores
    scores = torch.matmul(Q, K.transpose(-2, -1)) / np.sqrt(d_k)
    
    # Apply mask if provided
    if mask is not None:
        scores = scores.masked_fill(mask == 0, -1e9)
    
    # Apply softmax to get attention weights
    attention_weights = F.softmax(scores, dim=-1)
    
    # Apply attention weights to values
    output = torch.matmul(attention_weights, V)
    return output, attention_weights
```

Now let's create a simple example to demonstrate self-attention:

```python
# Create a simple sequence
seq_len = 5
d_k = 8
batch_size = 1
# Create random Q, K, V matrices
Q = torch.randn(batch_size, seq_len, d_k)
K = torch.randn(batch_size, seq_len, d_k)
V = torch.randn(batch_size, seq_len, d_k)
print(f"Q shape: {Q.shape}")
print(f"K shape: {K.shape}")
print(f"V shape: {V.shape}")
# Compute attention
output, attention_weights = scaled_dot_product_attention(Q, K, V)
print(f"Output shape: {output.shape}")
print(f"Attention weights shape: {attention_weights.shape}")
```

Let's visualize the attention weights:

```python
# Plot attention weights
plt.figure(figsize=(8, 6))
attention_matrix = attention_weights[0].detach().numpy()
plt.imshow(attention_matrix, cmap='Blues', aspect='auto')
plt.colorbar()
plt.title('Self-Attention Weights')
plt.xlabel('Key Position')
plt.ylabel('Query Position')
plt.xticks(range(seq_len))
plt.yticks(range(seq_len))
plt.show()
print("Attention weights matrix:")
print(attention_matrix.round(3))
```

---

## Exercise 2: Multi-Head Attention

In this exercise, we'll implement multi-head attention, which allows the model to attend to information from different representation subspaces at different positions.

```python
class MultiHeadAttention(nn.Module):
    def __init__(self, d_model: int, num_heads: int):
        super().__init__()
        assert d_model % num_heads == 0
        
        self.d_model = d_model
        self.num_heads = num_heads
        self.d_k = d_model // num_heads
        
        # Linear layers for Q, K, V projections
        self.W_q = nn.Linear(d_model, d_model)
        self.W_k = nn.Linear(d_model, d_model)
        self.W_v = nn.Linear(d_model, d_model)
        self.W_o = nn.Linear(d_model, d_model)
        
    def split_heads(self, x: torch.Tensor) -> torch.Tensor:
        """Split the last dimension into (num_heads, d_k)."""
        batch_size, seq_len, d_model = x.size()
        return x.view(batch_size, seq_len, self.num_heads, self.d_k).transpose(1, 2)
    
    def combine_heads(self, x: torch.Tensor) -> torch.Tensor:
        """Combine the heads back into a single dimension."""
        batch_size, num_heads, seq_len, d_k = x.size()
        return x.transpose(1, 2).contiguous().view(batch_size, seq_len, self.d_model)
    
    def forward(self, Q: torch.Tensor, K: torch.Tensor, V: torch.Tensor, mask: torch.Tensor = None) -> torch.Tensor:
        batch_size = Q.size(0)
        
        # Linear transformations and split into multiple heads
        Q = self.split_heads(self.W_q(Q))  # (batch_size, num_heads, seq_len, d_k)
        K = self.split_heads(self.W_k(K))  # (batch_size, num_heads, seq_len, d_k)
        V = self.split_heads(self.W_v(V))  # (batch_size, num_heads, seq_len, d_k)
        
        # Apply attention to each head
        attention_outputs = []
        for h in range(self.num_heads):
            head_output, _ = scaled_dot_product_attention(
                Q[:, h], K[:, h], V[:, h], mask
            )
            attention_outputs.append(head_output)
        
        # Concatenate all heads
        concat_attention = torch.stack(attention_outputs, dim=1)
        
        # Combine heads and apply final linear layer
        output = self.W_o(self.combine_heads(concat_attention))      
        return output
```

Let's test our multi-head attention implementation:

```python
# Test multi-head attention
d_model = 16
num_heads = 4
seq_len = 6
# Create random input
x = torch.randn(1, seq_len, d_model)
# Create multi-head attention layer
mha = MultiHeadAttention(d_model, num_heads)
# Apply multi-head attention
output = mha(x, x, x)
print(f"Input shape: {x.shape}")
print(f"Output shape: {output.shape}")
print(f"Number of parameters: {sum(p.numel() for p in mha.parameters())}")
```

---

## Exercise 3: Working with Pre-trained Language Models

In this exercise, we'll use the Hugging Face Transformers library to work with pre-trained language models.

```python
from transformers import AutoTokenizer, AutoModel, pipeline
import pandas as pd
```

Let's load a pre-trained model and tokenizer:

```python
# Load a smaller model for demonstration
model_name = "distilbert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)
print(f"Model: {model_name}")
print(f"Vocabulary size: {tokenizer.vocab_size}")
```

Let's explore tokenization:

```python
# Example text
text = "Transformers are amazing for natural language processing!"
# Tokenize the text
tokens = tokenizer.tokenize(text)
token_ids = tokenizer.encode(text)
print(f"Original text: {text}")
print(f"Tokens: {tokens}")
print(f"Token IDs: {token_ids}")
print(f"Decoded: {tokenizer.decode(token_ids)}")
```

Let's create embeddings for a sentence:

```python
# Create embeddings
inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
with torch.no_grad():
    outputs = model(**inputs)
    embeddings = outputs.last_hidden_state
print(f"Input shape: {inputs['input_ids'].shape}")
print(f"Embedding shape: {embeddings.shape}")
print(f"Embedding for first token: {embeddings[0, 0, :10]}")  # First 10 dimensions
```

---

## Exercise 4: Text Classification with Transformers

In this exercise, we'll use a pre-trained transformer model for text classification.

```python
from transformers import AutoModelForSequenceClassification, TrainingArguments, Trainer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import datasets
```

Let's create a simple dataset for sentiment analysis:

```python
# Create a simple sentiment dataset
texts = [
    "I love this movie, it's fantastic!",
    "This is the worst film I've ever seen.",
    "The acting was amazing and the plot was engaging.",
    "Terrible acting and boring storyline.",
    "Great cinematography and excellent performances.",
    "I couldn't stand watching this movie.",
    "Absolutely brilliant film with outstanding direction.",
    "Poor script and weak character development.",
    "This movie exceeded all my expectations!",
    "A complete waste of time and money."
]
labels = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0]  # 1 for positive, 0 for negative
# Create dataset
dataset = datasets.Dataset.from_dict({
    'text': texts,
    'label': labels
})
print(f"Dataset size: {len(dataset)}")
print(f"Sample: {dataset[0]}")
```

Let's load a model for sequence classification:

```python
# Load model for sequence classification
model_name = "distilbert-base-uncased"
num_labels = 2
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=num_labels)
```

```python
# Tokenize the dataset
def tokenize_function(examples):
    return tokenizer(examples["text"], padding="max_length", truncation=True, max_length=128)
tokenized_dataset = dataset.map(tokenize_function, batched=True)
```

Let's create a simple training setup, we start by splitting our dataset and configure our training parameters:

```python
train_dataset, eval_dataset = train_test_split(tokenized_dataset, test_size=0.3, random_state=42)
# Training arguments
training_args = TrainingArguments(
    output_dir="./results",
    learning_rate=2e-5,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=3,
    weight_decay=0.01,
    evaluation_strategy="epoch",
    save_strategy="epoch",
    load_best_model_at_end=True,
)
```

We can now create our trainer and train the model with the defined parameters:

```python
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
)
# Train the model
trainer.train()
```

---

## Exercise 5: Prompt Engineering

In this exercise, we'll explore prompt engineering techniques for working with Large Language Models. We can define a function to create prompts as follows:

```python
def create_prompt(task, context, examples=None):
    """Create a structured prompt for a given task."""
    prompt = f"Task: {task}\n\n"
    
    if context:
        prompt += f"Context: {context}\n\n"
    
    if examples:
        prompt += "Examples:\n"
        for i, example in enumerate(examples, 1):
            prompt += f"{i}. {example}\n"
        prompt += "\n"
    
    prompt += "Your response:"
    return prompt
```

We can use the function to define different tasks:

```python
tasks = {
    "sentiment_analysis": "Analyse the sentiment of the following text. Respond with 'positive', 'negative', or 'neutral'.",
    "summarisation": "Summarise the following text in 2-3 sentences.",
    "translation": "Translate the following text from English to Spanish.",
    "question_answering": "Answer the following question based on the given context."
}
```

And use the prompt creator to ask for a particular task:

```python
text = "The new AI model shows remarkable improvements in accuracy and efficiency."
sentiment_prompt = create_prompt(
    task=tasks["sentiment_analysis"],
    context=text
)
print("Sentiment Analysis Prompt:")
print(sentiment_prompt)
```

Let's create a more sophisticated prompt template that includes examples to show the LLM what we expect from it:

```python
def create_few_shot_prompt(task_description, examples, query):
    """Create a few-shot learning prompt."""
    prompt = f"{task_description}\n\n"
    
    for example in examples:
        prompt += f"Input: {example['input']}\n"
        prompt += f"Output: {example['output']}\n\n"
    
    prompt += f"Input: {query}\n"
    prompt += "Output:"
    
    return prompt
```

As an example we show how to clasiffy the sentifment of movies' reviews.

```python
# Example few-shot prompt
task_desc = "Classify the sentiment of movie reviews as positive or negative."
examples = [
    {"input": "This movie was absolutely terrible.", "output": "negative"},
    {"input": "I loved every minute of this film!", "output": "positive"},
    {"input": "The acting was superb and the plot was engaging.", "output": "positive"}
]
query = "The special effects were amazing but the story was confusing."
few_shot_prompt = create_few_shot_prompt(task_desc, examples, query)
print("Few-Shot Learning Prompt:")
print(few_shot_prompt)
```

This practical session covers the fundamental concepts of transformers, from implementing attention mechanisms from scratch to working with pre-trained models and prompt engineering techniques.

<!-- end NOTEBOOK: --> 