import React, { Component } from "react";

const EMOJIS = {
  RED_CIRCLE: String.fromCodePoint(0x1F534),
  BLUE_CIRCLE: String.fromCodePoint(0x1F535),
  WHITE_CIRCLE: String.fromCodePoint(0x26AA),
  KNIFE: String.fromCodePoint(0x1F52A),
  QUILL: String.fromCodePoint(0x2712, 0xFE0F), // Pen Nib
  SWORD: String.fromCodePoint(0x2694, 0xFE0F),
  SHIELD: String.fromCodePoint(0x1F6E1, 0xFE0F),
  FAN: String.fromCodePoint(0x1F341), // Maple Leaf
  STAFF: String.fromCodePoint(0x1F9AF), // White Cane 
  CURSE: String.fromCodePoint(0x1F4D3), // Notebook 
}

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
    const { onMouseDown } = this.props;
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
    >{playerName} {EMOJIS.RED_CIRCLE} {EMOJIS.BLUE_CIRCLE} {EMOJIS.WHITE_CIRCLE} {EMOJIS.KNIFE} {EMOJIS.QUILL} {EMOJIS.SWORD} {EMOJIS.SHIELD} {EMOJIS.FAN} {EMOJIS.STAFF}</li>
    );
  }
}
