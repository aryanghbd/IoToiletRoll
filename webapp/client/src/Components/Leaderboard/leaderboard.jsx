import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import Leaderboard1 from './leaderboard1.jsx';


class Leaderboard extends Component {
  constructor(props) {
    super(props)
    this.state = {
      users: props.leaderboard,
      paginate: 10
    };
  }
  render() {
    return (
      <div>
        <div style={{marginTop: 56}} className="container">
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