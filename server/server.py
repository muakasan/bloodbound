from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO, join_room
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


@socketio.on("joinGame")
@active_game
def handle_join_game(game: Game, pid: PlayerID) -> None:
    game.join_game(pid)


@socketio.on("setTarget")
@active_game
def handle_set_target(game: Game, pid: PlayerID, target_pid: PlayerID) -> None:
    game.set_target(pid, target_pid)


@socketio.on("newGame")
@active_game
def handle_new_game(game: Game) -> None:
    game.new_game()


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
