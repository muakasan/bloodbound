from typing import Optional
from bloodbound.game_state import PlayerID, GameState, Team, Step, Token
from flask_socketio import SocketIO, join_room
import random

GameCode = str

# Mock SocketIO for unit testing
if True:
    class SocketIO:
        def __init__(self):
            self.rooms = {}

        def emit(self, msg, data, json, room):
            print(f'{msg}@{room}(JSON:{json}): {data}')

    def join_room(game_code: GameCode):
        print(f'joined room {game_code}')


class Game:
    def handler(*steps: Step):
        def _dec(func):
            def _wrap(self, *args):
                valid = True
                # Check game step valid
                if steps and (self.state.step not in steps):
                    print(f'Game currently in step {self.state.step}, expected {steps}')
                    valid = False
                # Check player ids valid
                for arg, (name, _type) in zip(args, func.__annotations__.items()):
                    if _type is PlayerID and arg not in self.player_ids:
                        print(f'Arg {name} pid {arg}, expected {self.player_ids}')
                        valid = False
                res = func(*args) if valid else None
                self.emit_game_state()
                return res
            return _wrap
        return _dec

    def __init__(self, sio: SocketIO, game_code: GameCode):
        self.sio = sio
        self.game_code = game_code
        self.player_ids = set()
        self.new_game()

    def request_game_state(self) -> None:
        join_room(self.game_code)
        self.emit_game_state()

    def emit_game_state(self) -> None:
        self.sio.emit("gameState", self.state.encode(), json=True, room=self.game_code)

    def new_game(self):
        self.state = GameState.build(self.player_ids, dummy=True)

    def join_game(self, pid: PlayerID) -> None:
        if self.state.step == Step.LOBBY:
            join_room(self.game_code)
            self.player_ids.add(pid)
        self.emit_game_state()

    @handler(Step.SET_TARGET)
    def set_target(self, pid: PlayerID, target_pid: PlayerID) -> None:
        if pid == self.state.active and pid != target_pid:
            self.state.target = target_pid
            self.state.step = Step.INTERVENE
            self.state.intervene_offers = {target_pid: False}

    @handler(Step.INTERVENE)
    def intervene(self, pid: PlayerID, offer: bool) -> None:
        if pid != self.state.target:
            self.intervene_offers[pid] = offer
        if set(self.state.intervene_offers.keys()) == set(self.player_ids):
            self.state.step = Step.ACK_INTERVENE

    @handler(Step.ACK_INTERVENE)
    def ack_intervene(self, pid: PlayerID, offer_pid: Optional[PlayerID]) -> None:
        if pid == self.state.target:
            if offer_pid is None:
                self.state.intervener = None
                self.state.step = Step.SET_WOUND_I
            elif offer_pid != pid and self.state.intervene_offers[offer_pid]:
                self.state.intervener = offer_pid
                self.state.step = Step.SET_WOUND_I

    @handler(Step.SET_WOUND_I)
    def set_wound_i(self, pid: PlayerID, token: Token):
        raise NotImplementedError

    @handler(Step.SET_ABILITY)
    def no_ability(self, pid: PlayerID):
        raise NotImplementedError

    @handler(Step.SET_ABILITY)
    def elder_ability(self, pid: PlayerID):
        raise NotImplementedError

    @handler(Step.SET_ABILITY)
    def assassin_ability(self, pid: PlayerID, target_pid: PlayerID):
        raise NotImplementedError

    @handler(Step.SET_ABILITY)
    def harlequin_ability(self, pid: PlayerID, target_pid_1: PlayerID, target_pid_2: PlayerID):
        raise NotImplementedError

    @handler(Step.SET_ABILITY)
    def alchemist_ability(self, pid: PlayerID, heal: bool):
        raise NotImplementedError

    @handler(Step.SET_ABILITY)
    def mentalist_ability(self, pid: PlayerID, target_pid: PlayerID):
        raise NotImplementedError

    @handler(Step.SET_ABILITY)
    def guardian_ability(self, pid: PlayerID, target_pid: PlayerID):
        raise NotImplementedError

    @handler(Step.SET_ABILITY)
    def berserker_ability(self, pid: PlayerID):
        raise NotImplementedError

    @handler(Step.SET_ABILITY)
    def mage_ability(self, pid: PlayerID, target_pid: PlayerID):
        raise NotImplementedError

    @handler(Step.SET_ABILITY)
    def courtesan_ability(self, pid: PlayerID, target_pid: PlayerID):
        raise NotImplementedError

