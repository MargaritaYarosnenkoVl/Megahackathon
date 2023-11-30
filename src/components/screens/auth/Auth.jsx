import { useAuthPage } from '../../../hooks/useAuthPage';
import Layout from '../../layout/Layout';
import Button from '../../ui/button/Button';
import styles from './Auth.module.scss';


const Auth = () => {
	const { onSubmit, register, handleSubmit, errors } = useAuthPage();

	return (
		<Layout bgImage='./images/auth.jpg' justifyContent='center'>
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
		</Layout>
	);
};

export default Auth;
