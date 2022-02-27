import { UPDATE_LEADERBOARD, SET_LEADERBOARD } from './types'; // Register User
import store from '../store';

var mqtt = require('mqtt')

var client = mqtt.connect('mqtt://test.mosquitto.org:8080', { clientId: "clientId-p932yNuIfk" })

// handle connect
client.on("connect", function () {
  console.log("connected  " + client.connected);
  console.log("subscibing to topic: score");
  client.subscribe("score")
})

// handle messages
client.on("message", function(topic, payload) {
  let json = payload.toJSON()
  let updateValue = JSON.parse(json)
  store.dispatch(updateLeaderboard(updateValue))
})

// handle errors - exit
client.on("error", function (error) {
  console.log("Can't connect" + error);
  process.exit(1)
});

export const updateLeaderboard = (updateValue) => dispatch => {
  dispatch({
    type: UPDATE_LEADERBOARD,
    payload: updateValue
  })
}


export const publishHousehold = (household, callback) => dispatch => {
  console.log("publishing topic: household", " message: ", household);

  if (client.connected == true) {
    client.publish('household')
  }

  let initialLeaderboard = JSON.parse(household).map((val) => ({name: val.name, sheets: 0}))


  dispatch({
    type: SET_LEADERBOARD,
    payload: initialLeaderboard
  })
}