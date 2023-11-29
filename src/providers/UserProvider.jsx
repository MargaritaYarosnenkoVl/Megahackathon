import Cookies from 'js-cookie';
import { createContext, useState } from 'react';
import { TOKEN } from '../app.constants';
import { $axios } from '../api';


export const UserContext = createContext();

const UserProvider = ({ children }) => {
	const [infoUser, setInfoUser] = useState();
    const token = Cookies.get(TOKEN);

	const get_user = async () => {
		const requestOptions = {
			headers: { 
                "Content-Type": "application/x-www-form-urlencoded",
                'Authorization': 'Bearer ' + token,
			},
		};
		try {
			const responce = await $axios.get('https://212.20.45.230:8004/users/me', requestOptions);
			console.log(responce.data);
            setInfoUser(responce.data)
		} catch (error) {
			console.log(error);
		}
	};

	return (
		<UserContext.Provider value={{ infoUser, setInfoUser, token, get_user }}>
			{children}
		</UserContext.Provider>
	);
};

export default UserProvider;
