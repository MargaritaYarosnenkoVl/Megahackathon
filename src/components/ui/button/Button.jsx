import { useDispatch } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../../hooks/useAuth';
import { actions } from '../../../store/users/Users.slice';
import styles from './Button.module.scss';

const Button = ({
	children,
	saveInfo,
	editingNews,
	getValues,
	setIsEditNews,
	setIsViewEditNews,
}) => {
	const navigate = useNavigate();

	const { isAuth } = useAuth();

	const dispatch = useDispatch();

	return (
		<>
			{saveInfo === 'saveInfo' ? (
				<button className={styles.button_save}>{children}</button>
			) : saveInfo === 'saveEdit' ? (
				<button
					className={styles.button}
					onClick={() => {
						dispatch(
							actions.addEditingNews({
								id: editingNews.id,
								title: getValues('title'),
								description: getValues('description'),
								date: getValues('date'),
								source: getValues('source'),
								teg: getValues('teg'),
								comments: getValues('comments'),
							})
						);
						setIsEditNews(false);
						setIsViewEditNews(false);
					}}
				>
					{children}
				</button>
			) : saveInfo === 'no-saveEdit' ? ( //TODO: СДЕЛАТЬ ЧТОБЫ ВОЗВРАЩАЛО ЗНАЧЕНИЕ ПРИ ОТКРЫТИИ НОВОСТИ НАПРИМЕР ПРИ ОТКРЫТИИ СОХРАНЯТЬ В РЕДАКС А ПОТОМ ПРИ ОТМЕНЕ ЗАБИРАТЬ ОБРАТНО
				<button
					className={styles.button}
					onClick={() => {
						if (setIsEditNews) setIsEditNews(false);
						setIsViewEditNews(false);
					}}
				>
					{children}
				</button>
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
