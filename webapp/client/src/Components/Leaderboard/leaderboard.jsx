import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import Leaderboard1 from './leaderboard1.jsx';

var mqtt = require('mqtt')

var client = mqtt.connect('mqtt://test.mosquitto.org:8080', { clientId: "clientId-p932yNuIfk" })
console.log("connected flag  " + client.connected);

client.on("connect", function () {
  console.log("connected  " + client.connected);
})

//handle errors
client.on("error", function (error) {
  console.log("Can't connect" + error);
  process.exit(1)
});

//publish
function subscribe(message, callback) {
  console.log("subscibing to topic: score");

  if (client.connected == true) {
    client.subscribe("score")
  }
}

class Leaderboard extends Component {
  constructor(props) {
    super(props)
    this.state = {
      users: props.leaderboard,
      paginate: 100
    };
  }
  render() {
    return (
      <div>
        <h1 className="text-capitalize">
          hello </h1>
        <div>
          <Leaderboard1 users={this.state.users} paginate={this.state.paginate} />
        </div>
      </div>
    );
  }
}

Leaderboard.propTypes = {
  leaderboard: PropTypes.array.isRequired
};

const mapStateToProps = state => ({
  leaderboard: state.mqtt.leaderboard
});

export default connect(mapStateToProps, {})(Leaderboard);