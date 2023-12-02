import { createContext, useState } from 'react';

export const ResultNewsContext = createContext();

const ResultNewsProvider = ({ children }) => {
	const [request, setRequest] = useState();
	const [responseNews, setResponseNews] = useState();

	return (
		<ResultNewsContext.Provider value={{ request, setRequest, responseNews, setResponseNews }}>
			{children}
		</ResultNewsContext.Provider>
	);
};

export default ResultNewsProvider;
