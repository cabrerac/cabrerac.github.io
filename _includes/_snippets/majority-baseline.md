<!-- SLIDES: -->

## Majority Class

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>A <b>baseline</b> tells us what an answer with no work would give. The first one is the <b>majority class</b>, the most frequent label, said for every item.</p>
                <ul>
                    <li><p>Here 7 of 10 items are no, so the baseline says no to all of them</p></li>
                    <li><p>It is right on 7 of 10, an accuracy of 0.70, and its recall of yes is 0</p></li>
                    <li><p>A method must beat it on the counts that matter for the use</p></li>
                </ul>
                <p>Accuracy can look high while every yes is missed. Evaluation comes back to this.</p>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/eval-majority.svg" alt="Saying no to all of 7 no and 3 yes" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
