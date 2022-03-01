import { combineReducers } from 'redux';
import authReducer from './authReducers';
import errorReducer from './errorReducers';
import rollingReducers from './rollingReducers';
import mqttReducer from './mqttReducers';

export default combineReducers({
  auth: authReducer,
  errors: errorReducer,
  mqtt: mqttReducer,
  rolling: rollingReducers
});
