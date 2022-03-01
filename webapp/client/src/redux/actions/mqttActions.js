import { UPDATE_LEADERBOARD, SET_LEADERBOARD, SET_USERS } from './types'; // Register User
import store from '../store';

var mqtt = require('mqtt')

var client = mqtt.connect('mqtt://test.mosquitto.org:8080')

// handle connect
client.on("connect", function () {
  console.log("connected  " + client.connected);
  console.log("subscibing to topic: score");
  client.subscribe("score")
})

// handle messages
client.on("message", function(topic, payload) {
  let json = payload.toString()
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

function renameKey ( obj, oldKey, newKey ) {
  obj[newKey] = obj[oldKey];
  delete obj[oldKey];
}

function changeVal(obj, key1, key2){
  let val = obj[key1]
  obj[key2] = val
}


export const publishHousehold = (household, callback) => dispatch => {
  console.log("publishing topic: household", " message: ", household);

  if (client.connected == true) {
    client.publish('household', household)
  }

  let initialLeaderboard = JSON.parse(household).map((val) => ({name: val.name, sheets: 0}))
  let initialUsers = JSON.parse(household)
  initialUsers.forEach( x => renameKey( x, 'name', 'value' ) );
  initialUsers.forEach( x => changeVal( x, 'value', 'number'))
  initialUsers.forEach( x => renameKey( x, 'number', 'label' ) );

    console.log(initialUsers)
  dispatch({
    type: SET_LEADERBOARD,
    payload: initialLeaderboard
  })

  dispatch({
    type: SET_USERS,
    payload: initialUsers
  })
}