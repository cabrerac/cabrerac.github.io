<!-- SLIDES: -->

## Neural Network

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Three methods on the same 56 rows kept apart</b></p>
                <table class="table" style="font-size: 0.72em">
                    <thead>
                        <tr><th></th><th>TP</th><th>FP</th><th>FN</th><th>TN</th><th>Accuracy</th></tr>
                    </thead>
                    <tbody>
                        <tr><td>Majority class</td><td>29</td><td>27</td><td>0</td><td>0</td><td>0.518</td></tr>
                        <tr><td>Random forest</td><td>21</td><td>8</td><td>8</td><td>19</td><td>0.714</td></tr>
                        <tr><td>Logistic regression</td><td>14</td><td>7</td><td>15</td><td>20</td><td>0.607</td></tr>
                        <tr><td>One hidden layer</td><td>15</td><td>7</td><td>14</td><td>20</td><td>0.625</td></tr>
                    </tbody>
                </table>
                <ul>
                    <li><p>The network beats logistic regression by one row, and stays below the forest</p></li>
                    <li><p>Its output layer is a logistic regression on 8 learned columns. On 220 rows, those columns add little</p></li>
                </ul>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/nn-output-lr.svg" alt="Logistic regression next to the output layer of the network" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
