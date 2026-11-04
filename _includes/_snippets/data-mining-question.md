<!-- SLIDES: -->

## The Data Mining Question

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p>A <b>data mining question</b> states what someone needs to decide, how we will answer it, what counts as a good answer and who will use it.</p>
            </div>
        </div>
    </div>
</div>

## The Data Mining Question

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>A question needs four parts</b></p>
                <ul>
                    <li><b>Question:</b> what someone needs to decide</li>
                    <li><b>Steps:</b> how we will answer it</li>
                    <li><b>Standard:</b> what counts as a good answer</li>
                    <li><b>Use:</b> who uses the answer and how</li>
                </ul>
                <p>We write all four before we run any method.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/ml-project-canvas.svg" alt="Project canvas" style="height: 420px">
            </div>
        </div>
    </div>
</div>

## The Data Mining Question

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Question</b></p>
                <ul>
                    <li>Names a reader and a decision</li>
                    <li>Names the data it will use</li>
                    <li>Can be answered with that data</li>
                    <li>Is small enough for the time we have</li>
                </ul>
                <br>
                <p><b>Bad:</b> What is interesting in the data?</p>
                <p><b>Better:</b> Which ten books should the library buy again next term?</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/critical-thinking.png" alt="Critical thinking" style="height: 420px">
            </div>
        </div>
    </div>
</div>

## The Data Mining Question

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Steps</b></p>
                <ul>
                    <li>One line for each CRISP-DM phase</li>
                    <li>The preparation each method needs</li>
                    <li>The methods we will compare</li>
                    <li>Where a step can send us back</li>
                </ul>
                <p>Steps can change and the process is iterative.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/crisp-dm-process-diagram.png" alt="CRISP-DM process diagram" style="height: 400px">
                <div class="footnote">CRISP-DM Process Diagram - Kenneth Jensen, CC BY-SA 3.0 <https://creativecommons.org/licenses/by-sa/3.0>, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## The Data Mining Question

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Standard</b></p>
                <ul>
                    <li>Written before we see the results</li>
                    <li>Something we can check, not a feeling</li>
                    <li>Beats a baseline, such as chance or the most popular items</li>
                    <li>Beats the other candidates we found</li>
                    <li>Says what we do when nothing passes</li>
                </ul>
                <p>Without a standard any result looks good.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/growth-comparison.svg" alt="A plot comparing three growth curves" style="height: 380px">
            </div>
        </div>
    </div>
</div>

## The Data Mining Question

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Use</b></p>
                <ul>
                    <li>Who reads the answer</li>
                    <li>What they may decide with it</li>
                    <li>What they may not decide with it</li>
                    <li>What new evidence would change that use</li>
                </ul>
                <p>The use sets the limits of the answer.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/context-people.png" alt="Context and people" style="height: 420px">
            </div>
        </div>
    </div>
</div>

## The Data Mining Question

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <table class="table">
                    <thead>
                        <tr>
                            <th></th>
                            <th>Bad</th>
                            <th>Good</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr><td><b>Question</b></td><td>What is in the data?</td><td>Which loan types should the officer review first?</td></tr>
                        <tr><td><b>Steps</b></td><td>Run some models</td><td>Profile loans, prepare one table, compare two methods</td></tr>
                        <tr><td><b>Standard</b></td><td>Looks right</td><td>Finds more late loans than a random review of the data</td></tr>
                        <tr><td><b>Use</b></td><td>Not stated</td><td>Orders the review list. It never refuses a loan alone.</td></tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
