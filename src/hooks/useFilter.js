import { useContext } from 'react';
import { FilterContext } from '../providers/FilterProvider';

export const useFilter = () => useContext(FilterContext);
