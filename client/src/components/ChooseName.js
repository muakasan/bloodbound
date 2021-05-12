import React, { Component } from "react";

export default class ChooseName extends Component {
  constructor(props) {
    super(props);
    this.state = {
      formText: "", // The player's name
    };
  }

  handleSubmit = (event) => {
    event.preventDefault();
    const { formText } = this.state;
    const { setPlayerName } = this.props;
    setPlayerName(formText);
};

  onChange = (event) => {
    this.setState({
      formText: event.target.value,
    });
  };

  render() {
    const { formText } = this.state;
    return (
        <div className="homepage">
        <h2>Choose your name</h2>
        <form onSubmit={this.handleSubmit}>
        <input type="text" value={formText} onChange={this.onChange} />
        </form>
    </div>
    );
  }
}