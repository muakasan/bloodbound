from typing import List, Dict, Tuple, Any, Optional, Set
from enum import Enum, IntEnum
from dataclasses import dataclass, field, asdict
import random


PlayerID = int


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

class Role(IntEnum):
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
        return []
'''
class Role(Enum):
    ELDER     = (1, "elder", Token.GREY, Token.GREY)
    ASSASSIN  = (2, "assassin", Token.GREY, Token.GREY)
    HARLEQUIN = (3, "harlequin", Token.GREY, Token.GREY)
    ALCHEMIST = (4, "alchemist", Token.TEAM, Token.TEAM)
    MENTALIST = (5, "mentalist", Token.TEAM, Token.TEAM)
    GUARDIAN  = (6, "guardian", Token.TEAM, Token.TEAM)
    BERSERKER = (7, "berserker", Token.GREY, Token.TEAM)
    MAGE      = (8, "mage", Token.GREY, Token.TEAM)
    COURTESAN = (9, "courtesan", Token.GREY, Token.TEAM)

    def tokens(self) -> List[Token]:
        return [Token.RANK, *self.value[1:]]

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented

    def to_json(self):
        return self.value[0]
'''

class Item(str, Enum):
    SWORD = "sword"
    FAN = "fan"
    STAFF = "staff"
    SHIELD = "shield"
    QUILL = "quill"
    FALSECURSE = "falsecurse"
    TRUECURSE = "truecurse"


#TODO: populate with FSM
class Step(str, Enum):
    LOBBY         = "lobby"
    INGAME        = "ingame"
    COMPLETE      = "complete"

@dataclass
class Player:
    team: Team
    role: Role
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
    target: Optional[PlayerID] = None
    step: Step = Step.LOBBY

    @classmethod
    def build(cls, pids: Set[PlayerID], dummy=False):
        if dummy:
            pids = set([0, 1, 2, 3, 4, 5, 6, 7])
            new_instance = GameState()
            team_size = len(pids) // 2
            red_team = set(random.sample(pids, k=team_size))
            red_roles = random.sample(list(Role), k=team_size)
            blue_roles = random.sample(list(Role), k=team_size)
            for pid in pids:
                team = Team.RED if pid in red_team else Team.BLUE
                role = red_roles.pop() if team == Team.RED else blue_roles.pop()
                tokens = role.tokens()
                items = []
                player = Player(team, role, tokens, items, pid) # PID currently is position index
                new_instance.players[pid] = player
            new_instance.players[0].items = [Item.SWORD, Item.STAFF]
            new_instance.players[1].items = [Item.SHIELD]
            new_instance.players[1].tokens = [Token.BLUE, Token.GREY]
            new_instance.players[2].tokens = [Token.RANK]
            return new_instance
        assert len(pids) % 2 == 0 # don't support inquisitor yet
        new_instance = GameState()
        team_size = len(pids) // 2
        red_team = set(random.sample(pids, k=team_size))
        red_roles = random.sample(list(Role), k=team_size)
        blue_roles = random.sample(list(Role), k=team_size)
        for pid in pids:
            team = Team.RED if pid in red_team else Team.BLUE
            role = red_roles.pop() if team == Team.RED else blue_roles.pop()
            tokens = role.tokens()
            items = []
            player = Player(team, role, tokens, items, 0) # TODO make position correct
            new_instance.players[pid] = player
        return new_instance

    def encode(self) -> Dict[str, Any]:
        return asdict(self)

    def leader(self, team: Team) -> PlayerID:
        team_pids = [p for p in self.players if self.players[p].team == team]
        is_quill = any([Item.QUILL in self.players[p].items for p in team_pids])
        _fcn = max if is_quill else min
        return _fcn(team_pids, key=self.players.get)
