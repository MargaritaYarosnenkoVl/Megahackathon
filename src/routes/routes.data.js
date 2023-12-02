import AddNewUser from '../components/screens/add-newuser/AddNewUser';
import Auth from '../components/screens/auth/Auth';
import Favorite from '../components/screens/favorite/Favorite';
import History from '../components/screens/history/History';
import Home from '../components/screens/home/Home';
import LaterRead from '../components/screens/later-read/LaterRead';
import PersonalArea from '../components/screens/personal-area/PersonalArea';
import UserList from '../components/screens/users-list/UserList';

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
		path: '/home/personalArea',
		component: PersonalArea,
		isAuth: true,
	},
	{
		path: '/home/personalArea/adminPanel',
		component: UserList,
		isAuth: true,
	},
	{
		path: '/home/personalArea/adminPanel/addNewUser',
		component: AddNewUser,
		isAuth: true,
	},
	{
		path: '/home/history',
		component: History,
		isAuth: true,
	},
	{
		path: '/home/favorite',
		component: Favorite,
		isAuth: true,
	},
	{
		path: '/home/laterRead',
		component: LaterRead,
		isAuth: true,
	},
];
