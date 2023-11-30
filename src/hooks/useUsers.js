import { useContext } from 'react';
import { UsersContext } from '../providers/UsersProvider';

export const useUsers = () => useContext(UsersContext);
