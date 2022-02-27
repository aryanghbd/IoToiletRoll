import { UPDATE_LEADERBOARD, SET_LEADERBOARD } from '../actions/types';
const initialState = {
    leaderboard: [{name: "", score: 0}]
};

export default function(state = initialState, action) {
  switch (action.type) {
    case SET_LEADERBOARD:
      return {
        ...state,
        leaderboard: action.payload
      }
    case UPDATE_LEADERBOARD:
      return {
        ...state,
        leaderboard: state.leaderboard.map(
          (val) => val.name == action.payload.name ? action.payload : val
        )
      };
    default:
      return state;
  }
}
