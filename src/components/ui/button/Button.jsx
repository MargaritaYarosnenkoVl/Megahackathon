import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../../hooks/useAuth';
import styles from './Button.module.scss';

const Button = ({ children, saveInfo }) => {
	const navigate = useNavigate();

	const { isAuth } = useAuth();

	return (
		<>
			{saveInfo === 'saveInfo' ? (
				<button className={styles.button_save}>{children}</button>
			) : (
				<button
					className={styles.button}
					onClick={() => (isAuth ? navigate('/home') : '')}
				>
					{children}
				</button>
			)}
		</>
	);
};

export default Button;
