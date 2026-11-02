<!-- SLIDES: -->

## What is Data Mining

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p><b>Data mining</b> is the search for valid, new and useful patterns in large collections of data, as one step of a longer process of discovery.</p>
            </div>
        </div>
    </div>
</div>

## What is Data Mining

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 55%">
                <p><b>A definition from the 1990s</b></p>
                <table class="table">
                    <tr>
                        <td>
                            <p>"The nontrivial process of identifying valid, novel, potentially useful, and ultimately understandable patterns in data."</p>
                            <p><a href="https://ojs.aaai.org/aimagazine/index.php/aimagazine/article/view/1230" target="_blank" rel="noopener noreferrer">(Fayyad et al., 1996)</a></p>
                        </td>
                    </tr>
                </table>
                <p>Each word is a test a result has to pass.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 45%">
                <img src="{{ site.url }}/assets/media/images/data-mining-archival-images-of-ai.jpg" alt="Data mining, archival images of AI" style="height: 400px">
                <div class="footnote">Data Mining 3 - Hanna Barakat &amp; Archival Images of AI + AIxDESIGN, CC BY 4.0 <https://creativecommons.org/licenses/by/4.0>, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## What is Data Mining

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 55%">
                <p><b>Knowledge Discovery in Databases (KDD)</b> <a href="https://ojs.aaai.org/aimagazine/index.php/aimagazine/article/view/1230" target="_blank" rel="noopener noreferrer">(Fayyad et al., 1996)</a></p>
                <ul>
                    <li><b>Selection</b> - pick the target data</li>
                    <li><b>Preprocessing</b> - clean it and handle what is missing</li>
                    <li><b>Transformation</b> - reduce or reshape it for a method</li>
                    <li><b>Data mining</b> - search for patterns</li>
                    <li><b>Interpretation and evaluation</b> - decide what the patterns mean</li>
                </ul>
                <p>Data mining is one step of five. Most of the work sits around it.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 45%">
                <img src="{{ site.url }}/assets/media/images/data-mining-archival-images-of-ai.jpg" alt="Data mining, archival images of AI" style="height: 400px">
                <div class="footnote">Data Mining 3 - Hanna Barakat &amp; Archival Images of AI + AIxDESIGN, CC BY 4.0 <https://creativecommons.org/licenses/by/4.0>, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## What is Data Mining

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>SEMMA</b> from the SAS Institute <a href="https://recipp.ipp.pt/handle/10400.22/136" target="_blank" rel="noopener noreferrer">(Azevedo &amp; Santos, 2008)</a></p>
                <ul>
                    <li><b>Sample</b> - a part of the data that is big enough to matter and small enough to handle</li>
                    <li><b>Explore</b> - look for trends and odd values</li>
                    <li><b>Modify</b> - create, select, and transform variables</li>
                    <li><b>Model</b> - let a method search the data</li>
                    <li><b>Assess</b> - judge how useful and reliable the result is</li>
                </ul>
                <p>Close to KDD, and tied to one software suite.</p>
            </div>
        </div>
    </div>
</div>

## What is Data Mining

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 55%">
                <p><b>CRISP-DM</b>, the Cross Industry Standard Process for Data Mining</p>
                <p>Built by a consortium of users and suppliers: DaimlerChrysler, SPSS, NCR, and OHRA.</p>
                <p>Partly funded by the European Commission.</p>
                <p>Version 1.0 came out in 2000.</p>
                <p>Made to work for any sector and any tool.</p>
                <table class="table">
                    <tr>
                        <td>
                            <p>"The process model is independent of both the industry sector and the technology used."</p>
                            <p><a href="https://cs.unibo.it/montesi/CBD/Beatriz/10.1.1.198.5133.pdf" target="_blank" rel="noopener noreferrer">(Wirth &amp; Hipp, 2000)</a></p>
                        </td>
                    </tr>
                </table>
            </div>
            <div class="column vertical-middle text-left" style="width: 45%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/crisp-dm-process-diagram.png" alt="CRISP-DM process diagram" style="height: 380px">
                <div class="footnote">CRISP-DM Process Diagram - Kenneth Jensen, CC BY-SA 3.0 <https://creativecommons.org/licenses/by-sa/3.0>, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## What is Data Mining

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>Three processes, one idea</b> <a href="https://recipp.ipp.pt/handle/10400.22/136" target="_blank" rel="noopener noreferrer">(Azevedo &amp; Santos, 2008)</a></p>
                <table class="table" style="font-size: 0.9em">
                    <thead>
                        <tr>
                            <th>KDD</th>
                            <th>SEMMA</th>
                            <th>CRISP-DM</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr><td>Before KDD</td><td></td><td>Business understanding</td></tr>
                        <tr><td>Selection</td><td>Sample</td><td rowspan="2">Data understanding</td></tr>
                        <tr><td>Preprocessing</td><td>Explore</td></tr>
                        <tr><td>Transformation</td><td>Modify</td><td>Data preparation</td></tr>
                        <tr><td>Data mining</td><td>Model</td><td>Modeling</td></tr>
                        <tr><td>Interpretation and evaluation</td><td>Assess</td><td>Evaluation</td></tr>
                        <tr><td>After KDD</td><td></td><td>Deployment</td></tr>
                    </tbody>
                </table>
                <p>CRISP-DM names the start and the end. That is where the question and the use live.</p>
            </div>
        </div>
    </div>
</div>

## What is Data Mining

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>Later variants</b></p>
                <ul>
                    <li><b>Team Data Science Process</b> - Microsoft adds roles and project templates <a href="https://learn.microsoft.com/en-us/azure/architecture/data-science-process/overview" target="_blank" rel="noopener noreferrer">(Microsoft TDSP)</a></li>
                    <li><b>CRISP-ML(Q)</b> - adds quality checks and monitoring for machine learning <a href="https://doi.org/10.3390/make3020020" target="_blank" rel="noopener noreferrer">(Studer et al., 2021)</a></li>
                    <li><b>Twenty years later</b> - CRISP-DM still fits goal-directed projects, less so open exploration <a href="https://doi.org/10.1109/TKDE.2019.2962680" target="_blank" rel="noopener noreferrer">(Martínez-Plumed et al., 2021)</a></li>
                </ul>
                <p>The phases stay. What changes is who does them and how they are checked.</p>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
