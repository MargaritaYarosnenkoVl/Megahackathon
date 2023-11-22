import { $axios } from '../../../api';
import { useCheckToken } from '../../../hooks/useCheckToken';

const Home = () => {
	useCheckToken();
	const test = async () => {
		try {
			const responce = await $axios.get('https://212.20.45.230:8004/users/me');
			console.log(await responce);
		} catch (error) {
			console.log(error);
		}
	};

	return (
		<div>
			Home
			<button onClick={test}>test</button>
		</div>
	);
};

export default Home;
