<!-- SLIDES: -->

## Evaluation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 52%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%; height: 100%">
                <p><b>Why accuracy misleads: the Lecture 4 counts</b></p>
                <ul>
                    <li><p>19 of the 64 marked rows were on the topic. The majority class says no to all of them</p></li>
                    <li><p>It is right on 45 of 64, an accuracy of 0.70, and finds none of the 19. Its F1 is 0.00</p></li>
                    <li><p>TF-IDF with logistic regression finds 16 of the 19, with an F1 of 0.91</p></li>
                </ul>
            </div>
        </div>
    </div>
    <div class="row" style="height: 48%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%; height: 100%">
                <table class="table">
                    <thead>
                        <tr><th>Lecture 4, 64 marked rows</th><th>TP</th><th>FP</th><th>FN</th><th>TN</th><th>Accuracy</th><th>F1</th></tr>
                    </thead>
                    <tbody>
                        <tr><td>Majority class</td><td>0</td><td>0</td><td>19</td><td>45</td><td>0.70</td><td>0.00</td></tr>
                        <tr><td>TF-IDF with logistic regression</td><td>16</td><td>0</td><td>3</td><td>45</td><td>0.95</td><td>0.91</td></tr>
                    </tbody>
                </table>
                <p>Accuracy alone hides the rows a method misses. We report the four counts and F1.</p>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
