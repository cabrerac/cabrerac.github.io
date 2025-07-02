<!-- SLIDES: -->

## Reinforcement Learning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p>Reinforcement learning is a computational approach to learning from interaction with an environment to achieve a goal through <b>trial and error</b>, where an agent learns to make decisions by receiving rewards or penalties for its actions.</p>
            </div>
        </div>
    </div>
</div>

## Reinforcement Learning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/reinforcement-learning.svg" alt="Reinforcement Learning Framework" style="max-width: 100%; height: auto;">
                <div class="footnote">Reinforcement Learning Framework.</div>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Key Components:</b></p>
                <ul>
                    <li><b>Agent:</b> The learner and decision maker</li>
                    <li><b>Environment:</b> The world in which the agent operates</li>
                    <li><b>State:</b> Current situation of the environment</li>
                    <li><b>Action:</b> What the agent can do</li>
                    <li><b>Reward:</b> Feedback from the environment</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## Reinforcement Learning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p><b>Unlike supervised learning</b>, reinforcement learning does not have labeled examples of correct behavior. Instead, the agent must discover which actions lead to the highest rewards through exploration and experience.</p>
            </div>
        </div>
    </div>
</div>

## Reinforcement Learning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
                <p><b>Markov Decision Process (MDP):</b></p>
                <p>A mathematical framework for modeling decision-making in situations where outcomes are partly random and partly under the control of a decision maker.</p>
                <br>
                <p><b>Components:</b></p>
                <ul>
                    <li><b>S:</b> Set of states</li>
                    <li><b>A:</b> Set of actions</li>
                    <li><b>P:</b> State transition function</li>
                    <li><b>R:</b> Reward function</li>
                    <li><b>γ:</b> Discount factor</li>
                </ul>
            </div>
            <div class="column vertical-top text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/mdp.svg" alt="Markov Decision Process" style="max-width: 100%; height: auto;">
                <div class="footnote">Markov Decision Process.</div>
            </div>
        </div>
    </div>
</div>

## Reinforcement Learning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
                <p><b>Policy (π):</b></p>
                <p>A policy is a mapping from states to actions that tells the agent what to do in each state.</p>
                <br>
                <p><b>Deterministic Policy:</b></p>
                $$
                \pi: S \rightarrow A
                $$
                <br>
                <p><b>Stochastic Policy:</b></p>
                $$
                \pi: S \times A \rightarrow [0,1]
                $$
                <br>
                <p>where $\pi(s,a)$ is the probability of taking action $a$ in state $s$.</p>
            </div>
            <div class="column vertical-top text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/policy.svg" alt="Policy Function" style="max-width: 100%; height: auto;">
                <div class="footnote">Policy Function.</div>
            </div>
        </div>
    </div>
</div>

## Reinforcement Learning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
                <p><b>Value Function:</b></p>
                <p>The value function $V^\pi(s)$ represents the expected cumulative reward starting from state $s$ and following policy $\pi$.</p>
                <br>
                <p><b>State Value Function:</b></p>
                $$
                V^\pi(s) = \mathbb{E}_\pi\left[\sum_{k=0}^{\infty} \gamma^k R_{t+k+1} \mid S_t = s\right]
                $$
                <br>
                <p>where $\gamma \in [0,1]$ is the discount factor that determines the importance of future rewards.</p>
            </div>
            <div class="column vertical-top text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/value-function.svg" alt="Value Function" style="max-width: 100%; height: auto;">
                <div class="footnote">Value Function.</div>
            </div>
        </div>
    </div>
</div>

## Reinforcement Learning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
                <p><b>Q-Function (Action-Value Function):</b></p>
                <p>The Q-function $Q^\pi(s,a)$ represents the expected cumulative reward starting from state $s$, taking action $a$, and then following policy $\pi$.</p>
                <br>
                <p><b>Action-Value Function:</b></p>
                $$
                Q^\pi(s,a) = \mathbb{E}_\pi\left[\sum_{k=0}^{\infty} \gamma^k R_{t+k+1} \mid S_t = s, A_t = a\right]
                $$
                <br>
                <p>The Q-function tells us how good it is to take action $a$ in state $s$.</p>
            </div>
            <div class="column vertical-top text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/q-function.svg" alt="Q-Function" style="max-width: 100%; height: auto;">
                <div class="footnote">Q-Function.</div>
            </div>
        </div>
    </div>
</div>

## Reinforcement Learning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
                <p><b>Bellman Equation:</b></p>
                <p>The Bellman equation expresses the relationship between the value of a state and the values of its successor states.</p>
                <br>
                <p><b>State Value Bellman Equation:</b></p>
                $$
                V^\pi(s) = \sum_{a} \pi(s,a) \sum_{s'} P(s'|s,a) [R(s,a,s') + \gamma V^\pi(s')]
                $$
                <br>
                <p>This equation states that the value of a state equals the expected immediate reward plus the discounted value of the next state.</p>
            </div>
            <div class="column vertical-top text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/bellman-equation.svg" alt="Bellman Equation" style="max-width: 100%; height: auto;">
                <div class="footnote">Bellman Equation.</div>
            </div>
        </div>
    </div>
</div>

## Reinforcement Learning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
                <p><b>Q-Function Bellman Equation:</b></p>
                <p>The Bellman equation for the Q-function expresses the relationship between the Q-value of a state-action pair and the Q-values of subsequent state-action pairs.</p>
                <br>
                <p><b>Q-Function Bellman Equation:</b></p>
                $$
                Q^\pi(s,a) = \sum_{s'} P(s'|s,a) [R(s,a,s') + \gamma \sum_{a'} \pi(s',a') Q^\pi(s',a')]
                $$
                <br>
                <p>This equation states that the Q-value equals the expected immediate reward plus the discounted expected Q-value of the next state-action pair.</p>
            </div>
            <div class="column vertical-top text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/q-bellman.svg" alt="Q-Function Bellman Equation" style="max-width: 100%; height: auto;">
                <div class="footnote">Q-Function Bellman Equation.</div>
            </div>
        </div>
    </div>
</div>

## Reinforcement Learning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p><b>Optimal Policy:</b> A policy $\pi^*$ is optimal if it achieves the highest expected cumulative reward for all states.</p>
                <br>
                <p><b>Optimal Value Function:</b></p>
                $$
                V^*(s) = \max_\pi V^\pi(s)
                $$
                <br>
                <p><b>Optimal Q-Function:</b></p>
                $$
                Q^*(s,a) = \max_\pi Q^\pi(s,a)
                $$
            </div>
        </div>
    </div>
</div>

## Reinforcement Learning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
                <p><b>Optimal Bellman Equation:</b></p>
                <p>The optimal value function satisfies the Bellman optimality equation:</p>
                <br>
                <p><b>State Value Optimality:</b></p>
                $$
                V^*(s) = \max_a \sum_{s'} P(s'|s,a) [R(s,a,s') + \gamma V^*(s')]
                $$
                <br>
                <p><b>Q-Function Optimality:</b></p>
                $$
                Q^*(s,a) = \sum_{s'} P(s'|s,a) [R(s,a,s') + \gamma \max_{a'} Q^*(s',a')]
                $$
            </div>
            <div class="column vertical-top text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/optimal-bellman.svg" alt="Optimal Bellman Equation" style="max-width: 100%; height: auto;">
                <div class="footnote">Optimal Bellman Equation.</div>
            </div>
        </div>
    </div>
</div>

## Reinforcement Learning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p><b>Value Iteration Algorithm:</b></p>
                <p>An iterative algorithm to find the optimal value function and policy.</p>
                <br>
                <pre><code>Value Iteration Algorithm:
Initialize V(s) = 0 for all s
repeat
    for each state s:
        V(s) = max_a Σ_s' P(s'|s,a) [R(s,a,s') + γV(s')]
until convergence
Extract optimal policy: π*(s) = argmax_a Σ_s' P(s'|s,a) [R(s,a,s') + γV*(s')]
</code></pre>
            </div>
        </div>
    </div>
</div>

## Reinforcement Learning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
                <p><b>Q-Learning:</b></p>
                <p>A model-free reinforcement learning algorithm that learns the optimal action-value function directly from experience.</p>
                <br>
                <p><b>Q-Learning Update Rule:</b></p>
                $$
                Q(s,a) \leftarrow Q(s,a) + \alpha [R(s,a,s') + \gamma \max_{a'} Q(s',a') - Q(s,a)]
                $$
                <br>
                <p>where $\alpha$ is the learning rate and the term in brackets is the temporal difference error.</p>
            </div>
            <div class="column vertical-top text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/q-learning.svg" alt="Q-Learning" style="max-width: 100%; height: auto;">
                <div class="footnote">Q-Learning Algorithm.</div>
            </div>
        </div>
    </div>
</div>

## Reinforcement Learning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p><b>Exploration vs Exploitation:</b></p>
                <p>The fundamental trade-off in reinforcement learning between exploring new actions to discover better strategies and exploiting current knowledge to maximize immediate rewards.</p>
                <br>
                <p><b>ε-Greedy Policy:</b></p>
                $$
                \pi(s) = \begin{cases}
                \text{random action} & \text{with probability } \epsilon \\
                \arg\max_a Q(s,a) & \text{with probability } 1-\epsilon
                \end{cases}
                $$
            </div>
        </div>
    </div>
</div>

## Reinforcement Learning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
                <p><b>Policy Gradient Methods:</b></p>
                <p>Instead of learning value functions, policy gradient methods directly parameterize the policy and optimize it using gradient ascent.</p>
                <br>
                <p><b>Policy Parameterization:</b></p>
                $$
                \pi_\theta(s,a) = P(a|s,\theta)
                $$
                <br>
                <p><b>Objective Function:</b></p>
                $$
                J(\theta) = \mathbb{E}_{\pi_\theta}[R(\tau)]
                $$
                <br>
                <p>where $R(\tau)$ is the total reward of trajectory $\tau$.</p>
            </div>
            <div class="column vertical-top text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/policy-gradient.svg" alt="Policy Gradient" style="max-width: 100%; height: auto;">
                <div class="footnote">Policy Gradient Methods.</div>
            </div>
        </div>
    </div>
</div>

## Reinforcement Learning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
                <p><b>REINFORCE Algorithm:</b></p>
                <p>A policy gradient algorithm that uses the likelihood ratio trick to estimate the gradient.</p>
                <br>
                <p><b>Policy Gradient Theorem:</b></p>
                $$
                \nabla_\theta J(\theta) = \mathbb{E}_{\pi_\theta}[\nabla_\theta \log \pi_\theta(s,a) R(\tau)]
                $$
                <br>
                <p><b>REINFORCE Update:</b></p>
                $$
                \theta \leftarrow \theta + \alpha \nabla_\theta \log \pi_\theta(s,a) R(\tau)
                $$
            </div>
            <div class="column vertical-top text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/reinforce.svg" alt="REINFORCE Algorithm" style="max-width: 100%; height: auto;">
                <div class="footnote">REINFORCE Algorithm.</div>
            </div>
        </div>
    </div>
</div>

## Reinforcement Learning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p><b>Applications of Reinforcement Learning:</b></p>
                <br>
                <ul>
                    <li><b>Game Playing:</b> AlphaGo, AlphaZero, Atari games</li>
                    <li><b>Robotics:</b> Robot navigation, manipulation, locomotion</li>
                    <li><b>Autonomous Systems:</b> Self-driving cars, drones</li>
                    <li><b>Resource Management:</b> Inventory control, energy management</li>
                    <li><b>Recommendation Systems:</b> Personalized content delivery</li>
                    <li><b>Finance:</b> Algorithmic trading, portfolio optimization</li>
                </ul>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: --> 