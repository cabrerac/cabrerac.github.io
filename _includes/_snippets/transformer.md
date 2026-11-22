<!-- SLIDES: -->

## The Transformer Architecture

<div class="rows" style="height: 100%">
  <div class="row" style="height: 100%">
    <div class="columns" style="width: 100%">
      <div class="column vertical-middle text-center" style="width: 100%">
        <p>The Transformer is a deep neural network architecture based on the <b>multi-head attention mechanism</b> introduced by researchers at Google (<a href="https://proceedings.neurips.cc/paper_files/paper/2017/file/
                3f5ee243547dee91fbd053c1c4a845aa-Paper.pdf">Vaswani et al., 2017</a>). The original goal was to improve machine learning translation tasks based on <b>language modelling</b>.</p>
      </div>
    </div>
  </div>
</div>

## The Transformer Architecture

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

## The Transformer Architecture

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>In Natural Language Processing (NLP), language modelling includes machine learning models (i.e., deep learning) to predict the next token in a sentence.</p>
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

## The Transformer Architecture

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
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

## The Transformer Architecture

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
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

<!-- end SLIDES: -->

{% include _snippets/transformer-components.md %}

{% include _snippets/transformer-training.md %}

<!-- SLIDES: -->

## The Transformer Architecture

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
          <div class="column vertical-top text-left" style="width: 50%">
            <p><b>Training Process:</b></p>
            <p>The training process of a Transformer model can involve RL techniques for specific purposes:</p>
            <ul>
              <li><b>Reinforcement Learning from Human Feedback</b> to align the model with human preferences.</li>
              <li><b>Task-Specific RL</b> for fine-tuning for specific objectives like dialogue quality, summarisation, etc.</li>
            </ul>
          </div>
          <div class="column vertical-middle text-left" style="width: 50%">
            <img class="external-svg" src="https://upload.wikimedia.org/wikipedia/commons/1/1b/Reinforcement_learning_diagram.svg" alt="RL Framework" style="max-width: 100%; height: auto;">
            <div class="footnote">Reinforcement Learning Framework - Megajuice, CC0, via Wikimedia Commons.</div>
          </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
