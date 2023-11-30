import React from 'react';
import ReactDOM from 'react-dom/client';
import { Provider } from 'react-redux';
import './assets/styles/global.scss';
import AuthProvider from './providers/AuthProvider.jsx';
import UserProvider from './providers/UserProvider.jsx';
import Router from './routes/Router.jsx';
import { store } from './store/store.js';
import UsersProvider from './providers/UsersProvider.jsx';

ReactDOM.createRoot(document.getElementById('root')).render(
	<React.StrictMode>
		<AuthProvider>
			<UserProvider>
				<UsersProvider>
					<Provider store={store}>
						<Router />
					</Provider>
				</UsersProvider>
			</UserProvider>
		</AuthProvider>
	</React.StrictMode>
);
