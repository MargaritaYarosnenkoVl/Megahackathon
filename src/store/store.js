import { combineReducers, configureStore } from '@reduxjs/toolkit';
import { reducer as interlayer } from './interlayer/Interlayer.slice';
import { reducer as users } from './users/Users.slice';

const reducers = combineReducers({
	users: users,
	interlayer: interlayer,
});

export const store = configureStore({
	reducer: reducers,
});
