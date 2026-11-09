<!-- SLIDES: -->

## The Grouping Task

<div class="rows" style="height: 100%">
    <div class="row" style="height: 50%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 33%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/clusters-with-noise.svg" alt="Groups with noise points" style="max-height: 155px; max-width: 100%; width: auto;">
                <p><b>Business understanding</b></p>
                <p>Similar items and the rest</p>
            </div>
            <div class="column vertical-middle text-center" style="width: 33%">
                <table class="table" style="font-size: 0.7em">
                    <tbody>
                        <tr><td>Customers</td><td>purchases</td></tr>
                        <tr><td>Patients</td><td>measurements</td></tr>
                        <tr><td>Texts</td><td>words</td></tr>
                    </tbody>
                </table>
                <p><b>Data understanding</b></p>
                <p>Items described by attributes</p>
            </div>
            <div class="column vertical-middle text-center" style="width: 33%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/singular-value-decomposition.svg" alt="Singular value decomposition as rotation, scaling, rotation" style="max-height: 155px; max-width: 100%; width: auto;">
                <p><b>Data preparation</b></p>
                <p>Scaled items and a few directions</p>
            </div>
        </div>
    </div>
    <div class="row" style="height: 50%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 33%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/k-means-convergence.gif" alt="k-means moving its centres" style="max-height: 155px; max-width: 100%; width: auto;">
                <p><b>Modeling</b></p>
                <p>k-means, mixtures, and HDBSCAN</p>
            </div>
            <div class="column vertical-middle text-center" style="width: 33%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/permutation-test-animation.gif" alt="Permutation test" style="max-height: 155px; max-width: 100%; width: auto;">
                <p><b>Evaluation</b></p>
                <p>Silhouette, a baseline, and stability</p>
            </div>
            <div class="column vertical-middle text-center" style="width: 33%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/crisp-dm-process-diagram.png" alt="CRISP-DM process diagram" style="max-height: 155px; max-width: 100%; width: auto;">
                <p><b>Deployment</b></p>
                <p>What using a group would mean</p>
            </div>
        </div>
    </div>
</div>

## Conclusions

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <h3><a href="https://cabrerac.github.io/teaching/26-udenar-data-mining/l3-groups/" target="_blank">Lecture 3</a></h3>
                <ul>
                    <li>Groups of similar items</li>
                    <li>Data and methods</li>
                    <li>k-means, Gaussian mixtures, HDBSCAN</li>
                    <li>Items that fit no group</li>
                    <li>Evaluation and deployment</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <h3><a href="https://cabrerac.github.io/teaching/26-udenar-data-mining/l4-text/" target="_blank">Lecture 4</a></h3>
                <ul>
                    <li>Text extraction with marked examples</li>
                    <li>Data and methods</li>
                    <li>Keyword lists, TF-IDF with logistic regression, text encoders</li>
                    <li>Evaluation and deployment</li>
                </ul>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
