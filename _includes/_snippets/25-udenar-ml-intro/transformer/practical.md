<!-- NOTEBOOK: -->

# Practical Introduction

In this practical session, we will explore transformer architectures and work with Large Language Models (LLMs). We'll use pre-trained models, and learn about fine-tuning, RAG, and prompting techniques.

---

## Exercise 1: Working with Pre-trained Language Models

In this exercise, we'll use the [Hugging Face Transformers library](https://pypi.org/project/transformers/) to work with pre-trained language models. Hugging Face is a company that provides open-source tools and models for natural language processing tasks. This library offers a complete set of functions that we can use to download and manipulate pre-trained language models. You can explore [its documentation](https://huggingface.co/docs/transformers/en/index) to know it better and implement your ideas. 

```python
from transformers import AutoTokenizer, AutoModel, pipeline
import pandas as pd
```

Let's load a pre-trained model and tokenizer. We will use a small model called ["distilbert-base-uncased"](https://huggingface.co/distilbert/distilbert-base-uncased). This model has 64M of parameters and is a distilled version of BERT. [Hugging Face](https://huggingface.co/) offers a complete documentation of the models for developers to explore and use:

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

## Exercise 2: Comparing Fine-tuned vs Zero-shot Transformer Classification

In this exercise, we'll compare two approaches for sentiment analysis using transformers: fine-tuning a model on our dataset and using zero-shot inference with a pre-trained model.

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
# Split the dataset properly for HuggingFace datasets
train_testvalid = tokenized_dataset.train_test_split(test_size=0.3, seed=42)
train_dataset = train_testvalid['train']
eval_dataset = train_testvalid['test']
# Training arguments
training_args = TrainingArguments(
    output_dir="./results",
    learning_rate=2e-5,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=3,
    weight_decay=0.01,
    eval_strategy="epoch",
    save_strategy="epoch",
    load_best_model_at_end=True,
    report_to=[],
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

Once the model is trained, we can evaluate its performance. We create a wrapper function that calls the model with our inputs, and process the output of the model. In this case, we apply a softmax function to get the probability distribution of the output `logits`, then we get the predicted_class by selecting the one with higher probability value, and also get the confidence of the prediction:

```python
# Evaluate the model
eval_results = trainer.evaluate()
print(f"Evaluation results: {eval_results}")
# Use the trained model for predictions
def predict_sentiment(text, model, tokenizer):
    """Predict sentiment and return probability distribution."""
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=128)
    
    with torch.no_grad():
        outputs = model(**inputs)
        probabilities = torch.nn.functional.softmax(outputs.logits, dim=-1)
        predicted_class = torch.argmax(probabilities, dim=1).item()
        confidence = probabilities[0][predicted_class].item()
    
    sentiment = "positive" if predicted_class == 1 else "negative"
    return sentiment, confidence, probabilities[0].numpy()
# Test the model with new examples
test_texts = [
    "This movie was absolutely fantastic!",
    "I really didn't enjoy this film at all.",
    "The acting was mediocre but the story was interesting.",
    "Outstanding performance by all the actors!"
]
print("\n--- Model Predictions ---")
results = []
for text in test_texts:
    sentiment, confidence = predict_sentiment(text, model, tokenizer)
    print(f"Text: '{text}'")
    print(f"Predicted sentiment: {sentiment} (confidence: {confidence:.3f})")
    print()
    results.append({
        'text': text,
        'sentiment': sentiment,
        'confidence': confidence,
        'probabilities': probs
    })
```

We can also visualise the results for analysis:

```python
# Create visualizations
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
# Plot 1: Confidence scores
confidences = [r['confidence'] for r in results]
sentiments = [r['sentiment'] for r in results]
colors = ['green' if s == 'positive' else 'red' for s in sentiments]
ax1.bar(range(len(confidences)), confidences, color=colors, alpha=0.7)
ax1.set_xlabel('Test Examples')
ax1.set_ylabel('Confidence Score')
ax1.set_title('Model Confidence for Each Prediction')
ax1.set_xticks(range(len(confidences)))
ax1.set_xticklabels([f'Ex {i+1}' for i in range(len(confidences))], rotation=45)
ax1.grid(True, alpha=0.3)
# Plot 2: Probability distributions
x = np.arange(len(results))
width = 0.35
negative_probs = [r['probabilities'][0] for r in results]
positive_probs = [r['probabilities'][1] for r in results]
ax2.bar(x - width/2, negative_probs, width, label='Negative', color='red', alpha=0.7)
ax2.bar(x + width/2, positive_probs, width, label='Positive', color='green', alpha=0.7)
ax2.set_xlabel('Test Examples')
ax2.set_ylabel('Probability')
ax2.set_title('Probability Distribution for Each Prediction')
ax2.set_xticks(x)
ax2.set_xticklabels([f'Ex {i+1}' for i in range(len(results))], rotation=45)
ax2.legend()
ax2.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
# Print detailed probability breakdown
print("\n--- Detailed Probability Analysis ---")
for i, result in enumerate(results):
    print(f"Example {i+1}: '{result['text'][:50]}...'")
    print(f"  Negative probability: {result['probabilities'][0]:.3f}")
    print(f"  Positive probability: {result['probabilities'][1]:.3f}")
    print(f"  Predicted: {result['sentiment']} (confidence: {result['confidence']:.3f})")
    print()
# Store results for future comparison
fine_tuned_results = results.copy()
```

---

Now let's try zero-shot classification using a pre-trained model without fine-tuning. In this case, we are using the [`facebook/bart-large-mnli`](https://huggingface.co/facebook/bart-large-mnli) model, which has 407M parameters:

```python
from transformers import pipeline
# Create a zero-shot classification pipeline
zero_shot_classifier = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli",  # Good for zero-shot tasks
    device=0 if torch.cuda.is_available() else -1
)
# Define candidate labels
candidate_labels = ["positive", "negative"]
# Test the same examples with zero-shot classification
zero_shot_results = []
for text in test_texts:
    result = zero_shot_classifier(text, candidate_labels)   
    # Extract the best prediction
    predicted_label = result['labels'][0]
    confidence = result['scores'][0]
    zero_shot_results.append({
        'text': text,
        'sentiment': predicted_label,
        'confidence': confidence,
        'probabilities': result['scores']
    })
    print(f"Text: '{text}'")
    print(f"Zero-shot prediction: {predicted_label} (confidence: {confidence:.3f})")
    print()
```

We can compare the behaviour of both models as follows:

```python
# Compare the two approaches
print("=== COMPARISON: Fine-tuned vs Zero-shot ===")
print(f"{'Text':<50} {'Fine-tuned':<15} {'Zero-shot':<15}")
print("-" * 80)
for i, (fine_result, zero_result) in enumerate(zip(fine_tuned_results, zero_shot_results)):
    text_short = fine_result['text'][:45] + "..." if len(fine_result['text']) > 45 else fine_result['text']
    print(f"{text_short:<50} {fine_result['sentiment']:<15} {zero_result['sentiment']:<15}")
print("\n=== CONFIDENCE COMPARISON ===")
for i, (fine_result, zero_result) in enumerate(zip(fine_tuned_results, zero_shot_results)):
    print(f"Example {i+1}: Fine-tuned: {fine_result['confidence']:.3f}, Zero-shot: {zero_result['confidence']:.3f}")
```

---

## Exercise 3: LLM-based Sentiment Analysis

In this exercise, we'll create a generic class for interacting with Large Language Models. In this particular example, we will use Gemini but the approach should be the same for different LLMs. We start importing our relevant libraries:

```python
import google.generativeai as genai
import os
from typing import List, Dict, Any, Optional
import json
```

Then we define a class that will operate as an interface between our program and the LLM. The class will have methods to setup the connection with the LLM, create the prompt, parse the output, and send queries to the LLM.

```python
class LLMInterface:
    """Generic class for interacting with Large Language Models."""
    
    def __init__(self, api_key: str, model_name: str = "gemini-pro"):
        """
        Initialize the LLM interface.
        
        Args:
            api_key: API key for the LLM service
            model_name: Name of the model to use
        """
        self.api_key = api_key
        self.model_name = model_name
        self.client = None
        self._setup_client()
    
    def _setup_client(self):
        """Setup the client for the specific LLM service."""
        try:
            genai.configure(api_key=self.api_key)
            self.client = genai.GenerativeModel(self.model_name)
            print(f"Successfully connected to {self.model_name}")
        except Exception as e:
            print(f"Error setting up client: {e}")
            self.client = None
    
    def create_prompt(self, task: str, context: str = "", examples: Optional[List[Dict]] = None) -> str:
        """
        Create a structured prompt for a given task.
        
        Args:
            task: Description of the task to perform
            context: Additional context or input text
            examples: List of example input-output pairs
            
        Returns:
            Formatted prompt string
        """
        prompt = f"Task: {task}\n\n"
        
        if context:
            prompt += f"Context: {context}\n\n"
        
        if examples:
            prompt += "Examples:\n"
            for i, example in enumerate(examples, 1):
                prompt += f"{i}. Input: {example['input']}\n"
                prompt += f"   Output: {example['output']}\n\n"
        
        prompt += "Your response:"
        return prompt
    
    def query(self, prompt: str) -> Dict[str, Any]:
        """
        Send a query to the LLM and get a response.
        
        Args:
            prompt: The prompt to send to the LLM
            
        Returns:
            Raw response from the LLM
        """
        if not self.client:
            return {"error": "Client not initialized"}
        
        try:
            response = self.client.generate_content(prompt)
            response_text = response.text
            return {"response": response_text, "error": None}
        except Exception as e:
            return {"error": str(e), "response": None}
```

Now let's create independent domain-specific functions. The first function will parase the response we get from the LLM following the sentiment analysis logic:

```python
def parse_sentiment_response(response: str) -> Dict[str, Any]:
    """
    Parse sentiment analysis response from LLM.
    
    Args:
        response: Raw response from the LLM
        
    Returns:
        Parsed sentiment analysis results
    """
    try:
        response_lower = response.lower().strip()
        if "positive" in response_lower:
            sentiment = "positive"
            confidence = 0.8  # Default confidence for LLM responses
        elif "negative" in response_lower:
            sentiment = "negative"
            confidence = 0.8
        else:
            sentiment = "neutral"
            confidence = 0.5
        
        return {
            "sentiment": sentiment,
            "confidence": confidence,
            "raw_response": response
        }
    except Exception as e:
        return {"error": str(e), "raw_response": response}
```

The second function will perform the sentiment analysis task using the LLM interface class:

```python
def perform_sentiment_analysis(llm_interface: LLMInterface, text: str) -> Dict[str, Any]:
    """
    Perform sentiment analysis using the LLM interface.
    
    Args:
        llm_interface: Initialized LLM interface
        text: Text to analyze
        
    Returns:
        Sentiment analysis results
    """
    task = "Analyze the sentiment of the following text. Respond with 'positive', 'negative', or 'neutral'."
    examples = [
        {"input": "I love this movie!", "output": "positive"},
        {"input": "This is terrible.", "output": "negative"},
        {"input": "The weather is okay.", "output": "neutral"}
    ]
    
    prompt = llm_interface.create_prompt(task, context=text, examples=examples)
    raw_response = llm_interface.query(prompt)
    
    if raw_response.get("error"):
        return {"error": raw_response["error"]}
    return parse_sentiment_response(raw_response["response"])
```

We can now use the sentiment analysis function for our analysis. For using the LLM, you will need to get an `API-KEY` from the provider first. Follow the next steps to get your own `API-KEY`:

1. Go to Google AI Studio: https://makersuite.google.com/app/apikey
2. Sign in with your Google account
3. Click 'Create API Key'
4. Copy the generated API key"
5. Use it in the code below


```python
# Initialize the LLM interface with your API key
# Replace 'your-api-key-here' with your actual Gemini API key
api_key = "your-api-key-here"  # Replace this with your actual API key
# Create the interface
llm_interface = LLMInterface(api_key=api_key)
# Test the LLM interface with sentiment analysis
print("=== LLM-based Sentiment Analysis ===")
# Run sentiment analysis on test examples
gemini_results = []
for text in test_texts:
    result = perform_sentiment_analysis(llm_interface, text)
    gemini_results.append({
        'text': text,
        'sentiment': result.get('sentiment', 'unknown'),
        'confidence': result.get('confidence', 0.0),
        'raw_response': result.get('raw_response', '')
    })
    print(f"Text: '{text}'")
    print(f"Gemini prediction: {result.get('sentiment', 'unknown')} (confidence: {result.get('confidence', 0.0):.3f})")
    print(f"Raw response: {result.get('raw_response', '')}")
    print()
print("Note: If you get an error, make sure:")
print("1. You have a valid Gemini API key")
print("2. You have an internet connection")
print("3. The API key is correctly copied (no extra spaces)")
```

---

Let's compare all three approaches:

```python
# Function to compare all approaches
def compare_all_approaches(fine_tuned_results, zero_shot_results, gemini_results=None):
    """Compare results from all three approaches."""
    
    print("=== COMPREHENSIVE COMPARISON ===")
    print(f"{'Text':<40} {'Fine-tuned':<12} {'Zero-shot':<12} {'Gemini':<12}")
    print("-" * 80)
    
    for i, (fine_result, zero_result) in enumerate(zip(fine_tuned_results, zero_shot_results)):
        text_short = fine_result['text'][:35] + "..." if len(fine_result['text']) > 35 else fine_result['text']
        gemini_sentiment = gemini_results[i]['sentiment'] if gemini_results else "N/A"
        
        print(f"{text_short:<40} {fine_result['sentiment']:<12} {zero_result['sentiment']:<12} {gemini_sentiment:<12}")
    
    # Calculate agreement statistics
    agreements = []
    for i, (fine_result, zero_result) in enumerate(zip(fine_tuned_results, zero_shot_results)):
        agreement = fine_result['sentiment'] == zero_result['sentiment']
        agreements.append(agreement)
    
    agreement_rate = sum(agreements) / len(agreements)
    print(f"\nAgreement between Fine-tuned and Zero-shot: {agreement_rate:.2%}")
    
    # Confidence analysis
    print("\n=== CONFIDENCE ANALYSIS ===")
    fine_avg_conf = sum(r['confidence'] for r in fine_tuned_results) / len(fine_tuned_results)
    zero_avg_conf = sum(r['confidence'] for r in zero_shot_results) / len(zero_shot_results)
    
    print(f"Average confidence - Fine-tuned: {fine_avg_conf:.3f}")
    print(f"Average confidence - Zero-shot: {zero_avg_conf:.3f}")
    
    if gemini_results:
        gemini_avg_conf = sum(r['confidence'] for r in gemini_results) / len(gemini_results)
        print(f"Average confidence - Gemini: {gemini_avg_conf:.3f}")
# Run the comparison
compare_all_approaches(fine_tuned_results, zero_shot_results, gemini_results)
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