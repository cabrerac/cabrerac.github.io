<!-- SLIDES: -->

## Large Language Models (LLMs)

## Large Language Models (LLMs)

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
            <p>Large Language Models (LLMs) are AI models designed to <em>understand, generate, and manipulate human language</em>. They are built using deep learning techniques and are usually based on the Transfomer architecture and are trained on <b>vast amounts of data</b> to capture human language complexity. LLMs can perform a wide range of language tasks (e.g., text generation, classification, etc.).</p>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->

{% include _snippets/timelines/ai-history-2001-today.md %}

<!-- SLIDES: -->

## Large Language Models (LLMs)

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="https://upload.wikimedia.org/wikipedia/commons/3/34/Transformer%2C_full_architecture.png" alt="Transformer Architecture" style="max-width: 100%; height: auto;">
                <div class="footnote">Transformer Architecture - dvgodoy, CC BY 4.0 <https://creativecommons.org/licenses/by/4.0>, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## Large Language Models (LLMs)

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <ul>
                    <li><b>GPT-3:</b> Known for generating human-like text, it can perform tasks such as translation, question answering, and text completion.</li>
                    <li><b>BERT:</b> Excels in understanding the context of words in a sentence, making it ideal for tasks like sentiment analysis and named entity recognition.</li>
                    <li><b>T5 (Text-to-Text Transfer Transformer):</b> Converts all NLP tasks into a text-to-text format, enabling it to handle tasks like summarization and translation.</li>
                    <li><b>RoBERTa:</b> An optimized version of BERT, it improves performance on tasks like text classification and language inference.</li>
                    <li>...</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="https://upload.wikimedia.org/wikipedia/commons/3/34/Transformer%2C_full_architecture.png" alt="Transformer Architecture" style="max-width: 100%; height: auto;">
                <div class="footnote">Transformer Architecture - dvgodoy, CC BY 4.0 <https://creativecommons.org/licenses/by/4.0>, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## Large Language Models (LLMs)

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <img class="external-svg" src="https://upload.wikimedia.org/wikipedia/commons/0/06/Large-scale_AI_training_compute_%28FLOP%29_vs_Publication_date_%282017-2024%29.svg" alt="Training FLOP" style="max-width: 80%; height: auto;">
                <div class="footnote">Large-Scale AI Models Training - Epoch AI, CC BY 4.0 <https://creativecommons.org/licenses/by/4.0>, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## Large Language Models (LLMs)

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <img class="external-svg" src="https://upload.wikimedia.org/wikipedia/commons/6/64/Estimated_training_cost_of_some_AI_models_-_2024_AI_index.jpg" alt="Training Cost" style="max-width: 80%; height: auto;">
                <div class="footnote">Estimated Cost - Stanford Institute for Human-Centered Artificial Intelligence (permission obtained by email from the AI index research manager), CC BY-SA 4.0 <https://creativecommons.org/licenses/by-sa/4.0>, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## Large Language Models (LLMs)

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
            <p><b>Fine tuning</b> continues the training of a pre-trained LLM (e.g., GPT-3, BERT, etc.) to perform tasks on a particular domain (e.g., healthcare).</p>
            </div>
        </div>
    </div>
</div>

## Large Language Models (LLMs)

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/diagrams/fine-tuning-process.svg" alt="Fine Tuning Process" style="height: 500px">
                <div class="footnote">Fine Tuning Process</div>
            </div>
        </div>
    </div>
</div>

## Large Language Models (LLMs)

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>It is similar to a neural network training:</p>
                <ol>
                    <li><b>Data Collection:</b> Gather a large and relevant dataset for the specific domain or task.</li>
                    <li><b>Preprocessing:</b> Clean and preprocess the data to ensure it is in a suitable format for training.</li>
                    <li><b>Model Selection:</b> Choose a pre-trained LLM that is most suitable for the task at hand.</li>
                    <li><b>Supervised Learning:</b> Prompt engineering, error calculation, and adjusting weights using gradient descent and back-propagation.</li>
                    <li><b>Evaluation:</b> Assess the performance of the fine-tuned model using appropriate metrics and validation datasets.</li>
                    <li><b>Deployment:</b> Deploy the fine-tuned model for use in real-world applications.</li>
                </ol>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/diagrams/fine-tuning-process.svg" alt="Fine Tuning Process" style="height: 500px">
                <div class="footnote">Fine Tuning Process</div>
            </div>
        </div>
    </div>
</div>

## Large Language Models (LLMs)

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>It is similar to a neural network training:</p>
                <ol>
                    <li><b>Data Collection:</b> Gather a large and relevant dataset for the specific domain or task.</li>
                    <li><b>Preprocessing:</b> Clean and preprocess the data to ensure it is in a suitable format for training.</li>
                    <li><b>Model Selection:</b> Choose a pre-trained LLM that is most suitable for the task at hand.</li>
                    <li><b>Supervised Learning:</b> Prompt engineering, error calculation, and adjusting weights using gradient descent and back-propagation.</li>
                    <li><b>Evaluation:</b> Assess the performance of the fine-tuned model using appropriate metrics and validation datasets.</li>
                    <li><b>Deployment:</b> Deploy the fine-tuned model for use in real-world applications.</li>
                </ol>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/data-science-process.png" alt="Data Science Process" style="height: 500px">
                <div class="footnote">Data Science Process</div>
            </div>
        </div>
    </div>
</div>

## Large Language Models (LLMs)

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 95%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <img src="{{ site.url }}/assets/media/diagrams/data-assess-pipeline.svg" alt="Data Assess Pipeline" style="height: 500px">
            </div>
        </div>
    </div>
</div>

## Large Language Models (LLMs)

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <ul>
                    <li><b>Dataset Size:</b> Typically requires tens of gigabytes to terabytes of data.</li>
                    <li><b>RAM:</b> Depends on the model size (i.e., number of parameters). At least 64GB or 128GB of RAM.</li>
                    <li><b>GPU:</b> High-performance GPUs such as NVIDIA A100 or V100 for faster training times.</li>
                    <li><b>CPU:</b> Multi-core processors, ideally with 16 cores or more, to handle data preprocessing and other tasks.</li>
                    <li><b>Disk Space:</b> Sufficient storage, often in the range of several terabytes, to accommodate datasets and model checkpoints.</li>
                    <li><b>Network Bandwidth:</b> High-speed internet connection for downloading datasets and model updates.</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/diagrams/fine-tuning-process.svg" alt="Fine Tuning Process" style="height: 500px">
                <div class="footnote">Fine Tuning Process</div>
            </div>
        </div>
    </div>
</div>

## Large Language Models (LLMs)

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
            <p><b>Retrieval-Augmented Generation (RAG)</b> is an alternative to fine-tuning that combines pre-trained LLMs with external knowledge sources. Instead of adapting the model to a specific domain, RAG retrieves relevant information from a database or knowledge base to enhance the model's responses in real-time.</p>
            </div>
        </div>
    </div>
</div>

## Large Language Models (LLMs)

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>The process combines approaches from symbolic AI and databases:</p>
                <ol>
                    <li><b>Data Collection:</b> Gather a knowledge base that the RAG system can query.</li>
                    <li><b>Preprocessing:</b> Organize the knowledge base to ensure efficient retrieval and LLM integration.</li>
                    <li><b>Model Selection:</b> Choose a pre-trained LLM that can integrate with the retrieval system.</li>
                    <li><b>Retrieval Integration:</b> Using the knowledge base and the LLM in response to queries.</li>
                    <li><b>Evaluation:</b> Assessing the performance of the RAG system by using appropriate metrics.</li>
                    <li><b>Deployment:</b> Deploy the RAG system for real-time applications, ensuring it can access and retrieve information efficiently.</li>
                </ol>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/diagrams/rag-process.svg" alt="RAG Process" style="height: 500px">
                <div class="footnote">RAG Process</div>
            </div>
        </div>
    </div>
</div>

## Large Language Models (LLMs)

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>The process combines approaches from symbolic AI and databases:</p>
                <ol>
                    <li><b>Data Collection:</b> Gather a knowledge base that the RAG system can query.</li>
                    <li><b>Preprocessing:</b> Organize the knowledge base to ensure efficient retrieval and LLM integration.</li>
                    <li><b>Model Selection:</b> Choose a pre-trained LLM that can integrate with the retrieval system.</li>
                    <li><b>Retrieval Integration:</b> Using the knowledge base and the LLM in response to queries.</li>
                    <li><b>Evaluation:</b> Assessing the performance of the RAG system by using appropriate metrics.</li>
                    <li><b>Deployment:</b> Deploy the RAG system for real-time applications, ensuring it can access and retrieve information efficiently.</li>
                </ol>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/data-science-process.png" alt="Data Science Process" style="height: 500px">
                <div class="footnote">Data Science Process</div>
            </div>
        </div>
    </div>
</div>

## Large Language Models (LLMs)

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 95%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <img src="{{ site.url }}/assets/media/diagrams/data-assess-pipeline.svg" alt="Data Assess Pipeline" style="height: 500px">
            </div>
        </div>
    </div>
</div>

## Large Language Models (LLMs)

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <ul>
                    <li><b>Knowledge Base Size:</b> A comprehensive knowledge base can range from several gigabytes to terabytes.</li>
                    <li><b>RAM:</b> A minimum of 64GB is recommended to facilitate retrieval operations.</li>
                    <li><b>GPU:</b> Mid-range GPUs can suffice, but high-performance options like NVIDIA A100 can enhance performance.</li>
                    <li><b>CPU:</b> Multi-core processors for managing data preprocessing and retrieval tasks.</li>
                    <li><b>Disk Space:</b> Several terabytes may be necessary, depending on the data volume.</li>
                    <li><b>Network Bandwidth:</b> A high-speed internet connection for accessing external data sources and updating the knowledge base as needed.</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/diagrams/rag-process.svg" alt="RAG Process" style="height: 500px">
                <div class="footnote">RAG Process</div>
            </div>
        </div>
    </div>
</div>

## Large Language Models (LLMs)

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
            <p><b>Prompt Engineering</b> is a lightweight alternative to fine-tuning and RAG. Instead of changing model weights or building a retrieval pipeline, we craft <em>instructions, examples, and constraints</em> (the “prompt”) so that a frozen LLM performs the desired task.</p>
            </div>
        </div>
    </div>
</div>

## Large Language Models (LLMs)

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>Typical prompt-engineering workflow:</p>
                <ol>
                    <li><b>Task definition:</b> Specify what output format and style you need.</li>
                    <li><b>Baseline prompt:</b> Write a clear instruction (zero-shot) or add 1-5 examples (few-shot).</li>
                    <li><b>Iterate &amp; test:</b> Evaluate outputs, add system messages, or reorder examples to reduce errors &amp; bias.</li>
                    <li><b>Guardrails:</b> Include refusals, safety clauses, or value alignment statements.</li>
                    <li><b>Automation:</b> Use prompt templates or tools like LangChain/LlamaIndex to inject dynamic context.</li>
                    <li><b>Deployment:</b> Store the prompt with version control and monitor performance over time.</li>
                </ol>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/diagrams/prompt-engineering-process.svg" alt="Prompt Engineering Process" style="height: 500px">
                <div class="footnote">Prompt Engineering Process</div>
            </div>
        </div>
    </div>
</div>

## Large Language Models (LLMs)

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">

```python
expected_format = """
Return your answer in JSON with the following keys:
{
  "title": string,          # concise headline (≤ 12 words)
  "summary": [string, ...]  # 3–5 bullet points
}
"""

article = """<ARTICLE TEXT HERE>"""

prompt = f"""
You are a helpful assistant.

TASK: Summarise the article below.

OUTPUT FORMAT (baseline)
{expected_format}

ARTICLE
""" + article
```
</div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/diagrams/prompt-engineering-process.svg" alt="Prompt Engineering Process" style="height: 500px">
                <div class="footnote">Prompt Engineering Process</div>
            </div>
        </div>
    </div>
</div>

## Large Language Models (LLMs)

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">

```python
import gemini

gemini.api_key = "YOUR_API_KEY"

response = gemini.Completion.create(
    engine="gemini-001",
    prompt=prompt,
    max_tokens=150,
    temperature=0.7
)
print(response.choices[0].text.strip())
```
</div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/diagrams/prompt-engineering-process.svg" alt="Prompt Engineering Process" style="height: 500px">
                <div class="footnote">Prompt Engineering Process</div>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->

{% include _snippets/agentic-ai.md %}


<!-- SLIDES: -->

## Large Language Models (LLMs)

<!-- end SLIDES: -->

- reinforcement learning
- evaluation