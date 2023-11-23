import { useEffect, useRef } from 'react';
import { useLocation } from 'react-router-dom';

export const useCheckPath = () => {
	const userRef = useRef(null);
	const user_activeRef = useRef(null);
	const userBlockRef = useRef(null);
	const { pathname } = useLocation();

	useEffect(() => {
		if (pathname === '/home/personalArea') {
			userRef.current.style.display = 'none';
			user_activeRef.current.style.display = 'block';
			userBlockRef.current.style.color = 'white';
			userBlockRef.current.style.backgroundColor = 'rgba(0, 83, 154, 1)';
		}
	}, [pathname]);

	return {
		userRef,
		user_activeRef,
		userBlockRef,
	};
};
