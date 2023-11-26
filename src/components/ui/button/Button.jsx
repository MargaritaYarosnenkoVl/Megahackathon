import { useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../../hooks/useAuth';
import { useInfoUser } from '../../../hooks/useInfoUser';
import { actions } from '../../../store/users/Users.slice';
import styles from './Button.module.scss';

const Button = ({
	children,
	saveInfo,
	editingNews,
	getValues,
	setIsEditNews,
	setIsViewEditNews,
	mainPassword,
	secondPassword,
}) => {
	const navigate = useNavigate();

	const { isAuth } = useAuth();

	const { dispatch, name, prof, mobile, email, repeatPassword } = useInfoUser();

	const userInterlayer = useSelector(state => state.interlayer[0]);

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
						console.log(
							'mainPassword',
							mainPassword,
							': secondPassword',
							secondPassword
						);
						console.log(repeatPassword(mainPassword, secondPassword));
						setTest(true);
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
