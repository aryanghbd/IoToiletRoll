import { UPDATE_LEADERBOARD, SET_LEADERBOARD } from '../actions/types';
const initialState = {
  leaderboard: [
    { name: "", sheets: 0 }
  ]
};

export default function (state = initialState, action) {
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
          (val) => val.name == action.payload.name ? val.sheets=action.payload.sheets : val
        )
      };
    default:
      return state;
  }
}
