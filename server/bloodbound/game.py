from typing import Optional
#from bloodbound.game_state import PlayerID, GameState, Item, Role, Team, Step, Token
from game_state import PlayerID, GameState, Item, Role, Team, Step, Token
from flask_socketio import SocketIO, join_room
import random

GameCode = str

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
                res = func(self, *args) if valid else None
                self.emit_game_state()
                return res
            return _wrap
        return _dec

    def _wound_helper(self, pid: PlayerID, token: Token):
        player = self.state.players[pid]
        if token not in player.tokens:
            return False
        player.shown_tokens.append(token)
        #TODO: special case for inquisitor tokens
        player.tokens.remove(token)
        if len(player.shown_tokens) == 3: 
            for sword, shield in [(Item.SWORD_I, Item.SHIELD_I), (Item.SWORD_II, Item.SHIELD_II)]:
                if sword in player.items:
                    player.items.remove(sword)
                    for p in self.player_ids:
                        if shield in self.state.players[p].items:
                            self.state.players[p].items.remove(shield)
        return True

    def __init__(self, sio: SocketIO, game_code: GameCode):
        self.sio = sio
        self.game_code = game_code
        self.player_ids = set()
        self.state = GameState()

    def request_game_state(self) -> None:
        join_room(self.game_code)
        self.emit_game_state()

    def emit_game_state(self) -> None:
        self.sio.emit("gameState", self.state.encode(), json=True, room=self.game_code)

    def join_game(self, pid: PlayerID) -> None:
        if self.state.step == Step.LOBBY:
            join_room(self.game_code)
            self.player_ids.add(pid)
        self.emit_game_state()

    @handler(Step.LOBBY)
    def start_game(self, pid: PlayerID) -> None:
        self.state.reset(self.player_ids)
        self.state.step = Step.ACK_PEEK

    @handler(Step.ACK_PEEK)
    def ack_peek(self, pid: PlayerID) -> None:
        self.state.peeked[pid] = True
        if set(self.state.peeked.keys()) == set(self.player_ids):
            self.state.active = random.choice(list(self.player_ids))
            self.state.step = Step.SET_TARGET

    # Stabbing
    @handler(Step.SET_TARGET)
    def set_target(self, pid: PlayerID, target_pid: PlayerID) -> None:
        target = self.state.players[target_pid]
        if pid == self.state.active and pid != target_pid and \
                (Item.SHIELD_I not in target.items) and \
                (Item.SHIELD_II not in target.items):
            self.state.target = target_pid
            if Item.FAN in target.items and len(player.shown_tokens) == 3:
                self.state.captured = target_pid
                self.state.step = Step.COMPLETE
            elif Item.FAN in target.items:
                self.state.intervener = None
                self.state.wounded = target_pid
                self.state.step = Step.SET_WOUND_I
            else:
                # the target and players showing rank cannot intervene
                ineligible_players = [target_pid] + [p for p in self.player_ids if \
                        Token.RANK in self.state.players[p].shown_tokens]
                self.state.intervene_offers = {p: False for p in ineligible_players}
                self.state.step = Step.INTERVENE

    @handler(Step.INTERVENE)
    def intervene(self, pid: PlayerID, offer: bool) -> None:
        player = self.state.players[pid]
        if pid != self.state.target and \
                (Token.RANK not in player.shown_tokens):
            self.state.intervene_offers[pid] = offer
        if set(self.state.intervene_offers.keys()) == set(self.player_ids):
            self.state.step = Step.ACK_INTERVENE

    @handler(Step.ACK_INTERVENE)
    def ack_intervene(self, pid: PlayerID, offer_pid: Optional[PlayerID]) -> None:
        player = self.state.players[pid]
        if pid == self.state.target:
            if offer_pid is None and len(player.shown_tokens) == 3:
                self.state.captured = pid
                self.state.step = Step.COMPLETE
            elif offer_pid is None:
                self.state.intervener = None
                self.state.wounded = pid
                self.state.step = Step.SET_WOUND_I
            elif offer_pid != pid and self.state.intervene_offers[offer_pid]:
                self.state.intervener = offer_pid
                self.state.wounded = offer_pid
                self.state.step = Step.SET_ABILITY

    # No intervention
    @handler(Step.SET_WOUND_I)
    def set_wound_i(self, pid: PlayerID, token: Token):
        player = self.state.players[pid]
        if pid == self.state.target and self._wound_helper(pid, token):
            if token == Token.RANK:
                self.state.step = Step.SET_ABILITY
            else:
                self.state.active = pid
                self.state.step = Step.SET_TARGET

    @handler(Step.SET_ABILITY)
    def no_ability(self, pid: PlayerID):
        if pid == self.state.wounded:
            self.state.active = pid
            self.state.step = Step.SET_TARGET

    @handler(Step.SET_ABILITY)
    def elder_ability(self, pid: PlayerID):
        player = self.state.players[pid]
        if pid == self.state.wounded and player.role == Role.ELDER:
            player.items.append(Item.QUILL)
            self.state.active = pid
            self.state.step = Step.SET_TARGET

    @handler(Step.SET_ABILITY)
    def assassin_ability(self, pid: PlayerID, target_pid: PlayerID):
        player = self.state.players[pid]
        if pid == self.state.wounded and player.role == Role.ASSASSIN:
            target = self.state.players[target_pid]
            if len(target.shown_tokens) >= 2:
                self.state.captured = target_pid
                self.state.step = Step.COMPLETE
            else:
                self.state.wounded = target_pid
                self.state.step = Step.ASSASSIN_WOUND

    @handler(Step.ASSASSIN_WOUND)
    def assassin_wound(self, pid: PlayerID, token_1: Token, token_2: Token):
        player = self.state.players[pid]
        if pid == self.state.wounded:
            if self._wound_helper(pid, token_1) and \
                    self._wound_helper(pid, token_2):
                self.state.active = pid
                self.state.step = Step.SET_TARGET

    @handler(Step.SET_ABILITY)
    def harlequin_ability(self, pid: PlayerID, target_pid_1: PlayerID, target_pid_2: PlayerID):
        player = self.state.players[pid]
        if pid == self.state.wounded and player.role == Role.HARLEQUIN and \
                target_pid_1 != target_pid_2:
            self.state.active = pid
            self.state.step = Step.SET_TARGET

    @handler(Step.SET_ABILITY)
    def alchemist_ability(self, pid: PlayerID, heal: bool):
        player = self.state.players[pid]
        if pid == self.state.wounded and player.role == Role.ALCHEMIST and \
                pid == self.state.intervener:
            target = self.state.players[self.state.target]
            
            if heal and len(target.shown_tokens):
                self.state.step = Step.ALCH_HEAL
            elif heal: # target is not wounded, cannot heal
                self.state.active = pid
                self.state.step = Step.SET_TARGET
            elif len(target.shown_tokens) == 3:
                self.state.captured = self.state.target
                self.state.step = Step.COMPLETE
            else:
                self.state.wounded = self.state.target
                self.state.next_active = pid
                self.state.step = Step.SET_WOUND_II

    @handler(Step.ALCHEMIST_HEAL)
    def alchemist_heal(self, pid: PlayerID, token: Token):
        player = self.state.players[pid]
        if pid == self.state.target and token in player.shown_tokens:
            #TODO: special case for inquisitor tokens
            player.shown_tokens.remove(token)
            player.tokens.append(token)
            self.state.active = self.state.intervener
            self.state.step = Step.SET_TARGET

    @handler(Step.SET_ABILITY)
    def mentalist_ability(self, pid: PlayerID, target_pid: PlayerID):
        player = self.state.players[pid]
        if pid == self.state.wounded and player.role == Role.MENTALIST:
            target = self.state.players[target_pid]
            if len(target.shown_tokens) == 3:
                self.state.captured = target_pid
                self.state.step = Step.COMPLETE
            elif Token.RANK not in target.shown_tokens:
                self._wound_helper(target_pid, Token.RANK)
                self.state.active = target_pid
                self.state.step = Step.SET_TARGET
            else:
                self.state.wounded = target_pid
                self.state.next_active = target_pid
                self.state.step = Step.SET_WOUND_II

    @handler(Step.SET_ABILITY)
    def guardian_ability(self, pid: PlayerID, target_pid: PlayerID):
        player = self.state.players[pid]
        if pid == self.state.wounded and player.role == Role.GUARDIAN:
            target = self.state.players[target_pid]
            # Give SWORD/SHIELD_I if nobody else has SWORD_I, else SWORD_II
            give_sword_i = not any([Item.SWORD_I in self.state.players[p].items \
                for p in self.player_ids and p != pid])
            sword, shield = (Item.SWORD_I, Item.SHIELD_I) if give_sword_i else (Item.SWORD_II, Item.SHIELD_II)
            if sword not in player.items:
                player.items.append(sword)
            if shield not in target.items:
                target.items.append(shield)
            self.state.active = pid
            self.state.step = Step.SET_TARGET

    @handler(Step.SET_ABILITY)
    def berserker_ability(self, pid: PlayerID):
        player = self.state.players[pid]
        if pid == self.state.wounded and player.role == Role.BERSERKER:
            active = self.state.players[self.state.active]
            if len(active.shown_tokens) == 3:
                self.state.captured = self.state.active
                self.state.step = Step.COMPLETE
            else:
                self.state.wounded = target_pid
                self.state.next_active = pid
                self.state.step = Step.SET_WOUND_II

    @handler(Step.SET_ABILITY)
    def mage_ability(self, pid: PlayerID, target_pid: PlayerID):
        player = self.state.players[pid]
        if pid == self.state.wounded and player.role == Role.MAGE:
            target = self.state.players[target_pid]
            if Item.STAFF not in player.items:
                player.items.append(Item.STAFF)
            target.items.append(Item.STAFF)
            self.state.active = pid
            self.state.step = Step.SET_TARGET

    @handler(Step.SET_ABILITY)
    def courtesan_ability(self, pid: PlayerID, target_pid: PlayerID):
        player = self.state.players[pid]
        if pid == self.state.wounded and player.role == Role.COURTESAN:
            target = self.state.players[target_pid]
            target.items.append(Item.FAN)
            self.state.active = pid
            self.state.step = Step.SET_TARGET

    @handler(Step.SET_WOUND_II)
    def set_wound_ii(self, pid: PlayerID, token: Token):
        player = self.state.players[pid]
        if pid == self.state.wounded and self._wound_helper(pid, token):
            self.state.active = self.state.next_active
            self.state.step = Step.SET_TARGET

    @handler(Step.COMPLETE)
    def ack_complete(self, pid: PlayerID):
        self.state.complete_acked[pid] = True
        if set(self.state.complete_acked.keys()) == set(self.player_ids):
            self.state.reset(self.player_ids)
            self.state.step = Step.ACK_PEEK
        

if __name__ == "__main__":
    # Mock SocketIO for unit testing
    from json import dumps
    class SocketIO:
        def __init__(self):
            self.rooms = {}

        def emit(self, msg, data, json, room):
            print(f'\n{msg}@{room}(JSON:{json}):')
            print(dumps(data, sort_keys=True, indent=4))

    def join_room(game_code: GameCode):
        print(f'joined room {game_code}')

    pids = ["aidan", "duke", "kelvin", "aaron", "piotr", "ankur", "zaaim", "annie"]

    sio = SocketIO()
    game = Game(sio, "Coven")
    for pid in pids:
        game.join_game(pid)
    game.start_game('aidan')
    for pid in pids:
        game.ack_peek(pid)
    import pdb
    pdb.set_trace()
