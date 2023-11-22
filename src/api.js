import axios from 'axios';
import Cookies from 'js-cookie';
import { TOKEN } from './app.constants';

const API_URL = 'https://212.20.45.230:8004';

const token = Cookies.get(TOKEN);

export const $axios = axios.create({
	baseURL: API_URL,
	headers: {
		'Content-Type': 'application/x-www-form-urlencoded',
		// Authorization: `Bearer ${token}`,
	},
});

$axios.interceptors.request.use(
	config => {
		const token = Cookies.get(TOKEN);
		if (token) {
			config.headers.Authorization = `Bearer ${token}`;
		}
		return config;
	},
	error => {
		return Promise.reject(error);
	}
);
