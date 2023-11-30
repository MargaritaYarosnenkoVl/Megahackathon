import { BrowserRouter, Route, Routes } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import { routes } from './routes.data';

const Router = () => {
	const { isAuth } = useAuth();

	return (
		<BrowserRouter>
			<Routes>
				{routes.map(route => {
					if (route.isAuth && !isAuth) return false;
						
					return (
						<Route
							key={route.path}
							element={<route.component />}
							path={route.path}
						/>
					);
				})}
			</Routes>
		</BrowserRouter>
	);
};

export default Router;
