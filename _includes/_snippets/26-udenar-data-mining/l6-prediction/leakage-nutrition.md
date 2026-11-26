<!-- SLIDES: -->

## Leakage

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>The nutrition papers</b></p>
                <ul>
                    <li><p>The label internacional is made from n_countries, at least two countries</p></li>
                    <li><p>With n_countries kept in, the forest is right on all 56 rows. Its importance is 0.745</p></li>
                </ul>
                <table class="table" style="font-size: 0.8em">
                    <thead>
                        <tr><th>Lecture 6 notebook, 56 rows</th><th>Accuracy</th></tr>
                    </thead>
                    <tbody>
                        <tr><td>Majority class</td><td>0.518</td></tr>
                        <tr><td>Forest without n_countries</td><td>0.714</td></tr>
                        <tr><td>Forest with n_countries</td><td>1.000</td></tr>
                    </tbody>
                </table>
                <p>So n_countries is never an attribute of this label.</p>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/prediction-leakage-2.svg" alt="The same model with and without the suspect attribute" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
