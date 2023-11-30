import { createContext, useState } from 'react';

export const ResultNewsContext = createContext();

const ResultNewsProvider = ({ children }) => {
	const [request, setRequest] = useState();

	return (
		<ResultNewsContext.Provider value={{ request, setRequest }}>
			{children}
		</ResultNewsContext.Provider>
	);
};

export default ResultNewsProvider;
