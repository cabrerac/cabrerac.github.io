<!-- SLIDES: -->

## Attention and Recurrence

<div class="rows" style="height: 100%">
    <div class="row" style="height: 62%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
<img src="{{ site.url }}/assets/media/diagrams/attention-vs-recurrence-1.svg" alt="Recurrent network over five tokens" style="max-height: 330px; max-width: 100%; width: auto;">
            </div>
        </div>
    </div>
    <div class="row" style="height: 38%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <p><b>Recurrent network:</b> reads one token at a time and keeps a hidden state</p>
                <ul>
                    <li><p><b>Long paths:</b> <em>el</em> reaches <em>estación</em> only through every hidden state in between</p></li>
                    <li><p><b>Sequential:</b> step $t$ waits for step $t-1$, so a long text cannot be processed in parallel</p></li>
                </ul>
            </div>
        </div>
    </div>
</div>

## Attention and Recurrence

<div class="rows" style="height: 100%">
    <div class="row" style="height: 62%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
<img src="{{ site.url }}/assets/media/diagrams/attention-vs-recurrence-2.svg" alt="Recurrent and convolutional networks over five tokens" style="max-height: 330px; max-width: 100%; width: auto;">
            </div>
        </div>
    </div>
    <div class="row" style="height: 38%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <p><b>Convolutional network:</b> each unit sees a window of $k$ neighbouring tokens</p>
                <ul>
                    <li><p><b>Local:</b> two far tokens only meet after several stacked layers</p></li>
                    <li><p><b>Parallel:</b> every window is computed at the same time</p></li>
                </ul>
            </div>
        </div>
    </div>
</div>

## Attention and Recurrence

<div class="rows" style="height: 100%">
    <div class="row" style="height: 62%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
<img src="{{ site.url }}/assets/media/diagrams/attention-vs-recurrence-3.svg" alt="Recurrent network, convolutional network and attention over five tokens" style="max-height: 330px; max-width: 100%; width: auto;">
            </div>
        </div>
    </div>
    <div class="row" style="height: 38%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <p><b>Attention:</b> every token is compared with every earlier token in one step</p>
                <ul>
                    <li><p><b>Short paths:</b> <em>el</em> and <em>estación</em> are one step apart, however long the text</p></li>
                    <li><p><b>Parallel:</b> all positions are computed at once, which suits GPUs (<a href="https://proceedings.neurips.cc/paper_files/paper/2017/file/3f5ee243547dee91fbd053c1c4a845aa-Paper.pdf">Vaswani et al., 2017</a>)</p></li>
                </ul>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
