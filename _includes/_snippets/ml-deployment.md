<!-- SLIDES: -->

## ML Deployment

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <img class="external-svg" src="https://upload.wikimedia.org/wikipedia/commons/4/42/Shaba_Kenya_river.jpg" alt="Ewaso Nyiro River" style="height: 500px">
                <div class="footnote">Ewaso Nyiro River - Kenya: Marc Samsom, CC BY 2.0 <https://creativecommons.org/licenses/by/2.0>, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## ML Deployment

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="https://upload.wikimedia.org/wikipedia/commons/4/42/Shaba_Kenya_river.jpg" alt="Ewaso Nyiro River" style="height: 500px">
                <div class="footnote">Ewaso Nyiro River - Kenya: Marc Samsom, CC BY 2.0 <https://creativecommons.org/licenses/by/2.0>, via Wikimedia Commons</div>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/water-level-dekut.png" alt="Water Level Monitoring" style="height: 400px">
                <div class="footnote">Water Level Monitoring System at DeKUT (Kabi & Maina, 2021)</div>
            </div>
        </div>
    </div>
</div>

## ML Deployment

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/water-level-architecture.png" alt="Water Level Monitoring System Architecture" style="height: 500px">
                <div class="footnote">Water Level Monitoring System Architecture</div>
            </div>
        </div>
    </div>
</div>

## ML Deployment

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/water-level-architecture-ml-component.png" alt="Water Level Monitoring System Architecture" style="height: 500px">
                <div class="footnote">Water Level Monitoring System Architecture</div>
            </div>
        </div>
    </div>
</div>

## ML Deployment

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

## ML Deployment

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

## ML Deployment

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

## ML Deployment

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <img src="{{ site.url }}/assets/media/images/aco-14.png" alt="Ant-Colony Optimisation" style="height: 600px">
            </div>
        </div>
    </div>
</div>

## AI Systems

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <img src="{{ site.url }}/assets/media/images/aco-solution.png" alt="ACO Smart City" style="height: 600px">
            </div>
        </div>
    </div>
</div>

## ML Deployment

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
                <br>
                <p><b>Hardware considerations:</b></p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/water-level-dekut.png" alt="Water Level Monitoring" style="height: 400px">
                <div class="footnote">Water Level Monitoring System at DeKUT (Kabi & Maina, 2021)</div>
            </div>
        </div>
    </div>
</div>

## ML Deployment

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
                <br>
                <p><b>Hardware considerations:</b></p>
                <ul>
                    <li><b>Data Collection:</b> Ensure sufficient storage capacity for large datasets and high-speed data transfer capabilities.</li>
                    <li><b>Model Training:</b> Invest in powerful GPUs or TPUs to handle intensive computations and reduce training time.</li>
                    <li><b>Model Deployment:</b> Consider edge devices for real-time processing and scalability of the deployment infrastructure.</li>
                    <li><b>Maintenance and Updates:</b> Plan for hardware upgrades and maintenance to accommodate evolving model requirements.</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/water-level-dekut.png" alt="Water Level Monitoring" style="height: 400px">
                <div class="footnote">Water Level Monitoring System at DeKUT (Kabi & Maina, 2021)</div>
            </div>
        </div>
    </div>
</div>

## ML Deployment

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
                <br>
                <p><b>Software considerations:</b></p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/context-3.png" alt="AI System" style="height: 400px">
            </div>
        </div>
    </div>
</div>

## ML Deployment

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
                <br>
                <p><b>Software considerations:</b></p>
                <ul>
                    <li><b>Data Management:</b> Implement efficient data preprocessing and cleaning pipelines to ensure high-quality input for models.</li>
                    <li><b>Model Development:</b> Utilize frameworks like TensorFlow or PyTorch for building and experimenting with different model architectures.</li>
                    <li><b>Version Control:</b> Use tools like Git to manage code versions and collaborate effectively with team members.</li>
                    <li><b>Continuous Integration/Continuous Deployment (CI/CD):</b> Set up automated testing and deployment pipelines to streamline updates and ensure reliability.</li>
                    <li><b>Scalability:</b> Design software architecture to support scaling, such as using microservices or serverless computing for flexible resource management.</li>
                    <li><b>Security:</b> Implement robust security measures to protect data privacy and model integrity.</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/context-3.png" alt="AI System" style="height: 400px">
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->