<!-- SLIDES: -->

## The Prediction Task

<div class="rows" style="height: 100%">
    <div class="row" style="height: 50%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 33%">
                <img src="{{ site.url }}/assets/media/diagrams/decision-tree-1.svg" alt="A generic decision tree" style="max-height: 155px; max-width: 100%; width: auto;">
                <p><b>Business understanding</b></p>
                <p>A label given, not found</p>
            </div>
            <div class="column vertical-middle text-center" style="width: 33%">
                <table class="table" style="font-size: 0.7em">
                    <tbody>
                        <tr><td>Loans</td><td>repaid</td></tr>
                        <tr><td>Patients</td><td>a given label</td></tr>
                        <tr><td>Articles</td><td>internacional</td></tr>
                    </tbody>
                </table>
                <p><b>Data understanding</b></p>
                <p>A table with a given label, and leakage</p>
            </div>
            <div class="column vertical-middle text-center" style="width: 33%">
                <img src="{{ site.url }}/assets/media/diagrams/logreg-scaling-2.svg" alt="One-hot columns for a colour" style="max-height: 155px; max-width: 100%; width: auto;">
                <p><b>Data preparation</b></p>
                <p>Scaled, encoded, and filled columns</p>
            </div>
        </div>
    </div>
    <div class="row" style="height: 50%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 33%">
                <img src="{{ site.url }}/assets/media/diagrams/nn-output-lr.svg" alt="Logistic regression next to the output layer of the network" style="max-height: 155px; max-width: 100%; width: auto;">
                <p><b>Modeling</b></p>
                <p>A forest, logistic regression, a network</p>
            </div>
            <div class="column vertical-middle text-center" style="width: 33%">
                <img src="{{ site.url }}/assets/media/diagrams/eval-counts.svg" alt="Accuracy against the majority class" style="max-height: 155px; max-width: 100%; width: auto;">
                <p><b>Evaluation</b></p>
                <p>Four counts on rows kept apart, against the majority class</p>
            </div>
            <div class="column vertical-middle text-center" style="width: 33%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/crisp-dm-process-diagram.png" alt="CRISP-DM process diagram" style="max-height: 155px; max-width: 100%; width: auto;">
                <p><b>Deployment</b></p>
                <p>What using a prediction would mean</p>
            </div>
        </div>
    </div>
</div>

## Conclusions

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <h3><a href="https://cabrerac.github.io/teaching/26-udenar-data-mining/l6-prediction/" target="_blank">Lecture 6</a></h3>
                <ul>
                    <li>Prediction of a given label</li>
                    <li>Data and methods</li>
                    <li>Random forests, logistic regression, one hidden layer</li>
                    <li>Evaluation and deployment</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <h3><a href="https://cabrerac.github.io/teaching/26-udenar-data-mining/l7-research/" target="_blank">Lecture 7</a></h3>
                <ul>
                    <li>Transformers and large language models</li>
                    <li>Models that can change the data mining process</li>
                    <li>What they can do on the tasks of Lectures 2 to 6</li>
                    <li>Their risks</li>
                </ul>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
