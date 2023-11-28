import { createSlice } from '@reduxjs/toolkit';

const initialState = [
	{
		id: 0,
		name: 'Staisy',
		profession: 'da',
		number: '832',
		email: 'dsfsafdsf@sf.ru',
		password: {
			old: '43534',
			new: 'sdf',
		},
		urlImage: null,
	},
];

export const interlayer = createSlice({
	name: 'interlayer',
	initialState,
	reducers: {
		interlayerUserInfo: (state, { payload }) => {
			state[0] = { ...state[0], ...payload };
		},
		interlayerUserPassword: (state, { payload }) => {
			state[0].password = { ...state[0].password, ...payload };
		},
	},
});

export const { actions, reducer } = interlayer;
