import { useEffect, useRef } from 'react';
import { useLocation } from 'react-router-dom';

export const useCheckPath = () => {
	const userRef = useRef(null);
	const user_activeRef = useRef(null);
	const userBlockRef = useRef(null);

	const historyRef = useRef(null);
	const historyRef_active = useRef(null);
	const historyBlockRef = useRef(null);

	const favoriteRef = useRef(null);
	const favoriteRef_active = useRef(null);
	const favoriteBlockRef = useRef(null);

	const laterRef = useRef(null);
	const laterRef_active = useRef(null);
	const laterBlockRef = useRef(null);

	const { pathname } = useLocation();

	useEffect(() => {
		if (pathname === '/home/personalArea') {
			userRef.current.style.display = 'none';
			user_activeRef.current.style.display = 'block';
			userBlockRef.current.style.color = 'white';
			userBlockRef.current.style.backgroundColor = 'rgba(0, 83, 154, 1)';
		} else if (pathname === '/home/history') {
			historyRef.current.style.display = 'none';
			historyRef_active.current.style.display = 'block';
			historyBlockRef.current.style.color = 'white';
			historyBlockRef.current.style.backgroundColor = 'rgba(0, 83, 154, 1)';
		} else if (pathname === '/home/favorite') {
			favoriteRef.current.style.display = 'none';
			favoriteRef_active.current.style.display = 'block';
			favoriteBlockRef.current.style.color = 'white';
			favoriteBlockRef.current.style.backgroundColor = 'rgba(0, 83, 154, 1)';
		} else if (pathname === '/home/laterRead') {
			laterRef.current.style.display = 'none';
			laterRef_active.current.style.display = 'block';
			laterBlockRef.current.style.color = 'white';
			laterBlockRef.current.style.backgroundColor = 'rgba(0, 83, 154, 1)';
		}
	}, [pathname]);

	return {
		userRef,
		user_activeRef,
		userBlockRef,
		historyRef_active,
		historyRef,
		historyBlockRef,
		favoriteBlockRef,
		favoriteRef,
		favoriteRef_active,
		laterRef,
		laterRef_active,
		laterBlockRef,
	};
};
