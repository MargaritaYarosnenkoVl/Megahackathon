import Cookies from 'js-cookie';
import { createContext, useState } from 'react';
import { TOKEN } from '../app.constants';
import { $axios } from '../api';


export const UsersContext = createContext();

const UsersProvider = ({ children }) => {
	const [infoUsers, setInfoUsers] = useState();
    const token = Cookies.get(TOKEN);

	const get_users = async () => {
		const requestOptions = {
			headers: { 
                "Content-Type": "application/x-www-form-urlencoded",
                'Authorization': 'Bearer ' + token,
			},
		};
		try {
			const responce = await $axios.get('https://212.20.45.230:8004/auth/get_all_users', requestOptions);
            setInfoUsers(responce.data);
            console.log(responce.data);
		} catch (error) {
			console.log(error);
		}
	};

	return (
		<UsersContext.Provider value={{ infoUsers, setInfoUsers, get_users }}>
			{children}
		</UsersContext.Provider>
	);
};

export default UsersProvider;
