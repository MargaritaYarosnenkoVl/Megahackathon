import { useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../../hooks/useAuth';
import { useInfoUser } from '../../../hooks/useInfoUser';
import { useUsers } from '../../../hooks/useUsers';
import { actions } from '../../../store/users/Users.slice';
import styles from './Button.module.scss';

const Button = ({
	children,
	saveInfo,
	editingNews,
	getValues,
	setIsEditNews,
	setIsViewEditNews,
	secondPassword,
	result,
}) => {
	const navigate = useNavigate();

	const { isAuth } = useAuth();
	const { get_users } = useUsers();

	const { dispatch, repeatPassword } = useInfoUser();

	const userInterlayer = useSelector(state => state.interlayer[0]);

	const usersHandler = () => {
		get_users();
		navigate('/home/personalArea/adminPanel');
	};

	return (
		<>
			{saveInfo === 'saveInfo' ? (
				<button
					className={styles.button_save}
					onClick={() => {
						const userData = {
							name: userInterlayer.name,
							profession: userInterlayer.profession,
							number: userInterlayer.number,
							email: userInterlayer.email,
							password: repeatPassword(
								userInterlayer.password.new,
								secondPassword
							)
								? userInterlayer.password.new
								: userInterlayer.password.old,
						};
						dispatch(actions.editUserInfo(userData));
					}}
				>
					{children}
				</button>
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
			) : saveInfo === 'search' ? (
				<button className={styles.button}>{children}</button>
			) : saveInfo === 'filter-start' ? (
				<button className={styles.button} type='submit'>
					{children}
				</button>
			) : saveInfo === 'users' ? (
				<button
					className={styles.button_save}
					onClick={() =>
						isAuth ? navigate('/home/personalArea/adminPanel') : ''
					}
				>
					{children}
				</button>
			) : saveInfo === 'add_user' ? (
				<button
					className={styles.button_save}
					onClick={() => (isAuth ? navigate('/home/personalArea/adminPanel/addNewUser') : '')}
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
