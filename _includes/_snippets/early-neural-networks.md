<!-- SLIDES: -->

## Learning from Examples (1987 - present) - Data-driven Algorithms

<div class="rows" style="height: 100%">
    <div class="row" style="height: 20%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 33%">
                <p><strong>Problem Definition</strong></p>
            </div>
            <div class="column vertical-middle text-center" style="width: 33%">
                <p><strong>Formal Definition</strong></p>
            </div>
            <div class="column vertical-middle text-center" style="width: 33%">
                <p><strong>Computational Representation</strong></p>
            </div>
        </div>
    </div>
    <div class="row" style="height: 80%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 33%">
                <p>
                </p>
                <img src="{{ site.url }}/assets/media/diagrams/learning-from-data.svg" alt="Learning from data" style="width: 60%; background-color: #f6f8fa; margin-top: 1.0em;">
                <div class="footnote">Learning from examples: classification problem</div>
            </div>
            <div class="column vertical-middle text-left" style="width: 33%">
            </div>
            <div class="column vertical-middle text-left" style="width: 33%">
            </div>
        </div>
    </div>
</div>

## Learning from Examples (1987 - present) - Data-driven Algorithms

<div class="rows" style="height: 100%">
    <div class="row" style="height: 20%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 33%">
                <p><strong>Problem Definition</strong></p>
            </div>
            <div class="column vertical-middle text-center" style="width: 33%">
                <p><strong>Formal Definition</strong></p>
            </div>
            <div class="column vertical-middle text-center" style="width: 33%">
                <p><strong>Computational Representation</strong></p>
            </div>
        </div>
    </div>
    <div class="row" style="height: 80%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 33%">
                <p>
                    Agents cannot be fully pre-programmed. Agent must <b>learn from examples</b> to perform a task.
                </p>
                <img src="{{ site.url }}/assets/media/diagrams/learning-from-data.svg" alt="Learning from data" style="width: 60%; background-color: #f6f8fa; margin-top: 1.0em;">
                <div class="footnote">Learning from examples: classification problem</div>
            </div>
            <div class="column vertical-middle text-left" style="width: 33%">
            </div>
            <div class="column vertical-middle text-left" style="width: 33%">
            </div>
        </div>
    </div>
</div>

## Learning from Examples (1987 - present) - Data-driven Algorithms

<div class="rows" style="height: 100%">
    <div class="row" style="height: 20%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 33%">
                <p><strong>Problem Definition</strong></p>
            </div>
            <div class="column vertical-middle text-center" style="width: 33%">
                <p><strong>Formal Definition</strong></p>
            </div>
            <div class="column vertical-middle text-center" style="width: 33%">
                <p><strong>Computational Representation</strong></p>
            </div>
        </div>
    </div>
    <div class="row" style="height: 80%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 33%">
                <p>
                    Agents cannot be fully pre-programmed. Agent must <b>learn from examples</b> to perform a task.
                </p>
                <img src="{{ site.url }}/assets/media/diagrams/learning-from-data.svg" alt="Learning from data" style="width: 60%; background-color: #f6f8fa; margin-top: 1.0em;">
                <div class="footnote">Learning from examples: classification problem</div>
            </div>
            <div class="column vertical-middle text-left" style="width: 33%">
                <p>
                    <b>Learning from examples</b> requires a <em>function that approximates patterns in data, using a learning algorithm, and evaluation criteria</em>.
                </p>
$$
LD = (D, \mathcal{H}, L, A)
$$
$D$: dataset of examples $\{x_i\}$ or pairs $\{(x_i, y_i)\}$
$\mathcal{H}$: hypothesis space of possible functions
$L$: loss/reward function measuring success
$A$: algorithm to search through $\mathcal{H}$
            </div>
            <div class="column vertical-middle text-left" style="width: 33%">
            </div>
        </div>
    </div>
</div>

## Learning from Examples (1987 - present) - Data-driven Algorithms

<div class="rows" style="height: 100%">
    <div class="row" style="height: 20%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 33%">
                <p><strong>Problem Definition</strong></p>
            </div>
            <div class="column vertical-middle text-center" style="width: 33%">
                <p><strong>Formal Definition</strong></p>
            </div>
            <div class="column vertical-middle text-center" style="width: 33%">
                <p><strong>Computational Representation</strong></p>
            </div>
        </div>
    </div>
    <div class="row" style="height: 80%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 33%">
                <p>
                    Agents cannot be fully pre-programmed. Agent must <b>learn from examples</b> to perform a task.
                </p>
                <img src="{{ site.url }}/assets/media/diagrams/learning-from-data.svg" alt="Learning from data" style="width: 60%; background-color: #f6f8fa; margin-top: 1.0em;">
                <div class="footnote">Learning from examples: classification problem</div>
            </div>
            <div class="column vertical-middle text-left" style="width: 33%">
                <p>
                    <b>Learning from examples</b> requires a <em>function that approximates patterns in data, using a learning algorithm, and evaluation criteria</em>.
                </p>
$$
LD = (D, \mathcal{H}, L, A)
$$
$D$: dataset of examples $\{x_i\}$ or pairs $\{(x_i, y_i)\}$
$\mathcal{H}$: hypothesis space of possible functions
$L$: loss/reward function measuring success
$A$: algorithm to search through $\mathcal{H}$
            </div>
            <div class="column vertical-middle text-left" style="width: 33%">
                <p>
                    <b>Learning algorithms</b> use different computational representations during the <em>learning and inference</em>: dataframes, tuples, trees, graphs, matrices, etc. 
                </p>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->