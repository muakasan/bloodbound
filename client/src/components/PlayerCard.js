import React, { Component } from "react";
import { Token, Role, Item, Step } from "../enums";

let ITEMTOEMOJI = {}
ITEMTOEMOJI[Item.QUILL] = String.fromCodePoint(0x2712, 0xFE0F);
ITEMTOEMOJI[Item.SWORD] = String.fromCodePoint(0x2694, 0xFE0F); // Crossed Swords
ITEMTOEMOJI[Item.SHIELD] = String.fromCodePoint(0x1F6E1, 0xFE0F); // Shield
ITEMTOEMOJI[Item.FAN] = String.fromCodePoint(0x1F341); // Maple Leaf
ITEMTOEMOJI[Item.STAFF] = String.fromCodePoint(0x1F9AF); // White Cane 
ITEMTOEMOJI[Item.TRUECURSE] = String.fromCodePoint(0x1F4D3); // Notebook 
ITEMTOEMOJI[Item.FALSECURSE] = String.fromCodePoint(0x1F4D3); // Notebook

let TOKENTOEMOJI = {}
TOKENTOEMOJI[Token.BLUE] = String.fromCodePoint(0x1F535); // Blue Circle
TOKENTOEMOJI[Token.RED] = String.fromCodePoint(0x1F534); // Red Circle
TOKENTOEMOJI[Token.GREY] = String.fromCodePoint(0x26AA); // White Circle

export default class PlayerCard extends Component {
  constructor(props) {
    super(props);
    this.state = {
      playerName: "Aidan",
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
    const { onMouseDown, player } = this.props;
    const { tokens, items } = player;
    const { playerName } = this.state;
    return (
      <li onMouseDown={(event) => {
        this.setState({
          hover: false,
        });
        onMouseDown(event);
      }}
      onMouseLeave={() => this.setState({ hover: false })}
      onMouseEnter={() => this.setState({ hover: true })}
    >{playerName}
    {' '}
    { tokens.map(token => {
      if (token === Token.RANK){
        return <strong>{ player.role }</strong>;
      }
      return TOKENTOEMOJI[token];
    }) }
    {' - '}
    { items.map(item => {
      return ITEMTOEMOJI[item];
    }) }
    </li>
    );
  }
}
