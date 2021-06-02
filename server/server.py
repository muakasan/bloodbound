from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO, emit
import random
import os
from typing import Any

from bloodbound.game import Game
from bloodbound.game_state import PlayerID, Token

app = Flask(__name__, static_folder="../client/build")
socketio = SocketIO(app, cors_allowed_origins="*")

games = {}


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve(path: str) -> Any:
    if path != "" and os.path.exists(app.static_folder + "/" + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, "index.html")


def active_game(func):
    def wrapper(*args):
        global games

        game_code = args[0]
        game = get_or_create_game(game_code)

        new_args = [game] + list(args)[1:]

        ret = func(*new_args)
        if ret is not None:
            games[game_code] = ret

    return wrapper

@socketio.on("requestGameState")
@active_game
def handle_request_game_state(game: Game) -> None:
    game.request_game_state()

@socketio.on('message')
def handle_message(data):
    print('received message: ' + data)

@socketio.on("joinGame")
@active_game
def handle_join_game(game: Game, pid: str) -> None:
    print(f'{pid} joined {game}')
    game.join_game(pid)

@socketio.on("connect")
def test_connection() -> None:
    print("Connected")
    emit('my response', {'data': 'Connected'})

@socketio.on("setTarget")
@active_game
def handle_set_target(game: Game, pid: PlayerID, target_pid: PlayerID) -> None:
    game.set_target(pid, target_pid)

@socketio.on("newGame")
@active_game
def handle_new_game(game: Game) -> None:
    game.new_game()

@socketio.on("noAbility")
@active_game
def handle_no_ability(game: Game, pid: PlayerID) -> None:
    game.no_ability(pid)

@socketio.on("elderAbility")
@active_game
def handle_elder_ability(game: Game, pid: PlayerID) -> None:
    print("Called Elder Ability")
    game.elder_ability(pid)

@socketio.on("assassinAbility")
@active_game
def handle_assassin_ability(game: Game, pid: PlayerID, target_pid: PlayerID) -> None:
    game.assassin_ability(pid, target_pid)

@socketio.on("assassinWound")
@active_game
def handle_assasin_wound(game: Game, pid: PlayerID, token_1: str, token_2: str) -> None:
    game.assassin_wound(pid, Token(token_1), Token(token_2))

@socketio.on("harlequinAbility")
def handle_harlequin_ability(game: Game, pid: PlayerID, target_pid: PlayerID) -> None:
    game.harlequin_ability(pid, target_pid)

@socketio.on("alchemistAbility")
def handle_alchemist_ability(game: Game, pid: PlayerID, target_pid: PlayerID) -> None:
    game.alchemist_ability(pid, target_pid)

@socketio.on("alchemistHeal")
def handle_alchemist_heal(game: Game, pid: PlayerID, target_pid: PlayerID) -> None:
    game.alchemist_heal(pid, target_pid)

@socketio.on("mentalistAbility")
def handle_mentalist_ability(game: Game, pid: PlayerID, target_pid: PlayerID) -> None:
    game.mentalist_ability(pid, target_pid)

@socketio.on("guardianAbility")
def handle_guardian_ability(game: Game, pid: PlayerID, target_pid: PlayerID) -> None:
    game.guardian_ability(pid, target_pid)

@socketio.on("berserkerAbility")
def handle_berserker_ability(game: Game, pid: PlayerID) -> None:
    game.berserker_ability(pid)

@socketio.on("mageAbility")
def handle_mage_ability(game: Game, pid: PlayerID, target_pid: PlayerID) -> None:
    game.mage_ability(pid, target_pid)

@socketio.on("courtesanAbility")
def handle_courtesan_ability(game: Game, pid: PlayerID, target_pid: PlayerID) -> None:
    game.courtesan_ability(pid, target_pid)

@socketio.on("setWoundII")
def handle_set_wound_ii(game: Game, pid: PlayerID, token: str) -> None:
    game.set_wound_ii(pid, Token(token))

@socketio.on("ackComplete")
def handle_ack_complete(game: Game, pid: PlayerID) -> None:
    game.ack_complete(pid)

def get_or_create_game(game_code: str) -> Game:
    global games
    if game_code in games:
        return games[game_code]
    else:
        new_game = Game(socketio, game_code)
        games[game_code] = new_game
        return new_game


if __name__ == "__main__":
    socketio.run(app, port=8080)
