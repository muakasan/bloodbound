import React, { Component } from "react";
import { withRouter } from "react-router-dom";
import io from "socket.io-client";
import PlayerCard from "../components/PlayerCard";
import ChooseName from "../components/ChooseName";
import Lobby from "../components/Lobby";

import { Token, Role, Item, Step } from "../enums";


class Device extends Component {
  constructor(props) {
    super(props);

    this.lobbyId = this.props.match.params.lobbyId;
    this.deviceInner = React.createRef();
    this.state = {
      playerName: "",
      gameState: {},
      loading: true
    };
  }

  componentDidMount() {
    const serverUrl = process.env.NODE_ENV === "production" ? "/" : ":8080/";
    const client = io(serverUrl);
    client.on("connect", (socket) => {
      client.emit("requestGameState", this.lobbyId);
    });
    client.on("gameState", (updatedState) => {
      const { gameState } = this.state;
      this.setState({ loading: false, gameState: { ...gameState, ...updatedState }});
      console.log(`UPDATED GAME STATE: ${updatedState}`)
    });
    this.client = client;
  }

  setPlayerName = (playerName) => {
    this.setState({
      playerName: playerName
    });
    this.client.emit("joinGame", this.lobbyId, playerName);
  }
  playerCardClicked = (event) => {
    console.log("Hello at PlayerCard");
  };

  render() {
    const { gameState, playerName, loading } = this.state;

    const elements = ['test', 'test2'];
    if (loading) {
      return (

        <div className="device_parent">
          <p>Would you like to intervene?</p>
          <ul>
            <li>Yes</li>
            <li>No</li> 
          </ul>
          <p>Who would you like to intervene?</p>
          <ul>
            <li>Yes</li>
            <li>No</li> 
          </ul>
          <p>Pick Your Wound</p>
          <ul>
            <li>Red</li>
            <li>Blue</li>
            <li>Mystery</li>
            <li>Rank</li>
          </ul> 
          <ul>
            <li>Red</li>
            <li>Blue</li>
            <li>Mystery</li>
            <li>Rank</li>
          </ul> 
          <ul>
            {elements.map((value, index) => {
            return <li key={index}>{value}</li>
            })}
          </ul>
          <div className="device_outer">
            <div className="device">
              <div className="device_red" />
              <div className="device_wing_l" />
              <div className="device_wing_r" />
              <div className="device_inner" />
            </div>
          </div>
        </div>
      );
    }

    const {
      players, 
      step
    } = gameState;
    if (step === Step.LOBBY){
      console.log(gameState);
      if (playerName === ""){
        return <ChooseName setPlayerName={this.setPlayerName}/>
      }
      return <Lobby players={players} playerCardClicked={this.playerCardClicked} name={playerName}/>
    }
    if (step === Step.INGAME){
      return (
        <div className="device_parent">
          <p>Would you like to intervene?</p>
          <ul>
            <li>Yes</li>
            <li>No</li> 
          </ul>
          <p>Who would you like to intervene?</p>
          <ul>
            <li>Yes</li>
            <li>No</li> 
          </ul>
          <p>Pick Your Wound</p>
          <ul>
            <li>Red</li>
            <li>Blue</li>
            <li>Mystery</li>
            <li>Rank</li>
          </ul> 
          <ul>
            <li>Red</li>
            <li>Blue</li>
            <li>Mystery</li>
            <li>Rank</li>
          </ul> 
          <ul>
            {elements.map((value, index) => {
            return <li key={index}>{value}</li>
            })}
          </ul>
        </div>
      );        
    }
    if (step === Step.COMPLETE){
      return (
        <div className="device_parent">
        <p>Game Over</p>
        </div>
      )
    } else {
      throw Error(`Unable to render! Unknown step: ${step}.`);
    }
  }

}

export default withRouter(Device);
