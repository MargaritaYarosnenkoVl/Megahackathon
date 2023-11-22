import Auth from '../components/screens/auth/Auth';
import Home from '../components/screens/home/Home';
import PersonalArea from '../components/screens/personal-area/PersonalArea';

export const routes = [
	{
		path: '/home',
		component: Home,
		isAuth: true,
	},
	{
		path: '/',
		component: Auth,
		isAuth: false,
	},
	{
		path: '/personalArea',
		component: PersonalArea,
		isAuth: true,
	},
];
