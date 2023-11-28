import Cookies from 'js-cookie';
import { $axios } from '../api';
import { TOKEN } from '../app.constants';

export const authService = {
	main: async (email, password, setIsAuth) => {
		try {
			const { data } = await $axios.post(
				'https://212.20.45.230:8004/auth/jwt/login',
				`grant_type=&username=${email}&password=${password}&scope=&client_id=&client_secret=`
			);

			console.log(data);
			if (data.access_token) {
				Cookies.set(TOKEN, data.access_token);
				setIsAuth(true);
			}
		} catch (error) {
			console.log(error);
		}
	},
};
