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
  render() {
    const { onMouseDown, player } = this.props;
    const { tokens, items } = player;
    const { name } = player;
    return (
      <li onMouseDown={(event) => {
        this.setState({
          hover: false,
        });
        onMouseDown(event);
      }}
          onMouseLeave={() => this.setState({ hover: false })}
          onMouseEnter={() => this.setState({ hover: true })}
    >{name}
    {' '}
    { tokens.map((token, idx) => {
      if (token === Token.RANK){
        return <span key={idx}><strong>{ player.role }</strong></span>;
      }
      return TOKENTOEMOJI[token];
    }) }
    {' - '}
    { items.map((item, idx) => {
      return <span key={idx}>{ ITEMTOEMOJI[item] }</span>;
    }) }
    </li>
    );
  }
}
