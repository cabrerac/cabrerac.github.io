<!-- SLIDES: -->

## Majority Class

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>In the Lecture 6 notebook</b></p>
                <ul>
                    <li><p><b>Label:</b> internacional, an article with authors from at least two countries</p></li>
                    <li><p>276 articles with a label, 145 of them international</p></li>
                    <li><p>220 rows to learn and 56 kept apart, 52% international</p></li>
                    <li><p>The majority class says international to all 56 and is right on 0.518 of them</p></li>
                </ul>
                <p>Every method below is judged on the same 56 rows, against 0.518.</p>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/eval-split.svg" alt="Fit on the training rows, predict the rows kept apart" style="height: auto; max-width: 100%; max-height: 100%;">
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
