import Cookies from 'js-cookie';
import { useNavigate } from 'react-router-dom';
import { TOKEN } from '../../app.constants';
import { useAuth } from '../../hooks/useAuth';
import { useCheckPath } from '../../hooks/useCheckPath';
import styles from './LeftPanel.module.scss';
import { useUser } from '../../hooks/useUser';

const LeftPanel = () => {
	const navigate = useNavigate();
	const { setIsAuth } = useAuth();
	const { get_user, infoUser, setInfoUser } = useUser();

	const {
		userRef,
		user_activeRef,
		userBlockRef,
		historyBlockRef,
		historyRef,
		historyRef_active,
		favoriteBlockRef,
		favoriteRef,
		favoriteRef_active,
		laterRef,
		laterRef_active,
		laterBlockRef,
	} = useCheckPath();

	const logoutHandler = () => {
		Cookies.remove(TOKEN);
		setIsAuth(false);
		setInfoUser();
		navigate('/');
	};

	return (
		<div className={styles.wrapper}>
			<div className={styles.block_one}>
				<button
					ref={userBlockRef}
					className={styles.block_param}
					onClick={() => navigate('/home/personalArea')}
				>
					<img
						ref={userRef}
						className={styles.user}
						src='../../../images/icons/user.svg'
						alt='img'
					/>
					<img
						ref={user_activeRef}
						className={styles.user_active}
						src='../../../images/icons/user_white.svg'
						alt='img'
					/>
					<p>Личный кабинет</p>
				</button>
				<button className={styles.block_param}>
					<img
						className={styles.settings}
						src='../../../images/icons/settings.svg'
						alt='img'
					/>
					<img
						className={styles.settings_active}
						src='../../../images/icons/settings_white.svg'
						alt='img'
					/>
					<p>Настройки просмотра</p>
				</button>
			</div>
			<div className={styles.block_two}>
				<button
					ref={laterBlockRef}
					className={styles.block_param}
					onClick={() => navigate('/home/laterRead')}
				>
					<img
						ref={laterRef}
						className={styles.bookmark}
						src='../../../images/icons/bookmark.svg'
						alt='img'
					/>
					<img
						ref={laterRef_active}
						className={styles.bookmark_active}
						src='../../../images/icons/bookmark_white.svg'
						alt='img'
					/>
					<p>Читать потом</p>
				</button>
				<button
					className={styles.block_param}
					onClick={() => navigate('/home/favorite')}
					ref={favoriteBlockRef}
				>
					<img
						ref={favoriteRef}
						className={styles.blackStar}
						src='../../../images/icons/foulder_black.svg'
						alt='img'
					/>
					<img
						ref={favoriteRef_active}
						className={styles.blackStar_active}
						src='../../../images/icons/foulder_white.svg'
						alt='img'
					/>
					<p>Мои папки</p>
					{/* <img
						ref={favoriteRef}
						className={styles.blackStar}
						src='../../../images/icons/black_star.svg'
						alt='img'
					/>
					<img
						ref={favoriteRef_active}
						className={styles.blackStar_active}
						src='../../../images/icons/favorite_active_white.svg'
						alt='img'
					/>
					<p>Избранное</p> */}
				</button>
				{/* <button className={styles.block_param}>
					<img
						className={styles.foulder}
						src='../../../images/icons/foulder_black.svg'
						alt='img'
					/>
					<img
						className={styles.foulder_active}
						src='../../../images/icons/foulder_white.svg'
						alt='img'
					/>
					<p>Мои папки</p>
				</button> */}
				<button
					ref={historyBlockRef}
					className={styles.block_param}
					onClick={() => navigate('/home/history')}
				>
					<img
						ref={historyRef}
						className={styles.history}
						src='../../../images/icons/history.svg'
						alt='img'
					/>
					<img
						ref={historyRef_active}
						className={styles.history_active}
						src='../../../images/icons/history_white.svg'
						alt='img'
					/>
					<p>История просмотра</p>
				</button>
			</div>
			<button className={styles.block_param} onClick={logoutHandler}>
				<img
					className={styles.logout}
					src='../../../images/icons/logout.svg'
					alt='img'
				/>
				<img
					className={styles.logout_active}
					src='../../../images/icons/logout_white.svg'
					alt='img'
				/>
				<p>Выход</p>
			</button>
		</div>
	);
};

export default LeftPanel;
