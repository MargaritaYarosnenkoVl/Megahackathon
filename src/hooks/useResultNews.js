import { useContext } from 'react';
import { ResultNewsContext } from '../providers/ResultNewsProvider';

export const useResultNews = () => useContext(ResultNewsContext);
