import React from "react";
import styles from './ChangeUser.module.scss';
import { useState } from "react";


const ChangeUser = (props) => {
    const [username, setUsername] = useState();
	const [full_name, setFullName] = useState();
	const [email, setEmail] = useState();
	const [phone_number, setPhoneNumber] = useState();
	const [password, setPassword] = useState();

    const changeHandler = () => {
        props.setChangeModalActive(false);
        console.log(`Данные пользователя ${props.user.username} изменены.`);
    };

    return (
        <>
            <div className={styles.modal__text}>
                    <p>Пользователь {props.user.username}</p>
            </div>
            <div className={styles.modal__input}>
                <p>Логин</p>
                <input
                    autoFocus
                    // className={styles.h2}
                    type='text'
                    placeholder='Логин'
                    onChange={event => {setUsername(event.target.value)}}
                    defaultValue={props.user.username}
                />
            </div>
            <div className={styles.modal__input}>
                <p>ФИО</p>
                <input
                    autoFocus
                    // className={styles.h2}
                    type='text'
                    placeholder='ФИО'
                    onChange={event => {setFullName(event.target.value)}}
                    defaultValue={props.user.full_name}
                />
            </div>
            <div className={styles.modal__input}>
                <p>E-MAIL</p>
                <input
                    autoFocus
                    // className={styles.h2}
                    type='text'
                    placeholder='E-MAIL'
                    onChange={event => {setEmail(event.target.value)}}
                    defaultValue={props.user.email}
                />
            </div>
            <div className={styles.modal__input}>
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
                    defaultValue={props.user.role_name}
                />
            </div>
            <div className={styles.modal__input}>
                <p>Номер телефона</p>
                <input
                    autoFocus
                    // className={styles.h2}
                    type='text'
                    placeholder='Номер телефона'
                    onChange={event => {setPhoneNumber(event.target.value)}}
                    defaultValue={props.user.phone_number}
                />
            </div>
            <div className={styles.modal__input}>
                <p>Пароль</p>
                <input
                    autoFocus
                    // className={styles.h2}
                    type='text'
                    placeholder='Пароль'
                    onChange={event => {setPassword(event.target.value)}}
                    // defaultValue={props.user.phone_number}
                />
            </div>
            <div className={styles.modal__buttons}>
                <button onClick={changeHandler}>
                        Сохранить
                </button>
            </div>
        </> 
    );
};

export default ChangeUser;