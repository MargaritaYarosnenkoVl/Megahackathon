import { useAuthPage } from '../../../hooks/useAuthPage';
import Button from '../../ui/button/Button';
import styles from './Auth.module.scss';

const Auth = () => {
	const { onSubmit, register, handleSubmit, getValues, errors } = useAuthPage();

	return (
		<div className={styles.wrapper}>
			<div className={styles.auth}>
				<img
					className={styles.image_auth}
					src='./images/icons/userAuth.svg'
					alt='user'
				/>
				<form onSubmit={handleSubmit(onSubmit)}>
					<div className={styles.input_block}>
						<input
							{...register('email', {
								required: true,
								pattern: {
									value:
										/^([a-z0-9_-]+\.)*[a-z0-9_-]+@[a-z0-9_-]+(\.[a-z0-9_-]+)*\.[a-z]{2,6}$/,
								},
							})}
							type='text'
							placeholder='E-mail'
						/>
						{errors.email && <span>Введите email</span>}
					</div>

					<div className={styles.input_block}>
						<input
							{...register('password', { required: true })}
							type='password'
							placeholder='Password'
						/>
						{errors.password && <span>Введите пароль</span>}
					</div>

					<Button>Вход</Button>
				</form>
			</div>
		</div>
	);
};

export default Auth;
