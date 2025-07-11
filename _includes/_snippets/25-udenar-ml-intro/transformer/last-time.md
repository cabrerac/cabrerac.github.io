<!-- SLIDES: -->

## Hyperparameters Tuning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="https://upload.wikimedia.org/wikipedia/commons/1/15/Neural_Network.svg" alt="Deep Neural Network" style="max-width: 100%; height: auto;">
                <div class="footnote">Deep Neural Network with multiple hidden layers - QuantuMechaniX8, CC0, via Wikimedia Commons</div>
            </div>
            <div class="column vertical-top text-left" style="width: 50%">
                <p>There is not a straight single answer to determine the "right" hyperparameter values. But, experts follow similar steps:</p>
            <ol>
                <li>Become one with the data</li>
                <li>Set up the end-to-end training/evaluation skeleton</li> 
                <li>Start with a simple model. For most of the tasks, a fully-connected neural network with one hidden layer.</li>
                <li>Implement a complex model that overfits and regularise</li>
                <li>Tune the hyperparameters</li>
                <li>Continue training</li>
            </ol>
            <p>See more in <a href="https://karpathy.github.io/2019/04/25/recipe/">Karpathy's recipe</a>, and <a href="https://fullstackdeeplearning.com/spring2021/lecture-7/#:~:text=2%20%2D%20Strategy%20to%20Debug%20Neural,8%20%2D%20Conclusion">Tobin's lecture</a>.</p> 
            </div>
        </div>
    </div>
</div>

## Reinforcement Learning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p>Reinforcement learning is a computational approach to learning from interaction with an environment to achieve a goal through <b>trial and error</b>. An agent learns to make decisions 
                by receiving <b>rewards or penalties</b> (i.e., reinforcements) for its actions.</p>
            </div>
        </div>
    </div>
</div>

## Reinforcement Learning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/search-problem-instance-uninf.svg" alt="Search Agent Uninformed" style="max-width: 100%; height: auto;">
                <div class="footnote">Agent in an uninformed search problem.</div>
            </div>
            <div class="column vertical-top text-left" style="width: 50%">
                <p>The agent aims to <b>maximise the rewards</b> from its actions. Rewards can be <b>immediate or sparse</b>.</p>
                <p>Providing a reward signal is easier than providing labelled examples (i.e., supervised learning).</p>
                <img class="external-svg" src="https://upload.wikimedia.org/wikipedia/commons/1/1b/Reinforcement_learning_diagram.svg" alt="RL Framework" style="max-width: 100%; height: auto;">
                <div class="footnote">Reinforcement Learning Framework - Megajuice, CC0, via Wikimedia Commons.</div>
            </div>
        </div>
    </div>
</div>

## Reinforcement Learning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="https://upload.wikimedia.org/wikipedia/commons/1/1b/Reinforcement_learning_diagram.svg" alt="RL Framework" style="max-width: 100%; height: auto;">
                <div class="footnote">Reinforcement Learning Framework - Megajuice, CC0, via Wikimedia Commons.</div>
            </div>
            <div class="column vertical-top text-left" style="width: 50%">
                <br>
                <p>The RL framework is composed of:</p>
                <br>
                <ul>
                    <li><b>Agent:</b> The learner and decision maker</li>
                    <li><b>Environment:</b> The world in which the agent operates</li>
                    <li><b>State:</b> Current situation of the environment</li>
                    <li><b>Action:</b> What the agent can do</li>
                    <li><b>Reward:</b> Feedback from the environment</li>
                </ul>
                <p><b>The environment is stochastic</b>, meaning that the outcomes of actions taken by the agent in each state are not deterministic.</p>
            </div>
        </div>
    </div>
</div>

## Reinforcement Learning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="https://upload.wikimedia.org/wikipedia/commons/a/ad/Markov_Decision_Process.svg" alt="MDP Process" style="max-width: 100%; height: auto;">
                <div class="footnote">Markov Decision Process - waldoalvarez, CC BY-SA 4.0 <https://creativecommons.org/licenses/by-sa/4.0>, via Wikimedia Commons.</div>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Markov Decision Process (MDP):</b></p>
                <p>A mathematical framework for modeling sequential decisions problems for fully observable, stochastic environments. The outcomes are partly random and partly under the control of a decision maker.</p>
            </div>
        </div>
    </div>
</div>

## Reinforcement Learning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="https://upload.wikimedia.org/wikipedia/commons/1/1b/Reinforcement_learning_diagram.svg" alt="RL Framework" style="max-width: 100%; height: auto;">
                <div class="footnote">Reinforcement Learning Framework - Megajuice, CC0, via Wikimedia Commons.</div>
            </div>
            <div class="column vertical-top text-left" style="width: 50%">
            <br>
            <p>A <b>MDP</b> is a 4-tuple:</p>
<br>
$$
(S, A(s), P(s'|s,a), R(s,a,s'))
$$
<br>Where:
<br>
$S$ is a set of states with initial state $s_0$
$A(s)$ is a set of actions in each state
$P(s'|s,a)$ is a <b>transition model</b> that tells the probability of reaching $s'$, if the agent is in $s$ and performs action $a$
$R(s,a,s')$ is the  <b>reward function</b> that tells the reward for every transition from $s$ to $s'$ through $a$
</div>
        </div>
    </div>
</div>

## Reinforcement Learning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
<br>
<p>The <b>transition model</b> describes the outcome of each action in each state. Since the outcome is stochastic, we write:</p>
<br>
$$
P(s'|s,a)
$$
<br><b>Transitions are Markovian</b>: The probability of reaching $s'$ from $s$ depends only on $s$ and not on the history or earlier states.
<br><b>Uncertainty</b> once again brings MDPs closer to reality when compared against deterministic approaches.    
</div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="https://upload.wikimedia.org/wikipedia/commons/a/ad/Markov_Decision_Process.svg" alt="MDP Process" style="max-width: 100%; height: auto;">
                <div class="footnote">Markov Decision Process - waldoalvarez, CC BY-SA 4.0 <https://creativecommons.org/licenses/by-sa/4.0>, via Wikimedia Commons.</div>
            </div>  
        </div>
    </div>
</div>

## Reinforcement Learning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
<br>
<p>From every transition the agent receives a reward:</p>
<br>
$$
R(s,a,s')
$$
<br>The agent wants to <b>maximise</b> the sum of the <b>received rewards</b> (i.e., utility function):
<br>
$$
U_h=([s_0, a_0, s_1, a_1, ...,s_n])
$$
<br>The utility function $U_h$ depends on a sequence of states and actions named the <b>environment history</b>.
</div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="https://upload.wikimedia.org/wikipedia/commons/a/ad/Markov_Decision_Process.svg" alt="MDP Process" style="max-width: 100%; height: auto;">
                <div class="footnote">Markov Decision Process - waldoalvarez, CC BY-SA 4.0 <https://creativecommons.org/licenses/by-sa/4.0>, via Wikimedia Commons.</div>
            </div>  
        </div>
    </div>
</div>

## Reinforcement Learning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
<br>
<p>The solution for this problem is called a <b>policy</b>, which specifies what the agent should do for any state that the agent might reach. A policy is a mapping from states to actions 
that tells the agent what to do in each state:</p>
<br>
<p><b>Deterministic Policy:</b></p>
$$
\pi: S \rightarrow A
$$
<br><b>Stochastic Policy:</b>
$$
\pi: S \times A \rightarrow [0,1]
$$
where $\pi(s,a)$ is the probability of taking action $a$ in state $s$.
</div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/rl-policy.png" alt="RL Policy" style="max-width: 100%; height: auto;">
                <div class="footnote">Reinforcement Learning Policy.</div>
            </div>  
        </div>
    </div>
</div>

## Reinforcement Learning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
<br>
<p>The <b>quality of the policy</b> in a given state is measured by the expected utility of the possible environment histories generated by that policy. We can compute the utility of state 
sequences using additive (discounted) rewards as follows:</p>
<br>
$$
U_h=([s_0, a_0, s_1, a_1, s_2, ...]) = R(s_0, a_0, s_1) + \gamma R(s_1, a_1, s_2) + \gamma^2 R(s_2, a_2, s_3) + ...
$$
<br>where $\gamma \in [0,1]$ is the discount factor that determines the importance of future rewards.
<br>The expected utility of executing the policy $\pi$, starting in state $s$, is given by:
<br>
$$
U^\pi(s) = \mathbb{E}_\pi\left[\sum_{t=0}^{\infty} \gamma^t R(s_t, a_t, s_{t+1}) \mid s_0 = s\right]
$$
$\mathbb{E}$ is with respect to the probability distribution over state sequences determined by $s$ and $\pi$.
</div>
        </div>
    </div>
</div>

## Reinforcement Learning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
<br>
<p>We can compare policies at a given state using their expected utilities:</p>
<br>
$$
U^\pi(s) = \mathbb{E}_\pi\left[\sum_{t=0}^{\infty} \gamma^t R(s_t, a_t, s_{t+1}) \mid s_0 = s\right]
$$
$\mathbb{E}$ is with respect to the probability distribution over state sequences determined by $s$ and $\pi$.
<br>The goal is to select the policy $\pi^*$ that maximises the expected reward:
<br>
$$
\pi^*(s) = \arg\max_{\pi} U^\pi(s)
$$
<br>The policy $\pi^*(s)$ recommends an action for every state in the sequence starting in state $s$.
</div>
        </div>
    </div>
</div>

## Reinforcement Learning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <br>
                <p>The utility function allows the agent to <b>select actions by using the principle of maximum expected utility</b>. The agent chooses the action that maximises the reward for
                the next step plus the expected discounted utility of the subsequent step:</p>
<br>
$$
\pi^*(s) = \arg\max_{a \in A(s)} \sum_{s'} P(s'|s,a) [R(s,a,s') + \gamma U(s')]
$$
<br>The utility of a state is the expected reward for the next transition plus the discounted utility of the next state, assuming that the agent chooses the optimal action. The utility of a state
is given by:
$$
U(s) = \max_{a \in A(s)} \sum_{s'} P(s'|s,a) [R(s,a,s') + \gamma U(s')]
$$
<br>This is called <b>the Bellman Equation</b>, after Richard Bellman (1957). 
</div>
        </div>
    </div>
</div>

## Reinforcement Learning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/rl-value-function.png" alt="Value Function" style="max-width: 100%; height: auto;">
                <div class="footnote">Value Function.</div>
            </div>
        </div>
    </div>
</div>

## Reinforcement Learning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <br>
                <p>Another important quantity is <b>the action-utility function</b> or <em>Q-function</em>, which is the expected utility of taking a giving action in a given state:</p>
<br>
$$
Q(s,a) = \sum_{s'} P(s'|s,a) [R(s,a,s') + \gamma U(s')]
$$
<br>The <em>Q-function</em> tells us how good it is to take action $a$ in state $s$.
<br>The optimal policy can be extracted from $Q(s,a)$ as follows:
<br>
$$
\pi^*(s) = \arg\max_{a} Q(s,a)
$$
</div>
        </div>
    </div>
</div>

## Reinforcement Learning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/q-table-final.png" alt="Q-Matrix" style="max-width: 100%; height: auto;">
                <div class="footnote">Q-Matrix</div>
            </div>
        </div>
    </div>
</div>

## Reinforcement Learning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 60%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <img class="external-svg" src="https://upload.wikimedia.org/wikipedia/commons/1/1b/Reinforcement_learning_diagram.svg" alt="RL Framework" style="max-width: 100%; height: auto;">
                <div class="footnote">Reinforcement Learning Framework - Megajuice, CC0, via Wikimedia Commons.</div>
            </div>
        </div>
    </div>
    <div class="row" style="height: 10%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 50%">
                <p><b>Model-Based RL Agent</b></p>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <p><b>Model-Free RL Agent</b></p>
            </div>
        </div>
    </div>
    <div class="row" style="height: 30%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
                <ul>
                    <li>Knows transition model and reward function</li>
                    <li>Can simulate outcomes before taking actions</li>
                    <li>Value Iteration, Policy Iteration</li>
                </ul>
            </div>
            <div class="column vertical-top text-left" style="width: 50%">
                <ul>
                    <li>Unknown transition model and reward function</li>
                    <li>Cannot simulate outcomes</li>
                    <li>Q-Learning, DQN</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## Reinforcement Learning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 10%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-center" style="width: 33%">
                <p><b>Policy Iteration</b></p>
            </div>
            <div class="column vertical-top text-center" style="width: 33%">
                <p><b>Q-Value</b></p>
            </div>
            <div class="column vertical-top text-center" style="width: 33%">
                <p><b>DQN</b></p>
            </div>
        </div>
    </div>
    <div class="row" style="height: 90%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 33%">
                <p><b>Value-function</b></p>
                <p>Model-based with guaranteed convergence for finite and discrete problems.</p>
                <img class="external-svg" src="https://upload.wikimedia.org/wikipedia/commons/a/ad/Markov_Decision_Process.svg" alt="MDP Process" style="max-width: 100%; height: auto;">
                <div class="footnote">Markov Decision Process - waldoalvarez, CC BY-SA 4.0, via Wikimedia Commons.</div>
            </div>
            <div class="column vertical-top text-left" style="width: 33%">
                <p><b>Q-function</b></p>
                <p>Model-free and simple for small and discrete problems.</p>
                <img src="{{ site.url }}/assets/media/images/q-table-final.png" alt="Q-Matrix" style="max-width: 100%; height: auto;">
                <div class="footnote">Transition Matrix (Q).</div>
            </div>
            <div class="column vertical-top text-left" style="width: 33%">
                <p><b>Neural Network</b></p>
                <p>Model-free and complex for large and continuous problems.</p>
                <br>
                <br>
                <img class="external-svg" src="https://upload.wikimedia.org/wikipedia/commons/1/15/Neural_Network.svg" alt="Deep Neural Network" style="max-width: 100%; height: auto;">
                <div class="footnote">Deep Neural Network with multiple hidden layers - QuantuMechaniX8, CC0, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## Reinforcement Learning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/dqn-results.png" alt="DQN Results" style="max-width: 100%; height: auto;">
                <div class="footnote">Deep Q-Network (DQN) Results - ε-decay = 0.9999</div>
            </div>
        </div>
    </div>
</div>

## Reinforcement Learning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/dqn-log.png" alt="DQN Results" style="max-width: 100%; height: auto;">
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/dqn-epsilon-decay.png" alt="DQN Results" style="max-width: 100%; height: auto;">
                <div class="footnote">Deep Q-Network (DQN) Results - ε-decay = 0.9999</div>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: --> 