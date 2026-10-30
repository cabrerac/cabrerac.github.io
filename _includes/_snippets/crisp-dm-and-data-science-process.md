<!-- SLIDES: -->

## CRISP-DM and the Data Science Process

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/crisp-dm-process-diagram.png" alt="CRISP-DM process diagram" style="height: 400px">
                <div class="footnote">CRISP-DM Process Diagram - Kenneth Jensen, CC BY-SA 3.0 <https://creativecommons.org/licenses/by-sa/3.0>, via Wikimedia Commons</div>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/data-science-process.png" alt="Data Science Process" style="height: 400px">
            </div>
        </div>
    </div>
</div>

## CRISP-DM and the Data Science Process

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>Two maps of the same work</b></p>
                <table class="table">
                    <thead>
                        <tr>
                            <th>Access, Assess, Address</th>
                            <th>CRISP-DM</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr><td>The question comes first</td><td>Business understanding</td></tr>
                        <tr><td>Access - get the data in a usable form</td><td>Data understanding (collect, describe)</td></tr>
                        <tr><td>Assess - check quality and fitness</td><td>Data understanding (explore, verify) and data preparation</td></tr>
                        <tr><td>Address - answer the question</td><td>Modeling and evaluation</td></tr>
                        <tr><td>The answer informs a decision</td><td>Deployment</td></tr>
                    </tbody>
                </table>
                <p>CRISP-DM splits Address into a method, a check, and a use.</p>
            </div>
        </div>
    </div>
</div>

## CRISP-DM and the Data Science Process

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 45%">
                <p><b>The pipeline is the system around the project</b></p>
                <ul>
                    <li><b>Pipeline</b> - where data is ingested, stored, processed, and served</li>
                    <li><b>CRISP-DM</b> - what the team does with that data</li>
                    <li>A deployed answer often becomes a new stage of the pipeline</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 55%">
                <img src="{{ site.url }}/assets/media/diagrams/big-data-pipeline-template.svg" alt="Big data pipeline" style="height: 380px">
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
