<!-- SLIDES: -->

## AI Systems

## AI Systems

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <div style="font-size: 2em; margin: 40px 0;">
$$\text{model} + \text{data} \stackrel{\text{compute}}{\rightarrow} \text{prediction}$$
</div>
                <div style="margin-top: 30px;">
                </div>
            </div>
        </div>
    </div>
</div>

## AI Systems

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/context-1.png" alt="AI System" style="height: 400px">
            </div>
        </div>
    </div>
</div>

## AI Systems

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/context-2.png" alt="AI System" style="height: 400px">
            </div>
        </div>
    </div>
</div>

## AI Systems

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/context-3.png" alt="AI System" style="height: 400px">
            </div>
        </div>
    </div>
</div>

## AI Systems

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/decentralised-deployment.png" alt="Service Placement Problem" style="height: 400px">
            </div>
            <div class="column vertical-top text-left" style="width: 50%">
                <p><b>Dynamic Service Placement in Edge Computing</b></p>
                <br>
            </div>
        </div>
    </div>
</div>

## AI Systems

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/decentralised-deployment.png" alt="Service Placement Problem" style="height: 400px">
            </div>
            <div class="column vertical-top text-left" style="width: 50%">
                <p><b>Dynamic Service Placement in Edge Computing</b></p>
                <br>
                <ul>
                    <li>Edge servers are located close to end users, allowing for local data processing.</li>
                    <li>Services run on edge servers, which have limited resources.</li>
                    <li>The challenge is to determine the optimal allocation of services and edge servers to minimize latency while considering resource constraints.</li>
                    <li>This challenge is referred to as the Service Placement Problem.</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## AI Systems

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/decentralised-deployment.png" alt="Service Placement Problem" style="height: 400px">
            </div>
            <div class="column vertical-top text-left" style="width: 50%">
                <p><b>Dynamic Service Placement in Edge Computing</b></p>
                <br>
                <p>Objective Functions:</p>
<br>
$$\min_j wt_j + lat(D_j) \quad (1)$$
$$\min_i \sqrt{w_p \sigma(RR^{CPU})^2 + w_m \sigma(RR^{RAM})^2} \quad (2)$$
Subject to:
$$\sum_{k=1}^n rr_{ik}^{CPU} \leq r_i^{CPU} \quad (3)$$
$$\sum_{k=1}^n rr_{ik}^{RAM} \leq r_i^{RAM} \quad (4)$$
</div>
        </div>
    </div>
</div>

## AI Systems

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/pareto.png" alt="Pareto" style="height: 400px">
            </div>
            <div class="column vertical-top text-left" style="width: 50%">
                <p><b>Dynamic Service Placement in Edge Computing</b></p>
                <br>
                <p>Objective Functions:</p>
<br>
$$\min_j wt_j + lat(D_j) \quad (1)$$
$$\min_i \sqrt{w_p \sigma(RR^{CPU})^2 + w_m \sigma(RR^{RAM})^2} \quad (2)$$
Subject to:
$$\sum_{k=1}^n rr_{ik}^{CPU} \leq r_i^{CPU} \quad (3)$$
$$\sum_{k=1}^n rr_{ik}^{RAM} \leq r_i^{RAM} \quad (4)$$
</div>
        </div>
    </div>
</div>

## AI Systems

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/aco.png" alt="Ant-Colony Optimisation" style="height: 400px">
            </div>
            <div class="column vertical-top text-left" style="width: 50%">
                <p><b>Dynamic Service Placement in Edge Computing</b></p>
                <br>
                <p>Objective Functions:</p>
<br>
$$\min_j wt_j + lat(D_j) \quad (1)$$
$$\min_i \sqrt{w_p \sigma(RR^{CPU})^2 + w_m \sigma(RR^{RAM})^2} \quad (2)$$
Subject to:
$$\sum_{k=1}^n rr_{ik}^{CPU} \leq r_i^{CPU} \quad (3)$$
$$\sum_{k=1}^n rr_{ik}^{RAM} \leq r_i^{RAM} \quad (4)$$
</div>
        </div>
    </div>
</div>

## AI Systems

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/aco.png" alt="Ant-Colony Optimisation" style="height: 400px">
            </div>
            <div class="column vertical-top text-left" style="width: 50%">
                <p><b>Ant Colony Optimization Algorithm</b></p>
                <br>
$$P_{ij}(t) = \frac{[\tau_{ij}(t)]^\alpha \cdot [\eta_{ij}]^\beta}{\sum_{k \in N_i} [\tau_{ik}(t)]^\alpha \cdot [\eta_{ik}]^\beta} \quad (1)$$
$$\tau_{ij}(t+1) = (1-\rho) \cdot \tau_{ij}(t) + \Delta \tau_{ij}(t) \quad (2)$$
<br>Where: $P_{ij}(t)$ is the probability of moving from node $i$ to node $j$, $\tau_{ij}(t)$ is the pheromone level on edge $(i, j)$ at time $t$, $\eta_{ij}$ is the heuristic information (e.g., inverse of distance), $\alpha$ and $\beta$ are parameters to control the influence of pheromone and heuristic information, $\rho$ is the pheromone evaporation rate, $\Delta \tau_{ij}(t)$ is change in pheromone level.
</div>
        </div>
    </div>
</div>

## AI Systems

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/aco-1.png" alt="Ant-Colony Optimisation" style="height: 400px">
        </div>
    </div>
</div>

## AI Systems

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/aco-2.png" alt="Ant-Colony Optimisation" style="height: 400px">
        </div>
    </div>
</div>

## AI Systems

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/aco-3.png" alt="Ant-Colony Optimisation" style="height: 400px">
        </div>
    </div>
</div>

## AI Systems

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/aco-4.png" alt="Ant-Colony Optimisation" style="height: 400px">
        </div>
    </div>
</div>

## AI Systems

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/aco-5.png" alt="Ant-Colony Optimisation" style="height: 400px">
        </div>
    </div>
</div>

## AI Systems

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/aco-6.png" alt="Ant-Colony Optimisation" style="height: 400px">
        </div>
    </div>
</div>

## AI Systems

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/aco-7.png" alt="Ant-Colony Optimisation" style="height: 400px">
        </div>
    </div>
</div>

## AI Systems

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/aco-8.png" alt="Ant-Colony Optimisation" style="height: 400px">
        </div>
    </div>
</div>

## AI Systems

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/aco-9.png" alt="Ant-Colony Optimisation" style="height: 400px">
        </div>
    </div>
</div>

## AI Systems

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/aco-10.png" alt="Ant-Colony Optimisation" style="height: 400px">
        </div>
    </div>
</div>

## AI Systems

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/aco-11.png" alt="Ant-Colony Optimisation" style="height: 400px">
        </div>
    </div>
</div>

## AI Systems

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/aco-12.png" alt="Ant-Colony Optimisation" style="height: 400px">
        </div>
    </div>
</div>

## AI Systems

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/aco-13.png" alt="Ant-Colony Optimisation" style="height: 400px">
        </div>
    </div>
</div>

## AI Systems

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/aco-14.png" alt="Ant-Colony Optimisation" style="height: 400px">
        </div>
    </div>
</div>

<!-- end SLIDES: -->

- why is this important (maaco paper)
- infrastructure (hardware decisions)
- software decisions (oop, monolithic, soa, doa)