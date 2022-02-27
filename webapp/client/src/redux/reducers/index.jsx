import { combineReducers } from 'redux';
import authReducer from './authReducers';
import errorReducer from './errorReducers';
import mqttReducer from './mqttReducers';

export default combineReducers({
  auth: authReducer,
  errors: errorReducer,
  mqtt: mqttReducer
});
