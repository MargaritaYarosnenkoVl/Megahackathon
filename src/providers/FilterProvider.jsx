import { createContext, useState } from 'react';

export const FilterContext = createContext();

const FilterProvider = ({ children }) => {
	const [isViewFilter, setIsViewFilter] = useState(false);

	return (
		<FilterContext.Provider value={{ isViewFilter, setIsViewFilter }}>
			{children}
		</FilterContext.Provider>
	);
};

export default FilterProvider;
