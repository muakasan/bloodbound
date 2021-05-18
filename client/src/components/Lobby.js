import React, { Component } from "react";
import { Token, Role, Item, Step } from "../enums";
import PlayerCard from "../components/PlayerCard";

export default class Lobby extends Component {
  render() {
    const { playerIds, playerCardClicked, name } = this.props;
    return (
        <div className="device_parent">
            <p>In Lobby</p>
            <ul>
                { playerIds.map((playerId, index) => <li key={index}>{playerId}</li>)}
            </ul>
            <button>Start Game</button>
        </div>
    );
  }
}
