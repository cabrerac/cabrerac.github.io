<!-- SLIDES: -->

## Evaluation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>The same texts</b></p>
                <p>Yes means the method answers yes for that text.</p>
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
                <ul>
                    <li><b>All three:</b> A and B are a stronger candidate.</li>
                    <li><b>Keyword list only:</b> C is a yes from the list alone.</li>
                    <li><b>Encoder only:</b> D is a yes from the encoder alone.</li>
                </ul>
                <p>A text that only one method says yes to is not a winner.</p>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
