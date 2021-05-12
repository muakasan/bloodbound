import React, { Component } from "react";
import { Token, Role, Item, Step } from "../enums";
import PlayerCard from "../components/PlayerCard";
import sortPlayers from "../utils.js";

export default class Lobby extends Component {
  render() {
    const { players, playerCardClicked, name } = this.props;
    let playersList = sortPlayers(players);
    return (
        <div className="device_parent">
            <p>In Lobby</p>
            <ul>
                { playersList.map((value, index) => {
                return <PlayerCard 
                    onMouseDown={playerCardClicked}
                    player={value}
                    key={index}/>
                })}
            </ul>
            <button>Start Game</button>
        </div>
    );
  }
}
