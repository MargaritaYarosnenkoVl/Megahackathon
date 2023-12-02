import React, { useState } from "react";
import styles from './AddNewUser.module.scss';
import Layout from "../../layout/Layout";
import Header from "../../header/Header";
import Content from "../../content/Content";
import LeftPanel from "../../left-panel/LeftPanel";
import { Link } from "react-router-dom";
import { useUser } from "../../../hooks/useUser";
import Cookies from "js-cookie";
import { TOKEN } from "../../../app.constants";
import { $axios } from "../../../api";
import { useNavigate } from "react-router-dom";


const AddNewUser = () => {
	const [username, setUsername] = useState();
	const [full_name, setFullName] = useState();
	const [email, setEmail] = useState();
	const [phone_number, setPhoneNumber] = useState();
	const [password, setPassword] = useState();
	const [role, setRole] = useState();
	const token = Cookies.get(TOKEN);
	const navigate = useNavigate();

	// const requestOptions = {
	// 	headers: { 
	// 		"Content-Type": "application/json",
	// 		// 'Authorization': 'Bearer ' + token,
	// 	},
	// 	data: JSON.stringify({
	// 		email: email,
	// 		full_name: full_name,
	// 		is_active: true,
	// 		is_superuser: false,
	// 		is_verified: false,
	// 		password: password,
	// 		phone_number: phone_number,
	// 		role_name: "user",
	// 		username: username,
	// 	}),
	// };

	const addUser = async () => {

		try {
			const response = await $axios.post(
				'https://212.20.45.230:8004/auth/register',
				{
					email: {email},
					full_name: {full_name},
					is_active: true,
					is_superuser: false,
					is_verified: false,
					password: {password},
					phone_number: {phone_number},
					role_name: "user",
					username: {username},
				}
			);
			console.log(response);
		} catch (error) {
			console.log(error);
		}
	};


	const addHandler = () => {
		addUser();
		navigate('/home/personalArea/adminPanel');
	};

    return (
        <Layout justifyContent='space-between'>
			<Header />
			<Content>
				<LeftPanel />
				<div className={styles.wrapper}>
                    <div className={styles.block__adduser}>
                        <div className={styles.block__navigation}>
                            <Link to={'/home'}>Главная</Link>
                            <p>/</p>
                            <Link to={'/home/personalArea'}>Личный кабинет</Link>
                            <p>/</p>
                            <p>Пользователи</p>
                        </div>
						<div className={styles.text}>
							<p>ДОБАВЛЕНИЕ НОВОВГО ПОЛЬЗОВАТЕЛЯ</p>
						</div>
						<div className={styles.inputs}>
							<div className={styles.input}>
								<p>Логин</p>
								<input
									autoFocus
									type='text'
									placeholder='Логин'
									onChange={event => {setUsername(event.target.value)}}
								/>
							</div>
							<div className={styles.input}>
								<p>ФИО</p>
								<input
									autoFocus
									type='text'
									placeholder='ФИО'
									onChange={event => {setFullName(event.target.value)}}
								/>
							</div>
							<div className={styles.input}>
								<p>E-MAIL</p>
								<input
									autoFocus
									type='text'
									placeholder='E-MAIL'
									onChange={event => {setEmail(event.target.value)}}
								/>
							</div>
							<div className={styles.input}>
								<p>Должность</p>
								<input
									autoFocus
									// className={styles.h2}
									type='text'
									placeholder='Должность'
									// onClick={() => setIsViewName(!isViewName)}
									// onChange={event =>
									//     dispatch(
									//         interActions.interlayerUserInfo({
									//             name: event.target.value,
									//         })
									//     )
									// }
									// value={props.user.role_name}
								/>
							</div>
							<div className={styles.input}>
								<p>Номер телефона</p>
								<input
									autoFocus
									// className={styles.h2}
									type='text'
									placeholder='Номер телефона'
									onChange={event => {setPhoneNumber(event.target.value)}}
								/>
							</div>
							<div className={styles.input}>
								<p>Пароль</p>
								<input
									autoFocus
									// className={styles.h2}
									type='text'
									placeholder='Пароль'
									onChange={event => {setPassword(event.target.value)}}
								/>
							</div>
						</div>
						<div className={styles.button}>
							<button className={styles.button_save} onClick={addHandler}>
									Сохранить
							</button>
						</div>
					</div>
				</div>	
			</Content>
		</Layout>
    );
};

export default AddNewUser;