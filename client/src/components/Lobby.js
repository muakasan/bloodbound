import React, { Component } from "react";
import { Token, Role, Item, Step } from "../enums";
import PlayerCard from "../components/PlayerCard";
import sortPlayers from "../utils.js";

export default class Lobby extends Component {
  constructor(props) {
    super(props);
    this.state = {
    };
  }
  componentDidUpdate(prevProps, prevState) {
    /*
    // Only animate if clue changes
    if (
      prevProps.clues[0].length > 0 &&
      (JSON.stringify(prevProps.clues) !== JSON.stringify(this.props.clues) ||
        prevProps.color !== this.props.color)
    ) {
      this.setState({
        hide: true,
        oldClues: prevProps.clues,
        oldColor: prevProps.color,
      });
      window.setTimeout(() => {
        this.setState({
          hide: false,
        });
      }, 600);
    }
    */
  }

  render() {
    const { players, playerCardClicked } = this.props;
    // const { onMouseDown, player } = this.props;
    // const { tokens, items } = player;
    // const { playerName } = this.state;
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
