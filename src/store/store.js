import { combineReducers, configureStore } from '@reduxjs/toolkit';
import { reducer as users } from './users/Users.slice';

const reducers = combineReducers({
	users: users,
});

export const store = configureStore({
	reducer: reducers,
});
