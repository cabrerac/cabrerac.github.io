<!-- SLIDES: -->

## Early AI Approaches (1943-1969) - Searching Algorithms

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
                    <b>An agent</b> must find a way to reach <b>a goal</b> in its <b>environment</b>. But, the next step is not obvious.
                </p>
                <img class="external-svg" src="https://upload.wikimedia.org/wikipedia/commons/3/3b/Shortest_path_with_direct_weights.svg" alt="Shortest path problem" style="width: 90%; margin-top: 1.0em; background-color: #f6f8fa; padding: 10px; border-radius: 5px;">
                <div class="footnote">Shortest path problem: https://en.wikipedia.org/wiki/Shortest_path_problem</div>
            </div>
            <div class="column vertical-middle text-left" style="width: 33%">
                <p>
                    A <b>search problem</b> is defined by a <em>set of states, an initial state, a set of goal states, and a set of actions or transitions between states</em>.
                </p>
$$
P = (S, A, s_0, G)
$$
$S$: set of states
$A$: set of actions
$s_0$: initial state
$G$: set of goal states
</div>
            <div class="column vertical-middle text-left" style="width: 33%">
                <p>
                    A <b>search problem</b> is typically <em>modelled</em> using data structures such as graphs, adjacency matrices, queues and stacks.
                </p>
                <img src="{{ site.url }}/assets/media/diagrams/adjacency-matrix.svg" alt="Adjacency matrix for shortest path graph" style="width: 55%; background-color: #f6f8fa; margin-top: 1.0em;">
                <div class="footnote">Adjacency matrix</div>
            </div>
        </div>
    </div>
</div>

## Early AI Approaches (1943-1969) - AI Perception

## Early AI Approaches (1943-1969) - AI Perception

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
            <p><em>"Within ten years a digital computer will be the world's chess champion." (Simon & Newell, 1958)</em></p>
            <br>
            <p><em>"Machines will be capable, within twenty years, of doing any work a man can do." (Simon, 1965)</em></p>
            <br>
            <p><em>"Within a generation... the problem of creating 'artificial intelligence' will substantially be solved." (Minsky, 1967)</em></p>
            <br>
            <p><em>"In from three to eight years we will have a machine with the general intelligence of an average human being." (Minsky, 1970)</em></p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
            <img src="https://miro.medium.com/v2/resize:fit:1100/format:webp/1*u6BCtE6TOY-0kkZ0fwIZUg.jpeg" alt="You'll own slaves by 1965 (1957)" style="height: 400px">
            <div class="footnote">You'll own "slaves" by 1965 (1957) - https://medium.com/@theo/do-we-need-robot-rights-in-the-age-of-artificial-intelligence-690b9951bae0</div>
            </div>
        </div>
    </div>
</div>

## Early AI Approaches (1943-1969) - AI Perception

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
            <p><em>"Within ten years a digital computer will be the world's chess champion." (Simon & Newell, 1958)</em></p>
            <br>
            <p><em>"Machines will be capable, within twenty years, of doing any work a man can do." (Simon, 1965)</em></p>
            <br>
            <p><em>"Within a generation... the problem of creating 'artificial intelligence' will substantially be solved." (Minsky, 1967)</em></p>
            <br>
            <p><em>"In from three to eight years we will have a machine with the general intelligence of an average human being." (Minsky, 1970)</em></p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
            <img src="https://substackcdn.com/image/fetch/f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F64166aa9-130d-4019-8415-f942959dfccf_1255x783.jpeg" alt="Machines that Think Held Evil (1960)" style="height: 400px">
            <div class="footnote">Machines that Think Held Evil (1960) - https://newsletter.pessimistsarchive.org/p/the-original-ai-doomer-dr-norbert</div>
            </div>
        </div>
    </div>
</div>

## Early AI Approaches (1943-1969) - AI Perception

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
            <p><em>"Within ten years a digital computer will be the world's chess champion." (Simon & Newell, 1958)</em></p>
            <br>
            <p><em>"Machines will be capable, within twenty years, of doing any work a man can do." (Simon, 1965)</em></p>
            <br>
            <p><em>"Within a generation... the problem of creating 'artificial intelligence' will substantially be solved." (Minsky, 1967)</em></p>
            <br>
            <p><em>"In from three to eight years we will have a machine with the general intelligence of an average human being." (Minsky, 1970)</em></p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
            <img src="https://substackcdn.com/image/fetch/f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc015dd1b-3227-4cd5-bac4-cd10433a0440_1108x1263.jpeg" alt="Automation Concerns (1960)" style="height: 520px">
            <div class="footnote">Automation Concerns (1960) - https://newsletter.pessimistsarchive.org/p/the-original-ai-doomer-dr-norbert</div>
            </div>
        </div>
    </div>
</div>

## Early AI Approaches (1943-1969) - AI Perception

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
            <p><em>"Within ten years a digital computer will be the world's chess champion." (Simon & Newell, 1958)</em></p>
            <br>
            <p><em>"Machines will be capable, within twenty years, of doing any work a man can do." (Simon, 1965)</em></p>
            <br>
            <p><em>"Within a generation... the problem of creating 'artificial intelligence' will substantially be solved." (Minsky, 1967)</em></p>
            <br>
            <p><em>"In from three to eight years we will have a machine with the general intelligence of an average human being." (Minsky, 1970)</em></p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
            <img src="https://substackcdn.com/image/fetch/f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F72796ee7-51f4-49ed-85d7-f86ebab90fa8_1361x1783.jpeg" alt="IBM Response (1960)" style="height: 520px">
            <div class="footnote">IBM Response (1960) - https://newsletter.pessimistsarchive.org/p/the-original-ai-doomer-dr-norbert</div>
            </div>
        </div>
    </div>
</div>

## Early AI Approaches (1943-1969) - AI Limitations

## Early AI Approaches (1943-1969) - AI Limitations

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
            <p>Computing power, algorithms, and data were insufficient to solve real-world problems.</p>
            <br>
            <p>Combinatorial explosion</p>
            <br>
            <p>Easy tasks for humans are difficult for AI (Moravec's Paradox)</p>
            </div>
        </div>
    </div>
</div>

## Early AI Approaches (1943-1969) - AI Limitations

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
            <img class="external-svg" src="{{ site.url }}/assets/media/diagrams/search-problem-instance-uninf.svg" alt="Maze navigation search problem" style="width: 100%; margin-top: 1.0em; background-color: #f6f8fa; padding: 10px; border-radius: 5px;">
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
            <p>Computing power, algorithms, and data were insufficient to solve real-world problems.</p>
            <br>
            <p>Combinatorial explosion</p>
            <br>
            <p>Easy tasks for humans are difficult for AI (Moravec's Paradox)</p>
            </div>
        </div>
    </div>
</div>

## Early AI Approaches (1943-1969) - AI Limitations

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
            <img class="external-svg" src="{{ site.url }}/assets/media/diagrams/combinatorial-explosion.svg" alt="Combinatorial explosion diagram" style="width: 100%; margin-top: 1.0em; background-color: #f6f8fa; padding: 10px; border-radius: 5px;">
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
            <p>Computing power, algorithms, and data were insufficient to solve real-world problems.</p>
            <br>
            <p>Combinatorial explosion</p>
            <br>
            <p>Easy tasks for humans are difficult for AI (Moravec's Paradox)</p>
            </div>
        </div>
    </div>
</div>

## Early AI Approaches (1943-1969) - AI Limitations

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
            <img class="external-svg" src="{{ site.url }}/assets/media/diagrams/growth-comparison.svg" alt="Growth comparison diagram" style="width: 100%; margin-top: 1.0em; background-color: #f6f8fa; padding: 10px; border-radius: 5px;">
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
            <p>Computing power, algorithms, and data were insufficient to solve real-world problems.</p>
            <br>
            <p>Combinatorial explosion</p>
            <br>
            <p>Easy tasks for humans are difficult for AI (Moravec's Paradox)</p>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
