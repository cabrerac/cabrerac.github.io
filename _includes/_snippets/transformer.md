<!-- SLIDES: -->

## The Transformer Architecture

<div class="rows" style="height: 100%">
  <div class="row" style="height: 100%">
    <div class="columns" style="width: 100%">
      <div class="column vertical-middle text-left" style="width: 100%">
        <p>The Transformer is a deep neural network architecture based on the <b>multi-head attention mechanism</b> introduced by researchers at Google (<a href="https://proceedings.neurips.cc/paper_files/paper/2017/file/
                3f5ee243547dee91fbd053c1c4a845aa-Paper.pdf">Vaswani et al., 2017</a>). The original goal was to improve machine learning translation tasks based on <b>language modeling</b>.</p>
      </div>
    </div>
  </div>
</div>

## The Transformer Architecture

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
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
    </div>
</div>

## The Transformer Architecture

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <div class="columns" style="width: 100%">
                    <div class="column vertical-middle text-left" style="width: 50%">
                        <p>In Natural Language Processing (NLP), language modeling includes machine learning models (i.e., deep learning) to predict the next token in a sentence.</p>
                        <ul>
                            <li>Autoencoding tasks to fill in missing words (i.e., masked tokens)</li>
                            <li>Autoregressive tasks to generate the next token in a sentence</li>
                        </ul>
                    </div>
                    <div class="column vertical-middle text-left" style="width: 50%">
                        <img class="external-svg" src="https://upload.wikimedia.org/wikipedia/commons/3/34/Transformer%2C_full_architecture.png" alt="Transformer Architecture" style="max-width: 100%; height: auto;">
                        <div class="footnote">Transformer Architecture - dvgodoy, CC BY 4.0 <https://creativecommons.org/licenses/by/4.0>, via Wikimedia Commons</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

## The Transformer Architecture

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <div class="columns" style="width: 100%">
                    <div class="column vertical-top text-left" style="width: 50%">
                        <p>The main idea is to <b>pay attention to the context</b> of each word in a sentence when modelling language. For example, if context is <em>"Thanks for all the"</em> and we want to know how likely the next word is "fish":</p>
<br>
$$
P(\text{fish} \mid \text{Thanks for all the})
$$
</div>
                    <div class="column vertical-middle text-left" style="width: 50%">
                        <img class="external-svg" src="https://upload.wikimedia.org/wikipedia/commons/3/34/Transformer%2C_full_architecture.png" alt="Transformer Architecture" style="max-width: 100%; height: auto;">
                        <div class="footnote">Transformer Architecture - dvgodoy, CC BY 4.0 <https://creativecommons.org/licenses/by/4.0>, via Wikimedia Commons</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

## The Transformer Architecture

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <div class="columns" style="width: 100%">
                    <div class="column vertical-top text-left" style="width: 50%">
                        <p>The main idea is to <b>pay attention to the context</b> of each word in a sentence when modelling language. For example, if context is <em>"Thanks for all the"</em> and we want to know how likely the next word is "fish":</p>
<br>
$$
P(\text{fish} \mid \text{Thanks for all the})
$$
<br>We want to discover the probability distribution over a vocabulary $V$ for the next word in a sequence:
<br>
$$
P(X = x \mid \mathbf{Y}=y_{1:n}), \qquad x \in V.
$$
<br>where $Y$ is the sequence of words previous to $x$.
</div>
                    <div class="column vertical-middle text-left" style="width: 50%">
                        <img class="external-svg" src="https://upload.wikimedia.org/wikipedia/commons/3/34/Transformer%2C_full_architecture.png" alt="Transformer Architecture" style="max-width: 100%; height: auto;">
                        <div class="footnote">Transformer Architecture - dvgodoy, CC BY 4.0 <https://creativecommons.org/licenses/by/4.0>, via Wikimedia Commons</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

## The Transformer Architecture

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <div class="columns" style="width: 100%">
                    <div class="column vertical-top text-left" style="width: 50%">
                        <p>The transformer architecture solves this problem by:</p>
                        <ol>
                          <li><b>Tokenisation:</b> Convert sentence into tokens.</li>
                          <li><b>Input and Positional Embedding:</b> Convert input tokens into ordered embedded vectors.</li>
                          <li><b>Self-Attention:</b> Determine the relevance of each word to others in the sequence.</li>
                          <li><b>Feed-Forward Neural Network:</b> Pass the attention outputs through a feed-forward neural network to consolidate learned patterns.</li>
                          <li><b>Residual Connections and Layer Normalization:</b> Apply residual connections and layer normalization to stabilize and improve training.</li>
                          <li><b>Output Layer:</b> Use a linear layer followed by a softmax function to generate the final output probabilities.</li>
                      </ol>
                    </div>
                    <div class="column vertical-middle text-left" style="width: 50%">
                        <img class="external-svg" src="https://upload.wikimedia.org/wikipedia/commons/3/34/Transformer%2C_full_architecture.png" alt="Transformer Architecture" style="max-width: 100%; height: auto;">
                        <div class="footnote">Transformer Architecture - dvgodoy, CC BY 4.0 <https://creativecommons.org/licenses/by/4.0>, via Wikimedia Commons</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

## The Transformer Architecture

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <div class="columns" style="width: 100%">
                    <div class="column vertical-top text-left" style="width: 50%">
                      <p>1. <b>Tokenisation:</b> Convert sentence into tokens:</p>
                    </div>
                    <div class="column vertical-middle text-left" style="width: 50%">
                        <img class="external-svg" src="https://upload.wikimedia.org/wikipedia/commons/3/34/Transformer%2C_full_architecture.png" alt="Transformer Architecture" style="max-width: 100%; height: auto;">
                        <div class="footnote">Transformer Architecture - dvgodoy, CC BY 4.0 <https://creativecommons.org/licenses/by/4.0>, via Wikimedia Commons</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

## The Transformer Architecture

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <div class="columns" style="width: 100%">
                    <div class="column vertical-top text-left" style="width: 50%">
                      <p>1. <b>Tokenisation:</b> Convert sentence into tokens:</p>
                      <p>For example, consider the sentence: "So long and thanks for".</p>
                      <p>Tokenisation of this sentence would result in the following tokens:</p>
                      <ul>
                        <li>"So"</li>
                        <li>"long"</li>
                        <li>"and"</li>
                        <li>"thanks"</li>
                        <li>"for"</li>
                      </ul>
                      <p>Each word in the sentence is treated as an individual token.</p>
                    </div>
                    <div class="column vertical-middle text-left" style="width: 50%">
                        <img class="external-svg" src="https://upload.wikimedia.org/wikipedia/commons/3/34/Transformer%2C_full_architecture.png" alt="Transformer Architecture" style="max-width: 100%; height: auto;">
                        <div class="footnote">Transformer Architecture - dvgodoy, CC BY 4.0 <https://creativecommons.org/licenses/by/4.0>, via Wikimedia Commons</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

## The Transformer Architecture

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <div class="columns" style="width: 100%">
                    <div class="column vertical-top text-left" style="width: 50%">
                      <p>2. <b>Input and Positional Embedding:</b> Convert input tokens into ordered embedded vectors:</p>
                    </div>
                    <div class="column vertical-middle text-left" style="width: 50%">
                        <img class="external-svg" src="https://upload.wikimedia.org/wikipedia/commons/3/34/Transformer%2C_full_architecture.png" alt="Transformer Architecture" style="max-width: 100%; height: auto;">
                        <div class="footnote">Transformer Architecture - dvgodoy, CC BY 4.0 <https://creativecommons.org/licenses/by/4.0>, via Wikimedia Commons</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

## The Transformer Architecture

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <div class="columns" style="width: 100%">
                    <div class="column vertical-top text-left" style="width: 50%">
                      <p>2. <b>Input and Positional Embedding:</b> Convert input tokens into ordered embedded vectors:</p>
                      <p>Consider the tokens from the previous example: <b>"So", "long", "and", "thanks", "for"</b>. Each token is converted into a vector using an embedding matrix. For instance:</p>
                      <ul>
                        <li>"So" -> [0.1, 0.3, 0.5, 0.7]</li>
                        <li>"long" -> [0.2, 0.4, 0.6, 0.8]</li>
                        <li>"and" -> [0.3, 0.5, 0.7, 0.9]</li>
                        <li>"thanks" -> [0.4, 0.6, 0.8, 1.0]</li>
                        <li>"for" -> [0.5, 0.7, 0.9, 1.1]</li>
                      </ul>
                      <p>The embedding matrix has as many rows as words in a predefined vocabulary and as many columns as dimensions describing a word.</p>
                    </div>
                    <div class="column vertical-middle text-left" style="width: 50%">
                        <img class="external-svg" src="https://upload.wikimedia.org/wikipedia/commons/3/34/Transformer%2C_full_architecture.png" alt="Transformer Architecture" style="max-width: 100%; height: auto;">
                        <div class="footnote">Transformer Architecture - dvgodoy, CC BY 4.0 <https://creativecommons.org/licenses/by/4.0>, via Wikimedia Commons</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

## The Transformer Architecture

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <div class="columns" style="width: 100%">
                    <div class="column vertical-top text-left" style="width: 50%">
                      <p>2. <b>Input and Positional Embedding:</b> Convert input tokens into ordered embedded vectors:</p>
                      <p><b>Positional encoding</b> is then added to these vectors to incorporate the order of the tokens. For example:</p>
                      <ul>
                        <li>"So" -> [0.1, 0.3, 0.5, 0.7] + [0.0, 0.1, 0.2, 0.3]</li>
                        <li>"long" -> [0.2, 0.4, 0.6, 0.8] + [0.1, 0.2, 0.3, 0.4]</li>
                        <li>"and" -> [0.3, 0.5, 0.7, 0.9] + [0.2, 0.3, 0.4, 0.5]</li>
                        <li>"thanks" -> [0.4, 0.6, 0.8, 1.0] + [0.3, 0.4, 0.5, 0.6]</li>
                        <li>"for" -> [0.5, 0.7, 0.9, 1.1] + [0.4, 0.5, 0.6, 0.7]</li>
                      </ul>
                      <p>Positional embeddings can be defined randomly. Each position having a random representation.</p>
                      <p>The resulting vectors are used as input to the transformer model, capturing both the meaning and position of each word. These are updated at training.</p>
                    </div>
                    <div class="column vertical-middle text-left" style="width: 50%">
                        <img class="external-svg" src="https://upload.wikimedia.org/wikipedia/commons/3/34/Transformer%2C_full_architecture.png" alt="Transformer Architecture" style="max-width: 100%; height: auto;">
                        <div class="footnote">Transformer Architecture - dvgodoy, CC BY 4.0 <https://creativecommons.org/licenses/by/4.0>, via Wikimedia Commons</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

## The Transformer Architecture

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <div class="columns" style="width: 100%">
                    <div class="column vertical-top text-left" style="width: 50%">
                        <p>3. <b>Self-Attention:</b> Determine the relevance of each word to others in the sequence:</p>
                    </div>
                    <div class="column vertical-middle text-left" style="width: 50%">
                        <img class="external-svg" src="https://upload.wikimedia.org/wikipedia/commons/3/34/Transformer%2C_full_architecture.png" alt="Transformer Architecture" style="max-width: 100%; height: auto;">
                        <div class="footnote">Transformer Architecture - dvgodoy, CC BY 4.0 <https://creativecommons.org/licenses/by/4.0>, via Wikimedia Commons</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

## The Transformer Architecture

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <div class="columns" style="width: 100%">
                    <div class="column vertical-top text-left" style="width: 50%">
                      <p>3. <b>Self-Attention:</b> Determine the relevance of each word to others in the sequence:</p>
                      <p>The meaning of a word represented by the embeddings is influenced by previous words. We need a mechanism (i.e., head) to transform the initial meaning of the words accordingly:</p> 
<br>
$$
a_i = \sum_{j=1}^{i} \alpha_{ij}x_j
$$
<br>$\alpha_{ij}$ is the attention weight, indicating the importance of the $j^{th}$ word in the sequence to the $i^{th}$ word.
<br>
$$
\alpha_{ij} = \text{softmax}(\text{score}(x_i, x_j)) \quad \forall \, j \leq i
$$
</div>
                    <div class="column vertical-middle text-left" style="width: 50%">
                        <img class="external-svg" src="https://upload.wikimedia.org/wikipedia/commons/3/34/Transformer%2C_full_architecture.png" alt="Transformer Architecture" style="max-width: 100%; height: auto;">
                        <div class="footnote">Transformer Architecture - dvgodoy, CC BY 4.0 <https://creativecommons.org/licenses/by/4.0>, via Wikimedia Commons</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

## The Transformer Architecture

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <div class="columns" style="width: 100%">
                    <div class="column vertical-top text-left" style="width: 50%">
                      <p>3. <b>Self-Attention:</b> Determine the relevance of each word to others in the sequence:</p>
                      <p>The meaning of a word represented by the embeddings is influenced by previous words. We need a mechanism (i.e., head) to transform the initial meaning of the words accordingly:</p> 
<br>
$$
a_i = \sum_{j=1}^{i} \alpha_{ij}x_j
$$
<br>$\alpha_{ij}$ is the attention weight, indicating the importance of the $j^{th}$ word in the sequence to the $i^{th}$ word.
<br>
$$
\alpha_{ij} = \text{softmax}(\text{score}(x_i, x_j)) \quad \forall \, j \leq i
$$
</div>
                    <div class="column vertical-top text-left" style="width: 50%">
                    <p>In the self-attention mechanism, each input embedding can play three distinct roles: <b>query</b>, <b>key</b>, and <b>value</b>.</p>
                    <ul>
                        <li><b>Query:</b> As the current element compared to preceding inputs.</li>
                        <li><b>Key:</b> As a preceding input compared to the current element.</li>
                        <li><b>Value:</b> As a value of a element that gets weighted and summed up to compute the output of the current element.</li>
                    </ul>
                    <p>We define three matrices to project each input into a representation of its role:</p> 
<br>
$$
\textbf{q} = W^{Q}\textbf{x}, \quad \textbf{k} = W^{K}\textbf{x}, \quad \textbf{v} = W^{V}\textbf{x}
$$
</div>
                </div>
            </div>
        </div>
    </div>
</div>

## The Transformer Architecture

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <div class="columns" style="width: 100%">
                    <div class="column vertical-top text-left" style="width: 50%">
                      <p>3. <b>Self-Attention:</b> Determine the relevance of each word to others in the sequence:</p>
                      <p>The meaning of a word represented by the embeddings is influenced by previous words. We need a mechanism (i.e., head) to transform the initial meaning of the words accordingly:</p> 
<br>
$$
\alpha_{ij} = \text{softmax}\left(\frac{\textbf{q}_i \cdot \textbf{k}_j}{\sqrt{d_k}}\right) \quad \forall \, j \leq i
$$
$$
\text{head}_i = \sum_{j=1}^{i} \alpha_{ij}W^{V}
$$
$$
a_i = \text{head}_i W^O
$$
<br>$W^O$ reshapes the output of the head.
</div>
                    <div class="column vertical-top text-left" style="width: 50%">
                    <p>In the self-attention mechanism, each input embedding can play three distinct roles: <b>query</b>, <b>key</b>, and <b>value</b>.</p>
                    <ul>
                        <li><b>Query:</b> As the current element compared to preceding inputs.</li>
                        <li><b>Key:</b> As a preceding input compared to the current element.</li>
                        <li><b>Value:</b> As a value of a element that gets weighted and summed up to compute the output of the current element.</li>
                    </ul>
                    <p>We define three matrices to project each input into a representation of its role:</p> 
<br>
$$
\textbf{q} = W^{Q}\textbf{x}, \quad \textbf{k} = W^{K}\textbf{x}, \quad \textbf{v} = W^{V}\textbf{x}
$$
</div>
                </div>
            </div>
        </div>
    </div>
</div>

## The Transformer Architecture

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <div class="columns" style="width: 100%">
                    <div class="column vertical-top text-left" style="width: 50%">
                      <p>3. <b>Self-Attention:</b> Determine the relevance of each word to others in the sequence:</p>
                      <p>The meaning of a word represented by the embeddings is influenced by previous words. We need a mechanism (i.e., head) to transform the initial meaning of the words accordingly:</p> 
<br>
$$
\alpha_{ij} = \text{softmax}\left(\frac{\textbf{q}_i \cdot \textbf{k}_j}{\sqrt{d_k}}\right) \quad \forall \, j \leq i
$$
$$
\text{head}_i = \sum_{j=1}^{i} \alpha_{ij}W^{V}
$$
$$
a_i = \text{head}_i W^O
$$
<br>$W^O$ reshapes the output of the head.
</div>
                    <div class="column vertical-top text-left" style="width: 50%">
                      <img class="external-svg" src="https://upload.wikimedia.org/wikipedia/commons/3/34/Transformer%2C_full_architecture.png" alt="Transformer Architecture" style="max-width: 100%; height: auto;">
                      <div class="footnote">Transformer Architecture - dvgodoy, CC BY 4.0 <https://creativecommons.org/licenses/by/4.0>, via Wikimedia Commons</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

## The Transformer Architecture

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <div class="columns" style="width: 100%">
                    <div class="column vertical-top text-left" style="width: 50%">
                      <p>3. <b>Self-Attention:</b> Determine the relevance of each word to others in the sequence:</p>
                      <p>This is a multihead attention mechanism where each head has its own set of key, query, and value matrices:</p> 
<br>
$$
a_i = \text{concat}(\text{head}^{1}_i, \text{head}^{2}_i, \ldots, \text{head}^{h}_i) W^O
$$
<br>Each head focuses on different aspects of the language. One head can focus on the relationship between adjectives and nouns, another head can focus on the relation between verbs and subjects. These relationships transform the meaning of the input and are learned from the data as model's parameters. The additional meaning is added to the original input as a residual connection.
</div>
                    <div class="column vertical-top text-left" style="width: 50%">
                      <img class="external-svg" src="https://upload.wikimedia.org/wikipedia/commons/3/34/Transformer%2C_full_architecture.png" alt="Transformer Architecture" style="max-width: 100%; height: auto;">
                      <div class="footnote">Transformer Architecture - dvgodoy, CC BY 4.0 <https://creativecommons.org/licenses/by/4.0>, via Wikimedia Commons</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

## The Transformer Architecture

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <div class="columns" style="width: 100%">
                    <div class="column vertical-top text-left" style="width: 50%">
                        <p>4. <b>Feed-Forward Neural Network:</b> Pass the attention outputs through a feed-forward neural network to consolidate learned patterns:</p> 
                    </div>
                    <div class="column vertical-middle text-left" style="width: 50%">
                        <img class="external-svg" src="https://upload.wikimedia.org/wikipedia/commons/3/34/Transformer%2C_full_architecture.png" alt="Transformer Architecture" style="max-width: 100%; height: auto;">
                        <div class="footnote">Transformer Architecture - dvgodoy, CC BY 4.0 <https://creativecommons.org/licenses/by/4.0>, via Wikimedia Commons</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

## The Transformer Architecture

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <div class="columns" style="width: 100%">
                    <div class="column vertical-top text-left" style="width: 50%">
                        <p>4. <b>Feed-Forward Neural Network:</b> Pass the attention outputs through a feed-forward neural network to consolidate learned patterns:</p>
                        <p>Fully connected two layer network</p>
<br>
$$
\text{FFN}(x_i) = \text{ReLU}(x_i \textbf{W}_1 + b_1)\textbf{W}_2 + b_2
$$
<br>The input $x_i$ is first transformed by a linear layer with weights $\textbf{W}_1$ and bias $b_1$. The ReLU activation function is then applied to introduce non-linearity. This is followed by another linear transformation using weights $\textbf{W}_2$ and bias $b_2$. The FFN helps in learning complex patterns by combining the attention outputs in a non-linear manner.</p>
</div>
                    <div class="column vertical-middle text-left" style="width: 50%">
                        <img class="external-svg" src="https://upload.wikimedia.org/wikipedia/commons/3/34/Transformer%2C_full_architecture.png" alt="Transformer Architecture" style="max-width: 100%; height: auto;">
                        <div class="footnote">Transformer Architecture - dvgodoy, CC BY 4.0 <https://creativecommons.org/licenses/by/4.0>, via Wikimedia Commons</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

## The Transformer Architecture

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <div class="columns" style="width: 100%">
                    <div class="column vertical-top text-left" style="width: 50%">
                        <p>5. <b>Residual Connections and Layer Normalisation:</b></p>
                    </div>
                    <div class="column vertical-middle text-left" style="width: 50%">
                        <img class="external-svg" src="https://upload.wikimedia.org/wikipedia/commons/3/34/Transformer%2C_full_architecture.png" alt="Transformer Architecture" style="max-width: 100%; height: auto;">
                        <div class="footnote">Transformer Architecture - dvgodoy, CC BY 4.0 <https://creativecommons.org/licenses/by/4.0>, via Wikimedia Commons</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

## The Transformer Architecture

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <div class="columns" style="width: 100%">
                    <div class="column vertical-top text-left" style="width: 50%">
                        <p>5. <b>Residual Connections and Layer Normalisation:</b></p>
                        <p>Residual connections are used at different stages of the process to retain what the word originally meant while enriching it with context.</p>
                    </div>
                    <div class="column vertical-middle text-left" style="width: 50%">
                        <img class="external-svg" src="https://upload.wikimedia.org/wikipedia/commons/3/34/Transformer%2C_full_architecture.png" alt="Transformer Architecture" style="max-width: 100%; height: auto;">
                        <div class="footnote">Transformer Architecture - dvgodoy, CC BY 4.0 <https://creativecommons.org/licenses/by/4.0>, via Wikimedia Commons</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

## The Transformer Architecture

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <div class="columns" style="width: 100%">
                    <div class="column vertical-top text-left" style="width: 50%">
                        <p>5. <b>Residual Connections and Layer Normalisation:</b></p>
                        <p>Residual connections are used at different stages of the process to retain what the word originally meant while enriching it with context.</p>
                        <p>Layer normalisation is applied to keep the parameter values in a range that facilitate gradient descent.</p>
                    <br>
$$
\text{LayerNorm}(x_i) = \frac{x_i - \mu}{\sigma + \epsilon} \cdot \gamma + \beta
$$
<br>In the equation above, $x_i$ is the input vector, $\mu$ is the mean of the input, and $\sigma$ is the standard deviation. $\epsilon$ is a small constant added for numerical stability. $\gamma$ and $\beta$ are learnable parameters that scale and shift the normalized value, allowing the model to learn the optimal scale and shift for each feature.
</div>
                    <div class="column vertical-middle text-left" style="width: 50%">
                        <img class="external-svg" src="https://upload.wikimedia.org/wikipedia/commons/3/34/Transformer%2C_full_architecture.png" alt="Transformer Architecture" style="max-width: 100%; height: auto;">
                        <div class="footnote">Transformer Architecture - dvgodoy, CC BY 4.0 <https://creativecommons.org/licenses/by/4.0>, via Wikimedia Commons</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>


## The Transformer Architecture

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <div class="columns" style="width: 100%">
                    <div class="column vertical-top text-left" style="width: 50%">
                        <p>6. <b>Output Layer:</b> Use a linear layer followed by a softmax function to generate the final output probabilities:</p>
                    </div>
                    <div class="column vertical-middle text-left" style="width: 50%">
                        <img class="external-svg" src="https://upload.wikimedia.org/wikipedia/commons/3/34/Transformer%2C_full_architecture.png" alt="Transformer Architecture" style="max-width: 100%; height: auto;">
                        <div class="footnote">Transformer Architecture - dvgodoy, CC BY 4.0 <https://creativecommons.org/licenses/by/4.0>, via Wikimedia Commons</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

## The Transformer Architecture

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <div class="columns" style="width: 100%">
                    <div class="column vertical-top text-left" style="width: 50%">
                        <p>6. <b>Output Layer:</b> Use a linear layer followed by a softmax function to generate the final output probabilities:</p>
                    </div>
                    <div class="column vertical-middle text-left" style="width: 50%">
                        <img class="external-svg" src="https://upload.wikimedia.org/wikipedia/commons/3/34/Transformer%2C_full_architecture.png" alt="Transformer Architecture" style="max-width: 100%; height: auto;">
                        <div class="footnote">Transformer Architecture - dvgodoy, CC BY 4.0 <https://creativecommons.org/licenses/by/4.0>, via Wikimedia Commons</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

## The Transformer Architecture

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <div class="columns" style="width: 100%">
                    <div class="column vertical-top text-left" style="width: 50%">
                        <p>6. <b>Output Layer:</b> Use a linear layer followed by a softmax function to generate the final output probabilities:</p>
                        <p>The <b>linear layer</b> applies a learned weight matrix to the final hidden state, decoding the high-dimensional representation of the input sequence to a vector of logits, one for each possible output token.</p>
                    </div>
                    <div class="column vertical-middle text-left" style="width: 50%">
                        <img class="external-svg" src="https://upload.wikimedia.org/wikipedia/commons/3/34/Transformer%2C_full_architecture.png" alt="Transformer Architecture" style="max-width: 100%; height: auto;">
                        <div class="footnote">Transformer Architecture - dvgodoy, CC BY 4.0 <https://creativecommons.org/licenses/by/4.0>, via Wikimedia Commons</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

## The Transformer Architecture

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <div class="columns" style="width: 100%">
                    <div class="column vertical-top text-left" style="width: 50%">
                        <p>6. <b>Output Layer:</b> Use a linear layer followed by a softmax function to generate the final output probabilities:</p>
                        <p>The <b>linear layer</b> applies a learned weight matrix to the final hidden state, decoding the high-dimensional representation of the input sequence to a vector of logits, one for each possible output token.</p>
                        <p>The <b>softmax function</b> is applied to these logits to convert them into probabilities. The softmax function ensures that the output values are between 0 and 1 and that they sum up to 1, making them interpretable as probabilities. This step creates a probability distribution over the vocabulary.</p>
<br>
$$
P(X = x \mid \mathbf{Y}=y_{1:n}), \qquad x \in V.
$$
</div>
                    <div class="column vertical-middle text-left" style="width: 50%">
                        <img class="external-svg" src="https://upload.wikimedia.org/wikipedia/commons/3/34/Transformer%2C_full_architecture.png" alt="Transformer Architecture" style="max-width: 100%; height: auto;">
                        <div class="footnote">Transformer Architecture - dvgodoy, CC BY 4.0 <https://creativecommons.org/licenses/by/4.0>, via Wikimedia Commons</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>


## The Transformer Architecture

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <div class="columns" style="width: 100%">
                    <div class="column vertical-middle text-left" style="width: 50%">
                        <p>The transformer process is .</p>
                        <ul>
                            <li>Autoencoding tasks to fill in missing words (i.e., masked tokens)</li>
                            <li>Autoregressive tasks to generate the next token in a sentence</li>
                        </ul>
                    </div>
                    <div class="column vertical-middle text-left" style="width: 50%">
                        <img class="external-svg" src="https://upload.wikimedia.org/wikipedia/commons/3/34/Transformer%2C_full_architecture.png" alt="Transformer Architecture" style="max-width: 100%; height: auto;">
                        <div class="footnote">Transformer Architecture - dvgodoy, CC BY 4.0 <https://creativecommons.org/licenses/by/4.0>, via Wikimedia Commons</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

## The Transformer Architecture

<div class="rows" style="height: 100%">
  <div class="row" style="height: 100%">
    <div class="columns" style="width: 100%">
      <div class="column vertical-middle text-left" style="width: 50%">
        <p><b>Self-attention intuition</b></p>
        <ul>
          <li>Each word forms a query and asks: <em>"Which other words are relevant to me?"</em></li>
          <li>Relevance scored via dot products &amp; softmax &rarr; weighted average of word representations.</li>
          <li>All tokens attend simultaneously &ndash; fully parallel.</li>
        </ul>
      </div>
      <div class="column vertical-middle text-left" style="width: 50%">
        <img class="external-svg" src="https://upload.wikimedia.org/wikipedia/commons/4/4c/Attention-mechanism.svg" alt="Attention Mechanism" style="max-width: 100%; height: auto;">
        <div class="footnote">Toy self-attention heat-map &ndash; Lucas Beyer, CC-BY-SA.</div>
      </div>
    </div>
  </div>
</div>

## The Transformer Architecture

<div class="rows" style="height: 100%">
  <div class="row" style="height: 100%">
    <div class="columns" style="width: 100%">
      <div class="column vertical-middle text-left" style="width: 100%">
        <p><b>Scaled Dot-Product Attention</b></p>
        <p>Queries $Q\in\mathbb{R}^{n\times d}$, Keys $K$, Values $V$.</p>
<pre><code>Attention(Q, K, V) = softmax( Q K^T / \sqrt{d_k} ) V</code></pre>
        <p>Softmax builds a probability simplex &ndash; rows sum to one.</p>
      </div>
    </div>
  </div>
</div>

## The Transformer Architecture

<div class="rows" style="height: 100%">
  <div class="row" style="height: 100%">
    <div class="columns" style="width: 100%">
      <div class="column vertical-middle text-left" style="width: 50%">
        <p><b>Multi-Head Attention</b></p>
        <ul>
          <li>$h$ parallel attention heads &ndash; each with its own {W<sup>Q</sup>, W<sup>K</sup>, W<sup>V</sup>}.</li>
          <li>Heads capture different relations (syntax, position, semantics).</li>
          <li>Outputs are concatenated and projected back to $d_{model}$.</li>
        </ul>
      </div>
      <div class="column vertical-middle text-left" style="width: 50%">
        <img class="external-svg" src="https://upload.wikimedia.org/wikipedia/commons/9/95/Multi-head_attention.svg" alt="Multi-Head Attention" style="max-width: 100%; height: auto;">
        <div class="footnote">Multi-Head Attention &ndash; Anand Rao, CC-BY-SA.</div>
      </div>
    </div>
  </div>
</div>

## The Transformer Architecture

<div class="rows" style="height: 100%">
  <div class="row" style="height: 100%">
    <div class="columns" style="width: 100%">
      <div class="column vertical-middle text-left" style="width: 50%">
        <p><b>Positional Encoding</b></p>
        <ul>
          <li>No recurrence &rarr; order information injected explicitly.</li>
          <li>Sinusoidal: $PE_{pos,2i}=\sin(pos/10000^{2i/d})$, $PE_{pos,2i+1}=\cos(\cdot)$.</li>
          <li>Learned: position embeddings trained like word embeddings.</li>
        </ul>
      </div>
      <div class="column vertical-middle text-left" style="width: 50%">
        <img class="external-svg" src="https://upload.wikimedia.org/wikipedia/commons/f/ff/Positional_encoding.svg" alt="Positional Encoding" style="max-width: 100%; height: auto;">
        <div class="footnote">Sinusoidal positional stripes.</div>
      </div>
    </div>
  </div>
</div>

## The Transformer Architecture

<div class="rows" style="height: 100%">
  <div class="row" style="height: 100%">
    <div class="columns" style="width: 100%">
      <div class="column vertical-middle text-left" style="width: 100%">
        <p><b>Encoder Block</b></p>
        <ol>
          <li>Multi-Head Self-Attention + <em>Add &amp; LayerNorm</em></li>
          <li>Position-wise Feed-Forward (2-layer MLP) + <em>Add &amp; LayerNorm</em></li>
        </ol>
        <p>Decoder adds masked attention and cross-attention to encoder outputs.</p>
      </div>
    </div>
  </div>
</div>

## The Transformer Architecture

<div class="rows" style="height: 100%">
  <div class="row" style="height: 100%">
    <div class="columns" style="width: 100%">
      <div class="column vertical-middle text-left" style="width: 50%">
        <p><b>Training Objectives</b></p>
        <ul>
          <li><b>Causal LM:</b> predict next token (GPT, GPT-2).</li>
          <li><b>Masked LM:</b> predict masked tokens (BERT).</li>
          <li><b>Seq-to-Seq:</b> encoder-decoder with teacher forcing (T5, translation).</li>
        </ul>
      </div>
      <div class="column vertical-middle text-left" style="width: 50%">
        <img class="external-svg" src="https://upload.wikimedia.org/wikipedia/commons/3/3e/Transformer_language_modeling.svg" alt="Causal Mask" style="max-width: 100%; height: auto;">
        <div class="footnote">Causal masking pattern.</div>
      </div>
    </div>
  </div>
</div>

## The Transformer Architecture

<div class="rows" style="height: 100%">
  <div class="row" style="height: 100%">
    <div class="columns" style="width: 100%">
      <div class="column vertical-middle text-left" style="width: 100%">
        <p><b>Pros &amp; Cons</b></p>
        <ul>
          <li>+ Fully parallel &amp; GPU efficient</li>
          <li>+ Captures long-range dependencies directly</li>
          <li>− O(n²) memory/time &rarr; long-sequence variants (Longformer, Performer)</li>
          <li>− Data and compute-hungry for large models</li>
        </ul>
      </div>
    </div>
  </div>
</div>

## The Transformer Architecture

<div class="rows" style="height: 100%">
  <div class="row" style="height: 100%">
    <div class="columns" style="width: 100%">
      <div class="column vertical-middle text-left" style="width: 50%">
        <p><b>Applications</b></p>
        <ul>
          <li>Machine Translation (e.g., Google Translate)</li>
          <li>Code Completion (GitHub Copilot)</li>
          <li>Vision Transformers (ViT) for image classification</li>
          <li>Protein folding (AlphaFold)</li>
        </ul>
      </div>
      <div class="column vertical-middle text-left" style="width: 50%">
        <img class="external-svg" src="https://upload.wikimedia.org/wikipedia/commons/3/34/Transformer%2C_full_architecture.png" alt="Full Transformer" style="max-width: 100%; height: auto;">
        <div class="footnote">Full Transformer &ndash; Wikimedia.</div>
      </div>
    </div>
  </div>
</div>

## The Transformer Architecture

<div class="rows" style="height: 100%">
  <div class="row" style="height: 100%">
    <div class="columns" style="width: 100%">
      <div class="column vertical-middle text-center" style="width: 100%">
        <p><b>Further Reading</b></p>
        <ul>
          <li>Vaswani et al. 2017 &ndash; <em>Attention Is All You Need</em></li>
          <li>The Illustrated Transformer (jalammar.github.io)</li>
          <li>FlashAttention (Dao et al. 2022) for efficient kernels</li>
        </ul>
      </div>
    </div>
  </div>
</div>

<!-- end SLIDES: -->