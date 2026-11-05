<!-- SLIDES: -->

## Judging Graph Results

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p>With no labels, a graph result is judged <b>against citations</b>, <b>across seeds</b> and <b>against random pairs</b>.</p>
            </div>
        </div>
    </div>
</div>

## Judging Graph Results

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>No answer key</b></p>
                <p>A graph result has no marked examples, so we check it three ways.</p>
                <ul>
                    <li><b>Against citations:</b> does the place agree with how the literature cites a paper</li>
                    <li><b>Across seeds:</b> does node2vec give the same neighbours on a rerun</li>
                    <li><b>Against random pairs:</b> do neighbours share more topics than chance</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/social-network-analysis.jpg" alt="Social network analysis" style="height: 360px">
                <div class="footnote">Social Network Analysis Visualization - Martin Grandjean, CC BY-SA 3.0 <https://creativecommons.org/licenses/by-sa/3.0>, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
