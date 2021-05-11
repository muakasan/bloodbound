import React, { Component } from "react";
import { useParams } from "react-router-dom";
import socketIOClient from "socket.io-client";
import PlayerCard from "../components/PlayerCard";

/*
import { LeftBrain, RightBrain } from "../components/Shapes";
import DirectionToggle from "../components/DirectionToggle";
import Clue from "../components/Clue";
import Target from "../components/Target";
import ScoreIndicator from "../components/ScoreIndicator";
*/
import { Token, Role, Item, Step } from "../enums";

export default function Game() {
  let { lobbyId } = useParams();
  return <Device lobbyId={lobbyId} />;
}
// https://stackoverflow.com/a/9188211
// Converts player dict to array and sorts by position
// TODO handle putting current player last
function sortPlayers(playersDict){
  let playersArray = Object.values(playersDict);
  playersArray.sort(function(a, b){
    return a.position < b.position ? 1 : -1
  });
  return playersArray
}
class Device extends Component {
  constructor(props) {
    super(props);

    this.deviceInner = React.createRef();
    this.state = {
      gameState: {},
      psychic: false,
      controlsDisabled: false,
      client: null,
      roundNum: 0,
      gameId: 0,
      loading: true,
    };
  }

  disableControls() {
    this.setState({
      controlsDisabled: true,
    });
    window.setTimeout(() => {
      this.setState({
        controlsDisabled: false,
      });
    }, 1010);
  }

  componentDidMount() {
    const serverUrl = process.env.NODE_ENV === "production" ? "/" : ":8080/";
    const client = socketIOClient(serverUrl);
    const { lobbyId } = this.props;

    client.on("connect", () => {
      client.emit("requestGameState", lobbyId);
      console.log("REQUEST GAME STATE " + lobbyId);
    });
    client.on("gameState", (updatedState) => {
      const gameState = this.state.gameState;

      // If we update target position right away it reveals the result...
      const targetPosition = updatedState.targetPosition;
      if (!this.state.loading) {
        delete updatedState.targetPosition;
      }

      // Reset peek on new round
      let psychic = this.state.psychic;
      if (
        updatedState.roundNum !== gameState.roundNum ||
        updatedState.gameId !== gameState.gameId
      ) {
        psychic = false;
        this.disableControls();
      }

      this.setState({
        gameState: { ...gameState, ...updatedState },
        psychic: psychic,
        loading: false,
      });

      window.setTimeout(() => {
        const gameState = this.state.gameState;
        this.setState({
          gameState: { ...gameState, targetPosition: targetPosition },
        });
      }, 1010);
    });
    this.setState({
      client: client,
    });
  }
  playerCardClicked = (event) => {
    console.log("Hello at PlayerCard");
    /*
    const { client, gameState, psychic, controlsDisabled } = this.state;
    const { lobbyId } = this.props;

    if (!gameState.screenClosed || psychic || controlsDisabled) {
      return;
    }

    this.setState({
      gameState: {
        ...gameState,
        direction: Direction.getOther(gameState.direction),
        },
      },
      () => {
        client.emit("setDirection", lobbyId, this.state.gameState.direction);
    });
    */
  };
  // togglePsychicClicked = (event) => {
  //   const { psychic, controlsDisabled } = this.state;

  //   if (controlsDisabled) {
  //     return;
  //   }

  //   this.setState({
  //     psychic: !psychic,
  //   });
  // };

  // directionToggleClicked = (event) => {
  //   const { client, gameState, psychic, controlsDisabled } = this.state;
  //   const { lobbyId } = this.props;

  //   if (!gameState.screenClosed || psychic || controlsDisabled) {
  //     return;
  //   }

  //   this.setState(
  //     {
  //       gameState: {
  //         ...gameState,
  //         direction: Direction.getOther(gameState.direction),
  //       },
  //     },
  //     () => {
  //       client.emit("setDirection", lobbyId, this.state.gameState.direction);
  //     }
  //   );
  // };

  // newGameClicked = (event) => {
  //   let { client, controlsDisabled } = this.state;
  //   const { lobbyId } = this.props;

  //   if (controlsDisabled) {
  //     return;
  //   }

  //   this.disableControls();
  //   client.emit("newGame", lobbyId);
  // };

  // dialClicked = (event) => {
  //   const { client, gameState, psychic, controlsDisabled } = this.state;
  //   const { lobbyId } = this.props;
  //   if (!gameState.screenClosed || psychic || controlsDisabled) {
  //     return;
  //   }

  //   const rect = this.deviceInner.current.getBoundingClientRect();

  //   const xOrigin = rect.x + rect.width / 2;
  //   const yOrigin = rect.y + rect.height;

  //   const xOffset = event.clientX - xOrigin;
  //   const yOffset = event.clientY - yOrigin;

  //   let rotation = 2 * Math.PI - Math.atan2(xOffset, yOffset);
  //   if (rotation > 2 * Math.PI) {
  //     rotation -= 2 * Math.PI;
  //   }

  //   let dialPosition = rotation / Math.PI - 0.5;
  //   dialPosition = Math.min(dialPosition, 0.95);
  //   dialPosition = Math.max(dialPosition, 0.05);

  //   this.setState(
  //     {
  //       gameState: {
  //         ...gameState,
  //         dialPosition: dialPosition,
  //       },
  //     },
  //     () => {
  //       client.emit(
  //         "setDialPosition",
  //         lobbyId,
  //         this.state.gameState.dialPosition
  //       );
  //     }
  //   );
  // };

  screenHandleClicked = (event) => {
    let { client, gameState, controlsDisabled } = this.state;
    let { screenClosed, targetPosition } = gameState;
    const { lobbyId } = this.props;

    if (controlsDisabled) {
      return;
    }

    this.setState(
      {
        gameState: {
          ...gameState,
          screenClosed: !screenClosed,
          targetPosition: targetPosition,
        },
      },
      () => {
        if (screenClosed) {
          client.emit("reveal", lobbyId);
        } else {
          this.setState({
            psychic: false,
          });
          client.emit("nextRound", lobbyId);
        }
      }
    );
  };

  render() {
    const { psychic, gameState, loading } = this.state;

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
    console.log(typeof players);
    let playersList = sortPlayers(players);
    if (step === Step.LOBBY){
      console.log(gameState);
      return (
        <div className="device_parent">
        <p>In Lobby</p>
        <ul>
          { playersList.map((value, index) => {
            return <PlayerCard 
              onMouseDown={this.playerCardClicked}
              player={value}/>
          })}
        </ul>
        </div>
      )
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
    }
    // const rotation = Math.PI * (dialPosition + 1.5);

    /*
    const winner =
      score[Team.LEFT_BRAIN] <= score[Team.RIGHT_BRAIN]
        ? Team.RIGHT_BRAIN
        : Team.LEFT_BRAIN;

    return (
      <div className="device_parent">
        <div className="device_outer">
          <div className="device">
            <div className="device_red" />
            <div className="device_wing_l" />
            <div className="device_wing_r" />

            <div
              className="device_inner"
              ref={this.deviceInner}
              onMouseDown={this.dialClicked}
            >
              <div
                className="dial"
                style={{ transform: `rotate(${rotation}rad)` }}
              />
              <Target targetPosition={targetPosition} />
              <div
                className={(psychic ? "peek" : "") + " screen"}
                style={{ transform: `rotate(${screenClosed ? 360 : 187}deg)` }}
              />
            </div>

            <div
              className="screenHandle"
              onMouseDown={
                complete ? this.newGameClicked : this.screenHandleClicked
              }
              style={{
                transform: `rotate(${screenClosed ? 356.5 : 183.5}deg)`,
              }}
            >
              <div
                className={
                  (screenClosed ? "" : "flipped") + " screenHandleText"
                }
              >
                <span>{screenClosed ? "Reveal" : "Next Round"}</span>
              </div>
            </div>
          </div>
          <div className="togglePeek" onMouseDown={this.togglePsychicClicked}>
            Psychic
          </div>
          <DirectionToggle
            direction={direction}
            onMouseDown={this.directionToggleClicked}
            psychic={psychic}
          />
          <Clue clues={clues} color={clueColor} />
          <ScoreIndicator
            isTurn={turn === Team.LEFT_BRAIN}
            team={Team.LEFT_BRAIN}
            score={score[Team.LEFT_BRAIN]}
          />
          <ScoreIndicator
            isTurn={turn === Team.RIGHT_BRAIN}
            team={Team.RIGHT_BRAIN}
            score={score[Team.RIGHT_BRAIN]}
          />
          {complete ? (
            <div className="gameOver">
              {winner == Team.LEFT_BRAIN ? <LeftBrain /> : <RightBrain />}
              Team {winner ? "Right" : "Left"} Brain wins!
              <div className="newGame" onMouseDown={this.newGameClicked}>
                New Game
              </div>
            </div>
          ) : (
            ""
          )}
        </div>
      </div>
    );*/
  }    

}
