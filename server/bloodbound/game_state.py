from typing import List, Dict, Tuple, Any, Optional, Set
#from enum import Enum, IntEnum
from enum import Enum
from dataclasses import dataclass, field, asdict
import random


PlayerID = str


class Team(str, Enum):
    RED  = "red"
    BLUE = "blue"

    def other(self) -> "Team":
        if self == Team.RED:
            return Team.BLUE
        else:
            return Team.RED


class Token(str, Enum):
    GREY = "grey"
    BLUE = "blue"
    RED = "red"
    RANK = "rank"
    TEAM = "team"

    @classmethod
    def team_sub(cls, tokens: List["Token"], team: Team):
        def _sub(token):
            if token == Token.TEAM:
                return Token.RED if team == Team.RED else Token.BLUE
            return token
        return list(map(_sub, tokens))

class Role(int, Enum):
    ELDER     = 1
    ASSASSIN  = 2
    HARLEQUIN = 3
    ALCHEMIST = 4
    MENTALIST = 5
    GUARDIAN  = 6
    BERSERKER = 7
    MAGE      = 8
    COURTESAN = 9

    def tokens(self) -> List[Token]:
        if self in [Role.ELDER, Role.ASSASSIN, Role.HARLEQUIN]:
            return [Token.RANK, Token.GREY, Token.GREY]
        if self in [Role.ALCHEMIST, Role.MENTALIST, Role.GUARDIAN]:
            return [Token.RANK, Token.TEAM, Token.TEAM]
        if self in [Role.BERSERKER, Role.MAGE, Role.COURTESAN]:
            return [Token.RANK, Token.GREY, Token.TEAM]
        raise ValueError

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplementedError

class Item(str, Enum):
    FAN = "fan"
    STAFF = "staff"
    SHIELD_I = "shield_i"
    SWORD_I = "sword_i"
    SHIELD_II = "shield_ii"
    SWORD_II = "sword_ii"
    QUILL = "quill"
    FALSECURSE = "falsecurse"
    TRUECURSE = "truecurse"


class Step(str, Enum):
    LOBBY          = "lobby"
    ACK_PEEK       = "set_peek"
    SET_TARGET     = "set_target"
    INTERVENE      = "intervene"
    ACK_INTERVENE  = "ack_intervene"
    SET_WOUND_I    = "set_wound_i"
    SET_ABILITY    = "set_ability"
    ASSASSIN_WOUND = "assassin_wound"
    ALCHEMIST_HEAL = "alchemist_heal"
    SET_WOUND_II   = "set_wound_ii"
    COMPLETE       = "complete"


@dataclass
class Player:
    name: PlayerID
    team: Team
    role: Role
    shown_tokens: List[Token]
    tokens: List[Token]
    items: List[Item]
    position: int

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.role.value < other.role.value
        return NotImplemented


@dataclass
class GameState:
    players: Dict[PlayerID, Player] = field(default_factory=lambda: {})
    step: Step = Step.LOBBY
    peeked: Dict[PlayerID, bool] = field(default_factory=lambda: {})
    active: Optional[PlayerID] = None
    target: Optional[PlayerID] = None
    intervene_offers: Dict[PlayerID, bool] = field(default_factory=lambda: {})
    intervener: Optional[PlayerID] = None
    # player declaring wound token. cases:
    #   - after attack, intervener is None ->     wounded = target
    #   - after attack, intervener is not None -> wounded = intervener
    #   - after assassin ability  -> wounded = ability target
    #   - after alchemist ability -> wounded = ability target
    #   - after mentalist ability -> wounded = ability target
    #   - after berserker ability -> wounded = active
    wounded: Optional[PlayerID] = None
    # for wound_ii; alchemist & berserker keep knife, mentalist gives knife
    next_active: Optional[PlayerID] = None
    captured: Optional[PlayerID] = None
    complete_acked: Dict[PlayerID, bool] = field(default_factory=lambda: {})

    def reset(self, pids: Set[PlayerID], dummy=False):
        if dummy:
            pids = ["aidan", "duke", "kelvin", "aaron", "piotr", "ankur", "zaaim", "annie"]
            team_size = len(pids) // 2
            red_team = ["aidan", "kelvin", "piotr", "zaaim"]
            red_roles = [Role.ALCHEMIST, Role.HARLEQUIN, Role.ASSASSIN, Role.ELDER]
            blue_roles = [Role.COURTESAN, Role.MAGE, Role.BERSERKER, Role.MENTALIST]
            for (i, pid) in enumerate(pids):
                team = Team.RED if pid in red_team else Team.BLUE
                role = red_roles.pop() if team == Team.RED else blue_roles.pop()
                tokens = role.tokens(team)
                items = []
                player = Player(pid, team, role, tokens, items, i) # PID currently is position index
                self.players[pid] = player
            self.players["aidan"].items = [Item.SWORD, Item.STAFF]
            self.players["duke"].items = [Item.SHIELD]
            self.players["duke"].tokens = [Token.BLUE, Token.GREY]
            self.players["kelvin"].tokens = [Token.RANK]
            self.peeked = {pid:True for pid in pids}
            self.active = "ankur"
            self.target = "aidan"
            self.intervene_offers = {"kelvin": True}
            self.intervener = None
            return
        assert len(pids) % 2 == 0 # don't support inquisitor yet
        team_size = len(pids) // 2
        red_team = set(random.sample(pids, k=team_size))
        red_roles = random.sample(list(Role), k=team_size)
        blue_roles = random.sample(list(Role), k=team_size)
        for pid in pids:
            team = Team.RED if pid in red_team else Team.BLUE
            role = red_roles.pop() if team == Team.RED else blue_roles.pop()
            shown_tokens = []
            tokens = Token.team_sub(role.tokens(), team)
            items = []
            player = Player(pid, team, role, shown_tokens, tokens, items, 0) # TODO make position correct
            self.players[pid] = player
            self.peeked = {}
            self.active = None
            self.target = None
            self.intervene_offers = {}
            self.intervener = None

    def encode(self) -> Dict[str, Any]:
        return asdict(self)

    def leader(self, team: Team) -> PlayerID:
        team_pids = [p for p in self.players if self.players[p].team == team]
        is_quill = any([Item.QUILL in self.players[p].items for p in team_pids])
        _fcn = max if is_quill else min
        return _fcn(team_pids, key=self.players.get)
