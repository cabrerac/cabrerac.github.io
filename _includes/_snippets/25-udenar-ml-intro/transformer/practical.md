<!-- NOTEBOOK: -->

# Practical Introduction

In this practical session, we will explore transformer architectures and work with Large Language Models (LLMs). We'll use pre-trained models, and learn about fine-tuning, prompting, and RAG.

---

## Exercise 1: Working with Pre-trained Language Models

In this exercise, we'll use the [Hugging Face Transformers library](https://pypi.org/project/transformers/) to work with pre-trained language models. Hugging Face is a company that provides open-source tools and models for natural language processing tasks. This library offers a complete set of functions that we can use to download and manipulate pre-trained language models. You can explore [its documentation](https://huggingface.co/docs/transformers/en/index) to know it better and implement your ideas. 

```python
from transformers import AutoTokenizer, AutoModel, pipeline
import pandas as pd
import torch
import matplotlib.pyplot as plt
import numpy as np
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
    sentiment, confidence, probs = predict_sentiment(text, model, tokenizer)
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
    
    def __init__(self, api_key: str, model_name: str = "gemini-2.0-flash"):
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
```

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

## Exercise 4: Retrieval-Augmented Generation (RAG)

In this exercise, we'll implement a simple RAG system that combines document retrieval with LLM generation. RAG enhances LLM responses by providing relevant context from a knowledge base.

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
```

We started by importing the required libraries and now we can implement our RAG pipeline.

```python
class SimpleRAGSystem:
    """A simple RAG system using TF-IDF for retrieval and Gemini for generation."""
    
    def __init__(self, llm_interface: LLMInterface, documents: List[str]):
        """
        Initialize the RAG system.
        
        Args:
            llm_interface: Initialized LLM interface
            documents: List of documents to use as knowledge base
        """
        self.llm_interface = llm_interface
        self.documents = documents
        self.vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
        self.document_vectors = None
        self._build_index()
    
    def _build_index(self):
        """Build the document index using TF-IDF."""
        self.document_vectors = self.vectorizer.fit_transform(self.documents)
        print(f"Built index for {len(self.documents)} documents")
    
    def retrieve_relevant_documents(self, query: str, top_k: int = 3) -> List[str]:
        """
        Retrieve the most relevant documents for a given query.
        
        Args:
            query: The search query
            top_k: Number of top documents to retrieve
            
        Returns:
            List of relevant document texts
        """
        # Vectorize the query
        query_vector = self.vectorizer.transform([query])
        
        # Calculate similarities
        similarities = cosine_similarity(query_vector, self.document_vectors).flatten()
        
        # Get top-k document indices
        top_indices = similarities.argsort()[-top_k:][::-1]
        
        # Return relevant documents
        relevant_docs = [self.documents[i] for i in top_indices]
        return relevant_docs
    
    def generate_response(self, query: str, top_k: int = 3) -> Dict[str, Any]:
        """
        Generate a response using RAG.
        
        Args:
            query: The user's question
            top_k: Number of documents to retrieve
            
        Returns:
            Generated response with context
        """
        # Retrieve relevant documents
        relevant_docs = self.retrieve_relevant_documents(query, top_k)
        
        # Create context from retrieved documents
        context = "\n\n".join(relevant_docs)
        
        # Create RAG prompt
        task = "Answer the following question based on the provided context. If the context doesn't contain enough information to answer the question, say so."
        examples = [
            {
                "input": "What is machine learning?",
                "output": "Machine learning is a subset of artificial intelligence that enables computers to learn and make decisions from data without being explicitly programmed."
            }
        ]
        
        prompt = self.llm_interface.create_prompt(
            task=task,
            context=f"Context:\n{context}\n\nQuestion: {query}",
            examples=examples
        )
        
        # Generate response
        result = self.llm_interface.query(prompt)
        
        if result.get("error"):
            return {"error": result["error"]}
        
        return {
            "response": result["response"],
            "context": context,
            "relevant_docs": relevant_docs
        }
```

We need to create a knowledge base that drives the LLM responses.

```python
# Create a sample knowledge base about AI and machine learning
knowledge_base = [
    "Machine learning is a subset of artificial intelligence that enables computers to learn and make decisions from data without being explicitly programmed. It uses algorithms to identify patterns in data and make predictions or decisions.",
    
    "Deep learning is a subset of machine learning that uses neural networks with multiple layers to model and understand complex patterns. It has been particularly successful in image recognition, natural language processing, and speech recognition.",
    
    "Natural Language Processing (NLP) is a field of AI that focuses on the interaction between computers and human language. It includes tasks like text classification, sentiment analysis, machine translation, and question answering.",
    
    "Transformers are a type of neural network architecture that revolutionized NLP. They use attention mechanisms to process sequences of data and have become the foundation for models like BERT, GPT, and T5.",
    
    "Retrieval-Augmented Generation (RAG) is a technique that combines information retrieval with text generation. It retrieves relevant documents from a knowledge base and uses them as context for generating more accurate and informative responses.",
    
    "Fine-tuning is a process where a pre-trained model is further trained on a specific dataset for a particular task. This allows the model to adapt its knowledge to specific domains or applications.",
    
    "Zero-shot learning refers to the ability of a model to perform a task without having been specifically trained on examples of that task. Modern language models can often perform new tasks based on their pre-trained knowledge.",
    
    "Attention mechanisms allow neural networks to focus on different parts of the input when processing information. This is particularly useful in tasks like machine translation where different words in the source sentence are relevant to different words in the target sentence."
]
```

With all in place, we can now instantiate and use our RAG system.

```python
# Initialize the RAG system
rag_system = SimpleRAGSystem(llm_interface, knowledge_base)
# Test the RAG system with different questions
test_questions = [
    "What is machine learning?",
    "How do transformers work?",
    "What is the difference between deep learning and machine learning?",
    "How does RAG improve language model responses?",
    "What are attention mechanisms used for?"
]
print("=== RAG SYSTEM TESTING ===")
for question in test_questions:
    print(f"\nQuestion: {question}")
    result = rag_system.generate_response(question)   
    if result.get("error"):
        print(f"Error: {result['error']}")
    else:
        print(f"Answer: {result['response']}")
        print(f"Retrieved {len(result['relevant_docs'])} relevant documents")
        print("-" * 50)
# Demonstrate the retrieval process
print("\n=== DOCUMENT RETRIEVAL DEMONSTRATION ===")
query = "What is deep learning?"
relevant_docs = rag_system.retrieve_relevant_documents(query, top_k=2)
print(f"Query: {query}")
print(f"Retrieved {len(relevant_docs)} documents:")
for i, doc in enumerate(relevant_docs, 1):
    print(f"{i}. {doc[:100]}...")
```

---

---

## Exercise 5: LLM-based Agent for CartPole

In this exercise, we'll create an LLM-based agent to solve the [CartPole environment](https://gymnasium.farama.org/environments/classic_control/cart_pole/) from Gymnasium. CartPole is a classic control problem where we need to balance a pole on a moving cart by applying left or right forces.

```python
import gymnasium as gym
import numpy as np
from typing import Dict, Any, List
```

We implement a class that interacts with the CartPole environment:

```python
class LLMCartPoleAgent:
    """An LLM-based agent for solving the CartPole environment."""
    
    def __init__(self, llm_interface: LLMInterface):
        """
        Initialize the LLM agent.
        
        Args:
            llm_interface: Initialized LLM interface
        """
        self.llm_interface = llm_interface
        self.env = None
        self.episode_history = []
        
    def _create_observation_description(self, observation: np.ndarray) -> str:
        """
        Convert numerical observation to natural language description.
        
        Args:
            observation: Environment observation [cart_position, cart_velocity, pole_angle, pole_angular_velocity]
            
        Returns:
            Natural language description of the current state
        """
        cart_pos, cart_vel, pole_angle, pole_ang_vel = observation
        
        # Convert to degrees for easier understanding
        pole_angle_deg = np.degrees(pole_angle)
        
        description = f"""
Current CartPole State:
- Cart position: {cart_pos:.3f} (negative = left, positive = right)
- Cart velocity: {cart_vel:.3f} (negative = moving left, positive = moving right)
- Pole angle: {pole_angle_deg:.1f} degrees (negative = leaning left, positive = leaning right)
- Pole angular velocity: {pole_ang_vel:.3f} (negative = rotating left, positive = rotating right)
"""
        return description
    
    def _create_action_prompt(self, observation: np.ndarray, step_count: int) -> str:
        """
        Create a prompt for the LLM to decide the next action.
        
        Args:
            observation: Current environment observation
            step_count: Current step number in the episode
            
        Returns:
            Formatted prompt for action decision
        """
        state_description = self._create_observation_description(observation)
        
        task = f"""You are controlling a CartPole system. Your goal is to keep the pole balanced upright for as long as possible.

You can take one of two actions:
- Action 0: Push the cart LEFT
- Action 1: Push the cart RIGHT

Current step: {step_count}

{state_description}

Based on the current state, what action should you take to keep the pole balanced? Consider:
1. If the pole is leaning left, you might want to move the cart left to bring it back to center
2. If the pole is leaning right, you might want to move the cart right
3. Also consider the cart's current velocity and the pole's angular velocity

Respond with only the action number (0 or 1)."""

        return task
    
    def get_action(self, observation: np.ndarray, step_count: int = 0) -> int:
        """
        Get the next action from the LLM agent.
        
        Args:
            observation: Current environment observation
            step_count: Current step number
            
        Returns:
            Action to take (0 or 1)
        """
        prompt = self._create_action_prompt(observation, step_count)
        result = self.llm_interface.query(prompt)
        
        if result.get("error"):
            print(f"LLM Error: {result['error']}, using random action")
            return np.random.randint(0, 2)
        
        # Parse the response to extract the action
        response = result["response"].strip().lower()
        
        # Try to extract action from response
        if "0" in response or "left" in response or "push left" in response:
            return 0
        elif "1" in response or "right" in response or "push right" in response:
            return 1
        else:
            # Fallback to random action if response is unclear
            print(f"Unclear response: '{response}', using random action")
            return np.random.randint(0, 2)
    
    def run_episode(self, max_steps: int = 500, render: bool = False) -> Dict[str, Any]:
        """
        Run a single episode with the LLM agent.
        
        Args:
            max_steps: Maximum number of steps per episode
            render: Whether to render the environment
            
        Returns:
            Episode results
        """
        # Create environment
        render_mode = "human" if render else None
        self.env = gym.make("CartPole-v1", render_mode=render_mode)
        
        observation, info = self.env.reset(seed=42)
        total_reward = 0
        step_count = 0
        episode_history = []
        
        print(f"Starting CartPole episode (max {max_steps} steps)...")
        
        for step in range(max_steps):
            # Get action from LLM
            action = self.get_action(observation, step_count)
            
            # Take action in environment
            next_observation, reward, terminated, truncated, info = self.env.step(action)
            
            # Record step
            episode_history.append({
                'step': step_count,
                'observation': observation.copy(),
                'action': action,
                'reward': reward,
                'terminated': terminated,
                'truncated': truncated
            })
            
            total_reward += reward
            observation = next_observation
            step_count += 1
            
            # Check if episode ended
            if terminated or truncated:
                break
        
        self.env.close()
        
        result = {
            'total_reward': total_reward,
            'steps': step_count,
            'episode_history': episode_history,
            'success': step_count >= 195  # CartPole is considered solved at 195 steps
        }
        
        print(f"Episode finished: {step_count} steps, total reward: {total_reward}")
        print(f"Success: {result['success']}")
        
        return result
    
    def run_multiple_episodes(self, num_episodes: int = 5) -> List[Dict[str, Any]]:
        """
        Run multiple episodes and collect statistics.
        
        Args:
            num_episodes: Number of episodes to run
            
        Returns:
            List of episode results
        """
        results = []
        
        for episode in range(num_episodes):
            print(f"\n=== Episode {episode + 1}/{num_episodes} ===")
            result = self.run_episode(max_steps=500, render=False)
            results.append(result)
        
        # Calculate statistics
        total_rewards = [r['total_reward'] for r in results]
        steps = [r['steps'] for r in results]
        successes = [r['success'] for r in results]
        
        print(f"\n=== SUMMARY STATISTICS ===")
        print(f"Average reward: {np.mean(total_rewards):.2f} ± {np.std(total_rewards):.2f}")
        print(f"Average steps: {np.mean(steps):.2f} ± {np.std(steps):.2f}")
        print(f"Success rate: {np.mean(successes):.2%} ({sum(successes)}/{len(successes)})")
        print(f"Best episode: {max(total_rewards)} steps")
        print(f"Worst episode: {min(total_rewards)} steps")
        
        return results
```

We can test our LLM agent now:

```python
# Test the LLM agent on CartPole
print("=== LLM AGENT FOR CARTPOLE ===")
# Create the agent
llm_agent = LLMCartPoleAgent(llm_interface)
# Run multiple episodes
episode_results = llm_agent.run_multiple_episodes(num_episodes=3)
# Visualize results
import matplotlib.pyplot as plt
# Plot reward progression
plt.figure(figsize=(12, 4))
plt.subplot(1, 2, 1)
rewards = [r['total_reward'] for r in episode_results]
plt.bar(range(1, len(rewards) + 1), rewards)
plt.xlabel('Episode')
plt.ylabel('Total Reward')
plt.title('LLM Agent Performance')
plt.axhline(y=195, color='r', linestyle='--', label='Success Threshold')
plt.legend()
plt.subplot(1, 2, 2)
steps = [r['steps'] for r in episode_results]
plt.bar(range(1, len(steps) + 1), steps)
plt.xlabel('Episode')
plt.ylabel('Steps')
plt.title('Steps per Episode')
plt.axhline(y=195, color='r', linestyle='--', label='Success Threshold')
plt.legend()
plt.tight_layout()
plt.show()
# Analyze action patterns
print("\n=== ACTION ANALYSIS ===")
all_actions = []
for episode in episode_results:
    actions = [step['action'] for step in episode['episode_history']]
    all_actions.extend(actions)
action_counts = np.bincount(all_actions)
print(f"Action 0 (LEFT): {action_counts[0]} times ({action_counts[0]/len(all_actions):.1%})")
print(f"Action 1 (RIGHT): {action_counts[1]} times ({action_counts[1]/len(all_actions):.1%})")
```

---

## Homework - Reinforcement Learning Algorithm Implementation

The assignment focuses on extending the previous homework for session 8 on Reinforcement Learning to implement an LLM-based agent to solve the same problem. Your previous task was exploring the environments in the [Gymnasium platform](https://gymnasium.farama.org/) and solving a particular one with Reinforcement Learning. This time you will solve the same problem with a LLM-agent. Ideally, you can report a comparison of both approaches.

### Submission Guidelines

- Submit your solution as a Jupyter notebook with the following name format: `transformers_session_9_<email_username>.ipynb`
- Include clear comments explaining your code and design decisions
- Provide comprehensive analysis of your results
- Document any challenges faced and how you overcame them
- Include visualisations and comparisons of your results and model performance
- Due date: 17/07/2025

<DESCRIBE YOUR SOLUTION HERE>

```python
# Write your implementation here
```

<!-- end NOTEBOOK: --> 