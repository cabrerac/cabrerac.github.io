<!-- SLIDES: -->

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
                <p>Providing a reward signal is easier than providing labeled examples (i.e., supervised learning).</p>
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
                <p>Providing a reward signal is easier than providing labeled examples (i.e., supervised learning).</p>
                <img src="https://upload.wikimedia.org/wikipedia/commons/1/1b/Reinforcement_learning_diagram.svg" alt="RL Framework" style="max-width: 100%; height: auto;">
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
                <img src="https://upload.wikimedia.org/wikipedia/commons/1/1b/Reinforcement_learning_diagram.svg" alt="RL Framework" style="max-width: 100%; height: auto;">
                <div class="footnote">Reinforcement Learning Framework - Megajuice, CC0, via Wikimedia Commons.</div>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
            </div>
        </div>
    </div>
</div>


## Reinforcement Learning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="https://upload.wikimedia.org/wikipedia/commons/1/1b/Reinforcement_learning_diagram.svg" alt="RL Framework" style="max-width: 100%; height: auto;">
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
            </div>
        </div>
    </div>
</div>

## Reinforcement Learning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="https://upload.wikimedia.org/wikipedia/commons/1/1b/Reinforcement_learning_diagram.svg" alt="RL Framework" style="max-width: 100%; height: auto;">
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
                <img src="https://upload.wikimedia.org/wikipedia/commons/1/1b/Reinforcement_learning_diagram.svg" alt="RL Framework" style="max-width: 100%; height: auto;">
                <div class="footnote">Reinforcement Learning Framework - Megajuice, CC0, via Wikimedia Commons.</div>
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
                <img src="https://upload.wikimedia.org/wikipedia/commons/a/ad/Markov_Decision_Process.svg" alt="MDP Process" style="max-width: 100%; height: auto;">
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
                <img src="https://upload.wikimedia.org/wikipedia/commons/1/1b/Reinforcement_learning_diagram.svg" alt="RL Framework" style="max-width: 100%; height: auto;">
                <div class="footnote">Reinforcement Learning Framework - Megajuice, CC0, via Wikimedia Commons.</div>
            </div>
            <div class="column vertical-top text-left" style="width: 50%">
            <br>
            <p>A <b>MDP</b> is a 4-tuple:</p>
<br>
$$
(S, A(s), P(s'|s,a), R(s,a,s'))
$$
</div>
        </div>
    </div>
</div>

## Reinforcement Learning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="https://upload.wikimedia.org/wikipedia/commons/1/1b/Reinforcement_learning_diagram.svg" alt="RL Framework" style="max-width: 100%; height: auto;">
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
</div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="https://upload.wikimedia.org/wikipedia/commons/a/ad/Markov_Decision_Process.svg" alt="MDP Process" style="max-width: 100%; height: auto;">
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
<p>The <b>transition model</b> describes the outcome of each action in each state. Since the outcome is stochastic, we write:</p>
<br>
$$
P(s'|s,a)
$$
<br><b>Transitions are Markovian</b>: The probability of reaching $s'$ from $s$ depends only on $s$ and not on the history or earlier states.
<br><b>Uncertainty</b> once again brings MDPs closer to reality when compared against deterministic approaches.    
</div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="https://upload.wikimedia.org/wikipedia/commons/a/ad/Markov_Decision_Process.svg" alt="MDP Process" style="max-width: 100%; height: auto;">
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
</div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="https://upload.wikimedia.org/wikipedia/commons/a/ad/Markov_Decision_Process.svg" alt="MDP Process" style="max-width: 100%; height: auto;">
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
                <img src="https://upload.wikimedia.org/wikipedia/commons/a/ad/Markov_Decision_Process.svg" alt="MDP Process" style="max-width: 100%; height: auto;">
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
<p>The solution for this problem is called a <b>policy</b>, which specifies what the agent should do for any state that the agent might reach. A policy is a mapping from states 
to actions that tells the agent what to do in each state:</p>
<br>
<p><b>Deterministic Policy:</b></p>
$$
\pi: S \rightarrow A
$$
</div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="https://upload.wikimedia.org/wikipedia/commons/a/ad/Markov_Decision_Process.svg" alt="MDP Process" style="max-width: 100%; height: auto;">
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
                <img src="https://upload.wikimedia.org/wikipedia/commons/a/ad/Markov_Decision_Process.svg" alt="MDP Process" style="max-width: 100%; height: auto;">
                <div class="footnote">Markov Decision Process - waldoalvarez, CC BY-SA 4.0 <https://creativecommons.org/licenses/by-sa/4.0>, via Wikimedia Commons.</div>
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
                the next step plus the expected discounted utility of the subsequente step:</p>
<br>
$$
\pi^*(s) = \arg\max_{a \in A(s)} \sum_{s'} P(s'|s,a) [R(s,a,s') + \gamma U(s')]
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
                <br>
                <p>The utility function allows the agent to <b>select actions by using the principle of maximum expected utility</b>. The agent chooses the action that maximises the reward for
                the next step plus the expected discounted utility of the subsequente step:</p>
<br>
$$
\pi^*(s) = \arg\max_{a \in A(s)} \sum_{s'} P(s'|s,a) [R(s,a,s') + \gamma U(s')]
$$
<br>The utility of a state is the expected reward for the next transition plus the discounted utility of the next state, assumming that the agent chooses the optimal action. The utility of a state
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
                <br>
                <p>Another important quantity is <b>the action-utility function</b> or <em>Q-function</em>, which is the expected utility of taking a giving action in a given state:</p>
<br>
$$
Q(s,a) = \sum_{s'} P(s'|s,a) [R(s,a,s') + \gamma U(s')]
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
                <br>
                <p>Another important quantity is <b>the action-utility function</b> or <em>Q-function</em>, which is the expected utility of taking a giving action in a given state:</p>
<br>
$$
Q(s,a) = \sum_{s'} P(s'|s,a) [R(s,a,s') + \gamma U(s')]
$$
<br>$Q(s,a)$ relates to the utility function as follows:
<br>
$$
U(s) = \max_{a} Q(s,a)
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
                <br>
                <p>Another important quantity is <b>the action-utility function</b> or <em>Q-function</em>, which is the expected utility of taking a giving action in a given state:</p>
<br>
$$
Q(s,a) = \sum_{s'} P(s'|s,a) [R(s,a,s') + \gamma U(s')]
$$
<br>$Q(s,a)$ relates to the utility function as follows:
<br>
$$
U(s) = \max_{a} Q(s,a)
$$
<br>Then we have:
$$
Q(s,a) = \sum_{s'} P(s'|s,a) [R(s,a,s') + \gamma \max_{a'} Q(s',a')]
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
                <br>
                <p>Another important quantity is <b>the action-utility function</b> or <em>Q-function</em>, which is the expected utility of taking a giving action in a given state:</p>
<br>
$$
Q(s,a) = \sum_{s'} P(s'|s,a) [R(s,a,s') + \gamma U(s')]
$$
<br>The <em>Q-function</em> tells us how good it is to take action $a$ in state $s$.
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
    <div class="row" style="height: 60%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <img src="https://upload.wikimedia.org/wikipedia/commons/1/1b/Reinforcement_learning_diagram.svg" alt="RL Framework" style="max-width: 100%; height: auto;">
                <div class="footnote">Reinforcement Learning Framework - Megajuice, CC0, via Wikimedia Commons.</div>
            </div>
        </div>
    </div>
    <div class="row" style="height: 10%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 50%">
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
            </div>
        </div>
    </div>
    <div class="row" style="height: 30%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
            </div>
            <div class="column vertical-top text-left" style="width: 50%">
            </div>
        </div>
    </div>
</div>

## Reinforcement Learning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 60%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <img src="https://upload.wikimedia.org/wikipedia/commons/1/1b/Reinforcement_learning_diagram.svg" alt="RL Framework" style="max-width: 100%; height: auto;">
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
            </div>
            <div class="column vertical-top text-left" style="width: 50%">
            </div>
        </div>
    </div>
</div>

## Reinforcement Learning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 60%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <img src="https://upload.wikimedia.org/wikipedia/commons/1/1b/Reinforcement_learning_diagram.svg" alt="RL Framework" style="max-width: 100%; height: auto;">
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
                    <li>Unknow transition model and reward function</li>
                    <li>Cannot simulate outcomes</li>
                    <li>Q-Learning, DQN</li>
                </ul>
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
                <br>
                <p><b>Policy Iteration</b> is a model-based reinforcement learning algorithm that alternates between <em>policy evaluation</em> and <em>policy improvement</em> to find the optimal policy.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="https://upload.wikimedia.org/wikipedia/commons/a/ad/Markov_Decision_Process.svg" alt="MDP Process" style="max-width: 100%; height: auto;">
                <div class="footnote">Markov Decision Process - waldoalvarez, CC BY-SA 4.0, via Wikimedia Commons.</div>
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
                <br>
                <p><b>Policy Iteration</b> is a model-based reinforcement learning algorithm that alternates between <em>policy evaluation</em> and <em>policy improvement</em> to find the optimal policy.</p>
                <p>Finds the optimal policy through iterative refinement:</p>
                <ul>
                    <li>Requires a model of the environment (transition and reward functions)</li>
                    <li>Guaranteed to converge to the optimal policy</li>
                    <li>Works with finite state and action spaces</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="https://wikimedia.org/api/rest_v1/media/math/render/svg/c6200446103959c8994075edaddeddf91abb8166" alt="Stochastic Matrix" style="max-width: 100%; height: auto;">
                <div class="footnote">Stochastic Matrix.</div>
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
                <br>
                <p><b>Policy Iteration</b> consists of two main phases that alternate until convergence:</p>
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
                <br>
                <p><b>Policy Iteration</b> consists of two main phases that alternate until convergence:</p>
<br>
<p><b>1. Policy Evaluation:</b> Compute the value function for the current policy:</p>
<br>
$$
V^\pi(s) = \sum_{s'} P(s'|s,\pi(s)) [R(s,\pi(s),s') + \gamma V^\pi(s')]
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
                <br>
                <br>
                <p><b>Policy Iteration</b> consists of two main phases that alternate until convergence:</p>
<br>
<p><b>1. Policy Evaluation:</b> Compute the value function for the current policy:</p>
<br>
$$
V^\pi(s) = \sum_{s'} P(s'|s,\pi(s)) [R(s,\pi(s),s') + \gamma V^\pi(s')]
$$
<br>
<p><b>2. Policy Improvement:</b> Update the policy to be greedy with respect to the current value function:</p>
<br>
$$
\pi'(s) = \arg\max_a \sum_{s'} P(s'|s,a) [R(s,a,s') + \gamma V^\pi(s')]
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
                <p><b>Policy Iteration Algorithm:</b></p>
                <p>The algorithm iteratively improves the policy by alternating between evaluation and improvement steps until convergence to the optimal policy.</p>
<br>
$$
\pi^*(s) = \arg\max_a Q^*(s,a)
$$
</div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="https://upload.wikimedia.org/wikipedia/commons/a/ad/Markov_Decision_Process.svg" alt="MDP Process" style="max-width: 100%; height: auto;">
                <div class="footnote">Markov Decision Process - waldoalvarez, CC BY-SA 4.0, via Wikimedia Commons.</div>
            </div>
        </div>
    </div>
</div>

## Reinforcement Learning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
                <p><b>Policy Iteration Algorithm:</b></p>
                <p>The algorithm iteratively improves the policy by alternating between evaluation and improvement steps until convergence to the optimal policy.</p>
<br>
$$
\pi^*(s) = \arg\max_a Q^*(s,a)
$$
<br>The optimal policy maximizes the expected cumulative reward by selecting actions that lead to the highest Q-values.
<br>Policy iteration guarantees convergence to the optimal policy through the principle of policy improvement.
</div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="https://upload.wikimedia.org/wikipedia/commons/a/ad/Markov_Decision_Process.svg" alt="MDP Process" style="max-width: 100%; height: auto;">
                <div class="footnote">Markov Decision Process - waldoalvarez, CC BY-SA 4.0, via Wikimedia Commons.</div>
            </div>
        </div>
    </div>
</div>

## Reinforcement Learning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 60%">
<pre><code>Policy Iteration Algorithm:
Initialise policy π randomly
Repeat until convergence:
    // Policy Evaluation
    Repeat until convergence:
        For each state s:
            V(s) = Σ P(s'|s,π(s)) [R(s,π(s),s') + γV(s')]
    // Policy Improvement
    policy_stable = true
    For each state s:
        old_action = π(s)
        π(s) = argmaxₐ Σ P(s'|s,a) [R(s,a,s') + γV(s')]
        If old_action ≠ π(s):
            policy_stable = false
    If policy_stable:
        break
</code></pre>
</div>
            <div class="column vertical-middle text-left" style="width: 40%">
                <img src="https://upload.wikimedia.org/wikipedia/commons/a/ad/Markov_Decision_Process.svg" alt="MDP Process" style="max-width: 100%; height: auto;">
                <div class="footnote">Markov Decision Process - waldoalvarez, CC BY-SA 4.0, via Wikimedia Commons.</div>
            </div>
        </div>
    </div>
</div>

## Reinforcement Learning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 60%">
<pre><code>Policy Iteration Algorithm:
Initialise policy π randomly
Repeat until convergence:
    // Policy Evaluation
    Repeat until convergence:
        For each state s:
            V(s) = Σ P(s'|s,π(s)) [R(s,π(s),s') + γV(s')]
    // Policy Improvement
    policy_stable = true
    For each state s:
        old_action = π(s)
        π(s) = argmaxₐ Σ P(s'|s,a) [R(s,a,s') + γV(s')]
        If old_action ≠ π(s):
            policy_stable = false
    If policy_stable:
        break
</code></pre>
</div>
            <div class="column vertical-middle text-left" style="width: 40%">
                <p><b>Convergence Properties:</b></p>
                <ul>
                    <li><b>Monotonic Improvement:</b> Each iteration improves the policy</li>
                    <li><b>Finite Convergence:</b> Guaranteed to converge in finite steps</li>
                    <li><b>Optimal Policy:</b> Converges to the optimal policy π*</li>
                    <li><b>Bellman Optimality:</b> Final policy satisfies Bellman optimality equations</li>
                </ul>
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
                <p><b>Policy Iteration Limitations:</b></p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="https://wikimedia.org/api/rest_v1/media/math/render/svg/c6200446103959c8994075edaddeddf91abb8166" alt="Stochastic Matrix" style="max-width: 100%; height: auto;">
                <div class="footnote">Stochastic Matrix.</div>
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
                <p><b>Policy Iteration Limitations:</b></p>
                <ul>
                    <li><b>Model Dependency:</b> Requires complete knowledge of the environment's transition and reward functions.</li>
                    <li><b>Computational Cost:</b> Policy evaluation can be expensive for large state spaces, requiring iterative computation.</li>
                    <li><b>Discrete Spaces:</b> Designed for finite state and action spaces, not suitable for continuous environments.</li>
                    <li><b>Memory Requirements:</b> Needs to store value functions and policies for all states.</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="https://wikimedia.org/api/rest_v1/media/math/render/svg/c6200446103959c8994075edaddeddf91abb8166" alt="Stochastic Matrix" style="max-width: 100%; height: auto;">
                <div class="footnote">Stochastic Matrix.</div>
            </div>
        </div>
    </div>
</div>

## Reinforcement Learning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Q-learning</b> is a model-free reinforcement learning algorithm that learns the optimal action-value function <em>directly from experience</em> by interacting with the environment.</p>
                <p>Finds the optimal policy by learning the Q-function:</p>
                <ul>
                    <li>Does not require a model of the environment (transition or reward function)</li>
                    <li>Can be used in stochastic and unknown environments</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
            </div>
        </div>
    </div>
</div>

## Reinforcement Learning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Q-learning</b> is a model-free reinforcement learning algorithm that learns the optimal action-value function <em>directly from experience</em> by interacting with the environment.</p>
                <p>Finds the optimal policy by learning the Q-function:</p>
                <ul>
                    <li>Does not require a model of the environment (transition or reward function)</li>
                    <li>Can be used in stochastic and unknown environments</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/q-table-initial.png" alt="Q-Matrix" style="max-width: 100%; height: auto;">
                <div class="footnote">Transition Matrix (Q).</div>
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
                <br>
                <p>At each step, the agent <b>updates its estimate of the <em>Q-function</em></b> for a state and action using the observed reward and the maximum estimated value of the next state. The update rule is defined as follows:</p>
<br>
$$
Q(s,a) \leftarrow (1 - \alpha) Q(s,a) + \alpha [R(s,a,s') + \gamma \max_{a'} Q(s',a') - Q(s_t, a_t)]
$$
where:
$\alpha$ is the learning rate
$\gamma$ is the discount factor
$R(s,a,s')$ is the observed reward
$s'$ is the next state after taking action $a$ in $s$
</div>
        </div>
    </div>
</div>

## Reinforcement Learning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/q-table-initial.png" alt="Q-Matrix" style="max-width: 100%; height: auto;">
                <div class="footnote">Transition Matrix (Q).</div>
            </div>
        </div>
    </div>
</div>

## Reinforcement Learning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
<pre><code>Q-Learning Algorithm:
Initialize Q(s, a) arbitrarily for all s, a
Repeat (for each episode):
    Initialize state s
    Repeat (for each step of episode):
        a ← π(s)
        // Act according to a
        r ← = R(s, a, s')
        Q(s, a) ← update(Q, s, a, s', r)
        s ← s'
    until s is terminal
</code></pre>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/q-table-initial.png" alt="Q-Matrix" style="max-width: 100%; height: auto;">
                <div class="footnote">Transition Matrix (Q).</div>
            </div>
        </div>
    </div>
</div>

## Reinforcement Learning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
<pre><code>Q-Learning Algorithm:
Initialize Q(s, a) arbitrarily for all s, a
Repeat (for each episode):
    Initialize state s
    Repeat (for each step of episode):
        a ← π(s)
        // Act according to a
        r ← = R(s, a, s')
        Q(s, a) ← update(Q, s, a, s', r)
        s ← s'
    until s is terminal
</code></pre>
<p>The agent must balance <b>exploring</b> new actions to discover their value and <b>exploiting known actions</b> to maximize reward.</p>
</div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/q-table-initial.png" alt="Q-Matrix" style="max-width: 100%; height: auto;">
                <div class="footnote">Transition Matrix (Q).</div>
            </div>
        </div>
    </div>
</div>

## Reinforcement Learning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
<pre><code>Q-Learning Algorithm:
Initialize Q(s, a) arbitrarily for all s, a
Repeat (for each episode):
    Initialize state s
    Repeat (for each step of episode):
        a ← π(s)
        // Act according to a
        r ← = R(s, a, s')
        Q(s, a) ← update(Q, s, a, s', r)
        s ← s'
    until s is terminal
</code></pre>
<p>The agent must balance <b>exploring</b> new actions to discover their value and <b>exploiting known actions</b> to maximize reward.</p>
<p><b>ε-Greedy Policy:</b></p>
$$
\pi(s) = \begin{cases}
\text{random action} & \text{with probability } \epsilon \\
\arg\max_a Q(s,a) & \text{with probability } 1-\epsilon
\end{cases}
$$
</div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/q-table-initial.png" alt="Q-Matrix" style="max-width: 100%; height: auto;">
                <div class="footnote">Transition Matrix (Q).</div>
            </div>
        </div>
    </div>
</div>

## Reinforcement Learning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
<pre><code>Q-Learning Algorithm:
Initialize Q(s, a) arbitrarily for all s, a
Repeat (for each episode):
    Initialize state s
    Repeat (for each step of episode):
        a ← π(s)
        // Act according to a
        r ← = R(s, a, s')
        Q(s, a) ← update(Q, s, a, s', r)
        s ← s'
    until s is terminal
</code></pre>
<p>The agent must balance <b>exploring</b> new actions to discover their value and <b>exploiting known actions</b> to maximize reward.</p>
<p><b>ε-Greedy Policy:</b></p>
$$
\pi(s) = \begin{cases}
\text{random action} & \text{with probability } \epsilon \\
\arg\max_a Q(s,a) & \text{with probability } 1-\epsilon
\end{cases}
$$
</div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/q-table-final.png" alt="Q-Matrix" style="max-width: 100%; height: auto;">
                <div class="footnote">Transition Matrix (Q).</div>
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
                <p><b>Q-Learning Limitations:</b></p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/q-table-final.png" alt="Q-Matrix" style="max-width: 100%; height: auto;">
                <div class="footnote">Transition Matrix (Q).</div>
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
                <p><b>Q-Learning Limitations:</b></p>
                <ul>
                    <li><b>Scalability:</b> Q-learning struggles with large state spaces as it requires a Q-value for every state-action pair, leading to high memory usage.</li>
                    <li><b>Generalization:</b> Q-learning does not generalize well to unseen states since it relies on a discrete Q-table.</li>
                    <li><b>Continuous State Spaces:</b> Q-learning is not suitable for environments with continuous state spaces as it requires discretization, which can lead to loss of information.</li>
                    <li><b>Sample Inefficiency:</b> Q-learning can be sample inefficient, requiring many interactions with the environment to learn an optimal policy.</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/q-table-final.png" alt="Q-Matrix" style="max-width: 100%; height: auto;">
                <div class="footnote">Transition Matrix (Q).</div>
            </div>
        </div>
    </div>
</div>

## Reinforcement Learning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
            <p><b>Deep Q-Networks (DQN)</b> extend Q-learning to environments with large or continuous state spaces. It replaces the Q-table using <b>neural networks</b> to approximate the <em>Q-function</em>:</p>
<br>
$$
Q(s,a;\mathbf{w})
$$
</div>
            <div class="column vertical-middle text-left" style="width: 50%">
            </div>
        </div>
    </div>
</div>

## Reinforcement Learning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
                <p><b>Deep Q-Networks (DQN)</b> extend Q-learning to environments with large or continuous state spaces. It replaces the Q-table using <b>neural networks</b> to approximate the <em>Q-function</em>:</p>
<br>
$$
Q(s,a;\mathbf{w})
$$
</div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="https://upload.wikimedia.org/wikipedia/commons/1/15/Neural_Network.svg" alt="Deep Neural Network" style="max-width: 100%; height: auto;">
                <div class="footnote">Deep Neural Network with multiple hidden layers - QuantuMechaniX8, CC0, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## Reinforcement Learning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
                <p><b>Deep Q-Networks (DQN)</b> extend Q-learning to environments with large or continuous state spaces. It replaces the Q-table using <b>neural networks</b> to approximate the <em>Q-function</em>:</p>
<br>
$$
Q(s,a;\mathbf{w})
$$
<br>A main network approximates $Q(s,a)$ and $\mathbf{w}$ are its trainable parameters. The input of the network is the state and the output is a <em>Q-value</em> per possible action.
</div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="https://upload.wikimedia.org/wikipedia/commons/1/15/Neural_Network.svg" alt="Deep Neural Network" style="max-width: 100%; height: auto;">
                <div class="footnote">Deep Neural Network with multiple hidden layers - QuantuMechaniX8, CC0, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## Reinforcement Learning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
                <p><b>Deep Q-Networks (DQN)</b> extend Q-learning to environments with large or continuous state spaces. It replaces the Q-table using <b>neural networks</b> to approximate the <em>Q-function</em>:</p>
<br>
$$
Q(s,a;\mathbf{w})
$$
<br>A main network approximates $Q(s,a)$ and $\mathbf{w}$ are its trainable parameters. The input of the network is the state and the output is a <em>Q-value</em> per possible action.
<br>DQNs store past experiences $(s,a,r,s')$ in a replay buffer. During training a minibatch of experiences are selected. A target network is used to compute the target <em>Q-values</em> during updates.
</div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="https://upload.wikimedia.org/wikipedia/commons/1/15/Neural_Network.svg" alt="Deep Neural Network" style="max-width: 100%; height: auto;">
                <div class="footnote">Deep Neural Network with multiple hidden layers - QuantuMechaniX8, CC0, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## Reinforcement Learning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
<pre><code>DQN Algorithm:
Initialise replay buffer D
Initialise Q-network with random weights w
Initialise target Q-network with weights w⁻ = w
Repeat (for each episode):
    Initialise state s
    Repeat (for each step of episode):
        a ← π(s)
        // Act according to a
        r ← = R(s, a, s')
        Store (s, a, r, s') in D
        For each (s, a, r, s') in mini_batch(D):
            y = r + γ maxₐ' Q(s', a'; w⁻)
        w ← gradient_descent((y - Q(s, a; w))²)
        Every C steps, update w⁻ ← w
        s ← s'
    until s is terminal
</code></pre>
</div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="https://upload.wikimedia.org/wikipedia/commons/1/15/Neural_Network.svg" alt="Deep Neural Network" style="max-width: 100%; height: auto;">
                <div class="footnote">Deep Neural Network with multiple hidden layers - QuantuMechaniX8, CC0, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## Reinforcement Learning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
<pre><code>DQN Algorithm:
Initialise replay buffer D
Initialise Q-network with random weights w
Initialise target Q-network with weights w⁻ = w
Repeat (for each episode):
    Initialise state s
    Repeat (for each step of episode):
        a ← π(s)
        // Act according to a
        r ← = R(s, a, s')
        Store (s, a, r, s') in D
        For each (s, a, r, s') in mini_batch(D):
            y = r + γ maxₐ' Q(s', a'; w⁻)
        w ← gradient_descent((y - Q(s, a; w))²)
        Every C steps, update w⁻ ← w
        s ← s'
    until s is terminal
</code></pre>
</div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>ε-Greedy Policy:</b></p>
$$
\pi(s) = \begin{cases}
\text{random action} & \text{with probability } \epsilon \\
\arg\max_a Q(s,a; \mathbf{w}) & \text{with probability } 1-\epsilon
\end{cases}
$$
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
                <img src="https://upload.wikimedia.org/wikipedia/commons/a/ad/Markov_Decision_Process.svg" alt="MDP Process" style="max-width: 100%; height: auto;">
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
                <img src="https://upload.wikimedia.org/wikipedia/commons/1/15/Neural_Network.svg" alt="Deep Neural Network" style="max-width: 100%; height: auto;">
                <div class="footnote">Deep Neural Network with multiple hidden layers - QuantuMechaniX8, CC0, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## Reinforcement Learning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
                <img class="external-svg" src="https://media.springernature.com/full/springer-static/image/art%3A10.1038%2Fnature24270/MediaObjects/41586_2017_Article_BFnature24270_Fig1_HTML.jpg?as=webp" alt="AlphaGo Zero" style="max-width: 100%; height: auto;">
                <div class="footnote">Self-play reinforcement learning in AlphaGo Zero - <a href="https://www.nature.com/articles/nature24270">Silver et al., 2017</a>.</div>
            </div>
            <div class="column vertical-top text-left" style="width: 50%">
            </div>
        </div>
    </div>
</div>

## Reinforcement Learning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
                <img class="external-svg" src="https://media.springernature.com/full/springer-static/image/art%3A10.1038%2Fnature24270/MediaObjects/41586_2017_Article_BFnature24270_Fig1_HTML.jpg?as=webp" alt="AlphaGo Zero" style="max-width: 100%; height: auto;">
                <div class="footnote">Self-play reinforcement learning in AlphaGo Zero - <a href="https://www.nature.com/articles/nature24270">Silver et al., 2017</a>.</div>
            </div>
            <div class="column vertical-top text-left" style="width: 50%">
                <br>
                <p><b>AlphaGo Zero combines key RL concepts:</b></p>
                <ul>
                    <li><b>Self-play environment:</b> Agent plays against itself (no human data needed)</li>
                    <li><b>Policy network:</b> Learns π(s) → probability distribution over actions</li>
                    <li><b>Value network:</b> Learns V(s) → probability of winning from state s</li>
                    <li><b>Monte Carlo Tree Search:</b> Uses policy/value to guide search</li>
                    <li><b>Temporal difference learning:</b> Updates based on game outcomes</li>
                    <li><b>Experience replay:</b> Stores and learns from self-play games</li>
                </ul>
            </div>
        </div>
    </div>
</div>


<!-- end SLIDES: -->

{% include _snippets/timelines/ai-history-2001-today.md %}