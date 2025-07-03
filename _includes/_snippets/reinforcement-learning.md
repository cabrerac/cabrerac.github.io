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
                    <li>Q-Learning, REINFORCE</li>
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
                <p>At each step, the agent updates its estimate of $Q(s,a)$ using the observed reward and the maximum estimated value of the next state:</p>
$$
Q(s,a) \leftarrow Q(s,a) + \alpha [R(s,a,s') + \gamma \max_{a'} Q(s',a') - Q(s,a)]
$$
where:
<ul>
  <li>$\alpha$ is the learning rate</li>
  <li>$\gamma$ is the discount factor</li>
  <li>$R(s,a,s')$ is the observed reward</li>
  <li>$s'$ is the next state after taking action $a$ in $s$</li>
</ul>
</div>
        </div>
    </div>
</div>

## Reinforcement Learning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
<pre><code>Q-Learning Algorithm:
Initialize Q(s, a) arbitrarily for all s, a
Repeat (for each episode):
    Initialize state s
    Repeat (for each step of episode):
        Choose action a from s using policy derived from Q (e.g., ε-greedy)
        Take action a, observe reward r and next state s'
        Q(s, a) ← Q(s, a) + α [r + γ maxₐ' Q(s', a') - Q(s, a)]
        s ← s'
    until s is terminal
</code></pre>
            </div>
        </div>
    </div>
</div>

## Reinforcement Learning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p><b>Exploration vs Exploitation:</b> The agent must balance exploring new actions to discover their value and exploiting known actions to maximize reward.</p>
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
            <div class="column vertical-middle text-left" style="width: 60%">
                <p><b>Deep Q-Networks (DQN)</b> extend Q-learning to environments with large or continuous state spaces by using a neural network to approximate the Q-function:</p>
                <ul>
                    <li>Q-table is replaced by a neural network $Q(s,a;\theta)$ with parameters $\theta$</li>
                    <li>Can handle high-dimensional inputs (e.g., images)</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 40%">
                <img src="https://upload.wikimedia.org/wikipedia/commons/1/19/DQN-diagram.png" alt="DQN Architecture" style="max-width: 100%; height: auto;">
                <div class="footnote">DQN Architecture (source: Wikimedia Commons).</div>
            </div>
        </div>
    </div>
</div>

## Reinforcement Learning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <ul>
                    <li><b>Experience Replay:</b> Store agent's experiences $(s, a, r, s')$ in a replay buffer and sample random mini-batches for training. This breaks correlation between samples and improves stability.</li>
                    <li><b>Target Network:</b> Use a separate target network $Q_{\text{target}}$ to compute target values, updated less frequently than the main network. This reduces oscillations and divergence.</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## Reinforcement Learning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
<pre><code>DQN Algorithm:
Initialize replay buffer D
Initialize Q-network with random weights θ
Initialize target Q-network with weights θ⁻ = θ
Repeat (for each episode):
    Initialize state s
    Repeat (for each step of episode):
        With probability ε select a random action a
        otherwise select a = argmaxₐ Q(s, a; θ)
        Execute action a, observe reward r and next state s'
        Store (s, a, r, s') in D
        Sample random mini-batch from D
        For each (s, a, r, s') in batch:
            y = r + γ maxₐ' Q(s', a'; θ⁻)
        Perform gradient descent step on (y - Q(s, a; θ))²
        Every C steps, update θ⁻ ← θ
        s ← s'
    until s is terminal
</code></pre>
            </div>
        </div>
    </div>
</div>

## Reinforcement Learning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <table>
                    <thead>
                        <tr><th>Algorithm</th><th>Q Representation</th><th>State Space</th><th>Key Features</th></tr>
                    </thead>
                    <tbody>
                        <tr><td>Q-Learning</td><td>Table</td><td>Small/Discrete</td><td>Simple, Model-Free</td></tr>
                        <tr><td>DQN</td><td>Neural Network</td><td>Large/Continuous</td><td>Experience Replay, Target Network</td></tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: --> 

## Reinforcement Learning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
                <p><b>Q-Learning:</b></p>
                <p>A model-free reinforcement learning algorithm that learns the optimal action-value function directly from experience.</p>
                <p><b>Q-Learning Update Rule:</b></p>
$$
Q(s,a) \leftarrow Q(s,a) + \alpha [R(s,a,s') + \gamma \max_{a'} Q(s',a') - Q(s,a)]
$$
where $\alpha$ is the learning rate and the term in brackets is the temporal difference error.
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