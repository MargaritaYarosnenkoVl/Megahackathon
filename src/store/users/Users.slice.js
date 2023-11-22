import { createSlice } from '@reduxjs/toolkit';

const initialState = [
	{
		id: 0,
		name: 'Staisy',
		profession: 'da',
		number: '832',
		email: 'dsfsafdsf@sf.ru',
		password: '43534',
	},
];

export const Users = createSlice({
	name: 'users',
	initialState,
	reducers: {},
});

export const { actions, reducer } = Users;
