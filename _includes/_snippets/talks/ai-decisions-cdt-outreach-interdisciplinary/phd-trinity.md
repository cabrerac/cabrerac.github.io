<!-- SLIDES: -->

## Self-Adaptive Service Discovery

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>The problem:</b> large environments require autonomous service-oriented architectures.</p>
                <br>
                <p><b>The goal:</b> enable self-adaptive service discovery in dynamic urban environments. Service architectures should reorganise themselves in response to changing urban conditions.</p>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/adaptive-service-discovery.png" alt="Self-adaptive service discovery architecture" style="height: 400px">
            </div>
        </div>
    </div>
</div>

## Self-Adaptive Service Discovery

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>I tried to use a RL-based approach which <b>did not work</b> as expected in realistic conditions mainy because:</p>
                <ul>
                    <li>The real world was far more complex than the models assumed</li>
                    <li>My own knowledge of RL and its limitations was still developing</li>
                </ul>
                <br>
                <p>This was a <b>negative result</b>, but it became part of my PhD thesis. Negative results are not failures, they are an honest account of what we tried and what we learned.</p>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/rl-negative-result.png" alt="RL experiments — negative results" style="height: 400px">
            </div>
        </div>
    </div>
</div>

## Self-Adaptive Service Discovery

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>The experiments started to work when I introduced <b>strong assumptions</b>, simplifying the environment until it no longer reflected the real world.</p>
                <br>
                <p>RL worked, but only in a <b>very limited and controlled setting</b>.</p>
                <br>
                <p>This was the realisation: <b>ML can work in isolation, but deploying it in real-world environments is a fundamentally different challenge.</b></p>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/q-table-final.png" alt="RL experiments — working under assumptions" style="height: 400px">
            </div>
        </div>
    </div>
</div>

## Self-Adaptive Service Discovery

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>The experiments started to work when I introduced <b>strong assumptions</b>, simplifying the environment until it no longer reflected the real world.</p>
                <br>
                <p>RL worked, but only in a <b>very limited and controlled setting</b>.</p>
                <br>
                <p><b>ML can work in isolation, but deploying it in real-world environments is a fundamentally different challenge.</b></p>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/rl-working.png" alt="RL experiments — working under assumptions" style="height: 400px">
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
