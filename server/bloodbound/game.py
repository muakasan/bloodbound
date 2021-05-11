from bloodbound.game_state import PlayerID, GameState, Team, Step
from flask_socketio import SocketIO, join_room
import random
import json



class Game:
    def handler(*steps: Step):
        def _dec(func):
            def _wrap(*args):
                valid = True
                # Check game step valid
                if steps and (self.state.step not in steps):
                    valid = False
                # Check player ids valid
                for arg, _type in zip(args, func.__annotations.values()):
                    if _type is PlayerID and arg not in self.player_ids:
                        valid = False
                if valid:
                    res = func(*args)
                self.emit_game_state()
                return res
            return _wrap
        return _dec

    def __init__(self, sio: SocketIO, game_code: str):
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
        self.state = GameState.build(self.player_ids)

    @handler(Step.LOBBY)
    def join_game(self, pid: PlayerID) -> None:
        join_room(self.game_code)
        self.player_ids.add(pid)

    @handler(Step.INGAME)
    def set_target(self, pid: PlayerID, target_pid: PlayerID) -> None:
        self.state.target = target_pid
