# Questions for Sasha or Chatbot

- How does the game master get obserations of the players actions? I need the GM to get the observation of the proposal description. I might need to use an LLM for this part.
  - I might need a context component that has pre-observe defined .


- In output type next acting, what if you want to skips actions and have more observations? For now I'm just returning an empty action string.


- - What kind of string do I need to return for an action spec?






















# Meeting Voting


Chairperson decides which proposal to discuss (if there is more than one):

Introduce Proposal:
Proposal is made by person who talks about how it benefits self and community.

Discussion Phase:
Chairperson decides who speaks.

Voting Component:

Chairperson makes proposal

There will be up to five rounds for hand raising/lowering. In the first round people decide whether to vote to adopt by raising hand or to keep hand down.
Each subsequent round people observe who put up their hand. They can then decide:
 If hand is already up:
    Lower hand or
    keep it raised (vote to adopt)
 If hand is already down:
    raise hand (vote to adopt) or
    keep in down

If all hands are raised for two consequative rounds, the proposal is adopted. If all hands are raised after the fifth round, the proposal is adopted. Othewise the proposal is not adopted.

After voting, all participants observe that the proposal was adopted or not adopted.

When voting begins, the GM needs to make an observation for the chair person that it is time for them to clearly state the proposal and instruct everyone to raise their hand to vote to adopt the proposla or to keep their hand down pospone the decision. There is no option to vote to reject.

After the chairperson speaks, the GM provides this as an observation to all present.

The GM must start counting the round using an internal variable in the voting component.

The GM provides an action spec to each player with their choices, initially this will be raise or keep down for all players.

The GM's voting component tracks the hand raised or down status in a dictionary.

After all players take their actions for one round:

The GM checks if the resolution has been adopted (all hand up for two rounds or all hands up after round 5).
If no, the GM gives an observation to all players accurately stating the hand status of all present.
Then the GM generates action specs for each player based on their new hand status.
After round 5, make observation for all players whether the proposal was adopted or postponed.





