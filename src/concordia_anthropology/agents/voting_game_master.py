import re
from typing import Optional, Literal,  cast, TypeVar, Sequence
from concordia.agents.entity_agent_with_logging import EntityAgentWithLogging
from concordia.components.game_master import make_observation
from concordia.typing.entity_component import ActingComponent, ComponentContextMapping, ComponentWithLogging, ComponentState, ContextComponent
from concordia.typing.entity import ActionSpec, OutputType

from dataclasses import dataclass, asdict
from concordia.environment.engines import sequential
from concordia.components.game_master.make_observation import DEFAULT_CALL_TO_MAKE_OBSERVATION


# ---- Types

VoteStatus = Literal["up", "down"]
VoteOptionsDown = Literal["keep down", "raise"]
VoteOptionsUp = Literal["keep_raised", "lower"]


@dataclass
class VotingActionSpecOptions:
    down = ("keep down", "raise")
    up  = ("keep raised", "lower")
voting_action_spec_options = VotingActionSpecOptions()

Stage = Literal["present_proposal", "observe_votes", "voting", "finished"]
stages = ("present_proposal", "observe_votes", "voting", "finished")



# --- Utility ---
# Gets the initial dictionary of player's hands, with all hands down
def get_init_votes (players: list[str]) -> dict[str, VoteStatus]:
    hands : dict[str,VoteStatus] = {}
    for player in players:
        hands[player] = "down"
    return hands
T = TypeVar("T")

def head(seq: Sequence[T]) -> Optional[T]:
    return seq[0] if seq else None

# The ENUM OutputType in the Concordia libray has its fields defined with str type annotations and this breaks the type checking. So I've defined a function to get around it.

OutputTypeLiteral = Literal["free",
"choice",
"float",
"make_observation",
"next_acting",
"next_action_spec",
"resolve",
"terminate",
"next_game_master",
"skip_this_step",]

def outputType(type: OutputTypeLiteral) -> OutputType:
   return OutputType(type)


cast(OutputType, OutputType.FREE)


# State
@dataclass
class VotingState:
    players: list[str]
    remaining_in_stage: list[str]
    current_votes: dict[str, VoteStatus]
    chair: str

    # Default value fields
    prev_votes: Optional[dict[str, VoteStatus]] = None
    max_rounds: int = 5
    stage: Stage = "present_proposal"
    round_num: int = 1


    adopted : Optional[Literal["adopted", "not adopted"]] = None

    def __init__(self, players: list[str], chair: str):
        self.players = players
        self.current_votes = get_init_votes(players)
        assert chair in players
        self.chair = chair
        self.remaining_in_stage =  players.copy()



    def all_up(self, votes: dict[str, VoteStatus]):
        return all("up" == vote for vote in votes.values())

    def end_present_proposal(self):
        assert self.stage == "present_proposal" and self.remaining_in_stage == []
        # We skip observe votes for the first round since nobody has had a chance to decide yet.
        self.stage = "voting"
        self.remaining_in_stage = self.players.copy()


    def end_observe_votes(self):
        """Ends the observe_votes stage. Sets stage to "voting", Ensures that prev_votes are set equal to current_votes and resets remaining_in_stage."""
        assert self.stage == "observe_votes"  and self.remaining_in_stage == []
        self.remaining_in_stage = self.players.copy()
        self.prev_votes = {**self.current_votes}
        self.stage = "voting"

    def end_voting_round(self):
        """Performs checks and bookkeeping to end the round of voting."""
        assert self.stage == "voting"  and self.remaining_in_stage == []

        if self.prev_votes and self.all_up(self.prev_votes) and self.all_up(self.current_votes):
        # If all votes are up for this round and previous round, voting is finished and proposal is adopted.
            self.stage = "finished"
            self.adopted = "adopted"
        elif self.round_num < self.max_rounds:
            # We reset and go to next round
            self.stage = "observe_votes"
            self.remaining_in_stage = self.players.copy()
            self.round_num = self.round_num + 1

        else: # Last round, move to finished
            self.stage = "finished"
            self.remaining_in_stage = self.players.copy()
            if self.all_up(self.current_votes):
                self.adopted = "adopted"
            else:
                self.adopted = "not adopted"

    def record_player_completion_for_stage(self, player:str) -> None:
        assert player in self.players
        if player not in self.remaining_in_stage:
            self.remaining_in_stage  =  [p for p in self.remaining_in_stage  if p != player]

    def record_votes_observation(self, player: str) -> None:
        """This records when an observation has been make of the voting state by a player."""
        assert player in self.players
        assert self.stage == "observe_votes"
        self.record_player_completion_for_stage(player)


    def record_vote(self, player: str, vote: VoteStatus) -> None:
        """This records a vote by a player."""
        assert player in self.players
        assert self.stage == "voting"

        if player in self.remaining_in_stage:
            self.current_votes[player] = vote
            self.record_player_completion_for_stage(player)

    def next_player(self) -> Optional[str]:
        head(self.remaining_in_stage)



def entity_name_from_make_observation_CTA(call: str) -> str:
    """
    Extracts the {name} from the default make_observation call to action used by the engine.
    Returns the name if found otherwise throws an error.
    """
    # Fast path for the exact default template
    prefix = "What is the current situation faced by "
    if call.startswith(prefix):
        rest = call[len(prefix):]
        q = rest.find("?")
        if q != -1:
            return rest[:q].strip()

    raise ValueError()


# Acting Component
class VotingActingComponent(ActingComponent, ComponentWithLogging):

    def _init_(self,  next_game_master: str, players: list[str], chair: str, chair_title: str = "chairperson"  ):
        self.players = players
        assert chair in players
        self.chair = players
        self.chair_title = chair_title
        self.voting_state = VotingState(players, chair)
        self.next_game_master = next_game_master

    def get_state(self) -> ComponentState:
        return  cast(ComponentState, asdict(self.voting_state))

    # Not implemented.
    def set_state(self,state: ComponentState) -> None :
        pass



    def get_action_attempt(
      self,
      context: ComponentContextMapping,
      action_spec: ActionSpec,
    ) -> str:
        state = self.voting_state
        match state.stage:
            case "present_proposal":
                match action_spec.output_type:
                    case OutputType.MAKE_OBSERVATION:
                        player = entity_name_from_make_observation_CTA(action_spec.call_to_action)
                        if player == state.chair:
                            prompt =  """
                            It is time now for you to present the proposal for voting. Please clearly state the proposed course of action for everybody to listen.
                            """
                            return prompt





                    case OutputType.NEXT_ACTING:
                    case OutputType.NEXT_ACTION_SPEC:
                            # ActionSpec(output_type=outputType("free"), call_to_action=prompt )
                    case OutputType.RESOLVE:
                        if not state.not_observed_votes:
                            state.end_observe_votes()
                    case OutputType.TERMINATE:
                    case OutputType.NEXT_GAME_MASTER:
                    case OutputType.SKIP_THIS_STEP:
            case "observe_votes":
                match action_spec.output_type:
                    case OutputType.MAKE_OBSERVATION:
                        if state.not_observed_votes:
                        observer = state.next_vote_observer()

                    case OutputType.NEXT_ACTING:
                    case OutputType.NEXT_ACTION_SPEC:
                    case OutputType.RESOLVE:
                        if not state.not_observed_votes:
                            state.end_observe_votes()
                    case OutputType.TERMINATE:
                    case OutputType.NEXT_GAME_MASTER:
                    case OutputType.SKIP_THIS_STEP:


                if action_spec.output_type == OutputType.MAKE_OBSERVATION:


            case "voting":
                match action_spec.output_type:
                    case OutputType.MAKE_OBSERVATION:
                    case OutputType.NEXT_ACTING:
                        if state.not_voted:
                            next_player = state.next_voter()
                    case OutputType.NEXT_ACTION_SPEC:
                        self.get_voting_action_spec()
                    case OutputType.RESOLVE:
                        if not state.not_voted:
                            state.end_voting_round()
                    case OutputType.TERMINATE:
                    case OutputType.NEXT_GAME_MASTER:
                    case OutputType.SKIP_THIS_STEP:

    def solicit_proposal():








            case "finished":
                match action_spec.output_type:
                    case  OutputType.NEXT_ACTING:
                    case OutputType.NEXT_ACTION_SPEC


# class InitiateVoting(ContextComponent):
#     def pre_observe(self, observation: str) -> str:



# Class GameMasterNoModel(EntityAgentWithLogging):
#     act():

#     observe:



def voting_game_master(next_game_master: str, players: list[str], chair: str, chair_title: str = "chairperson"  ):
    components: dict[str, ContextComponent] = {}

    return EntityAgentWithLogging(
        agent_name="voting_game_master",
        act_component=VotingActingComponent(next_game_master, players, chair, chair_title ),
        context_components=components,
    )



