import React from 'react';
import ReactDOM from 'react-dom/client';
import { Provider } from 'react-redux';
import './assets/styles/global.scss';
import AuthProvider from './providers/AuthProvider.jsx';
import FilterProvider from './providers/FilterProvider.jsx';
import ResultNewsProvider from './providers/ResultNewsProvider.jsx';
import Router from './routes/Router.jsx';
import { store } from './store/store.js';

ReactDOM.createRoot(document.getElementById('root')).render(
	<React.StrictMode>
		<AuthProvider>
			<Provider store={store}>
				<FilterProvider>
					<ResultNewsProvider>
						<Router />
					</ResultNewsProvider>
				</FilterProvider>
			</Provider>
		</AuthProvider>
	</React.StrictMode>
);
