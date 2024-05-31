# CS7637_SP24-SemanticNetworks

## Overview
This assignment presents an ai agent designed to solve a Difficult Cross-ing - Transportation Problem.  The agent solves for the movements of animals back-and-forth across the river. The end-state is when all animals are on the right bank. The agent adapts a bread-first-search with a scoring for each move.

## The Transportation Problem
In this assignment, the algorithm employed attempts to solve a transportation problem, specifically a difficult crossing problem. Below is a summarization of the problem by Saul Amarel.
>“Three missionaries and three cannibals seek to cross a river (say from the left bank to the right bank). A boat is available which will hold two people, and which can >be navigated by any combi-nation of missionaries and cannibals involving one or two people. If the missionaries on either bank of the river, or 'en route' in the river, >are outnumbered at any time by cannibals, the cannibals will indulge in their anthropophagic tendencies and do away with the missionaries. Find the simplest schedule of >crossings that will permit all the missionaries and cannibals to cross the river safely.” [Amarel, 1968]

In this edition of the assignment, the two groups are sheep and wolves, taking the place of missionaries and cannibals, respectively. The algorithm is a version of breadth-first-search, without a priority-queue. 

A breadth-first-search “expands the shallowest nodes first; it is complete, opti-mal for unit action costs, but has exponential space complexity” (Russell, 2020). Figure 1 below captures the breadth-first-search algorithm.

<figure>
  <img src="https://github.gatech.edu/storage/user/36047/files/3cbb0588-3ae4-4ca3-b061-15da84ce427b" alt="Alt text">
  <figcaption>Figure 1—	Breadth-first search algorithm. (Russell, 2020).</figcaption>
</figure>

##Funcionality
The agent begins by initializing the boat direction, legal moves, state history, and the value of sheep and wolves on each side of the river. State history is an array, representing the position of each sheep, each wolf, and the direction of the boat for every action of the game.

### Generate a new state.
Because the boat can hold up to two animals, there are 5 combinations, repre-senting possible actions at every state. At each state, the set of possible actions is shuffled and looped through.

### Test the state.
For each action selected, temporary values of the initialized variables are updat-ed, then validated against two methods.
First, the action is checked against the 6 rules for animal positions. Second, the temporary state is checked against the previous states. If the action fails a rule or the state previously existed, the action is rejected, and the agent continues to through the loop

## Efficiency
The agent’s time and space complexity are included in Figure 2 below as Breadth-First. The time and space are exponential with the increase in animal count.

<figure>
  <img src="https://github.gatech.edu/storage/user/36047/files/16dd686c-3888-4e93-b694-3d5ffdeb1345" alt="Alt text">
  <figcaption>Figure 2—	Evaluation of search algorithms. is the branch-ing factor; is the maximum depth of the search tree; is the depth of the shallowest solution. (Russell, 2020).</figcaption>
</figure>

### Efficiency Improvements
To improve the performance of the agent, plausible actions are scored. The ac-tion with the best score is chosen. While performance is improved, the agent does not act as a uniform-cost search (UCS) with the scoring. A UCS algorithm does not terminate when the end state is reached; rather, the frontier is checked until empty, finding the path with the minimum cost to reach the state. This agent terminates at completion and only checks the score when adding an action, not the entire path cost.


## References
1. Amarel, S. (1968). On representations of problems of reasoning about actions. Machine intelligence.
2. Russell, S. J., & Norvig, P. (2020). Artificial intelligence: A Modern Approach. 4th Edition, Prentice-Hall, Upper Saddle River.
