import { UPDATE_LEADERBOARD, SET_LEADERBOARD } from '../actions/types';
const initialState = {
  leaderboard: [
    { name: "alnvjsdnvjlslvsj d", sheets: 1 },
    { name: "b", sheets: 2 },
    { name: "c", sheets: 3 },
    { name: "d", sheets: 4 },
    { name: "e", sheets: 5 },
    { name: "f", sheets: 6 },
    { name: "g", sheets: 7 }
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
          (val) => val.name == action.payload.name ? action.payload : val
        )
      };
    default:
      return state;
  }
}
