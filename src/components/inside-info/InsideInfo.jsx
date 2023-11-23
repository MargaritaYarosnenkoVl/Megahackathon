import { useState } from 'react';
import { Link } from 'react-router-dom';
import Button from '../ui/button/Button';
import styles from './InsideInfo.module.scss';

const InsideInfo = () => {
	const [name, setName] = useState('Иванов Иван Иванович');
	const [prof, setProf] = useState('Директор');
	const [mobile, setMobile] = useState('8-921-951-95-95');
	const [email, setEmail] = useState('tix@yandex.ru');

	const [isViewName, setIsViewName] = useState(false);
	const [isViewProf, setIsViewProf] = useState(false);
	const [isViewMobile, setIsViewMobile] = useState(false);
	const [isViewEmail, setIsViewEmail] = useState(false);

	return (
		<div className={styles.wrapper}>
			<div className={styles.block__image_profile}>
				<div className={styles.block__navigation}>
					<Link to={'/home'}>Главная</Link>
					<p>/</p>
					<p>Личный кабинет</p>
				</div>

				<img
					className={styles.image_profile}
					src='../images/auth.jpg'
					alt='image'
				/>
			</div>

			<div className={styles.block__content}>
				<div className={styles.block__name}>
					{isViewName ? (
						<>
							<input
								autoFocus
								className={styles.h2}
								type='text'
								placeholder='ФИО'
								onClick={() => setIsViewName(!isViewName)}
								onChange={event => setName(event.target.value)}
								value={name}
							/>
						</>
					) : (
						<>
							<h2 onClick={() => setIsViewName(!isViewName)}>{name}</h2>
						</>
					)}
					{isViewProf ? (
						<>
							<input
								autoFocus
								className={styles.p}
								type='text'
								placeholder='Должность'
								onClick={() => setIsViewProf(!isViewProf)}
								onChange={event => setProf(event.target.value)}
								value={prof}
							/>
						</>
					) : (
						<>
							<p onClick={() => setIsViewProf(!isViewProf)}>{prof}</p>
						</>
					)}
				</div>
				<div className={styles.block__contact}>
					<div className={styles.mobile}>
						<p>Мобильный телефон</p>
						{isViewMobile ? (
							<input
								autoFocus
								className={styles.p}
								type='text'
								placeholder='Телефон'
								onClick={() => setIsViewMobile(!isViewMobile)}
								onChange={event => setMobile(event.target.value)}
								value={mobile}
							/>
						) : (
							<p onClick={() => setIsViewMobile(!isViewMobile)}>
								8-921-951-95-95
							</p>
						)}
					</div>
					<div className={styles.email}>
						<p>Почта</p>
						{isViewEmail ? (
							<input
								autoFocus
								className={styles.p}
								type='text'
								placeholder='Почта'
								onClick={() => setIsViewEmail(!isViewEmail)}
								onChange={event => setEmail(event.target.value)}
								value={email}
							/>
						) : (
							<p onClick={() => setIsViewEmail(!isViewEmail)}>tix@yandex.ru</p>
						)}
					</div>
				</div>
				<div className={styles.block__password}>
					<label htmlFor='main'>Смена пароля</label>
					<input className={styles.main_pass} type='password' id='main' />
				</div>
				<div className={styles.block__password}>
					<label htmlFor='repeat'>Повторить новый пароль</label>
					<input className={styles.second_pass} type='password' id='repeat' />
				</div>
				<Button saveInfo='saveInfo'>сохранить</Button>
			</div>
		</div>
	);
};

export default InsideInfo;
