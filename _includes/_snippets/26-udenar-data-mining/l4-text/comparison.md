<!-- SLIDES: -->

## The Question and the Data

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p><b>Our question:</b> which nutrition papers match the question in their abstract, judged with marked examples?</p>
            </div>
        </div>
    </div>
</div>

## The Question and the Data

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 36%">
                <p><b>The nutrition papers</b></p>
                <ul>
                    <li>317 papers with a useful abstract, 96 of them positive (30%)</li>
                    <li>Target: OpenAlex topics on obesity, diet, nutrition, diabetes, cardiovascular health or blood pressure</li>
                    <li>64 papers kept apart, 19 of them yes</li>
                    <li>93 abstracts cut at 512 tokens</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 64%">
                <table class="table" style="font-size: 0.58em">
                    <thead>
                        <tr><th>Method</th><th>Kept apart F1 [95%]</th><th>Kept apart TP, FP, FN, TN</th><th>Five folds on the 253 training rows, F1 (accuracy)</th></tr>
                    </thead>
                    <tbody>
                        <tr><td>Majority baseline</td><td>0</td><td>0, 0, 19, 45</td><td>0 (0.70)</td></tr>
                        <tr><td>Keyword list</td><td>0.63 [0.43, 0.79]</td><td>12, 7, 7, 38</td><td>0.68 (0.81)</td></tr>
                        <tr><td>TF-IDF and logistic regression</td><td>0.91 [0.80, 1.00]</td><td>16, 0, 3, 45</td><td>0.77 (0.88)</td></tr>
                        <tr><td>Encoder and logistic regression</td><td>0.89 [0.76, 0.98]</td><td>16, 1, 3, 44</td><td>0.78 (0.86)</td></tr>
                    </tbody>
                </table>
                <p style="font-size: 0.8em">Encoder minus TF-IDF: [-0.09, 0.00]. No clear winner. With 19 yes papers, one paper moves F1 a lot.</p>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
