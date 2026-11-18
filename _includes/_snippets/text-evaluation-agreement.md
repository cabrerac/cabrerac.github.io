<!-- SLIDES: -->

## Evaluation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>The same texts</b></p>
                <table class="table">
                    <thead>
                        <tr><th>Text</th><th>Keyword list</th><th>TF-IDF</th><th>Encoder</th></tr>
                    </thead>
                    <tbody>
                        <tr><td>A, B</td><td>yes</td><td>yes</td><td>yes</td></tr>
                        <tr><td>C</td><td>yes</td><td>no</td><td>no</td></tr>
                        <tr><td>D</td><td>no</td><td>no</td><td>yes</td></tr>
                    </tbody>
                </table>
                <p>A text that all three say yes to is a stronger candidate. A text that only one says yes to is not a winner.</p>
                <p>The individual notebook runs TF-IDF on 64 marked nutrition abstracts, with the keyword list as the reference. The most common answer, no, gives 0.70, the keywords 0.78 and TF-IDF 0.95.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/text-methods-panels.png" alt="Accuracy, F1, and five-fold F1 of the three text methods" style="height: 470px">
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
