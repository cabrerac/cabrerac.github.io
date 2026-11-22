<!-- SLIDES: -->

## DOAgent

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 55%">
               <img class="external-svg" src="{{ site.url }}/assets/media/diagrams/doagent-architecture.svg" alt="DOAgent Architecture" style="height: 480px">
            </div>
            <div class="column vertical-middle text-left" style="width: 45%">
                <p>A <b>data-oriented library</b> for multi-agent systems. Agents coordinate through shared records.</p>
                <p><b>Records:</b> agent_update (each decision), outcome (each state), trace (cause and effect links).</p>
                <p><b>Logging levels:</b></p>
                <ul>
                    <li>Level 0: agent_update + outcome</li>
                    <li>Level 1: + trace + provenance + accountability</li>
                    <li>Level 2: + explanation + reasoning</li>
                </ul>
                <p><img class="external-svg" src="{{ site.url }}/assets/media/images/doagent-qr.png" alt="DOAgent QR Code" style="height: 80px; vertical-align: middle;"> <b><a href="https://github.com/cabrerac/doagent" target="_blank" rel="noopener noreferrer">GitHub repo</a></b></p>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
