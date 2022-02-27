import React, { Component } from 'react';
import { render } from 'react-dom';
import Leaderboard1 from './leaderboard1.jsx';

class Leaderboard extends Component {
  constructor(props) {
  super(props);
  this.state = {
    users: [{name: "Tj", score: 1},
            {name: "Chris", score: 69},
            {name: "Dave", score: 17},
            {name: "Ben", score: 11},
            {name: "Caty", score: 21},
            {name: "Miller", score: 33},
            {name: "Zack", score: 88},
            {name: "Sam", score: 42},
            {name: "Nicky", score: 22},
            {name: "Cheyenne", score: 55},
            {name: "Adela", score: 72},
            {name: "Wongo", score: 35},
            {name: "Brett", score: 98},
            {name: "Gina", score: 4},
            {name: "Allen", score: 7},
            {name: "Matt", score: 46},
            {name: "Amanda", score: 31},
            {name: "Jamie", score: 100},
            {name: "Sarah", score: 56},
            {name: "Owen", score: 45}],
    paginate: 100
  };
}
  render() {
    return (
    <div> 
        <h1 className="text-capitalize">
         hello </h1>
      <div>
        <Leaderboard1 users={this.state.users} paginate={this.state.paginate}/>
      </div>
    </div>
    );
  }
}

export default Leaderboard;